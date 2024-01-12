import requests

from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger


class Frontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def create_geometry_toolkit(self, project_selected=None, design_selected=None, geometry="Box", multiplier=1):

        self.ui.progress.progress = 0

        # Set active project and design
        self.get_properties()
        if project_selected and design_selected:
            for project in self.be_properties.project_list:
                if self.get_project_name(project) == project_selected and project_selected != "No project":
                    self.be_properties.active_project = project
                    if project_selected in list(self.be_properties.design_list.keys()):
                        designs = self.be_properties.design_list[project_selected]
                        for design in designs:
                            if design_selected in list(design.values())[0]:
                                self.be_properties.active_design = design
                                break
                    break

        # Multiplier and geometry
        self.be_properties.multiplier = float(multiplier)
        self.be_properties.geometry = geometry
        self.set_properties()

        response = requests.post(self.url + "/create_geometry")

        if response.ok:
            self.ui.progress.progress = 50
            # Start the thread
            self.running = True
            self.start()
            msg = "Create geometry call launched"
            logger.debug(msg)
            self.write_log_line(msg)
        else:
            msg = f"Failed backend call: {self.url}"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
