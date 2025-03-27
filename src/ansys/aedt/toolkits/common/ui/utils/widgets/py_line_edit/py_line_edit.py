from PySide6.QtWidgets import *
from ansys.aedt.toolkits.common.ui.utils.widgets.py_line_edit.styles import Styles


class PyLineEdit(QLineEdit):
    def __init__(
            self,
            text="",
            place_holder_text="",
            radius=8,
            border_size=2,
            color="#FFF",
            selection_color="#FFF",
            bg_color="#333",
            bg_color_active="#222",
            context_color="#00ABE8"
    ):
        super().__init__()

        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color
        )

    def set_stylesheet(
            self,
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color
    ):

        style_format = Styles.style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color
        )
        self.setStyleSheet(style_format)
