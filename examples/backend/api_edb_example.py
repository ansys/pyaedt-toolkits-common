import datetime
import os
import shutil
import tempfile

from ansys.aedt.toolkits.common.backend.api import EDBCommon

local_path = os.path.dirname(os.path.realpath(__file__))
test_folder = "common_toolkit_example_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
scratch_path = os.path.join(tempfile.gettempdir(), test_folder)
if not os.path.exists(scratch_path):
    try:
        os.makedirs(scratch_path)
    except:
        pass
example_project = shutil.copytree(
    os.path.join(local_path, "example_models", "edb_edge_ports.aedb"), os.path.join(scratch_path, "edb_edge_ports.aedb")
)

# Object with generic methods to control the toolkits
toolkit = EDBCommon()

# Load EDB project
msg2 = toolkit.load_edb(example_project)

# Get new properties
new_properties = toolkit.get_properties()

edb_project = new_properties["active_project"]

# Save project
directory, old_file_name = os.path.split(edb_project)
new_path = os.path.join(directory, "new_edb.aedb")
toolkit.save_edb(new_path)

# Save active project
toolkit.save_edb()

# Edb API
toolkit.logger.info("Play with EDB")
cell_names = toolkit.edb.cell_names

# Close EDB project
msg2 = toolkit.close_edb()
