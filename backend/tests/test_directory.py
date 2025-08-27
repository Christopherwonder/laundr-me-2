import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.crud import db_profiles
from app.schemas.profile import Profile
from app.schemas.directory import FreelancerProfile

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Populate the dummy database before each test
    db_profiles.clear()
    db_profiles[1] = FreelancerProfile(user_id=1, laundr_id="@jane_doe", headline="Software Engineer", skill_tags=["Python", "FastAPI"], rating=4.5, reviews=10)
    db_profiles[2] = FreelancerProfile(user_id=2, laundr_id="@john_smith", headline="Data Scientist", skill_tags=["Python", "PyTorch"], rating=4.8, reviews=25)
    db_profiles[3] = Profile(user_id=3, laundr_id="@sam_jones", headline="Product Manager", skill_tags=[])

    yield

    # Teardown: Clean up the dummy database after each test
    db_profiles.clear()

def test_search():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post("/api/v1/directory/search", json={"term": "Python"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 0
    assert len(data["freelancers"]) == 2
    assert data["freelancers"][0]["@laundrID"] == "@jane_doe"

def test_filter_freelancers():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post("/api/v1/directory/freelancers/filter", json={"category": "FastAPI"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["@laundrID"] == "@jane_doe"

def test_sort_freelancers_by_rating():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post("/api/v1/directory/freelancers/sort", json={"sort_by": "rating"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["@laundrID"] == "@john_smith" # 4.8 rating
    assert data[1]["@laundrID"] == "@jane_doe" # 4.5 rating

def test_sort_freelancers_by_ranking_score():
    headers = {"X-Compliance-Token": "test-token"}
    # This test ensures the ranking is deterministic
    response = client.post(
        "/api/v1/directory/freelancers/sort",
        json={
            "sort_by": "score",
            "rating_weight": 2.0,
            "sentiment_weight": 0.5,
            "activity_weight": 1.0,
            "proximity_weight": 0.2,
            "price_weight": 0.1,
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Based on the weights and dummy data, we can predict the order.
    # John Smith has a higher rating, so he should still be first.
    assert data[0]["@laundrID"] == "@john_smith"
    assert data[1]["@laundrID"] == "@jane_doe"
