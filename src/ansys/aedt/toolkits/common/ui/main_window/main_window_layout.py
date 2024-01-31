from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ansys.aedt.toolkits.common.ui.models import general_settings
from ansys.aedt.toolkits.common.ui.utils.images.load_images import LoadImages
from ansys.aedt.toolkits.common.ui.utils.themes.json_themes import ThemeHandler
from ansys.aedt.toolkits.common.ui.utils.ui_templates.pages.ui_main_pages import Ui_MainPages
from ansys.aedt.toolkits.common.ui.utils.widgets.py_credits.py_credits import PyCredits
from ansys.aedt.toolkits.common.ui.utils.widgets.py_left_column.py_left_column import PyLeftColumn
from ansys.aedt.toolkits.common.ui.utils.widgets.py_left_menu.py_left_menu import PyLeftMenu
from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from ansys.aedt.toolkits.common.ui.utils.widgets.py_progress.py_progress import PyProgress
from ansys.aedt.toolkits.common.ui.utils.widgets.py_right_column.py_right_column import PyRightColumn
from ansys.aedt.toolkits.common.ui.utils.widgets.py_title_bar.py_title_bar import PyTitleBar
from ansys.aedt.toolkits.common.ui.utils.widgets.py_window.py_window import PyWindow

# Widgets
from ansys.aedt.toolkits.common.ui.utils.windows.common_window_utils import CommonWindowUtils


def setup_parent_ui(parent):
    """Setup UI for parent."""
    parent.setObjectName("MainWindow")
    parent.resize(*general_settings.startup_size)
    parent.setMinimumSize(*general_settings.minimum_size)


class MainWindowLayout(CommonWindowUtils):
    """Class representing the main window of the application."""

    def __init__(self, app):
        CommonWindowUtils.__init__(self)

        self.app = app

        # Load available themes
        self.themes = ThemeHandler().items

        # Load available images
        self.images_load = LoadImages()

        icon = self._load_icon()
        self.app.setWindowIcon(icon)

        # Main window init
        self.main_window_layout = None
        self.main_window = None

        # Central menu
        self.central_frame = None
        self.central_layout = None
        self.central_widget = None

        # Left menu
        self.left_menu_frame = None
        self.left_menu_layout = None
        self.left_menu = None

        # Left column
        self.left_column_frame = None
        self.left_column_layout = None
        self.left_column = None

        # Title
        self.title_bar_frame = None
        self.title_bar_layout = None
        self.title_bar = None

        # Content
        self.content_frame = None
        self.content_layout = None
        self.load_pages = None

        # Progress
        self.progress_frame = None
        self.progress_layout = None
        self.progress = None
        self.logger = None

        # Credits
        self.credits_frame = None
        self.credits_layout = None
        self.credits = None

        # Right Column
        self.right_column_frame = None
        self.right_column_layout = None
        self.right_column = None

    def setup_ui(self):
        """Setup UI for parent widget."""
        setup_parent_ui(self.app)
        self.setup_main_window()
        self.setup_central_widget()
        self.setup_title_menu()
        self.setup_content_area()
        self.setup_progress_frame()
        self.setup_credits_frame()
        self.setup_left_menu()
        self.setup_left_column()
        self.setup_right_column()

        # Add frames to main window
        if self.main_window:
            # Left menu
            self.main_window.layout.addWidget(self.left_menu_frame)
            self.main_window.layout.addWidget(self.left_column_frame)

            # Central menu
            self.central_layout.addWidget(self.title_bar_frame)
            self.central_layout.addWidget(self.content_frame)
            self.central_layout.addWidget(self.progress_frame)
            self.central_layout.addWidget(self.credits_frame)
            self.main_window.layout.addWidget(self.central_frame)

            # Right column
            self.main_window.layout.addWidget(self.right_column_frame)

            # Import to set the UI
            self.app.setCentralWidget(self.main_window)

    def setup_main_window(self):
        """Setup main window."""
        color = self.themes["app_color"]
        self.main_window_layout = QHBoxLayout()
        self.main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.main_window = PyWindow(
            parent=self.app,
            bg_color=color["bg_one"],
            border_color=color["bg_two"],
            text_color=color["text_foreground"],
            border_radius=0,
            border_size=0,
        )
        self.main_window_layout.addWidget(self.main_window)

    def setup_central_widget(self):
        """Setup central widget."""
        self.central_frame = QFrame(self.main_window)
        self.central_layout = QVBoxLayout()
        self.central_frame.setLayout(self.central_layout)
        self.central_layout.setContentsMargins(3, 3, 3, 3)
        self.central_layout.setSpacing(6)

        self.central_widget = QWidget(self.main_window)
        style = f"""
        color: {self.themes["app_color"]["text_foreground"]};
        font: {general_settings.font["text_size"]}pt "{general_settings.font["family"]}";
        """
        self.central_widget.setStyleSheet(style)
        self.central_layout.addWidget(self.central_widget)

    def setup_title_menu(self):
        self.title_bar_frame = QFrame(self.central_widget)
        self.title_bar_frame.setMinimumHeight(40)
        self.title_bar_frame.setMaximumHeight(40)
        self.title_bar_layout = QVBoxLayout()
        self.title_bar_frame.setLayout(self.title_bar_layout)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = PyTitleBar(
            parent=self.main_window,
            app_parent=self.app,
            logo_width=100,
            logo_image=self.images_load.image_path("ANSS_Title.svg"),
            bg_color=self.themes["app_color"]["bg_two"],
            div_color=self.themes["app_color"]["bg_three"],
            btn_bg_color=self.themes["app_color"]["bg_two"],
            btn_bg_color_hover=self.themes["app_color"]["bg_three"],
            btn_bg_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            context_color=self.themes["app_color"]["context_color"],
            dark_one=self.themes["app_color"]["dark_one"],
            text_foreground=self.themes["app_color"]["text_foreground"],
            radius=8,
            font_family=general_settings.font["family"],
            title_size=general_settings.font["title_size"],
        )
        self.title_bar_layout.addWidget(self.title_bar)

    def setup_progress_frame(self):
        """Setup progress frame."""
        self.progress_frame = QFrame(self.central_widget)

        progress_menu_minimum = general_settings.progress_size["minimum"]

        self.progress_layout = QHBoxLayout()
        self.progress_frame.setLayout(self.progress_layout)
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.progress_frame.setMinimumHeight(progress_menu_minimum)
        self.progress_frame.setMaximumHeight(progress_menu_minimum)

        self.progress = PyProgress(
            progress=0,
            progress_color=self.themes["app_color"]["icon_color"],
            background_color=self.themes["app_color"]["bg_one"],
            text_color=self.themes["app_color"]["text_active"],
            font_size=general_settings.font["title_size"],
            font_family=general_settings.font["family"],
            width=10,
        )

        self.logger = PyLogger(
            text_color=self.themes["app_color"]["text_active"],
            background_color=self.themes["app_color"]["bg_two"],
            height=general_settings.progress_size["maximum"],
            font_size=general_settings.font["title_size"],
            font_family=general_settings.font["family"],
        )

        self.progress_layout.addWidget(self.logger)
        self.logger.log("{} logger".format(general_settings.app_name))
        self.progress_layout.addWidget(self.progress)

    def setup_credits_frame(self):
        """Setup credits frame."""
        self.credits_frame = QFrame(self.central_widget)
        self.credits_frame.setMinimumHeight(26)
        self.credits_frame.setMaximumHeight(26)
        self.credits_layout = QVBoxLayout()
        self.credits_frame.setLayout(self.credits_layout)
        self.credits_layout.setContentsMargins(0, 0, 0, 0)
        self.credits = PyCredits(
            bg=self.themes["app_color"]["bg_two"],
            text=general_settings.copyright,
            version=general_settings.version,
            font_family=general_settings.font["family"],
            text_size=general_settings.font["text_size"],
            text_description_color=self.themes["app_color"]["text_description"],
        )
        self.credits_layout.addWidget(self.credits)

    def setup_left_menu(self):
        """Setup left menu."""
        self.left_menu_frame = QFrame(self.main_window)
        self.left_menu_layout = QHBoxLayout()
        self.left_menu_frame.setLayout(self.left_menu_layout)
        left_menu_margin = general_settings.left_menu_content_margins
        left_menu_minimum = general_settings.left_menu_size["minimum"]
        self.left_menu_frame.setMaximumSize(left_menu_minimum + (left_menu_margin * 2), 17280)
        self.left_menu_frame.setMinimumSize(left_menu_minimum + (left_menu_margin * 2), 0)
        self.left_menu_layout.setContentsMargins(left_menu_margin, left_menu_margin, left_menu_margin, left_menu_margin)
        self.left_menu = PyLeftMenu(
            parent=self.left_menu_frame,
            app_parent=self.app,
            dark_one=self.themes["app_color"]["dark_one"],
            dark_three=self.themes["app_color"]["dark_three"],
            dark_four=self.themes["app_color"]["dark_four"],
            bg_one=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            context_color=self.themes["app_color"]["context_color"],
            text_foreground=self.themes["app_color"]["text_foreground"],
            text_active=self.themes["app_color"]["text_active"],
        )

        # Add left menu widget to left menu layout
        self.left_menu_layout.addWidget(self.left_menu)

    def setup_left_column(self):
        """Setup left column."""
        self.left_column_frame = QFrame(self.main_window)
        self.left_column_layout = QVBoxLayout()
        self.left_column_frame.setLayout(self.left_column_layout)
        self.left_column_frame.setMaximumWidth(general_settings.left_column_size["minimum"])
        self.left_column_frame.setMinimumWidth(general_settings.left_column_size["minimum"])
        self.left_column_frame.setStyleSheet(f"background: {self.themes['app_color']['bg_two']}")
        self.left_column_layout.setContentsMargins(0, 0, 0, 0)

        # Left column widget
        self.left_column = PyLeftColumn(
            text_title="Settings Left Frame",
            text_title_size=general_settings.font["title_size"],
            text_title_color=self.themes["app_color"]["text_foreground"],
            icon_path=self.images_load.icon_path("icon_settings.svg"),
            dark_one=self.themes["app_color"]["dark_one"],
            bg_color=self.themes["app_color"]["bg_three"],
            btn_color=self.themes["app_color"]["bg_three"],
            btn_color_hover=self.themes["app_color"]["bg_two"],
            btn_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            context_color=self.themes["app_color"]["context_color"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_close_path=self.images_load.icon_path("icon_close.svg"),
        )

        # Add left column widget to left menu layout
        self.left_column_layout.addWidget(self.left_column)

    def setup_right_column(self):
        """Setup right column."""
        self.right_column_frame = QFrame(self.main_window)
        self.right_column_layout = QVBoxLayout()
        self.right_column_frame.setLayout(self.right_column_layout)
        self.right_column_frame.setMaximumWidth(general_settings.right_column_size["minimum"])
        self.right_column_frame.setMinimumWidth(general_settings.right_column_size["minimum"])
        self.right_column_frame.setStyleSheet(f"background: {self.themes['app_color']['bg_two']}")
        self.right_column_layout.setContentsMargins(0, 0, 0, 0)

        # Left column widget
        self.right_column = PyRightColumn(
            text_title="Settings Right Frame",
            text_title_size=general_settings.font["title_size"],
            text_title_color=self.themes["app_color"]["text_foreground"],
            icon_path=self.images_load.icon_path("icon_settings.svg"),
            dark_one=self.themes["app_color"]["dark_one"],
            bg_color=self.themes["app_color"]["bg_three"],
            btn_color=self.themes["app_color"]["bg_three"],
            btn_color_hover=self.themes["app_color"]["bg_two"],
            btn_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            context_color=self.themes["app_color"]["context_color"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
        )

        # Add left column widget to left menu layout
        self.right_column_layout.addWidget(self.right_column)

    def setup_content_area(self):
        """Setup content area."""

        self.content_frame = QFrame(self.central_widget)
        self.content_layout = QVBoxLayout()

        self.content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.load_pages = Ui_MainPages()
        self.load_pages.setupUi(self.content_frame)
        self.content_layout.addWidget(self.content_frame)

    def add_page(self, page_ui):
        """Create a new widget using the provided UI code."""
        new_page = QWidget()
        new_ui = page_ui()
        new_ui.setupUi(new_page)

        # Add the new page to the existing layout
        self.load_pages.pages.addWidget(new_page)
        index = self.load_pages.pages.indexOf(new_page)
        return index

    def _load_icon(self):
        icon = QtGui.QIcon()
        icon.addFile(
            self.images_load.image_path("logo.png"),
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On,
        )
        return icon

    def update_progress_number(self, value):
        # This method will be called whenever the progress_updated signal is emitted
        print(f"Progress Number Updated: {value}")
