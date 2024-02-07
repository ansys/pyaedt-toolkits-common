# To run this example the user must have at least one active AEDT session.

from models import properties

from ansys.aedt.toolkits.common.backend.api import AEDTCommon

# Object with generic methods to control the toolkits
toolkit = AEDTCommon(properties)

# Get properties
new_properties = toolkit.get_properties()

# Get AEDT sessions
sessions = toolkit.aedt_sessions()

# Find if it is COM or GRPC
first_key, first_value = next(iter(sessions.items()))

if first_value == -1:
    use_grpc = False
    selected_process = first_key
else:
    use_grpc = True
    selected_process = first_value

# Set properties
new_properties = {"selected_process": selected_process, "use_grpc": use_grpc}
flag, msg = toolkit.set_properties(new_properties)

# Get new properties
new_properties = toolkit.get_properties()

# Launch AEDT. This is launched in a thread, so the script and the launch_aedt call run in parallel.
msg2 = toolkit.launch_thread(toolkit.launch_aedt)

# Wait for the toolkit thread to be idle and ready to accept new task.
toolkit.wait_to_be_idle()

# Get new properties. Now the properties should contain the project information.
new_properties = toolkit.get_properties()

# Connect to the design
flag2 = toolkit.connect_design("HFSS")

# Get new properties. Now the properties should contain the design information.
properties_aedt = toolkit.get_properties()

# Create a box
toolkit.logger.info("Create Box")
box = toolkit.aedtapp.modeler.create_box([100, 10, 10], [20, 20, 20])
box_name = box.name

# Release aedt
flag3 = toolkit.release_aedt()
