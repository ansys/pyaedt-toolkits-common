from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

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
        font_size,
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
            _bg_color_pressed=bg_color_pressed,
            _font_size=font_size,
        )
        self.setStyleSheet(custom_style)
