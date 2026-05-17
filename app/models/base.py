"""
Base model class with common functionality
"""

from datetime import datetime
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class BaseModel:
    """
    Base class for all domain models.
    Provides common fields and methods.
    """
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary representation.
        """
        return asdict(self)
    
    def is_deleted(self) -> bool:
        """
        Check if model is soft-deleted.
        """
        return self.deleted_at is not None
    
    def update(self, **kwargs) -> None:
        """
        Update model fields.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
