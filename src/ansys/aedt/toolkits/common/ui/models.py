import json
import os
from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class UIProperties(BaseModel):
    """Store common UI properties."""

    toolkit_name: str = "common"
    backend_url: str = "127.0.0.1"
    backend_port: int = 5001
    debug: bool = True
    log_file: str = "common_frontend.log"
    app_name: str = "Toolkit Wizard"
    main_title: str = "Toolkit Template Wizard"
    welcome_message: str = "Welcome to the Toolkit"
    version: str = "v0.0.1"
    copyright: str = "By: x"
    year: int = 2024
    startup_size: List[int] = Field(default_factory=list)
    minimum_size: List[int] = Field(default_factory=list)
    left_menu_size: Dict[str, int] = Field(default_factory=dict)
    left_menu_content_margins: int = 3
    left_column_size: Dict[str, int] = Field(default_factory=dict)
    right_column_size: Dict[str, int] = Field(default_factory=dict)
    progress_size: Dict[str, int] = Field(default_factory=dict)
    font: Dict[str, Any] = Field(default_factory=dict)
    high_resolution: bool = False
    theme: str = "ansys.json"
    images: str = ""
    add_left_menus: List[Dict] = Field(default_factory=list)
    add_title_bar_menus: List[Dict] = Field(default_factory=list)


class Properties(UIProperties, validate_assignment=True):
    """Store all properties."""


common_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "common_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.json")) as file_handler:
        common_kwargs = json.load(file_handler)

general_settings = Properties(**common_kwargs)
