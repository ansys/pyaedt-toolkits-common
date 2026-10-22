=============
API reference
=============

This section provides descriptions of the two APIs available for the Motor
Segmentation Toolkit:

- **Toolkit API**: Contains the ``Toolkit`` class, which provides methods for
  controlling the toolkit workflow. In addition to methods for creating a new
  or connecting to an existing AEDT session, this API provides methods for automating
  the segmentation and skew of a 3D motor.
- **Generic API**: Contains the ``AEDTCommonToolkit`` class, which provides basic
  functions for controlling AEDT that are shared between the backend and frontend.
  These functions are the same for all AEDT toolkits.

.. toctree::
   :maxdepth: 2

   api
   common_api
