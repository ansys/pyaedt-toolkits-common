# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

"""Utils module"""

from enum import Enum
import os
import random
import socket
import subprocess
import sys
import threading
import time

import psutil
import requests


def download_file(url, local_filename):
    """Download a file from a URL into a local file."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=4096):
                f.write(chunk)
    return local_filename


def is_server_running(server="localhost", port=5001):
    """Check if port is used."""
    result = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((server, port))
    except socket.error as e:
        print(f"Socket error occurred: {e}")
    finally:
        sock.close()
    if result == 0:
        return True
    return False


def find_free_port(server="localhost", start_port=5001, max_attempts=50):
    """Find free port."""
    port = start_port
    for _ in range(max_attempts):
        try:
            print("Trying port {}.".format(str(port)))
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((server, port))
                print("Port {} is free.".format(str(port)))
                return port
        except OSError:
            print("Port {} is used.".format(str(port)))
        except Exception as e:
            print("An error occurred:", e)
            return False
        port = random.randint(start_port, start_port + 100)
    return False


def wait_for_server(server="localhost", port=5001, timeout=10.0):
    """Wait for server response."""
    start_time = time.time()
    first_time = True
    while time.time() - start_time < timeout:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.settimeout(2)
            sock.connect((server, port))
            sock.close()
            print("\nServer is ready.")
            return True
        except socket.error as e:
            print(f"Socket error occurred: {e}")
            if first_time:
                print("Server not ready yet. Retrying...", end="")
                first_time = False
            else:
                print(".", end="")
            time.sleep(1)
        finally:
            sock.close()
    print("\nTimed out waiting for server.")
    return False


def run_command(*command, is_linux):
    """Run command in subprocess."""
    create_no_window = 0x08000000 if not is_linux else 0
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=create_no_window,
    )
    stdout, stderr = process.communicate()
    print(stdout.decode())


def server_actions(command, name, is_linux):
    """Run command as a separate thread."""
    thread = threading.Thread(target=run_command, args=command, kwargs={"is_linux": is_linux}, name=name)
    thread.daemon = True
    thread.start()
    return thread


def clean_python_processes(url, port):
    """Clean up Python processes."""
    for conn in psutil.net_connections():
        (ip_tmp, port_tmp) = conn.laddr
        pid = conn.pid
        if ip_tmp == url and port_tmp == port and pid and pid != 0:
            try:
                process = psutil.Process(pid)
                print(f"Killing process {process.pid} on {ip_tmp}:{port_tmp}")
                process.terminate()
            except psutil.NoSuchProcess:
                print(f"Process {process.pid} on {ip}:{port_tmp} was already killed")


def check_backend_communication(url_call):
    """Check backend communication."""
    try:
        response = requests.get(url_call + "/health")
        return response.ok
    except requests.exceptions.RequestException:
        logger.error("Failed to check backend communication.")
        return False


def process_desktop_properties(is_linux, url_call):
    """Process desktop properties."""
    desktop_pid = None
    desktop_version = None
    grpc = True
    is_student = False
    if "PYAEDT_SCRIPT_VERSION" in os.environ and "PYAEDT_SCRIPT_PORT" in os.environ:
        desktop_version = os.environ["PYAEDT_SCRIPT_VERSION"]
        desktop_pid = os.environ["PYAEDT_SCRIPT_PORT"]
        grpc = desktop_version > "2023.2" or is_linux
        if "PYAEDT_STUDENT_VERSION" in os.environ:
            is_student = os.environ["PYAEDT_STUDENT_VERSION"]
        if is_student == "True":
            desktop_version += " STUDENT"

    elif len(sys.argv) == 3:
        desktop_pid, desktop_version = sys.argv[1], sys.argv[2]

    if desktop_pid and desktop_version:
        new_properties = {
            "selected_process": int(desktop_pid),
            "aedt_version": desktop_version,
            "use_grpc": grpc,
            "non_graphical": False,
        }
        try:
            response = requests.put(url_call + "/properties", json=new_properties)
            if not response.ok:
                return
            print("Connect to AEDT session.")
            requests.post(url_call + "/launch_aedt")
            requests.post(url_call + "/wait_thread")
        except requests.exceptions.RequestException:
            logger.error("Properties update failed")


class ToolkitThreadStatus(str, Enum):
    """Provides an enumeration of statuses for a toolkit thread."""

    IDLE = "Toolkit is idle and ready to accept a new task."
    BUSY = "Toolkit is busy and processing a task."
    CRASHED = "Toolkit has crashed and is not functional."
    UNKNOWN = "Toolkit status is unknown."


class PropertiesUpdate(str, Enum):
    """Provides an enumeration of statuses for updating properties."""

    EMPTY = "Body is empty."
    SUCCESS = "Properties were updated successfully."
    VALIDATION_ERROR = "Error occurred during validation of properties field."
