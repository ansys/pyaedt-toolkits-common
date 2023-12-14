import os

import psutil
import pyaedt

from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.common.backend.properties import properties
from ansys.aedt.toolkits.common.backend.thread_manager import ThreadManager

thread = ThreadManager()


class ToolkitGeneric(object):
    """Generic API to control the toolkits.

    It provides basic functions to control AEDT and properties to share between backend and frontend.

    Examples
    --------
    >>> import time
    >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
    >>> toolkit = ToolkitGeneric()
    >>> properties = toolkit.get_properties()
    >>> new_properties = {"aedt_version": "2023.2"}
    >>> toolkit.set_properties(new_properties)
    >>> new_properties = toolkit.get_properties()
    >>> msg = toolkit.launch_aedt()
    >>> response = toolkit.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = toolkit.get_thread_status()
    """

    def __init__(self):
        self.properties = properties
        self.aedt_common = AedtGeneric()

    @staticmethod
    def set_properties(data):
        """Assign the passed data to the internal data model.

        Parameters
        ----------
        data : dict
            The dictionary containing the properties to be updated.

        Returns
        -------
        tuple[bool, str]
            A tuple indicating the success status and a message.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.set_properties({"property1": value1, "property2": value2})

        """

        logger.debug("Updating the internal properties")
        if data:
            try:
                for key in data:
                    setattr(properties, key, data[key])
                msg = "properties updated successfully"
                logger.debug(msg)
                return True, msg
            except:
                return False, "Frozen property access"
        else:
            msg = "body is empty!"
            logger.debug(msg)
            return False, msg

    @staticmethod
    def get_properties():
        """Get toolkit properties.

        Returns
        -------
        dict
            The dictionary containing the toolkit properties.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.get_properties()
        {"property1": value1, "property2": value2}
        """
        return properties.export_to_dict()

    @staticmethod
    def get_thread_status():
        """Get toolkit thread status.

        Returns
        -------
        bool
            ``True`` when active, ``False`` when not active.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.get_thread_status()
        """
        thread_running = thread.is_thread_running()
        is_toolkit_busy = properties.is_toolkit_busy
        if thread_running and is_toolkit_busy:  # pragma: no cover
            msg = "Backend running"
            # logger.debug(msg)
            return 0, msg
        elif (not thread_running and is_toolkit_busy) or (thread_running and not is_toolkit_busy):  # pragma: no cover
            msg = "Backend crashed"
            logger.error(msg)
            return 1, msg
        else:
            msg = "Backend free"
            logger.debug(msg)
            return -1, msg

    @staticmethod
    def installed_aedt_version():
        """
        Return the installed AEDT versions.

        Returns
        -------
        list
            List of installed AEDT versions.

        Examples
        --------
        >>> >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.installed_aedt_version()
        ["2021.1", "2021.2", "2022.1"]
        """

        # Detect existing AEDT installation
        installed_versions = []
        for ver in pyaedt.misc.list_installed_ansysem():
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
            List of AEDT PIDs.

        Examples
        --------
        >>> >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.aedt_sessions()
        [[pid1, grpc_port1], [pid2, grpc_port2]]
        """
        if not properties.is_toolkit_busy:
            version = properties.aedt_version
            keys = ["ansysedt.exe"]
            if not version:
                return []
            if version and "." in version:
                version = version[-4:].replace(".", "")
            if version < "222":  # pragma: no cover
                version = version[:2] + "." + version[2]
            sessions = []
            for p in psutil.process_iter():
                try:
                    if p.name() in keys:
                        cmd = p.cmdline()
                        if not version or (version and version in cmd[0]):
                            if "-grpcsrv" in cmd:
                                if not version or (version and version in cmd[0]):
                                    try:
                                        sessions.append(
                                            [
                                                p.pid,
                                                int(cmd[cmd.index("-grpcsrv") + 1]),
                                            ]
                                        )
                                    except IndexError:
                                        sessions.append(
                                            [
                                                p.pid,
                                                -1,
                                            ]
                                        )
                            else:
                                sessions.append(
                                    [
                                        p.pid,
                                        -1,
                                    ]
                                )
                except:
                    pass
            logger.debug(str(sessions))
            return sessions
        else:
            logger.debug("No active sessions")
            return []


class AedtGeneric(object):
    """Generic API to control AEDT.

    It provides basic functions to control AEDT and properties to share between backend and frontend.

    Examples
    --------
    >>> import time
    >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
    >>> toolkit = ToolkitGeneric()
    >>> properties = toolkit.get_properties()
    >>> new_properties = {"aedt_version": "2023.2"}
    >>> toolkit.set_properties(new_properties)
    >>> new_properties = toolkit.get_properties()
    >>> msg = toolkit.launch_aedt()
    >>> response = toolkit.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = toolkit.get_thread_status()
    """
    def __init__(self):
        self.desktop = None
        self.aedtapp = None
        self.aedt_apps = {
            "Circuit Design": "Circuit",
            "HFSS": "Hfss",
            "EMIT": "Emit",
            "HFSS 3D Layout Design": "Hfss3dLayout",
            "Icepak": "Icepak",
            "Maxwell 2D": "Maxwell2d",
            "Maxwell 3D": "Maxwell3d",
            "Maxwell Circuit": "MaxwellCircuit",
            "2D Extractor": "Q2d",
            "Q3D Extractor": "Q3d",
            "RMxprt": "Rmxprt",
            "Twin Builder": "Simplorer",
            "Mechanical": "Mechanical",
        }

    def aedt_connected(self):
        """Check if AEDT is connected.

        Returns
        -------
        tuple[bool, str]
            A tuple indicating the connection status and a message.

        Examples
        --------
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> import time
        >>> toolkit = ToolkitGeneric()
        >>> msg = toolkit.launch_aedt()
        >>> response = toolkit.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit.connect_aedt()
        >>> toolkit.aedt_connected()
        (True, "Toolkit connected to process <process_id> on Grpc <grpc_port>")
        >>> toolkit.release_aedt()
        """
        if self.desktop:
            if self.desktop.port != 0:
                msg = "Toolkit connected to process {} on Grpc {}".format(
                    str(self.desktop.aedt_process_id),
                    str(self.desktop.port),
                )
                logger.debug(msg)
            else:
                msg = "Toolkit connected to process {}".format(str(self.desktop.aedt_process_id))
                logger.debug(msg)
            connected = True
        else:
            msg = "Toolkit not connected to AEDT"
            logger.debug(msg)
            connected = False
        return connected, msg
    @staticmethod
    def get_project_name(project_path):
        """Get project name from project path.

        Returns
        -------
        str
            Project name
        """
        return os.path.splitext(os.path.basename(project_path))[0]

    def get_design_names(self):
        """Get design names for a specific project, the first one is the active.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit.get_design_names()
        """
        if properties.selected_process == 0:
            logger.error("Process ID not defined")
            return False

        design_list = []
        active_project = self.get_project_name(properties.active_project)
        if active_project and active_project != "No project":
            for design in properties.design_list[active_project]:
                design_list.append(design)

            if properties.active_design and properties.active_design in design_list:
                index = design_list.index(properties.active_design)
                design_list.insert(0, design_list.pop(index))

        return design_list

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
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit_free = toolkit.get_thread_status()
        """
        # Check if the backend is already connected to an AEDT session
        connected, msg = self.aedt_connected()
        if not connected:
            version = properties.aedt_version
            non_graphical = properties.non_graphical
            selected_process = properties.selected_process
            use_grpc = properties.use_grpc

            pyaedt.settings.use_grpc_api = use_grpc
            if selected_process == 0:  # pragma: no cover
                # Launch AEDT with COM
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    new_desktop_session=True,
                )
            elif use_grpc:
                # Launch AEDT with GRPC
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    port=selected_process,
                    new_desktop_session=False,
                )
            else:  # pragma: no cover
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    aedt_process_id=selected_process,
                    new_desktop_session=False,
                )

            if not self.desktop:
                msg = "AEDT not launched"
                logger.error(msg)
                return False

            msg = "AEDT launched"
            logger.debug(msg)

            # Save AEDT session properties
            if use_grpc:
                properties.selected_process = self.desktop.port
                logger.debug("Grpc port {}".format(str(self.desktop.port)))
            else:
                properties.selected_process = self.desktop.aedt_process_id
                logger.debug("Process ID {}".format(str(self.desktop.aedt_process_id)))

            self._save_project_info()

            if self.desktop.project_list():
                # If there are projects not saved in the session, PyAEDT could find issues loading some properties
                self.desktop.save_project()

            self.desktop.release_desktop(False, False)
            self.desktop = None

            logger.debug("Desktop released and project properties loaded")

        return True

    def connect_aedt(self):
        """Connect to an existing AEDT session.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit.connect_aedt()
        >>> toolkit.release_aedt()
        """
        if properties.selected_process == 0:
            logger.error("Process ID not defined")
            return False
        connected, msg = self.aedt_connected()
        if not connected:
            version = properties.aedt_version
            non_graphical = properties.non_graphical
            selected_process = properties.selected_process
            use_grpc = properties.use_grpc

            # Connect to AEDT
            pyaedt.settings.use_grpc_api = use_grpc
            logger.debug("Connecting AEDT")
            if use_grpc:
                # Launch AEDT with GRPC
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    port=selected_process,
                    new_desktop_session=False,
                )

            else:  # pragma: no cover
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    aedt_process_id=selected_process,
                    new_desktop_session=False,
                )

            if not self.desktop:  # pragma: no cover
                logger.debug("AEDT not connected")
                return False

            logger.debug("AEDT connected")
            return True

    def connect_design(self, app_name=None):
        """Connect to an application design.
        If a design exists, it takes the active project and design, if not,
        it creates a new design of the specified type. If no application specified, the default is ``"Hfss"``.

        Parameters
        ----------
        app_name : str, optional
            Aedt application name. The default is connecting to active design. Application available are:

            * Circuit Design
            * HFSS
            * Edb
            * EMIT
            * HFSS 3D Layout Design
            * Icepak
            * Maxwell 2D
            * Maxwell 3D
            * 2D Extractor
            * Q3D Extractor
            * Rmxprt
            * Twin Builder
            * Mechanical

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit.connect_design()

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

        if design_name != "No design":
            project_name = self.get_project_name(project_name)
            self.aedtapp = self.desktop[[project_name, design_name]]
            active_design = self.aedtapp.design_name
        elif app_name in list(self.aedt_apps.keys()):
            design_name = pyaedt.generate_unique_name(app_name)
            aedt_app_attr = getattr(pyaedt, self.aedt_apps[app_name])

            if properties.use_grpc:
                self.aedtapp = aedt_app_attr(
                    specified_version=properties.aedt_version,
                    port=properties.selected_process,
                    non_graphical=properties.non_graphical,
                    new_desktop_session=False,
                    projectname=project_name,
                    designname=design_name,
                )
            else:
                self.aedtapp = aedt_app_attr(
                    specified_version=properties.aedt_version,
                    aedt_process_id=properties.selected_process,
                    non_graphical=properties.non_graphical,
                    new_desktop_session=False,
                    projectname=project_name,
                    designname=design_name,
                )
            active_design = design_name
            self.aedtapp.save_project()
        else:
            logger.error("AEDT application not available in PyAEDT.")
            return False

        if self.aedtapp:
            project_name = self.aedtapp.project_file
            if self.aedtapp.project_file not in properties.project_list:
                properties.project_list.append(project_name)
                properties.design_list[self.aedtapp.project_name] = [active_design]

            if self.aedtapp.design_list and active_design not in properties.design_list[self.aedtapp.project_name]:
                properties.design_list[self.aedtapp.project_name].append(active_design)
            properties.active_project = project_name
            properties.active_design = active_design

            return True

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
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit.release_aedt(True, True)

        """
        released = False
        if self.desktop:
            try:
                released = self.desktop.release_desktop(close_projects, close_on_exit)
                self.desktop = None
                self.aedtapp = None
            except:
                logger.error("Desktop not released")
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
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit.open_project("path/to/file")
        >>> toolkit.release_aedt()

        """
        if not self.connect_aedt():
            return False
        if not os.path.exists(properties.active_project + ".lock") and self.desktop and project_name:
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
        >>> from ansys.aedt.toolkits.common.backend.api_generic import ToolkitGeneric
        >>> toolkit = ToolkitGeneric()
        >>> toolkit.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> toolkit.connect_aedt()
        >>> toolkit.save_project()
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
            self.aedtapp.release_desktop(False, False)
            logger.debug("Project saved: {}".format(project_path))
            return True
        else:  # pragma: no cover
            logger.error("Project not saved")
            return False

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
            for key in new_properties:
                setattr(properties, key, new_properties[key])


class EdbServiceGeneric(object):
    def __init__(self):
        self.edb = None
        self.layout_stats = {}

    def load_edb(self):
        """Missed docstring."""
        edb_file = properties.edb_file
        aedt_version = properties.aedt_version
        self.edb = pyaedt.Edb(edbversion=aedt_version, edbpath=edb_file)
        if self.edb and self.edb.cell_names:
            return True
        return False

    def close_edb(self):
        """Missed docstring."""
        if self.edb:
            result = self.edb.close_edb()
            self.edb = None
            return result

    def save_edb(self):
        """Missed docstring."""
        saved_edb = properties.saved_edb
        if self.edb:
            if self.save_edb:
                return self.edb.save_as(saved_edb)
            else:
                return self.edb.save(saved_edb)
        return False

    def get_net_list(self):
        """Missed docstring."""
        if self.edb:
            return list(self.edb.nets.nets.keys())
        return False

    def get_signal_nets(self):
        """Missed docstring."""
        if self.edb:
            return list(self.edb.nets.signal_nets.keys())
        return False

    def get_power_nets(self):
        """Missed docstring."""
        if self.edb:
            return list(self.edb.nets.power_nets.keys())
        return False

    def get_components(self):
        """Missed docstring."""
        if self.edb:
            component_list = []
            for cmp in list(self.edb.components.components.values()):
                cmp_data = ComponentData()
                cmp_data.refdes = cmp.refdes
                cmp_data.nets = cmp.nets
                cmp_data.type = cmp.type
                cmp_data.numpins = cmp.numpins
                cmp_data.partname = cmp.partname
                cmp_data.spice_model = cmp.spice_model
                cmp_data.placement_layer = cmp.placement_layer
                cmp_data.res_value = cmp.res_value
                cmp_data.ind_value = cmp.ind_value
                cmp_data.cap_value = cmp.cap_value
                cmp_data.is_enabled = cmp.is_enabled
                cmp_data.is_parallel_rlc = cmp.is_parallel_rlc
                component_list.append(cmp_data.__dict__)
            return component_list
        return False

    def get_all_layers(self):
        """Missed docstring."""
        if self.edb:
            return list(self.edb.stackup.stackup_layers.keys())

    def get_signal_layers(self):
        """Missed docstring."""
        if self.edb:
            return list(self.edb.stackup.signal_layers.keys())

    def get_dielectric_layers(self):
        """Missed docstring."""
        if self.edb:
            return list(self.edb.stackup.dielectric_layers.keys())

    def get_layout_stats(self):
        """Missed docstring."""
        if self.edb:
            edb_stats = self.edb.get_statistics().__dict__
            for k, v in edb_stats.items():
                if k[0] == "_":
                    self.layout_stats[k[1:]] = v
                else:
                    self.layout_stats[k] = v
            return self.layout_stats

    def get_layout_surface_ratio(self):
        """Missed docstring."""
        if self.layout_stats:
            if self.layout_stats["occupying_ratio"]:
                return self.layout_stats["occupying_surface"], self.layout_stats["occupying_ratio"]
        # bug compute surface area to be fixed
        stats = self.edb.get_statistics().__dict__
        for k, v in stats.items():
            if k[0] == "_":
                self.layout_stats[k[1:]] = v
            else:
                self.layout_stats[k] = v
        return self.layout_stats["occupying_surface"], self.layout_stats["occupying_ratio"]

    def get_extended_net(self):
        """Missed docstring."""
        net_dict = {}
        power_nets = list(self.edb.nets.power_nets.keys())
        for comp, inst in self.edb.components.instances.items():
            if inst.type in ["Resistor", "Inductor", "Capacitor"]:
                if inst.type == "Resistor" and self.edb._edb.Utility.Value(inst.res_value).ToDouble() < 50:
                    for n in inst.nets:
                        if n in net_dict:
                            net_dict[n].append(comp)
                        else:
                            net_dict[n] = [comp]
        extended_nets_dict = {}
        for net, comp_list1 in net_dict.items():
            comp_to_test = set(comp_list1)
            for net2, comp_list2 in net_dict.items():
                if not net == net2 and net not in power_nets and net2 not in power_nets:
                    if comp_to_test.intersection(set(comp_list2)):
                        if net in extended_nets_dict:
                            extended_nets_dict[net].append(net2)
                        else:
                            extended_nets_dict[net] = [net2]
        return extended_nets_dict

    def export_config_file(self):
        """Missed docstring."""
        if self.edb:
            config = {}
            config["filename"] = properties.filename
            config["dc_settings"] = properties.dc_settings
            config["ac_settings"] = properties.ac_settings
            config["batch_solve_settings"] = properties.batch_solve_settings
            config["setup_name"] = properties.setup_name
            config["solver_type"] = properties.solver_type
            json_file = properties.config_file
            if os.path.isfile(json_file):
                os.remove(json_file)
            with open(json_file, "w") as write_file:
                json.dump(config, write_file, indent=4)
            if os.path.isfile(json_file):
                return True
        return False

    def build_edb_project(self):
        """Missed docstring."""

        if self.edb:
            sim_config = self.edb.new_simulation_configuration()
            config = {}
            config["filename"] = properties.filename
            config["dc_settings"] = properties.dc_settings
            config["ac_settings"] = properties.ac_settings
            config["batch_solve_settings"] = properties.batch_solve_settings
            config["setup_name"] = properties.setup_name
            config["solver_type"] = properties.solver_type
            temp_folder = os.path.join(properties.filename, "_temp")
            if os.path.isdir(temp_folder):
                shutil.rmtree(temp_folder)
            os.mkdir(temp_folder)
            json_file = os.path.join(temp_folder, "simsetup.json")
            if os.path.isfile(json_file):
                os.remove(json_file)
            with open(json_file, "w") as write_file:
                json.dump(config, write_file, indent=4)
            if os.path.isfile(json_file):
                sim_config.import_json(json_file)
            edb_file_name = pathlib.Path(self.edb.directory).name
            temp_edb = os.path.join(temp_folder, edb_file_name)
            shutil.copytree(self.edb.directory, temp_edb)
            final_edb = os.path.join(properties.filename, edb_file_name)
            edb = pyaedt.Edb(edbversion=properties.aedt_version, edbpath=temp_edb)
            edb.build_simulation_project(sim_config)
            edb.save_as(final_edb)
            edb.close_edb()
            return final_edb
        return False


class ComponentData(object):
    """Missed docstring."""

    def __init__(self):
        self.refdes = ""
        self.numpins = 0
        self.type = "Resistor"
        self.partname = ""
        self.cap_value = 0.0
        self.res_value = 1.0
        self.ind_value = 0.0
        self.is_enabled = True
        self.is_parallel_rlc = True
        self.nets = []
        self.placement_layer = ""
        self.spice_model = ""
