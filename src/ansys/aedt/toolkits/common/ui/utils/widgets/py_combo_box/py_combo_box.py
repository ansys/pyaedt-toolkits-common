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
from PySide6.QtWidgets import QComboBox

from ansys.aedt.toolkits.common.ui.utils.widgets.py_combo_box.styles import Styles


class PyComboBox(QComboBox):
    """
    Combo box widget with customizable elements.

    Inherits QComboBox and includes customizable elements including
    text, radius, color, and background colors in different states.

    Parameters
    ----------
    text_list : list
        List of options in combo box.
    radius : int, optional
        Radius of combo box corners. The default is ``5``.
    bg_color : str, optional
        Background color of the combo box. The default is ``"#FFFFFF"``.
    bg_color_hover : str, optional
        Background color when mouse hovers over the combo box. The default is ``"#FFFFFF"``.
    text_color : str, optional
        Text color in the combo box. The default is ``"#000000"``.
    font_size : int, optional
        The font size of the text on the button.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import *
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import *

    >>> class MyApp(QMainWindow):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.combo_box = PyComboBox(text_list=['Option 1', 'Option 2'], radius=5)
    ...         self.combo_box.show()

    >>> if __name__ == "__main__":
    ...     app = QApplication([])
    ...     window = MyApp()
    ...     sys.exit(app.exec())
    """

    def __init__(
        self, text_list, radius=5, bg_color="#FFFFFF", bg_color_hover="#FFFFFF", text_color="#000000", font_size=12
    ):
        super().__init__()

        self.setCursor(Qt.PointingHandCursor)

        custom_style = Styles.bg_style.format(
            _border_radius=radius,
            _text_color=text_color,
            _bg_color=bg_color,
            _bg_color_hover=bg_color_hover,
            _font_size=font_size,
        )
        self.setStyleSheet(custom_style)

        self.addItems(text_list)
