""""""

from unittest.mock import patch

import pytest

MOCK_PROPERTIES = {"version": "0.1", "active_project": "Dummy project", "project_list": ["Dummy project"], "design_list": {"Dummy project": "Dummy design"}}

@pytest.fixture
def patched_window_methods():
    with patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.ApplicationWindow.check_connection", return_value=True), \
         patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.ApplicationWindow.get_properties", return_value=MOCK_PROPERTIES), \
         patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.ApplicationWindow.installed_versions", return_value=["25.1"]), \
         patch("examples.toolkit.pyaedt_toolkit.ui.run_frontend.SettingsMenu.process_id", return_value=12345), \
         patch("ansys.aedt.toolkits.common.ui.actions_generic.FrontendGeneric.set_properties", return_value=None):
        yield
