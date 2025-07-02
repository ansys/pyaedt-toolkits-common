import os.path

from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QSplashScreen

from examples.toolkit.pyaedt_toolkit.ui.models import properties


def show_splash_screen(app):
    """Show the splash screen for the application.

    This function creates a splash screen with a specified image and dimensions.
    It displays the splash screen for a certain duration before closing it.
    The splash screen is shown on top of the main application window.
    """
    if properties.high_resolution:
        splash_dim = 800
    else:
        splash_dim = 600
    splash_pix = QPixmap(os.path.join(os.path.dirname(__file__), "splash.png"))
    scaled_pix = splash_pix.scaled(splash_dim, splash_dim, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    splash = QSplashScreen(scaled_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.show()

    # Start the main application after the splash screen
    QTimer.singleShot(7000, splash.close)
    app.processEvents()
    return splash
