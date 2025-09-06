from datetime import date
from typing import List

from app.schemas.analytics import (
    ActivityFeedResponse,
    IncomeTrendResponse,
    ProjectionsResponse,
    RevenueReportResponse,
)
from app.services import analytics as analytics_service
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/activity/{user_id}", response_model=ActivityFeedResponse)
async def get_user_activity(user_id: str):
    """
    Retrieves the activity feed for a specific user, containing a mix of
    transactions and booking events in reverse chronological order.
    """
    activity_items = await analytics_service.get_activity_feed(user_id)
    return ActivityFeedResponse(items=activity_items)


@router.get("/projections/{user_id}", response_model=ProjectionsResponse)
async def get_revenue_projections(user_id: str):
    """
    Gets projected revenue from confirmed future bookings.
    """
    projections = await analytics_service.get_revenue_projections(user_id)
    return ProjectionsResponse(**projections)


@router.get("/income-trend/{user_id}", response_model=IncomeTrendResponse)
async def get_income_trend(
    user_id: str,
    start_date: date,
    end_date: date,
):
    """
    Gets income and expense trends over a specified date range.
    """
    trend_data = await analytics_service.get_income_trend(user_id, start_date, end_date)
    return IncomeTrendResponse(trend=trend_data)


@router.get("/revenue-report/{user_id}", response_model=RevenueReportResponse)
async def get_revenue_report(
    user_id: str,
    breakdown_by: str = Query("service", enum=["service", "client"]),
):
    """
    Gets a revenue report broken down by service or client.
    """
    report_data = await analytics_service.get_revenue_report(user_id, breakdown_by)
    return RevenueReportResponse(breakdown_by=breakdown_by, data=report_data)


@router.get("/export/financial-report/{user_id}")
async def export_financial_report(user_id: str):
    """
    Generates and returns a CSV file of the user's financial history.
    """
    csv_file = await analytics_service.generate_financial_report_csv(user_id)
    response = StreamingResponse(iter([csv_file.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = (
        "attachment; filename=financial_report.csv"
    )
    return response
