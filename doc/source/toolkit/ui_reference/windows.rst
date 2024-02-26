=======
Windows
=======

The window layout template is defined in the following directory:
`Main window layout <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/ui/main_window>`_.

The following directory contains the setup of the **main_window**, **home_menu** and **settings_column**.
`Common window setup <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/ui/common_windows>`_

The following script shows how you can use the previous files to initialize the application.

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

            # Create user interface object
            self.ui = MainWindowLayout(self)
            self.ui.setup()

            # Setup main
            self.main_window = MainWindow(self)
            self.main_window.setup()

            # Settings menu
            self.settings_menu = SettingsMenu(self)
            self.settings_menu.setup()

            self.home_menu = HomeMenu(self)
            self.home_menu.setup()


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = ApplicationWindow()
        window.show()
        sys.exit(app.exec())
