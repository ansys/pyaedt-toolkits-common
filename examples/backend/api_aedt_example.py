import time

from models import properties

from ansys.aedt.toolkits.common.backend.api import AEDTCommon
from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus

# Object with generic methods to control the toolkits
toolkit = AEDTCommon(properties)

# Get default properties
properties_from_backend = toolkit.get_properties()

# Set properties, useful to set more than one property
new_properties = {"use_grpc": True, "debug": False}
flag1, msg1 = toolkit.set_properties(new_properties)

# Get new properties
new_properties1 = toolkit.get_properties()

# You can set properties directly
properties.debug = True

# Get new properties
new_properties2 = toolkit.get_properties()

assert new_properties1["debug"] != new_properties2["debug"] == properties.debug

# Property type can not change
properties.debug = 1

# Property type can not change
new_properties3 = {"debug": [False]}
flag2, msg2 = toolkit.set_properties(new_properties3)

# Get AEDT sessions
sessions = toolkit.aedt_sessions()

# Get AEDT installed versions
versions = toolkit.installed_aedt_version()

# Launch AEDT. This is launched in a thread.
msg3 = toolkit.launch_thread(toolkit.launch_aedt)

# Get thread status
status = toolkit.get_thread_status()

# Wait until AEDT is launched.
while status == ToolkitThreadStatus.BUSY:
    time.sleep(1)
    status = toolkit.get_thread_status()

# Get new properties. Now the properties should contain the project information.
new_properties4 = toolkit.get_properties()

# Connect to the design
flag2 = toolkit.connect_design()

# Get new properties. Now the properties should contain the design information.
properties_aedt = toolkit.get_properties()

# Create a box
box = toolkit.aedtapp.modeler.create_box([10, 10, 10], [20, 20, 20])
box_name = box.name

# Release aedt
flag3 = toolkit.release_aedt()
