import pytest
from app.api.loads import invite_serializer
from app.crud import db_profiles, db_settings
from app.main import app
from app.schemas.profile import Profile
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Fixture to set up the dummy database before each test and clear it after."""
    # Clear previous data
    db_profiles.clear()
    db_settings.clear()

    # Create dummy users
    user1 = Profile(
        user_id=1,
        laundr_id="@user1",
        bio="user 1",
        user_intent_id="ui_1",
        kyc_status="verified",
    )
    user2 = Profile(
        user_id=2,
        laundr_id="@user2",
        bio="user 2",
        user_intent_id="ui_2",
        kyc_status="verified",
    )
    db_profiles[1] = user1
    db_profiles[2] = user2

    yield  # This is where the test runs

    # Teardown: clear the databases
    db_profiles.clear()
    db_settings.clear()


# --- Tests for /send-load ---


def test_send_load_success_on_platform():
    response = client.post(
        "/api/v1/loads/send-load",
        json={"sender_id": "@user1", "recipient_id": "@user2", "amount": 100.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["total_fee"] == 3.74  # (0.03 * 100) + 0.74
    assert data["sender_fee"] == 1.87
    assert data["recipient_fee"] == 1.87
    assert data["net_amount"] == 96.26
    assert data["message"] == "Load sent successfully to on-platform user."
    assert data["invite_link"] is None


def test_send_load_success_off_platform():
    response = client.post(
        "/api/v1/loads/send-load",
        json={"sender_id": "@user1", "recipient_id": "@newuser", "amount": 50.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert (
        data["message"]
        == "Load sent to an off-platform user. They will be invited to join."
    )
    assert data["invite_link"] is not None

    # Verify the token
    token = data["invite_link"].split("=")[-1]
    # In a real test suite, we might use freezegun to test expiration
    # For now, we'll just check that it decodes correctly.
    decoded_id = invite_serializer.loads(
        token, salt="invite-salt", max_age=1800
    )  # 30 minutes
    assert decoded_id == "@newuser"


def test_send_load_minimum_fee():
    response = client.post(
        "/api/v1/loads/send-load",
        json={"sender_id": "@user1", "recipient_id": "@user2", "amount": 10.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_fee"] == 1.50  # max(1.50, (0.03 * 10) + 0.74 = 1.04)
    assert data["sender_fee"] == 0.75
    assert data["recipient_fee"] == 0.75


def test_send_load_below_minimum_amount():
    response = client.post(
        "/api/v1/loads/send-load",
        json={"sender_id": "@user1", "recipient_id": "@user2", "amount": 4.99},
    )
    assert response.status_code == 400
    assert "at least $5.00" in response.json()["detail"]


def test_send_load_sender_not_found():
    response = client.post(
        "/api/v1/loads/send-load",
        json={"sender_id": "@nouser", "recipient_id": "@user2", "amount": 100.0},
    )
    assert response.status_code == 404


# --- Tests for /request-load ---


def test_request_load_success():
    response = client.post(
        "/api/v1/loads/request-load",
        json={"sender_id": "@user1", "recipient_id": "@user2", "amount": 20.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["total_fee"] == 1.50  # max(1.50, (0.03 * 20) + 0.74 = 1.34)
    assert (
        data["message"]
        == "Load request created successfully. The sender has been notified."
    )


def test_request_load_sender_not_found():
    response = client.post(
        "/api/v1/loads/request-load",
        json={"sender_id": "@nouser", "recipient_id": "@user2", "amount": 20.0},
    )
    assert response.status_code == 404


def test_request_load_recipient_not_found():
    response = client.post(
        "/api/v1/loads/request-load",
        json={"sender_id": "@user1", "recipient_id": "@nouser", "amount": 20.0},
    )
    assert response.status_code == 404


def test_request_load_below_minimum_amount():
    response = client.post(
        "/api/v1/loads/request-load",
        json={"sender_id": "@user1", "recipient_id": "@user2", "amount": 1.0},
    )
    assert response.status_code == 400


# --- Tests for /swap-funds ---


def test_swap_funds_success():
    response = client.post(
        "/api/v1/loads/swap-funds",
        json={"source_id": "@user1", "destination_id": "@user2", "amount": 500.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["total_fee"] == 15.74  # (0.03 * 500) + 0.74
    assert data["message"] == "Funds swapped successfully."


def test_swap_funds_source_not_found():
    response = client.post(
        "/api/v1/loads/swap-funds",
        json={"source_id": "@nouser", "destination_id": "@user2", "amount": 500.0},
    )
    assert response.status_code == 404


def test_swap_funds_destination_not_found():
    response = client.post(
        "/api/v1/loads/swap-funds",
        json={"source_id": "@user1", "destination_id": "@nouser", "amount": 500.0},
    )
    assert response.status_code == 404


def test_swap_funds_below_minimum_amount():
    response = client.post(
        "/api/v1/loads/swap-funds",
        json={"source_id": "@user1", "destination_id": "@user2", "amount": 4.99},
    )
    assert response.status_code == 400
    assert "at least $5.00" in response.json()["detail"]
