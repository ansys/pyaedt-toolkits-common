# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import ANY

# from PIL.ImageMath import lambda_eval
from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from examples.toolkit.pyaedt_toolkit.ui.run_frontend import ApplicationWindow
from examples.toolkit.pyaedt_toolkit.ui.windows.create_geometry.geometry_menu import CreateGeometryThread
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal

DEFAULT_URL = "http://127.0.0.1:5001"


class FakeCreateGeometryThread(QThread):
    finished_signal = Signal(bool)

    def run(self):
        QTimer.singleShot(0, lambda: self.finished_signal.emit(False))

def test_windows_default_values(patched_window_methods, qtbot):
    """Test the default values of the geometry menu in the application window."""
    windows = ApplicationWindow()    
    combo = windows.geometry_menu.geometry_combo
    multiplier = windows.geometry_menu.multiplier

    assert combo.currentText() == "Box"
    assert multiplier.text() == "1"


@patch("requests.post")
@patch.object(PyLogger, "log")
def test_windows_create_geometry_with_default_values(mock_log, mock_post, patched_window_methods, qtbot):
    """Test the creation of geometry with default values in the geometry menu."""
    windows = ApplicationWindow()

    qtbot.mouseClick(windows.geometry_menu.geometry_button, Qt.LeftButton)

    # Wait for the geometry thread to finish and then check the post request
    geometry_thread = windows.geometry_menu.geometry_thread
    assert geometry_thread.isRunning()
    qtbot.waitUntil(lambda: not geometry_thread.isRunning(), timeout=20000)
    mock_post.assert_called_once_with(f"{DEFAULT_URL}/create_geometry", timeout=ANY)

    assert any("Creating geometry." in call.args[0] for call in mock_log.call_args_list)
    assert any("Geometry created." in call.args[0] for call in mock_log.call_args_list)


@patch.object(PyLogger, "log")
def test_windows_create_geometry_aedt_not_connected(mock_log, patched_window_methods, qtbot):
    """Test the creation of geometry not connected to AEDT."""
    windows = ApplicationWindow()

    # Force aedt_thread to False
    windows.settings_menu.aedt_thread = False

    qtbot.mouseClick(windows.geometry_menu.geometry_button, Qt.LeftButton)

    assert any("AEDT not launched." in call.args[0] for call in mock_log.call_args_list)


@patch.object(PyLogger, "log")
def test_windows_create_geometry_backend_busy(mock_log, patched_window_methods, qtbot):
    windows = ApplicationWindow()

    windows.geometry_menu.geometry_thread = MagicMock()
    windows.geometry_menu.geometry_thread.isRunning.return_value = True

    qtbot.mouseClick(windows.geometry_menu.geometry_button, Qt.LeftButton)

    assert any("Toolkit running" in call.args[0] for call in mock_log.call_args_list)


@patch("requests.post")
@patch.object(PyLogger, "log")
@patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.ApplicationWindow.get_properties")
def test_geometry_button_clicked_no_active_project(mock_get_properties,
                                                   mock_log,
                                                   mock_post,
                                                   patched_window_methods,
                                                   qtbot):
    window = ApplicationWindow()

    mock_get_properties.return_value = {
        "version": "0.1",
        "project_list": ["Dummy project"],
        "design_list": {"Dummy project": "Dummy design"},
        "example": {},
    }

    qtbot.mouseClick(window.geometry_menu.geometry_button, Qt.LeftButton)

    assert any("Toolkit not connected to AEDT." in call.args[0] for call in mock_log.call_args_list)
    mock_post.assert_not_called()
