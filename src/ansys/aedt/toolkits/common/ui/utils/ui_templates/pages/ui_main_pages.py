# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pages.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLayout,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(1053, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainPages.sizePolicy().hasHeightForWidth())
        MainPages.setSizePolicy(sizePolicy)
        MainPages.setMaximumSize(QSize(16777212, 16777215))
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.home_page.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.home_page)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.welcome_base = QVBoxLayout()
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.logo = QFrame(self.home_page)
        self.logo.setObjectName(u"logo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setMinimumSize(QSize(400, 200))
        self.logo.setMaximumSize(QSize(400, 200))
        self.logo.setLayoutDirection(Qt.LeftToRight)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(6)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.welcome_base.addWidget(self.logo, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label = QLabel(self.home_page)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(500, 0))
        self.label.setMaximumSize(QSize(1000, 16777215))
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.welcome_base.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.page_1_layout.addLayout(self.welcome_base)

        self.pages.addWidget(self.home_page)
        self.empty_page = QWidget()
        self.empty_page.setObjectName(u"empty_page")
        self.empty_page.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.modeler_page_layout = QVBoxLayout(self.empty_page)
        self.modeler_page_layout.setObjectName(u"modeler_page_layout")
        self.modeler_window_layout = QVBoxLayout()
        self.modeler_window_layout.setSpacing(0)
        self.modeler_window_layout.setObjectName(u"modeler_window_layout")

        self.modeler_page_layout.addLayout(self.modeler_window_layout)

        self.pages.addWidget(self.empty_page)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Welcome to the toolkit", None))
    # retranslateUi

