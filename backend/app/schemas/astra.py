from pydantic import BaseModel
from typing import Optional

class AstraUserIntentCreate(BaseModel):
    laundr_id: str
    # In a real implementation, we would include more user details
    # as required by the Astra API documentation.

class AstraUserIntent(BaseModel):
    id: str # This will be the user_intent_id
    status: str # e.g., "pending", "verified", "rejected"
