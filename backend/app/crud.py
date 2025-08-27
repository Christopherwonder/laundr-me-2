from fastapi import HTTPException
from app.schemas.profile import Profile
from app.schemas.settings import Settings

# Dummy databases
db_profiles = {}
db_settings = {}

async def get_profile_by_id(user_id: int) -> Profile:
    if user_id not in db_profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profiles[user_id]
