from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.setdefault("default_user", []).append(websocket)

    def disconnect(self, websocket: WebSocket):
        for user_id in self.connections:
            if websocket in self.connections[user_id]:
                break
            self.connections[user_id].remove(websocket)
            if not self.connections[user_id]:
                del self.connections[user_id]

    async def send_to_user(self, user_id: str, data: dict):
        for ws in self.connections.get(user_id, []):
            await ws.send_json(data)

manager = ConnectionManager()