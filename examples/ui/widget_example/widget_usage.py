from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ansys.aedt.toolkits.common.ui.utils.widgets import *
from random import randint
import sys


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.py_window = PyWindow(self, margin=5, spacing=30)
        self.py_window.setFixedSize(400, 400)

        # Instantiate the widgets
        self.progress_bar = PyProgress(progress=0,
                                       progress_color="#FFB71B",
                                       background_color="#313131",
                                       width=10)

        self.icon_but = PyIconButton('icon_signal.svg',
                                     tooltip_text="Example", is_active=True)

        # Set window layout

        # Create a GroupBox for column 1
        column_group1 = QGroupBox()
        layout1 = QVBoxLayout()
        layout1.addWidget(self.progress_bar)
        layout1.addWidget(self.icon_but)
        column_group1.setLayout(layout1)

        # Instantiate the widgets for the right column
        self.icon = PyIcon('icon_signal.svg', "#FF0000")
        self.label = PyLabel("hola", font_size=15)
        self.divider = PyDiv(color="#FF0000", height=50, width=1)
        self.my_edit = PyLineEdit(place_holder_text="here your text")
        self.slider = PySlider()

        # Create a GroupBox for column 2
        self.py_window.layout.addWidget(self.icon)
        self.py_window.layout.addWidget(self.label)
        self.py_window.layout.addWidget(self.divider)
        self.py_window.layout.addWidget(self.my_edit)
        self.py_window.layout.addWidget(self.slider)
        self.py_window.layout.setAlignment(Qt.AlignCenter)

        self.logger = PyLogger()
        self.combo_box = PyComboBox(text_list=['Option 1', 'Option 2', 'Option 3'])
        self.credits = PyCredits(text="© 2023 MyApp Co.", version="1.2.3")
        self.left_column = PyLeftColumn(text_title="Left Column",
                                        text_title_size=8,
                                        icon_close_path='icon_close.svg')
        self.my_button = PyPushButton(text="My Button", radius=5, color="#000", bg_color="#fff", bg_color_hover="#eee",
                                      bg_color_pressed="#ddd")
        self.toggle = PyToggle(50, "#777", "#DDD", "#00BCFF", QEasingCurve.OutBounce)

        # Create a GroupBox for column 3
        column_group3 = QGroupBox()
        layout3 = QVBoxLayout()
        layout3.addWidget(self.logger)
        layout3.addWidget(self.combo_box)
        layout3.addWidget(self.credits)
        layout3.addWidget(self.left_column)
        layout3.addWidget(self.my_button)
        layout3.addWidget(self.toggle)
        column_group3.setLayout(layout3)

        # Title
        self.title = PyTitleBar(parent=self,
                                app_parent=self,
                                logo_width=50)
        title_layout = QVBoxLayout()
        title_layout.addWidget(self.title)

        self.left_menu = PyLeftMenu(parent=self,
                                    app_parent=self,
                                    icon_path='icon_signal.svg')
        self.left_menu.setMinimumWidth(150)

        # Create a GroupBox for the PyWindow widget
        window_group = QGroupBox()
        window_layout = QHBoxLayout()
        window_layout.addWidget(self.py_window)
        window_group.setLayout(window_layout)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_menu)

        main_layout.addWidget(column_group1)
        main_layout.addWidget(column_group3)

        # Right Column
        self.right_column = PyRightColumn(
            text_title="My App",
            text_title_size=15,
            text_title_color="black",
            dark_one="white",
            bg_color="gray",
            btn_color="blue",
            btn_color_hover="darkblue",
            btn_color_pressed="lightblue",
            icon_path='icon_signal.svg',
            icon_color="black",
            icon_color_hover="darkgray",
            icon_color_pressed="lightgray",
            context_color="gray",
            radius=10
        )
        main_layout.addWidget(self.right_column)
        main_layout.addWidget(window_group)

        # Add central content to title layout

        title_layout.addLayout(main_layout)

        # Set window layout
        widget = QWidget()
        widget.setLayout(title_layout)
        self.setCentralWidget(widget)

        # Create a QTimer to simulate progress
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_progress)
        self.timer.start(5000)

        self.combo_box.activated.connect(self.on_combo_box_changed)
        self.icon_but.clicked.connect(self.icon_pushed_changed)

        self.show()

    def simulate_progress(self):
        progress = randint(0, 100)
        self.progress_bar.progress = progress
        self.logger.log(f"Progress: {progress}%")

    def on_combo_box_changed(self, text):
        self.logger.log(f"ComboBox changed: {text}")

    def icon_pushed_changed(self):
        self.logger.log(f"Icon pushed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
