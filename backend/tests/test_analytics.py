from datetime import datetime, timedelta, timezone

import pytest
from app.main import app
from app.schemas.bookings import BookingResponse, BookingStatus
from app.services.astra import transactions_db
from app.services.bookings import bookings_db
from fastapi.testclient import TestClient

client = TestClient(app)

# --- Test Data ---

USER_ID = "user1"
FREELANCER_ID = "freelancer1"
CLIENT_ID = "client1"


def setup_test_data():
    """Clear and repopulate the dummy databases with a consistent dataset."""
    bookings_db.clear()
    transactions_db.clear()

    # Past, confirmed booking for freelancer (revenue)
    bookings_db["booking1"] = BookingResponse(
        id="booking1",
        client_id=CLIENT_ID,
        freelancer_id=FREELANCER_ID,
        start_time=datetime(2023, 7, 1, 10, 0, 0),
        end_time=datetime(2023, 7, 1, 11, 0, 0),
        service="Consulting",
        price=150.0,
        status=BookingStatus.CONFIRMED,
    )
    # Future, confirmed booking for freelancer (projection)
    bookings_db["booking2"] = BookingResponse(
        id="booking2",
        client_id=CLIENT_ID,
        freelancer_id=FREELANCER_ID,
        start_time=datetime.now(timezone.utc) + timedelta(days=10),
        end_time=datetime.now(timezone.utc) + timedelta(days=10, hours=1),
        service="Workshop",
        price=500.0,
        status=BookingStatus.CONFIRMED,
    )
    # Past, confirmed booking for client (expense)
    bookings_db["booking3"] = BookingResponse(
        id="booking3",
        client_id=USER_ID,
        freelancer_id=FREELANCER_ID,
        start_time=datetime(2023, 7, 2, 10, 0, 0),
        end_time=datetime(2023, 7, 2, 11, 0, 0),
        service="Data Analysis",
        price=300.0,
        status=BookingStatus.CONFIRMED,
    )

    # Received load (income)
    transactions_db.append(
        {
            "action": "send_load",
            "details": {
                "transaction_id": "tx1",
                "sender_id": "other_user",
                "recipient_id": USER_ID,
                "amount": 75.0,
            },
            "timestamp": datetime(2023, 7, 5, 12, 0, 0),
            "status": "completed",
        }
    )
    # Sent load (expense)
    transactions_db.append(
        {
            "action": "send_load",
            "details": {
                "transaction_id": "tx2",
                "sender_id": USER_ID,
                "recipient_id": "other_user",
                "amount": 50.0,
            },
            "timestamp": datetime(2023, 7, 6, 12, 0, 0),
            "status": "completed",
        }
    )


# --- Pytest Fixture ---


@pytest.fixture(autouse=True)
def setup():
    """Setup test data before each test."""
    setup_test_data()


# --- Test Cases ---


def test_get_activity_feed():
    """
    Tests that the activity feed returns a sorted list of all user activities.
    """
    response = client.get(f"/api/v1/analytics/activity/{USER_ID}")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]

    assert len(items) == 3  # booking3, tx1, tx2
    assert items[0]["id"] == "tx2"  # Most recent
    assert items[1]["id"] == "tx1"
    assert items[2]["id"] == "booking3"
    assert items[0]["description"] == "Sent load to other_user"


def test_get_revenue_projections():
    """
    Tests the revenue projection calculation for a freelancer.
    """
    response = client.get(f"/api/v1/analytics/projections/{FREELANCER_ID}")
    assert response.status_code == 200
    data = response.json()

    assert data["projected_revenue"] == 500.0
    assert data["from_booking_count"] == 1


def test_get_income_trend():
    """
    Tests the income trend aggregation over a specific date range.
    """
    start_date = "2023-07-01"
    end_date = "2023-07-31"
    response = client.get(
        f"/api/v1/analytics/income-trend/{USER_ID}?start_date={start_date}&end_date={end_date}"
    )
    assert response.status_code == 200
    data = response.json()["trend"]

    # Find the specific data points to verify
    day2_data = next((d for d in data if d["date"] == "2023-07-02"), None)
    day5_data = next((d for d in data if d["date"] == "2023-07-05"), None)
    day6_data = next((d for d in data if d["date"] == "2023-07-06"), None)

    assert day2_data is not None
    assert day2_data["expenses"] == 300.0
    assert day2_data["income"] == 0

    assert day5_data is not None
    assert day5_data["income"] == 75.0
    assert day5_data["expenses"] == 0

    assert day6_data is not None
    assert day6_data["expenses"] == 50.0
    assert day6_data["income"] == 0


def test_get_revenue_report():
    """
    Tests the revenue report generation for a freelancer, broken down by client.
    """
    response = client.get(
        f"/api/v1/analytics/revenue-report/{FREELANCER_ID}?breakdown_by=client"
    )
    assert response.status_code == 200
    data = response.json()

    assert data["breakdown_by"] == "client"
    # The freelancer has two past clients in the test data
    assert len(data["data"]) == 2

    # Sort by category to ensure consistent order for assertions
    sorted_data = sorted(data["data"], key=lambda x: x["category"])

    assert sorted_data[0]["category"] == CLIENT_ID
    assert sorted_data[0]["total_revenue"] == 150.0
    assert sorted_data[0]["transaction_count"] == 1

    assert sorted_data[1]["category"] == USER_ID
    assert sorted_data[1]["total_revenue"] == 300.0
    assert sorted_data[1]["transaction_count"] == 1


def test_financial_report_csv_export():
    """
    Tests that the financial report is generated in the correct CSV format.
    """
    response = client.get(f"/api/v1/analytics/export/financial-report/{USER_ID}")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]  # More robust check
    assert (
        "attachment; filename=financial_report.csv"
        in response.headers["content-disposition"]
    )

    content = response.text
    # Basic check for header and some expected content
    assert "Date,Description,Income,Expense,Category" in content
    assert "Data Analysis" in content
    assert "300.0" in content
    assert "Load received" in content
    assert "75.0" in content
    assert "Load sent" in content
    assert "50.0" in content
