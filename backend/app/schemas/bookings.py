from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BookingStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    COUNTERED = "countered"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class BookingCreate(BaseModel):
    client_id: str
    freelancer_id: str
    start_time: datetime
    end_time: datetime
    service: str
    price: float


class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    price: Optional[float] = None
    status: Optional[BookingStatus] = None


class BookingResponse(BaseModel):
    id: str
    client_id: str
    freelancer_id: str
    start_time: datetime
    end_time: datetime
    service: str
    price: float
    status: BookingStatus

    class Config:
        from_attributes = True


class CalendarEvent(BaseModel):
    id: str
    freelancer_id: str
    start_time: datetime
    end_time: datetime
    is_available: bool

    class Config:
        from_attributes = True


class Availability(BaseModel):
    start_time: datetime
    end_time: datetime
