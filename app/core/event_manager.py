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
        # Send existing event history
        await self.send_events_history(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_event(self, event: Dict[str, Any]):
        # Save event
        self.events.append(event)
        if len(self.events) > self.max_events:
            self.events.pop(0)
        
        # Broadcast to all connections
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(event)
            except:
                disconnected.add(connection)
        
        # Clean up disconnected connections
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

    async def clear_events(self):
        self.events.clear()
        # Notify all clients to clear events
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json({"type": "clear_events"})
            except:
                disconnected.add(connection)
        
        # Clean up disconnected connections
        for conn in disconnected:
            await self.disconnect(conn)