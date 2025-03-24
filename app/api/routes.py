from fastapi import APIRouter, WebSocket, Request, Response
from ..core.event_manager import EventManager
from ..models.event import GridEvent, CloudEvent

router = APIRouter()
event_manager = EventManager()

@router.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/api/events")
async def receive_event(request: Request):
    # Handle event grid subscription validation
    if request.headers.get("aeg-event-type") == "SubscriptionValidation":
        data = await request.json()
        validation_code = data[0]["data"]["validationCode"]
        return {"validationResponse": validation_code}
    
    # Handle actual events
    events = await request.json()
    if not isinstance(events, list):
        events = [events]
    
    for event in events:
        # Broadcast event to all connected clients
        await event_manager.broadcast_event(event)
    
    return Response(status_code=200)

@router.post("/api/events/clear")
async def clear_events():
    await event_manager.clear_events()
    return Response(status_code=200)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await event_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
    except:
        await event_manager.disconnect(websocket)