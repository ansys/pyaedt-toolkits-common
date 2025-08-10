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

from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ansys.aedt.toolkits.common.ui.utils.images.load_images import LoadImages
from ansys.aedt.toolkits.common.ui.utils.widgets.py_div.py_div import PyDiv
from ansys.aedt.toolkits.common.ui.utils.widgets.py_left_menu.py_left_menu_button import PyLeftMenuButton


class PyLeftMenu(QWidget):
    """
    Custom widget representing a left menu with toggle button, top and bottom layouts, and animated toggle behavior.

     Parameters
     ----------
     parent: QWidget, optional
         The parent widget.
     app_parent: QWidget, optional
         The parent widget of the application.
     dark_one: str, optional
         Color representing a dark shade.
     dark_three: str, optional
         Color representing a darker shade.
     dark_four: str, optional
         Color representing an even darker shade.
     bg_one: str, optional
         Background color of the left menu.
     icon_color: str, optional
         Color of the icons in the left menu.
     icon_color_hover: str, optional
         Color of the icons when hovered.
     icon_color_pressed: str, optional
         Color of the icons when pressed.
     icon_color_active: str, optional
         Color of the icons in an active state.
     context_color: str, optional
         Color representing a context or active state.
     text_foreground: str, optional
         Color of the text in the left menu.
     text_active: str, optional
         Color of the text in an active state.
     radius: int, optional
         Border radius of the left menu.
     minimum_width: int, optional
         Minimum width of the left menu. The default is ``50``.
     maximum_width: int, optional
         Maximum width of the left menu. The default is ``240``.
     icon_path: str, optional
         Path to the icon image file for the toggle button.
     icon_path_close: str, optional
         Path to the icon image file for the toggle button when the menu is closed.
     toggle_text: str, optional
         Text for the toggle button.
     toggle_tooltip: str, optional
         Tooltip text for the toggle button.
    """

    clicked = Signal(object)
    released = Signal(object)

    def __init__(
        self,
        parent=None,
        app_parent=None,
        dark_one="#1b1e23",
        dark_three="#21252d",
        dark_four="#272c36",
        bg_one="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        context_color="#568af2",
        text_foreground="#8a95aa",
        text_active="#dce1ec",
        radius=8,
        minimum_width=50,
        maximum_width=240,
        icon_path="icon_menu.svg",
        icon_path_close="icon_menu_close.svg",
        toggle_text="Hide Menu",
        toggle_tooltip="Show menu",
    ):
        super().__init__(parent)
        self._images_load = LoadImages()
        self._dark_one = dark_one
        self._dark_three = dark_three
        self._dark_four = dark_four
        self._bg_one = bg_one
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._text_foreground = text_foreground
        self._text_active = text_active
        self._radius = radius
        self._minimum_width = minimum_width
        self._maximum_width = maximum_width
        self._icon_path = self._images_load.icon_path(icon_path)
        self._icon_path_close = self._images_load.icon_path(icon_path_close)

        self._parent = parent
        self._app_parent = app_parent

        self.setup_ui()

        self.bg.setStyleSheet(f"background: {dark_one}; border-radius: {radius};")

        self.toggle_button = PyLeftMenuButton(
            app_parent,
            text=toggle_text,
            tooltip_text=toggle_tooltip,
            dark_one=self._dark_one,
            dark_three=self._dark_three,
            dark_four=self._dark_four,
            bg_one=self._bg_one,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_active,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            text_active=self._text_active,
            icon_path=icon_path,
        )
        self.toggle_button.clicked.connect(self.toggle_animation)
        self.div_top = PyDiv(dark_four)

        self.top_layout.addWidget(self.toggle_button)
        self.top_layout.addWidget(self.div_top)

        self.div_bottom = PyDiv(dark_four)
        self.div_bottom.hide()
        self.bottom_layout.addWidget(self.div_bottom)

    def add_menus(self, parameters):
        """
        Add menus to the left menu.

        Parameters
        ----------
        parameters: list
            List of dictionaries containing parameters for each menu item.
        """
        if parameters != None:
            for parameter in parameters:
                _btn_icon = parameter["btn_icon"]
                _btn_id = parameter["btn_id"]
                _btn_text = parameter["btn_text"]
                _btn_tooltip = parameter["btn_tooltip"]
                _show_top = parameter["show_top"]
                _is_active = parameter["is_active"]

                self.menu = PyLeftMenuButton(
                    self._app_parent,
                    text=_btn_text,
                    btn_id=_btn_id,
                    tooltip_text=_btn_tooltip,
                    dark_one=self._dark_one,
                    dark_three=self._dark_three,
                    dark_four=self._dark_four,
                    bg_one=self._bg_one,
                    icon_color=self._icon_color,
                    icon_color_hover=self._icon_color_active,
                    icon_color_pressed=self._icon_color_pressed,
                    icon_color_active=self._icon_color_active,
                    context_color=self._context_color,
                    text_foreground=self._text_foreground,
                    text_active=self._text_active,
                    icon_path=_btn_icon,
                    is_active=_is_active,
                )
                self.menu.clicked.connect(self.btn_clicked)
                self.menu.released.connect(self.btn_released)

                if _show_top:
                    self.top_layout.addWidget(self.menu)
                else:
                    self.div_bottom.show()
                    self.bottom_layout.addWidget(self.menu)

    def btn_clicked(self):
        """
        Emit signal when a menu button is clicked.
        """
        self.clicked.emit(self.menu)

    def btn_released(self):
        """
        Emit signal when a menu button is released.
        """
        self.released.emit(self.menu)

    def toggle_animation(self):
        """
        Toggle animation for hiding/showing the left menu.
        """
        self.animation = QPropertyAnimation(self._parent, b"minimumWidth")
        self.animation.stop()
        if self.width() == self._minimum_width:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self._maximum_width)
            self.toggle_button.set_active_toggle(True)
            self.toggle_button.set_icon(self._icon_path_close)
        else:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self._minimum_width)
            self.toggle_button.set_active_toggle(False)
            self.toggle_button.set_icon(self._icon_path)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()

    def set_visible_button(self, widget: str, visible: bool = True):
        """
        Sets the visibility of a QPushButton widget within the UI.

        This method searches for a QPushButton widget by its object name and sets its visibility.

        Parameters
        ----------
        widget : str
            The object name of the QPushButton to modify.
        visible : bool, optional
            A boolean indicating whether the button should be visible. The default is `False`.
        """
        btn = self.findChild(QPushButton, widget)
        if btn:
            btn.setVisible(visible)

    def select_only_one(self, widget: str):
        """
        Set the active state for a specific menu button and deactivate others.

        Parameters
        ----------
        widget : str
            ID of the menu button to set as active.
        """
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active(True)
            else:
                btn.set_active(False)

    def select_only_one_tab(self, widget: str):
        """
        Set the active tab state for a specific menu button and deactivate others.

        Parameters
        ----------
        widget : str
            ID of the menu button to set as active tab.
        """
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active_tab(True)
            else:
                btn.set_active_tab(False)

    def deselect_all(self):
        """
        Deactivate all menu buttons.
        """
        for btn in self.findChildren(QPushButton):
            btn.set_active(False)

    def deselect_all_tab(self):
        """
        Deactivate all menu tabs.
        """
        for btn in self.findChildren(QPushButton):
            btn.set_active_tab(False)

    def setup_ui(self):
        """
        Set up the user interface for the left menu.
        """
        self.left_menu_layout = QVBoxLayout(self)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)

        self.bg = QFrame()

        self.top_frame = QFrame()

        self.bottom_frame = QFrame()

        self._layout = QVBoxLayout(self.bg)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.top_layout = QVBoxLayout(self.top_frame)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(1)

        self.bottom_layout = QVBoxLayout(self.bottom_frame)
        self.bottom_layout.setContentsMargins(0, 0, 0, 8)
        self.bottom_layout.setSpacing(1)

        self._layout.addWidget(self.top_frame, 0, Qt.AlignTop)
        self._layout.addWidget(self.bottom_frame, 0, Qt.AlignBottom)

        self.left_menu_layout.addWidget(self.bg)
