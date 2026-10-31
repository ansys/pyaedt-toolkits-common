=====
Utils
=====

This section describes the classes for common widgets, objects, and layout templates, which
are all designed for versatile application use. While a description of each class follows,
you can click the class name to view detailed API reference information.

**``CommonWindowUtils``**

   .. currentmodule:: ansys.aedt.toolkits.common.ui.utils.windows.common_window_utils
   .. autosummary::
      :toctree: _autosummary

      CommonWindowUtils

**``LoadImages``**

   .. currentmodule:: ansys.aedt.toolkits.common.ui.utils.images.load_images
   .. autosummary::
      :toctree: _autosummary

      LoadImages

**``ThemeHandler``**

   .. currentmodule:: ansys.aedt.toolkits.common.ui.utils.themes.json_themes
   .. autosummary::
      :toctree: _autosummary

      ThemeHandler

You use the ``CommonWindowUtils`` class to create custom widgets in the UI. The PyAEDT
Common Toolkit also provides the additional widgets described in :ref:`widgets`.

In addition to wrapped PySide6 widgets, the PyAEDT Common Toolkit provides these UI
templates to enhance the overall layout:

- ``left_column.ui``
- ``right_column.ui``
- ``main_pages.ui``

These templates serve as a foundation for creating default layouts. You can explore these templates in the
`ui templates <https://github.com/ansys/pyaedt-toolkits-common/tree/main/src/ansys/aedt/toolkits/common/ui/utils/ui_templates>`_
directory of the repository.

.. toctree::
   :hidden:

   widgets/index
