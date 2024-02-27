.. _architecture:

Architecture
============

This repository is a common API for any new AEDT toolkit. It standardizes AEDT toolkits implementation.

The API provides some methods to connect to an existing AEDT session, open an existing
AEDT project or initialize a new AEDT session, which should be the basic capability of any toolkit.

The architecture is divided in two main parts:


1. The backend, using `Flask <https://flask.palletsprojects.com/en/2.3.x/>`_. Flask creates a REST API,
which let interact different services by simply doing HTTP requests.

2. The user interface, using `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_. Pyside6 has a designer tool
which allows to create user interfaces and it is translated to python directly.

Using Flask, the toolkit becomes interface agnostic, then you can decide change it and use a WebUI for instance
as user interface.

You can install the library like any other open source package. You can add this project as a dependency of the new toolkit.

The architecture is defined in the following picture:

.. image:: ../_static/toolkit_architecture.png
  :width: 800
  :alt: Toolkit architecture

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

Properties: How the information is exchanged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `models.py <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/backend/models.py>`_
stores the backend properties that are shared between backend and frontend by simply loading the
`properties <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/backend/common_properties.json>`_
content in the class properties.
To understand how backend and frontend interact you can refer to `ui actions <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py>`_.
For example, when an event is triggered by the frontend, the `get_properties() <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py#L143>`_
method builds the GET HTTP request to send to the backend in order to retrieve properties from backend.
The event of setting up a property calls the `set_properties() <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/src/ansys/aedt/toolkits/common/ui/actions_generic.py#L165>`_
method which builds the PUT HTTP request that is sent to the backend.

API
~~~

The :doc:`../toolkit/api` contains three classes: ``Common``, ``AEDTCommon``, ``EDBCommon``, which provides methods for
controlling the toolkit workflow.

REST API
~~~~~~~~

REST APIs are the most common web interfaces that allow various clients to communicate with services via the REST API.
JSON is the standard for transferring data. In fact REST APIs accept JSON for request payload and also send responses
to JSON.
In the client-server architecture model, the client sends the request to the server to fetch some information.
Server-side technologies decode JSON information and transmit back the response to the client and this interaction is
handled by the HTTP protocol.

How frontend and backend interact?
----------------------------------
Frontend sends a HTTP request to retrieve data, while backend returns appropriate results.

The toolkit uses CRUD (Create, Read, Update & Delete) operations that simply are HTTP request methods that specify
the action to perform through the request.

UI
~~

For UI reference see :doc:`../toolkit/ui`