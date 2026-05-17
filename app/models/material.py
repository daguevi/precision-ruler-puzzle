"""
Material domain models
"""

from dataclasses import dataclass
from typing import Optional
from .base import BaseModel


@dataclass
class Material(BaseModel):
    """Material type domain model."""
    name: str
    description: str = ""
    density_g_cm3: float = 0.0
    hardness_hv: Optional[float] = None
    thermal_stability: str = "standard"  # low, standard, high
    cost_per_unit: float = 0.0
    is_active: bool = True
    properties: str = ""  # JSON serialized
