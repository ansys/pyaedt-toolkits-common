import json
import os
from ansys.aedt.toolkits.common.properties_data import PropertiesData

with open(os.path.join(os.path.dirname(__file__), "properties.json")) as fh:
    _general_properties = json.load(fh)

_default_properties = {**_general_properties}
properties = PropertiesData(_default_properties)


def check_property_file_against_defaults(prop_filename):
    """
    Check if property exists in defaults.

    Parameters
    ----------
    prop_filename : str
        Qualified path of the property file to be checked

    Returns
    -------
    bool
        `True` if the files check passes, `False` otherwise
    """
    tmp_properties = PropertiesData(_default_properties)
    try:
        tmp_properties.read_from_file(prop_filename)
        return True
    except Exception as e:
        print(e)
        return False
