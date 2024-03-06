import json
from pathlib import Path

from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.models import general_settings


def _default_theme_setup(path: Path) -> Path:
    """
    Set up the default theme.

    If the "settings.json" file is not found, log an error and load the default theme from the specified path.

    Parameters
    ----------
    path : Path
        The base path for the default theme.

    Returns
    -------
    Path
        The full path to the default theme file.
    """
    logger.error(f'"settings.json" not found! Loaded default.')
    return path / "ansys_dark.json"


class ThemeHandler:
    """
    A class for managing themes in a PySide6 desktop application.

    This class handles the loading, exporting, and management of themes used in the application.

    Examples
    --------
    >>> theme_handler = ThemeHandler()
    >>> theme_handler.export_theme()
    """

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
        """
        Export the current theme to the theme file.

        Writes the current theme settings to the theme file in JSON format.
        """
        self.theme_path.write_text(json.dumps(self.items, indent=4), encoding="utf-8")

    def read_theme(self) -> None:
        """
        Read and load theme settings from the theme file.

        Reads the theme settings from the theme file in JSON format and updates the internal state.
        """
        self.items = json.loads(self.theme_path.read_text(encoding="utf-8"))
