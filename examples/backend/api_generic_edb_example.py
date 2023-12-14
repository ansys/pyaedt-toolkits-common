import time
from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric

# Object with generic methods to control the toolkits
toolkit = ToolkitGeneric()

# Get default properties
properties = toolkit.get_properties()

# Set properties, useful to set more than one property
new_properties = {"aedt_version": "2024.1"}
flag1, msg1 = toolkit.set_properties(new_properties)

# Get new properties
new_properties = toolkit.get_properties()

# You can also get and set properties through the toolkit object
assert new_properties == toolkit.properties.export_to_dict()

# You can also set properties directly
toolkit.properties.aedt_version = "2023.2"

# Get new properties
new_properties = toolkit.get_properties()

# Get AEDT sessions
sessions = toolkit.aedt_sessions()

# Get AEDT installed versions
versions = toolkit.installed_aedt_version()

# Launch AEDT. This is launched in a thread.
msg2 = toolkit.aedt_common.launch_aedt()

# Get thread status
response = toolkit.get_thread_status()

# Wait until AEDT is launched.
while response[0] == 0:
    time.sleep(1)
    response = toolkit.get_thread_status()

# Get new properties. Now the properties should contain the project information.
new_properties = toolkit.get_properties()

# Connect to the design
flag2 = toolkit.aedt_common.connect_design()

# Get new properties. Now the properties should contain the design information.
new_properties = toolkit.get_properties()

# Create a box
box = toolkit.aedt_common.aedtapp.modeler.create_box([10, 10, 10], [20, 20, 20])
box_name = box.name

# Release aedt
flag3 = toolkit.aedt_common.release_aedt()



