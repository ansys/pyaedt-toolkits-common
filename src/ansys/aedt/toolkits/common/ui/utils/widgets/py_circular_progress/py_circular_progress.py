from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

# Default parameter values
DEFAULT_VALUE = 0
DEFAULT_PROGRESS_WIDTH = 10
DEFAULT_IS_ROUNDED = True
DEFAULT_MAX_VALUE = 100
DEFAULT_PROGRESS_COLOR = "#ff79c6"
DEFAULT_ENABLE_TEXT = True
DEFAULT_FONT_FAMILY = "Segoe UI"
DEFAULT_FONT_SIZE = 12
DEFAULT_SUFFIX = "%"
DEFAULT_TEXT_COLOR = "#ff79c6"
DEFAULT_ENABLE_BG = True
DEFAULT_BG_COLOR = "#151617"


class PyCircularProgress(QWidget):
    """
    PyCircularProgress, a customized QWidget class for creating circular progress bars.

    Parameters
    ----------
    value : int, optional
        The current progress value, by default 0.
    progress_width : int, optional
        The width of the progress bar, by default 10.
    is_rounded : bool, optional
        Specifies the style of the progress bar cap, round if True, by default True.
    max_value : int, optional
        Specifies the maximum value of the progress, by default 100.
    progress_color : str, optional
        Specifies the color of the progress, by default "#ff79c6".
    enable_text : bool, optional
        Specifies if the progress value should be displayed as text if True, by default True.
    font_family : str, optional
        Specifies the font family of the text, by default "Segoe UI".
    font_size : int, optional
        Specifies the font size, by default 12.
    suffix : str, optional
        Specifies the suffix displayed after the progress value, by default "%".
    text_color : str, optional
        Specifies the color of the text, by default "#ff79c6".
    enable_bg : bool, optional
        Specifies if the progress bar background should be displayed if True, by default True.
    bg_color : str, optional
        Specifies the color of the background, by default "#44475a".

    Examples
    --------
    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from utils.widgets import *
    >>> app = QApplication(sys.argv)
    >>> circular_progress = PyCircularProgress()
    >>> circular_progress.set_value(60)
    >>> circular_progress.show()
    >>> sys.exit(app.exec())
    """

    def __init__(
            self,
            value=DEFAULT_VALUE,
            progress_width=DEFAULT_PROGRESS_WIDTH,
            is_rounded=DEFAULT_IS_ROUNDED,
            max_value=DEFAULT_MAX_VALUE,
            progress_color=DEFAULT_PROGRESS_COLOR,
            enable_text=DEFAULT_ENABLE_TEXT,
            font_family=DEFAULT_FONT_FAMILY,
            font_size=DEFAULT_FONT_SIZE,
            suffix=DEFAULT_SUFFIX,
            text_color=DEFAULT_TEXT_COLOR,
            enable_bg=DEFAULT_ENABLE_BG,
            bg_color=DEFAULT_BG_COLOR
    ):

        super().__init__()

        self.value = value
        self.progress_width = progress_width
        self.progress_rounded_cap = is_rounded
        self.max_value = max_value
        self.progress_color = progress_color
        self.enable_text = enable_text
        self.font_family = font_family
        self.font_size = font_size
        self.suffix = suffix
        self.text_color = text_color
        self.enable_bg = enable_bg
        self.bg_color = bg_color
        self.shadow = None

    def add_shadow(self, enable):
        """
        Add a shadow effect to the widget.

        Parameters
        ----------
        enable : bool
            Specifies if the shadow effect should be added.
        """
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 80))
            self.setGraphicsEffect(self.shadow)

    def set_value(self, value):
        """
        Set the progress value of the widget.

        Parameters
        ----------
        value : int
            The progress value.
        """
        self.value = value
        self.repaint()  # Render progress bar after change value

    def paintEvent(self, e):
        """
        Paint event to draw the widget.

        Parameters
        ----------
        e : QEvent
            The PaintEvent parameter, not used directly in this method.
        """
        width, height = self.width() - self.progress_width, self.height() - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)  # Remove pixelated edges
        paint.setFont(QFont(self.font_family, self.font_size))

        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)

        self.draw_bg(paint, margin, width, height)

        self.draw_progress(paint, margin, width, height, value)

        self.draw_text(paint, rect)

        paint.end()

    def draw_bg(self, paint, margin, width, height):
        """
        Draws the background of the circular progress bar if self.enable_bg is set to True.

        Parameters
        ----------
        paint : QPainter
            QPainter instance to use for drawing.
        margin : int
            Margin from the edge of the widget to start drawing.
        width, height : int
            Width and height of the circumference of the circular progress bar.
        """
        if self.enable_bg:
            pen = self._configure_pen(self.progress_width, self.bg_color, self.progress_rounded_cap)
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, 0, 360 * 16)

    def draw_progress(self, paint, margin, width, height, value):
        """
        Draws the progress indicator of the circular progress bar.

        Parameters
        ----------
        paint : QPainter
            QPainter instance to use for drawing.
        margin : int
            Margin from the edge of the widget to start drawing.
        width, height : int
            Width and height of the circumference of the circular progress bar.
        value : int
            Current value of the progress indicator.
        """
        pen = self._configure_pen(self.progress_width, self.progress_color, self.progress_rounded_cap)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

    def draw_text(self, paint, rect):
        """
        Draws the progress text inside the circular progress bar if self.enable_text is set to True.

        Parameters
        ----------
        paint : QPainter
            QPainter instance to use for drawing.
        rect : QRect
            Rectangle instance for the text position inside the circular progress bar.
        """
        if self.enable_text:
            pen = self._configure_pen(self.progress_width, self.text_color, self.progress_rounded_cap)
            paint.setPen(pen)
            paint.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}")

    @staticmethod
    def _configure_pen(width, color, rounded):
        """
        Configure a QPen instance.

        Parameters
        ----------
        width : int
            The width of the pen.
        color : str
            The color of the pen.
        rounded : bool
            If true, sets the pen's cap style to round.

        Returns
        -------
        QPen
            A configured QPen instance.
        """
        pen = QPen()
        pen.setWidth(width)
        if rounded:
            pen.setCapStyle(Qt.RoundCap)
        pen.setColor(QColor(color))
        return pen