from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter


class PyIcon(QWidget):
    """
    A custom QWidget acting as a colored icon.

    The icon and color can be customized during initialization.

    Parameters
    ----------
    icon_path : str
        Path to the icon image file.
    icon_color : str, optional
        The color of the icon in hex color code. The default is ``"#000000"``.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import *

    >>> class Example(QWidget):
    >>>     def __init__(self):
    >>>         super().__init__()
    >>>         layout = QVBoxLayout(self)
    >>>         layout.addWidget(QPushButton("Button 1"))
    >>>         layout.addWidget(PyIcon('path_to_icon.svg', "#FF0000"))
    >>>         layout.addWidget(QPushButton("Button 2"))

    >>> if __name__ == "__main__":
    >>>     app = QApplication([])
    >>>     window = Example()
    >>>     window.show()
    >>>     app.exec()
    """

    def __init__(
            self,
            icon_path,
            icon_color="#000000"
    ):
        super().__init__()

        self._icon_path = icon_path
        self._icon_color = icon_color

        self._setup_ui()

    def _setup_ui(self):
        """
        Sets up the user interface for the PyIcon widget.
        """
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter)

        self.set_icon(self._icon_path, self._icon_color)

        self.layout.addWidget(self.icon)

    def set_icon(self, icon_path, icon_color=None):
        """
        Set icon of the PyIcon widget.

        The icon and color can be customized during initialization.

        Parameters
        ----------
        icon_path : str
            Path to the icon image file.
        icon_color : str, optional
            The color of the icon in hex color code. The default is ``"#000000"``.
        """
        color = icon_color if icon_color else self._icon_color

        icon = QPixmap(icon_path)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        painter.end()

        self.icon.setPixmap(icon)
