import time

from models import properties

from ansys.aedt.toolkits.common.backend.api import AEDTCommon
from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus

# Object with generic methods to control the toolkits
toolkit = AEDTCommon(properties)

# Get properties
new_properties = toolkit.get_properties()

# Get AEDT sessions
sessions = toolkit.aedt_sessions()

# Find if it is COM or GRPC
if sessions[0][1] == -1:
    use_grpc = False
    selected_process = sessions[0][0]
else:
    use_grpc = True
    selected_process = sessions[0][1]

# Set properties
new_properties = {"selected_process": selected_process, "use_grpc": use_grpc}
flag, msg = toolkit.set_properties(new_properties)

# Get new properties
new_properties = toolkit.get_properties()

# Launch AEDT. This is launched in a thread, so the script and the launch_aedt call run in parallel.
msg2 = toolkit.launch_thread(toolkit.launch_aedt)

# Get thread status
status = toolkit.get_thread_status()

# Wait until AEDT is launched.
while status == ToolkitThreadStatus.BUSY:
    time.sleep(1)
    status = toolkit.get_thread_status()

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
