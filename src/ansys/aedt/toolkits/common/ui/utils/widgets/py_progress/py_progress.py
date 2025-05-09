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

from PySide6.QtCore import QRect
from PySide6.QtCore import QRectF
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QWidget


class PyProgress(QWidget):
    """
    A progress bar widget.

    Inherits QWidget and includes customizable elements including
    progress, background color, progress color, and width.

    Parameters
    ----------
    progress : float or int, optional
        Current progress value. The default is ``0``.
    progress_color: str, optional
        Color of progress bar. The default is ``"#ff79c6"``.
    background_color: str, optional
        Color of background. The default is ``"#151617"``.
    width: float or int
        Width of the progress bar. The default is ``10``.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import *
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets.py_progress.py_progress import PyProgress
    >>> from random import randint
    >>> from PySide6.QtCore import QTimer

    >>> class MyApp(QMainWindow):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.progress_bar = PyProgress(progress=0,
    ...                                        progress_color="#21252d",
    ...                                        background_color="#313131",
    ...                                        width=10)
    ...         timer = QTimer()
    ...         timer.timeout.connect(lambda: self.progress_bar.__setattr__("progress", randint(0, 100)))
    ...         timer.start(1000)
    ...         self.progress_bar.show()
    ...         sys.exit(app.exec())

    >>> if __name__ == "__main__":
    ...     app = QApplication([])
    ...     window = MyApp()
    ...     sys.exit(app.exec())
    """

    def __init__(
        self,
        progress=0,
        progress_color="#ff79c6",
        background_color="#151617",
        text_color="#FFFFFF",
        font_size=10,
        font_family="Segoe UI",
        width=10,
    ):
        super().__init__()
        self._progress = progress
        self._backgroundColor = QColor(background_color)
        self._progressColor = QColor(progress_color)
        self._text_color = QColor(text_color)
        self._progressWidth = width
        self._font_size = font_size
        self._font_family = font_family
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # Set the minimum size of the widget
        self.setMinimumSize(100, 100)

    @property
    def progress(self):
        """
        Get the current progress value.

        Returns
        -------
        float or int
            The current progress value.
        """
        return self._progress

    @progress.setter
    def progress(self, value):
        if 0 <= value <= 100:
            self._progress = value
            self.update()

    def paintEvent(self, e):
        """
        Paint the progress bar.

        Parameters
        ----------
        e : QPaintEvent
            Paint event.
        """
        paint = QPainter(self)
        paint.setRenderHint(QPainter.Antialiasing)

        # paint background
        bgRect = QRect(0, 0, self.width(), self.height())
        paint.fillRect(bgRect, self._backgroundColor)

        # paint circular progress bar
        paint.translate(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - self._progressWidth / 2
        pen = QPen(self._progressColor, self._progressWidth)
        paint.setPen(pen)
        rect = QRectF(-radius, -radius, 2 * radius, 2 * radius)
        paint.drawArc(rect, 90 * 16, -self._progress / 100.0 * 360 * 16)

        # draw progress text
        font = QFont(self._font_family, self._font_size)
        font.setBold(True)
        # font.setPointSize(30)
        paint.setFont(font)
        paint.setPen(self._text_color)  # You can change the text color here.
        paint.drawText(rect, Qt.AlignCenter, f"{self._progress}%")
