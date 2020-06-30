# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'early.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1663, 1137)
        icon = QIcon()
        icon.addFile(u"resources/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.actionSpecify_SD_Card_Location = QAction(MainWindow)
        self.actionSpecify_SD_Card_Location.setObjectName(u"actionSpecify_SD_Card_Location")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionSort_by_title_A_Z = QAction(MainWindow)
        self.actionSort_by_title_A_Z.setObjectName(u"actionSort_by_title_A_Z")
        self.actionSort_by_title_Z_A = QAction(MainWindow)
        self.actionSort_by_title_Z_A.setObjectName(u"actionSort_by_title_Z_A")
        self.actionSort_by_date_new_old = QAction(MainWindow)
        self.actionSort_by_date_new_old.setObjectName(u"actionSort_by_date_new_old")
        self.actionSort_by_date_old_new = QAction(MainWindow)
        self.actionSort_by_date_old_new.setObjectName(u"actionSort_by_date_old_new")
        self.actionSort_by_likes_high_low = QAction(MainWindow)
        self.actionSort_by_likes_high_low.setObjectName(u"actionSort_by_likes_high_low")
        self.actionSort_by_likes_low_high = QAction(MainWindow)
        self.actionSort_by_likes_low_high.setObjectName(u"actionSort_by_likes_low_high")
        self.actionSort_by_views_high_low = QAction(MainWindow)
        self.actionSort_by_views_high_low.setObjectName(u"actionSort_by_views_high_low")
        self.actionSort_by_views_low_high = QAction(MainWindow)
        self.actionSort_by_views_low_high.setObjectName(u"actionSort_by_views_low_high")
        self.actionSort_by_downloads_high_low = QAction(MainWindow)
        self.actionSort_by_downloads_high_low.setObjectName(u"actionSort_by_downloads_high_low")
        self.actionSort_by_downloads_low_high = QAction(MainWindow)
        self.actionSort_by_downloads_low_high.setObjectName(u"actionSort_by_downloads_low_high")
        self.actionCheck_For_Updates = QAction(MainWindow)
        self.actionCheck_For_Updates.setObjectName(u"actionCheck_For_Updates")
        self.actionReload_PatchStorage_patch_list = QAction(MainWindow)
        self.actionReload_PatchStorage_patch_list.setObjectName(u"actionReload_PatchStorage_patch_list")
        self.actionZOIA_Librarian_Help = QAction(MainWindow)
        self.actionZOIA_Librarian_Help.setObjectName(u"actionZOIA_Librarian_Help")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.left_widget = QTabWidget(self.centralwidget)
        self.left_widget.setObjectName(u"left_widget")
        self.left_widget.setTabShape(QTabWidget.Rounded)
        self.left_widget.setMovable(True)
        self.tab_ps_2 = QWidget()
        self.tab_ps_2.setObjectName(u"tab_ps_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_ps_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_5 = QWidget(self.tab_ps_2)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_6 = QVBoxLayout(self.widget_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.widget_7)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setMinimumSize(QSize(640, 480))
        self.splitter_2.setMaximumSize(QSize(16777215, 16777215))
        self.splitter_2.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.splitter_2.setFrameShape(QFrame.NoFrame)
        self.splitter_2.setFrameShadow(QFrame.Plain)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.splitter_2.setChildrenCollapsible(False)
        self.widget_8 = QWidget(self.splitter_2)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget_8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 9, 0)
        self.widget = QWidget(self.widget_8)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.searchbar_3 = QLineEdit(self.widget)
        self.searchbar_3.setObjectName(u"searchbar_3")

        self.horizontalLayout_3.addWidget(self.searchbar_3)

        self.search_button_3 = QPushButton(self.widget)
        self.search_button_3.setObjectName(u"search_button_3")

        self.horizontalLayout_3.addWidget(self.search_button_3)


        self.verticalLayout.addWidget(self.widget)

        self.table = QTableWidget(self.widget_8)
        if (self.table.columnCount() < 5):
            self.table.setColumnCount(5)
        if (self.table.rowCount() < 1):
            self.table.setRowCount(1)
        self.table.setObjectName(u"table")
        self.table.setFrameShadow(QFrame.Plain)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.table)

        self.splitter_2.addWidget(self.widget_8)
        self.text_browser = QTextBrowser(self.splitter_2)
        self.text_browser.setObjectName(u"text_browser")
        self.text_browser.setFrameShadow(QFrame.Plain)
        self.text_browser.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.splitter_2.addWidget(self.text_browser)

        self.horizontalLayout_7.addWidget(self.splitter_2)


        self.verticalLayout_6.addWidget(self.widget_7)


        self.horizontalLayout_6.addWidget(self.widget_6)


        self.verticalLayout_3.addWidget(self.widget_5)

        self.left_widget.addTab(self.tab_ps_2, "")
        self.tab_ls = QWidget()
        self.tab_ls.setObjectName(u"tab_ls")
        self.verticalLayout_4 = QVBoxLayout(self.tab_ls)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_9 = QWidget(self.tab_ls)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.widget_10 = QWidget(self.widget_9)
        self.widget_10.setObjectName(u"widget_10")
        self.verticalLayout_7 = QVBoxLayout(self.widget_10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.widget_11 = QWidget(self.widget_10)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.splitter_3 = QSplitter(self.widget_11)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setMinimumSize(QSize(640, 480))
        self.splitter_3.setMaximumSize(QSize(16777215, 16777215))
        self.splitter_3.setFrameShape(QFrame.NoFrame)
        self.splitter_3.setFrameShadow(QFrame.Plain)
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.splitter_3.setChildrenCollapsible(False)
        self.widget_12 = QWidget(self.splitter_3)
        self.widget_12.setObjectName(u"widget_12")
        sizePolicy.setHeightForWidth(self.widget_12.sizePolicy().hasHeightForWidth())
        self.widget_12.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget_12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 9, 0)
        self.widget_2 = QWidget(self.widget_12)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.searchbar_4 = QLineEdit(self.widget_2)
        self.searchbar_4.setObjectName(u"searchbar_4")

        self.horizontalLayout_4.addWidget(self.searchbar_4)

        self.search_button_4 = QPushButton(self.widget_2)
        self.search_button_4.setObjectName(u"search_button_4")

        self.horizontalLayout_4.addWidget(self.search_button_4)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.table_2 = QTableWidget(self.widget_12)
        if (self.table_2.columnCount() < 6):
            self.table_2.setColumnCount(6)
        if (self.table_2.rowCount() < 1):
            self.table_2.setRowCount(1)
        self.table_2.setObjectName(u"table_2")
        self.table_2.setFrameShadow(QFrame.Plain)
        self.table_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_2.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_2.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_2.setRowCount(1)
        self.table_2.setColumnCount(6)
        self.table_2.horizontalHeader().setStretchLastSection(True)
        self.table_2.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.table_2)

        self.splitter_3.addWidget(self.widget_12)
        self.text_browser_2 = QTextBrowser(self.splitter_3)
        self.text_browser_2.setObjectName(u"text_browser_2")
        self.text_browser_2.setFrameShadow(QFrame.Plain)
        self.text_browser_2.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.splitter_3.addWidget(self.text_browser_2)

        self.horizontalLayout_9.addWidget(self.splitter_3)


        self.verticalLayout_7.addWidget(self.widget_11)


        self.horizontalLayout_8.addWidget(self.widget_10)


        self.verticalLayout_4.addWidget(self.widget_9)

        self.left_widget.addTab(self.tab_ls, "")
        self.tab_sd = QWidget()
        self.tab_sd.setObjectName(u"tab_sd")
        self.horizontalLayout = QHBoxLayout(self.tab_sd)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.table_3 = QTableWidget(self.tab_sd)
        if (self.table_3.columnCount() < 1):
            self.table_3.setColumnCount(1)
        if (self.table_3.rowCount() < 64):
            self.table_3.setRowCount(64)
        self.table_3.setObjectName(u"table_3")
        self.table_3.setMinimumSize(QSize(1619, 0))
        self.table_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_3.setDragEnabled(True)
        self.table_3.setDragDropOverwriteMode(False)
        self.table_3.setDragDropMode(QAbstractItemView.InternalMove)
        self.table_3.setDefaultDropAction(Qt.MoveAction)
        self.table_3.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_3.setRowCount(64)
        self.table_3.setColumnCount(1)
        self.table_3.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout.addWidget(self.table_3)

        self.left_widget.addTab(self.tab_sd, "")

        self.horizontalLayout_2.addWidget(self.left_widget)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1663, 27))
        self.menuFiel = QMenu(self.menubar)
        self.menuFiel.setObjectName(u"menuFiel")
        self.menuSort = QMenu(self.menubar)
        self.menuSort.setObjectName(u"menuSort")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFiel.menuAction())
        self.menubar.addAction(self.menuSort.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFiel.addAction(self.actionSpecify_SD_Card_Location)
        self.menuFiel.addAction(self.actionCheck_For_Updates)
        self.menuFiel.addAction(self.actionReload_PatchStorage_patch_list)
        self.menuFiel.addSeparator()
        self.menuFiel.addAction(self.actionQuit)
        self.menuSort.addAction(self.actionSort_by_title_A_Z)
        self.menuSort.addAction(self.actionSort_by_title_Z_A)
        self.menuSort.addAction(self.actionSort_by_date_new_old)
        self.menuSort.addAction(self.actionSort_by_date_old_new)
        self.menuSort.addAction(self.actionSort_by_likes_high_low)
        self.menuSort.addAction(self.actionSort_by_likes_low_high)
        self.menuSort.addAction(self.actionSort_by_views_high_low)
        self.menuSort.addAction(self.actionSort_by_views_low_high)
        self.menuSort.addAction(self.actionSort_by_downloads_high_low)
        self.menuSort.addAction(self.actionSort_by_downloads_low_high)
        self.menuHelp.addAction(self.actionZOIA_Librarian_Help)

        self.retranslateUi(MainWindow)

        self.left_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ZOIA Librarian", None))
        self.actionSpecify_SD_Card_Location.setText(QCoreApplication.translate("MainWindow", u"Specify SD Card Location", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionSort_by_title_A_Z.setText(QCoreApplication.translate("MainWindow", u"Sort by title (A-Z)", None))
        self.actionSort_by_title_Z_A.setText(QCoreApplication.translate("MainWindow", u"Sort by title (Z-A)", None))
        self.actionSort_by_date_new_old.setText(QCoreApplication.translate("MainWindow", u"Sort by date (new-old)", None))
        self.actionSort_by_date_old_new.setText(QCoreApplication.translate("MainWindow", u"Sort by date (old-new)", None))
        self.actionSort_by_likes_high_low.setText(QCoreApplication.translate("MainWindow", u"Sort by likes (high-low)", None))
        self.actionSort_by_likes_low_high.setText(QCoreApplication.translate("MainWindow", u"Sort by likes (low-high)", None))
        self.actionSort_by_views_high_low.setText(QCoreApplication.translate("MainWindow", u"Sort by views (high-low)", None))
        self.actionSort_by_views_low_high.setText(QCoreApplication.translate("MainWindow", u"Sort by views (low-high)", None))
        self.actionSort_by_downloads_high_low.setText(QCoreApplication.translate("MainWindow", u"Sort by downloads (high-low)", None))
        self.actionSort_by_downloads_low_high.setText(QCoreApplication.translate("MainWindow", u"Sort by downloads (low-high)", None))
        self.actionCheck_For_Updates.setText(QCoreApplication.translate("MainWindow", u"Check For Patch Updates", None))
        self.actionReload_PatchStorage_patch_list.setText(QCoreApplication.translate("MainWindow", u"Reload PatchStorage Patch List", None))
        self.actionZOIA_Librarian_Help.setText(QCoreApplication.translate("MainWindow", u"ZOIA Librarian Help", None))
        self.search_button_3.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.left_widget.setTabText(self.left_widget.indexOf(self.tab_ps_2), QCoreApplication.translate("MainWindow", u"PatchStorage View", None))
#if QT_CONFIG(tooltip)
        self.left_widget.setTabToolTip(self.left_widget.indexOf(self.tab_ps_2), QCoreApplication.translate("MainWindow", u"Switch to view all ZOIA patches on PatchStorage", None))
#endif // QT_CONFIG(tooltip)
        self.search_button_4.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.left_widget.setTabText(self.left_widget.indexOf(self.tab_ls), QCoreApplication.translate("MainWindow", u"Local Storage View", None))
#if QT_CONFIG(tooltip)
        self.left_widget.setTabToolTip(self.left_widget.indexOf(self.tab_ls), QCoreApplication.translate("MainWindow", u"Switch to your locally saved patches", None))
#endif // QT_CONFIG(tooltip)
        self.left_widget.setTabText(self.left_widget.indexOf(self.tab_sd), QCoreApplication.translate("MainWindow", u"SD Card View", None))
        self.menuFiel.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSort.setTitle(QCoreApplication.translate("MainWindow", u"Sort", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

