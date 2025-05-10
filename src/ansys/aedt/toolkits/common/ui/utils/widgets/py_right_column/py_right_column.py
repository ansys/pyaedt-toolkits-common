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
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ansys.aedt.toolkits.common.ui.utils.ui_templates.columns.ui_right_column import Ui_RightColumn
from ansys.aedt.toolkits.common.ui.utils.widgets.py_icon.py_icon import PyIcon


class PyRightColumn(QWidget):
    """
    Custom widget representing a right column with a title, an icon, and a content area.

    Parameters
    ----------
    text_title : str
        The title text for the right column.
    text_title_size : int
        The font size of the title text.
    text_title_color : str
        The color of the title text.
    dark_one : str
        Color representing a dark shade.
    bg_color : str
        Background color of the right column.
    btn_color : str
        Color of the buttons in the right column.
    btn_color_hover : str
        Color of the buttons when hovered.
    btn_color_pressed : str
        Color of the buttons when pressed.
    icon_path : str
        Path to the icon image file.
    icon_color : str
        Color of the icon.
    icon_color_hover : str
        Color of the icon when hovered.
    icon_color_pressed : str
        Color of the icon when pressed.
    context_color : str
        Color representing a context or active state.
    radius : int
        Border radius of the right column.

    """

    clicked = Signal(object, name="right_column_clicked")
    released = Signal(object, name="right_column_released")

    def __init__(
        self,
        text_title,
        text_title_size,
        text_title_color,
        dark_one,
        bg_color,
        btn_color,
        btn_color_hover,
        btn_color_pressed,
        icon_path,
        icon_color,
        icon_color_hover,
        icon_color_pressed,
        context_color,
        radius=8,
    ):
        super().__init__()

        self._text_title = text_title
        self._text_title_size = text_title_size
        self._text_title_color = text_title_color
        self._icon_path = icon_path
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._btn_color = btn_color
        self._btn_color_hover = btn_color_hover
        self._btn_color_pressed = btn_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._context_color = context_color
        self._radius = radius

        self.setup_ui()

        self.menus = Ui_RightColumn()
        self.menus.setupUi(self.content_frame)

    def setup_ui(self):
        """
        Set up the user interface for the title bar.
        """
        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)

        self.title_frame = QFrame()
        self.title_frame.setMaximumHeight(47)
        self.title_frame.setMinimumHeight(47)

        self.title_base_layout = QVBoxLayout(self.title_frame)
        self.title_base_layout.setContentsMargins(5, 3, 5, 3)

        self.title_bg_frame = QFrame()
        self.title_bg_frame.setObjectName("title_bg_frame")
        self.title_bg_frame.setStyleSheet(
            f"""
        #title_bg_frame {{
            background-color: {self._bg_color};
            border-radius: {self._radius}px;
        }}
        """
        )

        self.title_bg_layout = QHBoxLayout(self.title_bg_frame)
        self.title_bg_layout.setContentsMargins(5, 5, 5, 5)
        self.title_bg_layout.setSpacing(3)

        self.icon_frame = QFrame()
        self.icon_frame.setFixedSize(30, 30)
        self.icon_frame.setStyleSheet("background: none;")
        self.icon_layout = QVBoxLayout(self.icon_frame)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_layout.setSpacing(5)
        self.icon = PyIcon(self._icon_path, self._icon_color)
        self.icon_layout.addWidget(self.icon, Qt.AlignCenter, Qt.AlignCenter)

        self.title_label = QLabel(self._text_title)
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet(
            f"""
        #title_label {{
            font-size: {self._text_title_size}pt;
            color: {self._text_title_color};
            padding-bottom: 2px;
            background: none;
        }}
        """
        )

        self.title_bg_layout.addWidget(self.icon_frame)
        self.title_bg_layout.addWidget(self.title_label)

        self.title_base_layout.addWidget(self.title_bg_frame)

        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background: none")

        self.base_layout.addWidget(self.title_frame)
        self.base_layout.addWidget(self.content_frame)
