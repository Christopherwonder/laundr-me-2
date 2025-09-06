import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.bookings import BookingStatus
from app.services.bookings import bookings_db
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Clear and repopulate the dummy database before each test."""
    bookings_db.clear()
    yield
    bookings_db.clear()

# --- Test Data ---
booking_payload = {
    "client_id": "client1",
    "freelancer_id": "freelancer1",
    "start_time": "2025-10-01T10:00:00",
    "end_time": "2025-10-01T11:00:00",
    "service": "Deep Cleaning",
    "price": 100.0,
}

# --- Comprehensive Tests ---

@patch('app.api.bookings.redis_service.reserve_slot', return_value=True)
@patch('app.api.bookings.bookings_service.send_load', new_callable=AsyncMock)
def test_full_negotiation_flow_happy_path(mock_send_load, mock_reserve_slot):
    """
    Tests the entire negotiation loop:
    1. Client creates a booking request.
    2. Freelancer counters with a new price.
    3. Client approves the counter-offer.
    """
    # 1. Client creates booking request
    response = client.post("/api/v1/bookings/", json=booking_payload)
    assert response.status_code == 200
    booking_data = response.json()
    booking_id = booking_data["id"]
    assert booking_data["status"] == BookingStatus.PENDING
    assert booking_data["price"] == 100.0

    # 2. Freelancer counters the request
    counter_payload = {"price": 120.0}
    response = client.post(f"/api/v1/bookings/{booking_id}/counter", json=counter_payload)
    assert response.status_code == 200
    booking_data = response.json()
    assert booking_data["status"] == BookingStatus.COUNTERED
    assert booking_data["price"] == 120.0

    # 3. Client approves the counter-offer
    response = client.post(f"/api/v1/bookings/{booking_id}/approve")
    assert response.status_code == 200
    booking_data = response.json()
    assert booking_data["status"] == BookingStatus.APPROVED

    # Verify that the deposit was sent
    mock_send_load.assert_called_once()
    load_create_arg = mock_send_load.call_args[0][0]
    assert load_create_arg.sender_id == "client1"
    assert load_create_arg.recipient_id == "freelancer1"
    assert load_create_arg.amount == 120.0 * 0.2  # 20% of the countered price

@patch('app.api.bookings.redis_service.reserve_slot', return_value=True)
def test_decline_flow(mock_reserve_slot):
    """
    Tests the flow where a booking is declined by the freelancer.
    """
    # 1. Client creates booking request
    response = client.post("/api/v1/bookings/", json=booking_payload)
    assert response.status_code == 200
    booking_id = response.json()["id"]

    # 2. Freelancer declines the request
    response = client.post(f"/api/v1/bookings/{booking_id}/decline")
    assert response.status_code == 200
    assert response.json()["status"] == BookingStatus.DECLINED

def test_create_booking_slot_already_reserved():
    """
    Tests that a booking cannot be created for a time slot that is already reserved.
    """
    with patch('app.api.bookings.redis_service.reserve_slot', return_value=False) as mock_reserve_slot:
        response = client.post("/api/v1/bookings/", json=booking_payload)
        assert response.status_code == 409
        assert "Time slot is currently reserved" in response.json()["detail"]
        mock_reserve_slot.assert_called_once()

@patch('app.api.bookings.redis_service.reserve_slot', return_value=True)
def test_approve_non_existent_booking(mock_reserve_slot):
    """
    Tests that approving a non-existent booking returns a 404 error.
    """
    response = client.post("/api/v1/bookings/non-existent-id/approve")
    assert response.status_code == 404
