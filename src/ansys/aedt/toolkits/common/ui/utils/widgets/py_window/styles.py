class Styles(object):
    bg_style = """
    #pod_bg_app {{
        background-color: {_bg_color};
        border-radius: {_border_radius};
        border: {_border_size}px solid {_border_color};
    }}
    QFrame {{
        color: {_text_color};
        font: {_text_font};
    }}
    """
