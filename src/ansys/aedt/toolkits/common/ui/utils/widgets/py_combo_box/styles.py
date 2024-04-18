class Styles(object):
    bg_style = """
    QComboBox {{
        border: 1px solid {_bg_color};
        border-radius: {_border_radius}px;
        background-color: {_bg_color};
        color: {_text_color};
        padding: 5px;
        font-size: {_font_size}pt;
    }}
    QComboBox::down-arrow {{
        top: 1px;
        left: 1px;
    }}
    QListView {{
        color: {_text_color};
        background-color: {_bg_color};
    }}"
    QComboBox:hover {{
        background-color: {_bg_color_hover};
    }}
    QComboBox:on {{
        padding-top: 3px;
        padding-left: 4px;
    }}
    """
