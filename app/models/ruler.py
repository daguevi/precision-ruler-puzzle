"""
Ruler domain models
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from .base import BaseModel


class RulerPreset(Enum):
    """Standard ruler preset configurations."""
    STANDARD = "standard"
    PRECISION = "precision"
    INDUSTRIAL = "industrial"


@dataclass
class Ruler(BaseModel):
    """Ruler preset domain model."""
    name: str
    total_length_mm: float
    maximum_stack_width_mm: float
    supported_engagement_modes: List[str] = field(default_factory=list)
    tolerance_microns: float = 10.0
    supported_materials: List[str] = field(default_factory=list)
    default_offset_mm: float = 0.0
    description: str = ""
    is_active: bool = True
    
    def is_compatible_with_width(self, width_mm: float) -> bool:
        """Check if ruler can accommodate given stack width."""
        return width_mm <= self.maximum_stack_width_mm
