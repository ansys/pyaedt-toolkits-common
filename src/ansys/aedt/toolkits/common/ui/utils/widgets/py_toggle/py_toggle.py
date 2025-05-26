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

from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QCheckBox


class PyToggle(QCheckBox):
    """
    Customizable toggle switch.

    Inherits QCheckBox and provides a customizable toggle switch with options
    for width, background color, circle color, active color, and animation curve.

    Parameters
    ----------
    width : int, optional
        Width of the toggle switch. The default is ``50``.
    bg_color : str, optional
        Background color of the toggle switch. The default is ``"#777"``.
    circle_color : str, optional
        Color of the circle in the toggle switch. The default is ``"#DDD"``.
    active_color : str, optional
        Color of the toggle switch when active. The default is ``"#00BCFF"``.
    text_color : str, optional
        Color of the toggle text. The default is ``"#FFFFFF"``.
    show_on_off: bool, optional
        Show on and off text in the toggle. The default value is ``False``.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import QApplication
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import PyToggle

    >>> class MyApp(QWidget):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.toggle = PyToggle()
    ...         self.toggle.stateChanged.connect(self.toggle_state_changed)
    ...         self.toggle.show()

    ...     def toggle_state_changed(self, state):
    ...         print("Toggle State:", state)

    >>> if __name__ == "__main__":
    ...     app = QApplication([])
    ...     window = MyApp()
    ...     sys.exit(app.exec())
    """

    def __init__(
        self,
        width=50,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCFF",
        text_color_on="#FFFFFF",
        text_color_off="#FFFFFF",
        show_on_off=False,
    ):
        QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color
        self._text_color_on = text_color_on
        self._text_color_off = text_color_off
        self._show_on_off = show_on_off

    def hitButton(self, pos: QPoint):
        """
        Determine if a button press occurred within the toggle switch.

        Parameters
        ----------
        pos : QPoint
            The position of the button press.

        Returns
        -------
        bool
            True if the button press occurred within the toggle switch, False otherwise.
        """
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(QFont("Segoe UI", 9, QFont.Bold))

        rect = QRect(0, 0, self.width(), self.height())
        p.setPen(Qt.NoPen)

        # Circle settings
        circle_diameter = self.height() - 6
        y_pos = (self.height() - circle_diameter) // 2
        margin = 6  # Margin from the edge of toggle

        if not self.isChecked():
            # Draw background
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(rect, self.height() / 2, self.height() / 2)

            # Draw circle (left)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(margin, y_pos, circle_diameter, circle_diameter)

            if self._show_on_off:
                # Draw OFF text (right side, but not near the circle)
                p.setPen(QColor(self._text_color_off))  # Customize color
                circle_right = margin + circle_diameter
                text_rect = QRect(circle_right, 0, self.width() - circle_right - 12, self.height())
                p.drawText(text_rect, Qt.AlignVCenter | Qt.AlignRight, "OFF")
        else:
            # Draw background
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(rect, self.height() / 2, self.height() / 2)

            # Draw circle (right)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self.width() - circle_diameter - margin, y_pos, circle_diameter, circle_diameter)

            # Draw ON text (left side, not near the circle)
            if self._show_on_off:
                p.setPen(QColor(self._text_color_on))
                text_rect = QRect(10, 0, 50, self.height())
                p.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, "ON")

        p.end()
