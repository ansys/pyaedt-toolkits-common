# # AEDT API example
#
# This example shows how to use the common AEDT API to launch a new AEDT session in a thread, create an Icepak design
# and create a box.

# ## Perform required imports
#
# Perform required imports.

# +

from ansys.aedt.toolkits.common.backend.api import AEDTCommon

# -

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
# Modify properties with a dictionary.

new_properties = {"use_grpc": True, "debug": False}
flag_set_properties, msg_set_properties = toolkit.set_properties(new_properties)


# ## Initialize AEDT
#
# Launch a new AEDT session in a thread.

thread_msg = toolkit.launch_thread(toolkit.launch_aedt)

# ## Wait for the toolkit thread to be idle
#
# Wait for the toolkit thread to be idle and ready to accept a new task.

toolkit.wait_to_be_idle()

# ## Connect design
#
# Connect or create a new design.

toolkit.connect_design("Icepak")

# ## Get toolkit properties
#
# Properties contain the project information.

new_properties_from_backend = toolkit.get_properties()

# ## Create a box
#
# Create a box in the design.

box = toolkit.aedtapp.modeler.create_box([10, 10, 10], [20, 20, 20])

# ## Save and release AEDT
#
# Save and release AEDT.

toolkit.release_aedt(True, True)
