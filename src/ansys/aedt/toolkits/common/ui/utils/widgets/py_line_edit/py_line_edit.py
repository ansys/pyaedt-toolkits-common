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

from PySide6.QtWidgets import QLineEdit

from ansys.aedt.toolkits.common.ui.utils.widgets.py_line_edit.styles import Styles


class PyLineEdit(QLineEdit):
    """
    Custom QLineEdit widget with enhanced styling.

    Parameters
    ----------
    text : str, optional
        The initial text for the line edit. Default is an empty string.
    place_holder_text : str, optional
        The placeholder text to be displayed when the line edit is empty. Default is an empty string.
    radius : int, optional
        The border radius of the line edit. Default is 8.
    border_size : int, optional
        The border size of the line edit. Default is 2.
    color : str, optional
        The text color of the line edit. Default is "#FFF" (white).
    selection_color : str, optional
        The text selection color of the line edit. Default is "#FFF" (white).
    bg_color : str, optional
        The background color of the line edit. Default is "#333" (dark gray).
    bg_color_active : str, optional
        The background color of the line edit when active. Default is "#222" (darker gray).
    context_color : str, optional
        The color representing a context or active state. Default is "#00ABE8" (blue).
    font_size : int, optional
        The font size of the text on the button.
    """

    def __init__(
        self,
        text="",
        place_holder_text="",
        radius=8,
        border_size=2,
        color="#FFF",
        selection_color="#FFF",
        bg_color="#333",
        bg_color_active="#222",
        context_color="#00ABE8",
        font_size=12,
    ):
        super().__init__()

        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        self.set_stylesheet(
            radius, border_size, color, selection_color, bg_color, bg_color_active, context_color, font_size
        )

    def set_stylesheet(
        self, radius, border_size, color, selection_color, bg_color, bg_color_active, context_color, font_size
    ):
        """
        Set the stylesheet for the PyLineEdit.

        Parameters
        ----------
        radius : int
            Border radius of the line edit.
        border_size : int
            Border size of the line edit.
        color : str
            Text color of the line edit.
        selection_color : str
            Text selection color of the line edit.
        bg_color : str
            Background color of the line edit.
        bg_color_active : str
            Background color when the line edit is active.
        context_color : str
            Color representing a context or active state.
        font_size : int
            The font size of the text on the button.

        """
        style_format = Styles.style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color,
            _font_size=font_size,
        )
        self.setStyleSheet(style_format)
