from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtWidgets import QHBoxLayout

from ansys.aedt.toolkits.common.ui.utils.widgets.py_window.styles import Styles


class PyWindow(QFrame):
    """
    Custom window frame widget with customizable styling and drop shadow effect.

    Inherits QFrame and provides a customizable window frame.

    Parameters
    ----------
    parent : QWidget
        The parent widget for this PyWindow.
    margin : int, optional
        The margin size around the window frame. Default is 0.
    spacing : int, optional
        The spacing between layout items. Default is 2.
    bg_color : str, optional
        The background color of the window frame. Default is "#2c313c".
    text_color : str, optional
        The text color of the window frame. Default is "#fff".
    text_font : str, optional
        The font of the text in the window frame. Default is "9pt 'Segoe UI'".
    border_radius : int, optional
        The border radius of the window frame corners. Default is 10.
    border_size : int, optional
        The size of the border around the window frame. Default is 2.
    border_color : str, optional
        The color of the border around the window frame. Default is "#343b48".

    """

    def __init__(
        self,
        parent,
        margin=0,
        spacing=2,
        bg_color="#2c313c",
        text_color="#fff",
        text_font="9pt 'Segoe UI'",
        border_radius=10,
        border_size=2,
        border_color="#343b48",
    ):
        super().__init__(parent)
        self.parent = parent
        self.margin = margin
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_font = text_font
        self.border_radius = border_radius
        self.border_size = border_size
        self.border_color = border_color

        self.setObjectName("pod_bg_app")

        self.set_stylesheet()

        # Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(spacing)

    def set_stylesheet(
        self, bg_color=None, border_radius=None, border_size=None, border_color=None, text_color=None, text_font=None
    ):
        """
        Sets the style sheet of the PyWindow with customizable attributes.

        Parameters
        ----------
        bg_color : str, optional
            The background color of the window frame.
        border_radius : int, optional
            The border radius of the window frame corners.
        border_size : int, optional
            The size of the border around the window frame.
        border_color : str, optional
            The color of the border around the window frame.
        text_color : str, optional
            The text color of the window frame.
        text_font : str, optional
            The font of the text in the window frame.

        Examples
        --------
        >>> import sys
        >>> from PySide6.QtWidgets import QApplication, QMainWindow
        >>> from ansys.aedt.toolkits.common.ui.utils.widgets import PyWindow

        >>> class MyApp(QMainWindow):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.window = PyWindow(self)
        ...         self.setCentralWidget(self.window)
        ...         self.show()

        >>> if __name__ == "__main__":
        ...     app = QApplication([])
        ...     window = MyApp()
        ...     sys.exit(app.exec())

        """
        # Use provided if not None else get the instance attribute
        style_args = {
            "_bg_color": bg_color or self.bg_color,
            "_border_radius": border_radius or self.border_radius,
            "_border_size": border_size or self.border_size,
            "_border_color": border_color or self.border_color,
            "_text_color": text_color or self.text_color,
            "_text_font": text_font or self.text_font,
        }

        self.setStyleSheet(Styles.bg_style.format(**style_args))

    def _addDropShadow(self) -> None:
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(self.shadow)
