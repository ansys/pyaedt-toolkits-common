.. _ref_getting_started:

===============
Getting Started
===============

If you want to develop a new toolkit, you will need first to understand the architecture.

This repository is a common API for any new AEDT toolkit. It standardizes AEDT toolkits implementation.

The API provides some methods to connect to an existing AEDT session, open an existing
AEDT project or initialize a new AEDT session, which should be the basic capability of any toolkit.

The architecture is split in two main parts:

1. The backend, using `Flask <https://flask.palletsprojects.com/en/2.3.x/>`_. Flask creates a REST API,
which let interact different services by simply doing HTTP requests.

2. The frontend, using `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_. Pyside6 has a designer tool
which allows to create user interfaces and it is translated to python directly.

Using Flask, the toolkit becomes interface agnostic, then you can decide change it and use a WebUI for instance
as user interface.

You can install the library like any other open source package. You can add this project as a dependency of the new toolkit.

If you need more information, go to :ref:`ref_toolkit_architecture`.


.. toctree::
   :hidden:
   :maxdepth: 2

   Architecture
   Installation
