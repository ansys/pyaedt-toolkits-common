from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from ansys.aedt.toolkits.common.ui.utils.widgets.py_push_button.styles import Styles


class PyPushButton(QPushButton):
    def __init__(
            self,
            text,
            radius,
            color,
            bg_color,
            bg_color_hover,
            bg_color_pressed,
            parent=None,
    ):
        super().__init__()

        self.setText(text)
        if parent is not None:
            self.setParent(parent)
        self.setCursor(Qt.PointingHandCursor)

        # SET STYLESHEET
        custom_style = Styles.style.format(
            _color=color,
            _radius=radius,
            _bg_color=bg_color,
            _bg_color_hover=bg_color_hover,
            _bg_color_pressed=bg_color_pressed
        )
        self.setStyleSheet(custom_style)
