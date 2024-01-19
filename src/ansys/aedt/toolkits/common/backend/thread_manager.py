import threading
import time
from typing import List

from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.common.backend.models import common_properties


class ThreadManager(object):
    """Class to control toolkit threads.

    Parameters
    ----------
    backend_properties : :class:`backend.models.Properties`
        Updated properties.

    """

    toolkit_thread_name = "Toolkit_Thread"

    def __init__(self, backend_properties=None):
        self.properties = common_properties
        if backend_properties:
            self.properties = backend_properties

    def process_exe(self, process, *args):
        """Execute process."""
        # Set the variable at process start
        self.properties.is_toolkit_busy = True

        # Start
        process(*args)

        # Waits for the thread closure
        time.sleep(0.5)

        # Set the variable at process end
        self.properties.is_toolkit_busy = False

    def launch_thread(self, process, *args):
        """Launch process."""
        if not self.properties.is_toolkit_busy:
            # Multithreading fails with COM
            logger.debug("Starting thread: {}".format(self.toolkit_thread_name))
            common_properties.is_toolkit_busy = True
            running_thread = threading.Thread(
                target=self.process_exe,
                name=self.toolkit_thread_name,
                args=(
                    process,
                    *args,
                ),
                daemon=True,
            )
            running_thread.start()
            return True
        else:
            return False

    @staticmethod
    def running_threads() -> List[threading.Thread]:
        """List the running threads."""
        threads_list = [thread for thread in threading.enumerate() if type(thread) == threading.Thread]
        return threads_list

    @classmethod
    def is_toolkit_thread_running(self) -> bool:
        """Check if the thread associated to the toolkit is running."""
        running_threads_names = [t.name for t in self.running_threads()]
        return self.toolkit_thread_name in running_threads_names
