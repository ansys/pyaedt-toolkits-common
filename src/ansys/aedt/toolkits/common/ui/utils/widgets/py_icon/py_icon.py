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
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class PyIcon(QWidget):
    """
    Icon widget with customizable elements.

    The icon and color can be customized during initialization.

    Parameters
    ----------
    icon_path : str
        Path to the icon image file.
    icon_color : str, optional
        The color of the icon in hex color code. The default is ``"#000000"``.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import *

    >>> class Example(QWidget):
    >>>     def __init__(self):
    >>>         super().__init__()
    >>>         layout = QVBoxLayout(self)
    >>>         layout.addWidget(QPushButton("Button 1"))
    >>>         layout.addWidget(PyIcon('path_to_icon.svg', "#FF0000"))
    >>>         layout.addWidget(QPushButton("Button 2"))

    >>> if __name__ == "__main__":
    >>>     app = QApplication([])
    >>>     window = Example()
    >>>     window.show()
    >>>     app.exec()
    """

    def __init__(self, icon_path, icon_color="#000000"):
        super().__init__()

        self._icon_path = icon_path
        self._icon_color = icon_color

        self._setup_ui()

    def _setup_ui(self):
        """
        Sets up the user interface for the PyIcon widget.
        """
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter)

        self.set_icon(self._icon_path, self._icon_color)

        self.layout.addWidget(self.icon)

    def set_icon(self, icon_path, icon_color=None):
        """
        Set icon of the PyIcon widget.

        The icon and color can be customized during initialization.

        Parameters
        ----------
        icon_path : str
            Path to the icon image file.
        icon_color : str, optional
            The color of the icon in hex color code. The default is ``"#000000"``.
        """
        color = icon_color if icon_color else self._icon_color

        icon = QPixmap(icon_path)
        icon = icon.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        painter.end()

        self.icon.setPixmap(icon)
