from PySide6.QtWidgets import *

style = """
/* HORIZONTAL */
QSlider {{ margin: {_margin}px; }}
QSlider::groove:horizontal {{
    border-radius: {_bg_radius}px;
    height: {_bg_size}px;
	margin: 0px;
	background-color: {_bg_color};
}}
QSlider::groove:horizontal:hover {{ background-color: {_bg_color_hover}; }}
QSlider::handle:horizontal {{
    border: none;
    height: {_handle_size}px;
    width: {_handle_size}px;
    margin: {_handle_margin}px;
	border-radius: {_handle_radius}px;
    background-color: {_handle_color};
}}
QSlider::handle:horizontal:hover {{ background-color: {_handle_color_hover}; }}
QSlider::handle:horizontal:pressed {{ background-color: {_handle_color_pressed}; }}

/* VERTICAL */
QSlider::groove:vertical {{
    border-radius: {_bg_radius}px;
    width: {_bg_size}px;
    margin: 0px;
	background-color: {_bg_color};
}}
QSlider::groove:vertical:hover {{ background-color: {_bg_color_hover}; }}
QSlider::handle:vertical {{
	border: none;
    height: {_handle_size}px;
    width: {_handle_size}px;
    margin: {_handle_margin}px;
	border-radius: {_handle_radius}px;
    background-color: {_handle_color};
}}
QSlider::handle:vertical:hover {{ background-color: {_handle_color_hover}; }}
QSlider::handle:vertical:pressed {{ background-color: {_handle_color_pressed}; }}
"""

class PySlider(QSlider):
    def __init__(
        self,
        margin = 0,
        bg_size = 20,
        bg_radius = 10,
        bg_color = "#1b1e23",
        bg_color_hover = "#1e2229",
        handle_margin = 2,
        handle_size = 16,
        handle_radius = 8,
        handle_color = "#568af2",
        handle_color_hover = "#6c99f4",
        handle_color_pressed = "#3f6fd1"
    ):
        super(PySlider, self).__init__()

        # FORMAT STYLE
        # ///////////////////////////////////////////////////////////////
        adjust_style = style.format(
            _margin = margin,
            _bg_size = bg_size,
            _bg_radius = bg_radius,
            _bg_color = bg_color,
            _bg_color_hover = bg_color_hover,
            _handle_margin = handle_margin,
            _handle_size = handle_size,
            _handle_radius = handle_radius,
            _handle_color = handle_color,
            _handle_color_hover = handle_color_hover,
            _handle_color_pressed = handle_color_pressed
        )

        # APPLY CUSTOM STYLE
        # ///////////////////////////////////////////////////////////////
        self.setStyleSheet(adjust_style)