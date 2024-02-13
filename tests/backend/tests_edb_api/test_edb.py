import os
import pytest

from tests.backend.conftest import PROJECT_NAME

pytestmark = [pytest.mark.edb_api]

class TestEDB:
    """Class defining a workflow to test EDBCommon."""

    def test_00_load_edb(self, edb_common, common_temp_dir):
        """Load EDB file."""
        EDB_EXAMPLE_PATH = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME}.aedb")
        DUMMY_PATH = EDB_EXAMPLE_PATH + "dummy"

        assert not edb_common.load_edb(DUMMY_PATH)
        assert edb_common.load_edb(EDB_EXAMPLE_PATH)
        assert not edb_common.load_edb(EDB_EXAMPLE_PATH)

    def test_01_save_edb(self, edb_common, common_temp_dir):
        """Save EDB file."""
        NEW_EDB_PATH = os.path.join(common_temp_dir, "input_data", "new_edb.aedb")

        assert edb_common.save_edb()
        assert edb_common.save_edb(NEW_EDB_PATH)

    def test_02_close_edb(self, edb_common):
        """Close EDB."""
        assert edb_common.close_edb()
        assert not edb_common.close_edb()
