# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_main_window(object):
    def setupUi(self, main_window):
        if main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1200, 800)
        main_window.setMinimumSize(QSize(1200, 800))
        self.action_connect_to_PatchStorage = QAction(main_window)
        self.action_connect_to_PatchStorage.setObjectName(u"action_connect_to_PatchStorage")
        self.action_update_files = QAction(main_window)
        self.action_update_files.setObjectName(u"action_update_files")
        self.action_upload_file = QAction(main_window)
        self.action_upload_file.setObjectName(u"action_upload_file")
        self.action_quit = QAction(main_window)
        self.action_quit.setObjectName(u"action_quit")
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(600, 0))
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.groupBox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(600, 0))
        self.ps_tab = QWidget()
        self.ps_tab.setObjectName(u"ps_tab")
        self.gridLayout_2 = QGridLayout(self.ps_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ps_filter_text = QLineEdit(self.ps_tab)
        self.ps_filter_text.setObjectName(u"ps_filter_text")

        self.gridLayout_2.addWidget(self.ps_filter_text, 0, 1, 1, 1)

        self.ps_filter_refresh = QPushButton(self.ps_tab)
        self.ps_filter_refresh.setObjectName(u"ps_filter_refresh")
        icon = QIcon()
        icon.addFile(u"resources/64w/Asset 2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ps_filter_refresh.setIcon(icon)
        self.ps_filter_refresh.setIconSize(QSize(27, 24))
        self.ps_filter_refresh.setFlat(False)

        self.gridLayout_2.addWidget(self.ps_filter_refresh, 0, 2, 1, 1)

        self.ps_tableview = QTableView(self.ps_tab)
        self.ps_tableview.setObjectName(u"ps_tableview")
        self.ps_tableview.setShowGrid(False)
        self.ps_tableview.verticalHeader().setVisible(False)
        self.ps_tableview.verticalHeader().setHighlightSections(False)

        self.gridLayout_2.addWidget(self.ps_tableview, 1, 1, 1, 2)

        self.tabWidget.addTab(self.ps_tab, "")
        self.local_tab = QWidget()
        self.local_tab.setObjectName(u"local_tab")
        self.gridLayout_4 = QGridLayout(self.local_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.local_filter_text = QLineEdit(self.local_tab)
        self.local_filter_text.setObjectName(u"local_filter_text")

        self.gridLayout_4.addWidget(self.local_filter_text, 0, 0, 1, 1)

        self.local_filter_refresh = QPushButton(self.local_tab)
        self.local_filter_refresh.setObjectName(u"local_filter_refresh")
        self.local_filter_refresh.setIcon(icon)
        self.local_filter_refresh.setIconSize(QSize(27, 24))
        self.local_filter_refresh.setFlat(False)

        self.gridLayout_4.addWidget(self.local_filter_refresh, 0, 1, 1, 1)

        self.local_tableview = QTableView(self.local_tab)
        self.local_tableview.setObjectName(u"local_tableview")
        self.local_tableview.setShowGrid(False)
        self.local_tableview.setGridStyle(Qt.NoPen)
        self.local_tableview.setSortingEnabled(True)
        self.local_tableview.setWordWrap(False)
        self.local_tableview.setCornerButtonEnabled(False)
        self.local_tableview.horizontalHeader().setCascadingSectionResizes(True)
        self.local_tableview.horizontalHeader().setMinimumSectionSize(64)
        self.local_tableview.horizontalHeader().setDefaultSectionSize(120)
        self.local_tableview.horizontalHeader().setStretchLastSection(True)
        self.local_tableview.verticalHeader().setVisible(False)
        self.local_tableview.verticalHeader().setCascadingSectionResizes(True)
        self.local_tableview.verticalHeader().setHighlightSections(False)
        self.local_tableview.verticalHeader().setStretchLastSection(False)

        self.gridLayout_4.addWidget(self.local_tableview, 1, 0, 1, 2)

        self.tabWidget.addTab(self.local_tab, "")
        self.sd_tab = QWidget()
        self.sd_tab.setObjectName(u"sd_tab")
        self.gridLayout_3 = QGridLayout(self.sd_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.sd_filter_text = QLineEdit(self.sd_tab)
        self.sd_filter_text.setObjectName(u"sd_filter_text")

        self.gridLayout_3.addWidget(self.sd_filter_text, 0, 0, 1, 1)

        self.sd_filter_refresh = QPushButton(self.sd_tab)
        self.sd_filter_refresh.setObjectName(u"sd_filter_refresh")
        self.sd_filter_refresh.setIcon(icon)
        self.sd_filter_refresh.setIconSize(QSize(27, 24))
        self.sd_filter_refresh.setFlat(False)

        self.gridLayout_3.addWidget(self.sd_filter_refresh, 0, 1, 1, 1)

        self.sd_tableview = QTableView(self.sd_tab)
        self.sd_tableview.setObjectName(u"sd_tableview")
        self.sd_tableview.setShowGrid(False)
        self.sd_tableview.setGridStyle(Qt.NoPen)
        self.sd_tableview.setSortingEnabled(True)
        self.sd_tableview.setWordWrap(False)
        self.sd_tableview.setCornerButtonEnabled(False)
        self.sd_tableview.horizontalHeader().setCascadingSectionResizes(True)
        self.sd_tableview.horizontalHeader().setMinimumSectionSize(64)
        self.sd_tableview.horizontalHeader().setDefaultSectionSize(120)
        self.sd_tableview.horizontalHeader().setStretchLastSection(True)
        self.sd_tableview.verticalHeader().setVisible(False)
        self.sd_tableview.verticalHeader().setCascadingSectionResizes(True)
        self.sd_tableview.verticalHeader().setHighlightSections(False)
        self.sd_tableview.verticalHeader().setStretchLastSection(False)

        self.gridLayout_3.addWidget(self.sd_tableview, 1, 0, 1, 2)

        self.tabWidget.addTab(self.sd_tab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(200, 0))
        self.gridLayout_14 = QGridLayout(self.widget)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.patch_view = QGraphicsView(self.widget)
        self.patch_view.setObjectName(u"patch_view")

        self.gridLayout_14.addWidget(self.patch_view, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        self.file_menu = QMenu(self.menubar)
        self.file_menu.setObjectName(u"file_menu")
        self.sdcard_menu = QMenu(self.menubar)
        self.sdcard_menu.setObjectName(u"sdcard_menu")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)

        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.sdcard_menu.menuAction())
        self.file_menu.addAction(self.action_connect_to_PatchStorage)
        self.file_menu.addAction(self.action_update_files)
        self.file_menu.addAction(self.action_upload_file)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action_quit)

        self.retranslateUi(main_window)

        self.tabWidget.setCurrentIndex(2)
        self.ps_filter_refresh.setDefault(False)
        self.local_filter_refresh.setDefault(False)
        self.sd_filter_refresh.setDefault(False)


        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"Zoia Library", None))
        self.action_connect_to_PatchStorage.setText(QCoreApplication.translate("main_window", u"Connect to PatchStorage", None))
        self.action_update_files.setText(QCoreApplication.translate("main_window", u"Update Files", None))
        self.action_upload_file.setText(QCoreApplication.translate("main_window", u"Upload File ...", None))
        self.action_quit.setText(QCoreApplication.translate("main_window", u"Quit", None))
        self.groupBox.setTitle("")
        self.ps_filter_text.setText("")
        self.ps_filter_text.setPlaceholderText(QCoreApplication.translate("main_window", u"Filter <multiple items sperated by a ;>", None))
        self.ps_filter_refresh.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ps_tab), QCoreApplication.translate("main_window", u"PatchStorage", None))
        self.local_filter_text.setText("")
        self.local_filter_text.setPlaceholderText(QCoreApplication.translate("main_window", u"Filter <multiple items sperated by a ;>", None))
        self.local_filter_refresh.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.local_tab), QCoreApplication.translate("main_window", u"Local Patches", None))
        self.sd_filter_text.setText("")
        self.sd_filter_text.setPlaceholderText(QCoreApplication.translate("main_window", u"Filter <multiple items sperated by a ;>", None))
        self.sd_filter_refresh.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sd_tab), QCoreApplication.translate("main_window", u"SD Card Patches", None))
        self.file_menu.setTitle(QCoreApplication.translate("main_window", u"File", None))
        self.sdcard_menu.setTitle(QCoreApplication.translate("main_window", u"SD Cards", None))
    # retranslateUi

