# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import threading
import time
from typing import List

from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.common.backend.models import common_properties


class ThreadManager(object):
    """Controls toolkit threads.

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
        else:  # pragma: no cover
            return False

    @staticmethod
    def running_threads() -> List[threading.Thread]:
        """List the running threads."""
        threads_list = [thread for thread in threading.enumerate() if type(thread) == threading.Thread]
        return threads_list

    @classmethod
    def is_toolkit_thread_running(self) -> bool:
        """Check if the thread associated with the toolkit is running."""
        running_threads_names = [t.name for t in self.running_threads()]
        return self.toolkit_thread_name in running_threads_names
