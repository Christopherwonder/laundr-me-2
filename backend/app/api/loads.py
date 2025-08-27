from fastapi import APIRouter, Depends, HTTPException
from app.schemas.loads import LoadCreate, LoadResponse, SwapFunds, AstraRoutineCreate
from app.services import astra
from app.utils import calculate_fees
from app.crud import db_profiles, get_profile_by_laundr_id

router = APIRouter()

# Dummy audit log
def audit_log(action: str, details: dict):
    print(f"AUDIT: {action} - {details}")

@router.post("/send-load", response_model=LoadResponse)
async def send_load(load: LoadCreate):
    sender_profile = await get_profile_by_laundr_id(load.sender_id)
    if not sender_profile:
        raise HTTPException(status_code=404, detail=f"Sender with laundr_id {load.sender_id} not found")

    total_fee, sender_fee, recipient_fee = calculate_fees(load.amount)
    net_amount = load.amount - total_fee

    recipient_profile = await get_profile_by_laundr_id(load.recipient_id)
    invite_link = None
    if not recipient_profile:
        invite_link = f"https://laundr.me/claim?code=TEMP_{load.recipient_id}"
        message = "Load sent to an off-platform user. They will be invited to join."
    else:
        message = "Load sent successfully to on-platform user."

    astra_routine_data = AstraRoutineCreate(type="send", amount=load.amount, source_id=load.sender_id, destination_id=load.recipient_id)
    routine = await astra.create_routine(astra_routine_data)

    audit_log("send_load", {"transaction_id": routine.id, "sender_id": load.sender_id, "recipient_id": load.recipient_id, "amount": load.amount, "fee": total_fee})

    return LoadResponse(transaction_id=routine.id, status=routine.status, sender_fee=sender_fee, recipient_fee=recipient_fee, total_fee=total_fee, net_amount=net_amount, message=message, invite_link=invite_link)

@router.post("/request-load", response_model=LoadResponse)
async def request_load(load: LoadCreate):
    sender_profile = await get_profile_by_laundr_id(load.sender_id)
    if not sender_profile:
        raise HTTPException(status_code=404, detail=f"Sender with laundr_id {load.sender_id} not found")
    recipient_profile = await get_profile_by_laundr_id(load.recipient_id)
    if not recipient_profile:
        raise HTTPException(status_code=404, detail=f"Recipient with laundr_id {load.recipient_id} not found")

    total_fee, sender_fee, recipient_fee = calculate_fees(load.amount)
    net_amount = load.amount - total_fee

    astra_routine_data = AstraRoutineCreate(type="request", amount=load.amount, source_id=load.sender_id, destination_id=load.recipient_id)
    routine = await astra.create_routine(astra_routine_data)

    audit_log("request_load", {"transaction_id": routine.id, "requester_id": load.recipient_id, "sender_id": load.sender_id, "amount": load.amount, "fee": total_fee})

    return LoadResponse(transaction_id=routine.id, status=routine.status, sender_fee=sender_fee, recipient_fee=recipient_fee, total_fee=total_fee, net_amount=net_amount, message="Load request created successfully. The sender has been notified.")

@router.post("/swap-funds", response_model=LoadResponse)
async def swap_funds(swap: SwapFunds):
    source_profile = await get_profile_by_laundr_id(swap.source_id)
    if not source_profile:
        raise HTTPException(status_code=404, detail=f"Source profile with laundr_id {swap.source_id} not found")
    destination_profile = await get_profile_by_laundr_id(swap.destination_id)
    if not destination_profile:
        raise HTTPException(status_code=404, detail=f"Destination profile with laundr_id {swap.destination_id} not found")

    total_fee, sender_fee, recipient_fee = calculate_fees(swap.amount)
    net_amount = swap.amount - total_fee

    astra_routine_data = AstraRoutineCreate(type="swap", amount=swap.amount, source_id=swap.source_id, destination_id=swap.destination_id)
    routine = await astra.create_routine(astra_routine_data)

    audit_log("swap_funds", {"transaction_id": routine.id, "source_id": swap.source_id, "destination_id": swap.destination_id, "amount": swap.amount, "fee": total_fee})

    return LoadResponse(transaction_id=routine.id, status=routine.status, sender_fee=sender_fee, recipient_fee=recipient_fee, total_fee=total_fee, net_amount=net_amount, message="Funds swapped successfully.")
