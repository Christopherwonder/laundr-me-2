import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.bookings import BookingStatus
from unittest.mock import patch, AsyncMock


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_create_booking_slot_available(client):
    with patch('app.api.bookings.redis_service.reserve_slot', return_value=True), \
         patch('app.api.bookings.bookings_service.create_booking', new_callable=AsyncMock) as mock_create_booking:

        mock_create_booking.return_value = {
            "id": "123",
            "client_id": "client1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-01T09:00:00",
            "end_time": "2025-09-01T10:00:00",
            "service": "cleaning",
            "price": 50.0,
            "status": BookingStatus.PENDING,
        }
        response = client.post("/api/v1/bookings/", json={
            "client_id": "client1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-01T09:00:00",
            "end_time": "2025-09-01T10:00:00",
            "service": "cleaning",
            "price": 50.0,
        })
        assert response.status_code == 200
        assert response.json()["status"] == BookingStatus.PENDING


@pytest.mark.asyncio
async def test_create_booking_slot_reserved(client):
    with patch('app.api.bookings.redis_service.reserve_slot', return_value=False):
        response = client.post("/api/v1/bookings/", json={
            "client_id": "client1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-01T09:00:00",
            "end_time": "2025-09-01T10:00:00",
            "service": "cleaning",
            "price": 50.0,
        })
        assert response.status_code == 409


@pytest.mark.asyncio
async def test_approve_booking(client):
    with patch('app.api.bookings.bookings_service.approve_booking', new_callable=AsyncMock) as mock_approve_booking:
        mock_approve_booking.return_value = {
            "id": "123",
            "client_id": "client1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-01T09:00:00",
            "end_time": "2025-09-01T10:00:00",
            "service": "cleaning",
            "price": 50.0,
            "status": BookingStatus.APPROVED
        }
        response = client.post("/api/v1/bookings/123/approve")
        assert response.status_code == 200
        assert response.json()["status"] == BookingStatus.APPROVED


@pytest.mark.asyncio
async def test_decline_booking(client):
    with patch('app.api.bookings.bookings_service.decline_booking', new_callable=AsyncMock) as mock_decline_booking:
        mock_decline_booking.return_value = {
            "id": "123",
            "client_id": "client1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-01T09:00:00",
            "end_time": "2025-09-01T10:00:00",
            "service": "cleaning",
            "price": 50.0,
            "status": BookingStatus.DECLINED
        }
        response = client.post("/api/v1/bookings/123/decline")
        assert response.status_code == 200
        assert response.json()["status"] == BookingStatus.DECLINED


@pytest.mark.asyncio
async def test_counter_booking(client):
    with patch('app.api.bookings.bookings_service.counter_booking', new_callable=AsyncMock) as mock_counter_booking:
        mock_counter_booking.return_value = {
            "id": "123",
            "client_id": "client1",
            "freelancer_id": "freelancer1",
            "start_time": "2025-09-01T09:00:00",
            "end_time": "2025-09-01T10:00:00",
            "service": "cleaning",
            "price": 60.0,
            "status": BookingStatus.COUNTERED,
        }
        response = client.post("/api/v1/bookings/123/counter", json={"price": 60.0})
        assert response.status_code == 200
        assert response.json()["status"] == BookingStatus.COUNTERED
        assert response.json()["price"] == 60.0
