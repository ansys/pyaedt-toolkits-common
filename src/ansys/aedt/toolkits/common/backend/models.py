import json
import os
from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class CommonProperties(BaseModel):
    """Store common AEDT properties."""

    toolkit: Dict[str, Any] = Field(default_factory=dict)
    aedt_version: str = "2023.2"
    non_graphical: bool = False
    active_project: str = ""
    active_design: str = ""
    project_list: List[str] = Field(default_factory=list)
    design_list: Dict[str, List[str]] = Field(default_factory=dict)
    selected_process: int = 0
    use_grpc: bool = True
    is_toolkit_busy: bool = False
    url: str = "127.0.0.1"
    port: int = 5001
    debug: bool = True
    log_file: str = "common_backend.log"


class Properties(CommonProperties, validate_assignment=True):
    """Store all properties."""

    def update_toolkit(self, toolkit_update: Dict[str, Any]):
        self.toolkit.update(toolkit_update)


common_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "common_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.json")) as file_handler:
        common_kwargs = json.load(file_handler)

backend_kwargs = {}
current_dir = os.getcwd()
backend_properties_file = os.path.expanduser(os.path.join(current_dir, "backend_properties.json"))
if os.path.exists(backend_properties_file):
    with open(backend_properties_file) as file_handler:
        backend_kwargs = json.load(file_handler)

toolkit_property = {}
if backend_kwargs:
    for backend_key, new_property_value in backend_kwargs.items():
        if backend_key in common_kwargs:
            common_kwargs[backend_key] = new_property_value
        else:
            toolkit_property[backend_key] = new_property_value

properties = Properties(**common_kwargs)

properties.update_toolkit(toolkit_property)
