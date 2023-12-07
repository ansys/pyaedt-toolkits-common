# TO BE DELETED


from ansys.aedt.toolkits.common.ui.utils.widgets import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import uuid


class AddRows(object):
    def __init__(self, ui):
        self.ui = ui




    # def add_n_buttons(self, layout=None, num_buttons=1, height=40, width=[200], text=['button']):
    #     def add_button(text='button'):
    #         button_obj = PyPushButton(
    #             text=text,
    #             radius=8,
    #             color=self.ui.themes["app_color"]["text_foreground"],
    #             bg_color=self.ui.themes["app_color"]["dark_one"],
    #             bg_color_hover=self.ui.themes["app_color"]["dark_three"],
    #             bg_color_pressed=self.ui.themes["app_color"]["dark_four"]
    #         )
    #         return button_obj
    #
    #     # some basic error checking, maybe not needed, just do it right
    #     if not isinstance(width, list):
    #         width = [width]
    #     if not isinstance(text, list):
    #         text = [text]
    #     if len(text) != num_buttons:
    #         if len(text) == 0:
    #             text = ["button"] * num_buttons
    #         elif len(text) > num_buttons:
    #             text = text[:num_buttons]
    #         elif len(text) < num_buttons:  # just reuse the first entry N times
    #             text = [text[0]] * num_buttons
    #     if len(width) != num_buttons:
    #         width = int(200 / num_buttons)  # left menu is about 200 wide
    #
    #     layout_main_obj = layout
    #     layout_row_obj = QHBoxLayout()
    #     layout_main_obj.addLayout(layout_row_obj)
    #
    #     all_objects = [layout_row_obj]
    #     for idx in range(num_buttons):
    #         button_obj = add_button(text=text[idx])
    #         button_obj.setMinimumHeight(height)
    #         layout_row_obj.addWidget(button_obj)
    #         button_obj.setFixedWidth(width[idx])
    #         all_objects.append(button_obj)
    #     return all_objects
    #

    #
    # def add_label_lineedit(self, layout, height=40, width=[100, 100], label='label1', text='lineedit', font_size=12):
    #
    #     layout_main_obj = layout
    #     layout_row_obj = QHBoxLayout()
    #     layout_main_obj.addLayout(layout_row_obj)
    #     label_obj = PyLabel(
    #         text=label,
    #         font_size=font_size,
    #         color=self.ui.themes["app_color"]["text_foreground"]
    #     )
    #     label_obj.setMinimumHeight(height)
    #     layout_row_obj.addWidget(label_obj)
    #
    #     lineedit_obj = PyLineEdit(
    #         text=text,
    #         place_holder_text="1.0",
    #         radius=8,
    #         border_size=2,
    #         color=self.ui.themes["app_color"]["text_foreground"],
    #         selection_color=self.ui.themes["app_color"]["white"],
    #         bg_color=self.ui.themes["app_color"]["dark_one"],
    #         bg_color_active=self.ui.themes["app_color"]["dark_three"],
    #         context_color=self.ui.themes["app_color"]["context_color"]
    #     )
    #     lineedit_obj.setMinimumHeight(height)
    #     layout_row_obj.addWidget(lineedit_obj)
    #
    #     label_obj.setFixedWidth(width[0])
    #     lineedit_obj.setFixedWidth(width[1])
    #
    #     return [layout_row_obj, label_obj, lineedit_obj]
    #

    #
    # def add_toggle_label_button_button(self, layout, height=40, width=[50, 100, 40, 40], label='label'):
    #
    #     layout_main_obj = layout
    #     layout_row_obj = QHBoxLayout()
    #     layout_main_obj.addLayout(layout_row_obj)
    #
    #     # increment=1
    #     # toggle_name = 'toggle_report_1'
    #     # base_name = 'toggle_report_'
    #     # while hasattr(self, toggle_name):
    #     #     toggle_name = f'{base_name}{increment}'
    #     #     increment += 1
    #
    #     toggle_obj = PyToggle(
    #         width=width[0],
    #         bg_color=self.ui.themes["app_color"]["dark_two"],
    #         circle_color=self.ui.themes["app_color"]["icon_color"],
    #         active_color=self.ui.themes["app_color"]["dark_one"]
    #     )
    #     toggle_obj.setMaximumHeight(height)
    #     layout_row_obj.addWidget(toggle_obj)
    #
    #     label_obj = PyLabel(
    #         text=label,
    #         font_size=20,
    #         color=self.ui.themes["app_color"]["text_foreground"]
    #     )
    #     label_obj.setMinimumHeight(height)
    #     layout_row_obj.addWidget(label_obj)
    #     label_obj.setAlignment(Qt.AlignLeft)
    #
    #     # button_obj1 = PyPushButton(
    #     #     text=button_text[0],
    #     #     radius=8,
    #     #     color=self.ui.themes["app_color"]["text_foreground"],
    #     #     bg_color=self.ui.themes["app_color"]["dark_one"],
    #     #     bg_color_hover=self.ui.themes["app_color"]["dark_three"],
    #     #     bg_color_pressed=self.ui.themes["app_color"]["dark_four"]
    #     # )
    #     button_obj1 = PyIconButton(
    #         icon_path=self.ui.images_load.icon_path("icon_settings.svg"),
    #         parent=self,
    #         app_parent=self.ui.central_widget,
    #         tooltip_text=None,
    #         width=width[2],
    #         height=height,
    #         radius=8,
    #         dark_one=self.ui.themes["app_color"]["dark_one"],
    #         icon_color=self.ui.themes["app_color"]["icon_color"],
    #         icon_color_hover=self.ui.themes["app_color"]["icon_hover"],
    #         icon_color_pressed=self.ui.themes["app_color"]["icon_active"],
    #         icon_color_active=self.ui.themes["app_color"]["icon_active"],
    #         bg_color=self.ui.themes["app_color"]["dark_one"],
    #         bg_color_hover=self.ui.themes["app_color"]["dark_three"],
    #         bg_color_pressed=self.ui.themes["app_color"]["pink"]
    #     )
    #     button_obj1.setMinimumHeight(height)
    #     layout_row_obj.addWidget(button_obj1)
    #
    #     #  = PyIconButton(
    #     #     text=button_text[1],
    #     #     radius=8,
    #     #     color=self.ui.themes["app_color"]["text_foreground"],
    #     #     bg_color=self.ui.themes["app_color"]["dark_one"],
    #     #     bg_color_hover=self.ui.themes["app_color"]["dark_three"],
    #     #     bg_color_pressed=self.ui.themes["app_color"]["dark_four"]
    #     # )
    #     button_obj2 = PyIconButton(
    #         icon_path=self.ui.images_load.icon_path("icon_close.svg"),
    #         parent=self,
    #         app_parent=self.ui.central_widget,
    #         tooltip_text=None,
    #         width=width[3],
    #         height=height,
    #         radius=8,
    #         dark_one=self.ui.themes["app_color"]["dark_one"],
    #         icon_color=self.ui.themes["app_color"]["icon_color"],
    #         icon_color_hover=self.ui.themes["app_color"]["icon_hover"],
    #         icon_color_pressed=self.ui.themes["app_color"]["icon_active"],
    #         icon_color_active=self.ui.themes["app_color"]["icon_active"],
    #         bg_color=self.ui.themes["app_color"]["dark_one"],
    #         bg_color_hover=self.ui.themes["app_color"]["dark_three"],
    #         bg_color_pressed=self.ui.themes["app_color"]["pink"]
    #     )
    #
    #     button_obj2.setMinimumHeight(height)
    #     layout_row_obj.addWidget(button_obj2)
    #
    #     # toggle_name.setFixedWidth(width[0])
    #     label_obj.setFixedWidth(width[1])
    #     button_obj1.setFixedWidth(width[2])
    #     button_obj2.setFixedWidth(width[3])
    #
    #     return layout_row_obj, toggle_obj, label_obj, button_obj1, button_obj2
    #
    # def add_label_toggle(self, layout, height=40, width=[50, 100], label='label', font_size=12):
    #
    #     layout_main_obj = layout
    #     layout_row_obj = QHBoxLayout()
    #     layout_main_obj.addLayout(layout_row_obj)
    #
    #     label_obj = PyLabel(
    #         text=label,
    #         font_size=font_size,
    #         color=self.ui.themes["app_color"]["text_foreground"]
    #     )
    #     label_obj.setMinimumHeight(height)
    #     layout_row_obj.addWidget(label_obj)
    #     label_obj.setAlignment(Qt.AlignLeft)
    #     label_obj.setFixedWidth(width[0])
    #
    #     toggle_obj = PyToggle(
    #         width=width[1],
    #         bg_color=self.ui.themes["app_color"]["dark_two"],
    #         circle_color=self.ui.themes["app_color"]["icon_color"],
    #         active_color=self.ui.themes["app_color"]["dark_one"]
    #     )
    #     toggle_obj.setMaximumHeight(height)
    #     layout_row_obj.addWidget(toggle_obj)
    #
    #     return layout_row_obj, label_obj, toggle_obj
    #

    #
    # def add_label_combobox_button(self, layout,
    #                               height=30,
    #                               width=[100, 50, 50],
    #                               label='label1',
    #                               combobox_list=['1', '2'],
    #                               font_size=12):
    #
    #     layout_main_obj = layout
    #     layout_row_obj = QHBoxLayout()
    #     layout_main_obj.addLayout(layout_row_obj)
    #     label_obj = PyLabel(
    #         text=label,
    #         font_size=font_size,
    #         color=self.ui.themes["app_color"]["text_foreground"]
    #     )
    #     label_obj.setMinimumHeight(height)
    #     layout_row_obj.addWidget(label_obj)
    #
    #     combobox_obj = PyComboBox(
    #         text=combobox_list,
    #         radius=8,
    #         color=self.ui.themes["app_color"]["dark_one"],
    #         bg_color=self.ui.themes["app_color"]["dark_two"],
    #         bg_color_hover=self.ui.themes["app_color"]["bg_three"],
    #         bg_color_pressed=self.ui.themes["app_color"]["bg_three"]
    #     )
    #     combobox_obj.setMinimumHeight(height)
    #     layout_row_obj.addWidget(combobox_obj)
    #
    #     button_obj = PyIconButton(
    #         icon_path=self.ui.images_load.icon_path("icon_close.svg"),
    #         parent=self,
    #         app_parent=self.ui.central_widget,
    #         tooltip_text=None,
    #         width=width[2],
    #         height=height,
    #         radius=8,
    #         dark_one=self.ui.themes["app_color"]["dark_one"],
    #         icon_color=self.ui.themes["app_color"]["icon_color"],
    #         icon_color_hover=self.ui.themes["app_color"]["icon_hover"],
    #         icon_color_pressed=self.ui.themes["app_color"]["icon_active"],
    #         icon_color_active=self.ui.themes["app_color"]["icon_active"],
    #         bg_color=self.ui.themes["app_color"]["dark_one"],
    #         bg_color_hover=self.ui.themes["app_color"]["dark_three"],
    #         bg_color_pressed=self.ui.themes["app_color"]["pink"]
    #     )
    #
    #     button_obj.setMinimumHeight(height)
    #     layout_row_obj.addWidget(button_obj)
    #
    #     label_obj.setFixedWidth(width[0])
    #     combobox_obj.setFixedWidth(width[1])
    #
    #     return [layout_row_obj, label_obj, combobox_obj, button_obj]
    #
    # def add_horizontal_spacer(self, frame, layout):
    #     random_str = str(uuid.uuid4().hex)[:5]
    #     line_name = f"line_{random_str}"
    #     verticalSpacer = QSpacerItem(100, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
    #     line = QFrame(frame)
    #     line.setObjectName(line_name)
    #     line.setFrameShape(QFrame.HLine)
    #     line.setFrameShadow(QFrame.Sunken)
    #     layout.addItem(verticalSpacer)
    #     layout.addWidget(line)
    #     layout.addItem(verticalSpacer)
