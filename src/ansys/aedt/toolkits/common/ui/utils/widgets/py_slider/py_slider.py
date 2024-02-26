from PySide6.QtWidgets import QSlider

from ansys.aedt.toolkits.common.ui.utils.widgets.py_slider.styles import Styles


class PySlider(QSlider):
    """
    Custom slider widget with customizable styles.

    Parameters
    ----------
    margin : int, optional
        The margin of the slider, by default 0.
    bg_size : int, optional
        The background size, by default 20.
    bg_radius : int, optional
        The background border radius, by default 10.
    bg_color : str, optional
        The background color, by default "#1b1e23".
    bg_color_hover : str, optional
        The background color on hover, by default "#1e2229".
    handle_margin : int, optional
        The margin of the slider handle, by default 2.
    handle_size : int, optional
        The size of the slider handle, by default 16.
    handle_radius : int, optional
        The border radius of the slider handle, by default 8.
    handle_color : str, optional
        The color of the slider handle, by default "#568af2".
    handle_color_hover : str, optional
        The color of the slider handle on hover, by default "#6c99f4".
    handle_color_pressed : str, optional
        The color of the slider handle when pressed, by default "#3f6fd1".
    """

    def __init__(
        self,
        margin=0,
        bg_size=20,
        bg_radius=10,
        bg_color="#1b1e23",
        bg_color_hover="#1e2229",
        handle_margin=2,
        handle_size=16,
        handle_radius=8,
        handle_color="#568af2",
        handle_color_hover="#6c99f4",
        handle_color_pressed="#3f6fd1",
    ):
        super(PySlider, self).__init__()

        adjust_style = Styles.style.format(
            _margin=margin,
            _bg_size=bg_size,
            _bg_radius=bg_radius,
            _bg_color=bg_color,
            _bg_color_hover=bg_color_hover,
            _handle_margin=handle_margin,
            _handle_size=handle_size,
            _handle_radius=handle_radius,
            _handle_color=handle_color,
            _handle_color_hover=handle_color_hover,
            _handle_color_pressed=handle_color_pressed,
        )

        self.setStyleSheet(adjust_style)
