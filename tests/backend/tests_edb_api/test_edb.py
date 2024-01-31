import os.path


class TestEDB:
    """EDBCommon unit tests."""

    def test_00_load_edb(self, edb_common, assert_handler, edb_example):
        """Connect AEDT."""

        assert not edb_common.load_edb(edb_example + "dummy")
        assert edb_common.load_edb(edb_example)
        assert not edb_common.load_edb(edb_example)

    def test_01_save_edb(self, edb_common, assert_handler, edb_example):
        """Connect AEDT."""
        assert edb_common.save_edb()
        directory, old_file_name = os.path.split(edb_example)
        new_path = os.path.join(directory, "new_edb.aedb")
        assert edb_common.save_edb(new_path)

    def test_02_close_edb(self, edb_common, assert_handler):
        """Open AEDT project."""
        assert edb_common.close_edb()
        assert not edb_common.close_edb()
