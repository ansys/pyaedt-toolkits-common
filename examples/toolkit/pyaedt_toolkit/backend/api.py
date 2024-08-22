import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent))

from models import properties
import numpy as np

from ansys.aedt.toolkits.common.backend.api import AEDTCommon
from ansys.aedt.toolkits.common.backend.logger_handler import logger


class ToolkitBackend(AEDTCommon):
    """Template API to control the toolkit workflow.

    This class provides methods to connect to a selected design and create geometries.

    Examples
    --------
    >>> from examples.toolkit.pyaedt_toolkit.backend.api import ToolkitBackend
    >>> toolkit_api = ToolkitBackend()
    >>> toolkit_api.launch_aedt()
    >>> toolkit_api.wait_to_be_idle()
    >>> toolkit_api.create_geometry()
    """

    def __init__(self):
        """Initialize the ``toolkit`` class."""
        AEDTCommon.__init__(self, properties)
        self.properties = properties
        self.multiplier = 1.0

    def create_geometry(self):
        """Create a box or a sphere in design.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> from examples.toolkit.pyaedt_toolkit.backend.api import ToolkitBackend
        >>> toolkit_api = ToolkitBackend()
        >>> toolkit_api.launch_aedt()
        >>> toolkit_api.wait_to_be_idle()
        >>> toolkit_api.create_geometry()
        """
        self.connect_design()

        if self.aedtapp:
            multiplier = self.properties.example.multiplier
            geometry = self.properties.example.geometry
            self.multiplier = multiplier
            prim = None
            if geometry == "Box":
                prim = self.draw_box()
            elif geometry == "Sphere":
                prim = self.draw_sphere()
            if not prim:
                logger.error("Primitive not created")
                return False
            self.release_aedt(False, False)
            return prim.name
        logger.error("Design not connected")
        return False

    def draw_box(self):
        """Draw a box.

        Returns
        -------
        :class:`ansys.aedt.core.modeler.object3d.Object3d`
            3D object.

        Examples
        --------
        >>> from examples.toolkit.pyaedt_toolkit.backend.api import ToolkitBackend
        >>> toolkit_api = ToolkitBackend()
        >>> toolkit_api.launch_aedt()
        >>> toolkit_api.wait_to_be_idle()
        >>> toolkit_api.connect_design()
        >>> toolkit_api.draw_box()
        >>> toolkit_api.release_aedt()
        """
        props = self._comp_props()
        pos_x = props[0][0]
        pos_y = props[0][1]
        pos_z = props[0][2]

        box = self.aedtapp.modeler.create_box(
            origin=[pos_x, pos_y, pos_z],
            sizes=[1 * self.multiplier, 1 * self.multiplier, 1 * self.multiplier],
        )

        box.color = (props[1][0], props[1][1], props[1][2])
        logger.debug("Box {} created".format(box.name))
        return box

    def draw_sphere(self):
        """Draw a sphere.

        Returns
        -------
        :class:`ansys.aedt.core.modeler.object3d.Object3d`
            3D object.

        Examples
        --------
        >>> from examples.toolkit.pyaedt_toolkit.backend.api import ToolkitBackend
        >>> toolkit_api = ToolkitBackend()
        >>> toolkit_api.launch_aedt()
        >>> toolkit_api.wait_to_be_idle()
        >>> toolkit_api.connect_design()
        >>> toolkit_api.draw_sphere()
        >>> toolkit_api.release_aedt()
        """

        props = self._comp_props()
        pos_x = props[0][0]
        pos_y = props[0][1]
        pos_z = props[0][2]

        sp = self.aedtapp.modeler.create_sphere(
            origin=[pos_x, pos_y, pos_z],
            radius=1 * self.multiplier,
        )

        sp.color = (props[1][0], props[1][1], props[1][2])
        logger.debug("Sphere {} created".format(sp.name))
        return sp

    @staticmethod
    def _comp_props():
        """Return a random position and color.

        Returns
        -------
        tuple[list, list]

        """
        pos = [np.random.random() * 20, np.random.random() * 20, np.random.random() * 20]
        r = str(np.random.randint(0, 255))
        g = str(np.random.randint(0, 255))
        b = str(np.random.randint(0, 255))

        return pos, [r, g, b]
