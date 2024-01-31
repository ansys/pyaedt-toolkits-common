from PySide6.QtWidgets import QLabel

from ansys.aedt.toolkits.common.ui.utils.widgets.py_label.styles import Styles


class PyLabel(QLabel):
    """
    Label widget with customizable elements.

    Parameters
    ----------
    text : str, optional
        Text to be displayed on the QLabel, by default an empty string.
    color : str, optional
        Color for the text, in hex format, by default '#000000' (black).
    font_size : int, optional
        Size for the font, by default is 8.
    font_weight : str, optional
        Weight for the font, by default is 'bold'.
    """

    def __init__(self, text="", color="#000000", font_size=8, font_weight="bold"):
        super().__init__()
        text and self.setText(text)
        self.apply_stylesheet(color, font_size, font_weight)

    def apply_stylesheet(self, color, font_size, font_weight):
        """
        Apply the custom styles defined in the class to the QLabel.

        Parameters
        ----------
        color : str
            Text color for the QLabel.
        font_size : int
            Font size for the QLabel.
        font_weight : str
            Font weight for the QLabel.
        """
        self.setStyleSheet(Styles.style.format(_color=color, _font_size=font_size, _font_weight=font_weight))
