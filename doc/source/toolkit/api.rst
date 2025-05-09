Backend API reference
=====================
The backend API contains three classes, `AEDTCommon``, ``EDBCommon``, and ``Common``,
which provide methods for controlling the toolkit workflow:

- ``AEDTCommon``: Provides methods for controlling AEDT. This class inherits the ``Common`` class.
- ``EDBCommon``: Provides methods for controlling EDB. This class inherits the ``Common`` class.
- ``Common``: Provides methods for controlling the toolkit flow.

In the following descriptions, you can click the class name to view detailed API information.

.. currentmodule:: ansys.aedt.toolkits.common.backend.api

.. autosummary::
   :toctree: _autosummary

   AEDTCommon
   EDBCommon
   Common

This code shows how to use the ``AEDTCommon`` class:

.. code:: python

    # Import API
    from ansys.aedt.toolkits.common.backend.api import AEDTCommon
    from ansys.aedt.toolkits.common.utils import ToolkitThreadStatus

    # Object with generic methods to control the toolkits
    toolkit = AEDTCommon(properties)

    # Get the default properties
    properties_from_backend = toolkit.get_properties()

    # Set properties, which is useful for setting more than one property
    new_properties = {"use_grpc": True, "debug": False}
    flag1, msg1 = toolkit.set_properties(new_properties)

    # Get new properties
    new_properties1 = toolkit.get_properties()

    # Get AEDT installed versions
    versions = toolkit.installed_aedt_version()

    # Launch AEDT in a thread
    msg3 = toolkit.launch_thread(toolkit.launch_aedt)

    # Wait until thread is finished
    toolkit.wait_to_be_idle()

    # Get new properties, which should now contain project information
    new_properties4 = toolkit.get_properties()

    # Connect to the design
    flag2 = toolkit.connect_design()

    # Create a box
    box = toolkit.aedtapp.modeler.create_box([10, 10, 10], [20, 20, 20])
    box_name = box.name

    # Release AEDT
    flag3 = toolkit.release_aedt()
