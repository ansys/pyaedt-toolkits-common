from random import randint
import sys

# from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import PyWindow

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QComboBox

from pyvistaqt import BackgroundPlotter
import pyvista as pv

from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import PyLogger


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)

        self.plotter = BackgroundPlotter(show=False)

        self.grid_layout.addWidget(self.plotter, 0, 0)

        self.v_layout = QVBoxLayout()

        # Horizontal Layout for ComboBox
        label = QLabel("Select Option:")
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        self.v_layout.addWidget(label)
        self.v_layout.addWidget(self.combo_box)

        # Add Vertical Layout to Grid Layout
        self.grid_layout.addLayout(self.v_layout, 1, 0)

        self.logger = PyLogger()
        self.v_layout.addWidget(self.logger)

        # Connect the combo box signal to a slot
        self.combo_box.currentIndexChanged.connect(lambda index: self.update_information(index))

        # Initial plot
        self.update_information(0)

    def update_information(self, index):
        # Handle the selection change and update the text edit
        selected_option = f"Selected Option: {index + 1}"
        self.logger.log(selected_option)

        # Clear existing mesh
        self.plotter.clear()

        # Add new mesh based on combo box option
        if index == 0:
            cad_mesh = pv.Sphere(radius=1)
            camera_position = [(3, 3, 3), (0, 0, 0), (0, 0, 1)]
        elif index == 1:
            cad_mesh = pv.Cylinder(radius=1, height=3)
            camera_position = [(0, 0, 5), (0, 0, 0), (0, 1, 0)]
        else:
            cad_mesh = pv.Box()
            camera_position = [(-2, -2, -2), (0, 0, 0), (0, 0, 1)]

        self.plotter.add_mesh(cad_mesh)

        # Set camera position and focal point
        self.plotter.camera_position = camera_position
        self.plotter.reset_camera_clipping_range()

        # Show the updated visualization
        self.plotter.show()

        self.plotter.add_axes_at_origin(labels_off=True, line_width=5)
        self.plotter.show_grid()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
