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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from ansys.aedt.toolkits.common.ui.utils.widgets.py_push_button.styles import Styles


class PyPushButton(QPushButton):
    """
    Initialize the PyPushButton.

    Parameters
    ----------
    text : str
        The title text for the right column.
    radius : int
        The border radius of the button.
    color : str
        The text color of the button.
    bg_color : str
        The background color of the button.
    bg_color_hover : int
        The background color of the button when hovered.
    bg_color_pressed : str
        The background color of the button when pressed.
    font_size : int
        The font size of the text on the button.
    parent : str, optional
        The parent widget. The default is None.

    """

    def __init__(
        self,
        text,
        radius,
        color,
        bg_color,
        bg_color_hover,
        bg_color_pressed,
        font_size,
        parent=None,
    ):
        super().__init__()

        self.setText(text)
        if parent is not None:
            self.setParent(parent)
        self.setCursor(Qt.PointingHandCursor)

        # SET STYLESHEET
        custom_style = Styles.style.format(
            _color=color,
            _radius=radius,
            _bg_color=bg_color,
            _bg_color_hover=bg_color_hover,
            _bg_color_pressed=bg_color_pressed,
            _font_size=font_size,
        )
        self.setStyleSheet(custom_style)
