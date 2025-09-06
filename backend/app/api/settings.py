from app.crud import db_settings
from app.dependencies import get_current_verified_user
from app.schemas.profile import Profile
from app.schemas.settings import Settings, SettingsUpdate
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


# Dummy audit log
def audit_log(action: str, details: dict):
    print(f"AUDIT: {action} - {details}")


@router.get("/{user_id}", response_model=Settings)
async def get_settings(user_id: int):
    if user_id not in db_settings:
        # Create default settings if none exist
        db_settings[user_id] = Settings(user_id=user_id)
    return db_settings[user_id]


@router.put("/{user_id}", response_model=Settings)
async def update_settings(
    user_id: int,
    settings_update: SettingsUpdate,
    current_user: Profile = Depends(get_current_verified_user),
):
    if user_id not in db_settings:
        db_settings[user_id] = Settings(user_id=user_id)

    existing_settings = db_settings[user_id]
    update_data = settings_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_settings, field, value)

    audit_log(
        "update_settings",
        {"user_id": user_id, "updated_fields": list(update_data.keys())},
    )
    return existing_settings
