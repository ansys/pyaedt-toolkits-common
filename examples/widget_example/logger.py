from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from ansys.aedt.toolkits.common.ui.utils.widgets.py_progress_bar.py_progress import PyProgress
from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from random import randint
from PySide6.QtCore import QTimer
import sys


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instantiate the widgets
        self.progress_bar = PyProgress(progress=0,
                                       progress_color="#FFB71B",
                                       background_color="#313131",
                                       width=10)
        self.logger = PyLogger()

        # Create a QTimer to simulate progress
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_progress)
        self.timer.start(1000)

        # Split the window into two areas
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.logger)
        splitter.addWidget(self.progress_bar)
        self.setCentralWidget(splitter)

        self.show()

    def simulate_progress(self):
        progress = randint(0, 100)
        self.progress_bar.progress = progress
        self.logger.log(f"Progress: {progress}%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
