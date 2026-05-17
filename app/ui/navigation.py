"""
Sidebar navigation component
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon


class SidebarNavigation(QWidget):
    """
    Left sidebar navigation panel.
    """
    
    navigation_changed = Signal(str)  # Emitted when page is selected
    
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(220)
        self.setMinimumWidth(220)
        self.setStyleSheet(self._get_style())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title
        title_label = self._create_title()
        layout.addWidget(title_label)
        
        # Navigation buttons
        nav_buttons = [
            ("Layouts", "layouts"),
            ("Rulers", "rulers"),
            ("Inventory", "inventory"),
            ("Edge Manager", "edge_manager"),
            ("Settings", "settings"),
        ]
        
        for label, page_id in nav_buttons:
            btn = self._create_nav_button(label, page_id)
            layout.addWidget(btn)
        
        layout.addStretch()
    
    def _create_title(self) -> QWidget:
        """
        Create title widget.
        """
        title_btn = QPushButton("PRECISION\nRULER")
        title_btn.setFont(QFont("Monospace", 9, QFont.Bold))
        title_btn.setCursor(Qt.PointingHandCursor)
        title_btn.setFlat(True)
        title_btn.setMinimumHeight(80)
        title_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d47a1;
                color: #64b5f6;
                border: none;
                padding: 12px;
                text-align: center;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        title_btn.clicked.connect(lambda: self.navigation_changed.emit("home"))
        return title_btn
    
    def _create_nav_button(self, label: str, page_id: str) -> QPushButton:
        """
        Create a navigation button.
        """
        btn = QPushButton(label)
        btn.setFlat(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(50)
        btn.setStyleSheet(self._get_button_style())
        btn.clicked.connect(lambda: self.navigation_changed.emit(page_id))
        return btn
    
    def _get_button_style(self) -> str:
        """
        Get button styling.
        """
        return """
            QPushButton {
                background-color: #2a2a2a;
                color: #b0b0b0;
                border: none;
                padding: 12px;
                text-align: left;
                font-weight: 500;
                border-left: 3px solid transparent;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                color: #ffffff;
                border-left: 3px solid #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
                color: #64b5f6;
                border-left: 3px solid #64b5f6;
            }
        """
    
    def _get_style(self) -> str:
        """
        Get sidebar styling.
        """
        return """
            QWidget {
                background-color: #1e1e1e;
                border-right: 1px solid #3a3a3a;
            }
        """
