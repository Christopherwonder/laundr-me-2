from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.bookings import BookingCreate, BookingResponse, BookingUpdate
from app.services import bookings as bookings_service
from app.services import redis as redis_service

router = APIRouter()


@router.get("/", response_model=List[BookingResponse])
async def get_all_bookings():
    return await bookings_service.get_all_bookings()


@router.post("/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate):
    slot_key = f"{booking.start_time.isoformat()}-{booking.end_time.isoformat()}"
    if not redis_service.reserve_slot(slot_key, booking.freelancer_id):
        raise HTTPException(status_code=409, detail="Time slot is currently reserved.")

    new_booking = await bookings_service.create_booking(booking)
    if not new_booking:
        redis_service.release_slot(slot_key, booking.freelancer_id)
        raise HTTPException(status_code=400, detail="Booking could not be created.")
    return new_booking


@router.post("/{booking_id}/approve", response_model=BookingResponse)
async def approve_booking(booking_id: str):
    booking = await bookings_service.approve_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/{booking_id}/decline", response_model=BookingResponse)
async def decline_booking(booking_id: str):
    booking = await bookings_service.decline_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/{booking_id}/counter", response_model=BookingResponse)
async def counter_booking(booking_id: str, booking_update: BookingUpdate):
    booking = await bookings_service.counter_booking(booking_id, booking_update)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
