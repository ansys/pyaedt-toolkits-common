class Styles(object):
    bg_style = """
    QComboBox {{
        border: none;
        padding: 10px;
        color: {_color};
        border-radius: {_radius};
        background-color: {_bg_color};
        selection-background-color: {_bg_color};
    }}
    QComboBox:editable {{
        background: black;
    }}
    QComboBox:!editable, QComboBox::drop-down:editable {{
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                     stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                     stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    }}
    /* QComboBox gets the "on" state when the popup is open */
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {{
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                    stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
    }}
    QComboBox:on {{ /* shift the text when the popup opens */
        padding-top: 3px;
        padding-left: 4px;
    }}
    QComboBox:drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        color: {_color};
        border-left-width: 1px;
        border-left-color: grey;
        border-left-style: solid; /* just a single line */
        border-top-right-radius: 3px; /* same radius as the QComboBox */
        border-bottom-right-radius: 3px;
    }}
    QComboBox::down-arrow:on {{ /* shift the arrow when popup is open */
        top: 1px;
        left: 1px;
    }}
    QComboBox QAbstractItemView {{
        border: none;
        background-color: {_bg_color};
        color: black;
        border-top-right-radius: 3px; /* same radius as the QComboBox */
        border-top-left-radius: 3px; /* same radius as the QComboBox */
        border-bottom-right-radius: 3px; /* same radius as the QComboBox */
        border-bottom-left-radius: 3px; /* same radius as the QComboBox */
    }}
    QComboBox::item {{
        padding-left: 0.5em;
        height: 2em;
    }}
    QComboBox::item:selected {{
        color: {_bg_color_pressed};
        background-color: transparent;
    }}
    QComboBox::indicator {{
        color: transparent;
        background-color: transparent;
        selection-color: transparent;
        selection-background-color: transparent;
    }}
    """
