============
UI reference
============

This library contains a versatile library designed to streamline the process of creating standard desktop applications
using the `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_.
The user interface (UI) API provides a set of pre-built components, utilities, and an API that simplifies
the development of robust and user-friendly applications.

The user interface (UI) API contains three main modules: ``Utils``, ``Windows``, ``actions_generic``:

- **windows**: provides the initialization of the defaults windows.

- **actions_generic**: provides methods to call the default REST API.

.. grid:: 2

    .. grid-item-card:: Utils :fa:`person-running`
        :padding: 2 2 2 2
        :link: ui_reference/utils
        :link-type: doc

        Methods to common desktop widgets, theme definition or user interface templates.

    .. grid-item-card:: Windows :fa:`book-bookmark`
        :padding: 2 2 2 2
        :link: ui_reference/windows
        :link-type: doc

        Defaults windows initialization.

    .. grid-item-card:: UI API reference :fa:`scroll`
        :padding: 2 2 2 2
        :link: ui_reference/actions
        :link-type: doc

        Generic methods to call the REST API.


.. toctree::
   :hidden:

   ui_reference/utils
   ui_reference/windows
   ui_reference/actions


The provided user interface has the following structure:

.. image:: ../_static/user_interface.png
  :width: 800
  :alt: User interface

Find here a `Default UI example <https://github.com/ansys-internal/pyaedt-toolkits-common/blob/main/examples/ui/default_ui/default_ui.py>`_.
