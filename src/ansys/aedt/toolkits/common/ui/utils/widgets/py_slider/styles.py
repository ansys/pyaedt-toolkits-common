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


class Styles(object):
    style = """
    /* HORIZONTAL */
    QSlider {{ margin: {_margin}px; }}
    QSlider::groove:horizontal {{
        border-radius: {_bg_radius}px;
        height: {_bg_size}px;
        margin: 0px;
        background-color: {_bg_color};
    }}
    QSlider::groove:horizontal:hover {{ background-color: {_bg_color_hover}; }}
    QSlider::handle:horizontal {{
        border: none;
        height: {_handle_size}px;
        width: {_handle_size}px;
        margin: {_handle_margin}px;
        border-radius: {_handle_radius}px;
        background-color: {_handle_color};
    }}
    QSlider::handle:horizontal:hover {{ background-color: {_handle_color_hover}; }}
    QSlider::handle:horizontal:pressed {{ background-color: {_handle_color_pressed}; }}

    /* VERTICAL */
    QSlider::groove:vertical {{
        border-radius: {_bg_radius}px;
        width: {_bg_size}px;
        margin: 0px;
        background-color: {_bg_color};
    }}
    QSlider::groove:vertical:hover {{ background-color: {_bg_color_hover}; }}
    QSlider::handle:vertical {{
        border: none;
        height: {_handle_size}px;
        width: {_handle_size}px;
        margin: {_handle_margin}px;
        border-radius: {_handle_radius}px;
        background-color: {_handle_color};
    }}
    QSlider::handle:vertical:hover {{ background-color: {_handle_color_hover}; }}
    QSlider::handle:vertical:pressed {{ background-color: {_handle_color_pressed}; }}
    """
