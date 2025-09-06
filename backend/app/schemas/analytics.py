from datetime import date, datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class ActivityType(str, Enum):
    BOOKING = "booking"
    LOAD = "load"
    SWAP = "swap"
    REQUEST = "request"


class ActivityItem(BaseModel):
    id: str
    type: ActivityType
    timestamp: datetime
    description: str
    amount: float
    status: str  # A common status field across all activities


class ActivityFeedResponse(BaseModel):
    items: List[ActivityItem]


# Schemas for Analytics Endpoints


class RevenueByCategory(BaseModel):
    category: str
    total_revenue: float
    transaction_count: int


class RevenueReportResponse(BaseModel):
    breakdown_by: str
    data: List[RevenueByCategory]


class TrendDataPoint(BaseModel):
    date: date
    income: float
    expenses: float
    net_income: float


class IncomeTrendResponse(BaseModel):
    trend: List[TrendDataPoint]


class ProjectionsResponse(BaseModel):
    projected_revenue: float
    from_booking_count: int
