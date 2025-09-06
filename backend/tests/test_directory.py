import pytest
from app.crud import db_profiles
from app.main import app
from app.schemas.directory import FreelancerProfile
from app.schemas.profile import Profile
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Clear and repopulate the dummy database before each test."""
    db_profiles.clear()
    db_profiles[1] = FreelancerProfile(
        user_id=1,
        laundr_id="@jane_doe",
        headline="Software Engineer",
        skill_tags=["Python", "FastAPI"],
        rating=4.5,
        reviews=10,
        sentiment_score=0.9,
        activity_score=0.85,
    )
    db_profiles[2] = FreelancerProfile(
        user_id=2,
        laundr_id="@john_smith",
        headline="Data Scientist",
        skill_tags=["Python", "PyTorch"],
        rating=4.8,
        reviews=25,
        sentiment_score=0.95,
        activity_score=0.9,
    )
    db_profiles[3] = Profile(
        user_id=3,
        laundr_id="@sam_jones",
        headline="Product Manager",
        skill_tags=["Agile", "Scrum"],
    )
    db_profiles[4] = FreelancerProfile(
        user_id=4,
        laundr_id="@emily_white",
        headline="UX Designer",
        skill_tags=["Figma", "Sketch"],
        rating=4.9,
        reviews=30,
        sentiment_score=0.98,
        activity_score=0.92,
    )
    db_profiles[5] = Profile(
        user_id=5,
        laundr_id="@chris_green",
        headline="Python Developer",
        skill_tags=["Python"],
    )

    yield

    # Teardown: Clean up the dummy database after each test
    db_profiles.clear()


# --- Search Endpoint Tests ---


def test_search_success():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/search", json={"term": "Python"}, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 1
    assert len(data["freelancers"]) == 2
    assert data["users"][0]["@laundrID"] == "@chris_green"
    freelancer_ids = {f["@laundrID"] for f in data["freelancers"]}
    assert freelancer_ids == {"@jane_doe", "@john_smith"}


def test_search_no_results():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/search", json={"term": "Ruby"}, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 0
    assert len(data["freelancers"]) == 0


def test_search_empty_term():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/search", json={"term": ""}, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    # Should return all profiles
    assert len(data["users"]) == 2
    assert len(data["freelancers"]) == 3


# --- Filter Endpoint Tests ---


def test_filter_freelancers_success():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/freelancers/filter",
        json={"category": "FastAPI"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["@laundrID"] == "@jane_doe"


def test_filter_freelancers_no_results():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/freelancers/filter",
        json={"category": "Django"},
        headers=headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_filter_freelancers_multiple_criteria():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/freelancers/filter",
        json={"category": "Python", "min_rating": 4.6},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["@laundrID"] == "@john_smith"


# --- Sort Endpoint Tests ---


def test_sort_freelancers_by_rating_desc():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/freelancers/sort",
        json={"sort_by": "rating"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert [d["@laundrID"] for d in data] == [
        "@emily_white",
        "@john_smith",
        "@jane_doe",
    ]


def test_sort_freelancers_by_reviews_asc():
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/freelancers/sort",
        json={"sort_by": "reviews"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert [d["@laundrID"] for d in data] == [
        "@jane_doe",
        "@john_smith",
        "@emily_white",
    ]


# --- Ranking Regression Test ---


def test_sort_freelancers_by_ranking_score_deterministic():
    """
    This test ensures the ranking algorithm is deterministic and produces the expected
    output for a fixed set of inputs and weights.
    """
    headers = {"X-Compliance-Token": "test-token"}
    response = client.post(
        "/api/v1/directory/freelancers/sort",
        json={
            "sort_by": "score",
            "rating_weight": 1.5,
            "sentiment_weight": 1.2,
            "activity_weight": 1.0,
            "proximity_weight": 0.0,  # Ignored in this test
            "price_weight": 0.0,  # Ignored in this test
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Expected scores:
    # Emily (4.9, 0.98, 0.92): (4.9*1.5) + (0.98*1.2) + (1.0*0.92) = 7.35 + 1.176 + 0.92 = 9.446
    # John (4.8, 0.95, 0.90):  (4.8*1.5) + (0.95*1.2) + (1.0*0.90) = 7.2 + 1.14 + 0.90 = 9.24
    # Jane (4.5, 0.90, 0.85):  (4.5*1.5) + (0.90*1.2) + (1.0*0.85) = 6.75 + 1.08 + 0.85 = 8.68

    ranked_ids = [d["@laundrID"] for d in data]
    assert ranked_ids == ["@emily_white", "@john_smith", "@jane_doe"]
