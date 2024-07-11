# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help_page.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Help(object):
    def setupUi(self, Help):
        if not Help.objectName():
            Help.setObjectName(u"Help")
        Help.resize(1205, 805)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Help.sizePolicy().hasHeightForWidth())
        Help.setSizePolicy(sizePolicy)
        Help.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Help)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.help_layout = QVBoxLayout()
        self.help_layout.setObjectName(u"help_layout")
        self.help_layout.setContentsMargins(-1, 0, -1, -1)
        self.help_label = QLabel(Help)
        self.help_label.setObjectName(u"help_label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.help_label.setFont(font)
        self.help_label.setAlignment(Qt.AlignCenter)

        self.help_layout.addWidget(self.help_label)

        self.help_grid = QGridLayout()
        self.help_grid.setObjectName(u"help_grid")
        self.help_grid.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.help_grid.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.help_layout.addLayout(self.help_grid)


        self.verticalLayout_2.addLayout(self.help_layout)


        self.retranslateUi(Help)

        QMetaObject.connectSlotsByName(Help)
    # setupUi

    def retranslateUi(self, Help):
        Help.setWindowTitle(QCoreApplication.translate("Help", u"Form", None))
        self.help_label.setText(QCoreApplication.translate("Help", u"AEDT Design", None))
    # retranslateUi

