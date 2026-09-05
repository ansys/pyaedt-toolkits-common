# # EDB simple example
#
# This example shows how to use the ``EDBCommon`` class to
# open an existing EDB project.

# ## Perform required imports
#
# Perform the required imports.

import os
import shutil

from ansys.aedt.core import generate_unique_folder_name

from ansys.aedt.toolkits.common.utils import download_file
from ansys.aedt.toolkits.common.backend.api import EDBCommon

# ## Initialize temporary folder and project settings
#
# Initialize a temporary folder to copy the input file into
# and specify project settings.

# +
URL_BASE = "https://raw.githubusercontent.com/ansys/example-data/master/toolkits/common/"
EDB_PROJECT = "edb_edge_ports.aedb/edb.def"
URL = os.path.join(URL_BASE, EDB_PROJECT)

temp_folder = os.path.join(generate_unique_folder_name())

edb_path = os.path.join(temp_folder, "edb_example.aedb")
os.makedirs(edb_path, exist_ok=True)
local_project = os.path.join(edb_path, "edb.def")

download_file(URL, local_project)
# -

# ## Initialize toolkit
#
# Initialize the toolkit.

toolkit = EDBCommon()

# ## Initialize EDB project
#
# Open the EDB project.

load_edb_msg = toolkit.load_edb(edb_path)

# ## Get toolkit properties
#
# Get toolkit properties, which contain the project information.

new_properties = toolkit.get_properties()
edb_project = new_properties["active_project"]

# ## Save project
#
# Copy the current project in a new file.

directory, old_file_name = os.path.split(edb_project)
new_path = os.path.join(directory, "new_edb.aedb")
toolkit.save_edb(new_path)

# ## Get cell names
#
# Get cell names using PyEDB.

toolkit.logger.info("Play with EDB")
cell_names = toolkit.edb.cell_names
toolkit.edb.nets.plot()

# ## Save and release EDB
#
# Save and release EDB.

toolkit.close_edb()

# ## Remove temporary folder
#
# Remove the temporary folder.

shutil.rmtree(temp_folder, ignore_errors=True)
