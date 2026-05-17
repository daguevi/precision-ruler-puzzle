"""
User domain models
"""

from dataclasses import dataclass
from typing import Optional
from .base import BaseModel


@dataclass
class User(BaseModel):
    """User account model."""
    username: str
    email: str
    full_name: str = ""
    password_hash: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
    preferences: str = ""  # JSON serialized
