.. _toolkit_example:

Toolkit example
===============

Explore a hands-on `toolkit example <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/examples/toolkit/pyaedt_toolkit>`_.

This example shows how to create a new toolkit using the common library.

Example walkthrough
~~~~~~~~~~~~~~~~~~~

Follow the steps outlined in the example to gain practical insights into toolkit implementation:

1. **Access the Example**: Navigate to the `toolkit example <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/examples/toolkit/pyaedt_toolkit>`_.

2. **Understanding the Toolkit Structure**:

   - Explore the directory and file structure of the example toolkit.
   - Gain insights into best practices for organizing toolkit components.

Toolkit structure
~~~~~~~~~~~~~~~~~

For optimal organization and maintainability, toolkits are recommended to adhere to the following structure:

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

Backend and frontend
~~~~~~~~~~~~~~~~~~~~

As described in the :ref:`architecture <architecture>`, toolkits must have a separation between backend and user interface.

1. **backend**: Houses backend functionalities, including API and REST API definitions, data processing, and communication with the common library.

2. **ui**: Focuses on frontend interactions, managing the user interface and connecting with backend functionalities.

API
~~~

The toolkit API controls the workflow, enabling the creation of an automated workflow without a user interface.
Inherit common methods as shown in the examples:

.. code:: python

    ToolkitBackend(AEDTCommon)


You can play with the API in the python console:

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
so they are protected. In models, specify the type. In this example, two new properties, "multiplier" and "geometry,"
are defined as float and string, respectively.

In `backend_properties.json`, define default values for both common and new properties.
These properties are correctly loaded by being imported into the toolkit API, as seen here.

.. code:: python

    from models import properties

Run backend
~~~~~~~~~~~

This script, conventionally named `rest_api.py` for its role in managing the REST API of the toolkit,
is referred to as `run_backend.py` in this example. Upon execution, this script launches a server that listens for incoming requests.

Similar to the API, this file inherits the common REST API, containing only the specific REST API functionalities
required for the toolkit. The following Python code segment imports the REST API application from the common library:

.. code:: python

    from ansys.aedt.toolkits.common.backend.rest_api import app

Additionally, it creates an instance of the toolkit API object:

.. code:: python

    toolkit_api = ToolkitBackend()

Run frontend
~~~~~~~~~~~~

The `run_frontend.py` script serves as the application launcher for the user interface, built using PySide6.
The file concludes with the following code, ensuring proper initialization using PySide6:

.. code:: python

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = ApplicationWindow()
        window.show()
        sys.exit(app.exec())

The initialization of the `ApplicationWindow` class calls different common pages defined in the
:ref:`user interface reference <user_interface>`.

If additional pages are to be added to the toolkit,
include them along with any required actions inside the "windows" directory.

Actions
~~~~~~~

Actions define the calls to the REST API, as described in the :ref:`common actions <common_actions>` reference.

User interface properties
~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to the backend, the user interface has its properties.
The `frontend_properties.json` file enables customization of the user interface theme, addition of new tabs, or modification of the URL and port for backend communication.

Run toolkit
~~~~~~~~~~~

The `run_toolkit.py` script facilitates the simultaneous execution of both the backend and user interface in two different threads.
This eliminates the need for users to launch the backend and frontend separately.
In cases where the backend is running remotely, users should first execute the backend on the remote machine before running this script.
