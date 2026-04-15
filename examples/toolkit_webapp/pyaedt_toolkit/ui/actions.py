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

from ansys.aedt.core.generic.file_utils import generate_unique_project_name
import requests

from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger


class Frontend(FrontendGeneric):
    def __init__(self, base_url: str = "http://127.0.0.1:5001"):
        super().__init__()
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def create_geometry_toolkit(self, project_selected=None, design_selected=None):
        # Set active project and design
        be_properties = self.get_properties()
        if project_selected and design_selected:
            if project_selected == "No Project":
                project_selected = generate_unique_project_name()
                be_properties["active_project"] = project_selected

            for project in be_properties["project_list"]:
                if self.get_project_name(project) == project_selected:
                    be_properties["active_project"] = project
                    if project_selected in list(be_properties["design_list"].keys()):
                        designs = be_properties["design_list"][project_selected]
                        for design in designs:
                            if design_selected == design:
                                be_properties["active_design"] = design
                                break
                    break
        else:
            project_selected = generate_unique_project_name()
            project_selected = self.get_project_name(project_selected)
            be_properties["active_project"] = project_selected

        self.set_properties(be_properties)

        print("Calling:", self._url("/create_geometry"))
        response = requests.post(self._url("/create_geometry"))

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.ok:
            msg = "Geometry created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self._url}"
            logger.error(msg)
            return False

    def close_desktop(self):
        print("Calling:", self._url("/close_aedt"))
        properties = {"close_projects": True, "close_desktop": True}
        response = requests.post(self._url("/close_aedt"), json=properties)

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.ok:
            msg = "Desktop closed."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self._url}"
            logger.error(msg)
            return False
