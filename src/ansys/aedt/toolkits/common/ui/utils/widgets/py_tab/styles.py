class Styles(object):
    style = """
    QTabWidget::pane {{
      border: 1px solid #21252d;
      top:-1px;
      background: {_color};
    }}
    QTabBar::tab {{
      background: {_unselected_color};
      border: 1px solid #21252d;
      border-top-left-radius: 7px;
      border-top-right-radius: 7px;
      padding: 5px;
      color: {_text_color};
    }}

    QTabBar::tab:selected {{
      background: {_selected_color};
      margin-bottom: -1px;
    }}
    """
