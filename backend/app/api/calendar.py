from typing import List

from app.schemas.bookings import Availability, CalendarEvent
from app.services import calendar as calendar_service
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/availability", response_model=List[Availability])
async def get_availability(freelancer_id: str):
    return calendar_service.get_availability(freelancer_id)


@router.post("/events", response_model=CalendarEvent)
async def create_event(event: CalendarEvent):
    return calendar_service.create_event(event)


@router.put("/events/{event_id}", response_model=CalendarEvent)
async def update_event(event_id: str, event: CalendarEvent):
    updated_event = calendar_service.update_event(event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event


@router.delete("/events/{event_id}", status_code=204)
async def delete_event(event_id: str):
    if not calendar_service.delete_event(event_id):
        raise HTTPException(status_code=404, detail="Event not found")
    return
