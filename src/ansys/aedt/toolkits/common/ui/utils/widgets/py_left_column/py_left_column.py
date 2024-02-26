from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ansys.aedt.toolkits.common.ui.utils.ui_templates.columns.ui_left_column import Ui_LeftColumn
from ansys.aedt.toolkits.common.ui.utils.widgets.py_icon.py_icon import PyIcon
from ansys.aedt.toolkits.common.ui.utils.widgets.py_left_column.py_left_button import PyLeftButton


class PyLeftColumn(QWidget):
    """
    Custom widget representing a left column with a title, an icon, and a close button.

    Parameters
    ----------
    text_title : str
        The title text for the left column.
    text_title_size : int
        The font size of the title text.
    text_title_color : str
        The color of the title text.
    dark_one : str
        Color representing a dark shade.
    bg_color : str
        Background color of the left column.
    btn_color : str
        Color of the close button.
    btn_color_hover : str
        Color of the close button when hovered.
    btn_color_pressed : str
        Color of the close button when pressed.
    icon_path : str
        Path to the icon image file.
    icon_color : str
        Color of the icon.
    icon_color_hover : str
        Color of the icon when hovered.
    icon_color_pressed : str
        Color of the icon when pressed.
    context_color : str
        Color representing a context or active state.
    icon_close_path : str
        Path to the close icon image file.
    radius : int
        Border radius of the left column.
    """

    clicked = Signal(object, name="left_column_clicked")
    released = Signal(object, name="left_column_released")

    def __init__(
        self,
        text_title="Title",
        text_title_size=10,
        text_title_color="#343b48",
        dark_one="#1b1e23",
        bg_color="#343b48",
        btn_color="#c3ccdf",
        btn_color_hover="#3c4454",
        btn_color_pressed="#2c313c",
        icon_path="no_icon.svg",
        icon_color="#343b48",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        context_color="#dce1ec",
        icon_close_path="no_icon.svg",
        radius=8,
    ):
        super().__init__()
        self._text_title = text_title
        self._text_title_size = text_title_size
        self._text_title_color = text_title_color
        self._icon_path = icon_path
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._btn_color = btn_color
        self._btn_color_hover = btn_color_hover
        self._btn_color_pressed = btn_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._context_color = context_color
        self._icon_close_path = icon_close_path
        self._radius = radius

        self.setup_ui()

        self.menus = Ui_LeftColumn()
        self.menus.setupUi(self.content_frame)

        self.btn_close.clicked.connect(self.btn_clicked)
        self.btn_close.released.connect(self.btn_released)

    def btn_clicked(self):
        """
        Emit signal when the close button is clicked.
        """
        self.clicked.emit(self.btn_close)

    def btn_released(self):
        """
        Emit signal when the close button is released.
        """
        self.released.emit(self.btn_close)

    def setup_ui(self):
        """
        Set up the user interface for the left column.
        """
        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)

        self.title_frame = QFrame()
        self.title_frame.setMaximumHeight(47)
        self.title_frame.setMinimumHeight(47)

        self.title_base_layout = QVBoxLayout(self.title_frame)
        self.title_base_layout.setContentsMargins(5, 3, 5, 3)

        self.title_bg_frame = QFrame()
        self.title_bg_frame.setObjectName("title_bg_frame")
        self.title_bg_frame.setStyleSheet(
            f"""
        #title_bg_frame {{
            background-color: {self._bg_color};
            border-radius: {self._radius}px;
        }}
        """
        )

        self.title_bg_layout = QHBoxLayout(self.title_bg_frame)
        self.title_bg_layout.setContentsMargins(5, 5, 5, 5)
        self.title_bg_layout.setSpacing(3)

        self.icon_frame = QFrame()
        self.icon_frame.setFixedSize(30, 30)
        self.icon_frame.setStyleSheet("background: none;")
        self.icon_layout = QVBoxLayout(self.icon_frame)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_layout.setSpacing(5)
        self.icon = PyIcon(self._icon_path, self._icon_color)
        self.icon_layout.addWidget(self.icon, Qt.AlignCenter, Qt.AlignCenter)

        self.title_label = QLabel(self._text_title)
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet(
            f"""
        #title_label {{
            font-size: {self._text_title_size}pt;
            color: {self._text_title_color};
            padding-bottom: 2px;
            background: none;
        }}
        """
        )

        self.btn_frame = QFrame()
        self.btn_frame.setFixedSize(30, 30)
        self.btn_frame.setStyleSheet("background: none;")

        self.btn_close = PyLeftButton(
            dark_one=self._dark_one,
            bg_color=self._btn_color,
            bg_color_hover=self._btn_color_hover,
            bg_color_pressed=self._btn_color_pressed,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_pressed,
            context_color=self._context_color,
            text_foreground=self._text_title_color,
            icon_path=self._icon_close_path,
            radius=6,
        )
        self.btn_close.setParent(self.btn_frame)
        self.btn_close.setObjectName("close_left_column")

        self.title_bg_layout.addWidget(self.icon_frame)
        self.title_bg_layout.addWidget(self.title_label)
        self.title_bg_layout.addWidget(self.btn_frame)

        self.title_base_layout.addWidget(self.title_bg_frame)

        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background: none")

        self.base_layout.addWidget(self.title_frame)
        self.base_layout.addWidget(self.content_frame)
