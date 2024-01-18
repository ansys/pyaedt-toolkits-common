from dataclasses import FrozenInstanceError
from dataclasses import dataclass

# from dataclasses import dataclass
from enum import Enum
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import psutil
import pyaedt
from pyaedt import Desktop
from pyaedt.misc import list_installed_ansysem
from pydantic import ValidationError

from ansys.aedt.toolkits.common.backend.constants import NAME_TO_AEDT_APP
from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.common.backend.models import properties
from ansys.aedt.toolkits.common.backend.thread_manager import ThreadManager

thread = ThreadManager()


class ToolkitThreadStatus(str, Enum):
    """Status of the toolkit thread."""

    IDLE = "Toolkit is idle and ready to accept a new task."
    BUSY = "Toolkit is busy and processing a task."
    CRASHED = "Toolkit has crashed and is not functional."
    UNKNOWN = "Toolkit unknown status."


class PropertiesUpdate(str, Enum):
    """Status of the toolkit thread."""

    EMPTY = "Body is empty."
    SUCCESS = "Properties updated successfully."
    FROZEN = "Properties are frozen, updated failed."
    VALIDATION_ERROR = "Error during validation of properties field."


@dataclass
class ToolkitConnectionStatus:
    """Status of the toolkit connection."""

    desktop: Optional[Desktop] = None

    def __str__(self):
        if self.desktop:
            res = f"Toolkit is connected to process {self.desktop.aedt_process_id}"
            if self.desktop.port != 0:
                res += f" on Grpc {self.desktop.port}."
        else:
            res = "Toolkit is not connected to AEDT."
        return res

    def is_connected(self):
        return self.desktop is not None


class Common:
    """Common API to control the toolkits.

    It provides basic functions to control AEDT, EDB and properties to share between backend and frontend.

    Examples
    --------
    >>> from ansys.aedt.toolkits.common.backend.api import Common
    >>> toolkit_api = Common()
    >>> toolkit_properties = toolkit_api.get_properties()
    >>> new_properties = {"aedt_version": "2023.1"}
    >>> toolkit_api.set_properties(new_properties)
    >>> new_properties = toolkit_api.get_properties()
    """

    def __init__(self):
        self.logger = logger

    @staticmethod
    def get_properties() -> Dict[str, str]:
        """Get toolkit properties.

        Returns
        -------
        dict
            Dictionary containing the toolkit properties.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api import Common
        >>> toolkit_api = Common()
        >>> toolkit_api.get_properties()
        {"property1": value1, "property2": value2}
        """
        res = properties.model_dump()
        return res

    @staticmethod
    def set_properties(data: Dict[str, Any]):
        """Assign the passed data to the internal data model.

        Parameters
        ----------
        data : dict
            Dictionary containing the properties to update.

        Returns
        -------
        tuple[bool, str]
            Tuple indicating the success status and a message.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api import Common
        >>> toolkit_api = Common()
        >>> value2 = 2
        >>> toolkit_api.set_properties({"property1": "value1", "property2": value2})
        """
        logger.info("Updating internal properties.")
        key = ""
        value = ""
        if data:
            try:
                for key, value in data.items():
                    logger.debug(f"Updating '{key}' with value {value}")
                    setattr(properties, key, value)
                msg = PropertiesUpdate.SUCCESS.value
                updated = True
                logger.debug(msg)
            except FrozenInstanceError:
                msg = PropertiesUpdate.FROZEN.value
                updated = False
                logger.error(msg)
            except ValidationError:
                msg = PropertiesUpdate.VALIDATION_ERROR.value
                updated = False
                logger.error(msg)
                logger.error(f"key {key} with value {value}")
        else:
            msg = PropertiesUpdate.EMPTY.value
            updated = False
            logger.debug(msg)
        return updated, msg

    @staticmethod
    def get_thread_status() -> ToolkitThreadStatus:
        """Get the toolkit thread status.

        Returns
        -------
        bool
            ``True`` when active, ``False`` when inactive.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api import Common
        >>> toolkit_api = Common()
        >>> toolkit_api.get_thread_status()
        """
        thread_running = thread.is_toolkit_thread_running()
        is_toolkit_busy = properties.is_toolkit_busy
        if thread_running and is_toolkit_busy:  # pragma: no cover
            res = ToolkitThreadStatus.BUSY
            logger.debug(res.value)
        elif (not thread_running and is_toolkit_busy) or (thread_running and not is_toolkit_busy):  # pragma: no cover
            res = ToolkitThreadStatus.CRASHED
            logger.error(res.value)
        else:
            res = ToolkitThreadStatus.IDLE
            logger.debug(res.value)
        return res

    @staticmethod
    def installed_aedt_version():
        """
        Get the installed AEDT versions.

        Returns
        -------
        list
            List of installed AEDT versions.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api import Common
        >>> toolkit_api = Common()
        >>> toolkit_api.installed_aedt_version()
        ["2022.2", "2023.2", "2024.1"]
        """

        # Detect existing AEDT installation
        installed_versions = []
        for ver in list_installed_ansysem():
            installed_versions.append(
                "20{}.{}".format(ver.replace("ANSYSEM_ROOT", "")[:2], ver.replace("ANSYSEM_ROOT", "")[-1])
            )
        logger.debug(str(installed_versions))
        return installed_versions

    @staticmethod
    def aedt_sessions():
        """Get information for the active AEDT sessions.

        Returns
        -------
        list
            List of AEDT process IDs (PIDs).

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api import Common
        >>> toolkit_api = Common()
        >>> toolkit_api.aedt_sessions()
        [[pid1, grpc_port1], [pid2, grpc_port2]]
        """
        res = []
        if not properties.is_toolkit_busy and properties.aedt_version:
            keys = ["ansysedt.exe"]
            version = properties.aedt_version
            if version and "." in version:
                version = version[-4:].replace(".", "")
            if version < "222":  # pragma: no cover
                version = version[:2] + "." + version[2]
            for process in filter(lambda p: p.name() in keys, psutil.process_iter()):
                cmd = process.cmdline()
                if version in cmd[0]:
                    try:
                        grpc_index = cmd.index("-grpcsrv") + 1
                        port = int(cmd[grpc_index])
                    except (ValueError, IndexError):
                        port = -1
                    res.append([process.pid, port])
            logger.debug(f"Active AEDT sessions: {res}.")
        else:
            logger.debug("No active sessions.")
        return res


class AEDTCommon(Common):
    """Provides common functions to control AEDT.

    It provides basic functions to control AEDT and properties to share between backend and frontend.

    Examples
    --------
    >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
    >>> toolkit_api = AEDTCommon()
    >>> msg = toolkit_api.launch_aedt()
    """

    def __init__(self):
        Common.__init__(self)
        self.desktop = None
        self.aedtapp = None

    def is_aedt_connected(self) -> Tuple[bool, str]:
        """Check if AEDT is connected.

        Returns
        -------
        tuple[bool, str]
            Tuple indicating the connection status and a message.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> msg = toolkit_api.launch_aedt()
        >>> response = toolkit_api.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit_api.get_thread_status()
        >>> toolkit_api.connect_aedt()
        >>> toolkit_api.is_aedt_connected()
        (True, "Toolkit connected to process <process_id> on Grpc <grpc_port>")
        >>> toolkit_api.release_aedt()
        """
        tcs = ToolkitConnectionStatus(desktop=self.desktop)
        connected = tcs.is_connected()
        msg = str(tcs)
        logger.debug(msg)
        return connected, msg

    @thread.launch_thread
    def launch_aedt(self):
        """Launch AEDT.

        This method is launched in a thread if grpc is enabled. AEDT is released once it is opened.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> toolkit_api.launch_aedt()
        """
        # Check if the backend is already connected to an AEDT session
        connected, msg = self.is_aedt_connected()
        if not connected:
            logger.debug("Launching AEDT.")
            pyaedt.settings.use_grpc_api = properties.use_grpc
            desktop_args = {
                "specified_version": properties.aedt_version,
                "non_graphical": properties.non_graphical,
            }

            # AEDT with COM
            if properties.selected_process == 0:  # pragma: no cover
                desktop_args["new_desktop_session"] = True
            # AEDT with gRPC
            elif properties.use_grpc:
                desktop_args["new_desktop_session"] = False
                desktop_args["port"] = properties.selected_process
            else:  # pragma: no cover
                desktop_args["new_desktop_session"] = False
                desktop_args["aedt_process_id"] = properties.selected_process
            self.desktop = pyaedt.Desktop(**desktop_args)

            if not self.desktop:
                logger.error("AEDT not launched.")
                return False
            logger.debug("AEDT launched.")
            # Save AEDT session properties
            if properties.use_grpc:
                properties.selected_process = self.desktop.port
                logger.debug("Grpc port {}.".format(str(self.desktop.port)))
            else:
                properties.selected_process = self.desktop.aedt_process_id
                logger.debug("Process ID {}.".format(str(self.desktop.aedt_process_id)))

            self._save_project_info()

            if self.desktop.project_list():
                # If there are projects not saved in the session, PyAEDT could find issues loading some properties
                self.desktop.save_project()

            self.release_aedt(False, False)

            logger.debug("Desktop released and project properties loaded.")

        return True

    def connect_aedt(self) -> bool:
        """Connect to an existing AEDT session.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> toolkit_api.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit_api.get_thread_status()
        >>> toolkit_api.connect_aedt()
        >>> toolkit_api.release_aedt()
        """
        if properties.selected_process == 0:
            logger.error("Process ID not defined.")
            return False

        is_aedt_connected = self.is_aedt_connected()
        if is_aedt_connected[0]:
            logger.debug("Toolkit is connected to AEDT.")
            return True

        # Connect to AEDT
        pyaedt.settings.use_grpc_api = properties.use_grpc
        logger.debug("Connecting AEDT.")

        desktop_args = {
            "specified_version": properties.aedt_version,
            "non_graphical": properties.non_graphical,
            "new_desktop_session": False,
        }
        if properties.use_grpc:
            desktop_args["port"] = properties.selected_process
        else:  # pragma: no cover
            desktop_args["aedt_process_id"] = properties.selected_process
        self.desktop = pyaedt.Desktop(**desktop_args)

        if not self.desktop:  # pragma: no cover
            logger.error("Toolkit is not connected to AEDT.")
            return False

        logger.debug("Toolkit is connected to AEDT.")
        return True

    def connect_design(self, app_name: Optional[str] = None):
        """Connect to an application design.

        If a design exists, this method uses the active project and design. If a design does not exist,
        this method creates a design of the specified type. If no application is specified, the default is ``"Hfss"``.

        Parameters
        ----------
        app_name : str
            AEDT application name. Options are:

            * ``"Circuit"``
            * ``"EMIT"``
            * ``"HFSS"``
            * ``"HFSS3DLayout"``
            * ``"Icepak"``
            * ``"Maxwell2D"``
            * ``"Maxwell3D"``
            * ``"Q2D"``
            * ``"Q3D"``
            * ``"Rmxprt"``
            * ``"Twin Builder"``
            * ``"Mechanical"``

        Returns
        -------
        bool
            Returns ``True`` if the connection to a design is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> toolkit_api.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit_api.get_thread_status()
        >>> toolkit_api.connect_design()

        """
        if not self.connect_aedt():
            return False

        project_name = properties.active_project
        design_name = "No design"

        if properties.active_design:
            design_name = properties.active_design

        pyaedt.settings.use_grpc_api = properties.use_grpc

        if not app_name:
            app_name = "HFSS"

        # Select app
        aedt_app = pyaedt.Hfss
        if design_name != "No design":
            project_name = self.get_project_name(project_name)
            self.aedtapp = self.desktop[[project_name, design_name]]
            active_design = self.aedtapp.design_name
        elif app_name in list(NAME_TO_AEDT_APP.keys()):
            design_name = pyaedt.generate_unique_name(app_name)
            aedt_app = getattr(pyaedt, NAME_TO_AEDT_APP[app_name])
            active_design = design_name
        else:
            logger.info("AEDT application not available in PyAEDT. Creating HFSS design.")
            design_name = pyaedt.generate_unique_name("Hfss")
            active_design = design_name

        if not self.aedtapp and aedt_app:
            aedt_app_args = {
                "specified_version": properties.aedt_version,
                "port": properties.selected_process,
                "non_graphical": properties.non_graphical,
                "new_desktop_session": False,
                "projectname": project_name,
                "designname": active_design,
            }
            if properties.use_grpc:
                aedt_app_args["port"] = properties.selected_process
            else:
                aedt_app_args["aedt_process_id"] = properties.selected_process

            self.aedtapp = aedt_app(**aedt_app_args)
            self.aedtapp.save_project()
            self._save_project_info()

        if self.aedtapp:
            project_name = self.aedtapp.project_file
            if self.aedtapp.project_file not in properties.project_list:
                properties.project_list.append(project_name)
                properties.design_list[self.aedtapp.project_name] = [active_design]

            if self.aedtapp.design_list and active_design not in properties.design_list[self.aedtapp.project_name]:
                properties.design_list[self.aedtapp.project_name].append(active_design)
            properties.active_project = project_name
            properties.active_design = active_design
            logger.info("Toolkit is connected to AEDT design.")
            return True
        else:
            logger.error("Toolkit not connected to AEDT design.")
            return False

    def release_aedt(self, close_projects=False, close_on_exit=False):
        """Release AEDT.

        Parameters
        ----------
        close_projects : bool, optional
            Whether to close the AEDT projects that are open in the session.
            The default is ``True``.
        close_on_exit : bool, optional
            Whether to close the active AEDT session on exiting AEDT.
            The default is ``True``.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> toolkit_api.launch_aedt()
        >>> toolkit_api.release_aedt(True, True)

        """
        released = False
        if self.desktop:
            try:
                released = self.desktop.release_desktop(close_projects, close_on_exit)
                self.desktop = None
                self.aedtapp = None
            except:
                logger.error("Desktop not released.")
                return False

        if self.aedtapp:
            try:
                released = self.aedtapp.release_desktop(close_projects, close_on_exit)
                self.aedtapp = None
            except:
                logger.error("Desktop not released")
                return False

        if not released and close_projects and close_on_exit:
            if self.connect_aedt():
                self.desktop.release_desktop(close_projects, close_on_exit)
        logger.info("Desktop released.")
        return True

    def open_project(self, project_name=None):
        """Open AEDT project.

        Parameters
        ----------
        project_name : str, optional
            Project path to open.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> toolkit_api.launch_aedt()
        >>> toolkit_api.open_project("path/to/file")
        >>> toolkit_api.release_aedt()

        """
        if not self.connect_aedt():
            return False
        if not os.path.exists(project_name + ".lock") and self.desktop and project_name:
            self.desktop.odesktop.OpenProject(project_name)
            logger.debug("Project {} opened".format(project_name))
            self._save_project_info()
            self.release_aedt(False, False)
            return True

        self.release_aedt(False, False)
        return False

    @thread.launch_thread
    def save_project(self, project_path=None):
        """Save project. It uses the properties to get the project path. This method is launched in a thread.

        Parameters
        ----------
        project_path : str, optional
            Path of the AEDT file to save.
            The default value is ``None`` in which case the current file is overwritten.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> toolkit_api.launch_aedt()
        >>> toolkit_api.connect_aedt()
        >>> toolkit_api.save_project()
        """
        if self.connect_design():
            if project_path and properties.active_project != project_path:
                old_project_name = self.get_project_name(properties.active_project)
                self.aedtapp.save_project(project_file=os.path.abspath(project_path))
                index = properties.project_list.index(properties.active_project)
                properties.project_list.pop(index)
                properties.active_project = project_path
                properties.project_list.append(project_path)
                new_project_name = self.get_project_name(properties.active_project)
                properties.design_list[new_project_name] = properties.design_list[old_project_name]
                if old_project_name != new_project_name:
                    del properties.design_list[old_project_name]
            else:
                self.aedtapp.save_project()
            self.release_aedt(False, False)
            logger.debug("Project saved: {}".format(project_path))
            return True
        else:  # pragma: no cover
            logger.error("Project not saved")
            return False

    @staticmethod
    def get_project_name(project_path) -> str:
        """Get project name from project path.

        Returns
        -------
        str
            Project name
        """
        return os.path.splitext(os.path.basename(project_path))[0]

    @staticmethod
    def get_design_names() -> List[str]:
        """Get design names for a specific project.

        The first design name returned is the active design.

        Returns
        -------
        list
            List of design names.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import AEDTCommon
        >>> toolkit_api = AEDTCommon()
        >>> toolkit_api.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit_api.get_thread_status()
        >>> toolkit_api.get_design_names()
        """
        design_list: List[str] = []
        if properties.selected_process == 0:
            logger.error("Process ID not defined")
            return design_list

        active_project = os.path.splitext(os.path.basename(properties.active_project))[0]
        if active_project and active_project != "No project":
            for design in properties.designs_by_project_name[active_project]:
                design_list.append(design)

            if properties.active_design in design_list:
                index = design_list.index(properties.active_design)
                design_list.insert(0, design_list.pop(index))
            else:
                design_list.append(properties.active_design)

        return design_list

    def _save_project_info(self):
        # Save project and design info
        new_properties = {}
        project_list = self.desktop.odesktop.GetProjectList()

        if project_list:
            new_properties["project_list"] = []
            active_project = self.desktop.odesktop.GetActiveProject()
            if not active_project:
                active_project = self.desktop.odesktop.SetActiveProject(project_list[0])
            active_project_name = active_project.GetName()
            active_design = active_project.GetActiveDesign()

            # Save active design info
            if active_design:
                active_design_name = active_design.GetName()
                active_design_name = (
                    active_design_name if ";" not in active_design_name else active_design_name.split(";")[1]
                )
                new_properties["active_design"] = active_design_name

            elif active_project.GetChildNames():
                # This case covers when the project has designs but none of them are active
                active_design_name = active_project.GetChildNames()[0]
                active_project.SetActiveDesign(active_design_name)
                new_properties["active_design"] = active_design_name

            # Save active project
            active_project_path = active_project.GetPath()
            new_properties["active_project"] = os.path.join(active_project_path, active_project_name + ".aedt")

            # Save projects info
            new_properties["design_list"] = {}
            for project in project_list:
                oproject = self.desktop.odesktop.SetActiveProject(project)
                project_name = oproject.GetName()
                project_path = oproject.GetPath()
                logger.debug("Project name: {}".format(project_name))
                new_properties["project_list"].append(os.path.join(project_path, project_name + ".aedt"))

                new_properties["design_list"][project_name] = []

                design_list = oproject.GetChildNames()

                if design_list:
                    for design_name in design_list:
                        new_properties["design_list"][project_name].append(design_name)

        if new_properties:
            self.set_properties(new_properties)


class EDBCommon(Common):
    """Generic API to control EDB.

    It provides basic functions to control AEDT and properties to share between backend and frontend.

    Examples
    --------
    >>> from ansys.aedt.toolkits.common.backend.api import EDBCommon
    >>> toolkit_api = EDBCommon()
    >>> toolkit_api.load_edb("path/to/file")
    """

    def __init__(self):
        Common.__init__(self)
        self.edb = None

    def load_edb(self, edb_path=None):
        """Load EDB project.

        Parameters
        ----------
        edb_path : str, optional
            Full path to the ``aedb`` folder.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import EDBCommon
        >>> toolkit_api = EDBCommon()
        >>> toolkit_api.load_edb("path/to/file")
        >>> toolkit_api.close_edb()
        """
        if self.edb:
            logger.error("Close EDB")
            return False
        if not edb_path:
            edb_path = properties.active_project
        if os.path.exists(edb_path):
            aedt_version = properties.aedt_version
            properties.active_project = edb_path
            self.edb = pyaedt.Edb(edbversion=aedt_version, edbpath=edb_path)
            logger.debug("Project {} opened".format(edb_path))
            return True
        logger.error("Project {} does not exist".format(edb_path))
        return False

    def close_edb(self):
        """Close EDB project.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import EDBCommon
        >>> toolkit_api = EDBCommon()
        >>> toolkit_api.load_edb("path/to/file")
        >>> toolkit_api.close_edb()
        """
        if self.edb:
            self.edb.close_edb()
            self.edb = None
            logger.error("Edb closed")
            return True
        logger.error("Edb not initialized")
        return False

    def save_edb(self, edb_path=None):
        """Save EDB project.

        Parameters
        ----------
        edb_path : str, optional
            Full path to the ``aedb`` folder.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api import EDBCommon
        >>> toolkit_api = EDBCommon()
        >>> toolkit_api.load_edb("path/to/file")
        >>> toolkit_api.save_edb("path/to/new_file")
        >>> toolkit_api.close_edb()
        """
        if self.edb:
            if not edb_path or os.path.normpath(edb_path) == os.path.normpath(self.edb.edbpath):
                self.edb.save()
                edb_path = self.edb.edbpath
            else:
                self.edb.save_as(edb_path)
            logger.info("Project {} saved".format(edb_path))
            return True
        return False
