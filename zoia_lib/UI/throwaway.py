# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'throwaway.ui'
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
        MainWindow.resize(1318, 1039)
        icon = QIcon()
        icon.addFile(u"resources/logo.png", QSize(), QIcon.Normal, QIcon.Off)
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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetNoConstraint)
        self.left_widget = QTabWidget(self.centralwidget)
        self.left_widget.setObjectName(u"left_widget")
        self.left_widget.setMovable(True)
        self.tab_ps_2 = QWidget()
        self.tab_ps_2.setObjectName(u"tab_ps_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_ps_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.searchbar_3 = QLineEdit(self.tab_ps_2)
        self.searchbar_3.setObjectName(u"searchbar_3")

        self.horizontalLayout_3.addWidget(self.searchbar_3)

        self.search_button_3 = QPushButton(self.tab_ps_2)
        self.search_button_3.setObjectName(u"search_button_3")

        self.horizontalLayout_3.addWidget(self.search_button_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.table = QTableWidget(self.tab_ps_2)
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.left_widget.addTab(self.tab_ps_2, "")
        self.tab_ls = QWidget()
        self.tab_ls.setObjectName(u"tab_ls")
        self.verticalLayout_4 = QVBoxLayout(self.tab_ls)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetNoConstraint)
        self.searchbar_4 = QLineEdit(self.tab_ls)
        self.searchbar_4.setObjectName(u"searchbar_4")

        self.horizontalLayout_6.addWidget(self.searchbar_4)

        self.search_button_4 = QPushButton(self.tab_ls)
        self.search_button_4.setObjectName(u"search_button_4")

        self.horizontalLayout_6.addWidget(self.search_button_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.table_2 = QTableWidget(self.tab_ls)
        self.table_2.setObjectName(u"table_2")
        self.table_2.setGridStyle(Qt.SolidLine)
        self.table_2.setSortingEnabled(True)

        self.verticalLayout_4.addWidget(self.table_2)

        self.left_widget.addTab(self.tab_ls, "")

        self.horizontalLayout_2.addWidget(self.left_widget)

        self.right_widget = QTextBrowser(self.centralwidget)
        self.right_widget.setObjectName(u"right_widget")

        self.horizontalLayout_2.addWidget(self.right_widget)


        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1318, 27))
        self.menuFiel = QMenu(self.menubar)
        self.menuFiel.setObjectName(u"menuFiel")
        self.menuSort = QMenu(self.menubar)
        self.menuSort.setObjectName(u"menuSort")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFiel.menuAction())
        self.menubar.addAction(self.menuSort.menuAction())
        self.menuFiel.addAction(self.actionSpecify_SD_Card_Location)
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
        self.menuFiel.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSort.setTitle(QCoreApplication.translate("MainWindow", u"Sort", None))
    # retranslateUi

