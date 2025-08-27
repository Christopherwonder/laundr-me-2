from fastapi import APIRouter, Depends, HTTPException
from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta

from app.schemas.loads import LoadCreate, LoadResponse, SwapFunds, AstraRoutineCreate
from app.services import astra
from app.utils import calculate_fees
from app.crud import db_profiles, get_profile_by_laundr_id

router = APIRouter()

# In a real app, this should be loaded from a secure config
SECRET_KEY = "a_very_secret_key_for_invites"
invite_serializer = URLSafeTimedSerializer(SECRET_KEY)


# Dummy audit log
def audit_log(action: str, details: dict):
    astra.log_transaction(action, details)


@router.post("/send-load", response_model=LoadResponse)
async def send_load(load: LoadCreate):
    # 1. Check if sender exists
    sender_profile = await get_profile_by_laundr_id(load.sender_id)
    if not sender_profile:
        raise HTTPException(status_code=404, detail=f"Sender with laundr_id {load.sender_id} not found")

    # 2. Calculate fees
    total_fee, sender_fee, recipient_fee = calculate_fees(load.amount)
    net_amount = load.amount - total_fee

    # 3. Check if recipient is on the platform
    recipient_profile = await get_profile_by_laundr_id(load.recipient_id)
    invite_link = None
    if not recipient_profile:
        # Off-platform user, generate invite link
        token = invite_serializer.dumps(load.recipient_id, salt="invite-salt")
        invite_link = f"https://laundr.me/claim?token={token}"
        message = "Load sent to an off-platform user. They will be invited to join."
    else:
        message = "Load sent successfully to on-platform user."

    # 4. Call Astra service to create routine
    astra_routine_data = AstraRoutineCreate(
        type="send",
        amount=load.amount,
        source_id=load.sender_id,
        destination_id=load.recipient_id
    )
    routine = await astra.create_routine(astra_routine_data)

    # 5. Log the transaction
    audit_log(
        "send_load",
        {
            "transaction_id": routine.id,
            "sender_id": load.sender_id,
            "recipient_id": load.recipient_id,
            "amount": load.amount,
            "fee": total_fee,
        },
    )

    # 6. Return response
    return LoadResponse(
        transaction_id=routine.id,
        status=routine.status,
        sender_fee=sender_fee,
        recipient_fee=recipient_fee,
        total_fee=total_fee,
        net_amount=net_amount,
        message=message,
        invite_link=invite_link,
    )

@router.post("/request-load", response_model=LoadResponse)
async def request_load(load: LoadCreate):
    # In a request, the sender is the one being asked for money,
    # and the recipient is the one making the request.

    # 1. Check if both users exist on the platform
    sender_profile = await get_profile_by_laundr_id(load.sender_id)
    if not sender_profile:
        raise HTTPException(status_code=404, detail=f"Sender with laundr_id {load.sender_id} not found")

    recipient_profile = await get_profile_by_laundr_id(load.recipient_id)
    if not recipient_profile:
        raise HTTPException(status_code=404, detail=f"Recipient with laundr_id {load.recipient_id} not found")

    # 2. Calculate fees
    total_fee, sender_fee, recipient_fee = calculate_fees(load.amount)
    net_amount = load.amount - total_fee

    # 3. Call Astra service to create routine
    astra_routine_data = AstraRoutineCreate(
        type="request",
        amount=load.amount,
        source_id=load.sender_id, # The person who will send the money
        destination_id=load.recipient_id # The person who will receive the money
    )
    routine = await astra.create_routine(astra_routine_data)

    # 4. Log the transaction
    audit_log(
        "request_load",
        {
            "transaction_id": routine.id,
            "requester_id": load.recipient_id,
            "sender_id": load.sender_id,
            "amount": load.amount,
            "fee": total_fee,
        },
    )

    # 5. Return response
    return LoadResponse(
        transaction_id=routine.id,
        status=routine.status,
        sender_fee=sender_fee,
        recipient_fee=recipient_fee,
        total_fee=total_fee,
        net_amount=net_amount,
        message="Load request created successfully. The sender has been notified.",
    )

@router.post("/swap-funds", response_model=LoadResponse)
async def swap_funds(swap: SwapFunds):
    # 1. Check if both users exist on the platform
    source_profile = await get_profile_by_laundr_id(swap.source_id)
    if not source_profile:
        raise HTTPException(status_code=404, detail=f"Source profile with laundr_id {swap.source_id} not found")

    destination_profile = await get_profile_by_laundr_id(swap.destination_id)
    if not destination_profile:
        raise HTTPException(status_code=404, detail=f"Destination profile with laundr_id {swap.destination_id} not found")

    # 2. Calculate fees
    total_fee, sender_fee, recipient_fee = calculate_fees(swap.amount)
    net_amount = swap.amount - total_fee

    # 3. Call Astra service to create routine
    astra_routine_data = AstraRoutineCreate(
        type="swap",
        amount=swap.amount,
        source_id=swap.source_id,
        destination_id=swap.destination_id
    )
    routine = await astra.create_routine(astra_routine_data)

    # 4. Log the transaction
    audit_log(
        "swap_funds",
        {
            "transaction_id": routine.id,
            "source_id": swap.source_id,
            "destination_id": swap.destination_id,
            "amount": swap.amount,
            "fee": total_fee,
        },
    )

    # 5. Return response
    return LoadResponse(
        transaction_id=routine.id,
        status=routine.status,
        sender_fee=sender_fee,
        recipient_fee=recipient_fee,
        total_fee=total_fee,
        net_amount=net_amount,
        message="Funds swapped successfully.",
    )
