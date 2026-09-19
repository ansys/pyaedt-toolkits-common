# # AEDT open project example
#
# This example shows how to use the ``AEDTCommon`` class to
# launch a new AEDT session in a thread and
# open an existing AEDT project.

# ## Perform required imports
#
# Perform the required imports.

import sys
import os
import shutil

from ansys.aedt.core import generate_unique_folder_name

from ansys.tools.common.example_download import download_manager
from ansys.aedt.toolkits.common.backend.api import AEDTCommon

# ## Initialize temporary folder and project settings
#
# Initialize a temporary folder to copy the input file into
# and specify project settings.

temp_folder = os.path.join(generate_unique_folder_name())
local_project = download_manager.download_file("Test.aedt", "toolkits/common", temp_folder)

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
# Open the project.

open_msg = toolkit.open_project(local_project)

# ## Get toolkit properties
#
# Get the toolkit properties, which contain the project information.

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
model = toolkit.aedtapp.plot(show=True)

# ## Save and release AEDT
#
# Save and release AEDT.

toolkit.release_aedt(True, True)

# ## Remove temporary folder
#
# Remove the temporary folder.

shutil.rmtree(temp_folder, ignore_errors=True)
