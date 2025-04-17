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
    assert event_manager.events[0]["id"] == "10"  # 最旧的事件应该被移除

@pytest.mark.asyncio
async def test_clear_events(event_manager, mock_websocket):
    """测试清除所有事件的功能"""
    # 添加一些测试事件
    test_events = [{"id": f"test-{i}"} for i in range(5)]
    for event in test_events:
        await event_manager.broadcast_event(event)
    
    # 确认事件已被添加
    assert len(event_manager.events) == 5
    
    # 添加一个连接
    await event_manager.connect(mock_websocket)
    
    # 清除所有事件
    await event_manager.clear_events()
    
    # 验证事件已被清除
    assert len(event_manager.events) == 0
    
    # 验证通知已发送给客户端
    mock_websocket.send_json.assert_called_with({"type": "clear_events"})