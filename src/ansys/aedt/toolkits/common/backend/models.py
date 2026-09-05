import json
import os
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class CommonProperties(BaseModel):
    """Store common AEDT properties."""

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
    toolkit_name: str = "common"
    log_file: str = "common_backend.log"


class Properties(CommonProperties, validate_assignment=True):
    """Store all properties."""


common_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "common_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.json")) as file_handler:
        common_kwargs = json.load(file_handler)

common_properties = Properties(**common_kwargs)
