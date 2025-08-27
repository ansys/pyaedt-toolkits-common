# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

import os
import time
from typing import Optional

from PySide6 import QtWidgets
import requests

from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.models import general_settings
from ansys.aedt.toolkits.common.utils import ToolkitThreadStatus

MSG_TK_RUNNING = "Please wait, toolkit running"
DEFAULT_REQUESTS_TIMEOUT = 10
"""Default timeout for requests in seconds."""
DEFAULT_AEDT_SESSION_VALUE = "New Session"
"""Default value for AEDT session selection in the UI."""


class FrontendGeneric:
    """This class provides a generic frontend for controlling the toolkit."""

    def __init__(self):
        logger.info("Frontend initialization...")

        self.ui = None
        url = general_settings.backend_url
        port = general_settings.backend_port
        self.url = f"http://{url}:{port}"
        self.logger = logger

        # Load toolkit icon
        self.images_path = os.path.join(os.path.dirname(__file__), "images")

    @staticmethod
    def poll_url(url: str, timeout: int = 10, interval: float = 0.5):
        """Poll a URL repeatedly until a successful response or a timeout is reached.

        This function sends repeated GET requests to the given URL at a fixed interval,
        stopping when a success response is received or when the specified timeout is
        exceeded.

        Parameters
        ----------
        url : str
            The URL to poll.
        timeout : int, optional
            Maximum total time (in seconds) to continue polling before giving up.
            Default is 10.
        interval : float, optional
            Time (in seconds) to wait between each request attempt.
            Default is 0.5.

        Returns
        -------
        tuple[bool, str | dict]
            A 2-tuple containing a boolean and a dict or string.
            The first element is a boolean stating if the GET requests succeeded.
            The second element is either the response content (parsed as JSON if successful)
            or a string describing the failure reason.
        """
        logger.debug(f"Polling url '{url}' for up to {timeout} seconds")

        end_time = time.time() + timeout
        response_success = False

        while time.time() < end_time and not response_success:
            try:
                response = requests.get(url, timeout=2.0)
                response_success = response.ok
                if response_success:
                    return True, response.json()
            except requests.exceptions.Timeout as e:
                logger.debug(f"Timeout while polling {url}: {e}")
            except requests.exceptions.RequestException as e:
                logger.debug(f"Request failed while polling {url}: {e}")

            time.sleep(interval)

        return False, f"Polling failed after {timeout} seconds."

    def check_connection(self):
        """Check the backend connection.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        url = self.url + "/health"
        response_success, response_content = self.poll_url(url)
        if response_success:
            logger.debug(response_content)
        else:
            logger.error(response_content)
        return response_success

    def backend_busy(self):
        """
        Check if the backend is currently busy.

        Returns
        -------
        bool
            ``True`` if the backend is busy, ``False`` otherwise.
        """
        try:
            response = requests.get(self.url + "/status", timeout=DEFAULT_REQUESTS_TIMEOUT)
            res = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
            return res
        except requests.exceptions.RequestException:
            logger.error("Get backend status failed")
            return False

    def wait_thread(self, timeout: int = DEFAULT_REQUESTS_TIMEOUT):
        """
        Wait thread until backend is idle.

        Parameters
        ----------
        timeout : int, optional
            Time out in seconds. The default is 10 seconds.

        Returns
        -------
        bool
            ``True`` when the backend is idle, ``False`` otherwise.
        """
        try:
            response = requests.get(self.url + "/wait_thread", timeout=timeout)
            return response.ok
        except requests.exceptions.RequestException:
            logger.error("Wait thread failed.")
            return False

    def installed_versions(self):
        """
        Get the installed versions of AEDT.

        Returns
        -------
        list or False
            A list of installed AEDT versions if successful, ``False`` otherwise.
        """
        try:
            response = requests.get(self.url + "/installed_versions", timeout=DEFAULT_REQUESTS_TIMEOUT)
            if response.ok:
                versions = response.json()
                return versions
        except requests.exceptions.RequestException:
            msg = "Get AEDT installed versions failed"
            self.log_and_update_progress(msg, log_level="error")
            return False

    def get_properties(self):
        """
        Get properties from the backend.

        Returns
        -------
        dict or False
            A dictionary of properties if successful, ``False`` otherwise.
        """
        try:
            response = requests.get(self.url + "/properties", timeout=DEFAULT_REQUESTS_TIMEOUT)
            if response.ok:
                data = response.json()
                if data:
                    logger.debug("Properties from backend updated successfully")
                    return data
                else:
                    logger.debug("Backend properties empty")
                    return False
        except requests.exceptions.RequestException:
            self.ui.update_logger("Get properties failed")

    def set_properties(self, data):
        """
        Set properties in the backend.

        Parameters
        ----------
        data : dict
            Dictionary of properties to set.
        """
        try:
            response = requests.put(self.url + "/properties", json=data, timeout=DEFAULT_REQUESTS_TIMEOUT)
            if response.ok:
                return response.json()
            else:
                return False
        except requests.exceptions.RequestException:
            msg = "Set properties failed"
            self.log_and_update_progress(msg, log_level="error")

    def find_process_ids(self, version, non_graphical):
        """
        Find AEDT sessions based on the selected version and graphical mode.

        Parameters
        ----------
        version : str
            AEDT version.
        non_graphical : bool
            Flag indicating graphical or non-graphical mode.

        Returns
        -------
        list or False
            A list of found AEDT sessions if successful, ``False`` otherwise.
        """
        try:
            be_properties = self.get_properties()
            be_properties["aedt_version"] = version
            be_properties["non_graphical"] = non_graphical
            self.set_properties(be_properties)
            response = requests.get(self.url + "/aedt_sessions", timeout=DEFAULT_REQUESTS_TIMEOUT)
            sessions = []
            if response.ok:
                sessions = response.json()
            return sessions
        except requests.exceptions.RequestException:
            logger.error(f"Find AEDT sessions failed")
            return False

    def launch_aedt(self, selected_version, selected_process, non_graphical=False):
        """Launch AEDT.

        Parameters
        ----------
        selected_version : str
            The selected AEDT version.
        selected_process : str
            The selected AEDT process.
        non_graphical : bool, optional
            Flag indicating whether to run AEDT in non-graphical mode. The default is False.
        """
        response = requests.get(self.url + "/status", timeout=DEFAULT_REQUESTS_TIMEOUT)
        res_busy = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
        res_idle = response.ok and response.json() == ToolkitThreadStatus.IDLE.value
        if res_busy:
            msg = MSG_TK_RUNNING
            self.log_and_update_progress(msg, log_level="debug")
        elif res_idle:
            self.ui.update_progress(0)
            response = requests.get(self.url + "/health", timeout=DEFAULT_REQUESTS_TIMEOUT)
            if response.ok and response.json() == "Toolkit is not connected to AEDT.":
                be_properties = self.get_properties()
                if be_properties["selected_process"] == 0 or not self.properties.block_settings_after_load:
                    be_properties["aedt_version"] = selected_version
                    be_properties["non_graphical"] = non_graphical
                    if selected_process != DEFAULT_AEDT_SESSION_VALUE:
                        be_properties["non_graphical"] = False
                        text_splitted = selected_process.split(" ")
                        if len(text_splitted) == 4:
                            be_properties["use_grpc"] = True
                            be_properties["selected_process"] = int(text_splitted[3])
                        else:
                            be_properties["use_grpc"] = False
                            be_properties["selected_process"] = int(text_splitted[1])
                    self.set_properties(be_properties)
                response = requests.post(self.url + "/launch_aedt", timeout=DEFAULT_REQUESTS_TIMEOUT)

                if response.status_code == 200:
                    msg = "Launching AEDT"
                    self.log_and_update_progress(msg, log_level="debug", progress=50)
                else:
                    msg = f"Failed backend call: {self.url}"
                    self.log_and_update_progress(msg, log_level="error", progress=100)
            else:
                msg = response.json()
                self.log_and_update_progress(msg, log_level="debug", progress=100)
        else:
            msg = response.json()
            self.log_and_update_progress(msg, log_level="debug", progress=100)

    def open_project(self, selected_project):
        """Open an AEDT project.

        Parameters
        ----------
        selected_project : str
            The path to the selected AEDT project.
        """
        response = requests.get(self.url + "/status", timeout=DEFAULT_REQUESTS_TIMEOUT)
        res_busy = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
        res_idle = response.ok and response.json() == ToolkitThreadStatus.IDLE.value
        if res_busy:
            msg = MSG_TK_RUNNING
            self.log_and_update_progress(msg, log_level="debug")
        elif res_idle:
            self.ui.update_progress(0)
            response = requests.get(self.url + "/health", timeout=DEFAULT_REQUESTS_TIMEOUT)
            if response.ok and response.json() == "Toolkit is not connected to AEDT.":
                response = requests.post(self.url + "/open_project", data=selected_project, timeout=20)
                if response.status_code == 200:
                    msg = "Project opened"
                    self.log_and_update_progress(msg, log_level="debug")
                else:
                    msg = f"Failed backend call: {self.url} + '/'open_project"
                    self.log_and_update_progress(msg, log_level="error", progress=100)
            else:
                msg = response.json()
                self.log_and_update_progress(msg, log_level="debug", progress=100)
        else:
            msg = response.json()
            self.log_and_update_progress(msg, log_level="debug", progress=100)

    def get_aedt_model(
        self,
        project_selected,
        design_selected,
        air_objects=True,
        encode=True,
        obj_list=None,
        export_path=None,
        export_as_single_objects=True,
    ):
        """Get AEDT model.

        Parameters
        ----------
        project_selected : str
            Project name.
        design_selected : str
            Design name.
        air_objects : bool, optional
            Define if air and vacuum objects will be exported.
        encode : bool, optional
            Whether to encode the file. The default is ``True``.
        obj_list : list, optional
            List of objects to export. The default is ``None``, in which case
            every model object except 3D, vacuum, and air objects are exported.
        export_path : str, optional
            Full path of the exported OBJ file.
            The default is ``None``, in which case the file is exported in the working directory.
        export_as_single_objects : bool, optional
            Whether to export the model as a single object. The default is ``True``.
            If ``False``, the model is exported as a list of objects for each object.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        # Set active project and design
        be_properties = self.get_properties()

        if project_selected == "No Project" or design_selected == "No Design":
            logger.error("Wrong project or design")
            return False
        else:
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

        self.set_properties(be_properties)

        response = requests.get(
            self.url + "/get_aedt_model",
            json={
                "air_objects": air_objects,
                "encode": encode,
                "obj_list": obj_list,
                "export_path": export_path,
                "export_as_single_objects": export_as_single_objects,
            },
            timeout=20,
        )

        if response.ok:
            msg = "Geometry created."
            logger.info(msg)
            return response.json()
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def get_aedt_data(self):
        """Get a list of AEDT projects.

        Returns
        -------
        list
            A list of AEDT project names. Returns ["No Project"] if no projects are available.
        """
        be_properties = self.get_properties()
        project_list = []
        if be_properties["active_project"]:
            if be_properties["project_list"]:
                for project in be_properties["project_list"]:
                    active_project_name = os.path.splitext(os.path.basename(project))[0]
                    project_list.append(active_project_name)
        else:
            project_list.append("No Project")
        return project_list

    @staticmethod
    def get_project_name(project_path):
        """Get project name from project path.

        Returns
        -------
        str
            Project name
        """
        return os.path.splitext(os.path.basename(project_path))[0]

    def update_design_names(self, active_project=None):
        """Update design names based on the active project.

        Parameters
        ----------
        active_project : str, optional
            The active AEDT project. If not provided, the current active project will be used.

        Returns
        -------
        list
            A list of design names.
        """
        be_properties = self.get_properties()
        if not active_project:
            if be_properties["active_project"] == "No Project":
                return ["No Design"]
            active_project = os.path.splitext(os.path.basename(be_properties["active_project"]))[0]
            if not active_project:
                active_project = "No Project"
                be_properties["active_project"] = active_project
        else:
            be_properties["active_project"] = active_project

        design_list = be_properties["design_list"].get(active_project)
        if not design_list:
            design_list = ["No Design"]
            be_properties["active_design"] = "No Design"
        else:
            be_properties["active_design"] = design_list[0]
        self.set_properties(be_properties)
        return design_list

    def save_project(self):
        """Save the current AEDT project.

        Opens a file dialog to select a location to save the AEDT project. The project is saved
        with a '.aedt' extension.

        Note:
            This method relies on backend communication to save the project.

        Returns
        -------
        None
        """
        dialog = QtWidgets.QFileDialog()
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        dialog.setOption(QtWidgets.QFileDialog.Option.DontConfirmOverwrite, True)
        file_name, _ = dialog.getSaveFileName(
            self,
            "Save new aedt file",
            "",
            "Aedt Files (*.aedt)",
        )

        if file_name:
            response = requests.get(self.url + "/status", timeout=DEFAULT_REQUESTS_TIMEOUT)
            res_busy = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
            res_idle = response.ok and response.json() == ToolkitThreadStatus.IDLE.value
            if res_busy:
                msg = MSG_TK_RUNNING
                self.log_and_update_progress(msg, log_level="debug")
            elif res_idle:
                response = requests.post(self.url + "/save_project", json=file_name, timeout=DEFAULT_REQUESTS_TIMEOUT)
                if response.ok:
                    msg = "Saving project: {}".format(file_name)
                    self.log_and_update_progress(msg, log_level="debug")
                else:
                    msg = f"Failed backend call: {self.url}"
                    self.log_and_update_progress(msg, log_level="error", progress=100)

    def release_only(self):
        """Release the AEDT desktop without closing projects."""
        response = requests.get(self.url + "/status", timeout=DEFAULT_REQUESTS_TIMEOUT)

        if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
            self.log_and_update_progress(MSG_TK_RUNNING, log_level="debug")
        else:
            properties = {"close_projects": False, "close_on_exit": False}
            if self.close():
                requests.post(self.url + "/close_aedt", json=properties, timeout=20)

    def release_and_close(self):
        """Release and close the AEDT desktop."""
        response = requests.get(self.url + "/status", timeout=DEFAULT_REQUESTS_TIMEOUT)

        if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
            self.log_and_update_progress(MSG_TK_RUNNING, log_level="debug")
        elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
            properties = {"close_projects": True, "close_on_exit": True}
            if self.close():
                requests.post(self.url + "/close_aedt", json=properties, timeout=20)

    def on_cancel_clicked(self):
        """Handle cancel button click."""
        self.close()

    def closeEvent(self, event):
        """Handle the close event of the application window."""
        close = QtWidgets.QMessageBox.question(
            self, "QUIT", "Confirm quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if close == QtWidgets.QMessageBox.Yes:
            logger.info("Closing toolkit")
            success = self.check_connection()
            if success:
                self.release_only()
            event.accept()
        else:
            event.ignore()

    def log_and_update_progress(self, msg, log_level: str = "debug", progress: Optional[int] = None):
        """Log a message and update the progress bar.

        This method logs the given message at the specified log level, and updates the progress
        bar to the given progress percentage if provided.

        Parameters
        ----------
        msg : str
            The log message.
        log_level : str, optional
            The log level (debug, info, warning, error, critical). The default is "debug".
        progress : int, optional
            The progress percentage. If provided, it updates the progress bar.
        """

        # toolkit logging
        log_levels = {
            "debug": logger.debug,
            "info": logger.info,
            "warning": logger.warning,
            "error": logger.error,
            "critical": logger.critical,
        }
        log_func = log_levels.get(log_level, "debug")
        log_func(msg)

        # UI logging
        self.ui.update_logger(msg)

        # Update progress bar if needed
        if progress is not None:
            self.ui.update_progress(progress)
