import json
from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session

from database import engine
from security import verify_token

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

def unregister_connection(websocket: WebSocket):
    username = connections.pop(websocket, None)
    if username:
        users.pop(username, None)
        game_positions.pop(username, None)
        pending_challenges.pop(username, None)
    return username

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
                        opponent_name = next(
                            p for p in battle["players"]
                            if p != user.username
                        )

                        player = battle["players"][user.username]
                        opponent = battle["players"][opponent_name]

                        await websocket.send_text(json.dumps({
                            "type": "battle:resume",
                            "payload": {
                                "player": player,
                                "opponent": opponent,
                            }
                        }))
                        if opponent_name in users:
                            await users[opponent_name].send_text(json.dumps({
                                "type": "battle:resume",
                                "payload": {
                                    "player": battle["players"][opponent_name],
                                    "opponent": battle["players"][user.username],
                                }
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
                except Exception as e:
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
                    battle = {
                        "players": {
                            attacker: {
                                "username": attacker,
                                "hp": 10000,
                                "score": 100,
                                "attackProgress": 0,
                            },
                            sender: {
                                "username": sender,
                                "hp": 10000,
                                "score": 1,
                                "attackProgress": 0,
                            },
                        },
                        "paused": False,
                        "started": True,
                    }

                    active_battles[attacker] = battle
                    active_battles[sender] = battle

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