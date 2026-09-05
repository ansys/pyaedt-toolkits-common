Toolkit API
===========
The Toolkit API contains the ``Toolkit`` class, which provides methods for
controlling the toolkit workflow. In addition to methods for creating a new
or connecting to an existing AEDT session, this API provides methods for automating
the segmentation and skew of a 3D motor.

.. currentmodule:: ansys.aedt.toolkits.motor.backend.api

.. autosummary::
   :toctree: _autosummary

   Toolkit

This code shows how to use the ``Toolkit`` class:

.. code:: python

    # Import required modules
    import time

    # Import backend
    from ansys.aedt.toolkits.motor.backend.api import Toolkit

    # Initialize generic service
    service = Toolkit()

    # Get the default properties loaded from JSON file
    properties = service.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2023.2"}
    service.set_properties(new_properties)
    properties = service.get_properties()

    # Launch AEDT
    msg = service.launch_aedt()

    # Wait until thread is finished
    response = service.get_thread_status()
    while response[0] == 0:
        time.sleep(1)
        response = service.get_thread_status()

    # Segment and skew motor
    service.segmentation()
    service.apply_skew()

    # Release AEDT
    service.release_aedt()
