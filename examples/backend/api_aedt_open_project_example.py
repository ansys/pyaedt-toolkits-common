import datetime
import os
import shutil
import tempfile

from models import properties

from ansys.aedt.toolkits.common.backend.api import AEDTCommon

local_path = os.path.dirname(os.path.realpath(__file__))
test_folder = "common_toolkit_example_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
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
toolkit = AEDTCommon(properties)

# Get default properties
properties = toolkit.get_properties()

# Set properties
new_properties = {"use_grpc": True}
flag1, msg1 = toolkit.set_properties(new_properties)

# Get new properties
new_properties = toolkit.get_properties()

# Launch AEDT. This is launched in a thread.
msg2 = toolkit.launch_thread(toolkit.launch_aedt)

# Wait for the toolkit thread to be idle and ready to accept new task.
toolkit.wait_to_be_idle()

# Get new properties.
new_properties = toolkit.get_properties()

# Open project.
msg2 = toolkit.open_project(example_project)

# Get new properties. Now the properties should contain the project information.
properties_aedt1 = toolkit.get_properties()

# Connect to the design
flag2 = toolkit.connect_design()

# Get new properties. Now the properties should contain the design information.
properties_aedt2 = toolkit.get_properties()

# Create a box
toolkit.logger.info("Create Box")
box = toolkit.aedtapp.modeler.create_box([10, 10, 10], [20, 20, 20])
box_name = box.name

# Release aedtapp
flag3 = toolkit.release_aedt(True, True)
