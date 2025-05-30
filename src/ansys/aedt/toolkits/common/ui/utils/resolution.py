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


def set_pyside_resolution(properties, use_tkinter=True):
    import os

    if not use_tkinter:
        properties.high_resolution = (
            os.getenv("AEDT_TOOLKIT_HIGH_RESOLUTION", "false").lower() in ("true", "1", "t")
            or properties.high_resolution
        )
        if properties.high_resolution:
            os.environ["QT_SCALE_FACTOR"] = "2"
        return True
    else:
        try:
            import tkinter

            app = tkinter.Tk()
            width = app.winfo_screenwidth()
            height = app.winfo_screenheight()
            app.destroy()
            if width > 1920 or height > 1080:
                properties.high_resolution = True
                os.environ["QT_SCALE_FACTOR"] = "2"
            else:
                properties.high_resolution = False
                os.environ["QT_SCALE_FACTOR"] = "1"
            return True
        except Exception:
            print("Tkinter failed")
            # If tkinter fails, fallback to first
            properties.high_resolution = (
                os.getenv("AEDT_TOOLKIT_HIGH_RESOLUTION", "false").lower() in ("true", "1", "t")
                or properties.high_resolution
            )
            if properties.high_resolution:
                os.environ["QT_SCALE_FACTOR"] = "2"
            return True
