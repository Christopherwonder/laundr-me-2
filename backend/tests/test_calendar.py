import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    return TestClient(app)


def test_get_availability(client):
    with patch('app.api.calendar.calendar_service.get_availability') as mock_get_availability:
        mock_get_availability.return_value = [
            {"start_time": "2025-09-01T09:00:00", "end_time": "2025-09-01T10:00:00"}
        ]
        response = client.get("/api/v1/calendar/availability?freelancer_id=freelancer1")
        assert response.status_code == 200
        assert len(response.json()) == 1


def test_create_event(client):
    with patch('app.api.calendar.calendar_service.create_event') as mock_create_event:
        mock_create_event.return_value = {
            "id": "event1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-02T10:00:00",
            "end_time": "2025-09-02T11:00:00",
            "is_available": False,
        }
        response = client.post("/api/v1/calendar/events", json={
            "id": "event1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-02T10:00:00",
            "end_time": "2025-09-02T11:00:00",
            "is_available": False,
        })
        assert response.status_code == 200
        assert response.json()["id"] == "event1"


def test_update_event(client):
    with patch('app.api.calendar.calendar_service.update_event') as mock_update_event:
        mock_update_event.return_value = {
            "id": "event1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-02T10:00:00",
            "end_time": "2025-09-02T11:00:00",
            "is_available": True,
        }
        response = client.put("/api/v1/calendar/events/event1", json={
            "id": "event1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-02T10:00:00",
            "end_time": "2025-09-02T11:00:00",
            "is_available": True
        })
        assert response.status_code == 200
        assert response.json()["is_available"] is True


def test_delete_event(client):
    with patch('app.api.calendar.calendar_service.delete_event') as mock_delete_event:
        mock_delete_event.return_value = True
        response = client.delete("/api/v1/calendar/events/event1")
        assert response.status_code == 204
