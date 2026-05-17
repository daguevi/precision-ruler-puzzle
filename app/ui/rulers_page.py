"""
Rulers UI module for CRUD operations
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                                QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                                QDoubleSpinBox, QDialog, QFormLayout, QMessageBox,
                                QDialogButtonBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.database.db_manager import DatabaseManager
from app.services.ruler_service import RulerService


class RulersPage(QWidget):
    """Rulers management module with CRUD operations."""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.ruler_service = RulerService(self.db_manager)
        
        self.setStyleSheet(self._get_style())
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Ruler Presets Management")
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setStyleSheet("color: #64b5f6;")
        layout.addWidget(header)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Add Ruler Preset")
        add_btn.clicked.connect(self._show_add_dialog)
        btn_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._refresh_table)
        btn_layout.addWidget(refresh_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Rulers table
        self.rulers_table = QTableWidget()
        self.rulers_table.setColumnCount(8)
        self.rulers_table.setHorizontalHeaderLabels([
            "ID", "Name", "Total Length (mm)", "Max Stack (mm)", 
            "Engagement Modes", "Tolerance (µm)", "Default Offset (mm)", "Action"
        ])
        self.rulers_table.setMinimumHeight(400)
        layout.addWidget(self.rulers_table)
        
        self.rulers_table.setStyleSheet("""
            QTableWidget {
                background-color: #3a3a3a;
                color: #ffffff;
                gridline-color: #555555;
            }
            QHeaderView::section {
                background-color: #0d47a1;
                color: #ffffff;
                padding: 6px;
                font-weight: bold;
            }
        """)
        
        # Style buttons
        self.setStyleSheet(self.getStyleSheet())
        
        self._refresh_table()
    
    def _refresh_table(self):
        """Refresh rulers table."""
        self.rulers_table.setRowCount(0)
        rulers = self.ruler_service.get_all_rulers()
        
        for row, ruler in enumerate(rulers):
            self.rulers_table.insertRow(row)
            
            items = [
                (0, str(ruler['id'])),
                (1, ruler['name']),
                (2, str(ruler['total_length_mm'])),
                (3, str(ruler['maximum_stack_width_mm'])),
                (4, ruler['supported_engagement_modes']),
                (5, str(ruler['tolerance_microns'])),
                (6, str(ruler['default_offset_mm']))
            ]
            
            for col, value in items:
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.rulers_table.setItem(row, col, item)
            
            # Action buttons
            action_layout = QHBoxLayout()
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, rid=ruler['id']: self._show_edit_dialog(rid))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, rid=ruler['id']: self._delete_ruler(rid))
            delete_btn.setStyleSheet("background-color: #8b0000;")
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.rulers_table.setCellWidget(row, 7, action_widget)
        
        self.rulers_table.resizeColumnsToContents()
    
    def _show_add_dialog(self):
        """Show add ruler dialog."""
        dialog = RulerEditDialog(self, None)
        if dialog.exec() == QDialog.Accepted:
            self._refresh_table()
            QMessageBox.information(self, "Success", "Ruler preset added successfully!")
    
    def _show_edit_dialog(self, ruler_id: int):
        """Show edit ruler dialog."""
        ruler = self.ruler_service.get_ruler(ruler_id)
        if ruler:
            dialog = RulerEditDialog(self, ruler)
            if dialog.exec() == QDialog.Accepted:
                self._refresh_table()
                QMessageBox.information(self, "Success", "Ruler preset updated successfully!")
    
    def _delete_ruler(self, ruler_id: int):
        """Delete ruler preset."""
        reply = QMessageBox.question(self, "Confirm Delete", 
                                      "Are you sure you want to delete this ruler preset?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.ruler_service.delete_ruler(ruler_id):
                self._refresh_table()
                QMessageBox.information(self, "Success", "Ruler preset deleted!")
    
    def _get_style(self) -> str:
        return """
            QWidget {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d47a1;
                color: #64b5f6;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton[text="Edit"] {
                background-color: #0d47a1;
            }
            QPushButton[text="Delete"] {
                background-color: #8b0000;
            }
        """
    
    def getStyleSheet(self) -> str:
        return self._get_style()


class RulerEditDialog(QDialog):
    """Dialog for adding/editing ruler presets."""
    
    def __init__(self, parent, ruler=None):
        super().__init__(parent)
        self.ruler = ruler
        self.ruler_service = parent.ruler_service
        
        self.setWindowTitle("Edit Ruler Preset" if ruler else "Add Ruler Preset")
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QLabel {
                color: #b0b0b0;
            }
            QLineEdit, QDoubleSpinBox {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 6px;
                border-radius: 4px;
            }
        """)
        
        layout = QFormLayout(self)
        
        # Name
        self.name_input = QLineEdit()
        if ruler:
            self.name_input.setText(ruler['name'])
        layout.addRow("Name:", self.name_input)
        
        # Total length
        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(100, 10000)
        if ruler:
            self.length_spin.setValue(ruler['total_length_mm'])
        else:
            self.length_spin.setValue(500)
        layout.addRow("Total Length (mm):", self.length_spin)
        
        # Max stack width
        self.max_stack_spin = QDoubleSpinBox()
        self.max_stack_spin.setRange(50, 5000)
        if ruler:
            self.max_stack_spin.setValue(ruler['maximum_stack_width_mm'])
        else:
            self.max_stack_spin.setValue(150)
        layout.addRow("Max Stack Width (mm):", self.max_stack_spin)
        
        # Tolerance
        self.tolerance_spin = QDoubleSpinBox()
        self.tolerance_spin.setRange(1, 100)
        if ruler:
            self.tolerance_spin.setValue(ruler['tolerance_microns'])
        else:
            self.tolerance_spin.setValue(10)
        layout.addRow("Tolerance (microns):", self.tolerance_spin)
        
        # Default offset
        self.offset_spin = QDoubleSpinBox()
        self.offset_spin.setRange(0, 10)
        if ruler:
            self.offset_spin.setValue(ruler['default_offset_mm'])
        else:
            self.offset_spin.setValue(0.5)
        layout.addRow("Default Offset (mm):", self.offset_spin)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._save)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
    
    def _save(self):
        """Save ruler preset."""
        data = {
            'name': self.name_input.text(),
            'total_length_mm': self.length_spin.value(),
            'maximum_stack_width_mm': self.max_stack_spin.value(),
            'tolerance_microns': self.tolerance_spin.value(),
            'default_offset_mm': self.offset_spin.value(),
        }
        
        if self.ruler:
            self.ruler_service.update_ruler(self.ruler['id'], data)
        else:
            self.ruler_service.create_ruler(data)
        
        self.accept()
