PyAEDT Common Toolkit
=====================

|pyansys| |PythonVersion| |GH-CI| |MIT| |coverage| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |GH-CI| image:: https://github.com/ansys/pyaedt-toolkits-common/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pyaedt-toolkits-common/actions/workflows/ci_cd.yml

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |coverage| image:: https://codecov.io/gh/ansys/pyaedt-toolkits-common/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pyaedt-toolkits-common

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
  :target: https://github.com/psf/black
  :alt: black

The PyAEDT Common Toolkit provides common methods for creating an Ansys Electronics Desktop (AEDT) toolkit.

A common toolkit library can bring numerous advantages in the creation and development of toolkits,
including enhancing efficiency, consistency, and collaboration.

The PyAEDT Common Toolkit has two main parts: a backend and a User Interface (UI).

- The backend has some common methods for controlling an AEDT session and also a
  REST API based on `Flask <https://flask.palletsprojects.com/en/2.3.x/>`_.

- The UI consists of some common methods for creating a desktop app based on
  `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_.

Requirements
~~~~~~~~~~~~
In addition to the runtime dependencies listed in
`Installation <https://aedt.common.toolkit.docs.pyansys.com/version/dev/getting_started/installation.html>`_,
the PyAEDT Common Toolkit requires AEDT 2023 R2 or later. This toolkit also supports the AEDT Student
Version for 2023 R2 or later.

Documentation and issues
~~~~~~~~~~~~~~~~~~~~~~~~
Documentation for the latest stable release is hosted at
`PyAEDT Common Toolkit documentation <https://aedt.common.toolkit.docs.pyansys.com/version/stable/index.html>`_.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the
development version or previously released versions.

On the `PyAEDT Common Toolkit Issues <https://github.com/ansys/pyaedt-toolkits-common/issues>`_ page, you can
create issues to report bugs and request new features. On the `Discussions <https://discuss.ansys.com/>`_
page on the Ansys Developer portal, you can post questions, share ideas, and get community feedback.

License
~~~~~~~
The PyAEDT Common Toolkit is licensed under the MIT license.

This toolkit makes no commercial claim over Ansys whatsoever.
The use of this toolkit requires a legally licensed copy of AEDT.
For more information, see the `Ansys Electronics <https://www.ansys.com/products/electronics>`_
page on the Ansys website.
