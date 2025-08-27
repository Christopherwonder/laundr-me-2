from fastapi import Depends, HTTPException, status
from app.crud import get_profile_by_id
from app.schemas.profile import Profile

async def get_current_verified_user(
    profile: Profile = Depends(get_profile_by_id)
) -> Profile:
    if profile.kyc_status != "verified":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has not been verified.",
        )
    return profile
