import json
from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session

from database import engine
from security import verify_token

# Diccionarios globales para rastrear las conexiones
connections: dict[WebSocket, str] = {}  # websocket -> username
users: dict[str, WebSocket] = {}        # username -> websocket
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
    return username



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

            elif msg_type == "chat:global":
                text = data.get("text")
                if not text:
                    continue

                await broadcast_chat_global(sender, text)

            elif msg_type.startswith("game:"):
                pass

    except WebSocketDisconnect:
        username = unregister_connection(websocket)
        if username:
            await broadcast_presence(username, False)
    except Exception:
        await websocket.close(code=1008)
        unregister_connection(websocket)