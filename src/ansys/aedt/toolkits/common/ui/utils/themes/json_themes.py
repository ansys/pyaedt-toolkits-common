import json
from pathlib import Path

from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.models import general_settings


def _default_theme_setup(path: Path) -> Path:
    logger.error(f'"settings.json" not found! Loaded default.')
    return path / "ansys.json"


class ThemeHandler:
    def __init__(self) -> None:
        theme = general_settings.theme
        current_file = Path(__file__).resolve()
        current_dir = current_file.parent
        theme_file = current_file.parent / theme
        self.available_themes = list(current_dir.glob("*.json"))
        self.items = {}

        if not theme_file.exists():
            theme_file = _default_theme_setup(current_dir)

        self.theme_path = theme_file
        self.read_theme()

    def export_theme(self) -> None:
        self.theme_path.write_text(json.dumps(self.items, indent=4), encoding="utf-8")

    def read_theme(self) -> None:
        self.items = json.loads(self.theme_path.read_text(encoding="utf-8"))
