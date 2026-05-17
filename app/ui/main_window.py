"""
Main application window
"""

from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from .navigation import SidebarNavigation
from .workspace import WorkspaceStack


class MainWindow(QMainWindow):
    """
    Main application window with sidebar navigation and workspace.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Precision Ruler Puzzle System")
        self.setWindowIcon(QIcon())
        self.setMinimumSize(QSize(1400, 900))
        
        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create sidebar and workspace
        self.sidebar = SidebarNavigation()
        self.workspace = WorkspaceStack()
        
        # Connect sidebar signals to workspace
        self.sidebar.navigation_changed.connect(self.workspace.show_page)
        
        # Add to layout using splitter for resize capability
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.workspace)
        splitter.setStretchFactor(0, 0)  # Sidebar fixed
        splitter.setStretchFactor(1, 1)  # Workspace expandable
        splitter.setCollapsible(0, False)
        
        layout.addWidget(splitter)
        
        # Set window properties
        self.setStyleSheet(self._get_window_style())
        self.showMaximized()
    
    def _get_window_style(self) -> str:
        """
        Get window-level styling.
        """
        return """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        """
