from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QWidget


class PyCredits(QWidget):
    """
    Credits information widget with customizable elements.

    Inherits QWidget and includes UILabels for credits and version information,
    with customizable styles.

    Parameters
    ----------
    text : str, optional
        Copyright text to be displayed. The default is ``"© 2024 MyApp Co."``.
    version : str, optional
        Version information text to be displayed. The default is ``"0.0.1"``.
    bg : str, optional
        Background color for the widget. The default is ``"FFFFFF"``.
    font_family : str, optional
        Font family name for the text. The default is ``"Segoe UI"``.
    text_size : int, optional
        Size of the text. The default is ``9``.
    text_description_color : str, optional
        Color of the text. The default is ``"#FFFFFF"``.
    radius : int, optional
        Radius of the widget's corners. The default is ``9``.
    padding : int, optional
        Padding applied to the text in the labels. The default is ``10``.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import *
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import *

    >>> class MyApp(QMainWindow):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.credits = PyCredits()
    ...         self.credits.show()

    >>> if __name__ == "__main__":
    ...     app = QApplication([])
    ...     window = MyApp()
    ...     sys.exit(app.exec())
    """

    def __init__(
        self,
        text="© 2024 MyApp Co.",
        version="0.0.1",
        bg="#FFFFFF",
        font_family="Segoe UI",
        text_size=9,
        text_description_color="#00000",
        radius=8,
        padding=10,
    ):
        super().__init__()

        self._copyright = text
        self._version = version
        self._bg = bg
        self._font_family = font_family
        self._text_size = text_size
        self._text_description_color = text_description_color
        self._radius = radius
        self._padding = padding

        self._setup_ui()

    def _setup_ui(self):
        """
        Setup and configure UI components.
        """
        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)

        style = f"""
        #bg_frame {{
            border-radius: {self._radius}px;
            background-color: {self._bg};
        }}
        .QLabel {{
            font: {self._text_size}pt "{self._font_family}";
            color: {self._text_description_color};
            padding-left: {self._padding}px;
            padding-right: {self._padding}px;
        }}
        """

        # Frame for credits
        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(style)

        # Add frame to layout
        self.widget_layout.addWidget(self.bg_frame)

        self.bg_layout = QHBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)

        self.copyright_label = QLabel(self._copyright)
        self.copyright_label.setAlignment(Qt.AlignVCenter)

        # Label for version
        self.version_label = QLabel(self._version)
        self.version_label.setAlignment(Qt.AlignVCenter)

        # Separator between copyright and version information
        self.separator = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add widgets to layout
        self.bg_layout.addWidget(self.copyright_label)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.version_label)
