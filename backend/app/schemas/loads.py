from pydantic import BaseModel, Field
from typing import Optional, Union

# Schemas for Astra Routines
class AstraRoutineCreate(BaseModel):
    type: str  # "send", "request", "swap"
    amount: float
    source_id: str
    destination_id: str

class AstraRoutine(BaseModel):
    id: str
    status: str

# Schemas for Loads API
class LoadCreate(BaseModel):
    amount: float = Field(..., gt=0, description="The amount to send or request.")
    sender_id: str
    recipient_id: str

class SwapFunds(BaseModel):
    amount: float = Field(..., gt=0, description="The amount to swap.")
    source_id: str
    destination_id: str

class LoadResponse(BaseModel):
    transaction_id: str
    status: str
    sender_fee: float
    recipient_fee: float
    total_fee: float
    net_amount: float
    message: str
    invite_link: Optional[str] = None
