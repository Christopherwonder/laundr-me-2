import uuid
from datetime import datetime
from typing import List

from app.schemas.bookings import Availability, CalendarEvent

# In-memory database for demonstration purposes
calendar_db = {}


def get_availability(freelancer_id: str) -> List[Availability]:
    """Returns a list of available time slots for a freelancer."""
    # This is a placeholder implementation.
    # In a real application, this would query the database for the freelancer's schedule.
    return [
        Availability(
            start_time=datetime(2025, 9, 1, 9, 0), end_time=datetime(2025, 9, 1, 11, 0)
        ),
        Availability(
            start_time=datetime(2025, 9, 1, 14, 0), end_time=datetime(2025, 9, 1, 17, 0)
        ),
    ]


def create_event(event: CalendarEvent) -> CalendarEvent:
    """Creates a new calendar event."""
    event_id = str(uuid.uuid4())
    event_data = event.model_dump()
    event_data.pop("id", None)  # Remove client-sent ID if it exists
    new_event = CalendarEvent(id=event_id, **event_data)
    calendar_db[event_id] = new_event
    return new_event


def update_event(event_id: str, event_update: CalendarEvent) -> CalendarEvent:
    """Updates an existing calendar event."""
    event = calendar_db.get(event_id)
    if not event:
        return None

    update_data = event_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)

    return event


def delete_event(event_id: str):
    """Deletes a calendar event."""
    if event_id in calendar_db:
        del calendar_db[event_id]
        return True
    return False
