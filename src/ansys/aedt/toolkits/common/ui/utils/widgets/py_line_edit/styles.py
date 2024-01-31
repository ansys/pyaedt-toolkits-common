class Styles(object):
    style = """
    QLineEdit {{
    background-color: {_bg_color};
    border-radius: {_radius}px;
    border: {_border_size}px solid transparent;
    padding-left: 10px;
    padding-right: 10px;
    selection-color: {_selection_color};
    selection-background-color: {_context_color};
    color: {_color};
    }}
    QLineEdit:focus {{
    border: {_border_size}px solid {_context_color};
    background-color: {_bg_color_active};
    }}
    """
