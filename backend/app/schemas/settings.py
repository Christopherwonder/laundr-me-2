from typing import Optional

from pydantic import BaseModel, Field


class SettingsBase(BaseModel):
    biometric_enabled: bool = False
    pin_enabled: bool = True
    notifications_enabled: bool = True
    spending_limit: float = 1000.0


class SettingsUpdate(BaseModel):
    biometric_enabled: Optional[bool] = None
    pin_enabled: Optional[bool] = None
    notifications_enabled: Optional[bool] = None
    spending_limit: Optional[float] = None


class Settings(SettingsBase):
    user_id: int

    model_config = {
        "from_attributes": True,
    }
