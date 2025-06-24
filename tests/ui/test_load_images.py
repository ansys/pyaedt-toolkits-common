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

import os
import pytest
from pathlib import Path
from unittest.mock import patch
from ansys.aedt.toolkits.common.ui.utils.images import load_images


@pytest.fixture
def valid_temp_dir(tmp_path):
    (tmp_path / "icons").mkdir()
    (tmp_path / "files").mkdir()
    (tmp_path / "icons" / "icon.png").touch()
    (tmp_path / "files" / "image.png").touch()
    return tmp_path


def test_init_with_valid_path(valid_temp_dir):
    loader = load_images.LoadImages(str(valid_temp_dir))
    assert loader.images_path == str(valid_temp_dir)


def test_icon_path_valid(valid_temp_dir):
    loader = load_images.LoadImages(str(valid_temp_dir))
    assert loader.icon_path("icon.png") == os.path.join(str(valid_temp_dir), "icons", "icon.png")


def test_image_path_valid(valid_temp_dir):
    loader = load_images.LoadImages(str(valid_temp_dir))
    assert loader.image_path("image.png") == os.path.join(str(valid_temp_dir), "files", "image.png")


def test_icon_path_invalid(valid_temp_dir):
    loader = load_images.LoadImages(str(valid_temp_dir))
    assert loader.icon_path("missing_icon.png") is False


def test_image_path_invalid(valid_temp_dir):
    loader = load_images.LoadImages(str(valid_temp_dir))
    assert loader.image_path("missing_image.png") is False


def test_init_with_general_settings_images(valid_temp_dir):
    with patch.object(load_images.general_settings, "images", str(valid_temp_dir)):
        loader = load_images.LoadImages()
        assert loader.images_path == str(valid_temp_dir)


def test_init_with_invalid_path_raises():
    with patch.object(load_images.general_settings, "images", "/this/path/does/not/exist"):
        with pytest.raises(FileNotFoundError):
            load_images.LoadImages()


def test_init_no_path_and_no_general_settings():
    with patch.object(load_images, "general_settings") as mock_settings:
        if hasattr(mock_settings, "images"):
            del mock_settings.images
        loader = load_images.LoadImages()
        assert loader.images_path == Path(__file__).resolve().parent