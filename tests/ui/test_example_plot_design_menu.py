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

from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from examples.toolkit.pyaedt_toolkit.ui.run_frontend import ApplicationWindow
from examples.toolkit.pyaedt_toolkit.ui.windows.plot_design.plot_design_menu import PlotDesignThread
from PySide6.QtCore import Qt

DEFAULT_URL = "http://127.0.0.1:5001"


@patch("requests.get")
@patch.object(PyLogger, "log")
def test_plot_design_menu_setup_and_button_click(mock_log, mock_get, patched_window_methods, qtbot):
    windows = ApplicationWindow()

    qtbot.mouseClick(windows.plot_design_menu.plot_design_button, Qt.LeftButton)

    # Wait for the geometry thread to finish and then check the post request
    get_model_thread = windows.plot_design_menu.get_model_thread
    with qtbot.waitSignal(get_model_thread.finished_signal, timeout=1000):
        pass

    args, kwargs = mock_get.call_args
    assert args[0] == f"{DEFAULT_URL}/get_aedt_model"
    assert "json" in kwargs

    assert "air_objects" in kwargs["json"]

    assert any("Exporting model." in call.args[0] for call in mock_log.call_args_list)
    assert any("Model exported." in call.args[0] for call in mock_log.call_args_list)


@patch.object(PyLogger, "log")
def test_windows_plot_design_aedt_not_connected(mock_log, patched_window_methods, qtbot):
    windows = ApplicationWindow()

    # Force aedt_thread to False
    windows.settings_menu.aedt_thread = False

    qtbot.mouseClick(windows.plot_design_menu.plot_design_button, Qt.LeftButton)

    assert any("AEDT not launched." in call.args[0] for call in mock_log.call_args_list)


@patch.object(PyLogger, "log")
def test_windows_plot_design_backend_busy(mock_log, patched_window_methods, qtbot):
    windows = ApplicationWindow()

    windows.plot_design_menu.get_model_thread = MagicMock()
    windows.plot_design_menu.get_model_thread.isRunning.return_value = True

    qtbot.mouseClick(windows.plot_design_menu.plot_design_button, Qt.LeftButton)

    assert any("Toolkit running" in call.args[0] for call in mock_log.call_args_list)


@patch.object(PyLogger, "log")
def test_windows_plot_design_non_success(mock_log, patched_window_methods, qtbot):
    windows = ApplicationWindow()
    windows.plot_design_menu.get_model_thread = MagicMock()
    windows.plot_design_menu.get_model_thread.model_info = None

    windows.plot_design_menu.get_model_finished()

    assert any("Failed backend call" in call.args[0] for call in mock_log.call_args_list)
