from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from ansys.aedt.toolkits.common.ui.utils.widgets.py_push_button.styles import Styles


class PyPushButton(QPushButton):
    """
    Initialize the PyPushButton.

    Parameters
    ----------
    text : str
        The title text for the right column.
    radius : int
        The border radius of the button.
    color : str
        The text color of the button.
    bg_color : str
        The background color of the button.
    bg_color_hover : int
        The background color of the button when hovered.
    bg_color_pressed : str
        The background color of the button when pressed.
    font_size : int
        The font size of the text on the button.
    parent : str, optional
        The parent widget. The default is None.

    """

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
