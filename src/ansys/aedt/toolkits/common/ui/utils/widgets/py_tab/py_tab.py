# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

from PySide6.QtWidgets import QTabWidget

from ansys.aedt.toolkits.common.ui.utils.widgets.py_tab.styles import Styles


class PyTab(QTabWidget):
    """
    Initialize the PyTab.

    Parameters
    ----------
    color : str
        The pane color.
    text_color : str
        The text color.
    selected_color : int
        The color of the selected tab.
    unselected_color : str
        The color of the unselected tab.
    """

    def __init__(self, color, text_color, selected_color, unselected_color):
        super().__init__()

        # SET STYLESHEET
        custom_style = Styles.style.format(
            _color=color, _unselected_color=unselected_color, _selected_color=selected_color, _text_color=text_color
        )
        self.setStyleSheet(custom_style)
