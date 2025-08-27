import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from app.schemas.astra import AstraUserIntentCreate, AstraUserIntent
from app.schemas.loads import AstraRoutineCreate, AstraRoutine

ASTRA_API_URL = "https://api.astra.financial/v1"

# In-memory database for demonstration purposes
transactions_db: List[Dict[str, Any]] = []


def log_transaction(action: str, details: dict):
    """Stores a transaction event for the activity feed."""
    print(f"AUDIT: {action} - {details}")
    log_entry = {
        "action": action,
        "details": details,
        "timestamp": datetime.now(timezone.utc),
        "status": "completed"  # Mock status for all transactions
    }
    transactions_db.append(log_entry)


async def create_user_intent(user_data: AstraUserIntentCreate) -> AstraUserIntent:
    """
    Creates a user intent with the Astra API.
    In a real implementation, this would make a POST request to the Astra API.
    For now, we'll mock the response.
    """
    print(f"Calling Astra API to create user intent for {user_data.laundr_id}")

    # Mocked response
    user_intent_id = f"ui_{uuid.uuid4()}"
    return AstraUserIntent(id=user_intent_id, status="pending")

async def create_routine(routine_data: AstraRoutineCreate) -> AstraRoutine:
    """
    Creates a routine with the Astra API.
    In a real implementation, this would make a POST request to the Astra API.
    For now, we'll mock the response.
    """
    print(f"Calling Astra API to create {routine_data.type} routine for {routine_data.amount}")

    # Mocked response
    routine_id = f"rt_{uuid.uuid4()}"
    return AstraRoutine(id=routine_id, status="completed")
