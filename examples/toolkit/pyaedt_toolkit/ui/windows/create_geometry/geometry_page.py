# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'geometry_page.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Geometry(object):
    def setupUi(self, Geometry):
        if not Geometry.objectName():
            Geometry.setObjectName(u"Geometry")
        Geometry.resize(605, 442)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Geometry.sizePolicy().hasHeightForWidth())
        Geometry.setSizePolicy(sizePolicy)
        Geometry.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Geometry)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.dimension_multiplier_label = QLabel(Geometry)
        self.dimension_multiplier_label.setObjectName(u"dimension_multiplier_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dimension_multiplier_label.sizePolicy().hasHeightForWidth())
        self.dimension_multiplier_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.dimension_multiplier_label.setFont(font)
        self.dimension_multiplier_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.dimension_multiplier_label)

        self.line = QFrame(Geometry)
        self.line.setObjectName(u"line")
        sizePolicy1.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy1)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(255, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(255, 63, 63, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(127, 0, 0, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(170, 0, 0, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush6 = QBrush(QColor(255, 255, 255, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush6)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush2)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush8 = QBrush(QColor(0, 0, 0, 127))
        brush8.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush8)
#endif
        palette.setBrush(QPalette.Active, QPalette.Accent, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush8)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.Accent, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        brush9 = QBrush(QColor(127, 0, 0, 127))
        brush9.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush9)
#endif
        brush10 = QBrush(QColor(255, 76, 76, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Accent, brush10)
        self.line.setPalette(palette)
        self.line.setFrameShadow(QFrame.Raised)
        self.line.setLineWidth(2)
        self.line.setMidLineWidth(5)
        self.line.setFrameShape(QFrame.HLine)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 15, -1, 15)
        self.multiplier_label = QLabel(Geometry)
        self.multiplier_label.setObjectName(u"multiplier_label")
        sizePolicy.setHeightForWidth(self.multiplier_label.sizePolicy().hasHeightForWidth())
        self.multiplier_label.setSizePolicy(sizePolicy)
        self.multiplier_label.setFrameShape(QFrame.StyledPanel)
        self.multiplier_label.setFrameShadow(QFrame.Raised)
        self.multiplier_label.setLineWidth(5)
        self.multiplier_label.setMidLineWidth(2)

        self.horizontalLayout.addWidget(self.multiplier_label)

        self.line_4 = QFrame(Geometry)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.multiplier = QLineEdit(Geometry)
        self.multiplier.setObjectName(u"multiplier")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.multiplier.sizePolicy().hasHeightForWidth())
        self.multiplier.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.multiplier)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.select_geometry_label = QLabel(Geometry)
        self.select_geometry_label.setObjectName(u"select_geometry_label")
        self.select_geometry_label.setFont(font)
        self.select_geometry_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.select_geometry_label)

        self.line_2 = QFrame(Geometry)
        self.line_2.setObjectName(u"line_2")
        sizePolicy1.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy1)
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Light, brush2)
        palette1.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Dark, brush4)
        palette1.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.BrightText, brush6)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush6)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Active, QPalette.AlternateBase, brush2)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush8)
#endif
        palette1.setBrush(QPalette.Active, QPalette.Accent, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette1.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.BrightText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush8)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.Accent, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.BrightText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush9)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.Accent, brush10)
        self.line_2.setPalette(palette1)
        font1 = QFont()
        font1.setKerning(True)
        self.line_2.setFont(font1)
        self.line_2.setFrameShadow(QFrame.Raised)
        self.line_2.setLineWidth(1)
        self.line_2.setMidLineWidth(5)
        self.line_2.setFrameShape(QFrame.HLine)

        self.verticalLayout_2.addWidget(self.line_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 15, 0, 15)
        self.geometry_label = QLabel(Geometry)
        self.geometry_label.setObjectName(u"geometry_label")
        self.geometry_label.setFrameShape(QFrame.StyledPanel)

        self.horizontalLayout_2.addWidget(self.geometry_label)

        self.line_3 = QFrame(Geometry)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.geometry_combo = QComboBox(Geometry)
        self.geometry_combo.addItem("")
        self.geometry_combo.addItem("")
        self.geometry_combo.setObjectName(u"geometry_combo")

        self.horizontalLayout_2.addWidget(self.geometry_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.geometry_plot_layout = QVBoxLayout()
        self.geometry_plot_layout.setObjectName(u"geometry_plot_layout")
        self.geometry_plot_layout.setContentsMargins(-1, 0, -1, -1)

        self.verticalLayout_2.addLayout(self.geometry_plot_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.create_geometry_button = QPushButton(Geometry)
        self.create_geometry_button.setObjectName(u"create_geometry_button")
        self.create_geometry_button.setFlat(False)

        self.verticalLayout_2.addWidget(self.create_geometry_button)


        self.retranslateUi(Geometry)

        self.create_geometry_button.setDefault(True)


        QMetaObject.connectSlotsByName(Geometry)
    # setupUi

    def retranslateUi(self, Geometry):
        Geometry.setWindowTitle(QCoreApplication.translate("Geometry", u"Form", None))
        self.dimension_multiplier_label.setText(QCoreApplication.translate("Geometry", u"Dimension multiplier", None))
        self.multiplier_label.setText(QCoreApplication.translate("Geometry", u"Value", None))
        self.multiplier.setText(QCoreApplication.translate("Geometry", u"1", None))
        self.select_geometry_label.setText(QCoreApplication.translate("Geometry", u"Select geometry", None))
        self.geometry_label.setText(QCoreApplication.translate("Geometry", u"Geometry", None))
        self.geometry_combo.setItemText(0, QCoreApplication.translate("Geometry", u"Box", None))
        self.geometry_combo.setItemText(1, QCoreApplication.translate("Geometry", u"Cylinder", None))

        self.create_geometry_button.setText(QCoreApplication.translate("Geometry", u"Create geometry", None))
    # retranslateUi

