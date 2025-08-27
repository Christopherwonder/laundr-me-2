from app.schemas.bookings import BookingCreate, BookingResponse, BookingUpdate, BookingStatus
from app.api.loads import send_load
from app.schemas.loads import LoadCreate
import uuid

# In-memory database for demonstration purposes
bookings_db = {}


def audit_log(action: str, details: dict):
    """Placeholder for audit logging."""
    print(f"AUDIT: {action} - {details}")


async def create_booking(booking: BookingCreate) -> BookingResponse:
    """Creates a new booking and reserves the time slot."""
    booking_id = str(uuid.uuid4())
    new_booking = BookingResponse(
        id=booking_id,
        status=BookingStatus.PENDING,
        **booking.model_dump()
    )
    bookings_db[booking_id] = new_booking
    audit_log("booking_created", {"booking_id": booking_id})
    return new_booking


async def approve_booking(booking_id: str) -> BookingResponse:
    """Approves a booking and initiates the deposit."""
    booking = bookings_db.get(booking_id)
    if not booking:
        return None  # Or raise HTTPException

    # Initiate deposit
    deposit_load = LoadCreate(
        sender_id=booking.client_id,
        recipient_id=booking.freelancer_id,
        amount=booking.price * 0.2  # 20% deposit
    )
    await send_load(deposit_load)

    booking.status = BookingStatus.APPROVED
    audit_log("booking_approved", {"booking_id": booking_id})
    return booking


async def decline_booking(booking_id: str) -> BookingResponse:
    """Declines a booking."""
    booking = bookings_db.get(booking_id)
    if not booking:
        return None
    booking.status = BookingStatus.DECLINED
    audit_log("booking_declined", {"booking_id": booking_id})
    return booking


async def counter_booking(booking_id: str, booking_update: BookingUpdate) -> BookingResponse:
    """Counters a booking with new terms."""
    booking = bookings_db.get(booking_id)
    if not booking:
        return None

    # Update booking with new terms
    if booking_update.start_time:
        booking.start_time = booking_update.start_time
    if booking_update.end_time:
        booking.end_time = booking_update.end_time
    if booking_update.price:
        booking.price = booking_update.price

    booking.status = BookingStatus.COUNTERED
    audit_log("booking_countered", {"booking_id": booking_id, "update": booking_update.model_dump()})
    return booking


async def get_all_bookings():
    """Returns all bookings."""
    return list(bookings_db.values())
