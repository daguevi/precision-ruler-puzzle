"""
Application settings domain models
"""

from dataclasses import dataclass
from .base import BaseModel


@dataclass
class Settings(BaseModel):
    """Application settings model."""
    key: str
    value: str
    setting_type: str = "string"  # string, int, float, boolean, json
    description: str = ""
    is_user_editable: bool = True
