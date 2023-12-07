from PySide6.QtSvgWidgets import *
from PySide6.QtCore import *
from ansys.aedt.toolkits.common.ui.properties import general_settings


class SetupMainWindow(object):
    def __init__(self, app):
        self._app = app
        # App title
        self._app.setWindowTitle(general_settings.app_name)

    def setup_gui(self):

        # Add title
        if not hasattr(general_settings, "main_title"):
            title = "Welcome to the Toolkit"
        else:
            title = general_settings.main_title
        self._app.ui.title_bar.set_title(title)

        # Add menus
        self._app.ui.left_menu.add_menus(general_settings.add_left_menus)
        self._app.ui.title_bar.add_menus(general_settings.add_title_bar_menus)

        # Set left menu signal
        self._app.ui.left_menu.clicked.connect(self.main_clicked)

        # Set left column signal
        self._app.ui.left_column.clicked.connect(self.main_clicked)

        # Set title bar menu signal
        self._app.ui.title_bar.clicked.connect(self.main_clicked)

        # Set right column signal
        self._app.ui.right_column.clicked.connect(self.main_clicked)

        # Load main page
        self._app.ui.set_page(self._app.ui.load_pages.home_page)

        # Add logo to main page
        main_logo = QSvgWidget(self._app.ui.images_load.image_path("ANSS_BIG.D.svg"))
        self._app.ui.load_pages.logo_layout.addWidget(main_logo, Qt.AlignCenter, Qt.AlignCenter)

    def get_selected_menu(self):
        if self._app.ui.title_bar.sender() is not None:
            return self._app.ui.title_bar.sender()
        elif self._app.ui.left_menu.sender() is not None:
            return self._app.ui.left_menu.sender()
        elif self._app.ui.left_column.sender() is not None:
            return self._app.ui.left_column.sender()
        elif self._app.ui.right_column.sender() is not None:
            return self._app.ui.right_column.sender()

    def main_clicked(self):
        selected_menu = self.get_selected_menu()

        is_left_visible = self._app.ui.is_left_column_visible()
        is_right_visible = self._app.ui.is_right_column_visible()

        self._app.ui.left_menu.select_only_one(selected_menu.objectName())

        if selected_menu.objectName() == 'home_menu' and not is_left_visible:
            self._app.ui.set_page(self._app.ui.load_pages.home_page)
            self._app.ui.toggle_left_column()
            self._app.ui.set_left_column_menu(
                menu=self._app.ui.left_column.menus.menu_home,
                title="Home",
                icon_path=self._app.ui.images_load.icon_path("icon_home.svg"))

        elif selected_menu.objectName() == 'top_settings' and not is_right_visible:
            if is_left_visible:
                self._app.ui.toggle_left_column()
            self._app.ui.toggle_right_column()
            self._app.ui.set_right_column_menu(title="Settings")

        elif selected_menu.objectName() == 'progress_menu':
            if is_left_visible:
                self._app.ui.toggle_left_column()
            self._app.ui.toggle_progress()

        elif is_left_visible or selected_menu.objectName() == "close_left_column" or is_right_visible:
            if self._app.ui.is_left_column_visible():
                selected_menu.set_active(False)
                self._app.ui.toggle_left_column()
            elif self._app.ui.is_right_column_visible:
                self._app.ui.toggle_right_column()
