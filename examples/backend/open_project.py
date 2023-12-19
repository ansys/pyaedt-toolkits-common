import time
import os
import datetime
import tempfile
import shutil
from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric

local_path = os.path.dirname(os.path.realpath(__file__))
test_folder = "common_toolkit_example" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
scratch_path = os.path.join(tempfile.gettempdir(), test_folder)
if not os.path.exists(scratch_path):
    try:
        os.makedirs(scratch_path)
    except:
        pass
example_project = shutil.copy(
    os.path.join(local_path, "example_models", "Test.aedt"), os.path.join(scratch_path, "Test.aedt")
)

# Object with generic methods to control the toolkits
toolkit = ToolkitGeneric()

# Get default properties
properties = toolkit.get_properties()

# Set properties
new_properties = {"aedt_version": "2023.2"}
flag1, msg1 = toolkit.set_properties(new_properties)

# Get new properties
new_properties = toolkit.get_properties()

# Launch AEDT. This is launched in a thread.
msg2 = toolkit.aedt_common.launch_aedt()

# Get thread status
response = toolkit.get_thread_status()

# Wait until AEDT is launched.
while response[0] == 0:
    time.sleep(1)
    response = toolkit.get_thread_status()

# Get new properties.
new_properties = toolkit.get_properties()

# Open project.
msg2 = toolkit.aedt_common.open_project(example_project)

# Get new properties. Now the properties should contain the project information.
new_properties = toolkit.get_properties()

# Connect to the design
flag2 = toolkit.aedt_common.connect_design()

# Get new properties. Now the properties should contain the design information.
new_properties = toolkit.get_properties()

# Create a box
box = toolkit.aedt_common.aedtapp.modeler.create_box([10, 10, 10], [20, 20, 20])
box_name = box.name

# Release aedtapp
flag3 = toolkit.aedt_common.release_aedt()
