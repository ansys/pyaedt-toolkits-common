from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ansys.aedt.toolkits.common.ui.properties import general_settings
from ansys.aedt.toolkits.common.ui.utils.widgets import *


class CommonWindow(object):
    """
    Class representing a common window with various UI functionalities.

    Args:
        app (QApplication): The QApplication instance.

    Attributes:
        ui (UI): The UI instance.
        left_box (QPropertyAnimation): Animation for the left column box.
        right_box (QPropertyAnimation): Animation for the right column box.
        group (QParallelAnimationGroup): Animation group for both columns.

    """

    def __init__(self):
        self.load_pages = None
        self.left_column = None
        self.left_column_frame = None
        self.right_column_frame = None
        self.right_column = None
        self.title_bar_frame = None
        self.left_menu = None
        self.themes = None
        self.group = None
        self.progress_frame = None

    def set_page(self, page):
        """
        Set the current page in the load_pages widget.

        :param page: The page widget to set as the current page.
        :return: None
        """
        self.load_pages.pages.setCurrentWidget(page)

    def get_left_menu(self, object_name):
        """
        :rtype: QPushButton
        :param object_name: the name of the button object in the left menu.
        :return: the QPushButton object with the given object_name found in the left menu of the CommonWindow UI.
        """
        return self.left_menu.findChild(QPushButton, object_name)

    def set_left_column_menu(self, menu, title, icon_path):
        """
        Set the left column menu, title, and icon path of the CommonWindow UI.

        :param menu: The menu widget to be set as the current widget in the left column.
        :param title: The title to be set in the left column title label.
        :param icon_path: The path to the icon image file to be set in the left column icon.

        :return: None
        """
        self.left_column.menus.menus.setCurrentWidget(menu)
        self.left_column.title_label.setText(title)
        self.left_column.icon.set_icon(icon_path)

    def is_left_column_visible(self):
        """
        Check if the left column is visible.

        :return: True if the left column is visible, False otherwise.
        """
        return self.left_column_frame.width() != 0

    def is_right_column_visible(self):
        """
        Checks if the right column is visible.

        :return: True if the right column is visible, False otherwise.
        """
        return self.right_column_frame.width() != 0

    def is_progress_visible(self):
        """
        Checks if the progress bar is visible.

        :return: True if the progress bar is visible, False otherwise.
        """
        return self.progress_frame.height() != 0

    def set_right_column_menu(self, title):
        """
        Sets the title of the right column menu.

        :param title: The title to be set.
        :return: None
        """
        self.right_column.title_label.setText(title)

    def get_title_bar(self, object_name):
        """
        :param object_name: The name of the QPushButton object.
        :return: The QPushButton object with the specified object_name found in the title_bar_frame of the CommonWindow's UI.
        """
        return self.title_bar_frame.findChild(QPushButton, object_name)

    def add_combobox(self,
                     layout,
                     height=40,
                     width=None,
                     label='label1',
                     combobox_list=None,
                     font_size=12):
        """
        Adds a label and combobox to a layout.
        :param layout: The layout object to which the label and combobox will be added.
        :param height: The height of the label and combobox widgets. Default is 40.
        :param width: The width of the label and combobox widgets. If not provided, a default width of [100, 100] will be used.
        :param label: The text to be displayed on the label widget. Default is 'label1'.
        :param combobox_list: A list of items to be displayed in the combobox. If not provided, a default list of ['1', '2'] will be used.
        :param font_size: The font size of the label widget. Default is 12.
        :return: A list containing the layout row object, label object, and combobox object.

        """
        combobox_list = combobox_list or []
        width = width or [100, 100]

        app_color = self.themes["app_color"]
        text_foreground = app_color["text_foreground"]
        dark_one = app_color["dark_one"]
        dark_two = app_color["dark_two"]
        bg_three = app_color["bg_three"]

        layout_row = QHBoxLayout()
        layout.addLayout(layout_row)

        label_widget = PyLabel(
            text=label, font_size=font_size, color=text_foreground
        )
        label_widget.setMinimumHeight(height)
        label_widget.setFixedWidth(width[0])
        layout_row.addWidget(label_widget)

        combobox_widget = PyComboBox(
            text=combobox_list,
            radius=8,
            color=dark_one,
            bg_color=dark_two,
            bg_color_hover=bg_three,
            bg_color_pressed=bg_three,
        )
        combobox_widget.setMinimumHeight(height)
        combobox_widget.setFixedWidth(width[1])
        layout_row.addWidget(combobox_widget)

        return [layout_row, label_widget, combobox_widget]

    def add_toggle(self, layout, height=40, width=None, label=None, font_size=12):
        """
        Add a label and a toggle button to a specified layout.

        :param layout: Layout object to add the label and toggle button to.
        :param height: Height of the label and toggle. Default is 40.
        :param width: Width of the label and toggle. Default is [50, 100, 50] if None.
        :param label: Label text. Default is ['label1', 'label2'] if None.
        :param font_size: Font size for the label text. Default is 12.
        :return: A tuple containing the layout row, label object, toggle object, and second label object
        """

        label = label or ['label1', 'label2']
        width = width or [50, 100, 50]

        layout_row = QHBoxLayout()
        layout.addLayout(layout_row)

        label1 = self._create_label(label[0], font_size, height, width[0])
        layout_row.addWidget(label1)

        toggle = self._create_toggle(width[1], height)
        layout_row.addWidget(toggle)

        label2 = self._create_label(label[1], font_size, height, width[2])
        layout_row.addWidget(label2)

        return layout_row, label1, toggle, label2

    def add_icon_button(self, layout, icon, height=40, width=None, text='lineedit'):
        """
        :param layout: The layout to which the icon button and line edit will be added.
        :param icon: The path to the icon that will be displayed on the button.
        :param height: The height of the icon button and line edit. Default is 40.
        :param width: The width of the icon button. If not provided, it will be set to a default value.
        :param text: The placeholder text for the line edit. Default is 'lineedit'.
        :return: A list containing the layout row object, the button object, and the line edit object.
        """
        if width is None:
            width = [20, 180]

        layout_row_obj = QHBoxLayout()
        layout.addLayout(layout_row_obj)

        button_obj1 = PyIconButton(
            icon_path=icon,
            parent=self,
            app_parent=None,
            tooltip_text=None,
            width=width[0],
            height=height,
            radius=10,
            dark_one=self._get_color_theme("dark_one"),
            icon_color=self._get_color_theme("icon_color"),
            icon_color_hover=self._get_color_theme("icon_hover"),
            icon_color_pressed=self._get_color_theme("icon_active"),
            icon_color_active=self._get_color_theme("icon_active"),
            bg_color=self._get_color_theme("dark_one"),
            bg_color_hover=self._get_color_theme("dark_three"),
            bg_color_pressed=self._get_color_theme("pink")
        )
        button_obj1.setMinimumHeight(height)
        layout_row_obj.addWidget(button_obj1)

        lineedit_obj = PyLineEdit(
            text="",
            place_holder_text=text,
            radius=8,
            border_size=2,
            color=self._get_color_theme("text_foreground"),
            selection_color=self._get_color_theme("white"),
            bg_color=self._get_color_theme("dark_one"),
            bg_color_active=self._get_color_theme("dark_three"),
            context_color=self._get_color_theme("context_color")
        )
        lineedit_obj.setMinimumHeight(height)
        layout_row_obj.addWidget(lineedit_obj)

        lineedit_obj.setFixedWidth(width[1])

        return [layout_row_obj, button_obj1, lineedit_obj]

    def add_n_buttons(self, layout=None, num_buttons=1, height=40, width=[200], text=['button']):

        # some basic error checking, maybe not needed, just do it right
        if not isinstance(width, list):
            width = [width]
        if not isinstance(text, list):
            text = [text]
        if len(text) != num_buttons:
            if len(text) == 0:
                text = ["button"] * num_buttons
            elif len(text) > num_buttons:
                text = text[:num_buttons]
            elif len(text) < num_buttons:  # just reuse the first entry N times
                text = [text[0]] * num_buttons
        if len(width) != num_buttons:
            width = int(200 / num_buttons)  # left menu is about 200 wide

        layout_main_obj = layout
        layout_row_obj = QHBoxLayout()
        layout_main_obj.addLayout(layout_row_obj)

        all_objects = [layout_row_obj]
        for idx in range(num_buttons):
            button_obj = self._add_button(text=text[idx])
            button_obj.setMinimumHeight(height)
            layout_row_obj.addWidget(button_obj)
            button_obj.setFixedWidth(width[idx])
            all_objects.append(button_obj)
        return all_objects

    def toggle_left_column(self):
        """
        Toggles the left column of the CommonWindow by starting a box animation.

        :return: None
        """
        self.start_box_animation("left")

    def toggle_right_column(self):
        """
        Toggles the display of the right column in a common window.

        :return: None
        """
        self.start_box_animation("right")

    def start_box_animation(self, direction):
        """
        :param direction: The direction in which the box animation should be performed. Possible values are "left" and "right".
        :return: None

        This method starts a box animation in the specified direction. The animation involves changing the width of the left and right boxes in a window. The width values for the boxes are retrieved from the "general_settings" module. The animation duration is determined by the "time_animation" variable.

        The method first calculates the minimum and maximum width values for both the left and right boxes. It then retrieves the current width of the left and right boxes from the UI.

        If the direction is "left" and the current width of the left box is equal to the minimum width, the animation will set the width of the left box to the maximum width. Otherwise, the width of the left box will be set to the minimum width.

        Similarly, if the direction is "right" and the current width of the right box is equal to the minimum width, the animation will set the width of the right box to the maximum width. Otherwise, the width of the right box will be set to the minimum width.

        Finally, the method calls the "setup_animation" method to initiate the box animation with the calculated width values and the specified animation duration.
        """
        time_animation = general_settings.time_animation
        minimum_left = general_settings.left_column_size["minimum"]
        maximum_left = general_settings.left_column_size["maximum"]
        minimum_right = general_settings.right_column_size["minimum"]
        maximum_right = general_settings.right_column_size["maximum"]

        left_box_width = self.left_column_frame.width()
        right_box_width = self.right_column_frame.width()

        left_width = maximum_left if left_box_width == minimum_left and direction == "left" else minimum_left
        right_width = maximum_right if right_box_width == minimum_right and direction == "right" else minimum_right

        self.setup_animation(left_box_width, right_box_width, left_width, right_width, time_animation)

    def setup_animation(self, left_start, right_start, left_end, right_end, duration):
        """
        :param left_start: The starting value for the left box animation.
        :param right_start: The starting value for the right box animation.
        :param left_end: The ending value for the left box animation.
        :param right_end: The ending value for the right box animation.
        :param duration: The duration of the animation in milliseconds.
        :return: None

        This method sets up an animation for the left and right columns of the UI. It creates animations for the minimumWidth property of the left and right column frames and adds them to a parallel animation group. The animation group is then started.
        """
        # ANIMATION LEFT BOX
        left_box = self.create_animation(self.left_column_frame, b"minimumWidth", left_start, left_end,
                                         duration)

        # ANIMATION RIGHT BOX
        right_box = self.create_animation(self.right_column_frame, b"minimumWidth", right_start, right_end,
                                          duration)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(left_box)
        self.group.addAnimation(right_box)
        self.group.start()

    def toggle_progress(self):
        """
        Toggles the progress row.

        :return: None
        """
        minimum_progress = general_settings.progress_size["minimum"]
        maximum_progress = general_settings.progress_size["maximum"]
        progress_box_height = self.progress_frame.height()
        self.logger.log("hola")
        from random import randint
        self.progress.__setattr__("progress", randint(0, 100))
        progress_width = maximum_progress if progress_box_height == minimum_progress else minimum_progress
        self.progress_frame.setMaximumHeight(progress_width)

    @staticmethod
    def create_animation(obj, property_name, start_val, end_val, duration):
        """
        Create an animation with specified parameters.

        :param obj: The object on which the animation will be applied.
        :type obj: QObject
        :param property_name: The name of the property to animate.
        :type property_name: str
        :param start_val: The initial value of the property.
        :type start_val: Any
        :param end_val: The final value of the property.
        :type end_val: Any
        :param duration: The duration of the animation in milliseconds.
        :type duration: int
        :return: The created animation.
        :rtype: QPropertyAnimation
        """
        animation = QPropertyAnimation(obj, property_name)
        animation.setDuration(duration)
        animation.setStartValue(start_val)
        animation.setEndValue(end_val)
        animation.setEasingCurve(QEasingCurve.InOutQuart)
        return animation

    def _create_toggle(self, width, height):
        toggle = PyToggle(
            width=width,
            bg_color=self.themes["app_color"]["dark_one"],
            circle_color=self.themes["app_color"]["icon_color"],
            active_color=self.themes["app_color"]["dark_one"]
        )
        toggle.setMaximumHeight(height)
        return toggle

    def _create_label(self, text, font_size, height, width):
        label = PyLabel(
            text=text,
            font_size=font_size,
            color=self.themes["app_color"]["text_foreground"]
        )
        label.setMinimumHeight(height)
        label.setAlignment(Qt.AlignLeft)
        label.setFixedWidth(width)
        return label

    def _get_color_theme(self, color_key):
        return self.themes["app_color"][color_key]

    def _add_button(self, text='button'):
        button_obj = PyPushButton(
            text=text,
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        return button_obj
