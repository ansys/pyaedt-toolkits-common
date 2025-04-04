from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QCheckBox


class PyToggle(QCheckBox):
    """
    Customizable toggle switch.

    Inherits QCheckBox and provides a customizable toggle switch with options
    for width, background color, circle color, active color, and animation curve.

    Parameters
    ----------
    width : int, optional
        Width of the toggle switch. The default is ``50``.
    bg_color : str, optional
        Background color of the toggle switch. The default is ``"#777"``.
    circle_color : str, optional
        Color of the circle in the toggle switch. The default is ``"#DDD"``.
    active_color : str, optional
        Color of the toggle switch when active. The default is ``"#00BCFF"``.

    Examples
    --------
    >>> import sys
    >>> from PySide6.QtWidgets import QApplication
    >>> from ansys.aedt.toolkits.common.ui.utils.widgets import PyToggle

    >>> class MyApp(QWidget):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.toggle = PyToggle()
    ...         self.toggle.stateChanged.connect(self.toggle_state_changed)
    ...         self.toggle.show()

    ...     def toggle_state_changed(self, state):
    ...         print("Toggle State:", state)

    >>> if __name__ == "__main__":
    ...     app = QApplication([])
    ...     window = MyApp()
    ...     sys.exit(app.exec())
    """

    def __init__(self, width=50, bg_color="#777", circle_color="#DDD", active_color="#00BCFF"):
        QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

    def hitButton(self, pos: QPoint):
        """
        Determine if a button press occurred within the toggle switch.

        Parameters
        ----------
        pos : QPoint
            The position of the button press.

        Returns
        -------
        bool
            True if the button press occurred within the toggle switch, False otherwise.
        """
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        """
        Paint the toggle switch.

        Parameters
        ----------
        e : QPaintEvent
            Paint event.
        """
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(QFont("Segoe UI", 9))

        # SET PEN
        p.setPen(Qt.NoPen)

        # DRAW RECT
        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(4, 3, 22, 22)
        else:
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self.width() - 26, 3, 22, 22)

        p.end()
