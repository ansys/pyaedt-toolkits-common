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
