# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from ansys.aedt.toolkits.common.ui.utils.themes import json_themes


@pytest.fixture
def theme_dir(tmp_path):
    # Create test theme files
    (tmp_path / "ansys_dark.json").write_text(json.dumps({"dark": True}), encoding="utf-8")
    (tmp_path / "custom_theme.json").write_text(json.dumps({"color": "blue"}), encoding="utf-8")
    return tmp_path


def test_default_theme_loaded_if_missing(theme_dir):
    theme_path = theme_dir / "non_existing_theme.json"
    with patch.object(json_themes.general_settings, "theme", theme_path.name):
        handler = json_themes.ThemeHandler()
        assert handler.theme_path.name == "ansys_dark.json"
        assert len(handler.items["app_color"]) == 27


def test_custom_theme_loaded(theme_dir):
    theme_file = theme_dir / "custom_theme.json"

    with (
        patch.object(json_themes.general_settings, "theme", theme_file.name),
        patch("ansys.aedt.toolkits.common.ui.utils.themes.json_themes.Path") as mock_path_class,
    ):
        mock_path_instance = mock_path_class.return_value
        mock_path_instance.resolve.return_value = theme_file

        handler = json_themes.ThemeHandler()
        assert handler.theme_path.name == "custom_theme.json"
        assert handler.items == {"color": "blue"}


def test_available_themes_listed(theme_dir):
    with patch.object(json_themes.general_settings, "theme", "custom_theme.json"):
        handler = json_themes.ThemeHandler()
        theme_files = [f.name for f in handler.available_themes]
        assert "ansys_dark.json" in theme_files


def test_export_theme_writes_file(theme_dir):
    theme_file = theme_dir / "custom_theme.json"
    with (
        patch.object(json_themes.general_settings, "theme", theme_file.name),
        patch("ansys.aedt.toolkits.common.ui.utils.themes.json_themes.Path") as mock_path_class,
    ):
        mock_path_instance = mock_path_class.return_value
        mock_path_instance.resolve.return_value = theme_file

        handler = json_themes.ThemeHandler()

        handler.items["new_key"] = "new_value"
        handler.export_theme()

        exported = json.loads(theme_file.read_text(encoding="utf-8"))
        assert exported["color"] == "blue"
        assert exported["new_key"] == "new_value"
