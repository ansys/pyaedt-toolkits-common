# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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
import sys

import streamlit as st

# isort: off
# Default user interface properties
# isort: on

# Toolkit frontend API

if len(sys.argv) > 1:
    backend_url = sys.argv[1]
else:
    backend_url = "http://127.0.0.1:5000"

st.title("Simple AEDT Toolkit - Create geometry")


def _get_frontend():
    if "frontend" not in st.session_state:
        from examples.toolkit_webapp.pyaedt_toolkit.ui.actions import Frontend

        st.session_state.frontend = Frontend()
    return st.session_state.frontend

frontend = _get_frontend()

if st.button("Create geometry"):
    with st.spinner("Creating geometry in AEDT..."):
        success = frontend.create_geometry_toolkit()

    if success:
        st.success("Geometry created successfully!")
    else:
        st.error("Failed to create geometry.")

if st.button("Close Desktop"):
    with st.spinner("Closing AEDT Desktop..."):
        success = frontend.close_desktop()

    if success:
        st.success("Desktop closed successfully!")
    else:
        st.error("Failed to close desktop.")