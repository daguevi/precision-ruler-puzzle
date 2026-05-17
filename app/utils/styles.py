"""
Application styling and theming
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette


def apply_dark_theme(app: QApplication) -> None:
    """
    Apply dark technical theme to application.
    """
    palette = QPalette()
    
    # Colors
    dark_bg = QColor(0x1e, 0x1e, 0x1e)      # #1e1e1e
    darker_bg = QColor(0x2a, 0x2a, 0x2a)    # #2a2a2a
    text_color = QColor(0xff, 0xff, 0xff)   # White
    accent_color = QColor(0x64, 0xb5, 0xf6) # Light blue
    
    # Set palette colors
    palette.setColor(QPalette.Window, dark_bg)
    palette.setColor(QPalette.Base, darker_bg)
    palette.setColor(QPalette.Text, text_color)
    palette.setColor(QPalette.PlaceholderText, QColor(0x80, 0x80, 0x80))
    palette.setColor(QPalette.Button, darker_bg)
    palette.setColor(QPalette.ButtonText, text_color)
    palette.setColor(QPalette.Highlight, accent_color)
    palette.setColor(QPalette.HighlightedText, QColor(0xff, 0xff, 0xff))
    
    app.setPalette(palette)
    
    # Set stylesheet for additional customization
    app.setStyle("Fusion")
