from datetime import datetime
import pytest
from app.models.event import GridEvent, CloudEvent

def test_grid_event_creation():
    event_data = {
        "id": "123",
        "subject": "test-subject",
        "event_type": "test.event",
        "data": {"key": "value"},
        "event_time": datetime.now(),
        "topic": "test-topic"
    }
    event = GridEvent(**event_data)
    assert event.id == "123"
    assert event.subject == "test-subject"
    assert event.event_type == "test.event"
    assert event.data == {"key": "value"}
    assert event.topic == "test-topic"

def test_cloud_event_creation():
    event_data = {
        "id": "456",
        "source": "test-source",
        "type": "test.event",
        "data": {"key": "value"},
        "time": datetime.now(),
        "specversion": "1.0",
        "subject": "test-subject"
    }
    event = CloudEvent(**event_data)
    assert event.id == "456"
    assert event.source == "test-source"
    assert event.type == "test.event"
    assert event.data == {"key": "value"}
    assert event.subject == "test-subject"
    assert event.specversion == "1.0"