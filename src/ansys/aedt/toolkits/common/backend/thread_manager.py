from functools import wraps
import threading
import time
from typing import List

from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.common.backend.models import properties


class ThreadManager(object):
    """Class to control toolkit threads."""

    toolkit_thread_name = "Toolkit_Thread"

    def __init__(self):
        pass

    @classmethod
    def process_exe(cls, process, *args):
        """Execute process."""
        # Set the variable at process start
        properties.is_toolkit_busy = True

        # Start
        process(*args)

        # Waits for the thread closure
        time.sleep(0.5)

        # Set the variable at process end
        properties.is_toolkit_busy = False

    @classmethod
    def launch_thread(cls, process):
        """Launch process."""

        @wraps(process)
        def inner_function(*args):
            if not properties.is_toolkit_busy:
                # Multithreading fails with COM
                logger.debug("Starting thread: {}".format(cls.toolkit_thread_name))
                properties.is_toolkit_busy = True
                running_thread = threading.Thread(
                    target=cls.process_exe,
                    name=cls.toolkit_thread_name,
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

        return inner_function

    @staticmethod
    def running_threads() -> List[threading.Thread]:
        """List the running threads."""
        threads_list = [thread for thread in threading.enumerate() if type(thread) == threading.Thread]
        return threads_list

    @classmethod
    def is_toolkit_thread_running(cls) -> bool:
        """Check if the thread associated to the toolkit is running."""
        running_threads_names = [t.name for t in cls.running_threads()]
        return cls.toolkit_thread_name in running_threads_names
