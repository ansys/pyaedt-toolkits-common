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

"""
Common conftest
"""
import os
from pathlib import Path
import shutil
from typing import List

import pytest

UI_TESTS_PREFIX = "tests/ui"


@pytest.fixture(scope="session")
def common_temp_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("test_common_toolkit_workflows", numbered=True)
    src_folder = os.path.join(Path(__file__).parent, "input_data")
    shutil.copytree(src_folder, os.path.join(tmp_dir, "input_data"))

    yield tmp_dir


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]):
    """Hook used to apply marker on tests."""
    for item in items:
        # Mark unit, integration and system tests
        if item.nodeid.startswith(UI_TESTS_PREFIX):
            item.add_marker(pytest.mark.ui)
