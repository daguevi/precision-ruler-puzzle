"""
Inventory domain models
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from .base import BaseModel


class ComponentType(Enum):
    """Component types in inventory."""
    EDGE_BLOCK = "edge_block"
    CORE_SPACER = "core_spacer"
    PRECISION_CORE_TILE = "precision_core_tile"
    GRIP_RING = "grip_ring"
    MICRO_SHIM = "micro_shim"


class MaterialProfile(Enum):
    """Material profiles for components."""
    HARDENED_CORE = "hardened_core"
    STANDARD = "standard"
    PRECISION = "precision"


@dataclass
class InventoryItem(BaseModel):
    """Inventory item master record."""
    component_type: ComponentType
    thickness_mm: float
    outer_diameter_mm: float
    inner_diameter_mm: float
    material_profile: MaterialProfile = MaterialProfile.STANDARD
    precision_class: str = "standard"
    description: str = ""
    is_active: bool = True
    
    # Stock tracking
    total_quantity: int = 0
    reserved_quantity: int = 0
    available_quantity: int = 0


@dataclass
class InventoryBatch(BaseModel):
    """Batch tracking for inventory items."""
    inventory_item_id: int
    batch_code: str
    quantity: int
    received_date: str
    expiry_date: Optional[str] = None
    notes: str = ""
    is_available: bool = True


@dataclass
class InventoryMovement(BaseModel):
    """Audit trail for inventory movements."""
    inventory_item_id: int
    movement_type: str  # 'in', 'out', 'reserve', 'release'
    quantity: int
    reference_type: str  # 'layout', 'adjustment', 'inventory_check'
    reference_id: Optional[int] = None
    notes: str = ""
