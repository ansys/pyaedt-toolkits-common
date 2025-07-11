import atexit
import multiprocessing
import os
import sys
import time

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from ansys.aedt.toolkits.common.utils import check_backend_communication
from ansys.aedt.toolkits.common.utils import clean_python_processes
from ansys.aedt.toolkits.common.utils import find_free_port
from ansys.aedt.toolkits.common.utils import is_server_running
from ansys.aedt.toolkits.common.utils import process_desktop_properties

from examples.toolkit.pyaedt_toolkit.backend.models import properties as backend_properties
from examples.toolkit.pyaedt_toolkit.ui.models import properties as frontend_properties

backend = None
ui = None


def start_backend(pp):
    """Start the backend process."""
    from examples.toolkit.pyaedt_toolkit.backend.run_backend import run_backend

    print(f"Starting backend on port {pp}...")
    run_backend(pp)


def show_splash_and_start_frontend(app, url, port):
    from examples.toolkit.pyaedt_toolkit.ui.run_frontend import run_frontend
    from examples.toolkit.pyaedt_toolkit.ui.splash import show_splash_screen

    splash = show_splash_screen(app)  # Should return the splash widget
    url_call = f"http://{url}:{port}"

    def check_backend():
        if check_backend_communication(url_call):
            splash.close()
            run_frontend(url, port, app)
        else:
            QTimer.singleShot(500, check_backend)  # Check again in 0.5s
   
    check_backend()


if __name__ == "__main__":
    multiprocessing.freeze_support()

    is_linux = os.name == "posix"
    new_port = find_free_port(backend_properties.url, backend_properties.port)
    if not new_port:
        raise Exception(f"No free ports available in {backend_properties.url}")

    backend_properties.port = new_port
    frontend_properties.backend_port = new_port
    url = frontend_properties.backend_url
    port = frontend_properties.backend_port
    url_call = f"http://{url}:{port}"
    python_path = sys.executable
    splash_thread = None


    def terminate_processes():
        print("Terminating backend and frontend processes...")
        backend_process.terminate()
        backend_process.join()
        print("Processes terminated.")


    # Clean python processes when script ends
    atexit.register(clean_python_processes, url, port)

    # Check if backend is already running
    if is_server_running(server=url, port=port):
        raise Exception(f"A process is already running at: {url_call}")

    # Launch backend process
    backend_process = multiprocessing.Process(target=start_backend, args=(new_port,))
    backend_process.start()

    # Connect to AEDT session if necessary
    process_desktop_properties(is_linux, url_call)

    app = QApplication(sys.argv)
    show_splash_and_start_frontend(app, url, port)
    app.aboutToQuit.connect(terminate_processes)
    sys.exit(app.exec())
