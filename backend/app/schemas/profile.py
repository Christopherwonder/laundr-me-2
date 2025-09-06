from typing import List, Optional

from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    laundr_id: str = Field(..., alias="@laundrID")
    bio: Optional[str] = None
    headline: Optional[str] = None
    skill_tags: List[str] = []


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    headline: Optional[str] = None
    skill_tags: Optional[List[str]] = None


class Profile(ProfileBase):
    user_id: int
    user_intent_id: Optional[str] = None
    kyc_status: str = "not_started"

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
