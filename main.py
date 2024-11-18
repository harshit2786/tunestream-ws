from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json

app = FastAPI()

class NotificationManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, space_id: str, websocket: WebSocket):
        await websocket.accept()
        if space_id not in self.active_connections:
            self.active_connections[space_id] = []
        self.active_connections[space_id].append(websocket)

    def disconnect(self, space_id: str, websocket: WebSocket):
        self.active_connections[space_id].remove(websocket)
        if not self.active_connections[space_id]:
            del self.active_connections[space_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, space_id: str, message: dict):
        if space_id in self.active_connections:
            message_str = json.dumps(message)
            for connection in self.active_connections[space_id]:
                await connection.send_text(message_str)

notification_manager = NotificationManager()

@app.websocket("/spaceclients/{space_id}")
async def websocket_endpoint(websocket: WebSocket, space_id: str):
    await notification_manager.connect(space_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "broadcast":
                await notification_manager.broadcast(space_id, {"command" : "fetch"})
    except WebSocketDisconnect:
        notification_manager.disconnect(space_id, websocket)
