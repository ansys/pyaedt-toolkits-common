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

from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from examples.toolkit.pyaedt_toolkit.ui.run_frontend import ApplicationWindow
from PySide6.QtCore import Qt

DEFAULT_URL = "http://127.0.0.1:5001"


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
    with qtbot.waitSignal(geometry_thread.finished_signal, timeout=1000):
        pass
    mock_post.assert_called_once_with(f"{DEFAULT_URL}/create_geometry")

    assert any("Creating geometry." in call.args[0] for call in mock_log.call_args_list)
    assert any("Geometry created." in call.args[0] for call in mock_log.call_args_list)
