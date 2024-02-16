# # AEDT simple example
#
# This example shows how to use the Common AEDT API to
# launch a new AEDT session in a thread,
# create a HFSS design and create a coaxial.

# ## Perform required imports
#
# Perform required imports.

import sys
from ansys.aedt.toolkits.common.backend.api import AEDTCommon

# ## Initialize toolkit
#
# Initialize the toolkit.

toolkit = AEDTCommon()

# ## Get toolkit properties
#
# Get the toolkit properties.

properties_from_backend = toolkit.get_properties()

# ## Set properties
#
# Set non graphical mode.

set_properties = {"non_graphical": True}
flag_set_properties, msg_set_properties = toolkit.set_properties(set_properties)

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

# ## Connect design
#
# Connect or create a new design.

toolkit.connect_design("HFSS")

# ## Get toolkit properties
#
# Properties contain the project information.

new_properties = toolkit.get_properties()

# ## Create a coaxial
#
# Create a coaxial in the design.

coax = toolkit.aedtapp.modeler.create_coaxial([0, 0, 0], 1)

# ## Save and release AEDT
#
# Save and release AEDT.

toolkit.release_aedt(True, True)
