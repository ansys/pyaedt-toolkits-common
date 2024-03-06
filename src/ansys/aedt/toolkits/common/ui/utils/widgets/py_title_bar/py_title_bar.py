from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ansys.aedt.toolkits.common.ui.utils.images.load_images import LoadImages
from ansys.aedt.toolkits.common.ui.utils.widgets.py_div.py_div import PyDiv

from .py_title_button import PyTitleButton

_is_maximized = False
_old_size = QSize()


class PyTitleBar(QWidget):
    """
    Custom title bar for the application window.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    app_parent : QWidget
        The main application window.
    logo_image : str, optional
        The path to the logo image file, by default "ansys-primary-logo-white.svg".
    logo_width : int, optional
        The width of the logo, by default 10.
    dark_one : str, optional
        The color for the dark theme, by default "#1b1e23".
    bg_color : str, optional
        The background color, by default "#343b48".
    div_color : str, optional
        The color for dividers, by default "#3c4454".
    btn_bg_color : str, optional
        The background color for buttons, by default "#343b48".
    btn_bg_color_hover : str, optional
        The background color for buttons on hover, by default "#3c4454".
    btn_bg_color_pressed : str, optional
        The background color for buttons on pressed state, by default "#2c313c".
    icon_color : str, optional
        The default icon color, by default "#c3ccdf".
    icon_color_hover : str, optional
        The icon color on hover, by default "#dce1ec".
    icon_color_pressed : str, optional
        The icon color on pressed state, by default "#edf0f5".
    icon_color_active : str, optional
        The icon color for the active state, by default "#f5f6f9".
    context_color : str, optional
        The context color, by default "#6c99f4".
    text_foreground : str, optional
        The text color, by default "#8a95aa".
    radius : int, optional
        The border radius, by default 8.
    font_family : str, optional
        The font family, by default "Segoe UI".
    title_size : int, optional
        The font size for the title, by default 10.
    """

    clicked = Signal(object)
    released = Signal(object)

    def __init__(
        self,
        parent,
        app_parent,
        logo_image="ansys-primary-logo-white.svg",
        logo_width=10,
        dark_one="#1b1e23",
        bg_color="#343b48",
        div_color="#3c4454",
        btn_bg_color="#343b48",
        btn_bg_color_hover="#3c4454",
        btn_bg_color_pressed="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        context_color="#6c99f4",
        text_foreground="#8a95aa",
        radius=8,
        font_family="Segoe UI",
        title_size=10,
    ):
        super().__init__(parent)

        self._images_load = LoadImages()
        self._logo_image = logo_image
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._div_color = div_color
        self._parent = parent
        self._app_parent = app_parent
        self._btn_bg_color = btn_bg_color
        self._btn_bg_color_hover = btn_bg_color_hover
        self._btn_bg_color_pressed = btn_bg_color_pressed
        self._context_color = context_color
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._font_family = font_family
        self._title_size = title_size
        self._text_foreground = text_foreground

        self.setup_ui()

        self.bg.setStyleSheet(f"background-color: {bg_color}; border-radius: {radius}px;")

        self.top_logo.setMinimumWidth(logo_width)
        self.top_logo.setMaximumWidth(logo_width)

        def moveWindow(event):
            if parent.isMaximized():
                self.maximize_restore()
                # self.resize(_old_size)
                curso_x = parent.pos().x()
                curso_y = event.globalPos().y() - QCursor.pos().y()
                parent.move(curso_x, curso_y)

            if event.buttons() == Qt.LeftButton:
                if getattr(parent.dragPos, "toPoint", None):
                    print(parent.pos())
                    print(event.scenePosition().toPoint())
                    print(parent.dragPos.toPoint())
                    parent.move(parent.pos() + event.scenePosition().toPoint() - parent.dragPos.toPoint())
                else:
                    parent.move(parent.pos() + event.scenePosition().toPoint() - parent.dragPos)
                parent.dragPos = event.scenePosition().toPoint()
                event.accept()

        self.bg_layout.addWidget(self.top_logo)
        self.bg_layout.addWidget(self.div_1)
        self.bg_layout.addWidget(self.title_label)
        self.bg_layout.addWidget(self.div_2)

        self.minimize_button.released.connect(lambda: parent.showMinimized())
        self.maximize_restore_button.released.connect(lambda: self.maximize_restore())
        self.close_button.released.connect(lambda: parent.close())

        self.bg_layout.addLayout(self.custom_buttons_layout)

    def add_menus(self, parameters):
        """
        Add custom menus to the title bar.

        Parameters
        ----------
        parameters : list of dict
            List of dictionaries, each containing information about a menu button.
            Each dictionary should have the following keys:
            - btn_icon: str, the icon file for the button.
            - btn_id: str, the ID of the button.
            - btn_tooltip: str, the tooltip text for the button.
            - is_active: bool, whether the button is initially active or not.
        """
        if parameters is not None and len(parameters) > 0:
            for parameter in parameters:
                _btn_icon = self._images_load.icon_path(parameter["btn_icon"])
                _btn_id = parameter["btn_id"]
                _btn_tooltip = parameter["btn_tooltip"]
                _is_active = parameter["is_active"]

                self.menu = PyTitleButton(
                    self._parent,
                    self._app_parent,
                    btn_id=_btn_id,
                    tooltip_text=_btn_tooltip,
                    dark_one=self._dark_one,
                    bg_color=self._bg_color,
                    bg_color_hover=self._btn_bg_color_hover,
                    bg_color_pressed=self._btn_bg_color_pressed,
                    icon_color=self._icon_color,
                    icon_color_hover=self._icon_color_active,
                    icon_color_pressed=self._icon_color_pressed,
                    icon_color_active=self._icon_color_active,
                    context_color=self._context_color,
                    text_foreground=self._text_foreground,
                    icon_path=_btn_icon,
                    is_active=_is_active,
                )
                self.menu.clicked.connect(self.btn_clicked)
                self.menu.released.connect(self.btn_released)

                self.custom_buttons_layout.addWidget(self.menu)

    def btn_clicked(self):
        """
        Handle the button click event.
        """
        self.clicked.emit(self.menu)

    def btn_released(self):
        """
        Handle the button release event.
        """
        self.released.emit(self.menu)

    def set_title(self, title):
        """
        Set the title of the application.

        Parameters
        ----------
        title : str
            The title to be set.
        """
        self.title_label.setText(title)

    def maximize_restore(self):
        """
        Maximize or restore the application window.
        """
        global _is_maximized
        global _old_size

        def change_ui():
            if _is_maximized:
                self._parent.ui.main_window_layout.setContentsMargins(0, 0, 0, 0)
                self._parent.ui.main_window.set_stylesheet(border_radius=0, border_size=0)
                self.maximize_restore_button.set_icon(self._images_load.icon_path("icon_restore.svg"))
            else:
                self._parent.ui.main_window_layout.setContentsMargins(10, 10, 10, 10)
                self._parent.ui.main_window.set_stylesheet(border_radius=10, border_size=2)
                self.maximize_restore_button.set_icon(self._images_load.icon_path("icon_maximize.svg"))

        # CHECK EVENT
        if self._parent.isMaximized():
            _is_maximized = False
            self._parent.showNormal()
            change_ui()
        else:
            _is_maximized = True
            _old_size = QSize(self._parent.width(), self._parent.height())
            self._parent.showMaximized()
            change_ui()

    def setup_ui(self):
        """
        Set up the user interface for the title bar.
        """
        self.title_bar_layout = QVBoxLayout(self)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.bg = QFrame()

        self.bg_layout = QHBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(10, 0, 5, 0)
        self.bg_layout.setSpacing(0)

        self.div_1 = PyDiv(self._div_color)
        self.div_2 = PyDiv(self._div_color)
        self.div_3 = PyDiv(self._div_color)

        self.top_logo = QLabel()
        self.top_logo_layout = QVBoxLayout(self.top_logo)
        self.top_logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_svg = QSvgWidget()
        self.logo_svg.load(self._images_load.image_path(self._logo_image))
        self.top_logo_layout.addWidget(self.logo_svg, Qt.AlignCenter, Qt.AlignCenter)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.title_label.setStyleSheet(f'font: {self._title_size}pt "{self._font_family}"')

        self.custom_buttons_layout = QHBoxLayout()
        self.custom_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_buttons_layout.setSpacing(3)

        self.minimize_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text="Close app",
            dark_one=self._dark_one,
            bg_color=self._btn_bg_color,
            bg_color_hover=self._btn_bg_color_hover,
            bg_color_pressed=self._btn_bg_color_pressed,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            radius=6,
            icon_path=self._images_load.icon_path("icon_minimize.svg"),
        )

        self.maximize_restore_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text="Maximize app",
            dark_one=self._dark_one,
            bg_color=self._btn_bg_color,
            bg_color_hover=self._btn_bg_color_hover,
            bg_color_pressed=self._btn_bg_color_pressed,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            radius=6,
            icon_path=self._images_load.icon_path("icon_maximize.svg"),
        )

        self.close_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text="Close app",
            dark_one=self._dark_one,
            bg_color=self._btn_bg_color,
            bg_color_hover=self._btn_bg_color_hover,
            bg_color_pressed=self._context_color,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_active,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            radius=6,
            icon_path=self._images_load.icon_path("icon_close.svg"),
        )

        self.title_bar_layout.addWidget(self.bg)
