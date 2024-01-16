import json
import os

from ansys.aedt.toolkits.common.properties_data import PropertiesData

with open(os.path.join(os.path.dirname(__file__), "properties.json")) as fh:
    _properties = json.load(fh)

_default_properties = {**_properties}
general_settings = PropertiesData(_default_properties)

be_properties = PropertiesData({})
be_properties._unfreeze()
