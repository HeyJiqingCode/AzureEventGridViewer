import pytest
from pytest import fixture
from unittest.mock import AsyncMock, Mock
from app.core.event_manager import EventManager

@pytest.fixture
def event_manager():
    return EventManager()

@pytest.fixture
def mock_websocket():
    websocket = AsyncMock()
    websocket.send_json = AsyncMock()
    websocket.receive_text = AsyncMock()
    websocket.close = AsyncMock()
    return websocket

@pytest.mark.asyncio
async def test_connect(event_manager, mock_websocket):
    await event_manager.connect(mock_websocket)
    assert mock_websocket in event_manager.active_connections
    mock_websocket.accept.assert_called_once()

@pytest.mark.asyncio
async def test_disconnect(event_manager, mock_websocket):
    await event_manager.connect(mock_websocket)
    await event_manager.disconnect(mock_websocket)
    assert mock_websocket not in event_manager.active_connections

@pytest.mark.asyncio
async def test_broadcast_event(event_manager, mock_websocket):
    await event_manager.connect(mock_websocket)
    test_event = {"id": "test", "data": "test_data"}
    await event_manager.broadcast_event(test_event)
    mock_websocket.send_json.assert_called_once_with(test_event)

@pytest.mark.asyncio
async def test_max_events_limit(event_manager):
    for i in range(event_manager.max_events + 10):
        await event_manager.broadcast_event({"id": str(i)})
    assert len(event_manager.events) == event_manager.max_events
    assert event_manager.events[0]["id"] == "10"  # 最老的事件应该被移除