.. _toolkit_example:

Toolkit example
===============

The `examples/toolkit/pyaedt_toolkit <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/examples/toolkit/pyaedt_toolkit>`_
folder contains all files for creating a toolkit using the PyAEDT Common Toolkit.

Example walkthrough
~~~~~~~~~~~~~~~~~~~

Follow the steps outlined in the example to gain practical insights into toolkit implementation:

1. **Access the example**: Navigate to the `examples/toolkit/pyaedt_toolkit <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/examples/toolkit/pyaedt_toolkit>`_
   folder.

2. **Understand the toolkit structure**:

   - Explore the directory and file structure of the example toolkit.
   - Gain insights into best practices for organizing toolkit components.

Toolkit structure
~~~~~~~~~~~~~~~~~

For optimal organization and maintainability, toolkits should adhere to the following structure:

.. code-block:: text

   pyaedt-toolkits-example
   ├── backend
   │   ├── api.py
   │   ├── models.py
   │   ├── backend_properties.json
   │   └── run_backend.py
   │
   ├── ui
   │   ├── run_frontend.py
   │   ├── actions.py
   │   ├── frontend_properties.json
   │   ├── windows
   │   └── models.json
   │
   └── run_toolkit.py

Backend and UI
~~~~~~~~~~~~~~

As described in :ref:`Architecture <architecture>`, toolkits must have a separation between the
backend and UI.

- The ``backend`` directory houses backend functionalities, including API and REST API definitions,
  data processing, and communication with the common library.

- The ``ui`` folder focuses on frontend interactions, managing the UI and connecting with backend
  functionalities.

API
~~~

The ``toolkit`` API controls the workflow, enabling the creation of an automated workflow without a UI.

.. code:: python

    ToolkitBackend(AEDTCommon)

The following code shows how to inherit common methods.
You can play with the API in the Python console:

.. code:: python

    # Import API
    from examples.toolkit.pyaedt_toolkit.backend.api import ToolkitBackend

    # Object with generic methods to control the toolkits
    toolkit_api = ToolkitBackend()

    # Launch AEDT, using common API method
    toolkit_api.launch_aedt()
    toolkit_api.wait_to_be_idle()

    # Create geometry, using specific API method
    toolkit_api.create_geometry()


Models and properties
~~~~~~~~~~~~~~~~~~~~~

To introduce new properties to the toolkit, define them using models. Properties have a fixed type,
so they are protected. In models, specify the type. In this example, two new properties, ``multiplier``
and ``geometry``, are defined as float and string, respectively.

In the ``backend_properties.json`` file, define default values for both common and new properties.
These properties are correctly loaded by being imported into the toolkit API, as seen here:

.. code:: python

    from models import properties

Run backend
~~~~~~~~~~~

A script, conventionally named  ``rest_api.py`` for its role in managing the REST API of the toolkit,
is referred to as ``run_backend.py`` in this example. Upon execution, the script launches a server that
listens for incoming requests.

Similar to the API, this file inherits the common REST API, containing only the specific REST API functionalities
required for the toolkit. The following Python code imports the REST API application from the common library:

.. code:: python

    from ansys.aedt.toolkits.common.backend.rest_api import app

This code then creates an instance of the toolkit API object:

.. code:: python

    toolkit_api = ToolkitBackend()

Run frontend
~~~~~~~~~~~~

The ``run_frontend.py`` script serves as the application launcher for the UI, built using PySide6.
The file concludes with the following code, ensuring proper initialization using PySide6:

.. code:: python

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = ApplicationWindow()
        window.show()
        sys.exit(app.exec())

The initialization of the ``ApplicationWindow`` class calls different common pages defined in
:ref:`UI reference <user_interface>`.

If additional pages are to be added to the toolkit, include them along with any required actions
inside the ``windows`` directory.

Common actions
~~~~~~~~~~~~~~

Common actions define the calls to the REST API, as described in :ref:`Actions <common_actions>`.

UI properties
~~~~~~~~~~~~~

Similar to the backend, the UI has its own properties. The ``frontend_properties.json`` file enables
customization of the UI theme, addition of new tabs, and modification of the URL and port for backend
communication.

Run toolkit
~~~~~~~~~~~

The ``run_toolkit.py`` script facilitates the simultaneous execution of both the backend and UI in two
different threads. This eliminates the need for launching the backend and UI separately.
In cases where the backend is running remotely, execute the backend on the remote machine
before running this script.
