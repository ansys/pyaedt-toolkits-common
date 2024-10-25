from PySide6.QtWidgets import QTabWidget

from ansys.aedt.toolkits.common.ui.utils.widgets.py_tab.styles import Styles


class PyTab(QTabWidget):
    """
    Initialize the PyTab.

    Parameters
    ----------
    color : str
        The pane color.
    text_color : str
        The text color.
    selected_color : int
        The color of the selected tab.
    unselected_color : str
        The color of the unselected tab.
    """

    def __init__(self, color, text_color, selected_color, unselected_color):
        super().__init__()

        # SET STYLESHEET
        custom_style = Styles.style.format(
            _color=color, _unselected_color=unselected_color, _selected_color=selected_color, _text_color=text_color
        )
        self.setStyleSheet(custom_style)
