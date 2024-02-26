from PySide6.QtCore import QEvent
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton


class PyIconButton(QPushButton):
    """
    Icon button widget that can be used as a colored icon.

    The icon and color can be customized during initialization.

    Parameters
    ----------
    icon_path : str
        Path to the icon image file.
    tooltip_text : str, optional
        Text for tooltip.
    btn_id : str, optional
        Identifier for the button.
    width : int, optional
        Width of the button.
    height : int, optional
        Height of the button.
    radius : int, optional
        Radius for rounded corners.
    bg_color : str, optional
        Background color in hex color code.
    bg_color_hover : str, optional
        Background color when hovered in hex color code.
    bg_color_pressed : str, optional
        Background color when being pressed in hex color code.
    icon_color : str, optional
        Icon color in hex color code.
    icon_color_hover : str, optional
        Icon color when hovered in hex color code.
    icon_color_pressed : str, optional
        Icon color when being pressed in hex color code.
    icon_color_active : str, optional
        Active icon color in hex color code.
    dark_one : str, optional
        Color for dark theme in hex color code.
    text_foreground : str, optional
        Text color in hex color code.
    context_color : str, optional
        Context color in hex color code.
    top_margin : int, optional
        Top margin for tooltip.
    is_active : bool, optional
        Whether the button is currently active.

    The rest of the parameters customize the look and emit signals for
    different user interactions.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import *

    >>> class Example(QWidget):
    >>>     def __init__(self):
    >>>         super().__init__()
    >>>         layout = QVBoxLayout(self)
    >>>         layout.addWidget(QPushButton("Button 1"))
    >>>         layout.addWidget(PyIconButton('icon_signal.svg', "#FF0000", tooltip_text="Example")
    >>>         )
    >>>         layout.addWidget(QPushButton("Button 2"))

    >>> if __name__ == "__main__":
    >>>     app = QApplication([])
    >>>     window = Example()
    >>>     window.show()
    >>>     app.exec()
    """

    def __init__(
        self,
        icon_path=None,
        tooltip_text="",
        btn_id=None,
        width=30,
        height=30,
        radius=8,
        bg_color="#343b48",
        bg_color_hover="#3c4454",
        bg_color_pressed="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        dark_one="#1b1e23",
        text_foreground="#8a95aa",
        context_color="#568af2",
        top_margin=40,
        is_active=False,
    ):
        super().__init__()

        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName(btn_id)

        self._bg_color = bg_color
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._top_margin = top_margin
        self._is_active = is_active
        # Set Parameters
        self._set_bg_color = bg_color
        self._set_icon_path = icon_path
        self._set_icon_color = icon_color
        self._set_border_radius = radius

        # TOOLTIP
        if tooltip_text:
            self._tooltip_text = tooltip_text
            self._tooltip = Tooltip(tooltip_text, dark_one, text_foreground)
            self._tooltip.hide()

    def set_active(self, is_active):
        """
        Set the active state of the button.

        Parameters
        ----------
        is_active : bool
            Whether the button is active or not.
        """
        self._is_active = is_active
        self.repaint()

    def is_active(self):
        """
        Check if the button is in an active state.

        Returns
        -------
        bool
            True if the button is active, False otherwise.
        """
        return self._is_active

    def paintEvent(self, event):
        """
        Paint the button.

        Parameters
        ----------
        event : QEvent
            Paint event.
        """
        # PAINTER
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._is_active:
            # BRUSH
            brush = QBrush(QColor(self._context_color))
        else:
            # BRUSH
            brush = QBrush(QColor(self._set_bg_color))

        # CREATE RECTANGLE
        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(rect, self._set_border_radius, self._set_border_radius)

        # DRAW ICONS
        self.icon_paint(paint, self._set_icon_path, rect)

        # END PAINTER
        paint.end()

    def change_style(self, event):
        """
        Change the style of the button based on the given event.

        Parameters
        ----------
        event : QEvent
            Event triggering the style change.
        """
        if event == QEvent.Enter:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()
        elif event == QEvent.Leave:
            self._set_bg_color = self._bg_color
            self._set_icon_color = self._icon_color
            self.repaint()
        elif event == QEvent.MouseButtonPress:
            self._set_bg_color = self._bg_color_pressed
            self._set_icon_color = self._icon_color_pressed
            self.repaint()
        elif event == QEvent.MouseButtonRelease:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()

    def enterEvent(self, event):
        """
        Handle the enter event.

        Parameters
        ----------
        event : QEvent
            Enter event.
        """
        self.change_style(QEvent.Enter)

    def leaveEvent(self, event):
        """
        Handle the leave event.

        Parameters
        ----------
        event : QEvent
            Leave event.
        """
        self.change_style(QEvent.Leave)

    def mousePressEvent(self, event):
        """
        Handle the mouse press event.

        Parameters
        ----------
        event : QEvent
            Mouse press event.
        """
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonPress)
            self.setFocus()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        """
        Handle the mouse release event.

        Parameters
        ----------
        event : QEvent
            Mouse release event.
        """
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonRelease)
            return self.released.emit()

    def icon_paint(self, qp, image, rect):
        """
        Paint the icon on the button.

        Parameters
        ----------
        qp : QPainter
            QPainter object.
        image : str
            Path to the icon image file.
        rect : QRect
            Rectangle for the icon placement.
        """
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        if self._is_active:
            painter.fillRect(icon.rect(), self._icon_color_active)
        else:
            painter.fillRect(icon.rect(), self._set_icon_color)
        qp.drawPixmap((rect.width() - icon.width()) / 2, (rect.height() - icon.height()) / 2, icon)
        painter.end()

    def set_icon(self, icon_path):
        """
        Set the icon for the button.

        Parameters
        ----------
        icon_path : str
            Path to the icon image file.
        """
        self._set_icon_path = icon_path
        self.repaint()


class Tooltip(QLabel):
    """
    Tooltip class to display tooltip for the PyIconButton.

    Parameters
    ----------
    tooltip : str
        Text to be displayed in the tooltip.
    dark_one : str
        Dark color for theming.
    text_foreground : str
        Text foreground color.
    """

    style_tooltip = """
    QLabel {{
        background-color: {_dark_one};
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        font: 800 9pt "Segoe UI";
    }}
    """

    def __init__(self, tooltip, dark_one, text_foreground):
        QLabel.__init__(self)

        style = self.style_tooltip.format(_dark_one=dark_one, _text_foreground=text_foreground)
        self.setObjectName("label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setText(tooltip)
        self.adjustSize()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
