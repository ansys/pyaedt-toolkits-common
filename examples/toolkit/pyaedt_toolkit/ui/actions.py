import requests

from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger

from pyaedt.generic.general_methods import generate_unique_project_name


class Frontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def create_geometry_toolkit(self, project_selected=None, design_selected=None, geometry="Box", multiplier=1):
        # Set active project and design
        self.get_properties()
        if project_selected and design_selected:
            if project_selected == "No Project":
                project_selected = generate_unique_project_name()
                project_selected = self.get_project_name(project_selected)

            for project in self.be_properties.project_list:
                if self.get_project_name(project) == project_selected:
                    self.be_properties.active_project = project
                    if project_selected in list(self.be_properties.design_list.keys()):
                        designs = self.be_properties.design_list[project_selected]
                        for design in designs:
                            if design_selected == design:
                                self.be_properties.active_design = design
                                break
                    break
        else:
            project_selected = generate_unique_project_name()
            project_selected = self.get_project_name(project_selected)

        # Multiplier and geometry
        self.be_properties.multiplier = float(multiplier)
        self.be_properties.geometry = geometry
        self.be_properties.active_project = project_selected
        self.set_properties()

        response = requests.post(self.url + "/create_geometry")

        if response.ok:
            msg = "Geometry created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False
