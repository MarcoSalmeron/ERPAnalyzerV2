from typing import Dict

from fastapi import WebSocket


# Gestor de conexiones WebSocket para el Orchestration Monitor
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, thread_id: str) -> bool:
        """Register a new socket for ``thread_id``.

        Returns True if the connection was accepted, False otherwise.
        Refuses to overwrite an existing live connection so a second client
        cannot hijack the stream of an in-flight analysis by racing on a
        known thread id.
        """
        if thread_id in self.active_connections:
            # Reject duplicate subscription with a policy-violation close code.
            await websocket.close(code=1008)
            return False
        await websocket.accept()
        self.active_connections[thread_id] = websocket
        return True

    def disconnect(self, thread_id: str):
        if thread_id in self.active_connections:
            del self.active_connections[thread_id]

    async def send_update(self, thread_id: str, message: dict):
        if thread_id in self.active_connections:
            await self.active_connections[thread_id].send_json(message)
        else:
            print(f"⚠️ No hay socket conectado para: {thread_id}")

    async def close_connection(self, thread_id: str):
        if thread_id in self.active_connections:
            websocket = self.active_connections[thread_id]
            await websocket.close(code=1000)
            del self.active_connections[thread_id]
            print(f"🔌 Socket cerrado físicamente para: {thread_id}")


manager = ConnectionManager()