.. _architecture:

Architecture
============

This repository is a common API for any new AEDT toolkit. It standardizes AEDT toolkits implementation.

The API provides some methods to connect to an existing AEDT session, open an existing
AEDT project or initialize a new AEDT session, which should be the basic capability of any toolkit.

The architecture is divided in two main parts:


1. **Backend**: Comprising API and REST API, the API is built on PyAEDT, and the REST API utilizes `Flask <https://flask.palletsprojects.com/en/2.3.x/>`_.
Flask facilitates the creation of a REST API, enabling interaction between different services through HTTP requests.

2. **User interface**: Implemented using `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_.
Pyside6 includes a designer tool for creating user interfaces, translated directly to Python.

By leveraging Flask, the toolkit becomes interface-agnostic, allowing flexibility in choosing different user interfaces such as a WebUI.

Installation
~~~~~~~~~~~~

The library can be installed like any other open source package and added as a dependency to the new toolkit project.
:ref:`Installation page <installation>`.

Toolkit architecture diagram
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: ../_static/toolkit_architecture.png
  :width: 800
  :alt: Toolkit architecture

Toolkit frontend and backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The library is structured as follows:

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

1. `.github <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/.github>`_: Contains GitHub actions configuration.

2. `doc <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/doc>`_: Documentation structure.

3. `common <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common>`_: Toolkit code, split into backend and frontend.

    3.1 `backend <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/backend>`_: The non-user-facing part of the toolkit, handling requests and preparing data for the frontend. Key files include:

        3.1.1 **rest_api.py**: Defines Flask entrypoints.
        3.1.2 **api.py**: Defines the toolkit API.
        3.1.3 **common_properties.json**: Defines common backend properties.
        3.1.4 **models.py**: Defines the properties class to store backend properties.

    3.2 `ui <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/ui>`_: The user interface part of the toolkit. Key files include:

        3.2.1 **common_properties.json**: Defines common user interface properties.
        3.2.2 **models.py**: Defines the properties class to store user interface properties.

4. `tests <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/tests>`_: Folder containing backend unit tests.

Models and properties
~~~~~~~~~~~~~~~~~~~~~

The `models.py <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/backend/models.py>`_
stores the backend properties that are shared between backend and frontend. Properties are loaded by loading the content of
`properties <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/backend/common_properties.json>`_ in the class properties.

To understand how backend and frontend interact you can refer to `ui actions <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py>`_.
For example, when an event is triggered by the frontend, the `get_properties() <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py#L143>`_
method builds the GET HTTP request to send to the backend to retrieve properties from backend.
The event of setting up a property calls the `set_properties() <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py#L165>`_
method which builds the PUT HTTP request that is sent to the backend.

API
~~~

The :doc:`../toolkit/api` contains three classes: ``Common``, ``AEDTCommon``, ``EDBCommon``, which provides methods for
controlling the toolkit workflow.

REST API
~~~~~~~~

REST APIs are standard web interfaces allowing clients to communicate with services via HTTP requests.
JSON is the standard for transferring data. In fact REST APIs accept JSON for request payload and also send responses
to JSON.

In the client-server architecture model, the client sends the request to the server to fetch some information.
Server-side technologies decode JSON information and transmit back the response to the client and this interaction is
handled by the HTTP protocol.

How frontend and backend interact?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Frontend sends HTTP requests to retrieve data, while the backend returns appropriate results.

The toolkit uses CRUD (Create, Read, Update & Delete) operations that simply are HTTP request methods that specify
the action to perform through the request.

UI
~~

For UI reference see :doc:`../toolkit/ui`