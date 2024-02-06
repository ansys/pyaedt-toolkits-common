PyAEDT Common Toolkit
=====================

|pyansys| |PythonVersion| |GH-CI| |MIT| |coverage| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |GH-CI| image:: https://github.com/ansys-internal/pyaedt-toolkits-common/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys-internal/pyaedt-toolkits-common/actions/workflows/ci_cd.yml

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |coverage| image:: https://codecov.io/gh/ansys/pyaedt-toolkits-common/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pyaedt-toolkits-common

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
  :target: https://github.com/psf/black
  :alt: black


The ``pyaedt-toolkits-common`` package provides common methods to create a new toolkit using PyAEDT.
This package has two main parts: backend and user interface.

The backend has some common methods to control Ansys Electronics Desktop (AEDT) session, and in addition,
it has a REST API based on `Flask <https://flask.palletsprojects.com/en/2.3.x/>`_.

The user interface has some common methods to create a desktop application based on `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_.

You can install both backend and user interface methods from PyPI:

.. code:: python

    pip install pyaedt-toolkits-common[all]

You can install only the backend methods from PyPI, this is useful if you only need the common API:

.. code:: python

    pip install pyaedt-toolkits-common


Requirements
~~~~~~~~~~~~
In addition to the runtime dependencies listed in the installation information, this toolkit
requires Ansys Electronics Desktop (AEDT) 2023 R2 or later. The AEDT Student Version is also supported.

Documentation and issues
~~~~~~~~~~~~~~~~~~~~~~~~
The documentation provides the `API reference <https://aedt.toolkit.common.docs.pyansys.com/version/dev/Toolkit/index.html>`_ to create a new toolkit,
you can also find a `Toolkit example <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/examples/toolkit/pyaedt_toolkit>`_.

On the `Common Toolkit Issues <https://github.com/ansys-internal/pyaedt-toolkits-common/issues>`_ page, you can
create issues to submit questions, report bugs, and request new features.

License
~~~~~~~
This toolkit is licensed under the MIT license.

This module makes no commercial claim over Ansys whatsoever.
The use of the interactive control of this toolkit requires a legally licensed
local copy of AEDT. For more information about AEDT,
visit the `AEDT page <https://www.ansys.com/products/electronics>`_
on the Ansys website.
