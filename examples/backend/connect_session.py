import time
from ansys.aedt.toolkits.common.backend.api import Backend

# Object with generic methods to control the toolkits
toolkit = Backend()

# Get default properties
properties = toolkit.get_properties()
# You can also get and set properties through the toolkit object
assert properties == toolkit.properties.export_to_dict()

# Get AEDT sessions
sessions = toolkit.aedt_sessions()

# Find if it is COM or GRPC
if sessions[0][1] == -1:
    use_grpc = False
    selected_process = sessions[0][0]
else:
    use_grpc = True
    selected_process = sessions[0][1]

# Set properties - at least one AEDT should be open
toolkit.properties.aedt_version = "2023.2"
toolkit.properties.selected_process = selected_process
toolkit.properties.use_grpc = use_grpc

# Get new properties
new_properties = toolkit.get_properties()

# Launch AEDT. This is launched in a thread, so the script and the launch_aedt call run in parallel.
msg2 = toolkit.launch_aedt()

# Get thread status
response = toolkit.get_thread_status()

# Wait until AEDT is launched.
while response[0] == 0:
    time.sleep(1)
    response = toolkit.get_thread_status()

# Get new properties. Now the properties should contain the project information.
new_properties = toolkit.get_properties()

# Connect to the design
flag2 = toolkit.connect_design("HFSS")

# Get new properties. Now the properties should contain the design information.
new_properties = toolkit.get_properties()

# Create a box
box = toolkit.aedtapp.modeler.create_box([100, 10, 10], [20, 20, 20])
box_name = box.name

# Release aedt
flag3 = toolkit.release_aedt()


