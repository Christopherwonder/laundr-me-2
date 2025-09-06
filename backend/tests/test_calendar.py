import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.calendar import calendar_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Clear the dummy database before each test."""
    calendar_db.clear()
    yield
    calendar_db.clear()

# --- Test Data ---
event_payload = {
    "id": "placeholder-id",
    "freelancer_id": "freelancer1",
    "start_time": "2025-11-01T10:00:00",
    "end_time": "2025-11-01T12:00:00",
    "is_available": False,
}

# --- Comprehensive Tests ---

def test_create_and_get_event():
    """
    Tests creating a new calendar event and ensures it's stored correctly.
    """
    # Create the event
    response = client.post("/api/v1/calendar/events", json=event_payload)
    assert response.status_code == 200
    created_event = response.json()
    event_id = created_event["id"]

    # Verify the event is in the database (via the service layer)
    assert event_id in calendar_db
    assert calendar_db[event_id].freelancer_id == "freelancer1"

def test_update_event():
    """
    Tests updating an existing calendar event.
    """
    # First, create an event
    response = client.post("/api/v1/calendar/events", json=event_payload)
    assert response.status_code == 200
    created_event = response.json()
    event_id = created_event["id"]

    # Now, update it
    update_payload = {
        "freelancer_id": "freelancer1",
        "start_time": "2025-11-01T10:00:00",
        "end_time": "2025-11-01T12:00:00",
        "is_available": True,
        "id": event_id,
    }
    response = client.put(f"/api/v1/calendar/events/{event_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["is_available"] is True

    # Verify the update in the database
    assert calendar_db[event_id].is_available is True

def test_delete_event():
    """
    Tests deleting an existing calendar event.
    """
    # First, create an event
    response = client.post("/api/v1/calendar/events", json=event_payload)
    assert response.status_code == 200
    event_id = response.json()["id"]

    # Now, delete it
    response = client.delete(f"/api/v1/calendar/events/{event_id}")
    assert response.status_code == 204

    # Verify it's gone from the database
    assert event_id not in calendar_db

def test_update_non_existent_event():
    """
    Tests that updating a non-existent event returns a 404 error.
    """
    update_payload = {
        "freelancer_id": "freelancer1",
        "start_time": "2025-11-01T10:00:00",
        "end_time": "2025-11-01T12:00:00",
        "is_available": True,
        "id": "non-existent-id",
    }
    response = client.put("/api/v1/calendar/events/non-existent-id", json=update_payload)
    assert response.status_code == 404

def test_delete_non_existent_event():
    """
    Tests that deleting a non-existent event returns a 404 error.
    """
    response = client.delete("/api/v1/calendar/events/non-existent-id")
    assert response.status_code == 404
