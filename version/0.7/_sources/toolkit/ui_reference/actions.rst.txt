.. _common_actions:

=======
Actions
=======

The ``FrontendGeneric`` class provides a generic UI for controlling the toolkit. A backend must be running previously.

.. currentmodule:: ansys.aedt.toolkits.common.ui.actions_generic

.. autoclass:: FrontendGeneric
   :members:
   :exclude-members: QMainWindow

You can modify the default properties with the following script:

.. code:: python

    # Import API
    from ansys.aedt.toolkits.common.ui.models import general_settings

    general_settings.high_resolution = False
