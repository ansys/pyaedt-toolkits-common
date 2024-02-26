# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_design_page.ui'
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

class Ui_Plot_Design(object):
    def setupUi(self, Plot_Design):
        if not Plot_Design.objectName():
            Plot_Design.setObjectName(u"Plot_Design")
        Plot_Design.resize(1205, 805)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Plot_Design.sizePolicy().hasHeightForWidth())
        Plot_Design.setSizePolicy(sizePolicy)
        Plot_Design.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Plot_Design)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plot_design_layout = QVBoxLayout()
        self.plot_design_layout.setObjectName(u"plot_design_layout")
        self.plot_design_layout.setContentsMargins(-1, 0, -1, -1)
        self.plot_design_label = QLabel(Plot_Design)
        self.plot_design_label.setObjectName(u"plot_design_label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.plot_design_label.setFont(font)
        self.plot_design_label.setAlignment(Qt.AlignCenter)

        self.plot_design_layout.addWidget(self.plot_design_label)

        self.plot_design_grid = QGridLayout()
        self.plot_design_grid.setObjectName(u"plot_design_grid")
        self.plot_design_grid.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.plot_design_grid.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.plot_design_layout.addLayout(self.plot_design_grid)


        self.verticalLayout_2.addLayout(self.plot_design_layout)


        self.retranslateUi(Plot_Design)

        QMetaObject.connectSlotsByName(Plot_Design)
    # setupUi

    def retranslateUi(self, Plot_Design):
        Plot_Design.setWindowTitle(QCoreApplication.translate("Plot_Design", u"Form", None))
        self.plot_design_label.setText(QCoreApplication.translate("Plot_Design", u"AEDT Design", None))
    # retranslateUi

