# # Properties example
#
# This example shows how to use the properties models.
# These properties allow sharing information through all the workflow.

# ## Add new properties
#
# Before importing the common module, you can add new properties.
# You first need to create a file which contains the new properties type, [Models](models.py).
# Then add a file which sets the needed default values, [New default properties](backend_properties.json).
# Finally, import the properties.

from models import properties

# ## Perform required imports
#
# Perform required imports.

import sys
from ansys.aedt.toolkits.common.backend.api import Common

# ## Initialize toolkit
#
# Initialize the toolkit with the new properties.

toolkit = Common(properties)

# ## Get properties
#
# Get properties.

toolkit.get_properties()

# ## Set property with set_properties
#
# Set new property.

set_properties = {"invented_property": [1, 2, 3]}
toolkit.set_properties(set_properties)
toolkit.get_properties()

# ## Set property directly
#
# Set property directly.

properties.invented_property = [10, 20, 30]
toolkit.get_properties()

# ## Set wrong property
#
# It is not possible to change property type.

set_properties = {"invented_property": 1}
toolkit.set_properties(set_properties)
