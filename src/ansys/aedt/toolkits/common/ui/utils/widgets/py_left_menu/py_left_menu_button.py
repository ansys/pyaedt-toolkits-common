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

import os

from PySide6.QtCore import QEvent
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton

from ansys.aedt.toolkits.common.ui.utils.images.load_images import LoadImages


class PyLeftMenuButton(QPushButton):
    def __init__(
        self,
        app_parent,
        text,
        btn_id=None,
        tooltip_text="",
        margin=4,
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
        icon_path="icon_add_user.svg",
        icon_active_menu="active_menu.svg",
        is_active=False,
        is_active_tab=False,
        is_toggle_active=False,
    ):
        super().__init__()
        self._images_load = LoadImages()
        self.setText(text)
        self.setCursor(Qt.PointingHandCursor)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setObjectName(btn_id)

        self._icon_path = self._images_load.icon_path(icon_path)
        self._icon_active_menu = self._images_load.icon_path(icon_active_menu)

        self._margin = margin
        self._dark_one = dark_one
        self._dark_three = dark_three
        self._dark_four = dark_four
        self._bg_one = bg_one
        self._context_color = context_color
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._set_icon_color = self._icon_color
        self._set_bg_color = self._dark_one
        self._set_text_foreground = text_foreground
        self._set_text_active = text_active
        self._parent = app_parent
        self._is_active = is_active
        self._is_active_tab = is_active_tab
        self._is_toggle_active = is_toggle_active

        self._tooltip_text = tooltip_text
        self.tooltip = _ToolTip(app_parent, tooltip_text, dark_one, context_color, text_foreground)
        self.tooltip.hide()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setFont(self.font())

        rect = QRect(4, 5, self.width(), self.height() - 10)
        rect_inside = QRect(4, 5, self.width() - 8, self.height() - 10)
        rect_icon = QRect(0, 0, 50, self.height())
        rect_blue = QRect(4, 5, 20, self.height() - 10)
        rect_inside_active = QRect(7, 5, self.width(), self.height() - 10)
        rect_text = QRect(45, 0, self.width() - 50, self.height())

        if self._is_active:
            p.setBrush(QColor(self._context_color))
            p.drawRoundedRect(rect_blue, 8, 8)

            p.setBrush(QColor(self._bg_one))
            p.drawRoundedRect(rect_inside_active, 8, 8)

            icon_path = self._icon_active_menu
            app_path = os.path.abspath(os.getcwd())
            icon_path = os.path.normpath(os.path.join(app_path, icon_path))
            self._set_icon_color = self._icon_color_active
            self.icon_active(p, icon_path, self.width())

            p.setPen(QColor(self._set_text_active))
            p.drawText(rect_text, Qt.AlignVCenter, self.text())

            # DRAW ICONS
            self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)

        elif self._is_active_tab:
            p.setBrush(QColor(self._dark_four))
            p.drawRoundedRect(rect_blue, 8, 8)

            p.setBrush(QColor(self._bg_one))
            p.drawRoundedRect(rect_inside_active, 8, 8)

            icon_path = self._icon_active_menu
            app_path = os.path.abspath(os.getcwd())
            icon_path = os.path.normpath(os.path.join(app_path, icon_path))
            self._set_icon_color = self._icon_color_active
            self.icon_active(p, icon_path, self.width())

            p.setPen(QColor(self._set_text_active))
            p.drawText(rect_text, Qt.AlignVCenter, self.text())

            self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)

        # NORMAL BG
        else:
            if self._is_toggle_active:
                # BG INSIDE
                p.setBrush(QColor(self._dark_three))
                p.drawRoundedRect(rect_inside, 8, 8)

                # DRAW TEXT
                p.setPen(QColor(self._set_text_foreground))
                p.drawText(rect_text, Qt.AlignVCenter, self.text())

                # DRAW ICONS
                if self._is_toggle_active:
                    self.icon_paint(p, self._icon_path, rect_icon, self._context_color)
                else:
                    self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)
            else:
                # BG INSIDE
                p.setBrush(QColor(self._set_bg_color))
                p.drawRoundedRect(rect_inside, 8, 8)

                # DRAW TEXT
                p.setPen(QColor(self._set_text_foreground))
                p.drawText(rect_text, Qt.AlignVCenter, self.text())

                # DRAW ICONS
                self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)

        p.end()

    def set_active(self, is_active):
        self._is_active = is_active
        if not is_active:
            self._set_icon_color = self._icon_color
            self._set_bg_color = self._dark_one

        self.repaint()

    def set_active_tab(self, is_active):
        self._is_active_tab = is_active
        if not is_active:
            self._set_icon_color = self._icon_color
            self._set_bg_color = self._dark_one

        self.repaint()

    def is_active(self):
        return self._is_active

    def is_active_tab(self):
        return self._is_active_tab

    def set_active_toggle(self, is_active):
        self._is_toggle_active = is_active

    def set_icon(self, icon_path):
        self._icon_path = icon_path
        self.repaint()

    def icon_paint(self, qp, image, rect, color):
        icon = QPixmap(image)
        # if icons are not 30x30, they will be scaled
        icon = icon.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap((rect.width() - icon.width()) / 2, (rect.height() - icon.height()) / 2, icon)
        painter.end()

    def icon_active(self, qp, image, width):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), self._bg_one)
        qp.drawPixmap(width - 5, 0, icon)
        painter.end()

    def change_style(self, event):
        if event == QEvent.Enter:
            if not self._is_active:
                self._set_icon_color = self._icon_color_hover
                self._set_bg_color = self._dark_three
            self.repaint()
        elif event == QEvent.Leave:
            if not self._is_active:
                self._set_icon_color = self._icon_color
                self._set_bg_color = self._dark_one
            self.repaint()
        elif event == QEvent.MouseButtonPress:
            if not self._is_active:
                self._set_icon_color = self._context_color
                self._set_bg_color = self._dark_four
            self.repaint()
        elif event == QEvent.MouseButtonRelease:
            if not self._is_active:
                self._set_icon_color = self._icon_color_hover
                self._set_bg_color = self._dark_three
            self.repaint()

    def enterEvent(self, event):
        self.change_style(QEvent.Enter)
        if self.width() == 50 and self._tooltip_text:
            self.move_tooltip()
            self.tooltip.show()

    def leaveEvent(self, event):
        self.change_style(QEvent.Leave)
        self.tooltip.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonPress)
            self.tooltip.hide()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonRelease)
            return self.released.emit()

    def move_tooltip(self):
        # GET MAIN WINDOW PARENT
        gp = self.mapToGlobal(QPoint(0, 0))

        # SET WIDGET TO GET POSITION
        # Return absolute position of widget inside app
        pos = self._parent.mapFromGlobal(gp)

        # FORMAT POSITION
        # Adjust tooltip position with offset
        pos_x = pos.x() + self.width() + 5
        pos_y = pos.y() + (self.width() - self.tooltip.height()) // 2

        # SET POSITION TO WIDGET
        # Move tooltip position
        self.tooltip.move(pos_x, pos_y)


class _ToolTip(QLabel):
    # TOOLTIP / LABEL StyleSheet
    style_tooltip = """
    QLabel {{
        background-color: {_dark_one};
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-left: 3px solid {_context_color};
        font: 800 9pt "Segoe UI";
    }}
    """

    def __init__(self, parent, tooltip, dark_one, context_color, text_foreground):
        QLabel.__init__(self)

        # LABEL SETUP
        style = self.style_tooltip.format(
            _dark_one=dark_one, _context_color=context_color, _text_foreground=text_foreground
        )
        self.setObjectName("label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setMinimumWidth(50)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
