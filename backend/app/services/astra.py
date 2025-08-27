import uuid
from app.schemas.astra import AstraUserIntentCreate, AstraUserIntent

ASTRA_API_URL = "https://api.astra.financial/v1"

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
