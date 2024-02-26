from PySide6.QtCore import QEvent
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton


class PyTitleButton(QPushButton):
    """
    Customizable title button.

    Inherits QPushButton and provides a customizable title button.

    Parameters
    ----------
    parent : QWidget
        Parent widget.
    app_parent : QWidget, optional
        Application parent widget. The default is ``None``.
    tooltip_text : str, optional
        Tooltip text for the button. The default is an empty string.
    btn_id : str, optional
        Button ID. The default is ``None``.
    width : int, optional
        Width of the button. The default is ``30``.
    height : int, optional
        Height of the button. The default is ``30``.
    radius : int, optional
        Border radius of the button. The default is ``8``.
    bg_color : str, optional
        Background color of the button. The default is ``"#343b48"``.
    bg_color_hover : str, optional
        Background color when the mouse hovers over the button. The default is ``"#3c4454"``.
    bg_color_pressed : str, optional
        Background color when the button is pressed. The default is ``"#2c313c"``.
    icon_color : str, optional
        Icon color of the button. The default is ``"#c3ccdf"``.
    icon_color_hover : str, optional
        Icon color when the mouse hovers over the button. The default is ``"#dce1ec"``.
    icon_color_pressed : str, optional
        Icon color when the button is pressed. The default is ``"#edf0f5"``.
    icon_color_active : str, optional
        Icon color when the button is active. The default is ``"#f5f6f9"``.
    icon_path : str, optional
        Path to the icon image. The default is ``"no_icon.svg"``.
    dark_one : str, optional
        Dark color for styling. The default is ``"#1b1e23"``.
    context_color : str, optional
        Context color for styling. The default is ``"#568af2"``.
    text_foreground : str, optional
        Text foreground color. The default is ``"#8a95aa"``.
    is_active : bool, optional
        Initial state of the button (active or not). The default is ``False``.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import QApplication, QWidget
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import PyTitleButton

    >>> class MyApp(QWidget):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.title_button = PyTitleButton(self, tooltip_text="Click me!")
    ...         self.title_button.clicked.connect(self.on_button_clicked)
    ...         self.title_button.released.connect(self.on_button_released)
    ...
    ...     def on_button_clicked(self):
    ...         print("Button Clicked!")
    ...
    ...     def on_button_released(self):
    ...         print("Button Released!")
    ...
    >>> if __name__ == "__main__":
    ...     app = QApplication([])
    ...     window = MyApp()
    ...     sys.exit(app.exec())
    """

    def __init__(
        self,
        parent,
        app_parent=None,
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
        icon_path="no_icon.svg",
        dark_one="#1b1e23",
        context_color="#568af2",
        text_foreground="#8a95aa",
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
        self._top_margin = self.height() + 6
        self._is_active = is_active

        self._set_bg_color = bg_color
        self._set_icon_path = icon_path
        self._set_icon_color = icon_color
        self._set_border_radius = radius

        self._parent = parent
        self._app_parent = app_parent

        self._tooltip_text = tooltip_text
        self._tooltip = _ToolTip(app_parent, tooltip_text, dark_one, context_color, text_foreground)
        self._tooltip.hide()

    def set_active(self, is_active):
        """
        Set the active state of the button.

        Parameters
        ----------
        is_active : bool
            True to set the button as active, False otherwise.
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
        Paint the button and its icon.

        Parameters
        ----------
        event : QEvent
            Paint event.
        """
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
            The event triggering the style change.

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
        Event triggered when the mouse enters the button.

        Parameters
        ----------
        event : QEvent
            Mouse enter event.
        """
        self.change_style(QEvent.Enter)
        self.move_tooltip()
        self._tooltip.show()

    def leaveEvent(self, event):
        """
        Event triggered when the mouse leaves the button.

        Parameters
        ----------
        event : QEvent
            Mouse leave event.
        """
        self.change_style(QEvent.Leave)
        self.move_tooltip()
        self._tooltip.hide()

    def mousePressEvent(self, event):
        """
        Event triggered when the left mouse button is pressed.

        Parameters
        ----------
        event : QEvent
            Mouse press event.
        """
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonPress)
            # SET FOCUS
            self.setFocus()
            # EMIT SIGNAL
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        """
        Event triggered when the left mouse button is released.

        Parameters
        ----------
        event : QEvent
            Mouse release event.
        """
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonRelease)
            # EMIT SIGNAL
            return self.released.emit()

    def icon_paint(self, qp, image, rect):
        """
        Draw the icon with specified colors.

        Parameters
        ----------
        qp : QPainter
            The QPainter object.
        image : str
            Path to the icon image.
        rect : QRect
            Rectangle representing the button's area.
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
        Set the icon of the button.

        Parameters
        ----------
        icon_path : str
            Path to the icon image.
        """
        self._set_icon_path = icon_path
        self.repaint()

    def move_tooltip(self):
        """
        Move the tooltip to the appropriate position relative to the button.
        """
        # GET MAIN WINDOW PARENT
        gp = self.mapToGlobal(QPoint(0, 0))

        # SET WIDGET TO GET POSITION
        # Return absolute position of widget inside app
        pos = self._parent.mapFromGlobal(gp)

        # FORMAT POSITION
        # Adjust tooltip position with offset
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self._top_margin

        # SET POSITION TO WIDGET
        # Move tooltip position
        self._tooltip.move(pos_x, pos_y)


class _ToolTip(QLabel):
    # TOOLTIP / LABEL StyleSheet
    style_tooltip = """
    QLabel {{
        background-color: {_dark_one};
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-right: 3px solid {_context_color};
        font: 800 9pt "Segoe UI";
    }}
    """

    def __init__(self, parent, tooltip, dark_one, context_color, text_foreground):
        QLabel.__init__(self)

        # LABEL SETUP
        style = self.style_tooltip.format(
            _dark_one=dark_one, _context_color=context_color, _text_foreground=text_foreground
        )
        self.setObjectName("label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
