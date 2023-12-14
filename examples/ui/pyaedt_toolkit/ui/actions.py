from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger

# from ansys.aedt.toolkits.common.backend.common.properties_data import PropertiesData
#
# be_properties = PropertiesData({})
# be_properties._unfreeze()


class ToolkitFrontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def start_generation(self):
        if self.backend_busy():
            msg = "Toolkit running"
            logger.debug(msg)
            self.write_log_line(msg)
            return

        pass
