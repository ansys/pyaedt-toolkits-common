from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger


class Frontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def start_generation(self):
        if self.backend_busy():
            msg = "Toolkit running"
            logger.debug(msg)
            self.write_log_line(msg)
            return

        pass
