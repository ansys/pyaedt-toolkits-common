class Styles(object):
    style = """
    /* HORIZONTAL */
    QSlider {{ margin: {_margin}px; }}
    QSlider::groove:horizontal {{
        border-radius: {_bg_radius}px;
        height: {_bg_size}px;
        margin: 0px;
        background-color: {_bg_color};
    }}
    QSlider::groove:horizontal:hover {{ background-color: {_bg_color_hover}; }}
    QSlider::handle:horizontal {{
        border: none;
        height: {_handle_size}px;
        width: {_handle_size}px;
        margin: {_handle_margin}px;
        border-radius: {_handle_radius}px;
        background-color: {_handle_color};
    }}
    QSlider::handle:horizontal:hover {{ background-color: {_handle_color_hover}; }}
    QSlider::handle:horizontal:pressed {{ background-color: {_handle_color_pressed}; }}

    /* VERTICAL */
    QSlider::groove:vertical {{
        border-radius: {_bg_radius}px;
        width: {_bg_size}px;
        margin: 0px;
        background-color: {_bg_color};
    }}
    QSlider::groove:vertical:hover {{ background-color: {_bg_color_hover}; }}
    QSlider::handle:vertical {{
        border: none;
        height: {_handle_size}px;
        width: {_handle_size}px;
        margin: {_handle_margin}px;
        border-radius: {_handle_radius}px;
        background-color: {_handle_color};
    }}
    QSlider::handle:vertical:hover {{ background-color: {_handle_color_hover}; }}
    QSlider::handle:vertical:pressed {{ background-color: {_handle_color_pressed}; }}
    """
