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

import os
import pytest

@pytest.mark.tests_edb_api
class TestEDB:
    """EDBCommon unit tests."""

    def test_00_load_edb(self, edb_common, common_temp_dir):
        """Load EDB."""
        edb_example = os.path.join(common_temp_dir, "input_data", "edb_test.aedb")
        assert not edb_common.load_edb(edb_example + "dummy")
        assert edb_common.load_edb(edb_example)
        assert not edb_common.load_edb(edb_example)

    def test_01_save_edb(self, edb_common, common_temp_dir):
        """Save EDB."""
        assert edb_common.save_edb()
        new_path = os.path.join(common_temp_dir, "input_data", "new_edb.aedb")
        assert edb_common.save_edb(new_path)

    def test_02_close_edb(self, edb_common):
        """Close EDB."""
        assert edb_common.close_edb()
        assert not edb_common.close_edb()
