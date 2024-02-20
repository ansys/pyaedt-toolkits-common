# # AEDT open project example
#
# This example shows how to use the Common AEDT API to
# launch a new AEDT session in a thread and
# open an existing AEDT project.

# ## Perform required imports
#
# Perform required imports.

import sys
import os
import shutil

from pyaedt import generate_unique_folder_name

from ansys.aedt.toolkits.common.utils import download_file
from ansys.aedt.toolkits.common.backend.api import AEDTCommon

# ## Initialize temporary folder and project settings
#
# Initialize a temporary folder to copy the input file into
# and specify project settings.

# +
URL_BASE = "https://raw.githubusercontent.com/ansys/example-data/master/toolkits/common/"
AEDT_PROJECT = "Test.aedt"
URL = os.path.join(URL_BASE, AEDT_PROJECT)

temp_folder = os.path.join(generate_unique_folder_name())

local_project = os.path.join(temp_folder, AEDT_PROJECT)

download_file(URL, local_project)
# -

# ## Initialize toolkit
#
# Initialize the toolkit.

toolkit = AEDTCommon()

# ## Initialize AEDT
#
# Launch a new AEDT session in a thread.

thread_msg = toolkit.launch_thread(toolkit.launch_aedt)

# ## Wait for the toolkit thread to be idle
#
# Wait for the toolkit thread to be idle and ready to accept a new task.

idle = toolkit.wait_to_be_idle()
if not idle:
    print("AEDT not initialized.")
    sys.exit()

# ## Open project
#
# Open project.

open_msg = toolkit.open_project(local_project)

# ## Get toolkit properties
#
# Properties contain the project information.

new_properties = toolkit.get_properties()

# ## Connect design
#
# Connect or create a new design.

toolkit.connect_design()

# ## Create a box
#
# Create a box in the design.

toolkit.logger.info("Create Box")
box = toolkit.aedtapp.modeler.create_box([10, 10, 10], [20, 20, 20])
box.plot()

# ## Save and release AEDT
#
# Save and release AEDT.

toolkit.release_aedt(True, True)

# ## Remove temporary folder
#
# Remove the temporary folder.

shutil.rmtree(temp_folder, ignore_errors=True)
