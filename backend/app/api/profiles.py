from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas.profile import Profile, ProfileCreate, ProfileUpdate
from app.schemas.astra import AstraUserIntentCreate
from app.services import astra
from app.dependencies import get_current_verified_user
from app.crud import db_profiles, get_profile_by_id

router = APIRouter()

next_user_id = 1

# Dummy audit log
def audit_log(action: str, details: dict):
    print(f"AUDIT: {action} - {details}")

@router.post("/", response_model=Profile, status_code=201)
async def create_profile(profile: ProfileCreate):
    global next_user_id
    if any(p.laundr_id == profile.laundr_id for p in db_profiles.values()):
        raise HTTPException(status_code=400, detail="@laundrID already registered")

    # Create Astra User Intent
    astra_user_intent_data = AstraUserIntentCreate(laundr_id=profile.laundr_id)
    user_intent = await astra.create_user_intent(astra_user_intent_data)

    new_profile = Profile(
        user_id=next_user_id,
        user_intent_id=user_intent.id,
        kyc_status=user_intent.status,
        **profile.model_dump()
    )
    db_profiles[next_user_id] = new_profile
    audit_log("create_profile", {"user_id": next_user_id, "laundr_id": new_profile.laundr_id, "user_intent_id": user_intent.id})
    next_user_id += 1
    return new_profile

@router.put("/{user_id}", response_model=Profile)
async def update_profile(
    user_id: int,
    profile_update: ProfileUpdate,
    current_user: Profile = Depends(get_current_verified_user),
):
    existing_profile = await get_profile_by_id(user_id)
    update_data = profile_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_profile, field, value)

    audit_log("update_profile", {"user_id": user_id, "updated_fields": list(update_data.keys())})
    return existing_profile


@router.get("/{user_id}", response_model=Profile)
async def get_profile(profile: Profile = Depends(get_profile_by_id)):
    return profile
