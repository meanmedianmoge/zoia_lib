import platform

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFontDialog, QApplication, QFileDialog
import os
import json

from zoia_lib.backend.utilities import meipass


class ZOIALibrarianUtil:
    """The ZOIALibrarianUTIL class is responsible for all
    auxiliary activities that may be required by other ZOIALibrarian
    classes.
    """

    def __init__(self, ui, window):
        """Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        window: A reference to the main UI window for icon consistency.
        """

        # Get the ui reference
        self.ui = ui
        self.window = window

        self.dark = True
        self.row_inversion = False
        self.font = QFont("Verdana", 10)

    def change_font(self, name):
        """Changes the font used throughout the application.
        Currently triggered via a menu action.

        name: Used to specify whether the font should be resized or
              changed to a different font family.
        """

        # Get the context.
        if name == "":
            # Case 1: Default Change Font menu option.
            ok, f = QFontDialog.getFont(self.window)
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
            self.font = f
            new_font = f
            big_font = QFont(f.toString().split(",")[0], f.pointSize() + 6)

            # self.ui.tabs.setFont(new_font)

            # PS tab
            self.ui.table_PS.setFont(new_font)
            self.ui.table_PS.horizontalHeader().setFont(new_font)
            self.ui.text_browser_PS.setFont(big_font)
            self.ui.refresh_pch_btn.setFont(new_font)
            self.ui.btn_dwn_all.setFont(new_font)

            # Local tab
            self.ui.table_local.setFont(new_font)
            self.ui.table_local.horizontalHeader().setFont(new_font)
            self.ui.text_browser_local.setFont(big_font)
            self.ui.back_btn_local.setFont(new_font)
            self.ui.check_for_updates_btn.setFont(new_font)
            self.ui.update_patch_notes.setFont(new_font)
            self.ui.btn_show_routing.setFont(new_font)
            self.ui.page_label.setFont(new_font)
            self.ui.back_btn.setFont(new_font)
            self.ui.btn_next_page.setFont(new_font)
            self.ui.btn_prev_page.setFont(new_font)

            # SD tab
            self.ui.sd_tree.setFont(new_font)
            self.ui.table_sd_left.setFont(new_font)
            self.ui.table_sd_left.horizontalHeader().setFont(new_font)
            self.ui.table_sd_left.verticalHeader().setFont(new_font)
            self.ui.table_sd_right.setFont(new_font)
            self.ui.table_sd_right.horizontalHeader().setFont(new_font)
            self.ui.table_sd_right.verticalHeader().setFont(new_font)
            self.ui.delete_folder_sd_btn.setFont(new_font)
            self.ui.set_export_dir_btn.setFont(new_font)
            self.ui.import_all_btn.setFont(new_font)
            self.ui.import_all_ver_btn.setFont(new_font)

            # Folders tab
            self.ui.table_bank_local.setFont(new_font)
            self.ui.table_bank_local.horizontalHeader().setFont(new_font)
            self.ui.table_bank_left.setFont(new_font)
            self.ui.text_browser_viz.setFont(new_font)
            self.ui.table_bank_left.horizontalHeader().setFont(new_font)
            self.ui.table_bank_left.verticalHeader().setFont(new_font)
            self.ui.table_bank_right.setFont(new_font)
            self.ui.table_bank_right.horizontalHeader().setFont(new_font)
            self.ui.table_bank_right.verticalHeader().setFont(new_font)
            self.ui.back_btn_bank.setFont(new_font)
            self.ui.btn_save_bank.setFont(new_font)
            self.ui.btn_load_bank.setFont(new_font)
            self.ui.btn_clear_bank.setFont(new_font)
            self.ui.btn_export_bank.setFont(new_font)
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
                    # Need trys here in case the table does not have a
                    # cell widget there yet.
                    try:
                        self.ui.table_sd_left.cellWidget(i, 1).setFont(new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_sd_left.cellWidget(i, 2).setFont(new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_sd_right.cellWidget(i, 1).setFont(new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_sd_right.cellWidget(i, 2).setFont(new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_left.cellWidget(i, 1).setFont(new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_left.cellWidget(i, 2).setFont(new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_right.cellWidget(i, 1).setFont(new_font)
                    except AttributeError:
                        pass
                    try:
                        self.ui.table_bank_right.cellWidget(i, 2).setFont(new_font)
                    except AttributeError:
                        pass
                if self.ui.table_bank_local.cellWidget(0, 0) is not None:
                    for i in range(self.ui.table_bank_local.rowCount()):
                        self.ui.table_bank_local.cellWidget(i, 0).setFont(new_font)

    def save_pref(self, w, h, sd, path):
        """Saves and writes the state of a UI window to pref.json

        w: The width of the main window.
        h: The height of the main window.
        sd: The path to an the root of a specified SD card.
        path: The path to the backend .ZoiaLibraryApp directory.
        """

        # Capture the necessary specs on exit.
        window = {
            "width": w,
            "height": h,
            "font": self.ui.table_PS.horizontalHeader().font().toString().split(",")[0],
            "font_size": self.ui.table_PS.horizontalHeader().font().pointSize(),
            "sd_root": "" if sd is None else sd,
        }
        ps_sizes = {
            "col_0": self.ui.table_PS.columnWidth(0),
            "col_1": self.ui.table_PS.columnWidth(1),
            "col_2": self.ui.table_PS.columnWidth(2),
            "col_3": self.ui.table_PS.columnWidth(3),
            "split_left": self.ui.splitter_PS.sizes()[0],
            "split_right": self.ui.splitter_PS.sizes()[1],
        }
        local_sizes = {
            "col_0": self.ui.table_local.columnWidth(0),
            "col_1": self.ui.table_local.columnWidth(1),
            "col_2": self.ui.table_local.columnWidth(2),
            "col_3": self.ui.table_local.columnWidth(3),
            "col_4": self.ui.table_local.columnWidth(4),
            "col_5": self.ui.table_local.columnWidth(5),
            "split_left": self.ui.splitter_local.sizes()[0],
            "split_right": self.ui.splitter_local.sizes()[1],
            "split_top": self.ui.splitter_local_hori.sizes()[0],
            "split_bottom": self.ui.splitter_local_hori.sizes()[1],
        }
        sd_sizes = {
            "col_0": self.ui.table_sd_left.columnWidth(0),
            "col_1": self.ui.table_sd_left.columnWidth(1),
            "col_2": self.ui.table_sd_right.columnWidth(0),
            "col_3": self.ui.table_sd_right.columnWidth(1),
            "split_top": self.ui.splitter_sd_vert.sizes()[0],
            "split_bottom": self.ui.splitter_sd_vert.sizes()[1],
            "split_left": self.ui.splitter_sd_hori.sizes()[0],
            "split_right": self.ui.splitter_sd_hori.sizes()[1],
        }
        bank_sizes = {
            "col_0": self.ui.table_bank_left.columnWidth(0),
            "col_1": self.ui.table_bank_right.columnWidth(0),
            "col_2": self.ui.table_bank_local.columnWidth(0),
            "col_3": self.ui.table_bank_local.columnWidth(1),
            "col_4": self.ui.table_bank_local.columnWidth(2),
            "col_5": self.ui.table_bank_local.columnWidth(3),
            "split_left": self.ui.splitter_bank.sizes()[0],
            "split_middle": self.ui.splitter_bank.sizes()[1],
            "split_right": self.ui.splitter_bank.sizes()[2],
            "split_bank_left": self.ui.splitter_bank_tables.sizes()[0],
            "split_bank_right": self.ui.splitter_bank_tables.sizes()[1],
        }
        dark_mode = {"enabled": not self.dark}
        row_invert = {"enabled": not self.row_inversion}

        # Write the data to pref.json for subsequent launches.
        with open(os.path.join(path, "pref.json"), "w") as f:
            f.write(
                json.dumps(
                    [
                        window,
                        ps_sizes,
                        local_sizes,
                        sd_sizes,
                        bank_sizes,
                        dark_mode,
                        row_invert,
                    ]
                )
            )

    def toggle_dark(self):
        """Toggles the theme for the application.
        Currently triggered via a menu action.
        """

        app = QApplication.instance()
        # Pick the right stylesheet based on the OS.
        sheet = {
            ("darwin", True): "osx-light.css",
            ("windows", True): "light.css",
            ("linux", True): "light.css",
            ("darwin", False): "osx-dark.css",
            ("windows", False): "dark.css",
            ("linux", False): "dark.css",
        }[(platform.system().lower(), self.dark)]

        with open(meipass("zoia_lib/UI/resources/{}".format(sheet)), "r") as f:
            data = f.read()

        self.dark = not self.dark
        app.setStyleSheet(data)
        self.change_font(self.font)

    def row_invert(self):
        """Either enables of disables alternating row colours for
        tables depending on the previous state of the tables.
        Currently triggered via a menu action.
        """

        if self.row_inversion:
            self.ui.table_PS.setAlternatingRowColors(True)
            self.ui.table_local.setAlternatingRowColors(True)
            self.ui.table_sd_left.setAlternatingRowColors(False)
            self.ui.table_sd_right.setAlternatingRowColors(False)
            self.ui.table_bank_local.setAlternatingRowColors(False)
            self.ui.table_bank_left.setAlternatingRowColors(False)
            self.ui.table_bank_right.setAlternatingRowColors(False)
        else:
            self.ui.table_PS.setAlternatingRowColors(False)
            self.ui.table_local.setAlternatingRowColors(False)
            self.ui.table_sd_left.setAlternatingRowColors(False)
            self.ui.table_sd_right.setAlternatingRowColors(False)
            self.ui.table_bank_local.setAlternatingRowColors(False)
            self.ui.table_bank_left.setAlternatingRowColors(False)
            self.ui.table_bank_right.setAlternatingRowColors(False)

        self.row_inversion = not self.row_inversion

    def set_row_inversion(self, value):
        """Setter method to specify whether alternating rows is enabled."""
        self.row_inversion = value

    def set_dark(self, value):
        """Setter method to specify whether dark mode is enabled."""
        self.dark = value

    def set_font(self, f):
        """Setter method to specify the font to be used for the app."""
        self.font = f

    def open_local_backend(self):
        """Opens a FileBrowser showing the app's local backend."""

        QFileDialog.getExistingDirectory(
            None, "Local Backend", self.window.path
            # QFileDialog.DontUseNativeDialog
        )

    def documentation(self):
        """Passes documentation to the front-end PS tab."""

        with open(meipass("documentation/Resources/manual.html"), "r", errors="ignore") as f:
            manual = f.read()

        self.ui.text_browser_PS.setText(
            """
            {}
        """.format(
                manual
            )
        )

    def faq(self):
        """Passes FAQ to the front-end PS tab."""

        with open(meipass("documentation/Resources/faq.html"), "r", errors="ignore") as f:
            faq = f.read()

        self.ui.text_browser_PS.setText(
            """
            {}
        """.format(
                faq
            )
        )

    def tips(self):
        """Passes Tips & Tricks to front-end PS tab."""

        with open(meipass("documentation/Resources/tips.html"), "r", errors="ignore") as f:
            tips = f.read()

        self.ui.text_browser_PS.setText(
            """
            {}
        """.format(
                tips
            )
        )

    def mod_idx(self):
        """Passes Module Index to front-end PS tab."""

        with open(meipass("documentation/Resources/mod.html"), "r", errors="ignore") as f:
            mod = f.read()

        self.ui.text_browser_PS.setText(
            """
            {}
        """.format(
                mod
            )
        )

    def firmware(self):
        """Passes firmware changelog to front-end PS tab."""

        with open(meipass("documentation/Resources/changelog.html"), "r", errors="ignore") as f:
            logs = f.read()

        self.ui.text_browser_PS.setText(
            """
            {}
        """.format(
                logs
            )
        )

    @staticmethod
    def multi_drag_drop(rows_left, rows_right, table_1, table_2, f1):
        """Attempts to move multiple rows from one table at the same
        time. This can be within the same table or to a companion table.

        rows_left: An array containing the rows currently stored in the
                   left table.
        rows_right: And array containing the rows currently stored in
                    the right table.
        table_1: The left table associated with the multi drag/drop.
        table_2: The right table associated with the multi drag/drop.
        f1: A function to move the useful data associated with the rows.
        """

        first_item = None
        first_item_index = -1

        # Figure out which rows var to use depending on whether we
        # originate from the left or right.
        if len(rows_left) > 1 and len(rows_right) == 0:
            curr_rows = rows_left
            main_table = table_1
            other_table = table_2
        else:
            curr_rows = rows_right
            main_table = table_2
            other_table = table_1

        # Find the first entry for the current set of rows.
        for i in sorted(curr_rows):
            i = i.row()
            i = int("%d" % i)
            temp = main_table.item(i, 0)
            if temp is not None and temp.text() != "":
                first_item = temp
                first_item_index = i
                if main_table == table_2:
                    first_item_index += 32
                break
        first_item_text = first_item.text()
        for i in range(64):
            if i < 32:
                temp_left = table_1.item(i, 0)
                temp_right = None
            else:
                temp_right = table_2.item(i - 32, 0)
                temp_left = None
            if main_table == table_1:
                temp_main = temp_left
                temp_other = temp_right
            else:
                temp_main = temp_right
                temp_other = temp_left
            if (
                temp_main is not None
                and i != first_item_index
                and temp_main.text() == first_item_text
            ) or (temp_other is not None and temp_other.text() == first_item_text):
                # We found the first item!
                # row = sorted(curr_rows)[-1].row()
                # row = int('%d' % row)
                rows = [int(x.row()) for x in sorted(curr_rows)]
                if curr_rows == rows_right:
                    # row += 32
                    rows = [32 + x for x in rows]
                # for j in range(first_item_index, row + 1):
                for j in rows:
                    if j == first_item_index:
                        i = i + (j - first_item_index)
                    else:
                        i += 1
                    if i > 31:
                        if curr_rows == rows_right:
                            temp1 = main_table.item(j - 32, 0)
                        else:
                            temp1 = main_table.item(j, 0)
                        temp2 = other_table.item(i - 32, 0)
                    else:
                        if curr_rows == rows_right:
                            temp1 = main_table.item(j - 32, 0)
                        else:
                            temp1 = main_table.item(j, 0)
                        temp2 = main_table.item(i, 0)
                    if temp1 is None and temp2 is None:
                        continue
                    elif temp1 is None and temp2 is not None:
                        f1(i, j)
                    elif (
                        temp1 is not None
                        and temp2 is None
                        or temp1 is not None
                        and temp2 is not None
                    ):
                        f1(j, i)
                    elif temp1 is None and temp2 is not None:
                        f1(i, j)

        # Delete phantom rows from row insertions.
        table_1.setRowCount(32)
        table_2.setRowCount(32)
