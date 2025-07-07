# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
from PySide6.QtCore import Qt
from ansys.aedt.toolkits.common.ui.utils.widgets.py_combo_box.py_combo_box import PyComboBox


@pytest.fixture
def sample_items():
    return ["Option 1", "Option 2", "Option 3"]


def test_pycombobox_basic(qtbot, sample_items):
    combo = PyComboBox(sample_items, radius=10, bg_color="#111111", bg_color_hover="#222222", text_color="#333333", font_size=14)
    qtbot.addWidget(combo)

    # Check if items were added
    assert combo.count() == len(sample_items)
    for i, text in enumerate(sample_items):
        assert combo.itemText(i) == text

    # Assert cursor shape
    assert combo.cursor().shape() == Qt.PointingHandCursor

    # Assert style
    style = combo.styleSheet()
    assert "border-radius: 10" in style or "border-radius: 10px" in style
    assert "#111111" in style
    assert "#222222" in style
    assert "#333333" in style
    assert "font-size: 14" in style or "font-size: 14px" in style


def test_pycombobox_selection(qtbot, sample_items):
    combo = PyComboBox(sample_items)
    qtbot.addWidget(combo)

    # Selection second item
    combo.setCurrentIndex(1)
    assert combo.currentText() == sample_items[1]

    # Select next item
    combo.setCurrentIndex(2)
    assert combo.currentText() == sample_items[2]