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
        MainWindow.resize(1663, 1174)
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
        self.actionAlternating_Row_Colours = QAction(MainWindow)
        self.actionAlternating_Row_Colours.setObjectName(u"actionAlternating_Row_Colours")
        self.actionImport_A_Patch = QAction(MainWindow)
        self.actionImport_A_Patch.setObjectName(u"actionImport_A_Patch")
        self.actionToggle_Dark_Mode = QAction(MainWindow)
        self.actionToggle_Dark_Mode.setObjectName(u"actionToggle_Dark_Mode")
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
        self.splitter_2.setHandleWidth(10)
        self.splitter_2.setChildrenCollapsible(False)
        self.widget_8 = QWidget(self.splitter_2)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget_8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
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
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setOpenLinks(True)
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
        self.splitter = QSplitter(self.splitter_3)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.searchbar_4 = QLineEdit(self.layoutWidget)
        self.searchbar_4.setObjectName(u"searchbar_4")

        self.horizontalLayout_4.addWidget(self.searchbar_4)

        self.search_button_4 = QPushButton(self.layoutWidget)
        self.search_button_4.setObjectName(u"search_button_4")

        self.horizontalLayout_4.addWidget(self.search_button_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.table_2 = QTableWidget(self.layoutWidget)
        if (self.table_2.columnCount() < 6):
            self.table_2.setColumnCount(6)
        if (self.table_2.rowCount() < 1):
            self.table_2.setRowCount(1)
        self.table_2.setObjectName(u"table_2")
        self.table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_2.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_2.setRowCount(1)
        self.table_2.setColumnCount(6)
        self.table_2.horizontalHeader().setStretchLastSection(True)
        self.table_2.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.table_2)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget_2 = QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.verticalLayout_9 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.update_patch_notes = QPushButton(self.layoutWidget_2)
        self.update_patch_notes.setObjectName(u"update_patch_notes")

        self.verticalLayout_9.addWidget(self.update_patch_notes)

        self.text_browser_2 = QTextBrowser(self.layoutWidget_2)
        self.text_browser_2.setObjectName(u"text_browser_2")
        self.text_browser_2.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextEditable|Qt.TextSelectableByMouse)
        self.text_browser_2.setOpenExternalLinks(True)
        self.text_browser_2.setOpenLinks(True)

        self.verticalLayout_9.addWidget(self.text_browser_2)

        self.splitter.addWidget(self.layoutWidget_2)
        self.splitter_3.addWidget(self.splitter)

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
        __qtablewidgetitem = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(13, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(14, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(15, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(16, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(17, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(18, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(19, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(20, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(21, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(22, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(23, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(24, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(25, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(26, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(27, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(28, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(29, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(30, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(31, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(32, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(33, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(34, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(35, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(36, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(37, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(38, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(39, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(40, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(41, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(42, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(43, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(44, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(45, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(46, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(47, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(48, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(49, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(50, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(51, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(52, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(53, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(54, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(55, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(56, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(57, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(58, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(59, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(60, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(61, __qtablewidgetitem61)
        __qtablewidgetitem62 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(62, __qtablewidgetitem62)
        __qtablewidgetitem63 = QTableWidgetItem()
        self.table_3.setVerticalHeaderItem(63, __qtablewidgetitem63)
        self.table_3.setObjectName(u"table_3")
        self.table_3.setMinimumSize(QSize(1619, 0))
        self.table_3.setAcceptDrops(True)
        self.table_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_3.setDragEnabled(True)
        self.table_3.setDragDropOverwriteMode(False)
        self.table_3.setDragDropMode(QAbstractItemView.InternalMove)
        self.table_3.setDefaultDropAction(Qt.TargetMoveAction)
        self.table_3.setAlternatingRowColors(False)
        self.table_3.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_3.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_3.setRowCount(64)
        self.table_3.setColumnCount(1)
        self.table_3.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout.addWidget(self.table_3)

        self.left_widget.addTab(self.tab_sd, "")
        self.tab_bank = QWidget()
        self.tab_bank.setObjectName(u"tab_bank")
        self.left_widget.addTab(self.tab_bank, "")

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
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFiel.menuAction())
        self.menubar.addAction(self.menuSort.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFiel.addAction(self.actionSpecify_SD_Card_Location)
        self.menuFiel.addAction(self.actionCheck_For_Updates)
        self.menuFiel.addAction(self.actionReload_PatchStorage_patch_list)
        self.menuFiel.addAction(self.actionImport_A_Patch)
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
        self.menuOptions.addAction(self.actionAlternating_Row_Colours)
        self.menuOptions.addAction(self.actionToggle_Dark_Mode)

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
        self.actionAlternating_Row_Colours.setText(QCoreApplication.translate("MainWindow", u"Alternating Row Colours", None))
        self.actionImport_A_Patch.setText(QCoreApplication.translate("MainWindow", u"Import A Patch (.bin)", None))
        self.actionToggle_Dark_Mode.setText(QCoreApplication.translate("MainWindow", u"Toggle Dark Mode", None))
        self.search_button_3.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.left_widget.setTabText(self.left_widget.indexOf(self.tab_ps_2), QCoreApplication.translate("MainWindow", u"PatchStorage View", None))
#if QT_CONFIG(tooltip)
        self.left_widget.setTabToolTip(self.left_widget.indexOf(self.tab_ps_2), QCoreApplication.translate("MainWindow", u"Switch to view all ZOIA patches on PatchStorage", None))
#endif // QT_CONFIG(tooltip)
        self.search_button_4.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.update_patch_notes.setText(QCoreApplication.translate("MainWindow", u"Update Patch Notes", None))
        self.left_widget.setTabText(self.left_widget.indexOf(self.tab_ls), QCoreApplication.translate("MainWindow", u"Local Storage View", None))
#if QT_CONFIG(tooltip)
        self.left_widget.setTabToolTip(self.left_widget.indexOf(self.tab_ls), QCoreApplication.translate("MainWindow", u"Switch to your locally saved patches", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem = self.table_3.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem1 = self.table_3.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem2 = self.table_3.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qtablewidgetitem3 = self.table_3.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"3", None));
        ___qtablewidgetitem4 = self.table_3.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"4", None));
        ___qtablewidgetitem5 = self.table_3.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"5", None));
        ___qtablewidgetitem6 = self.table_3.verticalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"6", None));
        ___qtablewidgetitem7 = self.table_3.verticalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"7", None));
        ___qtablewidgetitem8 = self.table_3.verticalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"8", None));
        ___qtablewidgetitem9 = self.table_3.verticalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"9", None));
        ___qtablewidgetitem10 = self.table_3.verticalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"10", None));
        ___qtablewidgetitem11 = self.table_3.verticalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"11", None));
        ___qtablewidgetitem12 = self.table_3.verticalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"12", None));
        ___qtablewidgetitem13 = self.table_3.verticalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"13", None));
        ___qtablewidgetitem14 = self.table_3.verticalHeaderItem(14)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"14", None));
        ___qtablewidgetitem15 = self.table_3.verticalHeaderItem(15)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"15", None));
        ___qtablewidgetitem16 = self.table_3.verticalHeaderItem(16)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"16", None));
        ___qtablewidgetitem17 = self.table_3.verticalHeaderItem(17)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"17", None));
        ___qtablewidgetitem18 = self.table_3.verticalHeaderItem(18)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"18", None));
        ___qtablewidgetitem19 = self.table_3.verticalHeaderItem(19)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"19", None));
        ___qtablewidgetitem20 = self.table_3.verticalHeaderItem(20)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"20", None));
        ___qtablewidgetitem21 = self.table_3.verticalHeaderItem(21)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"21", None));
        ___qtablewidgetitem22 = self.table_3.verticalHeaderItem(22)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"22", None));
        ___qtablewidgetitem23 = self.table_3.verticalHeaderItem(23)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"23", None));
        ___qtablewidgetitem24 = self.table_3.verticalHeaderItem(24)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"24", None));
        ___qtablewidgetitem25 = self.table_3.verticalHeaderItem(25)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"25", None));
        ___qtablewidgetitem26 = self.table_3.verticalHeaderItem(26)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"26", None));
        ___qtablewidgetitem27 = self.table_3.verticalHeaderItem(27)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"27", None));
        ___qtablewidgetitem28 = self.table_3.verticalHeaderItem(28)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"28", None));
        ___qtablewidgetitem29 = self.table_3.verticalHeaderItem(29)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"29", None));
        ___qtablewidgetitem30 = self.table_3.verticalHeaderItem(30)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"30", None));
        ___qtablewidgetitem31 = self.table_3.verticalHeaderItem(31)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"31", None));
        ___qtablewidgetitem32 = self.table_3.verticalHeaderItem(32)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"32", None));
        ___qtablewidgetitem33 = self.table_3.verticalHeaderItem(33)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"33", None));
        ___qtablewidgetitem34 = self.table_3.verticalHeaderItem(34)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"34", None));
        ___qtablewidgetitem35 = self.table_3.verticalHeaderItem(35)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"35", None));
        ___qtablewidgetitem36 = self.table_3.verticalHeaderItem(36)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"36", None));
        ___qtablewidgetitem37 = self.table_3.verticalHeaderItem(37)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"37", None));
        ___qtablewidgetitem38 = self.table_3.verticalHeaderItem(38)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"38", None));
        ___qtablewidgetitem39 = self.table_3.verticalHeaderItem(39)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"39", None));
        ___qtablewidgetitem40 = self.table_3.verticalHeaderItem(40)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"40", None));
        ___qtablewidgetitem41 = self.table_3.verticalHeaderItem(41)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"41", None));
        ___qtablewidgetitem42 = self.table_3.verticalHeaderItem(42)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"42", None));
        ___qtablewidgetitem43 = self.table_3.verticalHeaderItem(43)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"43", None));
        ___qtablewidgetitem44 = self.table_3.verticalHeaderItem(44)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"44", None));
        ___qtablewidgetitem45 = self.table_3.verticalHeaderItem(45)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"45", None));
        ___qtablewidgetitem46 = self.table_3.verticalHeaderItem(46)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"46", None));
        ___qtablewidgetitem47 = self.table_3.verticalHeaderItem(47)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"47", None));
        ___qtablewidgetitem48 = self.table_3.verticalHeaderItem(48)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"48", None));
        ___qtablewidgetitem49 = self.table_3.verticalHeaderItem(49)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"49", None));
        ___qtablewidgetitem50 = self.table_3.verticalHeaderItem(50)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"50", None));
        ___qtablewidgetitem51 = self.table_3.verticalHeaderItem(51)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("MainWindow", u"51", None));
        ___qtablewidgetitem52 = self.table_3.verticalHeaderItem(52)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("MainWindow", u"52", None));
        ___qtablewidgetitem53 = self.table_3.verticalHeaderItem(53)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("MainWindow", u"53", None));
        ___qtablewidgetitem54 = self.table_3.verticalHeaderItem(54)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("MainWindow", u"54", None));
        ___qtablewidgetitem55 = self.table_3.verticalHeaderItem(55)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("MainWindow", u"55", None));
        ___qtablewidgetitem56 = self.table_3.verticalHeaderItem(56)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("MainWindow", u"56", None));
        ___qtablewidgetitem57 = self.table_3.verticalHeaderItem(57)
        ___qtablewidgetitem57.setText(QCoreApplication.translate("MainWindow", u"57", None));
        ___qtablewidgetitem58 = self.table_3.verticalHeaderItem(58)
        ___qtablewidgetitem58.setText(QCoreApplication.translate("MainWindow", u"58", None));
        ___qtablewidgetitem59 = self.table_3.verticalHeaderItem(59)
        ___qtablewidgetitem59.setText(QCoreApplication.translate("MainWindow", u"59", None));
        ___qtablewidgetitem60 = self.table_3.verticalHeaderItem(60)
        ___qtablewidgetitem60.setText(QCoreApplication.translate("MainWindow", u"60", None));
        ___qtablewidgetitem61 = self.table_3.verticalHeaderItem(61)
        ___qtablewidgetitem61.setText(QCoreApplication.translate("MainWindow", u"61", None));
        ___qtablewidgetitem62 = self.table_3.verticalHeaderItem(62)
        ___qtablewidgetitem62.setText(QCoreApplication.translate("MainWindow", u"62", None));
        ___qtablewidgetitem63 = self.table_3.verticalHeaderItem(63)
        ___qtablewidgetitem63.setText(QCoreApplication.translate("MainWindow", u"63", None));
        self.left_widget.setTabText(self.left_widget.indexOf(self.tab_sd), QCoreApplication.translate("MainWindow", u"SD Card View", None))
        self.left_widget.setTabText(self.left_widget.indexOf(self.tab_bank), QCoreApplication.translate("MainWindow", u"Banks", None))
        self.menuFiel.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSort.setTitle(QCoreApplication.translate("MainWindow", u"Sort", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

