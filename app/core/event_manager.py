from typing import Set, Dict, Any
import json
from fastapi import WebSocket
from ..models.event import GridEvent, CloudEvent

class EventManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.events: list[Dict[str, Any]] = []
        self.max_events = 100

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        # 发送现有事件历史
        await self.send_events_history(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_event(self, event: Dict[str, Any]):
        # 保存事件
        self.events.append(event)
        if len(self.events) > self.max_events:
            self.events.pop(0)
        
        # 广播到所有连接
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(event)
            except:
                disconnected.add(connection)
        
        # 清理断开的连接
        for conn in disconnected:
            await self.disconnect(conn)

    async def send_events_history(self, websocket: WebSocket):
        for event in self.events:
            try:
                await websocket.send_json(event)
            except:
                await self.disconnect(websocket)
                break

    async def close(self):
        for connection in self.active_connections.copy():
            try:
                await connection.close()
            except:
                pass
        self.active_connections.clear()