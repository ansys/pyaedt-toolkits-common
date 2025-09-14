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
from ansys.aedt.toolkits.common.ui.actions_generic import DEFAULT_AEDT_SESSION_VALUE
from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from examples.toolkit.pyaedt_toolkit.ui.run_frontend import ApplicationWindow

from tests.ui.conftest import INSTALLED_VERSIONS
from PySide6.QtCore import Qt

DUMMY_FILE_PATH = "dummy.aedt"

def test_settings_default_values(patched_window_methods, qtbot):
    """Test the default values of the settings menu in the application window."""
    windows = ApplicationWindow()
    menu = windows.settings_menu

    widget = menu.aedt_version
    assert INSTALLED_VERSIONS == [widget.itemText(i) for i in range(widget.count())]
    assert INSTALLED_VERSIONS[0] == widget.currentText()

    widget = menu.aedt_session
    assert DEFAULT_AEDT_SESSION_VALUE == widget.currentText()

    widget = menu.browse
    assert not widget.isChecked()

    widget = menu.connect_aedt
    assert "" == menu.file.text()

@patch("PySide6.QtWidgets.QFileDialog.getOpenFileName", return_value=(DUMMY_FILE_PATH, None))
def test_settings_browse_interaction(mock_get_open, patched_window_methods, qtbot):
    """Test the default values of the incident wave menu in the application window."""
    windows = ApplicationWindow()
    menu = windows.settings_menu

    widget = menu.browse
    qtbot.mouseClick(widget, Qt.LeftButton)

    mock_get_open.assert_called_once()
    assert DUMMY_FILE_PATH == menu.file.text()
