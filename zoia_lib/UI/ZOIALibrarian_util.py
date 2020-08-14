import platform

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFontDialog, QApplication
import os
import json


class ZOIALibrarianUtil:

    def __init__(self, ui):

        # Get the ui reference
        self.ui = ui
        self.dark = True
        self.font = None

    def change_font(self, name):
        """ Changes the font used throughout the application.
        Currently triggered via a menu action.
        """

        # Get the context.
        if name == "":
            # Case 1: Default Change Font menu option.
            ok, f = QFontDialog.getFont()
            start = False
        elif name == "+" or name == "-":
            # Case 2: Increase/Decrease font size menu option.
            f = self.ui.table_PS.font()
            f_size = f.pointSize() + 2 if name == "+" else f.pointSize() - 2
            f = f.toString().split(",")[0]
            f = QFont(f, f_size)
            ok, start = True, False
        else:
            if type(name) == str:
                # Case 3.1: Init with pref.json
                f = name.split("%")
                f = QFont(f[0], int(f[1]))
            else:
                # Case 3.2: Init without pref.json (first launch).
                f = name
            ok, start = True, True
        if ok:
            # Change the font for everything (within reason).
            new_font = f
            big_font = QFont(f.toString().split(",")[0], f.pointSize() + 6)

            self.ui.table_PS.setFont(new_font)
            self.ui.table_PS.horizontalHeader().setFont(new_font)
            self.ui.table_local.setFont(new_font)
            self.ui.table_local.horizontalHeader().setFont(new_font)
            self.ui.table_sd_left.setFont(new_font)
            self.ui.table_sd_left.horizontalHeader().setFont(new_font)
            self.ui.table_sd_left.verticalHeader().setFont(new_font)
            self.ui.table_sd_right.setFont(new_font)
            self.ui.table_sd_right.horizontalHeader().setFont(new_font)
            self.ui.table_sd_right.verticalHeader().setFont(new_font)
            self.ui.table_bank_local.setFont(new_font)
            self.ui.table_bank_local.horizontalHeader().setFont(new_font)
            self.ui.table_bank_left.setFont(new_font)
            self.ui.table_bank_left.horizontalHeader().setFont(new_font)
            self.ui.table_bank_left.verticalHeader().setFont(new_font)
            self.ui.table_bank_right.setFont(new_font)
            self.ui.table_bank_right.horizontalHeader().setFont(new_font)
            self.ui.table_bank_right.verticalHeader().setFont(new_font)
            self.ui.tabs.setFont(new_font)
            self.ui.sd_tree.setFont(new_font)
            self.ui.text_browser_PS.setFont(big_font)
            self.ui.text_browser_local.setFont(big_font)
            self.ui.text_browser_bank.setFont(big_font)

            if not start:
                for i in range(self.ui.table_PS.rowCount()):
                    self.ui.table_PS.cellWidget(i, 0).setFont(new_font)
                    self.ui.table_PS.cellWidget(i, 4).setFont(new_font)
                if self.ui.table_local.cellWidget(0, 0) is not None:
                    for i in range(self.ui.table_local.rowCount()):
                        self.ui.table_local.cellWidget(i, 0).setFont(new_font)
                        self.ui.table_local.cellWidget(i, 4).setFont(new_font)
                        self.ui.table_local.cellWidget(i, 5).setFont(new_font)
                for i in range(32):
                    try:
                        self.ui.table_sd_left.cellWidget(i, 1).setFont(
                            new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_sd_left.cellWidget(i, 2).setFont(
                            new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_sd_right.cellWidget(i, 1).setFont(
                            new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_sd_right.cellWidget(i, 2).setFont(
                            new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_left.cellWidget(i, 1).setFont(
                            new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_left.cellWidget(i, 2).setFont(
                            new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_right.cellWidget(i, 1).setFont(
                            new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_right.cellWidget(i, 2).setFont(
                            new_font)
                    except AttributeError:
                        pass
                if self.ui.table_bank_local.cellWidget(0, 0) is not None:
                    for i in range(self.ui.table_bank_local.rowCount()):
                        self.ui.table_bank_local.cellWidget(i, 0).setFont(
                            new_font)

    def save_pref(self, w, h, sd, path):
        """ Saves and writes the state of a UI window to pref.json
        """

        # Capture the necessary specs on exit.
        window = {
            "width": w,
            "height": h,
            "font":
                self.ui.table_PS.horizontalHeader().font().toString().split(
                    ",")[0],
            "font_size":
                self.ui.table_PS.horizontalHeader().font().pointSize(),
            "sd_root": "" if sd is None else sd
        }
        ps_sizes = {
            "col_0": self.ui.table_PS.columnWidth(0),
            "col_1": self.ui.table_PS.columnWidth(1),
            "col_2": self.ui.table_PS.columnWidth(2),
            "col_3": self.ui.table_PS.columnWidth(3),
            "split_left": self.ui.splitter_PS.sizes()[0],
            "split_right": self.ui.splitter_PS.sizes()[1]
        }
        local_sizes = {
            "col_0": self.ui.table_local.columnWidth(0),
            "col_1": self.ui.table_local.columnWidth(1),
            "col_2": self.ui.table_local.columnWidth(2),
            "col_3": self.ui.table_local.columnWidth(3),
            "col_4": self.ui.table_local.columnWidth(4),
            "col_5": self.ui.table_local.columnWidth(5),
            "split_left": self.ui.splitter_local.sizes()[0],
            "split_right": self.ui.splitter_local.sizes()[1]
        }
        sd_sizes = {
            "col_0": self.ui.table_sd_left.columnWidth(0),
            "col_1": self.ui.table_sd_left.columnWidth(1),
            "col_2": self.ui.table_sd_right.columnWidth(0),
            "col_3": self.ui.table_sd_right.columnWidth(1),
            "split_top": self.ui.splitter_sd_vert.sizes()[0],
            "split_bottom": self.ui.splitter_sd_vert.sizes()[1],
            "split_left": self.ui.splitter_sd_hori.sizes()[0],
            "split_right": self.ui.splitter_sd_hori.sizes()[1]
        }
        bank_sizes = {
            "col_0": self.ui.table_bank_left.columnWidth(0),
            "col_1": self.ui.table_bank_right.columnWidth(0),
            "col_2": self.ui.table_bank_local.columnWidth(0),
            "col_3": self.ui.table_bank_local.columnWidth(1),
            "col_4": self.ui.table_bank_local.columnWidth(2),
            "split_left": self.ui.splitter_bank.sizes()[0],
            "split_middle": self.ui.splitter_bank.sizes()[1],
            "split_right": self.ui.splitter_bank.sizes()[2],
            "split_bank_left": self.ui.splitter_bank_tables.sizes()[0],
            "split_bank_right": self.ui.splitter_bank_tables.sizes()[1]
        }
        dark_mode = {
            "enabled": not self.dark
        }

        with open(os.path.join(path, "pref.json"), "w") as f:
            f.write(json.dumps([window, ps_sizes, local_sizes,
                                sd_sizes, bank_sizes, dark_mode]))

    def toggle_dark(self):
        app = QApplication.instance()
        sheet = {
            ("darwin", True): "osx-light.css",
            ("windows", True): "light.css",
            ("linux", True): "light.css",
            ("darwin", False): "osx-dark.css",
            ("windows", False): "dark.css",
            ("linux", True): "dark.css"
        }[(platform.system().lower(), self.dark)]

        with open(os.path.join("zoia_lib", "UI", "resources",
                               sheet), "r") as f:
            data = f.read()

        self.dark = not self.dark
        app.setStyleSheet(data)
        self.change_font(self.font)

    def row_invert(self):
        """ Either enables of disables alternating row colours for
        tables depending on the previous state of the tables.
        Currently triggered via a menu action.
        """

        self.ui.table_PS.setAlternatingRowColors(
            not self.ui.table_PS.alternatingRowColors())
        self.ui.table_local.setAlternatingRowColors(
            not self.ui.table_local.alternatingRowColors())
        self.ui.table_sd_left.setAlternatingRowColors(
            not self.ui.table_sd_left.alternatingRowColors())
        self.ui.table_sd_right.setAlternatingRowColors(
            not self.ui.table_sd_right.alternatingRowColors())
        self.ui.table_bank_local.setAlternatingRowColors(
            not self.ui.table_bank_local.alternatingRowColors())
        self.ui.table_bank_left.setAlternatingRowColors(
            not self.ui.table_bank_left.alternatingRowColors())
        self.ui.table_bank_right.setAlternatingRowColors(
            not self.ui.table_bank_right.alternatingRowColors())

    def set_dark(self, value):
        """ Setter method to specify whether dark mode is enabled.
        """
        self.dark = value

    def set_font(self, f):
        """ Setter method to specify the font to be used for the app.
        """
        self.font = f
