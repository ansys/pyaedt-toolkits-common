=======
Windows
=======

The Windows layout template is in the
`main_window <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/ui/main_window>`_
directory in the repository.

The `Common_windows <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/ui/common_windows>`_
directory contains the files for setting up the **main window**, **home menu**, and **settings column**.

The following script shows how to use the previous files to initialize the application.

.. code:: python

    # Import API
    import os
    import sys
    from PySide6.QtWidgets import QApplication

    from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
    from ansys.aedt.toolkits.common.ui.common_windows.main_window import MainWindow
    from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu
    from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import (
        MainWindowLayout,
    )
    from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric


    # Object with generic methods to control the toolkits
    class ApplicationWindow(FrontendGeneric):
        def __init__(self):

            FrontendGeneric.__init__(self)

            # Create UI object
            self.ui = MainWindowLayout(self)
            self.ui.setup()

            # Set up main window
            self.main_window = MainWindow(self)
            self.main_window.setup()

            # Set up settings menu
            self.settings_menu = SettingsMenu(self)
            self.settings_menu.setup()

            self.home_menu = HomeMenu(self)
            self.home_menu.setup()


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = ApplicationWindow()
        window.show()
        sys.exit(app.exec())
