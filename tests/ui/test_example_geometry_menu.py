from unittest.mock import patch

from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from examples.toolkit.pyaedt_toolkit.ui.run_frontend import ApplicationWindow
from PySide6.QtCore import Qt

DEFAULT_URL = "http://127.0.0.1:5001"


def test_windows_default_values(qtbot):
    """Test the default values of the geometry menu in the application window."""
    windows = ApplicationWindow()    
    combo = windows.geometry_menu.geometry_combo
    multiplier = windows.geometry_menu.multiplier

    assert combo.currentText() == "Box"
    assert multiplier.text() == "1"

@patch("requests.post")
@patch.object(PyLogger, "log")
def test_windows_create_geometry_with_default_values(mock_log, mock_post, qtbot):
    """Test the creation of geometry with default values in the geometry menu."""
    windows = ApplicationWindow()

    qtbot.mouseClick(windows.geometry_menu.geometry_button, Qt.LeftButton)

    # Wait for the geometry thread to finish and then check the post request
    geometry_thread = windows.geometry_menu.geometry_thread
    with qtbot.waitSignal(geometry_thread.finished_signal, timeout=1000):
        pass
    mock_post.assert_called_once_with(f"{DEFAULT_URL}/create_geometry")

    assert any("Creating geometry." in call.args[0] for call in mock_log.call_args_list)
    assert any("Geometry created." in call.args[0] for call in mock_log.call_args_list)
