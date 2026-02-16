from PySide6.QtWidgets import *
from PySide6.QtGui import *

from ansys.aedt.toolkits.common.ui.utils.widgets.py_window.styles import Styles


class PyWindow(QFrame):
    def __init__(self, parent, margin=0, spacing=2,
                 bg_color="#2c313c", text_color="#fff", text_font="9pt 'Segoe UI'",
                 border_radius=10, border_size=2, border_color="#343b48", enable_shadow=True):
        super().__init__(parent)
        self.parent = parent
        self.margin = margin
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_font = text_font
        self.border_radius = border_radius
        self.border_size = border_size
        self.border_color = border_color
        self.enable_shadow = enable_shadow

        self.setObjectName("pod_bg_app")

        self.set_stylesheet()

        # Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(spacing)

        # Add shadow
        if enable_shadow:
            self._addDropShadow()

    def set_stylesheet(self, bg_color=None, border_radius=None, border_size=None,
                       border_color=None, text_color=None, text_font=None):
        # Use provided if not None else get the instance attribute
        style_args = {
            "_bg_color": bg_color or self.bg_color,
            "_border_radius": border_radius or self.border_radius,
            "_border_size": border_size or self.border_size,
            "_border_color": border_color or self.border_color,
            "_text_color": text_color or self.text_color,
            "_text_font": text_font or self.text_font
        }

        self.setStyleSheet(Styles.bg_style.format(**style_args))

    def _addDropShadow(self) -> None:
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(self.shadow)
