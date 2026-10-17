# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'right_column.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_RightColumn(object):
    def setupUi(self, RightColumn):
        if not RightColumn.objectName():
            RightColumn.setObjectName(u"RightColumn")
        RightColumn.resize(240, 600)
        self.verticalLayout = QVBoxLayout(RightColumn)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.menus = QStackedWidget(RightColumn)
        self.menus.setObjectName(u"menus")
        self.menu_settings = QWidget()
        self.menu_settings.setObjectName(u"menu_settings")
        self.menu_settings_layout = QVBoxLayout(self.menu_settings)
        self.menu_settings_layout.setSpacing(5)
        self.menu_settings_layout.setObjectName(u"menu_settings_layout")
        self.menu_settings_layout.setContentsMargins(5, 5, 5, 5)
        self.settings_vertical_layout = QVBoxLayout()
        self.settings_vertical_layout.setObjectName(u"settings_vertical_layout")

        self.menu_settings_layout.addLayout(self.settings_vertical_layout)

        self.verticalSpacer_a = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.menu_settings_layout.addItem(self.verticalSpacer_a)

        self.menus.addWidget(self.menu_settings)

        self.verticalLayout.addWidget(self.menus)


        self.retranslateUi(RightColumn)

        self.menus.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RightColumn)
    # setupUi

    def retranslateUi(self, RightColumn):
        RightColumn.setWindowTitle(QCoreApplication.translate("RightColumn", u"Form", None))
    # retranslateUi

