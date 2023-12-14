import os
import sys
import time

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
import qdarkstyle
import requests

from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.properties import be_properties
from ansys.aedt.toolkits.common.ui.main_window.thread_manager import FrontendThread


class FrontendGeneric(QtWidgets.QMainWindow, FrontendThread):
    def __init__(self):
        logger.info("Frontend initialization...")
        super(FrontendGeneric, self).__init__()
        # FrontendThread.__init__(self)

        self.url = None
        # Load toolkit icon
        self.images_path = os.path.join(os.path.dirname(__file__), "images")

    # def write_log_line(self, value):
    #     self.log_text.insertPlainText(value + "\n")
    #     tc = self.log_text.textCursor()
    #     tc.setPosition(self.log_text.document().characterCount())
    #     self.log_text.setTextCursor(tc)

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
            return True
        else:
            return False

    def installed_versions(self):
        try:
            response = requests.get(self.url + "/installed_versions")
            if response.ok:
                versions = response.json()
                return versions
        except requests.exceptions.RequestException:
            self.write_log_line("Get AEDT installed versions failed")
            return False

    def get_properties(self):
        try:
            response = requests.get(self.url + "/get_properties")
            if response.ok:
                properties = response.json()
                return properties
        except requests.exceptions.RequestException:
            return False

    def set_properties(self, data):
        try:
            response = requests.put(self.url + "/set_properties", json=data)
            if response.ok:
                response.json()
        except requests.exceptions.RequestException:
            self.write_log_line(f"Set properties failed")

    def change_thread_status(self):
        self.find_process_ids()
        logger.info("Frontend thread finished")
        # self.update_progress(100)

    def find_process_ids(self):
        self.aedt_sess_combobox.clear()
        all_proc_ids = []
        all_proc_ids_str = []
        try:
            # Modify selected version
            properties = self.get_properties()
            properties["aedt_version"] = self.aedt_ver_combobox.currentText()
            self.set_properties(properties)

            response = requests.get(self.url + "/aedt_sessions")
            if response.ok:
                sessions = response.json()
                for session in sessions:
                    if session[1] == -1:
                        self.aedt_sess_combobox.addItem("Process {}".format(session[0], session[1]))
                        all_proc_ids.append(session[0])
                        all_proc_ids_str.append("Process {}".format(session[0], session[1]))
                    else:
                        self.aedt_sess_combobox.addItem("Process {} on Grpc {}".format(session[0], session[1]))
                        all_proc_ids.append(session[0])
                        all_proc_ids_str.append("Process {} on Grpc {}".format(session[0], session[1]))
                if len(all_proc_ids) > 0:
                    properties["selected_process"] = all_proc_ids[0]
                else:
                    properties["selected_process"] = 0
                self.set_properties(properties)
            self.aedt_sess_combobox.addItem("Create New Session")
            all_proc_ids.append("Create New Session")
            self.aedt_sess_combobox.setCurrentIndex(0)

            return True
        except requests.exceptions.RequestException:
            self.write_log_line(f"Find AEDT sessions failed")
            return False

    def update_design_names(self):
        self.blockSignals(True)
        self.design_combobox.clear()
        try:
            # Modify selected version
            properties = self.get_properties()
            designs = properties['design_list'][self.project_combobox.currentText()]

            for design in designs:
                self.design_combobox.addItem(list(design.values())[0])
            if not designs:
                self.design_combobox.addItem("No design")

            self.design_combobox.setCurrentIndex(0)
            properties["active_design"] = designs[0]
            self.set_properties(properties)
            self.blockSignals(False)
            return True
        except requests.exceptions.RequestException:
            self.write_log_line(f"Find AEDT designs failed")
            self.blockSignals(False)
            return False

    # def find_setup_names(self):
    #     self.blockSignals(True)
    #     response = requests.get(self.url + "/get_status")
    #
    #     if response.ok and response.json() == "Backend running":
    #         self.write_log_line("Please wait, toolkit running")
    #     elif response.ok and response.json() == "Backend free":
    #         # self.setup_aedt_combo.clear()
    #         try:
    #             # Modify selected version
    #             properties = self.get_properties()
    #             current_project_selection = self.project_combobox.currentText()
    #             properties["active_project"] = current_project_selection
    #             current_design_selection = self.design_combobox.currentText()
    #             available_designs = properties['design_list'][current_project_selection]
    #             for each in available_designs: # probably better way to get the design type from desgisn_list
    #                 if current_design_selection == list(each.values())[0]:
    #                     properties["active_design"] = each
    #             self.set_properties(properties)
    #
    #             response = requests.get(self.url + "/get_setup_names")
    #             if response.ok:
    #                 setups = response.json()
    #                 # for setup in setups:
    #                 #     self.setup_aedt_combo.addItem(setup)
    #                 # if not setups:
    #                 #     self.setup_aedt_combo.addItem("No setup")
    #             self.blockSignals(False)
    #             return True
    #         except requests.exceptions.RequestException:
    #             self.write_log_line(f"Find AEDT designs failed")
    #             self.blockSignals(False)
    #             return False

    def launch_aedt(self):

        try:
            response = requests.get(self.url + "/get_status")
        except requests.exceptions.RequestException:
            logger.error("Backend not running. Launch AEDT failed.")
            return False

        properties = self.get_properties()
        selected_session = self.aedt_sess_combobox.currentText().split(" ")
        if len(selected_session) == 2:
            properties["selected_process"] = int(selected_session[1])
            properties["use_grpc"] = False
            self.set_properties(properties)
        elif len(selected_session) == 5:
            properties["selected_process"] = int(selected_session[1])
            properties["use_grpc"] = True
            self.set_properties(properties)

        if response.ok and response.json() == "Backend running":
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == "Backend free":
            # self.update_progress(0)
            response = requests.get(self.url + "/health")
            if response.ok and response.json() == "Toolkit not connected to AEDT":
                properties = self.get_properties()
                if properties["selected_process"] == 0:
                    properties["aedt_version"] = self.aedt_ver_combobox.currentText()
                    properties["non_graphical"] = False
                    if self.aedt_sess_combobox.currentText() == "Create New Session":
                        if not properties["active_project"]:
                            properties["selected_process"] = 0
                    else:
                        text_splitted = self.aedt_sess_combobox.currentText().split(" ")
                        if len(text_splitted) == 5:
                            properties["use_grpc"] = True
                            properties["selected_process"] = int(text_splitted[4])
                        else:
                            properties["use_grpc"] = False
                            properties["selected_process"] = int(text_splitted[1])
                    self.set_properties(properties)

                response = requests.post(self.url + "/launch_aedt")

                if response.status_code == 200:
                    # self.update_progress(50)
                    # Start the thread
                    self.running = True
                    logger.debug("Launching AEDT")
                    self.start()
                    if not MainFunctions.is_left_column_visible(self):
                        # Show / Hide
                        MainFunctions.toggle_left_column(self)
                        self.ui.left_menu.select_only_one_tab('btn_home')
                    # self.toolkit_tab.removeTab(0)
                else:
                    self.write_log_line(f"Failed backend call: {self.url}")
                    # self.update_progress(100)
            else:
                self.write_log_line(response.json())
                # self.update_progress(100)
        else:
            self.write_log_line(response.json())
            # self.update_progress(100)

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

    @staticmethod
    def set_font(ui_obj):
        ui_obj._font = QtGui.QFont()
        ui_obj._font.setPointSize(12)
        ui_obj.setFont(ui_obj._font)
        ui_obj.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))
        ui_obj.top_menu_bar.setFont(ui_obj._font)

    @staticmethod
    def _load_icon(images_path):
        icon = QtGui.QIcon()
        icon.addFile(
            os.path.join(images_path, "logo_cropped.png"),
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        icon.addFile(
            os.path.join(images_path, "logo_cropped.png"),
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On,
        )
        return icon


class XStream(QtCore.QObject):
    """User interface message streamer."""

    _stdout = None
    _stderr = None

    messageWritten = QtCore.Signal(str)

    def flush(self):
        """Pass."""
        pass

    def fileno(self):
        """File."""
        return -1

    def write(self, msg):
        """Write a message."""
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        """Info logger."""
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        """Error logger."""
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr
