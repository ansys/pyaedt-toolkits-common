import os
import time

from PySide6 import QtWidgets
import requests

from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus
from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.models import general_settings


class FrontendGeneric(QtWidgets.QMainWindow):
    def __init__(self):
        logger.info("Frontend initialization...")
        self.ui = None
        super(FrontendGeneric, self).__init__()

        url = general_settings.backend_url
        port = general_settings.backend_port
        self.url = f"http://{url}:{port}"

        self.logger = logger

        # Load toolkit icon
        self.images_path = os.path.join(os.path.dirname(__file__), "images")

    def poll_url(self, url: str, timeout: int = 10):
        """Perform GET requests on an URL.
        
        Continuously perform GET requests to the specified URL until a valid response is received.

        Parameters
        ----------
        timeout : int, optional
            Time out in seconds. The default is 10 seconds.
        
        Returns
        -------
        tuple
            A 2-tuple containing a string and a boolean.
            The boolean states if the GET requests succeeded.
            The string represents the response or exception content.
        """
        logger.debug(f"Poll url '{url}'")

        count = 0
        response_content = None
        response_success = False
        try:
            while not response_success and count < 10:
                time.sleep(1)
                response = requests.get(url)
                response_success = response.ok
                count += 1
        except requests.exceptions.RequestException as e:
            response_content = f"Backend error occured. Exception {str(e)}"
        else:
            response_content = response.json()
        return response_success, response_content

    def backend_busy(self):
        try:
            response = requests.get(self.url + "/status")
            res = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
            return res
        except requests.exceptions.RequestException:
            logger.error("Get backend status failed")
            return False

    def installed_versions(self):
        try:
            response = requests.get(self.url + "/installed_versions")
            if response.ok:
                versions = response.json()
                return versions
        except requests.exceptions.RequestException:
            msg = "Get AEDT installed versions failed"
            logger.error(msg)
            self.ui.logger.log(msg)
            return False

    def get_properties(self):
        try:
            response = requests.get(self.url + "/properties")
            if response.ok:
                data = response.json()
                if data:
                    logger.debug("Properties from backend updated successfully")
                    return data
                else:
                    logger.debug("Backend properties empty")
                    return False
        except requests.exceptions.RequestException:
            self.ui.logger.log("Get properties failed")

    def set_properties(self, data):
        try:
            response = requests.put(self.url + "/properties", json=data)
            if response.ok:
                response.json()
        except requests.exceptions.RequestException:
            msg = f"Set properties failed"
            logger.error(msg)
            self.ui.logger.log(msg)

    def find_process_ids(self, version):
        try:
            be_properties = self.get_properties()
            be_properties["aedt_version"] = version
            self.set_properties(be_properties)
            response = requests.get(self.url + "/aedt_sessions")
            sessions = []
            if response.ok:
                sessions = response.json()
            return sessions
        except requests.exceptions.RequestException:
            logger.error(f"Find AEDT sessions failed")
            return False

    def launch_aedt(self, selected_version, selected_process, non_graphical=False):
        response = requests.get(self.url + "/status")
        res_busy = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
        res_idle = response.ok and response.json() == ToolkitThreadStatus.IDLE.value
        if res_busy:
            msg = "Please wait, toolkit running"
            logger.debug(msg)
            self.ui.logger.log(msg)
        elif res_idle:
            self.ui.progress.progress = 0
            response = requests.get(self.url + "/health")
            if response.ok and response.json() == "Toolkit is not connected to AEDT.":
                be_properties = self.get_properties()
                if be_properties["selected_process"] == 0:
                    be_properties["aedt_version"] = selected_version
                    be_properties["non_graphical"] = non_graphical
                    if selected_process != "New Session":
                        be_properties["non_graphical"] = False
                        text_splitted = selected_process.split(" ")
                        if len(text_splitted) == 4:
                            be_properties["use_grpc"] = True
                            be_properties["selected_process"] = int(text_splitted[3])
                        else:
                            be_properties["use_grpc"] = False
                            be_properties["selected_process"] = int(text_splitted[1])
                    self.set_properties(be_properties)

                response = requests.post(self.url + "/launch_aedt")

                if response.status_code == 200:
                    self.ui.progress.progress = 50
                    msg = "Launching AEDT"
                    logger.debug(msg)
                    self.ui.logger.log(msg)
                else:
                    msg = f"Failed backend call: {self.url}"
                    logger.error(msg)
                    self.ui.logger.log(msg)
                    self.ui.progress.progress = 100
            else:
                msg = response.json()
                logger.debug(msg)
                self.ui.logger.log(msg)
                self.ui.progress.progress = 100
        else:
            msg = response.json()
            logger.debug(msg)
            self.ui.logger.log(msg)
            self.ui.progress.progress = 100

    def open_project(self, selected_project):
        response = requests.get(self.url + "/status")
        res_busy = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
        res_idle = response.ok and response.json() == ToolkitThreadStatus.IDLE.value
        if res_busy:
            msg = "Please wait, toolkit running"
            logger.debug(msg)
            self.ui.logger.log(msg)

        elif res_idle:
            self.ui.progress.progress = 0
            response = requests.get(self.url + "/health")
            if response.ok and response.json() == "Toolkit not connected to AEDT":
                response = requests.post(self.url + "/open_project", data=selected_project)
                if response.status_code == 200:
                    msg = "Project opened"
                    self.ui.logger.log(msg)
                else:
                    msg = f"Failed backend call: {self.url} + '/'open_project"
                    logger.error(msg)
                    self.ui.logger.log(msg)
                    self.ui.progress.progress = 100
            else:
                msg = response.json()
                logger.debug(msg)
                self.ui.logger.log(msg)
                self.ui.progress.progress = 100
        else:
            msg = response.json()
            logger.debug(msg)
            self.ui.logger.log(msg)
            self.ui.progress.progress = 100

    def get_aedt_data(self):
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
        be_properties = self.get_properties()
        if not active_project:
            if be_properties["active_project"] == "No Project":
                return ["No Design"]
            active_project = os.path.splitext(os.path.basename(be_properties["active_project"]))[0]
        else:
            be_properties["active_project"] = active_project
            self.set_properties(be_properties)
        design_list = be_properties["design_list"].get(active_project)
        if not design_list:
            design_list = ["No Design"]
        return design_list

    def save_project(self):
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
            response = requests.get(self.url + "/status")
            res_busy = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
            res_idle = response.ok and response.json() == ToolkitThreadStatus.IDLE.value
            if res_busy:
                self.write_log_line("Please wait, toolkit running")
            elif res_idle:
                # self.project_name.setText(file_name)
                be_properties = self.get_properties()
                # properties["active_project"] = file_name
                # self.set_properties(properties)
                # self.update_progress(0)
                response = requests.post(self.url + "/save_project", json=file_name)
                if response.ok:
                    msg = "Saving project: {}".format(file_name)
                    logger.debug(msg)
                    self.ui.logger.log(msg)
                else:
                    msg = f"Failed backend call: {self.url}"
                    logger.debug(msg)
                    self.write_log_line(msg)
                    self.ui.progress.progress = 100

    def release_only(self):
        """Release desktop."""
        response = requests.get(self.url + "/status")

        if response.ok and response.json() == "Toolkit is busy and processing a task.":
            self.write_log_line("Please wait, toolkit running")
        else:
            properties = {"close_projects": False, "close_on_exit": False}
            if self.close():
                requests.post(self.url + "/close_aedt", json=properties)

    def release_and_close(self):
        """Release and close desktop."""
        response = requests.get(self.url + "/status")

        if response.ok and response.json() == "Toolkit is busy and processing a task.":
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == "Backend free":
            properties = {"close_projects": True, "close_on_exit": True}
            if self.close():
                requests.post(self.url + "/close_aedt", json=properties)

    def on_cancel_clicked(self):
        self.close()

    def closeEvent(self, event):
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
