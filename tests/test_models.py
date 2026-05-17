"""
Tests for data models
"""

import pytest
from app.models.layout import Layout, LayoutBlock, EngagementMode, LayoutStyle, SpacerMaterial


class TestLayout:
    """Test suite for Layout model."""
    
    def test_layout_creation(self):
        """Test creating a layout instance."""
        layout = Layout(
            name="Test Layout",
            master_board_width_mm=1000.0,
            layer_thickness_mm=5.0,
            ruler_id=1,
            material_id=1,
            side_offset_mm=10.0
        )
        
        assert layout.name == "Test Layout"
        assert layout.master_board_width_mm == 1000.0
        assert layout.status == "draft"
    
    def test_layout_block_total_width(self):
        """Test block total width calculation."""
        block = LayoutBlock(
            layout_id=1,
            width_mm=250.0,
            quantity=4
        )
        
        assert block.total_width() == 1000.0
    
    def test_layout_validation_success(self):
        """Test successful layout validation."""
        layout = Layout(
            name="Valid Layout",
            master_board_width_mm=1000.0,
            layer_thickness_mm=5.0,
            ruler_id=1,
            material_id=1,
            side_offset_mm=10.0,
            blocks=[
                LayoutBlock(layout_id=1, width_mm=250.0, quantity=4)
            ]
        )
        
        is_valid, message = layout.validate_block_configuration()
        assert is_valid
    
    def test_layout_validation_overflow(self):
        """Test layout validation with overflow."""
        layout = Layout(
            name="Overflow Layout",
            master_board_width_mm=1000.0,
            layer_thickness_mm=5.0,
            ruler_id=1,
            material_id=1,
            side_offset_mm=10.0,
            blocks=[
                LayoutBlock(layout_id=1, width_mm=300.0, quantity=4)  # Total 1200mm
            ]
        )
        
        is_valid, message = layout.validate_block_configuration()
        assert not is_valid
        assert "exceeds" in message.lower()
