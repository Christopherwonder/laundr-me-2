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


def test_create_profile():
    response = client.post(
        "/api/v1/profiles/", json={"@laundrID": "testuser", "bio": "test bio"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["@laundrID"] == "testuser"
    assert data["bio"] == "test bio"
    assert "user_id" in data
    assert "user_intent_id" in data
    assert data["kyc_status"] == "pending"


def test_create_profile_duplicate_laundrid():
    response = client.post(
        "/api/v1/profiles/", json={"@laundrID": "duplicate", "bio": "test bio"}
    )
    assert response.status_code == 201
    response = client.post(
        "/api/v1/profiles/", json={"@laundrID": "duplicate", "bio": "test bio"}
    )
    assert response.status_code == 400


def test_get_profile():
    response = client.post(
        "/api/v1/profiles/", json={"@laundrID": "getme", "bio": "test bio"}
    )
    user_id = response.json()["user_id"]

    response = client.get(f"/api/v1/profiles/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["@laundrID"] == "getme"


def test_update_profile_unverified():
    response = client.post(
        "/api/v1/profiles/", json={"@laundrID": "unverified_user", "bio": "test bio"}
    )
    user_id = response.json()["user_id"]

    response = client.put(f"/api/v1/profiles/{user_id}", json={"bio": "updated bio"})
    assert response.status_code == 403


def test_update_profile_verified():
    response = client.post(
        "/api/v1/profiles/", json={"@laundrID": "verified_user", "bio": "test bio"}
    )
    user_id = response.json()["user_id"]

    # Manually update the KYC status to "verified" in the dummy DB
    db_profiles[user_id].kyc_status = "verified"

    response = client.put(
        f"/api/v1/profiles/{user_id}", json={"bio": "updated bio for verified user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "updated bio for verified user"
