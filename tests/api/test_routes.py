import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_subscription_validation(client):
    validation_code = "1234567890"
    response = client.post(
        "/api/events",
        headers={"aeg-event-type": "SubscriptionValidation"},
        json=[{
            "data": {"validationCode": validation_code}
        }]
    )
    assert response.status_code == 200
    assert response.json() == {"validationResponse": validation_code}

def test_receive_event(client):
    event = {
        "id": "test-event",
        "subject": "test-subject",
        "eventType": "test.event",
        "data": {"key": "value"},
        "eventTime": "2025-03-24T10:00:00Z"
    }
    response = client.post("/api/events", json=event)
    assert response.status_code == 200

def test_receive_multiple_events(client):
    events = [
        {
            "id": f"test-event-{i}",
            "subject": f"test-subject-{i}",
            "eventType": "test.event",
            "data": {"key": f"value-{i}"},
            "eventTime": "2025-03-24T10:00:00Z"
        }
        for i in range(3)
    ]
    response = client.post("/api/events", json=events)
    assert response.status_code == 200

def test_clear_events(client):
    """测试清除所有事件的API接口"""
    response = client.post("/api/events/clear")
    assert response.status_code == 200