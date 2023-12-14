import logging
import os

from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
import requests

from ansys.aedt.toolkits.common.ui.properties import be_properties

logger = logging.getLogger("Global")


class FrontendThread(QThread):
    def __int__(self):
        self.status_changed = Signal(bool)
        self.running = True

    def run(self):
        while self.running:
            response = requests.get(self.url + "/get_status")
            if response.ok and response.json() != "Backend running":
                self.running = False
                self.get_properties()
                if be_properties.active_project and "project_aedt_combo" in self.__dir__():
                    self.project_aedt_combo.clear()
                    if not be_properties.project_list:
                        self.project_aedt_combo.addItem("No project")
                    else:
                        cont = 0
                        for project in be_properties.project_list:
                            active_project_name = self.get_project_name(project)
                            self.project_aedt_combo.addItem(active_project_name)
                            if active_project_name == self.get_project_name(project):
                                self.project_aedt_combo.setCurrentIndex(cont)
                            cont += 1

                if be_properties.active_design and "design_aedt_combo" in self.__dir__():
                    self.design_aedt_combo.clear()
                    if not be_properties.design_list:
                        self.design_aedt_combo.addItem("No design")
                    else:
                        cont = 0
                        design_name = be_properties.active_design
                        active_design_list = be_properties.design_list[active_project_name]
                        for design in active_design_list:
                            self.design_aedt_combo.addItem(list(design.values())[0])
                            if list(design_name.values())[0] == design:
                                self.design_aedt_combo.setCurrentIndex(cont)
                            cont += 1

                # Emit the status_changed signal if the status changes
                self.status_changed.emit(self.running)

            # Sleep for a certain amount of time before checking again
            self.msleep(200)

#
# class Worker(QThread):
#     # Worker thread class
#     finished = Signal()
#
#     def run(self):
#         # your lengthy process here
#         print("Run some process")
#         self.finished.emit()
#
#
# class ApplicationWindow:
#
#     def __init__(self):
#         super(ApplicationWindow, self).__init__()
#
#         self.thread = None  # Worker thread object
#
#     def start_thread(self):
#         if not self.thread:
#             self.thread = Worker()
#
#             # connect signal from Worker thread to slot in ApplicationWindow
#             self.thread.finished.connect(self.thread_finished)
#
#             self.thread.start()
#
#     def stop_thread(self):
#         if self.thread:
#             self.thread.quit()
#             self.thread.wait()
#             self.thread = None
#
#     @Slot()
#     def thread_finished(self):
#         print("Thread finished.")
#         self.stop_thread()  # You can optionally stop and delete the thread here
#
#     def thread_running(self):
#         return bool(self.thread)