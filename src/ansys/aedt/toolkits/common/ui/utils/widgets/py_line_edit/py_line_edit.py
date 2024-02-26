from PySide6.QtWidgets import QLineEdit

from ansys.aedt.toolkits.common.ui.utils.widgets.py_line_edit.styles import Styles


class PyLineEdit(QLineEdit):
    """
    Custom QLineEdit widget with enhanced styling.

    Parameters
    ----------
    text : str, optional
        The initial text for the line edit. Default is an empty string.
    place_holder_text : str, optional
        The placeholder text to be displayed when the line edit is empty. Default is an empty string.
    radius : int, optional
        The border radius of the line edit. Default is 8.
    border_size : int, optional
        The border size of the line edit. Default is 2.
    color : str, optional
        The text color of the line edit. Default is "#FFF" (white).
    selection_color : str, optional
        The text selection color of the line edit. Default is "#FFF" (white).
    bg_color : str, optional
        The background color of the line edit. Default is "#333" (dark gray).
    bg_color_active : str, optional
        The background color of the line edit when active. Default is "#222" (darker gray).
    context_color : str, optional
        The color representing a context or active state. Default is "#00ABE8" (blue).

    """

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
        context_color="#00ABE8",
    ):
        super().__init__()

        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        self.set_stylesheet(radius, border_size, color, selection_color, bg_color, bg_color_active, context_color)

    def set_stylesheet(self, radius, border_size, color, selection_color, bg_color, bg_color_active, context_color):
        """
        Set the stylesheet for the PyLineEdit.

        Parameters
        ----------
        radius : int
            Border radius of the line edit.
        border_size : int
            Border size of the line edit.
        color : str
            Text color of the line edit.
        selection_color : str
            Text selection color of the line edit.
        bg_color : str
            Background color of the line edit.
        bg_color_active : str
            Background color when the line edit is active.
        context_color : str
            Color representing a context or active state.

        """
        style_format = Styles.style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color,
        )
        self.setStyleSheet(style_format)
