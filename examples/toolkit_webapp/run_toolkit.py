# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import atexit
import multiprocessing
import os
import socket
import subprocess
import sys
import time

from ansys.aedt.toolkits.common.utils import clean_python_processes
from ansys.aedt.toolkits.common.utils import find_free_port
from ansys.aedt.toolkits.common.utils import is_server_running

from examples.toolkit_webapp.pyaedt_toolkit.backend.models import properties as backend_properties

backend = None
ui = None


def start_backend(pp):
    """Start the backend process."""
    from examples.toolkit_webapp.pyaedt_toolkit.backend.run_backend import run_backend

    print(f"Starting backend on port {pp}...")
    run_backend(pp)


def start_frontend(url, port):
    """Start the frontend process."""
    frontend_port = _find_free_port_streamlit()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_url = f"http://{url}:{port}"

    frontend_path = os.path.join(
        base_dir,
        "pyaedt_toolkit/ui",
        "run_frontend.py")
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        frontend_path,
        "--server.port",
        str(frontend_port),
        "--",
        backend_url
    ])

def _find_free_port_streamlit():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


if __name__ == "__main__":
    multiprocessing.freeze_support()

    is_linux = os.name == "posix"
    new_port = find_free_port(backend_properties.url, backend_properties.port)
    if not new_port:
        raise Exception(f"No free ports available in {backend_properties.url}")

    backend_properties.port = new_port
    url = backend_properties.url
    url_call = f"http://{url}:{new_port}"


    def terminate_processes():
        print("Terminating backend and frontend processes...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.join()
        frontend_process.join()
        print("Processes terminated.")


    # Clean python processes when script ends
    atexit.register(clean_python_processes, url, new_port)

    # Check if backend is already running
    if is_server_running(server=url, port=new_port):
        raise Exception(f"A process is already running at: {url_call}")

    # Launch backend process
    backend_process = multiprocessing.Process(target=start_backend, args=(new_port,))
    backend_process.start()
    time.sleep(2)

    # Launch frontend process
    frontend_process = multiprocessing.Process(target=start_frontend, args=(url, new_port))
    frontend_process.start()

    try:
        backend_process.join()
        frontend_process.join()
    except KeyboardInterrupt:
        terminate_processes()
