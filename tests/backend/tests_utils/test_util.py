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

import pytest

# pytestmark = [pytest.mark.utils]

import threading
from unittest.mock import patch, MagicMock

from ansys.aedt.toolkits.common.utils import run_command, server_actions, wait_for_server, find_free_port


@pytest.fixture
def mock_subprocess():
    """Mock subprocess.Popen to avoid actual process execution."""
    with patch('subprocess.Popen') as mock_popen:
        mock_popen.return_value.communicate.return_value = (b'Test output', b'')
        yield mock_popen


@pytest.fixture
def mock_socket():
    """Mock socket.socket to avoid actual network connection."""
    with patch('socket.socket') as mock_socket:
        mock_socket.return_value.connect_ex.return_value = 0
        yield mock_socket


def test_run_command(mock_subprocess):
    """Test run_command function."""
    run_command('ls', is_linux=True)
    mock_subprocess.assert_called_once()


def test_server_actions(mock_subprocess):
    """Test server_actions function."""
    command = ('ls',)
    name = 'TestThread'
    is_linux = True

    thread = server_actions(command, name, is_linux)
    assert isinstance(thread, threading.Thread)
    assert thread.name == name
    assert thread.is_alive()

    thread.join()

    mock_subprocess.assert_called_once()


def test_wait_for_server(mock_socket):
    """Test wait_for_server function."""
    assert wait_for_server('localhost', 5001, timeout=1.0)


def test_find_free_port():
    """Test find_free_port function."""
    assert isinstance(find_free_port(server='localhost', start_port=5001), int)

    assert isinstance(find_free_port(), int)
