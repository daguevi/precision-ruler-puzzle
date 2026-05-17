"""
Edge Manager UI module (placeholder with future extension hooks)
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class EdgeManagerPage(QWidget):
    """Edge Manager module (coming soon)."""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet(self._get_style())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addStretch()
        
        # Title
        title = QLabel("Edge Manager")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ffc107;")
        layout.addWidget(title)
        
        # Coming Soon badge
        badge = QLabel("🚀 COMING SOON")
        badge.setFont(QFont("Arial", 16, QFont.Bold))
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet("color: #ffc107; margin: 20px;")
        layout.addWidget(badge)
        
        # Description
        desc = QLabel(
            "Manage divider ring positions and edge block configurations.\n\n"
            "Features in development:\n"
            "• Divider ring alignment\n"
            "• Edge block configuration\n"
            "• Separator disc positioning\n"
            "• Precision measurements"
        )
        desc.setFont(QFont("Arial", 11))
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #b0b0b0; line-height: 1.8;")
        layout.addWidget(desc)
        
        # Notify button
        notify_btn = QPushButton("🔔 Notify Me When Ready")
        notify_btn.setMinimumWidth(200)
        notify_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #000000;
                border: none;
                padding: 12px 24px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ffed4e;
            }
        """)
        notify_btn.clicked.connect(self._handle_notify)
        
        btn_layout = QVBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(notify_btn, alignment=Qt.AlignCenter)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        layout.addStretch()
    
    def _handle_notify(self):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Thanks!", "You'll be notified when Edge Manager is ready!")
    
    def _get_style(self) -> str:
        return """
            QWidget {
                background-color: #2a2a2a;
                color: #ffffff;
            }
        """
