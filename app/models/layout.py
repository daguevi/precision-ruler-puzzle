"""
Layout domain models
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from .base import BaseModel


class EngagementMode(Enum):
    """Engagement modes for ruler assembly."""
    STANDARD = "standard"
    ALTERNATING = "alternating"


class LayoutStyle(Enum):
    """Layout symmetry styles."""
    CENTER_BALANCED = "center_balanced"
    SHOULDER_DATUM_REF = "shoulder_datum_ref"


class SpacerMaterial(Enum):
    """Spacer material options."""
    METAL_BOTH = "metal_both"
    RUBBER_BONDED_BOTH = "rubber_bonded_both"


@dataclass
class LayoutBlock(BaseModel):
    """Represents a single block requirement in a layout."""
    layout_id: int
    width_mm: float
    quantity: int
    description: str = ""
    
    def total_width(self) -> float:
        """Calculate total width consumed by this block group."""
        return self.width_mm * self.quantity


@dataclass
class LayoutSequence(BaseModel):
    """Represents the assembly sequence for a ruler."""
    layout_id: int
    ruler_position: str  # 'top' or 'bottom'
    sequence_order: int
    component_type: str  # 'edge_block', 'spacer', 'grip_ring', 'micro_shim'
    component_id: int
    quantity: int
    thickness_mm: float
    

@dataclass
class Layout(BaseModel):
    """Main layout domain model."""
    name: str
    master_board_width_mm: float
    layer_thickness_mm: float
    ruler_id: int
    material_id: int
    side_offset_mm: float
    engagement_mode: EngagementMode = EngagementMode.STANDARD
    layout_style: LayoutStyle = LayoutStyle.CENTER_BALANCED
    spacer_material: SpacerMaterial = SpacerMaterial.METAL_BOTH
    use_micro_shims: bool = False
    
    # Derived fields (populated after optimization)
    status: str = "draft"  # draft, optimizing, complete, failed
    total_stack_width_mm: Optional[float] = None
    estimated_compensation_mm: Optional[float] = None
    warnings: str = ""
    
    # Relations (loaded separately)
    blocks: List[LayoutBlock] = field(default_factory=list)
    sequences: List[LayoutSequence] = field(default_factory=list)
    
    def validate_block_configuration(self) -> tuple[bool, str]:
        """
        Validate that blocks don't exceed master board width.
        Returns (is_valid, message)
        """
        total_used = sum(b.total_width() for b in self.blocks)
        
        if total_used > self.master_board_width_mm:
            return False, f"Block width ({total_used}mm) exceeds board width ({self.master_board_width_mm}mm)"
        
        if total_used == 0:
            return False, "No blocks configured"
        
        return True, "Valid"
    
    def get_utilization_percent(self) -> float:
        """Calculate board width utilization percentage."""
        if self.master_board_width_mm == 0:
            return 0.0
        total_used = sum(b.total_width() for b in self.blocks)
        return (total_used / self.master_board_width_mm) * 100
