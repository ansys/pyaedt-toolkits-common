.. _user_interface:

================
UI API reference
================

The PyADT Common Toolkit is designed to streamline the process of creating standard AEDT applications
using `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_.
The UI API provides a set of pre-built components, utilities, and an API that simplifies
the development of robust and user-friendly applications.

The UI API contains three main modules: ``Utils``, ``Windows``, and ``Generic actions``:

.. grid:: 2

    .. grid-item-card:: Utils :fa:`person-running`
        :padding: 2 2 2 2
        :link: ui_reference/utils
        :link-type: doc

        Common user interface classes to define widgets and load templates.

    .. grid-item-card:: Windows :fa:`book-bookmark`
        :padding: 2 2 2 2
        :link: ui_reference/windows
        :link-type: doc

        Default Windows initialization.

    .. grid-item-card:: Generic actions :fa:`scroll`
        :padding: 2 2 2 2
        :link: ui_reference/actions
        :link-type: doc

        Generic methods to call the REST API.


.. toctree::
   :hidden:

   ui_reference/utils
   ui_reference/windows
   ui_reference/actions


This image shows the structure of the UI:

.. image:: ../_static/user_interface.png
  :width: 800
  :alt: UI structure

The UI is contained inside the main window. The main window contains some common widgets,
such as the credits and title, that are initialized by default. You use the content widget
to add new pages.

For initialization information, see the `UI example <https://github.com/ansys-internal/pyaedt-toolkits-common/tree/main/examples/ui/default_ui_example>`_.
