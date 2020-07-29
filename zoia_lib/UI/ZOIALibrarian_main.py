import json
import os
from os.path import expanduser

from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QMainWindow, QMessageBox, QInputDialog, \
    QFileDialog, QPushButton, QTableWidgetItem, QRadioButton, QDesktopWidget

import zoia_lib.UI.ZOIALibrarian as ui_main
import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors
from zoia_lib.UI.ZOIALibrarian_bank import ZOIALibrarianBank
from zoia_lib.UI.ZOIALibrarian_util import ZOIALibrarianUtil
from zoia_lib.UI.ZOIALibrarian_sd import ZOIALibrarianSD
from zoia_lib.backend.api import PatchStorage
from zoia_lib.backend.patch_delete import PatchDelete
from zoia_lib.backend.patch_export import PatchExport
from zoia_lib.backend.patch_save import PatchSave
from zoia_lib.backend.patch_update import PatchUpdate

ps = PatchStorage()
update = PatchUpdate()
save = PatchSave()
export = PatchExport()
delete = PatchDelete()


class ZOIALibrarianMain(QMainWindow):
    """ The ZOIALibrarian_Main class represents the frontend for the
    application. It allows users to interact with the various backend
    functions available. These include searching, downloading, sorting,
    and exporting patches; among other functions.

    Any changes made to the .ui file will not be reflected unless the
    following command is run from the UI directory:
        pyside2-uic.exe ZOIALibrarian.ui -o ZOIALibrarian.py

    Known issues:
     - Sorting order is not maintained when exiting out of the
       version history table of a patch.
     - The code is a mess and should be refactored into separate modules
       where possible.
    """

    def __init__(self):
        """ Initializes the UI for the application. Currently, upon
        being launched for the first time, it queries the PS API for all
        ZOIA patches and gets the metadata. Upon subsequent launches,
        it will search for previously stored metadata, compare it to
        the # of patches currently on PS, and either begin using the
        cached data, or get the most recent patches and add them to the
        cache; and subsequently start the application.
        """

        super().__init__()
        # Setup the UI using ZOIALibrarian.py
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)

        self.backend_path = save.get_backend_path()

        # Message box init
        self.icon = QIcon(os.path.join(os.getcwd(), "zoia_lib", "UI",
                                       "resources", "logo.ico"))
        self.msg = QMessageBox()
        self.msg.setWindowIcon(self.icon)

        # Helper classes init
        self.sd = ZOIALibrarianSD(self.ui, self.import_patch, self.msg,
                                  delete)
        self.bank = ZOIALibrarianBank(self.ui, self.backend_path, self.msg)
        self.util = ZOIALibrarianUtil(self.ui)

        self.data_PS = None
        self.patch_cache = []
        self.search_data_PS = None
        self.search_data_local = None
        self.search_data_bank = None
        self.data_local = None
        self.search_data_local_version = None
        self.search_data_bank_version = None
        self.data_local_version = None
        self.data_bank = None
        self.data_bank_version = None
        self.local_selected = None
        self.selected = None
        self.prev_tag_cat = None
        self.table_title_size = None
        self.table_local_title_size = None
        self.table_bank_local_title_size = None
        self.prev_sort = None
        self.curr_ver = None
        self.can_export_bank = False
        self.ps_sizes = None
        self.local_sizes = None
        self.sd_sizes = None
        self.bank_sizes = None
        self.font = None

        # Check for metadata in the user's backend.
        if "data.json" not in os.listdir(self.backend_path):
            ps_data = ps.get_all_patch_data_init()
            with open(os.path.join(self.backend_path, "data.json"),
                      "w") as f:
                f.write(json.dumps(ps_data))
                self.data_PS = ps_data
        else:
            # Got previous metadata, need to ensure that there are no
            # new patches.
            with open(os.path.join(self.backend_path, "data.json"),
                      "r") as f:
                data = json.loads(f.read())
            if len(data) == ps.patch_count:
                # Assume no new patches; allow the user to refresh manually.
                self.data_PS = data
            elif len(data) > ps.patch_count:
                # Uh oh, some patches got deleted on PatchStorage.
                ps_data = ps.get_all_patch_data_init()
                with open(os.path.join(self.backend_path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(ps_data))
                    self.data_PS = ps_data
            else:
                # Get the new patch metadata that we don't have.
                new_patches = ps.get_newest_patches(len(data))
                data = new_patches + data
                with open(os.path.join(self.backend_path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(data))
                    self.data_PS = data

        # Set the window icon
        self.setWindowIcon(QIcon(self.icon))

        # Disabling widgets the user doesn't have access to on startup.
        self.ui.tab_sd.setEnabled(False)
        self.ui.update_patch_notes.setEnabled(False)
        self.ui.import_all_btn.setEnabled(False)
        self.ui.import_all_ver_btn.setEnabled(False)
        self.ui.back_btn_local.setEnabled(False)
        self.ui.back_btn_bank.setEnabled(False)
        self.ui.btn_save_bank.setEnabled(False)
        self.ui.btn_export_bank.setEnabled(False)
        self.ui.delete_folder_sd_btn.setEnabled(False)
        if len(os.listdir(os.path.join(self.backend_path, "Banks"))) == 0:
            self.ui.btn_load_bank.setEnabled(False)

        # Load preferences from previous sessions (if they exist)
        if os.path.exists(os.path.join(self.backend_path, "pref.json")):
            # SD Card previously specified.
            with open(os.path.join(self.backend_path, "pref.json"), "r") as f:
                data = json.loads(f.read())
            if data[0]["sd_root"] is not "" \
                    and os.path.exists(data[0]["sd_root"]):
                self.sd.set_sd_root(data[0]["sd_root"])
                self.ui.tab_sd.setEnabled(True)
                self.sd.set_export(True)
                self.sd.sd_path(True, self.width())

            self.resize(data[0]["width"], data[0]["height"])

            # Font
            self.font = QFont(data[0]["font"], data[0]["font_size"])

            self.ps_sizes = data[1]
            self.local_sizes = data[2]
            self.sd_sizes = data[3]
            self.bank_sizes = data[4]

            # PS Table
            self.ui.table_PS.setColumnWidth(0, self.ps_sizes["col_0"])
            self.ui.table_PS.setColumnWidth(1, self.ps_sizes["col_1"])
            self.ui.table_PS.setColumnWidth(2, self.ps_sizes["col_2"])
            self.ui.table_PS.setColumnWidth(3, self.ps_sizes["col_3"])

            # Local Table
            self.ui.table_local.setColumnWidth(0, self.local_sizes["col_0"])
            self.ui.table_local.setColumnWidth(1, self.local_sizes["col_1"])
            self.ui.table_local.setColumnWidth(2, self.local_sizes["col_2"])
            self.ui.table_local.setColumnWidth(3, self.local_sizes["col_3"])
            self.ui.table_local.setColumnWidth(4, self.local_sizes["col_4"])

            # SD Tables
            self.ui.table_sd_left.setColumnWidth(0, self.sd_sizes["col_0"])
            self.ui.table_sd_left.setColumnWidth(1, self.sd_sizes["col_1"])
            self.ui.table_sd_right.setColumnWidth(0, self.sd_sizes["col_2"])
            self.ui.table_sd_right.setColumnWidth(1, self.sd_sizes["col_3"])

            # Bank Tables
            self.ui.table_bank_left.setColumnWidth(0, self.bank_sizes["col_0"])
            self.ui.table_bank_right.setColumnWidth(0,
                                                    self.bank_sizes["col_1"])
            self.ui.table_bank_local.setColumnWidth(0,
                                                    self.bank_sizes["col_2"])
            self.ui.table_bank_local.setColumnWidth(1,
                                                    self.bank_sizes["col_3"])
            self.ui.table_bank_local.setColumnWidth(2,
                                                    self.bank_sizes["col_4"])

        else:
            self.ui.table_sd_left.setColumnWidth(0, self.width() * 0.4)
            self.ui.table_sd_left.setColumnWidth(1, self.width() * 0.1)
            self.ui.table_sd_right.setColumnWidth(0, self.width() * 0.4)
            self.ui.table_sd_right.setColumnWidth(1, self.width() * 0.1)
            self.ui.table_bank_left.setColumnWidth(0, self.width() * 0.2)
            self.ui.table_bank_left.setColumnWidth(1, self.width() * 0.1)
            self.ui.table_bank_right.setColumnWidth(0, self.width() * 0.2)
            self.ui.table_bank_right.setColumnWidth(1, self.width() * 0.1)
            self.showMaximized()

        # Connect buttons and items to methods.
        self.ui.tabs.currentChanged.connect(self.tab_switch)
        self.ui.actionAlternating_Row_Colours.triggered.connect(
            lambda: self.util.row_invert())
        self.ui.actionSort_by_title_A_Z.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_title_Z_A.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_date_new_old.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_date_old_new.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_likes_high_low.triggered.connect(
            self.sort_and_set)
        self.ui.actionSort_by_likes_low_high.triggered.connect(
            self.sort_and_set)
        self.ui.actionSort_by_views_high_low.triggered.connect(
            self.sort_and_set)
        self.ui.actionSort_by_views_low_high.triggered.connect(
            self.sort_and_set)
        self.ui.actionSort_by_downloads_high_low.triggered.connect(
            self.sort_and_set)
        self.ui.actionSort_by_downloads_low_high.triggered.connect(
            self.sort_and_set)
        self.ui.actionSpecify_SD_Card_Location.triggered.connect(
            lambda: self.sd.sd_path(False, self.width()))
        self.ui.actionImport_Multiple_Patches.triggered.connect(
            self.mass_import)
        self.ui.actionFont.triggered.connect(
            lambda: self.util.change_font(""))
        self.ui.actionIncrease_Font_Size.triggered.connect(
            lambda: self.util.change_font("+"))
        self.ui.actionDecrease_Font_Size.triggered.connect(
            lambda: self.util.change_font("-"))
        self.ui.actionQuit.triggered.connect(self.try_quit)
        self.ui.check_for_updates_btn.clicked.connect(
            self.update_local_patches)
        self.ui.actionImport_Version_History_directory.triggered.connect(
            self.version_import)
        self.ui.refresh_pch_btn.clicked.connect(self.reload_ps)
        self.ui.update_patch_notes.clicked.connect(self.update_patch_notes)
        self.ui.actionImport_A_Patch.triggered.connect(self.import_patch)
        self.ui.table_local.installEventFilter(self)
        self.ui.table_sd_left.installEventFilter(self)
        self.ui.table_sd_right.installEventFilter(self)
        self.ui.table_bank_local.installEventFilter(self)
        self.ui.table_bank_left.installEventFilter(self)
        self.ui.table_bank_right.installEventFilter(self)
        self.ui.searchbar_PS.returnPressed.connect(self.search)
        self.ui.searchbar_local.returnPressed.connect(self.search)
        self.ui.searchbar_bank.returnPressed.connect(self.search)
        self.ui.searchbar_PS.installEventFilter(self)
        self.ui.searchbar_local.installEventFilter(self)
        self.ui.searchbar_bank.installEventFilter(self)
        self.ui.sd_tree.clicked.connect(
            lambda: self.sd.prepare_sd_view())
        self.ui.import_all_btn.clicked.connect(self.mass_import)
        self.ui.import_all_ver_btn.clicked.connect(self.version_import)
        self.ui.back_btn_local.clicked.connect(self.go_back)
        self.ui.back_btn_bank.clicked.connect(self.go_back)
        self.ui.btn_load_bank.clicked.connect(self.bank.load_bank)
        self.ui.btn_save_bank.clicked.connect(self.bank.save_bank)
        self.ui.btn_export_bank.clicked.connect(
            lambda: self.bank.export_bank(self.sd, export))
        self.ui.delete_folder_sd_btn.clicked.connect(
            lambda: self.sd.delete_sd_item(delete))

        # Font consistency.
        self.util.change_font(QFont("Verdana", 10) if self.font is None else
                              data[0]["font"] + "%" + str(
                                  data[0]["font_size"]))

        # Modify the display sizes for some widgets.
        if self.ps_sizes is None:
            self.ui.splitter_PS.setSizes([self.width() * 0.325,
                                          self.width() * 0.675])
        else:
            self.ui.splitter_PS.setSizes([self.ps_sizes["split_left"],
                                          self.ps_sizes["split_right"]])
        if self.local_sizes is None:
            self.ui.splitter_local.setSizes([self.width() * 0.325,
                                             self.width() * 0.675])
        else:
            self.ui.splitter_local.setSizes([self.local_sizes["split_left"],
                                             self.local_sizes["split_right"]])
        if self.sd_sizes is None:
            self.ui.splitter_sd_hori.setSizes([self.width() * 0.5,
                                               self.width() * 0.5])
            self.ui.splitter_sd_vert.setSizes([self.width() * 0.185,
                                               self.width() * 0.815])
        else:
            self.ui.splitter_sd_vert.setSizes([self.sd_sizes["split_top"],
                                               self.sd_sizes["split_bottom"]])
            self.ui.splitter_sd_hori.setSizes([self.sd_sizes["split_left"],
                                               self.sd_sizes["split_right"]])
        if self.bank_sizes is None:
            self.ui.splitter_bank_tables.setSizes([self.width() * 0.5,
                                                   self.width() * 0.5])
            self.ui.splitter_bank.setSizes([self.width() * 0.5, self.width() *
                                            0.25, self.width() * 0.25])
        else:
            self.ui.splitter_bank_tables.setSizes(
                [self.bank_sizes["split_bank_left"],
                 self.bank_sizes["split_bank_right"]])
            self.ui.splitter_bank.setSizes([self.bank_sizes["split_left"],
                                            self.bank_sizes["split_middle"],
                                            self.bank_sizes["split_right"]])

        # Sort and set the data.
        self.sort_and_set()

        # Center the application on launch.
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def tab_switch(self):
        """ Actions performed whenever a tab is switched to within the
        application.
        """

        # Reset the previous tag/cat (if it existed).
        self.prev_tag_cat = None

        # Figure out what tab we switched to.
        if self.ui.tabs.currentIndex() == 1 \
                or self.ui.tabs.currentIndex() == 3:
            self.get_local_patches()
            # Context cleanup
            if self.ui.tabs.currentIndex() == 3:
                self.ui.text_browser_bank.setText("")
            else:
                self.ui.text_browser_local.setText("")
                self.ui.update_patch_notes.setEnabled(False)
            self.sort_and_set()
        elif self.ui.tabs.currentIndex() == 2:
            # SD card tab, need to check if an SD card has been specified.
            if self.sd.get_sd_root() is None:
                self.msg.setWindowTitle("No SD Path")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Please specify your SD card path!")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                self.msg.setInformativeText(None)
                self.sd.sd_path(False, self.width())
                self.ui.tabs.setCurrentIndex(1)
        elif self.ui.tabs.currentIndex() == 0:
            pass
            # self.sort_and_set()

    def set_data(self, search=False, version=False):
        """ Sets the data for the various patch tables. This is done
        when the app begins, whenever a tab is returned to, whenever a
        search is initiated within a tab, or whenever a version history
        is expanded.

        This is for use with table_PS, table_local, and table_bank. For
        other tables, please see set_data_sd().

        search: True if we need are setting the data after a search has
                initiated, False otherwise. Defaults to False.
        version: True if we are using patch version data,
                 False otherwise. Defaults to False.
        """

        # Figure out what table we are working with.
        table_index = self.ui.tabs.currentIndex()

        # Get the current table.
        curr_table = {
            0: self.ui.table_PS,
            1: self.ui.table_local,
            3: self.ui.table_bank_local
        }[table_index]

        # Clear the contents of the table
        curr_table.clearContents()

        # Figure out the data we are using.
        data = {
            (0, True, False): self.search_data_PS,
            (0, False, False): self.data_PS,
            (1, True, True): self.search_data_local_version,
            (1, False, True): self.data_local_version,
            (1, True, False): self.search_data_local,
            (1, False, False): self.data_local,
            (3, True, True): self.search_data_bank_version,
            (3, False, True): self.data_bank_version,
            (3, True, False): self.search_data_bank,
            (3, False, False): self.data_bank
        }[(table_index, search, version)]

        data_length = len(data)

        # Set the rows for the table.
        curr_table.setRowCount(data_length)

        # Iterate through the data so that we can set each row.
        for i in range(data_length):
            # Button for the header "Title"
            btn_title = QRadioButton(data[i]["title"], self)
            title = data[i]["title"]
            # Wrap the title if it exceeds 25 characters in length.
            if len(title) > 25:
                temp = title.split(" ")
                count = 0
                title = ""
                for text in temp:
                    title += text + " "
                    count += len(text) + 1
                    if count > 25:
                        count = 0
                        title += "\n"
                btn_title.setText(title.rstrip())
            if (table_index == 1 and self.ui.back_btn_local.isEnabled()) or \
                    (table_index == 3 and self.ui.back_btn_bank.isEnabled()):
                btn_title.setObjectName(str(data[i]["id"]) + "_v"
                                        + str(data[i]["revision"]))
                btn_title.setText(data[i]["title"] + "\n"
                                  + data[i]["files"][0]["filename"])
            elif (table_index == 1 and
                  not self.ui.back_btn_local.isEnabled()) \
                    or (table_index == 3 and
                        not self.ui.back_btn_bank.isEnabled()):
                if len(os.listdir(os.path.join(self.backend_path,
                                               str(data[i]["id"])))) > 2:
                    btn_title.setText(title.rstrip() + "\n[Multiple Versions]")
                btn_title.setObjectName(str(data[i]["id"]))
            else:
                btn_title.setObjectName(str(data[i]["id"]))
            btn_title.toggled.connect(self.display_patch_info)
            btn_title.setFont(self.ui.table_PS.font())
            curr_table.setCellWidget(i, 0, btn_title)

            # Text for the headers "Tags" and "Categories"
            for j in range(2):
                index = "tags" if j == 0 else "categories"
                text = ""
                if len(data[i][index]) > 2:
                    for k in range(0, len(data[i][index]) - 1):
                        text += data[i][index][k]["name"] + ", "
                    text += "and " \
                            + data[i][index][len(data[i][index]) - 1]["name"]
                elif len(data[i][index]) == 2:
                    text = data[i][index][0]["name"] + " and " \
                           + data[i][index][1]["name"]
                else:
                    try:
                        text = data[i][index][0]["name"]
                    except IndexError:
                        text = "No " + index

                text_item = QTableWidgetItem(text)
                text_item.setTextAlignment(Qt.AlignCenter)
                if table_index == 1 and not \
                        self.ui.back_btn_local.isEnabled() and len(os.listdir(
                    os.path.join(self.backend_path, str(data[i]["id"])))) > 2:
                    text_item.setFlags(
                        Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                curr_table.setItem(i, j + 1, text_item)

            # Text for the header "Date Modified"
            date = QTableWidgetItem(data[i]["updated_at"][:10])
            date.setTextAlignment(Qt.AlignCenter)
            date.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            curr_table.setItem(i, 3, date)

            # If we are on tab index 0, we need a "Download" header item.
            if table_index == 0:
                dwn = QPushButton("Click me\nto download!", self)
                dwn.setFont(self.ui.table_PS.horizontalHeader().font())
                dwn.clicked.connect(self.initiate_download)
                dwn.setObjectName(str(data[i]["id"]))
                dwn.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, "
                    "x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 19), "
                    "stop:1 rgba(255, 255, 255, 255));")

                # Only enable it if we haven't already downloaded the patch.
                if (str(data[i]["id"])) in os.listdir(self.backend_path):
                    dwn.setEnabled(False)
                    dwn.setText("Downloaded!")
                curr_table.setCellWidget(i, 4, dwn)

            # If we are on tab index 1, we need "Export" and "Delete"
            # header items.
            elif table_index == 1:
                if "[Multiple Versions]" in btn_title.text():
                    expt = QPushButton("See Version\nHistory to\nexport!")
                    expt.setEnabled(False)
                else:
                    expt = QPushButton("Click me\nto export!")
                if self.ui.back_btn_local.isEnabled():
                    expt.setObjectName(str(data[i]["id"]) + "_v"
                                       + str(data[i]["revision"]))
                else:
                    expt.setObjectName(str(data[i]["id"]))
                expt.setFont(self.ui.table_PS.horizontalHeader().font())
                expt.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, "
                    "x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 19), "
                    "stop:1 rgba(255, 255, 255, 255));")
                expt.clicked.connect(self.initiate_export)
                curr_table.setCellWidget(i, 4, expt)

                delete = QPushButton("X")
                if self.ui.back_btn_local.isEnabled():
                    delete.setObjectName(str(data[i]["id"]) + "_v"
                                         + str(data[i]["revision"]))
                else:
                    delete.setObjectName(str(data[i]["id"]))
                delete.setFont(self.ui.table_PS.horizontalHeader().font())
                delete.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, "
                    "x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 19), "
                    "stop:1 rgba(255, 255, 255, 255));")
                delete.clicked.connect(self.initiate_delete)
                curr_table.setCellWidget(i, 5, delete)

        # Also set the title size and resize the columns.
        if table_index == 0:
            if self.ps_sizes is None:
                curr_table.resizeColumnsToContents()
                curr_table.setColumnWidth(1, self.width() * 0.1)
                curr_table.setColumnWidth(2, self.width() * 0.1)
                curr_table.setColumnWidth(3, self.width() * 0.1)
                self.ui.splitter_PS.setSizes([self.width() * 0.6,
                                              self.width() * 0.4])
                curr_table.resizeRowsToContents()
            else:
                curr_table.resizeRowsToContents()
            if self.local_sizes is None:
                curr_table.resizeColumnsToContents()
                curr_table.setColumnWidth(1, self.width() * 0.1)
                curr_table.setColumnWidth(2, self.width() * 0.1)
                curr_table.setColumnWidth(3, self.width() * 0.1)
                curr_table.setColumnWidth(4, self.width() * 0.05)
                curr_table.setColumnWidth(5, self.width() * 0.03)
                self.ui.splitter_local.setSizes([self.width() * 0.6,
                                                 self.width() * 0.4])
                curr_table.resizeRowsToContents()
            else:
                curr_table.resizeRowsToContents()

        else:
            if self.bank_sizes is None:
                curr_table.resizeColumnsToContents()
                curr_table.setColumnWidth(1, self.width() * 0.14)
                curr_table.setColumnWidth(2, self.width() * 0.14)
                curr_table.resizeRowsToContents()
            else:
                curr_table.resizeRowsToContents()

    def get_version_patches(self, context):
        """ Retrieves the versions of a patch that is locally stored to
        a user's backend local storage.

        context: True for the Local Storage View tab, False for the
                 Banks tab.
        """
        if self.sender() is None:
            idx = self.curr_ver
        else:
            idx = self.sender().objectName()
            if "_" in idx:
                idx = idx.split("_")[0]
            self.curr_ver = idx
        self.prev_tag_cat = None
        if context:
            self.data_local_version = []
            curr_data = self.data_local_version
        else:
            self.data_bank_version = []
            curr_data = self.data_bank_version

        # Get all of the patch versions into one place.
        for pch in os.listdir(os.path.join(self.backend_path, idx)):
            if pch.split(".")[1] == "json":
                # Got the metadata
                with open(os.path.join(self.backend_path, idx, pch)) as f:
                    temp = json.loads(f.read())
                curr_data.append(temp)

        if context:
            self.ui.update_patch_notes.setEnabled(False)

        self.ui.text_browser_bank.setText("")
        self.sort_and_set()

    def initiate_download(self):
        """ Attempts to download a patch from the PS API. Once the
        download completes, it will be saved to the backend application
        directory.

        Currently, only patches uploaded as .bin or .zip files will
        successfully download. Support for additional file formats will
        be implemented in subsequent releases.
        """

        self.ui.statusbar.showMessage("Starting download...",
                                      timeout=5000)

        # TODO Replace with FCFS thread scheduling
        try:
            save.save_to_backend(ps.download(str(
                self.sender().objectName())))
            self.sender().setEnabled(False)
            self.sender().setText("Downloaded!")
            self.ui.statusbar.showMessage("Download complete!", timeout=5000)
        except errors.SavingError:
            self.msg.setWindowTitle("Invalid File Type")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Unfortunately, that patch is not in a "
                             "supported format.")
            self.msg.setInformativeText("Supported formats are .bin and .zip")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setInformativeText(None)

    def initiate_export(self):
        """ Attempts to export a patch saved in the backend to an SD
        card. This requires that the user has previously set their SD
        card path using sd_path(). Should the patch be missing, a
        message prompt will inform the user that it must be specified.

        The application will ask for a slot number, and this is forced
        to be between 0 and 63 inclusive. Should the user specify a slot
        and the application detects that the slot is occupied by another
        patch on the SD card, the user will be asked if they wish to
        overwrite the other patch. If yes, exporting will export the new
        patch and delete the other patch that previously occupied the
        slot. If no, the user will be asked to enter a different slot
        number. At any point, the user can abort the operation by
        closing the message dialog or hitting the "Cancel" button.
        Currently triggered via a button press.
        """

        # Exporting this way will only export to a directory named "to_zoia"
        # So we need to check if it exists. If it doesn't, we create it.
        if self.sd.get_sd_root is None:
            # No SD path.
            self.msg.setWindowTitle("No SD Path")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please specify your SD card path!")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.sd.sd_path(False, self.width())
            self.msg.setInformativeText(None)
        else:
            if "to_zoia" not in os.listdir(self.sd.get_sd_root()):
                os.mkdir(os.path.join(self.sd.get_sd_root(), "to_zoia"))
            while True:
                # Ask for a slot
                slot, ok = QInputDialog().getInt(self, "Patch Export",
                                                 "Slot number:", minValue=0,
                                                 maxValue=63)

                if slot >= 0 and ok:
                    self.ui.statusbar.showMessage("Patch be movin",
                                                  timeout=5000)
                    # Got a slot and the user hit "OK"
                    try:
                        export.export_patch_bin(self.sender().objectName(),
                                                os.path.join(
                                                    self.sd.get_sd_root(),
                                                    "to_zoia"), slot)
                        self.ui.statusbar.showMessage("Export complete!",
                                                      timeout=5000)
                        break
                    except errors.ExportingError:
                        # There was already a patch in that slot.
                        self.msg.setWindowTitle("Slot Exists")
                        self.msg.setIcon(QMessageBox.Information)
                        self.msg.setText(
                            "That slot is occupied by another patch. "
                            "Would you like to overwrite it?")
                        self.msg.setStandardButtons(QMessageBox.Yes |
                                                    QMessageBox.No)
                        value = self.msg.exec_()
                        if value == QMessageBox.Yes:
                            # Overwrite the other patch.
                            try:
                                export.export_patch_bin(
                                    self.sender().objectName(),
                                    os.path.join(self.sd.get_sd_root(),
                                                 "to_zoia"),
                                    slot, True)
                                self.ui.statusbar.showMessage(
                                    "Export complete!", timeout=5000)
                            except FileNotFoundError:
                                idx = str(self.sender().objectName()) + "_v1"
                                export.export_patch_bin(idx, os.path.join(
                                    self.sd.get_sd_root(), "to_zoia"), slot,
                                                        True)
                                self.ui.statusbar.showMessage(
                                    "Export complete!", timeout=5000)
                            break
                        else:
                            continue
                    except FileNotFoundError:
                        idx = str(self.sender().objectName()) + "_v1"
                        export.export_patch_bin(idx,
                                                os.path.join(
                                                    self.sd.get_sd_root(),
                                                    "to_zoia"), slot,
                                                True)
                        self.ui.statusbar.showMessage(
                            "Export complete!", timeout=5000)
                        break
                else:
                    # Operation was aborted.
                    break

    def initiate_delete(self):
        """ Attempts to delete a patch that is stored on a user's local
        filesystem.
        """

        if "_" not in self.sender().objectName():
            if len(os.listdir(
                    os.path.join(self.backend_path,
                                 self.sender().objectName()))) > 2 \
                    and not self.ui.back_btn_local.isEnabled():
                delete.delete_full_patch_directory(self.sender().objectName())
            else:
                delete.delete_patch(self.sender().objectName())
            self.get_local_patches()
            self.sort_and_set()
            self.set_data()
        else:
            delete.delete_patch(os.path.join(self.curr_ver,
                                             self.sender().objectName()))
            self.get_version_patches(self.ui.tabs.currentIndex() == 1)

        # Reset the text browser.
        self.ui.text_browser_local.setText("")

    def get_local_patches(self):
        """ Retrieves the metadata for patches that a user has previously
        downloaded and saved to their machine's backend.
        """
        if self.ui.tabs.currentIndex() == 1:
            self.data_local = []
            curr_data = self.data_local
        else:
            self.data_bank = []
            curr_data = self.data_bank
        for patches in os.listdir(self.backend_path):
            # Look for patch directories in the backend.
            if patches != "Banks" and patches != "data.json" and \
                    patches != '.DS_Store' and patches != "pref.json":
                for pch in os.listdir(os.path.join(self.backend_path,
                                                   patches)):
                    # Read the metadata so that we can set up the tables.
                    if pch.split(".")[1] == "json":
                        with open(os.path.join(self.backend_path,
                                               patches, pch)) as f:
                            temp = json.loads(f.read())
                        curr_data.append(temp)
                        break

    def display_patch_info(self):
        """ Queries the PS API for additional patch information whenever
        a patch is selected in the PS table or local table. Information
        is displayed via HTML.

        Should the patch contain multiple versions, a call to
        display_patch_versions is ran instead.

        Currently triggered via a radio button selection.
        """

        if self.sender().isChecked():
            if (self.ui.tabs.currentIndex() == 1
                or self.ui.tabs.currentIndex() == 3) and \
                    "_" not in self.sender().objectName() and \
                    len(os.listdir(
                        os.path.join(self.backend_path,
                                     self.sender().objectName()))) > 2:
                # We are pointing to a version directory.
                self.display_patch_versions(
                    self.ui.tabs.currentIndex() == 1)
                return
            name = str(self.sender().objectName())
            ver = ""
            if "_" in self.sender().objectName():
                name, ver = name.split("_")
            temp = None
            if self.ui.tabs.currentIndex() == 0:
                temp = self.ui.text_browser_PS
                self.selected = name
                if len(self.patch_cache) == 0:
                    content = ps.get_patch_meta(name)
                    self.patch_cache.append(content)
                else:
                    content = None
                    for pch in self.patch_cache:
                        if str(pch["id"]) == name:
                            content = pch
                            break
                    if content is None:
                        content = ps.get_patch_meta(name)
                        self.patch_cache.append(content)
            else:
                if self.ui.tabs.currentIndex() == 1:
                    temp = self.ui.text_browser_local
                    self.ui.update_patch_notes.setEnabled(True)
                elif self.ui.tabs.currentIndex() == 3:
                    temp = self.ui.text_browser_bank
                self.local_selected = name
                if ver is not "":
                    self.local_selected += "_" + ver
                try:
                    with open(os.path.join(self.backend_path, name,
                                           name + ".json")) \
                            as f:
                        content = json.loads(f.read())
                except FileNotFoundError:
                    with open(os.path.join(self.backend_path,
                                           name,
                                           name + "_{}.json".format(ver))) \
                            as f:
                        content = json.loads(f.read())
            if content["preview_url"] == "":
                content["preview_url"] = "None provided"
            else:
                content["preview_url"] = "<a href=" + content["preview_url"] \
                                         + ">Click here</a>"
            if "license" not in content or content["license"] is None or \
                    content["license"]["name"] == "":
                legal = "None provided"
            else:
                legal = content["license"]["name"]
            content["content"] = content["content"].replace("\n", "<br/>")

            # TODO Add artwork to HTML view (test case when offline).

            temp.setHtml("<html><h3>"
                         + content["title"] + "</h3><u>Author:</u> "
                         + content["author"]["name"] + "<br/><u>Likes:</u> "
                         + str(content["like_count"])
                         + "<br/><u>Downloads:</u> "
                         + str(content["download_count"])
                         + "<br/><u>Views:</u> "
                         + str(content["view_count"]) + "<br/><u>License:</u> "
                         + legal + "<br/><u>Preview:</u> "
                         + content["preview_url"]
                         + "<br/><br/><u>Patch Notes:</u><br/>"
                         + content["content"] + "</html>")

    def display_patch_versions(self, context):
        """ Displays the contents of a patch that has multiple versions.
        Currently triggered via a button press.

        context: True for the Local Storage View tab, False for the
                 Banks tab.
        """
        if context:
            # Clean up the tab.
            self.ui.text_browser_local.setText("")
            self.ui.searchbar_local.setText("")
            self.ui.update_patch_notes.setEnabled(False)
            self.ui.back_btn_local.setEnabled(True)
            # Prepare the table.
            self.get_version_patches(True)
        else:
            # Clean up the tab.
            self.ui.text_browser_bank.setText("")
            self.ui.searchbar_bank.setText("")
            self.ui.back_btn_bank.setEnabled(True)
            # Prepare the table.
            self.get_version_patches(False)

    def reload_ps(self):
        """ Reloads the PS table view to accurately reflect new uploads.
        Currently triggered via a menu action.
        """

        # Get the new patch metadata that we don't have (if any).
        self.ui.refresh_pch_btn.setEnabled(False)
        self.data_PS = ps.get_all_patch_data_init()
        with open(os.path.join(self.backend_path, "data.json"), "w") as f:
            f.write(json.dumps(self.data_PS))
        self.ui.searchbar_PS.setText("")
        self.sort_and_set()
        self.ui.refresh_pch_btn.setEnabled(True)
        self.ui.statusbar.showMessage("Patch list refreshed!", timeout=5000)
        self.msg.setWindowTitle("Patches Refreshed")
        self.msg.setText("The PatchStorage patch list has been refreshed.")
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def search(self):
        """ Initiates a data search for the metadata that is retrieved
        via the PS API or that is stored locally. The search will then
        set the table to display the returned query matches.
        Currently triggered via a button press.
        """

        # Case 1: PS tab
        if self.ui.tabs.currentIndex() == 0 \
                and self.ui.searchbar_PS.text() != "":
            self.search_data_PS = \
                util.search_patches(self.data_PS,
                                    self.ui.searchbar_PS.text())
            self.set_data(True)
        # Case 2: Local tab
        elif self.ui.tabs.currentIndex() == 1 \
                and self.ui.searchbar_local.text() != "":
            # Case 2.1: No version
            if not self.ui.back_btn_local.isEnabled():
                self.search_data_local = \
                    util.search_patches(self.data_local,
                                        self.ui.searchbar_local.text())
                self.set_data(True)
            # Case 2.2: Version
            else:
                self.search_data_local_version = \
                    util.search_patches(self.data_local_version,
                                        self.ui.searchbar_local.text())
                self.set_data(True, True)
        # Case 3: Bank tab
        elif self.ui.tabs.currentIndex() == 3 \
                and self.ui.searchbar_bank.text() != "":
            # Case 3.1: No version
            if not self.ui.back_btn_bank.isEnabled():
                self.search_data_bank = \
                    util.search_patches(self.data_bank,
                                        self.ui.searchbar_bank.text())
                self.set_data(True)
            # Case 3.2: Version
            else:
                self.search_data_bank_version = \
                    util.search_patches(self.data_bank_version,
                                        self.ui.searchbar_bank.text())
                self.set_data(True, True)

    def sort_and_set(self):
        """ Sorts and sets the metadata in a table depending on the
        option selection via the menu.
        Currently triggered via a menu action.
        """

        # Determine how to sort the data.
        try:
            curr_sort = {
                "refresh_pch_btn": (6, True),
                "tabs": (6, True),
                "actionSort_by_title_A_Z": (1, False),
                "actionSort_by_title_Z_A": (1, True),
                "actionSort_by_date_new_old": (6, True),
                "actionSort_by_date_old_new": (6, False),
                "actionSort_by_likes_high_low": (3, True),
                "actionSort_by_likes_low_high": (3, False),
                "actionSort_by_views_high_low": (5, True),
                "actionSort_by_views_low_high": (5, False),
                "actionSort_by_downloads_high_low": (4, True),
                "actionSort_by_downloads_low_high": (4, False)
            }[self.sender().objectName()]
            self.prev_sort = curr_sort
        except KeyError:
            curr_sort = self.prev_sort
        except AttributeError:
            curr_sort = (6, True)
            self.prev_sort = curr_sort

        table_index = self.ui.tabs.currentIndex()

        # Determine the context in which to perform the sort.
        # Case 1: A user forces a reload of the PS patch list.
        if self.sender() is not None and self.sender().objectName() == \
                "refresh_pch_btn":
            util.sort_metadata(curr_sort[0], self.data_PS, curr_sort[1])
            self.set_data(self.ui.searchbar_PS.text() != "")
        # Case 2: Sorting on the PatchStorage tab.
        # ->Case 2.1: Sorting on the PS tab with the search bar empty.
        elif table_index == 0 and self.ui.searchbar_PS.text() == "":
            util.sort_metadata(curr_sort[0], self.data_PS, curr_sort[1])
            self.set_data()
        # ->Case 2.2: Sorting on the PS tab with the search bar containing
        #             text.
        elif table_index == 0 and self.ui.searchbar_PS.text() != "":
            if self.search_data_PS is None:
                self.search_data_PS = self.data_PS
            util.sort_metadata(curr_sort[0], self.search_data_PS,
                               curr_sort[1])
            self.set_data(True)
        # Case 3: Sorting on the Local Storage View tab.
        # ->Case 3.1: Sorting on the Local tab, no version, and an empty
        #             search bar
        elif table_index == 1 and self.ui.searchbar_local.text() == "" \
                and not self.ui.back_btn_local.isEnabled():
            util.sort_metadata(curr_sort[0], self.data_local, curr_sort[1])
            self.set_data()
        # ->Case 3.2: Local tab, no version, text in the search bar.
        elif table_index == 1 and self.ui.searchbar_local.text() != "" \
                and not self.ui.back_btn_local.isEnabled():
            if self.search_data_local is None:
                self.search_data_local = self.data_local
            util.sort_metadata(curr_sort[0], self.search_data_local,
                               curr_sort[1])
            self.set_data(True)
        # ->Case 3.3: Local tab, it is a version, no text in the search bar.
        elif table_index == 1 and self.ui.searchbar_local.text() == "" \
                and self.ui.back_btn_local.isEnabled():
            util.sort_metadata(7, self.data_local_version,
                               False)
            self.set_data(version=True)
        # ->Case 3.4: Local tab, it is a version, and text is in the search
        #             bar.
        elif table_index == 1 and self.ui.searchbar_local.text() != "" \
                and self.ui.back_btn_local.isEnabled():
            if self.search_data_local_version is None:
                self.search_data_local_version = self.data_local_version
            util.sort_metadata(7, self.search_data_local_version,
                               False)
            self.set_data(True, True)
        # Case 4: Sorting on the Banks tab.
        # ->Case 4.1: Sorting on the Banks tab, no version, and an empty search
        #             bar.
        elif table_index == 3 and self.ui.searchbar_bank.text() == "" \
                and not self.ui.back_btn_bank.isEnabled():
            util.sort_metadata(curr_sort[0], self.data_bank, curr_sort[1])
            self.set_data()
        # ->Case 4.2: Bank tab, no version, text in the search bar.
        elif table_index == 3 and self.ui.searchbar_bank.text() != "" \
                and not self.ui.back_btn_bank.isEnabled():
            if self.search_data_bank is None:
                self.search_data_bank = self.data_bank
            util.sort_metadata(curr_sort[0], self.search_data_bank,
                               curr_sort[1])
            self.set_data(True)
        # ->Case 4.3: Bank tab, it is a version, no text in the search bar.
        elif table_index == 3 and self.ui.searchbar_bank.text() == "" \
                and self.ui.back_btn_bank.isEnabled():
            util.sort_metadata(7, self.data_bank_version,
                               False)
            self.set_data(version=True)
        # ->Case 4.4: Bank tab, it is a version, and text is in the search bar.
        elif table_index == 3 and self.ui.searchbar_bank.text() != "" \
                and self.ui.back_btn_bank.isEnabled():
            if self.search_data_bank_version is None:
                self.search_data_bank_version = self.data_bank_version
            util.sort_metadata(7, self.search_data_bank_version,
                               False)
            self.set_data(True, True)

    def update_local_patches(self):
        """ Attempts to update any patch that is stored in the user's
        backend directory.

        TODO List which patches were updated.
        """

        self.ui.statusbar.showMessage("Checking for updates...",
                                      timeout=5000)
        count = update.check_for_updates()
        if count == 0:
            self.msg.setWindowTitle("No Updates")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("All of the patches you have downloaded are "
                             "the latest version!")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
        else:
            self.msg.setWindowTitle("Updates")
            self.msg.setIcon(QMessageBox.Information)
            if count == 1:
                self.msg.setText("Successfully updated 1 patch.")
            else:
                self.msg.setText(
                    "Successfully updated " + str(count) + " patches.")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()

    def update_patch_notes(self):
        """ Updates the patch notes for a patch that has been previously
        locally saved to a user's machine.
        Currently triggered via a button click.
        """

        text = self.ui.text_browser_local.toPlainText()
        try:
            text = text.split("Patch Notes:")[1]
            update.update_data(self.local_selected, text.strip("\n"), 3)
        except IndexError:
            update.update_data(self.local_selected, "", 3)
        self.ui.statusbar.showMessage("Successfully updated patch notes.",
                                      timeout=5000)

    def import_patch(self):
        """ Attempts to import a patch into the librarian.
        Currently triggered via a menu action.
        """

        # Prepare a message box.
        self.msg.setWindowTitle("Patch Already In Library")
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("That patch exists within your locally "
                         "saved patches.\nNo importing has occurred.")
        self.msg.setStandardButtons(QMessageBox.Ok)

        if self.sd.get_sd_path() is not None and \
                self.ui.tabs.currentIndex() == 2:
            for sd_pch in os.listdir(self.sd.get_sd_path()):
                try:
                    index = int(self.sender().objectName())
                except ValueError:
                    break
                if index < 10:
                    index = "00{}".format(index)
                else:
                    index = "0{}".format(index)
                if index == sd_pch[:3]:
                    try:
                        save.import_to_backend(
                            os.path.join(self.sd.get_sd_path(), sd_pch))
                        self.ui.statusbar.showMessage("Import complete!")
                        self.msg.setWindowTitle("Import Complete")
                        self.msg.setText(
                            "The patch has been successfully imported!")
                        self.msg.exec_()
                        return
                    except errors.SavingError:
                        self.msg.exec_()
                        self.msg.setInformativeText(None)
                        return

        pch = QFileDialog.getOpenFileName()[0]
        if pch == "":
            return
        try:
            save.import_to_backend(pch)
            if self.ui.tabs.currentIndex() == 1:
                self.get_local_patches()
                self.sort_and_set()
                self.set_data(self.ui.searchbar_local.text() != "")
            self.ui.statusbar.showMessage("Import complete!")
            self.msg.setWindowTitle("Import Complete")
            self.msg.setText("The patch has been successfully imported!")
            self.msg.exec_()
            if (self.ui.tabs.currentIndex() == 1 and not
                self.ui.back_btn_local.isEnabled()) or \
                    (self.ui.tabs.currentIndex() == 3 and not
                     self.ui.back_btn_bank.isEnabled()):
                self.get_local_patches()
                self.sort_and_set()

        except errors.BadPathError:
            self.msg.setWindowTitle("No Patch Found")
            self.msg.setText("Incorrect file selected, importing failed.")
            self.msg.exec_()
        except errors.SavingError:
            self.msg.exec_()

    def mass_import(self):
        """ Attempts to mass import any patches found within a target
        directory. Unlike import_patch, failing to import a patch will
        not create a message box. A message box will be displayed at the
        end indicating how many patches were and were not imported.
        Currently triggered via a button press.
        """
        imp_cnt = 0
        fail_cnt = 0
        if self.sender() is not None and self.sender().objectName() == \
                "actionImport_Multiple_Patches":
            input_dir = QFileDialog.getExistingDirectory(None,
                                                         'Select a directory',
                                                         expanduser("~"))

            if input_dir is "" or not os.path.isdir(input_dir):
                self.msg.setWindowTitle("Invalid Selection")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Please select a directory.")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                return
        else:
            input_dir = self.sd.get_sd_path()
        for pch in os.listdir(input_dir):
            if pch.split(".")[1] == "bin":
                # At this point we have done everything to ensure it's a
                # ZOIA patch, save for binary analysis.
                try:
                    save.import_to_backend(os.path.join(input_dir, pch))
                    imp_cnt += 1
                except errors.SavingError:
                    fail_cnt += 1
                    continue

        self.msg.setWindowTitle("Import Complete")
        self.msg.setIcon(QMessageBox.Information)
        if imp_cnt > 0:
            self.msg.setText(
                "Successfully imported {} patches.".format(imp_cnt))
        else:
            self.msg.setText("Did not import any patches.")
        if fail_cnt > 0:
            if fail_cnt == 1:
                self.msg.setInformativeText(
                    "{} was already saved in the library "
                    "and was not "
                    "imported.".format(fail_cnt))
            else:
                self.msg.setInformativeText(
                    "{} were already saved in the library "
                    "and were not "
                    "imported.".format(fail_cnt))
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
        self.msg.setInformativeText(None)
        self.get_local_patches()
        self.sort_and_set()

    def version_import(self):
        if self.sender().objectName() != "import_all_ver_btn":
            input_dir = QFileDialog.getExistingDirectory(None,
                                                         'Select a directory',
                                                         expanduser("~"))
            if input_dir is "" or not os.path.isdir(input_dir):
                self.msg.setWindowTitle("Invalid Selection")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Please select a directory.")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                return
        else:
            input_dir = self.sd.get_sd_path()
        fails = save.import_to_backend(input_dir, True)
        if fails == 0:
            self.msg.setWindowTitle("Success")
            self.msg.setText("Successfully created a Version History.")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            return
        else:
            self.msg.setWindowTitle("Warning")
            self.msg.setText("Certain patches in the specified Version History"
                             "already existed in the Librarian. Please delete"
                             "them before attempting to import a version "
                             "history if you would like them to appear.")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            return
        if (self.ui.tabs.currentIndex() == 1 and not
            self.ui.back_btn_local.isEnabled()) or \
                (self.ui.tabs.currentIndex() == 3 and not
                 self.ui.back_btn_bank.isEnabled()):
            self.get_local_patches()
            self.sort_and_set()

    def eventFilter(self, o, e):
        """ Deals with events that originate from various widgets
        present in the GUI.

        o: The source object that triggered the event.
        e: The event that was triggered.
        """

        # SD card tab swap/move
        if o.objectName() == "table_sd_left" or o.objectName() == \
                "table_sd_right":
            self.sd.events(o, e)
        elif o.objectName() == "table_bank_local" or o.objectName() == \
                "table_bank_left" or o.objectName() == "table_bank_right":
            self.bank.events(o, e)
        elif o.objectName() == "searchbar_PS" \
                or o.objectName() == "searchbar_local" \
                or o.objectName() == "searchbar_bank":
            if e.type() == QEvent.KeyRelease:
                if self.ui.searchbar_local.text() == "" \
                        and self.ui.tabs.currentIndex() == 1 \
                        and not self.ui.back_btn_local.isEnabled():
                    self.set_data()
                elif self.ui.searchbar_PS.text() == "" \
                        and self.ui.tabs.currentIndex() == 0:
                    self.set_data()
                elif self.ui.searchbar_local.text() == "" \
                        and self.ui.tabs.currentIndex() == 1 \
                        and self.ui.back_btn_local.isEnabled():
                    self.get_version_patches(True)
                    self.set_data(version=True)
                elif self.ui.searchbar_bank.text() == "" \
                        and self.ui.tabs.currentIndex() == 3 \
                        and not self.ui.back_btn_bank.isEnabled():
                    self.get_local_patches()
                    self.set_data()
                elif self.ui.searchbar_bank.text() == "" \
                        and self.ui.tabs.currentIndex() == 3 \
                        and self.ui.back_btn_bank.isEnabled():
                    self.get_version_patches(False)
                    self.set_data(version=True)
                return True
        elif o.objectName() == "table_local":
            if e.type() == QEvent.FocusIn:
                if self.prev_tag_cat is None:
                    return False
                else:
                    new_text = self.ui.table_local.item(self.prev_tag_cat[0],
                                                        self.prev_tag_cat[1]
                                                        ).text()
                    if new_text == self.prev_tag_cat[2] \
                            or self.ui.table_local.currentColumn() == 3:
                        return False
                    else:
                        self.update_tags_cats(
                            new_text, self.prev_tag_cat[1] == 1,
                            self.ui.table_local.cellWidget(
                                self.ui.table_local.currentRow(),
                                4).objectName())
                        return True
            elif e.type() == QEvent.FocusOut:
                try:
                    if self.ui.table_local.currentColumn() != 3:
                        self.prev_tag_cat = (
                            self.ui.table_local.currentRow(),
                            self.ui.table_local.currentColumn(),
                            self.ui.table_local.selectedItems()[0].text())
                    return True
                except IndexError:
                    return False
        return False

    def update_tags_cats(self, text, mode, idx):
        """ Updates the tags or categories for a locally downloaded
        patch.

        text: The text used to discern tags and categories from.
        mode: True for tags update, False for categories update.
        """

        # Case 1 - The text is empty (i.e., delete everything)
        if text == "":
            if mode:
                update.update_data(idx, [], 1)
            else:
                update.update_data(idx, [], 2)
            if not self.ui.back_btn_local.isEnabled():
                self.get_local_patches()
                self.sort_and_set()
                self.set_data(self.ui.searchbar_local != "")
            else:
                self.get_version_patches(True)
        # Case 2 - Leftover text from when there are no tags/categories
        elif text == "No tags" or text == "No categories":
            pass
        # Case 3 - The text isn't empty and contains tags/categories
        else:
            # Tags/categories are separated by commas
            items = text.split(",")
            done = []
            for curr in items:
                curr = curr.strip()
                if " and " in curr and curr[0] != " ":
                    # They listed tags as "This and that"
                    done.append({
                        "name": curr.split(" and ")[0]
                    })
                    curr = curr.split(" and ")[1]
                elif "and " in curr and curr[0:3] == "and":
                    curr = curr.split("and ")[1]
                done.append({
                    "name": curr
                })
            if mode:
                update.update_data(idx, done, 1)
            else:
                update.update_data(idx, done, 2)
            if not self.ui.back_btn_local.isEnabled():
                self.get_local_patches()
                self.sort_and_set()
            else:
                self.get_version_patches(True)

    def go_back(self):
        """ Returns to the default local patch screen.
        Currently triggered via a button press.
        """

        # Do the necessary cleanup depending on the context.
        if self.sender().objectName() == "back_btn_local":
            self.ui.searchbar_local.setText("")
            self.ui.text_browser_local.setText("")
            self.ui.back_btn_local.setEnabled(False)
            self.ui.update_patch_notes.setEnabled(False)
        elif self.sender().objectName() == "back_btn_bank":
            self.ui.searchbar_bank.setText("")
            self.ui.text_browser_bank.setText("")
            self.ui.back_btn_bank.setEnabled(False)
        # Sort and display the data.
        self.get_local_patches()
        self.sort_and_set()

    def closeEvent(self, event):
        """ Override the default close operation so certain application
        settings can be saved.
        """

        self.util.save_pref(self.width(), self.height(), self.sd.get_sd_root(),
                            self.backend_path)

    def try_quit(self):
        """ Forces the application to close.
        Currently triggered via a menu action.
        """

        # Save application settings and then exit.
        self.closeEvent(None)
        self.close()
