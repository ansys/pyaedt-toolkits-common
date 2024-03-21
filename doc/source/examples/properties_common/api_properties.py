# # Properties example
#
# This example shows how to use the ``Common`` class, which contains properties models.
# These properties provide for sharing information through all the workflow.

# ## Add new properties
#
# Before importing the common module, you can add new properties.
# First create a file that contains the new properties type, [Models](models.py).
# Then add a [TOML file](backend_properties.toml) that sets the needed default values.
# Finally, import the properties.

from models import properties

# ## Perform required imports
#
# Perform the required imports.

import sys
from ansys.aedt.toolkits.common.backend.api import Common

# ## Initialize toolkit
#
# Initialize the toolkit with the new properties.

toolkit = Common(properties)

# ## Get properties
#
# Get the properties.

toolkit.get_properties()

# ## Set property
#
# Use ``set_properties`` to set the new property.

set_properties = {"invented_property": [1, 2, 3]}
toolkit.set_properties(set_properties)
toolkit.get_properties()

# ## Set property directly
#
# Set the property directly.

properties.invented_property = [10, 20, 30]
toolkit.get_properties()

# ## Set wrong property
#
# Set the wrong property. It is not possible to change the property type.

set_properties = {"invented_property": 1}
toolkit.set_properties(set_properties)
