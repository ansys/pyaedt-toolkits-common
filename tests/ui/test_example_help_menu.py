from unittest.mock import patch

from examples.toolkit.pyaedt_toolkit.ui.run_frontend import ApplicationWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QDesktopServices

from examples.toolkit.pyaedt_toolkit.ui.windows.help.help_menu import ABOUT_TEXT, DOCUMENTATION_URL, ISSUE_TRACKER_URL


def test_windows_about_button(qtbot):
    """Test the About button in the help menu."""

    def check_and_close_msg_box():
        """Check the message box content and close it."""
        for w in QApplication.topLevelWidgets():
            if isinstance(w, QMessageBox):
                assert "About" == w.windowTitle()
                assert ABOUT_TEXT == w.text()
                ok_button = w.button(QMessageBox.Ok)
                qtbot.mouseClick(ok_button, Qt.LeftButton)
                return True
        return False

    # Define a function to check the message box and close it after a short delay
    QTimer.singleShot(10, check_and_close_msg_box)

    windows = ApplicationWindow()    
    qtbot.mouseClick(windows.help_menu.help_button, Qt.LeftButton)


@patch.object(QDesktopServices, 'openUrl')
def test_windows_documentation_online_button(mock_open_url, qtbot):
    """Test the online documentation button in the help menu."""
    EXPECTED_ARGUMENT = QUrl(DOCUMENTATION_URL)
    windows = ApplicationWindow()    

    qtbot.mouseClick(windows.help_menu.online_documentation_button, Qt.LeftButton)

    mock_open_url.assert_called_once_with(EXPECTED_ARGUMENT)


@patch.object(QDesktopServices, 'openUrl')
def test_windows_issue_tracker_button(mock_open_url, qtbot):
    """Test the issue tracker button in the help menu."""
    EXPECTED_ARGUMENT = QUrl(ISSUE_TRACKER_URL)
    windows = ApplicationWindow()    

    qtbot.mouseClick(windows.help_menu.issue_tracker_button, Qt.LeftButton)

    mock_open_url.assert_called_once_with(EXPECTED_ARGUMENT)
