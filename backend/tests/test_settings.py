import pytest
from app.crud import db_profiles, db_settings
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_dbs():
    db_profiles.clear()
    db_settings.clear()
    yield


def test_get_settings():
    # Create a profile first
    response = client.post(
        "/api/v1/profiles/", json={"@laundrID": "settings_user", "bio": "test bio"}
    )
    user_id = response.json()["user_id"]

    response = client.get(f"/api/v1/settings/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["biometric_enabled"] == False
    assert data["spending_limit"] == 1000.0


def test_update_settings_unverified():
    # Create a profile first
    response = client.post(
        "/api/v1/profiles/",
        json={"@laundrID": "unverified_user_settings", "bio": "test bio"},
    )
    user_id = response.json()["user_id"]

    response = client.put(f"/api/v1/settings/{user_id}", json={"spending_limit": 500})
    assert response.status_code == 403


def test_update_settings_verified():
    # Create a profile first
    response = client.post(
        "/api/v1/profiles/",
        json={"@laundrID": "verified_user_settings", "bio": "test bio"},
    )
    user_id = response.json()["user_id"]

    # Manually update the KYC status to "verified" in the dummy DB
    db_profiles[user_id].kyc_status = "verified"

    response = client.put(f"/api/v1/settings/{user_id}", json={"spending_limit": 500})
    assert response.status_code == 200
    data = response.json()
    assert data["spending_limit"] == 500
