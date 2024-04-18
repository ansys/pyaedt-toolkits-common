from pyaedt.generic.general_methods import generate_unique_project_name
import requests

from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger


class Frontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def create_geometry_toolkit(self, project_selected=None, design_selected=None):
        # Set active project and design
        be_properties = self.get_properties()
        if project_selected and design_selected:
            if project_selected == "No Project":
                project_selected = generate_unique_project_name(rootname=self.plot_design_menu.temp_folder)
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

        response = requests.post(self.url + "/create_geometry")

        self.properties.example.primitives_created.append(response.text)

        if response.ok:
            msg = "Geometry created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False
