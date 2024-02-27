.. _rest_api:

REST API
========

REST APIs are the most common web interfaces that allow various clients to communicate with services via the REST API.
JSON is the standard for transferring data. In fact REST APIs accept JSON for request payload and also send responses
to JSON.
In the client-server architecture model, the client sends the request to the server to fetch some information.
Server-side technologies decode JSON information and transmit back the response to the client and this interaction is
handled by the HTTP protocol.

How frontend and backend interact?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Frontend sends a HTTP request to retrieve data, while backend returns appropriate results.

The toolkit uses CRUD (Create, Read, Update & Delete) operations that simply are HTTP request methods that specify
the action to perform through the request.

Toolkit frontend and backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Toolkit architecture is defined with the following structure:

.. code-block:: text

   pyaedt-toolkits-common
   ├── .github
   │   └──workflows
   │      └── ci_cd.yml
   ├── doc
   │   └──source
   │      ├── examples
   │      └── getting_started
   │      └── toolkit
   ├── src.ansys.aedt.toolkits
   │    └──common
   │       ├── backend
   │       │   ├── api.py
   │       │   ├── rest_api.py
   │       │   ├── common_properties.json
   │       │   └── models.py
   │       ├── ui
   │       │   ├── common_windows
   │       │   ├── main_window
   │       │   └── utils
   │       │   └── common_properties.json
   │       │   └── models.py
   ├── tests
   │   └── backend
   ├── pyproject.toml
   └── README.rst

1. `.github <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/.github>`_ contains the GitHub actions.

2. `doc <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/doc>`_ contains the documentation structure.

3. `common <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common>`_ contains the toolkit code. It is split in backend and frontend.

    3.1 `backend <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/backend>`_: It is the part of the toolkit that is not visible to the end user.
        It receives requests and prepares data which is sent back to the frontend.
        There are four important files:
            3.1.1 **rest_api.py** where the HTTP requests are defined.
            3.1.2 **api.py** where the toolkit API is defined.
            3.1.3 **common_properties.json** where the common backend properties are defined.
            3.1.4 **models.py** defines the **Properties** class to store all backend properties.

    3.2 `ui <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/ui>`_: It is the part of the toolkit that interfaces with the end user.
        There are two main files:
        3.2.1 **common_properties.json** where the common ui properties are defined.
        3.2.2 **models.py** defines the **UIProperties** class to store all ui properties.

4. `tests <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/tests>`_: folder containing the unit tests of the backend.

How the information is exchanged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To understand how backend and frontend interact you can refer to `ui actions <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py>`_.
For example, when an event is triggered by the frontend, the `get_properties() <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py#L143>`_
method builds the GET HTTP request to send to the backend in order to retrieve properties from backend.
The event of setting up a property calls the `set_properties() <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py#L165>`_
method which builds the PUT HTTP request that is sent to the backend.