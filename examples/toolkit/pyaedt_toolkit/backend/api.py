import numpy as np
import os
import json
from ansys.aedt.toolkits.common.backend.properties import properties

# Load toolkit properties
with open(os.path.join(os.path.dirname(__file__), "properties.json")) as fh:
    _properties = json.load(fh)
for key, value in _properties.items():
    if hasattr(properties, key):
        setattr(properties, key, value)

from ansys.aedt.toolkits.common.backend.api import Backend
from ansys.aedt.toolkits.common.backend.api import thread
from ansys.aedt.toolkits.common.backend.logger_handler import logger


class ToolkitBackend(Backend):
    """Template API to control the toolkit workflow.

    This class provides methods to connect to a selected design and create geometries.

    Examples
    --------
    >>> import time
    >>> toolkit_api = ToolkitBackend()
    >>> msg1 = toolkit_api.launch_aedt()
    >>> response = toolkit_api.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = toolkit_api.get_thread_status()
    >>> msg3 = toolkit_api.create_geometry()
    >>> response = toolkit_api.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = toolkit_api.get_thread_status()
    """

    def __init__(self):
        """Initialize the ``Toolkit`` class."""
        Backend.__init__(self)
        self.multiplier = 1.0
        self.comps = []

    @thread.launch_thread
    def create_geometry(self):
        """Create a box or a sphere in design. If the toolkit is using Grpc, it is launched in a thread.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> toolkit_api = ToolkitBackend()
        >>> msg1 = toolkit_api.launch_aedt()
        >>> response = toolkit_api.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit_api.get_thread_status()
        >>> msg3 = toolkit_api.create_geometry()
        >>> response = toolkit_api.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit_api.get_thread_status()
        """
        self.connect_design()

        if self.aedtapp:
            multiplier = properties.multiplier
            geometry = properties.geometry
            self.multiplier = multiplier
            if geometry == "Box":
                self.draw_box()
            elif geometry == "Sphere":
                self.draw_sphere()
            self.aedtapp.release_desktop(False, False)
            self.aedtapp = None
            return True
        return False

    def draw_box(self):
        """Draw a box.

        Returns
        -------
        :class:`pyaedt.modeler.object3d.Object3d`
            3D object.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.api import Toolkit
        >>> import time
        >>> service = Toolkit()
        >>> msg1 = service.launch_aedt()
        >>> response = service.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_design()
        >>> service.draw_box()
        >>> service.release_aedt()
        """
        props = self._comp_props()
        pos_x = props[0][0]
        pos_y = props[0][1]
        pos_z = props[0][2]

        box = self.aedtapp.modeler.create_box(
            position=[pos_x, pos_y, pos_z],
            dimensions_list=[1 * self.multiplier, 1 * self.multiplier, 1 * self.multiplier],
        )

        box.color = (props[1][0], props[1][1], props[1][2])
        logger.debug("Box {} created".format(box.name))
        return box

    def draw_sphere(self):
        """Draw a sphere.

        Returns
        -------
        :class:`pyaedt.modeler.object3d.Object3d`
            3D object.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.api import Toolkit
        >>> import time
        >>> service = Toolkit()
        >>> msg1 = service.launch_aedt()
        >>> response = service.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_design()
        >>> service.draw_sphere()
        """

        props = self._comp_props()
        pos_x = props[0][0]
        pos_y = props[0][1]
        pos_z = props[0][2]

        sp = self.aedtapp.modeler.create_sphere(
            position=[pos_x, pos_y, pos_z],
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
