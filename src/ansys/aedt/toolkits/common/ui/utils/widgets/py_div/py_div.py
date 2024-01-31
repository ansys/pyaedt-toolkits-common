from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QWidget


class PyDiv(QWidget):
    """
    Vertical divider widget with customizable elements.

    Parameters
    ----------
    color : str, optional
        The color of the divider in hex color code. The default is ``"#000000"``.
    height : float, optional
        Divider height. The default is ``0``.
    width : float, optional
        Divider width. The default is ``20``.

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
    >>>         layout.addWidget(PyDiv("#FF0000", 20))
    >>>         layout.addWidget(QPushButton("Button 2"))

    >>> if __name__ == "__main__":
    >>>     app = QApplication([])
    >>>     window = Example()
    >>>     window.show()
    >>>     app.exec()
    """

    def __init__(self, color="#000000", height=0, width=20):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)
        self.frame_line = QFrame()
        self.frame_line.setStyleSheet(f"background: {color};")
        self.frame_line.setMaximumWidth(width)
        self.frame_line.setMinimumWidth(width)
        self.frame_line.setMaximumHeight(height)
        self.frame_line.setMaximumHeight(height)
        self.layout.addWidget(self.frame_line)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
