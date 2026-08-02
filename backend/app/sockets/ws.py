import json
import time
from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from utils.security import verify_token
from sqlmodel import Session, select

from core.database import engine

# Diccionarios globales para rastrear las conexiones
connections: dict[WebSocket, str] = {}  # websocket -> username
users: dict[str, WebSocket] = {}        # username -> websocket
game_positions: dict[str, tuple[int, int]] = {}
pending_challenges: dict[str, str] = {}  # attacker_username -> target_username (awaiting response)
active_battles: dict[str, dict] = {}
paused_battles: set[str] = set()

async def broadcast_presence(username: str, online: bool):
    payload = json.dumps({
        "type": "presence:update",
        "payload": {"username": username, "online": online}
    })
    for conn in list(connections.keys()):
        try:
            await conn.send_text(payload)
        except Exception:
            pass

async def broadcast_chat_global(sender: str, text: str):
    payload = json.dumps({
        "type": "chat:global",
        "payload": {"from": sender, "text": text}
    })
    for conn in list(connections.keys()):
        try:
            await conn.send_text(payload)
        except Exception:
            pass

async def broadcast_fetch():
    payload = json.dumps({"type": "fetch"})
    for conn in list(connections.keys()):
        try:
            await conn.send_text(payload)
        except Exception:
            pass

def unregister_connection(websocket: WebSocket):
    username = connections.pop(websocket, None)
    if username:
        users.pop(username, None)
        game_positions.pop(username, None)
        pending_challenges.pop(username, None)
    return username


def default_stats() -> dict:
    return {"hp": 600, "attack": 70, "attackSpeed": 1, "defense": 5}

def compute_stats(player_username: str) -> dict:
    from services import getStats
    from models import User
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == player_username)).first()
    print(user.id)
    if user is None:
        return default_stats()

    try:
        stats = getStats(user.id)
    except HTTPException:
        return default_stats()

    return {
        "hp": max(1, round(abs(stats["vitality"]))),
        "attack": abs(stats["attack"]),
        "attackSpeed": max(0.1, abs(stats["speed"])),
        "defense": abs(stats["defense"]),
    }

async def notify_pending_attackers(target_username: str):
    """If someone challenged target_username and is still waiting, tell them it's off."""
    attackers = [atk for atk, tgt in pending_challenges.items() if tgt == target_username]
    for atk in attackers:
        pending_challenges.pop(atk, None)
        if atk in users:
            try:
                await users[atk].send_text(json.dumps({"type": "game:error"}))
            except Exception:
                pass

async def send_to_users(usernames: list[str], payload: dict):
    """Send a message to specific users by username, if they're connected."""
    message = json.dumps(payload)
    for username in usernames:
        ws = users.get(username)
        if ws:
            try:
                await ws.send_text(message)
            except Exception:
                pass

async def broadcast_except(sender_ws: WebSocket, payload: dict):
    """Send a message to all connected users except the sender."""
    message = json.dumps(payload)
    for ws in list(connections.keys()):
        if ws is not sender_ws:
            try:
                await ws.send_text(message)
            except Exception:
                pass


async def broadcast_all(payload: dict):
    """Send a message to all connected users including sender."""
    message = json.dumps(payload)
    for ws in list(connections.keys()):
        try:
            await ws.send_text(message)
        except Exception:
            pass

async def begin_battle(sender, attacker):
    pending_challenges.pop(attacker, None)
    pending_challenges.pop(sender, None)
    attacker_stats = compute_stats(attacker)
    sender_stats = compute_stats(sender)

    battle = {
        "players": {
            attacker: {
                "username": attacker,
                "attackProgress": 0,
                "maxHp": attacker_stats["hp"],
                **attacker_stats,
            },
            sender: {
                "username": sender,
                "attackProgress": 0,
                "maxHp": sender_stats["hp"],
                **sender_stats,
            },
        },
        "paused": False,
        "started": True,
        "last_attack": {},
    }

    active_battles[attacker] = battle
    active_battles[sender] = battle

    await send_to_users([attacker, sender], {
        "type": "battle:init",
        "payload": {"battle": battle["players"]}
    })

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            msg_type = data.get("type")
            if not msg_type:
                await websocket.send_text(json.dumps({
                    "type": "error", 
                    "payload": "Missing message type"
                }))
                continue
            if msg_type == "auth":
                token = data.get("token")
                if not token:
                    await websocket.send_text(json.dumps({
                        "type": "error", 
                        "payload": "Token is required"
                    }))
                    continue

                try:
                    with Session(engine) as session:
                        user = verify_token(token, session)
                    
                    connections[websocket] = user.username
                    users[user.username] = websocket
                    battle = active_battles.get(user.username)

                    if battle:
                        opponent_name = next(p for p in battle["players"] if p != user.username)
                        player = battle["players"][user.username]
                        opponent = battle["players"][opponent_name]

                        await websocket.send_text(json.dumps({
                            "type": "battle:resume",
                            "payload": {"player": player, "opponent": opponent}
                        }))
                    await websocket.send_text(json.dumps({
                        "type": "auth:success",
                        "payload": {"username": user.username}
                    }))
                    await broadcast_presence(user.username, True)

                    await websocket.send_text(json.dumps({
                        "type": "presence:list",
                        "payload": {"online": list(users.keys())}
                    }))
                except Exception:
                    # Si el token es inválido o expiró
                    await websocket.send_text(json.dumps({
                        "type": "auth:fail", 
                        "payload": "Invalid or expired token"
                    }))
                    await websocket.close(code=1008)
                    unregister_connection(websocket)
                    return
                continue
            if msg_type == "get_lobby_players":
                await websocket.send_text(json.dumps({
                        "type": "lobby_list",
                        "payload": {"lobby_players": game_positions}
                }))
                continue

            sender = connections.get(websocket)
            if not sender:
                await websocket.send_text(json.dumps({
                    "type": "error", 
                    "payload": "Not authenticated. Send 'auth' first."
                }))
                continue
            if msg_type == "chat:message":
                target = data.get("to")
                text = data.get("text")
                if not target or not text:
                    continue
                
                payload = {
                    "type": "chat:message",
                    "payload": {
                        "from": sender,
                        "to": target,
                        "text": text
                    }
                }
                if target in users:
                    await users[target].send_text(json.dumps(payload))
                
                await websocket.send_text(json.dumps(payload))
            if msg_type == 'lobby:move':
                game_positions[sender] = (data["x"], data["y"])
                await broadcast_except(websocket, {"type": "sheep_move", "username": sender, "x": data["x"], "y": data["y"]})
                continue

            if msg_type == "chat:global":
                text = data.get("text")
                if not text:
                    continue

                await broadcast_chat_global(sender, text)

            if msg_type == 'game:attack':
                target = data.get("user")
                if not target or target not in users:
                    await websocket.send_text(json.dumps({"type": "game:error"}))
                    continue
                try:
                    await users[target].send_text(json.dumps({
                        "type": "game:game_petition",
                        "payload": {"enemy": sender}
                    }))
                    pending_challenges[sender] = target
                except Exception:
                    await websocket.send_text(json.dumps({"type": "game:error"}))
                continue
            if msg_type == 'game:response':
                attacker = data.get("target")
                accepted = data.get("accepted")

                pending_challenges.pop(attacker, None)

                if accepted:
                    attacker_stats = compute_stats(attacker)
                    sender_stats = compute_stats(sender)

                    battle = {
                        "players": {
                            attacker: {
                                "username": attacker,
                                "attackProgress": 0,
                                "maxHp": attacker_stats["hp"],
                                **attacker_stats,
                            },
                            sender: {
                                "username": sender,
                                "attackProgress": 0,
                                "maxHp": sender_stats["hp"],
                                **sender_stats,
                            },
                        },
                        "paused": False,
                        "started": True,
                        "last_attack": {},
                    }

                    active_battles[attacker] = battle
                    active_battles[sender] = battle

                    await send_to_users([attacker, sender], {
                        "type": "battle:init",
                        "payload": {"battle": battle["players"]}
                    })

                if attacker in users:
                    await users[attacker].send_text(json.dumps({
                        "type": "game:answer",
                        "response": accepted
                    }))

                continue
            if msg_type == 'battle:end':

                battle = active_battles.get(sender)

                if battle:
                    for player in battle["players"]:
                        active_battles.pop(player, None)

                await websocket.send_text(json.dumps({
                    "type":"battle:destroyed"
                }))

                continue
            if msg_type == 'game:disconnect':
                game_positions.pop(sender, None)
                await broadcast_except(websocket, {"type": "game:disconnect", "user": sender})
                continue
            if msg_type == 'game:ready':
                battle = active_battles.get(sender)
                if not battle:
                    continue

                opponent_name = next((p for p in battle["players"] if p != sender), None)

                # only resume once the OTHER player is actually connected
                if opponent_name in users:
                    battle["paused"] = False
                    battle["last_attack"] = {}

                    # tell the reconnecting client it can start
                    await websocket.send_text(json.dumps({"type": "battle:opponent_reconnected"}))
                    # tell the other client too, in case they were paused/waiting
                    await users[opponent_name].send_text(json.dumps({"type": "battle:opponent_reconnected"}))
                continue
            if msg_type == 'game:attack_action':
                target = data.get("target")

                battle = active_battles.get(sender)
                if not battle:
                    continue

                players = battle["players"]

                # El objetivo tiene que ser exactamente el rival real de ESTA batalla
                opponent_of_sender = next((p for p in players if p != sender), None)
                if target != opponent_of_sender:
                    continue

                attacker_stats = players.get(sender)
                target_stats = players.get(target)
                if not attacker_stats or not target_stats:
                    continue

                if attacker_stats["hp"] <= 0 or target_stats["hp"] <= 0:
                    continue

                if battle.get("paused"):
                    print("[DEBUG] attack ignored because battle paused")
                    continue

                # Rate limit: no se puede atacar más rápido de lo que attackSpeed permite
                now = time.monotonic()
                min_interval = 1.0 / attacker_stats["attackSpeed"]
                last = battle.setdefault("last_attack", {}).get(sender, 0)
                if now - last < min_interval * 0.7:  # 30% de tolerancia por jitter de red
                    continue
                battle["last_attack"][sender] = now

                # El daño se calcula SIEMPRE aquí, nunca se confía en lo que manda el cliente
                damage = max(1, round(attacker_stats["attack"] - target_stats["defense"]))
                target_stats["hp"] = max(0, target_stats["hp"] - damage)

                hit_payload = json.dumps({
                    "type": "battle:hit",
                    "payload": {
                        "attacker": sender,
                        "target": target,
                        "damage": damage,
                        "targetHp": target_stats["hp"],
                    }
                })

                # Se lo mandamos a AMBOS jugadores, incluido el propio atacante
                for name in (sender, target):
                    if name in users:
                        try:
                            await users[name].send_text(hit_payload)
                        except Exception:
                            pass

                continue

    except WebSocketDisconnect:
        username = unregister_connection(websocket)

        if username:
            await broadcast_presence(username, False)
            await notify_pending_attackers(username)

            battle = active_battles.get(username)
            if battle:
                battle["paused"] = True

                opponent = next(
                    player for player in battle["players"]
                    if player != username
                )

                if opponent in users:
                    await users[opponent].send_text(json.dumps({
                        "type": "battle:paused"
                    }))
    except Exception:
        username = unregister_connection(websocket)
        if username:
            await notify_pending_attackers(username)
        await websocket.close(code=1008)