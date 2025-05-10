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

from PySide6.QtCore import QEvent
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton


class PyLeftButton(QPushButton):
    """
    Left button widget designed to function as a left-aligned button with various style and interaction options.

    Parameters
    ----------
    btn_id : str, optional
        Button identifier.
    width : int, optional
        Button width.
    height : int, optional
        Button height.
    radius : int, optional
        Button corner radius.
    bg_color : str, optional
        Button background color.
    bg_color_hover : str, optional
        Button background color when hovered.
    bg_color_pressed : str, optional
        Button background color when pressed.
    icon_color : str, optional
        Icon color.
    icon_color_hover : str, optional
        Icon color when hovered.
    icon_color_pressed : str, optional
        Icon color when pressed.
    icon_color_active : str, optional
        Active icon color.
    icon_path : str, optional
        Path to icon file.
    dark_one : str, optional
        Dark color for theming.
    context_color : str, optional
        Context color for theming.
    text_foreground : str, optional
        Text foreground color.
    is_active : bool, optional
        Whether the button is active.

    """

    def __init__(
        self,
        btn_id=None,
        width=30,
        height=30,
        radius=8,
        bg_color="#343b48",
        bg_color_hover="#3c4454",
        bg_color_pressed="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        icon_path="no_icon.svg",
        dark_one="#1b1e23",
        context_color="#568af2",
        text_foreground="#8a95aa",
        is_active=False,
    ):
        super().__init__()

        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName(btn_id)

        self._bg_color = bg_color
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._top_margin = self.height() + 6
        self._is_active = is_active

        self._set_bg_color = bg_color
        self._set_icon_path = icon_path
        self._set_icon_color = icon_color
        self._set_border_radius = radius

    def set_active(self, is_active):
        """
        Set the active state of the button.

        Parameters
        ----------
        is_active : bool
            Whether the button is active.
        """
        self._is_active = is_active
        self.repaint()

    def is_active(self):
        """
        Check if the button is active.

        Returns
        -------
        bool
            True if the button is active, False otherwise.
        """
        return self._is_active

    def paintEvent(self, event):
        """
        Paint the button.

        Parameters
        ----------
        event : QEvent
            Paint event.
        """
        # PAINTER
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._is_active:
            brush = QBrush(QColor(self._bg_color_pressed))
        else:
            brush = QBrush(QColor(self._set_bg_color))

        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(rect, self._set_border_radius, self._set_border_radius)

        self.icon_paint(paint, self._set_icon_path, rect)

        paint.end()

    def change_style(self, event):
        """
        Change the button style based on the event type.

        Parameters
        ----------
        event : QEvent
            Event triggering the style change.
        """
        if event == QEvent.Enter:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()
        elif event == QEvent.Leave:
            self._set_bg_color = self._bg_color
            self._set_icon_color = self._icon_color
            self.repaint()
        elif event == QEvent.MouseButtonPress:
            self._set_bg_color = self._bg_color_pressed
            self._set_icon_color = self._icon_color_pressed
            self.repaint()
        elif event == QEvent.MouseButtonRelease:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()

    def enterEvent(self, event):
        """
        Handle the enter event.

        Parameters
        ----------
        event : QEvent
            Enter event.
        """
        self.change_style(QEvent.Enter)

    def leaveEvent(self, event):
        """
        Handle the leave event.

        Parameters
        ----------
        event : QEvent
            Leave event.
        """
        self.change_style(QEvent.Leave)

    def mousePressEvent(self, event):
        """
        Handle the mouse press event.

        Parameters
        ----------
        event : QEvent
            Mouse press event.
        """
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonPress)
            # SET FOCUS
            self.setFocus()
            # EMIT SIGNAL
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        """
        Handle the mouse release event.

        Parameters
        ----------
        event : QEvent
            Mouse release event.
        """
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonRelease)
            # EMIT SIGNAL
            return self.released.emit()

    def icon_paint(self, qp, image, rect):
        """
        Paint the icon on the button.

        Parameters
        ----------
        qp : QPainter
            QPainter object.
        image : str
            Path to the icon image.
        rect : QRect
            Rectangle to paint the icon within.
        """
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        if self._is_active:
            painter.fillRect(icon.rect(), self._context_color)
        else:
            painter.fillRect(icon.rect(), self._set_icon_color)
        qp.drawPixmap((rect.width() - icon.width()) / 2, (rect.height() - icon.height()) / 2, icon)
        painter.end()

    def set_icon(self, icon_path):
        """
        Set the icon for the button.

        Parameters
        ----------
        icon_path : str
            Path to the icon image file.
        """
        self._set_icon_path = icon_path
        self.repaint()
