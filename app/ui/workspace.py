"""
Main workspace with stacked pages
"""

from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class WorkspaceStack(QStackedWidget):
    """
    Stacked widget container for all workspace pages.
    """
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet(self._get_style())
        
        # Add pages
        self.pages = {}
        self._create_pages()
    
    def _create_pages(self) -> None:
        """
        Create and register all workspace pages.
        """
        pages = [
            ("home", self._create_home_page),
            ("layouts", self._create_layouts_page),
            ("rulers", self._create_rulers_page),
            ("inventory", self._create_inventory_page),
            ("edge_manager", self._create_edge_manager_page),
            ("settings", self._create_settings_page),
        ]
        
        for page_id, create_func in pages:
            page = create_func()
            self.addWidget(page)
            self.pages[page_id] = page
    
    def show_page(self, page_id: str) -> None:
        """
        Show a specific page by ID.
        """
        if page_id in self.pages:
            self.setCurrentWidget(self.pages[page_id])
    
    def _create_home_page(self) -> QWidget:
        """Create home/welcome page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Precision Ruler Puzzle System")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #64b5f6; margin: 40px;")
        
        subtitle = QLabel("A precision engineering puzzle game")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #a0a0a0; margin: 20px;")
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        
        return page
    
    def _create_layouts_page(self) -> QWidget:
        """Create layouts module page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Layouts Module (Coming Soon)")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #64b5f6;")
        layout.addWidget(label)
        return page
    
    def _create_rulers_page(self) -> QWidget:
        """Create rulers module page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Rulers Module (Coming Soon)")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #64b5f6;")
        layout.addWidget(label)
        return page
    
    def _create_inventory_page(self) -> QWidget:
        """Create inventory module page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Inventory Module (Coming Soon)")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #64b5f6;")
        layout.addWidget(label)
        return page
    
    def _create_edge_manager_page(self) -> QWidget:
        """Create edge manager module page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Edge Manager (Coming Soon)")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #ffc107;")
        layout.addWidget(label)
        return page
    
    def _create_settings_page(self) -> QWidget:
        """Create settings module page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Settings Module (Coming Soon)")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #64b5f6;")
        layout.addWidget(label)
        return page
    
    def _get_style(self) -> str:
        """
        Get workspace styling.
        """
        return """
            QStackedWidget {
                background-color: #2a2a2a;
                color: #ffffff;
            }
        """
