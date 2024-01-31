class Styles(object):
    style = """
    QPushButton {{
    border: none;
    padding-left: 10px;
    padding-right: 5px;
    color: {_color};
    border-radius: {_radius};
    background-color: {_bg_color};
    font-size: {_font_size}pt;
    }}
    QPushButton:hover {{
    background-color: {_bg_color_hover};
    }}
    QPushButton:pressed {{
    background-color: {_bg_color_pressed};
    }}
    """
