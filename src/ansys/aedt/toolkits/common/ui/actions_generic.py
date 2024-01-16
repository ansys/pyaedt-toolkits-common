import os
import time

from PySide6 import QtWidgets
import requests

from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.properties import be_properties


class FrontendGeneric(QtWidgets.QMainWindow):

    def __init__(self):
        logger.info("Frontend initialization...")
        self.ui = None
        super(FrontendGeneric, self).__init__()

        self.be_properties = be_properties
        self.url = None
        self.logger = logger

        # Load toolkit icon
        self.images_path = os.path.join(os.path.dirname(__file__), "images")

    def check_connection(self):
        try:
            logger.debug("Check backend connection")
            count = 0
            response = False
            while not response and count < 10:
                time.sleep(1)
                response = requests.get(self.url + "/health")
                count += 1

            if response.ok:
                logger.debug(response.json())
                return True
            logger.error(response.json())
            return False

        except requests.exceptions.RequestException as e:
            logger.error("Backend not running")
            return False

    def backend_busy(self):
        response = requests.get(self.url + "/get_status")
        if response.ok and response.json() == "Backend running":
            # logger.debug("Backend running")
            return True
        else:
            logger.debug("Backend free")
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
            response = requests.get(self.url + "/get_properties")
            if response.ok:
                data = response.json()
                logger.debug("Updating the properties from backend.")
                if data:
                    for key in data:
                        setattr(be_properties, key, data[key])
                    logger.debug("Properties from backend updated successfully.")
                    return True
                else:
                    logger.debug("body is empty!")
                    return False
        except requests.exceptions.RequestException:
            self.ui.logger.log("Get properties failed")

    def set_properties(self):
        try:
            response = requests.put(self.url + "/set_properties", json=be_properties.export_to_dict())
            if response.ok:
                response.json()
        except requests.exceptions.RequestException:
            msg = f"Set properties failed"
            logger.error(msg)
            self.ui.logger.log(msg)

    def find_process_ids(self, version):
        try:
            self.get_properties()
            be_properties.aedt_version = version
            self.set_properties()
            response = requests.get(self.url + "/aedt_sessions")
            sessions = []
            if response.ok:
                sessions = response.json()
            return sessions
        except requests.exceptions.RequestException:
            logger.error(f"Find AEDT sessions failed")
            return False

    def launch_aedt(self, selected_version, selected_process, non_graphical=False):
        response = requests.get(self.url + "/get_status")

        if response.ok and response.json() == "Backend running":
            msg = "Please wait, toolkit running"
            logger.debug(msg)
            self.ui.logger.log(msg)

        elif response.ok and response.json() == "Backend free":
            self.ui.progress.progress = 0
            response = requests.get(self.url + "/health")
            if response.ok and response.json() == "Toolkit not connected to AEDT":
                self.get_properties()
                if be_properties.selected_process == 0:
                    be_properties.aedt_version = selected_version
                    be_properties.non_graphical = non_graphical
                    if selected_process != "New Session":
                        text_splitted = selected_process.split(" ")
                        if len(text_splitted) == 5:
                            be_properties.use_grpc = True
                            be_properties.selected_process = int(text_splitted[4])
                        else:
                            be_properties.use_grpc = False
                            be_properties.selected_process = int(text_splitted[1])
                    self.set_properties()

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
        response = requests.get(self.url + "/get_status")

        if response.ok and response.json() == "Backend running":
            msg = "Please wait, toolkit running"
            logger.debug(msg)
            self.ui.logger.log(msg)

        elif response.ok and response.json() == "Backend free":
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
        self.get_properties()
        project_list = []
        if be_properties.active_project:
            if be_properties.project_list:
                for project in be_properties.project_list:
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
        self.get_properties()
        if not active_project:
            if be_properties.active_project == "No Project":
                return ["No Design"]
            active_project = os.path.splitext(os.path.basename(be_properties.active_project))[0]
        else:
            be_properties.active_project = active_project
            self.set_properties()
        design_list = be_properties.design_list.get(active_project)
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
            response = requests.get(self.url + "/get_status")

            if response.ok and response.json() == "Backend running":
                self.write_log_line("Please wait, toolkit running")
            elif response.ok and response.json() == "Backend free":
                # self.project_name.setText(file_name)
                properties = self.get_properties()
                # properties["active_project"] = file_name
                # self.set_properties(properties)
                # self.update_progress(0)
                response = requests.post(self.url + "/save_project", json=file_name)
                if response.ok:
                    # self.update_progress(50)
                    # Start the thread
                    self.running = True
                    logger.debug("Saving project: {}".format(file_name))
                    self.start()
                    self.write_log_line("Saving project process launched")
                else:
                    msg = f"Failed backend call: {self.url}"
                    logger.debug(msg)
                    self.write_log_line(msg)
                    # self.update_progress(100)

    def release_only(self):
        """Release desktop."""
        response = requests.get(self.url + "/get_status")

        if response.ok and response.json() == "Backend running":
            self.write_log_line("Please wait, toolkit running")
        else:
            properties = {"close_projects": False, "close_on_exit": False}
            if self.close():
                requests.post(self.url + "/close_aedt", json=properties)

    def release_and_close(self):
        """Release and close desktop."""
        response = requests.get(self.url + "/get_status")

        if response.ok and response.json() == "Backend running":
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
