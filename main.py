#!/usr/bin/env python3
"""
Precision Ruler Puzzle System
Main application entry point
"""

import sys
import os
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.database.db_manager import DatabaseManager
from app.ui.main_window import MainWindow
from app.utils.styles import apply_dark_theme


def initialize_application():
    """
    Initialize application: database, theme, fonts.
    """
    # Initialize database with schema and seed data
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Configure application appearance
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Set default font for better readability
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply dark technical theme
    apply_dark_theme(app)
    
    return app


def main():
    """
    Main application entry point.
    """
    try:
        # Initialize application
        app = initialize_application()
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Run application
        sys.exit(app.exec())
    
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
