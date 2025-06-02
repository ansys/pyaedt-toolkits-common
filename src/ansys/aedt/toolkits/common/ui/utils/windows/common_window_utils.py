# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QParallelAnimationGroup
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QWidgetItem

from ansys.aedt.toolkits.common.ui.models import general_settings
from ansys.aedt.toolkits.common.ui.utils.widgets import PyComboBox
from ansys.aedt.toolkits.common.ui.utils.widgets import PyIconButton
from ansys.aedt.toolkits.common.ui.utils.widgets import PyLabel
from ansys.aedt.toolkits.common.ui.utils.widgets import PyLineEdit
from ansys.aedt.toolkits.common.ui.utils.widgets import PyPushButton
from ansys.aedt.toolkits.common.ui.utils.widgets import PyToggle


class CommonWindowUtils(object):
    """
    Class representing a common window with various UI functionalities.
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
        self.__resize = 1

    def set_page(self, page):
        """
        Set the current page in the load_pages widget.

        Parameters
        ----------
        page : QWidget
            The page widget to be displayed as the current page.
        """
        self.load_pages.pages.setCurrentWidget(page)
        self.window_refresh()

    def get_left_menu(self, object_name):
        """
        Retrieves the QPushButton object in the left menu of the CommonWindow UI.

        Parameters
        ----------
        object_name : str
            The name of the button object to be retrieved from the left menu.

        Returns
        -------
        QPushButton
            The QPushButton object with the given object_name found in the left menu of the CommonWindow UI.
        """
        return self.left_menu.findChild(QPushButton, object_name)

    def set_left_column_menu(self, menu, title, icon_path):
        """
        Configures the left column of the CommonWindow UI by setting the current widget as the provided `menu`,
         the title in the left column's title label as the provided `title`,
          and the icon in the left column as the icon specified by `icon_path`.

        Parameters
        ----------
        menu : QWidget
            The menu widget to be set as the current widget in the left column.
        title : str
            The title to be set in the left column's title label.
        icon_path : str
            The path to the icon image file to be set in the left column's icon.
        """
        self.left_column.menus.menus.setCurrentWidget(menu)
        self.left_column.title_label.setText(title)
        self.left_column.icon.set_icon(icon_path)

    def is_left_column_visible(self):
        """
        Check if the left column is visible.

        Returns
        -------
        bool
            ``True`` if the left column is visible, ``False`` otherwise.
        """
        return self.left_column_frame.width() != 0

    def is_right_column_visible(self):
        """
        Checks if the right column is visible.

        Returns
        -------
        bool
            ``True`` if the right column is visible, ``False`` otherwise.
        """
        return self.right_column_frame.width() != 0

    def is_progress_visible(self):
        """
        Checks if the progress bar is visible.

        Returns
        -------
        bool
            ``True`` if the progress bar is visible, ``False`` otherwise.
        """
        return self.progress_frame.height() != 0

    def set_right_column_menu(self, title):
        """
        Sets the title of the right column menu.

        Parameters
        ----------
        title: str
            The title to be set.
        """
        self.right_column.title_label.setText(title)

    def get_title_bar(self, object_name):
        """
        Get title.

        Parameters
        ----------
        object_name: str
            The name of the QPushButton object.

        """
        return self.title_bar_frame.findChild(QPushButton, object_name)

    def add_combobox(self, layout, height=40, width=None, label="label1", combobox_list=None, font_size=12):
        """
        Adds a label and combobox to a layout.

        Parameters
        ----------
        layout: QLayout
            The layout object to which the label and combobox will be added.
        height: int, optional
            The height of the label and combobox widgets. Default is 40.
        width: list, optional
            The width of the label and combobox widgets. If not provided, a default width of [100, 100] will be used.
        label: str, optional
            The text to be displayed on the label widget. Default is 'label1'.
        combobox_list: list, optional
            A list of items to be displayed in the combobox. If not provided, a default list of ['1', '2'] will be used.
        font_size: int, optional
            The font size of the label widget. Default is 12.

        Returns
        -------
        list
            A list containing the layout row object, label object, and combobox object.
        """
        combobox_list = combobox_list or []
        width = width or [100, 100]

        app_color = self.themes["app_color"]
        text_foreground = app_color["text_foreground"]
        combo_color = app_color["combo_color"]
        combo_hover = app_color["combo_hover"]

        layout_row = QHBoxLayout()
        layout.addLayout(layout_row)

        label_widget = self._create_label(
            text=label, font_size=font_size, height=height, width=width[0], color=text_foreground
        )
        # Label aligned to the left
        label_widget.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout_row.addWidget(label_widget)

        combobox_widget = PyComboBox(
            text_list=combobox_list,
            radius=8,
            bg_color=combo_color,
            bg_color_hover=combo_hover,
            text_color=text_foreground,
            font_size=font_size,
        )
        combobox_widget.setMinimumHeight(height)
        combobox_widget.setFixedWidth(width[1])

        # Box aligned to the right
        layout_row.addWidget(combobox_widget, alignment=Qt.AlignVCenter | Qt.AlignRight)

        return [layout_row, label_widget, combobox_widget]

    def add_textbox(self, layout, height=40, width=None, label="label1", initial_text=None, font_size=12):
        """
        Adds a label and textbox to a layout.

        Parameters
        ----------
        layout: QLayout
            The layout object to which the label and combobox will be added.
        height: int, optional
            The height of the label and combobox widgets. The default is `40`.
        width: list, optional
            The width of the label and combobox widgets. If not provided, a default width of `[100, 100]` will be used.
        label: str, optional
            The text to be displayed on the label widget. The default is '"label1"'.
        initial_text: str, optional
            Text to be displayed in the textbox.
        font_size: int, optional
            The font size of the label widget. The default is `12`.

        Returns
        -------
        list
            A list containing the layout row object, label object, and combobox object.
        """
        initial_text = initial_text or " "
        width = width or [100, 100]

        app_color = self.themes["app_color"]
        text_foreground = app_color["text_foreground"]
        bg_color = app_color["combo_color"]

        layout_row = QHBoxLayout()
        layout.addLayout(layout_row)

        label_widget = self._create_label(label, font_size, height, width[0])
        label_widget.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout_row.addWidget(label_widget)

        linebox_widget = PyLineEdit(
            text=initial_text,
            radius=8,
            bg_color=bg_color,
            color=text_foreground,
            selection_color=app_color["white"],
            bg_color_active=app_color["dark_three"],
            context_color=app_color["context_color"],
            font_size=font_size,
        )
        linebox_widget.setMinimumHeight(height)
        linebox_widget.setFixedWidth(width[1])
        layout_row.addWidget(linebox_widget, alignment=Qt.AlignVCenter | Qt.AlignRight)

        return [layout_row, label_widget, linebox_widget]

    def add_toggle(
        self,
        layout,
        height=40,
        width=None,
        label=None,
        font_size=12,
        bg_color=None,
        circle_color=None,
        active_color=None,
        text_color_on=None,
        text_color_off=None,
        show_on_off=False,
    ):
        """
        Add a label and a toggle button to a specified layout.

        Parameters
        ----------
        layout: QLayout
            Layout object to add the label and toggle button to.
        height: int, optional
            Height of the label and toggle. The default value is ``40``.
        width: list, optional
            Width of the label and toggle. The default is [50, 100, 50] if ``None``.
        label: list of str, optional
            Label text. The default value is ``['label1', 'label2']``.
        font_size: int, optional
            Font size for the label text. The default value is ``12``.
        bg_color : str, optional
            Background color of the toggle switch. The default is ``label_off``.
        circle_color : str, optional
            Color of the circle in the toggle switch. The default is ``icon_color``.
        active_color : str, optional
            Color of the toggle switch when active. The default is ``label_on``.
        text_color_on : str, optional
            Color of the on toggle text. The default is ``text_foreground``.
        text_color_off : str, optional
            Color of the off toggle text. The default is ``text_foreground``.
        show_on_off: bool, optional
            Show on and off text in the toggle. The default value is ``False``.

        Returns
        -------
        tuple
            A tuple containing the layout row, label object, toggle object, and second label object
        """

        label = label or ["label1", "label2"]
        width = width or [50, 100, 50]

        if not bg_color:
            bg_color = self.themes["app_color"]["label_off"]
        if not circle_color:
            circle_color = self.themes["app_color"]["icon_color"]
        if not active_color:
            active_color = self.themes["app_color"]["label_on"]
        if not text_color_on:
            text_color_on = self.themes["app_color"]["text_foreground"]
        if not text_color_off:
            text_color_off = self.themes["app_color"]["text_foreground"]

        main_row = QHBoxLayout()
        layout.addLayout(main_row)

        # Left container
        left_container = QHBoxLayout()
        label1 = self._create_label(label[0], font_size, height, width[0])
        label1.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        left_container.addWidget(label1)
        left_container.addStretch()
        main_row.addLayout(left_container)

        # Central contained
        toggle_container = QHBoxLayout()

        toggle = self._create_toggle(
            width[1],
            height,
            bg_color=bg_color,
            circle_color=circle_color,
            active_color=active_color,
            show_on_off=show_on_off,
            text_color_on=text_color_on,
            text_color_off=text_color_off,
        )

        if width[2] != 0:
            # If label2, toggle centered
            toggle_container.addStretch()
            toggle_container.addWidget(toggle, alignment=Qt.AlignVCenter)
            toggle_container.addStretch()

            # Right container
            right_container = QHBoxLayout()
            right_container.addStretch()
            label2 = self._create_label(label[1], font_size, height, width[2])
            label2.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            right_container.addWidget(label2)
            main_row.addLayout(toggle_container)
            main_row.addLayout(right_container)
        else:
            # If no label2, toggle in the right
            toggle_container.addStretch()
            toggle_container.addWidget(toggle, alignment=Qt.AlignVCenter | Qt.AlignRight)
            label2 = None
            main_row.addLayout(toggle_container)

        return main_row, label1, toggle, label2

    def add_icon_button(self, layout, icon, height=40, width=None, text="lineedit"):
        """
        Add icon button.

        Parameters
        ----------
        layout: QLayout
            The layout to which the icon button and line edit will be added.
        icon: QIcon
            The path to the icon that will be displayed on the button.
        height: int, optional
            The height of the icon button and line edit. Default is 40.
        width: list, optional
            The width of the icon button. If not provided, it will be set to a default value.
        text: str, optional
            The placeholder text for the line edit. Default is 'lineedit'.

        Returns
        -------
        list
            A list containing the layout row object, the button object, and the line edit object.
        """
        if width is None:
            width = [20, 180]

        layout_row_obj = QHBoxLayout()
        layout.addLayout(layout_row_obj)

        button_obj1 = PyIconButton(
            icon_path=icon,
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
            bg_color_pressed=self._get_color_theme("pink"),
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
            context_color=self._get_color_theme("context_color"),
        )
        lineedit_obj.setMinimumHeight(height)
        layout_row_obj.addWidget(lineedit_obj)

        lineedit_obj.setFixedWidth(width[1])

        return [layout_row_obj, button_obj1, lineedit_obj]

    def add_n_buttons(self, layout=None, num_buttons=1, height=40, width=[200], text=["button"], font_size=10):
        """
        Add a specified number of buttons to a layout object.

        Parameters
        ----------
        layout: QLayout, optional
            The layout to which the buttons will be added. If None, a new QHBoxLayout will be created.
        num_buttons: int, optional
            The number of buttons to be added to the layout. Default is 1.
        height: int, optional
            The height of the buttons. Default is 40.
        width: list of int, optional
            The widths of the buttons. If list length is less than num_buttons, all buttons take the same width.
            Default is [200].
        text: list of str, optional
            The texts to be displayed on the buttons.
            If list length is less than num_buttons, all buttons display the same text.
            Default is ['button'].
        font_size: float or int, optional
            Font size. Default is ``10``.

        Returns
        -------
        list
             A list containing the layout row object and the button objects.
        """

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
            button_obj = self._add_button(text=text[idx], font_size=font_size)
            button_obj.setMinimumHeight(height)
            layout_row_obj.addWidget(button_obj)
            button_obj.setFixedWidth(width[idx])
            all_objects.append(button_obj)
            layout_row_obj.setAlignment(Qt.AlignCenter)

        return all_objects

    def add_vertical_line(self, layout, top_spacer=None, bot_spacer=None):
        """
        Add a vertical line.

        Parameters
        ----------
        layout: QLayout
            Layout object to add the label and toggle button to.
        top_spacer: list, optional
            Top spacer. Default is [0, 10].
        bot_spacer: list, optional
            Bottom, spacer. Default is [0, 10].
        """

        top_spacer = top_spacer or [0, 10]
        bot_spacer = bot_spacer or [0, 10]

        spacer = QSpacerItem(top_spacer[0], top_spacer[1], QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout.addItem(spacer)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: {};".format(self.themes["app_color"]["dark_two"]))
        layout.addWidget(line)
        spacer = QSpacerItem(bot_spacer[0], bot_spacer[1], QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout.addItem(spacer)

        return line

    def toggle_left_column(self):
        """
        Toggles the left column of the CommonWindow by starting a box animation.
        """
        self.start_box_animation("left")

    def toggle_right_column(self):
        """
        Toggles the display of the right column in a common window.
        """
        self.start_box_animation("right")

    def window_refresh(self):
        """Window refresh"""
        # Store the original size
        original_size = self.app.size()

        if self.__resize == 1:
            self.__resize = -1
        else:
            self.__resize = 1

        # Change the size slightly to trigger a repaint
        self.app.resize(original_size.width() + self.__resize, original_size.height())

        # Restore the original size
        self.app.resize(original_size)

    def start_box_animation(self, direction):
        """
        Starts a box animation in the specified direction.

        Parameters
        ----------
        direction: str
            The direction in which the box animation should be performed.
            Possible values are "left" and "right".

        """
        minimum_left = general_settings.left_column_size["minimum"]
        maximum_left = general_settings.left_column_size["maximum"]
        minimum_right = general_settings.right_column_size["minimum"]
        maximum_right = general_settings.right_column_size["maximum"]

        left_box_width = self.left_column_frame.width()
        right_box_width = self.right_column_frame.width()

        left_width = maximum_left if left_box_width == minimum_left and direction == "left" else minimum_left
        right_width = maximum_right if right_box_width == minimum_right and direction == "right" else minimum_right

        self.setup_animation(left_box_width, right_box_width, left_width, right_width)

    def setup_animation(self, left_start, right_start, left_end, right_end):
        """
        Sets up an animation for the left and right columns of the UI.

        Parameters
        ----------
        left_start: int
            The starting value for the left box animation.
        right_start: int
            The starting value for the right box animation.
        left_end: int
            The ending value for the left box animation.
        right_end: int
            The ending value for the right box animation.
        """
        # ANIMATION LEFT BOX
        left_box = self.create_animation(self.left_column_frame, b"minimumWidth", left_start, left_end)

        # ANIMATION RIGHT BOX
        right_box = self.create_animation(self.right_column_frame, b"minimumWidth", right_start, right_end)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(left_box)
        self.group.addAnimation(right_box)
        self.group.start()

    def toggle_progress(self, mode=0):
        """
        Toggles the visibility of the progress row.

        Parameters
        ----------
        mode : int, optional
            The mode of the toggle operation. Default is 0.
            - 0: Toggles the progress row between open and closed states.
            - 1: Opens the progress row.
            - 2: Closes the progress row.
        """
        minimum_progress = general_settings.progress_size["minimum"]
        maximum_progress = general_settings.progress_size["maximum"]
        if mode == 0:
            progress_box_height = self.progress_frame.height()
            progress_width = maximum_progress if progress_box_height == minimum_progress else minimum_progress
            self.progress_frame.setMaximumHeight(progress_width)
        elif mode == 1:
            self.progress_frame.setMaximumHeight(maximum_progress)
        else:
            self.progress_frame.setMaximumHeight(minimum_progress)

    def clear_layout(self, layout):
        """Clear all layout."""
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                item.widget().close()
            elif isinstance(item, QSpacerItem):
                pass
                # no need to do extra stuff
            else:
                self.clear_layout(item.layout())

            # remove the item from layout
            layout.removeItem(item)

    def update_progress(self, progress_value):
        """Clear all layout."""
        self.progress.progress = progress_value

    def update_logger(self, text):
        """Clear all layout."""
        self.logger.log(text)

    @staticmethod
    def item_index(layout, item):
        """
        Item index.
        """
        try:
            for i in range(layout.count()):
                if layout.itemAt(i) == item:
                    return i
                elif layout.itemAt(i).widget() == item:
                    return i
            return -1
        except:
            return -1

    @staticmethod
    def remove_item(layout, index):
        """
        Remove item by index.
        """
        item = layout.itemAt(index)
        if item:
            widget = item.widget()
            if widget:
                layout.removeWidget(widget)
                widget.deleteLater()
            else:
                layout.removeItem(item)
        layout.update()

    @staticmethod
    def create_animation(obj, property_name, start_val, end_val):
        """
        Creates an animation with specified parameters.

        Parameters
        ----------
        obj: QObject
            The object on which the animation will be applied.
        property_name: str
            The name of the property to animate.
        start_val: Any
            The initial value of the property.
        end_val: Any
            The final value of the property.

        Returns
        -------
        QPropertyAnimation
            The created animation.
        """
        animation = QPropertyAnimation(obj, property_name)
        animation.setStartValue(start_val)
        animation.setEndValue(end_val)
        animation.setEasingCurve(QEasingCurve.InOutQuart)
        return animation

    def _create_toggle(
        self,
        width,
        height,
        bg_color=None,
        circle_color=None,
        active_color=None,
        text_color_on=None,
        text_color_off=None,
        show_on_off=False,
    ):

        if not bg_color:
            bg_color = self.themes["app_color"]["label_off"]
        if not circle_color:
            circle_color = self.themes["app_color"]["icon_color"]
        if not active_color:
            active_color = self.themes["app_color"]["label_off"]
        if not text_color_on:
            text_color_on = self.themes["app_color"]["text_foreground"]
        if not text_color_off:
            text_color_off = self.themes["app_color"]["text_foreground"]

        toggle = PyToggle(
            width=width,
            bg_color=bg_color,
            circle_color=circle_color,
            active_color=active_color,
            text_color_on=text_color_on,
            text_color_off=text_color_off,
            show_on_off=show_on_off,
        )
        toggle.setMaximumHeight(height)
        return toggle

    def _create_label(self, text, font_size, height, width, color=None):
        if color is None:
            color = self.themes["app_color"]["text_foreground"]
        label = PyLabel(text=text, font_size=font_size, color=color)
        label.setMinimumHeight(height)
        label.setAlignment(Qt.AlignLeft)
        label.setFixedWidth(width)
        return label

    def _get_color_theme(self, color_key):
        return self.themes["app_color"][color_key]

    def _add_button(self, text="button", font_size=10):
        button_obj = PyPushButton(
            text=text,
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=font_size,
        )
        return button_obj
