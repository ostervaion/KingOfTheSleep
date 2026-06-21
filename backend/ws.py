import json
from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session

from database import engine
from security import verify_token

connections: dict[WebSocket, str] = {}
users: dict[str, WebSocket] = {}


def unregister_connection(websocket: WebSocket):
    username = connections.pop(websocket, None)
    if username:
        users.pop(username, None)


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            if data["type"] == "auth":
                with Session(engine) as session:
                    user = verify_token(data["token"], session)
                connections[websocket] = user.username
                users[user.username] = websocket
                await websocket.send_text("authenticated")

            elif data["type"] == "message":
                sender = connections.get(websocket)
                target = data["to"]
                if sender and target in users:
                    payload = {"from": sender, "text": data["text"]}
                    await users[target].send_text(json.dumps(payload))
                    await websocket.send_text(json.dumps(payload))
                else:
                    await websocket.send_text("user not connected")
    except WebSocketDisconnect:
        unregister_connection(websocket)
    except Exception:
        await websocket.close(code=1008)
        unregister_connection(websocket)
