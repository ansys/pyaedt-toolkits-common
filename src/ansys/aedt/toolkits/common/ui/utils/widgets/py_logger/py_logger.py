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

from PySide6.QtGui import QFont
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QTextEdit


class PyLogger(QTextEdit):
    """
    Logger widget.

    Inherits QTextEdit and provides a simple interface for logging strings.

    Parameters
    ----------
    text_color : str, optional
        Text color. The default is ``"#f5f6f9"``.
    background_color: str, optional
        Color of background. The default is ``"#000000"``.
    font_size: float or int, optional
        Font size. The default is ``10``.
    font_family: str, optional
        Font size. The default is ``"Segoe UI``".
    height: float or int
        Logger height. The default is ``10``.
    """

    def __init__(
        self, text_color="#f5f6f9", background_color="#000000", font_size=10, font_family="Segoe UI", height=50
    ):
        super().__init__()
        self.setReadOnly(True)
        font = (QFont(font_family, font_size),)
        self.setFont(font)
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color}")
        self.setFixedHeight(height)
        self._font_size = font_size
        self._font_family = font_family

    def log(self, message):
        """
        Logs a message to the widget.

        Parameters:
            message: The string message to log.
        """
        self.append(message)

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
