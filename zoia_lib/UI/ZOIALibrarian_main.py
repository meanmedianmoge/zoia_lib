import json
import os
from os.path import expanduser

from PySide2.QtCore import QEvent
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import zoia_lib.UI.ZOIALibrarian as ui_main
import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors
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
backend_path = save.get_backend_path()
icon = QIcon(os.path.join(os.getcwd(), "zoia_lib", "UI", "resources",
                          "logo.ico"))


class ZOIALibrarianMain(QMainWindow):
    """ The ZOIALibrarian_Main class represents the frontend for the
    application. It allows users to interact with the various backend
    functions available. These include searching, downloading, sorting,
    and exporting patches; among other functions.

    Any changes made to the .ui file will not be reflected unless the
    following command is run from the UI directory:
        pyside2-uic.exe .\ZOIALibrarian.ui -o .\ZOIALibrarian/.py

    Known issues:
     - Sorting order is not maintained when exiting out of the
       version history table of a patch.
     - The code is a mess and should be refactored into separate classes
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

        # Variable initialization.
        self.data_PS = None
        self.data_banks = None
        self.search_data_PS = None
        self.search_data_local = None
        self.search_data_bank = None
        self.data_local = None
        self.search_data_local_version = None
        self.search_data_bank_version = None
        self.data_local_version = None
        self.data_bank = None
        self.data_bank_version = None
        self.sd_card_root = None
        self.sd_card_path = None
        self.local_selected = None
        self.selected = None
        self.prev_tag_cat = None
        self.dark = False
        self.table_title_size = None
        self.table_local_title_size = None
        self.table_bank_local_title_size = None
        self.prev_sort = None
        self.curr_ver = None
        self.can_export_bank = False

        # Check for metadata in the user's backend.
        if "data.json" not in os.listdir(backend_path):
            ps_data = ps.get_all_patch_data_init()
            with open(os.path.join(backend_path, "data.json"),
                      "w") as f:
                f.write(json.dumps(ps_data))
                self.data_PS = ps_data
        else:
            # Got previous metadata, need to ensure that there are no
            # new patches.
            with open(os.path.join(backend_path, "data.json"),
                      "r") as f:
                data = json.loads(f.read())
            if len(data) == ps.patch_count:
                # Assume no new patches; allow the user to refresh manually.
                self.data_PS = data
            elif len(data) > ps.patch_count:
                # Uh oh, some patches got deleted on PatchStorage.
                ps_data = ps.get_all_patch_data_init()
                with open(os.path.join(backend_path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(ps_data))
                    self.data_PS = ps_data
            else:
                # Get the new patch metadata that we don't have.
                new_patches = ps.get_newest_patches(len(data))
                data = new_patches + data
                with open(os.path.join(backend_path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(data))
                    self.data_PS = data

        # Set the window icon
        self.setWindowIcon(QIcon(icon))

        # Setup the headers for the tables.
        self.ui.table_PS.setHorizontalHeaderLabels(["Title", "Tags",
                                                    "Categories",
                                                    "Date Modified",
                                                    "Download"])
        self.ui.table_local.setHorizontalHeaderLabels(["Title", "Tags",
                                                       "Categories",
                                                       "Date Modified",
                                                       "Export", "Delete"])
        self.ui.table_sd_left.setHorizontalHeaderLabels(["Patch", "Remove",
                                                         "Import"])
        self.ui.table_sd_right.setHorizontalHeaderLabels(["Patch", "Remove",
                                                          "Import"])
        self.ui.table_bank_local.setHorizontalHeaderLabels(["Title", "Tags",
                                                            "Categories",
                                                            "Date Modified"])
        self.ui.table_bank_left.setHorizontalHeaderLabels(["Patch", "Remove"])
        self.ui.table_bank_right.setHorizontalHeaderLabels(["Patch", "Remove"])

        # Forcing some column widths ahead of time.
        self.ui.table_sd_left.setColumnWidth(0, self.width() * 0.4)
        self.ui.table_sd_left.setColumnWidth(1, self.width() * 0.1)
        self.ui.table_sd_right.setColumnWidth(0, self.width() * 0.4)
        self.ui.table_sd_right.setColumnWidth(1, self.width() * 0.1)
        self.ui.table_bank_left.setColumnWidth(0, self.width() * 0.2)
        self.ui.table_bank_left.setColumnWidth(1, self.width() * 0.1)
        self.ui.table_bank_right.setColumnWidth(0, self.width() * 0.2)
        self.ui.table_bank_right.setColumnWidth(1, self.width() * 0.1)

        # Disabling widgets the user doesn't have access to on startup.
        self.ui.tab_sd.setEnabled(False)
        self.ui.update_patch_notes.setEnabled(False)
        self.ui.import_all_btn.setEnabled(False)
        self.ui.back_btn_local.setEnabled(False)
        self.ui.back_btn_bank.setEnabled(False)
        self.ui.btn_save_bank.setEnabled(False)
        self.ui.btn_export_bank.setEnabled(False)

        # Connect buttons and items to methods.
        self.ui.tabs.currentChanged.connect(self.tab_switch)
        self.ui.actionAlternating_Row_Colours.triggered.connect(
            self.row_invert)
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
        self.ui.actionSpecify_SD_Card_Location.triggered.connect(self.sd_path)
        self.ui.actionImport_Multiple_Patches.triggered.connect(
            self.mass_import)
        self.ui.check_for_updates_btn.clicked.connect(self.update)
        self.ui.refresh_pch_btn.clicked.connect(self.reload_ps)
        self.ui.actionQuit.triggered.connect(self.try_quit)
        self.ui.update_patch_notes.clicked.connect(self.update_patch_notes)
        self.ui.actionImport_A_Patch.triggered.connect(self.import_patch)
        self.ui.actionToggle_Dark_Mode.triggered.connect(self.toggle_darkmode)
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
        self.ui.sd_tree.clicked.connect(self.prepare_sd_view)
        self.ui.import_all_btn.clicked.connect(self.mass_import)
        self.ui.back_btn_local.clicked.connect(self.go_back)
        self.ui.back_btn_bank.clicked.connect(self.go_back)
        self.ui.btn_load_bank.clicked.connect(self.load_bank)
        self.ui.btn_save_bank.clicked.connect(self.save_bank)
        self.ui.btn_export_bank.clicked.connect(self.export_bank)

        # Font consistency.
        self.ui.table_PS.setFont(QFont('Verdana', 10))
        self.ui.table_local.setFont(QFont('Verdana', 10))
        self.ui.table_sd_left.setFont(QFont('Verdana', 10))
        self.ui.table_sd_right.setFont(QFont('Verdana', 10))
        self.ui.table_bank_local.setFont(QFont('Verdana', 10))
        self.ui.table_bank_left.setFont(QFont('Verdana', 10))
        self.ui.table_bank_right.setFont(QFont('Verdana', 10))
        self.ui.text_browser_PS.setFont(QFont('Verdana', 16))
        self.ui.text_browser_local.setFont(QFont('Verdana', 16))
        self.ui.text_browser_bank.setFont(QFont('Verdana', 16))

        # Modify the display sizes for some widgets.
        self.ui.splitter_PS.setSizes([self.width() * 0.325,
                                      self.width() * 0.675])
        self.ui.splitter_local.setSizes([self.width() * 0.325,
                                         self.width() * 0.675])
        self.ui.splitter_sd_hori.setSizes([self.width() * 0.5,
                                           self.width() * 0.5])
        self.ui.splitter_bank_tables.setSizes([self.width() * 0.5,
                                               self.width() * 0.5])
        self.ui.splitter_sd_vert.setSizes([self.width() * 0.185,
                                           self.width() * 0.815])
        self.ui.splitter_bank.setSizes([self.width() * 0.25, self.width() *
                                        0.25, self.width() * 0.5])

        # Sort and set the data.
        self.sort_and_set()

        # Ensure the application starts as maximized.
        self.setFocusPolicy(Qt.StrongFocus)
        self.showMaximized()

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
            if self.sd_card_root is None:
                msg = QMessageBox()
                msg.setWindowTitle("No SD Path")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(icon)
                msg.setText("Please specify your SD card path!")
                msg.setInformativeText("File -> Specify SD Card Location")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.ui.tabs.setCurrentIndex(1)

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
        for patches in os.listdir(backend_path):
            # Look for patch directories in the backend.
            if patches != "Banks" and patches != "data.json" and \
                    patches != '.DS_Store':
                for pch in os.listdir(os.path.join(backend_path,
                                                   patches)):
                    # Read the metadata so that we can set up the tables.
                    if pch.split(".")[1] == "json":
                        with open(os.path.join(backend_path,
                                               patches, pch)) as f:
                            temp = json.loads(f.read())
                        curr_data.append(temp)
                        break

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
        for pch in os.listdir(os.path.join(backend_path, idx)):
            if pch.split(".")[1] == "json":
                # Got the metadata
                with open(os.path.join(backend_path, idx, pch)) as f:
                    temp = json.loads(f.read())
                curr_data.append(temp)

        if context:
            self.ui.text_browser_local.setText("")
            self.ui.update_patch_notes.setEnabled(False)
            self.sort_and_set()
        else:
            self.ui.text_browser_bank.setText("")
            self.sort_and_set()

    def prepare_sd_view(self):
        """ Prepare the SD Card tab after an SD card location
        has been specified.
        """

        self.ui.import_all_btn.setEnabled(False)
        path = self.ui.sd_tree.currentIndex().data()
        temp = self.ui.sd_tree.currentIndex()
        while True:
            temp = temp.parent()
            if temp.data() is not None and self.sd_card_root \
                    not in temp.data():
                path = os.path.join(temp.data(), path)
                continue
            break
        self.sd_card_path = os.path.join(self.sd_card_root, path)
        self.set_data_sd()
        # If any patches populate the tables, enable the import all button.
        # TODO Find out if this can be determined without iterating through the
        #  entire table.
        for i in range(64):
            if i < 32:
                if self.ui.table_sd_left.item(i, 0).text() != "":
                    self.ui.import_all_btn.setEnabled(True)
                    break
            else:
                if self.ui.table_sd_right.item(i - 32, 0).text() != "":
                    self.ui.import_all_btn.setEnabled(True)
                    break

    def set_data_sd(self):
        """ Sets the data for the SD card table.
        """

        # Cleanup the tables
        for i in range(32):
            self.ui.table_sd_left.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_sd_left.setCellWidget(i, 1, None)
            self.ui.table_sd_left.setCellWidget(i, 2, None)
            self.ui.table_sd_right.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_sd_right.setCellWidget(i, 1, None)
            self.ui.table_sd_right.setCellWidget(i, 2, None)

        # Make sure we have an sd_card_path to work with.
        if not os.path.isdir(self.sd_card_path):
            return

        for pch in os.listdir(self.sd_card_path):
            # Get the index
            index = pch.split("_")[0]
            if index[0] == "0":
                # Get the useful int index.
                index = int(index[1:3])

                # Setup the buttons we are adding
                push_button = QPushButton("X")
                push_button.setObjectName(str(index))
                push_button.setFont(QFont('Verdana', 10))
                push_button.clicked.connect(self.remove_sd)

                import_btn = QPushButton("Click me to import!")
                import_btn.setObjectName(str(index))
                import_btn.setFont(QFont('Verdana', 10))
                import_btn.clicked.connect(self.import_patch)

                if index < 32:
                    # Left sd table.
                    self.ui.table_sd_left.setItem(index, 0,
                                                  QTableWidgetItem(pch))
                    self.ui.table_sd_left.setCellWidget(index, 1, push_button)
                    self.ui.table_sd_left.setCellWidget(index, 2, import_btn)
                else:
                    # Right sd table.
                    self.ui.table_sd_right.setItem(index - 32, 0,
                                                   QTableWidgetItem(pch))
                    self.ui.table_sd_right.setCellWidget(index - 32, 1,
                                                         push_button)
                    self.ui.table_sd_right.setCellWidget(index - 32, 2,
                                                         import_btn)

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

        curr_table = {
            0: self.ui.table_PS,
            1: self.ui.table_local,
            3: self.ui.table_bank_local
        }[table_index]

        # Clear the contents of the table
        curr_table.clearContents()

        # Figure out the data we are using.
        if table_index == 0:
            if search:
                data = self.search_data_PS
            else:
                data = self.data_PS
        elif table_index == 1:
            if version:
                if search:
                    data = self.search_data_local_version
                else:
                    data = self.data_local_version
            else:
                if search:
                    data = self.search_data_local
                else:
                    data = self.data_local
        else:
            if version:
                if search:
                    data = self.search_data_bank_version
                else:
                    data = self.data_bank_version
            else:
                if search:
                    data = self.search_data_bank
                else:
                    data = self.data_bank

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
                if len(os.listdir(os.path.join(backend_path,
                                               str(data[i]["id"])))) > 2:
                    btn_title.setText(title.rstrip() + "\n[Multiple Versions]")
                btn_title.setObjectName(str(data[i]["id"]))
            else:
                btn_title.setObjectName(str(data[i]["id"]))
            btn_title.toggled.connect(self.display_patch_info)
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
                    os.path.join(backend_path, str(data[i]["id"])))) > 2:
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
                dwn.setFont(QFont('Verdana', 10))
                dwn.clicked.connect(self.initiate_download)
                dwn.setObjectName(str(data[i]["id"]))

                # Only enable it if we haven't already downloaded the patch.
                if (str(data[i]["id"])) in os.listdir(backend_path):
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
                expt.setFont(QFont('Verdana', 10))
                expt.clicked.connect(self.initiate_export)
                curr_table.setCellWidget(i, 4, expt)

                delete = QPushButton("X")
                if self.ui.back_btn_local.isEnabled():
                    delete.setObjectName(str(data[i]["id"]) + "_v"
                                         + str(data[i]["revision"]))
                else:
                    delete.setObjectName(str(data[i]["id"]))
                delete.setFont(QFont('Verdana', 10))
                delete.clicked.connect(self.initiate_delete)
                curr_table.setCellWidget(i, 5, delete)

        # Also set the title size and resize the columns.
        # TODO Replace magic numbers with calculated values.
        if table_index == 0:
            curr_table.resizeColumnsToContents()
            if self.table_title_size is None:
                self.table_title_size = curr_table.columnWidth(0)
            else:
                curr_table.setColumnWidth(0, self.table_title_size)
            curr_table.setColumnWidth(1, 140)
            curr_table.setColumnWidth(2, 140)
            curr_table.resizeRowsToContents()
        elif table_index == 1:
            curr_table.resizeColumnsToContents()
            if self.table_local_title_size is None:
                self.table_local_title_size = curr_table.columnWidth(0)
            else:
                curr_table.setColumnWidth(0, self.table_local_title_size)
            curr_table.setColumnWidth(1, 140)
            curr_table.setColumnWidth(2, 140)
            curr_table.setColumnWidth(4, 100)
            curr_table.setColumnWidth(5, 50)
            curr_table.resizeRowsToContents()
        else:
            curr_table.resizeColumnsToContents()
            if self.table_bank_local_title_size is None:
                self.table_bank_local_title_size = curr_table.columnWidth(
                    0)
            else:
                curr_table.setColumnWidth(0,
                                          self.table_bank_local_title_size)
            curr_table.setColumnWidth(1, 140)
            curr_table.setColumnWidth(2, 140)
            curr_table.setColumnWidth(3, 100)
            curr_table.resizeRowsToContents()

    def set_data_bank(self):
        """ Populates the bank export tables with data..
        """

        # Cleanup the tables
        for i in range(32):
            self.ui.table_bank_left.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_bank_left.setItem(i, 1, QTableWidgetItem(None))
            self.ui.table_bank_left.setCellWidget(i, 1, None)
            self.ui.table_bank_right.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_bank_right.setItem(i, 1, QTableWidgetItem(None))
            self.ui.table_bank_right.setCellWidget(i, 1, None)

        # PyQt tables make zero sense.
        self.ui.table_bank_left.clearContents()
        self.ui.table_bank_right.clearContents()

        for pch in self.data_banks:
            idx = pch["id"]
            slot = pch["slot"]
            ver = None
            if "_" not in idx:
                with open(os.path.join(backend_path,
                                       idx, "{}.json".format(idx)), "r") as f:
                    temp = json.loads(f.read())
            else:
                idx, ver = idx.split("_")
                with open(os.path.join(backend_path,
                                       idx, "{}_{}.json".format(idx, ver)),
                          "r") as f:
                    temp = json.loads(f.read())
            name = temp["files"][0]["filename"]
            rmv_button = QPushButton("Remove")
            rmv_button.setObjectName(str(temp["id"]))
            if ver is not None:
                rmv_button.setObjectName(str(temp["id"]) + "_" + ver)
            else:
                rmv_button.setObjectName(str(temp["id"]))
            rmv_button.clicked.connect(self.remove_bank_item)
            if "_zoia_" in name and len(name.split("_", 1)[0]) == 3:
                name = name.split("_", 2)[2]
            elif len(name.split("_", 1)[0]) == 3:
                name = name.split("_", 1)[1]
            if slot < 10:
                name = "00{}_zoia_".format(slot) + name
            else:
                name = "0{}_zoia_".format(slot) + name
            if slot < 32:
                self.ui.table_bank_left.setItem(
                    slot, 0, QTableWidgetItem(name))
                self.ui.table_bank_left.setCellWidget(
                    slot, 1, rmv_button)
            else:
                self.ui.table_bank_right.setItem(
                    slot - 32, 0, QTableWidgetItem(name))
                self.ui.table_bank_right.setCellWidget(
                    slot - 32, 1, rmv_button)

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
            msg = QMessageBox()
            msg.setWindowTitle("Invalid File Type")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Unfortunately, that patch is not in a "
                        "supported format.")
            msg.setInformativeText("Supported formats are .bin and .zip")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

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
        if self.sd_card_root is None:
            # No SD path.
            msg = QMessageBox()
            msg.setWindowTitle("No SD Path")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please specify your SD card path!")
            msg.setInformativeText("File -> Specify SD Card Location")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            if "to_zoia" not in os.listdir(self.sd_card_root):
                os.mkdir(os.path.join(self.sd_card_root, "to_zoia"))
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
                                                os.path.join(self.sd_card_root,
                                                             "to_zoia"), slot)
                        self.ui.statusbar.showMessage("Export complete!",
                                                      timeout=5000)
                        break
                    except errors.ExportingError:
                        # There was already a patch in that slot.
                        msg = QMessageBox()
                        msg.setWindowTitle("Slot Exists")
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("That slot is occupied by another patch. "
                                    "Would you like to overwrite it?")
                        msg.setStandardButtons(QMessageBox.Yes |
                                               QMessageBox.No)
                        value = msg.exec_()
                        if value == QMessageBox.Yes:
                            # Overwrite the other patch.
                            try:
                                export.export_patch_bin(
                                    self.sender().objectName(),
                                    os.path.join(self.sd_card_root, "to_zoia"),
                                    slot, True)
                                self.ui.statusbar.showMessage(
                                    "Export complete!", timeout=5000)
                            except FileNotFoundError:
                                idx = str(self.sender().objectName()) + "_v1"
                                export.export_patch_bin(idx, os.path.join(
                                    self.sd_card_root, "to_zoia"), slot, True)
                                self.ui.statusbar.showMessage(
                                    "Export complete!", timeout=5000)
                            break
                        else:
                            continue
                    except FileNotFoundError:
                        idx = str(self.sender().objectName()) + "_v1"
                        export.export_patch_bin(idx,
                                                os.path.join(self.sd_card_root,
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
                    os.path.join(backend_path,
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

    def remove_sd(self):
        """ Removes a patch that is stored on a user's SD card.
        Currently triggered via a button press.
        """
        row = self.sender().objectName()
        index = "00{}".format(row) if len(row) < 2 else "0{}".format(row)
        delete.delete_patch_sd(index, self.sd_card_path)
        self.set_data_sd()

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
                        os.path.join(backend_path,
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
                content = ps.get_patch_meta(name)
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
                    with open(os.path.join(backend_path, name,
                                           name + ".json")) \
                            as f:
                        content = json.loads(f.read())
                except FileNotFoundError:
                    with open(os.path.join(backend_path,
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
        self.data_PS = ps.get_all_patch_data_init()
        with open(os.path.join(backend_path, "data.json"), "w") as f:
            f.write(json.dumps(self.data_PS))
        self.ui.searchbar_PS.setText("")
        self.sort_and_set()
        self.ui.statusbar.showMessage("Patch list refreshed!", timeout=5000)

    def sd_path(self):
        """ Allows the user to specify the path to their SD card via
        their OS file explorer dialog. Note, nothing is done to ensure
        that the location selected is actually an SD card.
        Currently triggered via a menu action.
        """

        input_dir = QFileDialog.getExistingDirectory(None,
                                                     'Select an SD Card:',
                                                     expanduser("~"))
        if input_dir is not "" and os.path.isdir(input_dir):
            if "/" in input_dir:
                # THIS IS NEEDED FOR WINDOWS.
                # This comes from a bug with QFileDialog returning the
                # wrong path separator on Windows for some odd reason.
                input_dir = input_dir.split("/")[0]
            elif "\\" in input_dir:
                input_dir = input_dir.split("\\")[0]
            elif "//" in input_dir:
                input_dir = input_dir.split("//")[0]
            elif "\\\\" in input_dir:
                input_dir = input_dir.split("\\\\")[0]
            else:
                input_dir = input_dir.split(os.path.sep)[0]
            self.sd_card_root = str(input_dir)
            self.ui.tab_sd.setEnabled(True)
            self.can_export_bank = True
        else:
            self.ui.tab_sd.setEnabled(False)
            self.can_export_bank = False
            self.ui.tabs.setCurrentIndex(1)

        # Setup the SD card tree view for the SD Card tab.
        model = QFileSystemModel()
        model.setRootPath(self.sd_card_root)
        self.ui.sd_tree.setModel(model)
        self.ui.sd_tree.setRootIndex(model.setRootPath(self.sd_card_root))
        self.ui.sd_tree.setColumnWidth(0, self.width() // 4)

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

    def update(self):
        """ Attempts to update any patch that is stored in the user's
        backend directory.

        TODO List which patches were updated.
        """

        self.ui.statusbar.showMessage("Checking for updates...",
                                      timeout=5000)
        count = update.check_for_updates()
        if count == 0:
            msg = QMessageBox()
            msg.setWindowTitle("No Updates")
            msg.setIcon(QMessageBox.Information)
            msg.setText("All of the patches you have downloaded are "
                        "the latest version!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Updates")
            msg.setIcon(QMessageBox.Information)
            if count == 1:
                msg.setText("Successfully updated 1 patch.")
            else:
                msg.setText("Successfully updated " + str(count) + " patches.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def row_invert(self):
        """ Either enables of disables alternating row colours for
        tables; depending on the previous state of the tables.
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

    def update_patch_notes(self):
        """ Updates the patch notes for a patch that has been previously
        locally saved to a user's machine.
        Currently triggered via a button click.
        """

        text = self.ui.text_browser_local.toPlainText()
        try:
            text = text.split("Patch Notes:")[1]
            update.update_data(self.local_selected, text.rstrip(), 3)
        except IndexError:
            update.update_data(self.local_selected, "", 3)
        self.ui.statusbar.showMessage("Successfully updated patch notes.",
                                      timeout=5000)

    def import_patch(self):
        """ Attempts to import a patch. into the librarian.
        Currently triggered via a menu action.
        """

        if self.sd_card_path is not None and \
                self.ui.tabs.currentIndex() == 2:
            for sd_pch in os.listdir(self.sd_card_path):
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
                        save.import_to_backend(os.path.join(self.sd_card_path,
                                                            sd_pch))
                        self.ui.statusbar.showMessage("Import complete!")
                        return
                    except errors.SavingError:
                        msg = QMessageBox()
                        msg.setWindowTitle("Patch Already In Library")
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("That patch exists within your locally "
                                    "saved patches.")
                        msg.setInformativeText("No importing has occurred.")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
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
            if (self.ui.tabs.currentIndex() == 1 and not
            self.ui.back_btn_local.isEnabled()) or \
                    (self.ui.tabs.currentIndex() == 3 and not
                    self.ui.back_btn_bank.isEnabled()):
                self.get_local_patches()
                self.sort_and_set()

        except errors.BadPathError:
            msg = QMessageBox()
            msg.setWindowTitle("No Patch Found")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Incorrect file selected, importing failed.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except errors.SavingError:
            msg = QMessageBox()
            msg.setWindowTitle("Patch Already In Library")
            msg.setIcon(QMessageBox.Information)
            msg.setText("That patch exists within your locally saved "
                        "patches.")
            msg.setInformativeText("No importing has occurred.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

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
                msg = QMessageBox()
                msg.setWindowTitle("Invalid Selection")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Please select a directory.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
        else:
            input_dir = self.sd_card_path
        for pch in os.listdir(input_dir):
            if pch[0] == "0" and pch.split(".")[1] == "bin" \
                    and "_zoia_" in pch:
                # At this point we have done everything to ensure it's a ZOIA
                # patch, save for binary analysis.
                try:
                    save.import_to_backend(os.path.join(input_dir, pch))
                    imp_cnt += 1
                except errors.SavingError:
                    fail_cnt += 1
                    continue

        msg = QMessageBox()
        msg.setWindowTitle("Import Complete")
        msg.setIcon(QMessageBox.Information)
        if imp_cnt > 0:
            msg.setText("Successfully imported {} patches.".format(imp_cnt))
        else:
            msg.setText("Did not import any patches.")
        if fail_cnt > 0:
            if fail_cnt == 1:
                msg.setInformativeText("{} was already saved in the library "
                                       "and was not "
                                       "imported.".format(fail_cnt))
            else:
                msg.setInformativeText("{} were already saved in the library "
                                       "and were not "
                                       "imported.".format(fail_cnt))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def move_patch_bank(self, src, dest):
        """ Attempts to move a patch from one bank slot to another
        Currently triggered via a QTableWidget move event.

        src: The index the item originated from.
        dest: The index the item is being moved to.
        """

        self.ui.table_bank_left.clearSelection()
        self.ui.table_bank_right.clearSelection()

        swap = False

        # Setup the new item.
        if src < 32:
            idx = self.ui.table_bank_left.cellWidget(src, 1).objectName()
        else:
            idx = self.ui.table_bank_right.cellWidget(src - 32,
                                                      1).objectName()

        for pch in self.data_banks:
            if dest == pch["slot"]:
                # We are doing a swap.
                swap = True
                break
        if swap:
            # We are doing a swap.
            # Get the other item.
            if dest < 32:
                idx_dest = self.ui.table_bank_left.cellWidget(dest,
                                                              1).objectName()
            else:
                idx_dest = self.ui.table_bank_right.cellWidget(dest - 32,
                                                               1).objectName()

            # Get the old values out.
            for pch in self.data_banks:
                if pch["slot"] == src or pch["slot"] == dest:
                    self.data_banks.remove(pch)

            # Add the new values in.
            self.data_banks.append({
                "slot": dest,
                "id": idx
            })
            self.data_banks.append({
                "slot": src,
                "id": idx_dest
            })
        else:
            # We are doing a move.

            self.data_banks.append({
                "slot": dest,
                "id": idx
            })

            for pch in self.data_banks:
                if pch["slot"] == src:
                    self.data_banks.remove(pch)
                    break

        # Set the data.
        self.set_data_bank()

        for i in range(64):
            if i == dest:
                if i > 31:
                    self.ui.table_bank_right.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)
                else:
                    self.ui.table_bank_left.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)

        self.get_bank_data()

    def move_patch_sd(self, src, dest):
        """ Attempts to move a patch from one SD card slot to another
        Currently triggered via a QTableWidget move event.

        src: The index the item originated from.
        dest: The index the item is being moved to.
        """

        self.ui.table_sd_left.clearSelection()
        self.ui.table_sd_right.clearSelection()

        # We need to find out if we are just doing a simple move or a swap.
        if dest < 10:
            dest = str("00{}".format(dest))
        else:
            dest = str("0{}".format(dest))
        if src < 10:
            src = str("00{}".format(src))
        else:
            src = str("0{}".format(src))
        src_pch = None
        dest_pch = None
        for pch in os.listdir(self.sd_card_path):
            if pch[:3] == src:
                src_pch = pch
            if pch[:3] == dest:
                dest_pch = pch
            if src_pch is not None and dest_pch is not None:
                # We are doing a swap.
                try:
                    os.rename(os.path.join(self.sd_card_path, src_pch),
                              os.path.join(self.sd_card_path, dest
                                           + src_pch[3:]))
                    os.rename(os.path.join(self.sd_card_path, dest_pch),
                              os.path.join(self.sd_card_path, src
                                           + dest_pch[3:]))
                except FileExistsError:
                    # Swapping files that are named the same thing.
                    os.rename(os.path.join(self.sd_card_path, src_pch),
                              os.path.join(self.sd_card_path, "064"
                                           + src_pch[3:]))
                    # Swapping files that are named the same thing.
                    os.rename(os.path.join(self.sd_card_path, dest_pch),
                              os.path.join(self.sd_card_path, src
                                           + dest_pch[3:]))
                    os.rename(os.path.join(self.sd_card_path, "064"
                                           + src_pch[3:]),
                              os.path.join(self.sd_card_path, dest
                                           + src_pch[3:]))
                self.set_data_sd()
                dest = int(dest)
                for i in range(64):
                    if i == dest:
                        if i > 31:
                            self.ui.table_sd_right.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                        else:
                            self.ui.table_sd_left.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                return

        # We are doing a move.

        os.rename(os.path.join(self.sd_card_path, src_pch),
                  os.path.join(self.sd_card_path, dest + src_pch[3:]))

        dest = int(dest)
        for i in range(64):
            if i == dest:
                if i > 31:
                    self.ui.table_sd_right.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)
                else:
                    self.ui.table_sd_left.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)

        self.set_data_sd()

    def toggle_darkmode(self):
        """ Toggles dark mode for the application.
        Currently not implemented in the UI.

        TODO Modify the stylesheets to have them conform to the initial
             application style.
        """

        app = QApplication.instance()
        if not self.dark:
            # Turn on dark mode.
            with open(os.path.join("zoia_lib", "UI", "resources",
                                   "stylesheets", "dark.qss"), "r") as f:
                data = f.read()
            self.dark = True
        else:
            # Turn off dark mode.
            with open(os.path.join("zoia_lib", "UI", "resources",
                                   "stylesheets", "light.qss"), "r") as f:
                data = f.read()
            self.dark = False

        app.setStyleSheet(data)

    def eventFilter(self, o, e):
        """ Deals with events that originate from various widgets
        present in the GUI.

        o: The source object that triggered the event.
        e: The event that was triggered.
        """

        # SD card tab swap/move
        if o.objectName() == "table_sd_left" or o.objectName() == \
                "table_sd_right":
            if e.type() == QEvent.ChildAdded:
                self.ui.table_sd_left.hideColumn(1)
                self.ui.table_sd_left.hideColumn(2)
                self.ui.table_sd_right.hideColumn(1)
                self.ui.table_sd_right.hideColumn(2)

            elif e.type() == QEvent.ChildRemoved:
                # We have dropped an item, so now we need to rename it
                # or swap it with the item that was previously in that
                # slot.
                self.ui.table_sd_left.showColumn(1)
                self.ui.table_sd_left.showColumn(2)
                self.ui.table_sd_right.showColumn(1)
                self.ui.table_sd_right.showColumn(2)

                dst_index = None

                if o.objectName() == "table_sd_left":
                    src_index = self.ui.table_sd_left.currentRow()
                else:
                    src_index = self.ui.table_sd_right.currentRow() + 32

                if (self.ui.table_sd_left.item(src_index, 0) is not None and
                    self.ui.table_sd_left.item(src_index, 0).text() == "") \
                        or (self.ui.table_sd_right.item(src_index - 32, 0)
                            is not None and self.ui.table_sd_right.item(
                            src_index - 32, 0).text() == ""):
                    # Then it is actually the destination
                    dst_index = src_index
                    # Find the item that just got "deleted"
                    for i in range(64):
                        if i < 32:
                            temp = self.ui.table_sd_left.item(i, 0)
                        else:
                            temp = self.ui.table_sd_right.item(i - 32, 0)
                        if temp.text() == "":
                            if i < 10:
                                temp_index = "00{}".format(i)
                            else:
                                temp_index = "0{}".format(i)
                            for pch in os.listdir(self.sd_card_path):
                                if "{}_zoia_".format(temp_index) in pch:
                                    if i != dst_index:
                                        self.move_patch_sd(i, dst_index)
                                        return True
                                    else:
                                        return False
                else:
                    for i in range(64):
                        if i < 32:
                            temp = self.ui.table_sd_left.item(i, 0)
                        else:
                            temp = self.ui.table_sd_right.item(i - 32, 0)
                        if temp is not None and temp.text() != "":
                            if temp.text()[1] == "0":
                                # one digit
                                temp = int(temp.text()[2])
                            else:
                                # two digits
                                temp = int(temp.text()[1:3])
                            if temp != i:
                                dst_index = i
                    if dst_index is None:
                        # We need to delete the row that just got created.
                        self.ui.table_sd_left.removeRow(32)
                        self.ui.table_sd_right.removeRow(32)
                        return False
                    if src_index != dst_index:
                        self.move_patch_sd(src_index, dst_index)
                    return True
        elif o.objectName() == "table_bank_local":
            if e.type() == QEvent.ChildAdded:
                self.ui.table_bank_left.hideColumn(1)
                self.ui.table_bank_right.hideColumn(1)
            elif e.type() == QEvent.ChildRemoved:
                self.ui.table_bank_left.showColumn(1)
                self.ui.table_bank_right.showColumn(1)

                # Get the current row that was dragged.
                src = self.ui.table_bank_local.currentRow()
                # We need to find out where we dragged the item to
                drop_index = None
                for i in range(64):
                    if i < 32:
                        if self.ui.table_bank_left.item(i, 1) is not None:
                            drop_index = i
                            break
                    else:
                        if self.ui.table_bank_right.item(i - 32, 1) is not \
                                None:
                            drop_index = i
                            break

                if drop_index is not None:
                    # We actually dragged it over.
                    idx = self.ui.table_bank_local.cellWidget(src,
                                                              0).objectName()
                    if ("_" not in idx and len(os.listdir(os.path.join(
                            backend_path, idx))) == 2) or "_" in idx:
                        # Not working within a version directory.
                        # Just a single patch
                        if self.data_banks is not None:
                            # Drop the patch we dragged to from the list if
                            # need be.
                            for pch in self.data_banks:
                                if pch["slot"] == drop_index:
                                    self.data_banks.remove(pch)
                        else:
                            # Need to enable the buttons now that there is a
                            # patch in the tables.
                            self.data_banks = []
                            self.ui.btn_save_bank.setEnabled(True)
                            self.ui.btn_export_bank.setEnabled(True)

                        self.data_banks.append({
                            "slot": drop_index,
                            "id": idx
                        })

                        self.set_data_bank()
                    else:
                        # An entire version directory was dragged over.
                        pch_num = int((len(os.listdir(os.path.join(
                            backend_path, idx))) / 2) - 1)
                        if drop_index + pch_num > 63:
                            self.set_data_bank()
                            msg = QMessageBox()
                            msg.setWindowTitle("No Space")
                            msg.setIcon(QMessageBox.Information)
                            msg.setText("The version directory contain {} "
                                        "patches, so it must be dragged to "
                                        "slot {} or lower.".format(pch_num +
                                                                   1, 63 -
                                                                   pch_num))
                            msg.setStandardButtons(QMessageBox.Ok)
                            msg.exec_()
                        else:
                            # Remove all of the patches that are in the way.
                            if self.data_banks is None:
                                self.data_banks = []
                                self.ui.btn_save_bank.setEnabled(True)
                                self.ui.btn_export_bank.setEnabled(True)
                            else:
                                for pch in self.data_banks:
                                    for i in range(drop_index, drop_index
                                                               + pch_num):
                                        if pch["slot"] == i:
                                            self.data_banks.remove(pch)
                            # Add all of the version patches
                            for i in range(1, pch_num + 2):
                                self.data_banks.append({
                                    "slot": drop_index + i - 1,
                                    "id": "{}_v{}".format(idx, i)
                                })

                            self.set_data_bank()
        elif o.objectName() == "table_bank_left" or o.objectName() == \
                "table_bank_right":
            if e.type() == QEvent.ChildAdded:
                self.ui.table_bank_left.hideColumn(1)
                self.ui.table_bank_right.hideColumn(1)
                self.get_bank_data()
            elif e.type() == QEvent.ChildRemoved:
                # We have dropped an item, so now we need to rename it
                # or swap it with the item that was previously in that
                # slot.
                self.ui.table_bank_left.showColumn(1)
                self.ui.table_bank_right.showColumn(1)

                dst_index = None

                if o.objectName() == "table_bank_left":
                    src_index = self.ui.table_bank_left.currentRow()
                else:
                    src_index = self.ui.table_bank_right.currentRow() + 32

                if (src_index < 32 and self.ui.table_bank_left.item(
                        src_index, 0)) is None \
                        or (src_index > 31 and self.ui.table_bank_right.item(
                    src_index - 32, 0) is None):
                    # Then it is actually the destination
                    dst_index = src_index
                    # Find the item that just got "deleted"
                    for i in range(64):
                        if i < 32:
                            temp = self.ui.table_bank_left.item(i, 0)
                            temp2 = self.ui.table_bank_left.cellWidget(i, 1)
                        else:
                            temp = self.ui.table_bank_right.item(i - 32, 0)
                            temp2 = self.ui.table_bank_right.cellWidget(i - 32
                                                                        , 1)
                        if temp is None and temp2 is not None:
                            self.move_patch_bank(i, dst_index)
                else:
                    for i in range(64):
                        if i < 32:
                            temp = self.ui.table_bank_left.item(i, 0)
                        else:
                            temp = self.ui.table_bank_right.item(i - 32, 0)
                        if temp is not None and temp.text() != "":
                            if temp.text()[1] == "0":
                                # one digit
                                temp = int(temp.text()[2])
                            else:
                                # two digits
                                temp = int(temp.text()[1:3])
                            if temp != i:
                                dst_index = i
                    if dst_index is None:
                        # We need to delete the row that just got created.
                        self.ui.table_bank_left.removeRow(32)
                        self.ui.table_bank_right.removeRow(32)
                        return False
                    if src_index != dst_index:
                        self.move_patch_bank(src_index, dst_index)
                    return True

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
                        self.prev_tag_cat = (self.ui.table_local.currentRow(),
                                             self.ui.table_local.currentColumn(
                                             ),
                                             self.ui.table_local.selectedItems(
                                             )[0].text())
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
        self.sort_and_set()

    def load_bank(self):
        """ Loads a Bank file that was previously saved to the
        backend directory.
        Currently triggered via a button press.
        """

        bnk_file = QFileDialog.getOpenFileName(None,
                                               "Select A Patch Bank:",
                                               os.path.join(backend_path,
                                                            "Banks"))[0]
        if bnk_file is not "":
            if "/" in bnk_file:
                bnk_file = bnk_file.split("/")[-1]
            elif "\\" in bnk_file:
                bnk_file = bnk_file.split("\\")[-1]
            elif "//" in bnk_file:
                bnk_file = bnk_file.split("//")[-1]
            elif "\\\\" in bnk_file:
                bnk_file = bnk_file.split("\\\\")[-1]
            else:
                bnk_file = bnk_file.split(os.path.sep)[-1]
        else:
            return

        with open(os.path.join(backend_path, "Banks", bnk_file), "r") as f:
            self.data_banks = json.loads(f.read())

        found_item = False
        for i in range(64):
            if i < 32:
                if self.ui.table_bank_left.cellWidget(i, 1) is not None:
                    found_item = True
                    break
            else:
                if self.ui.table_bank_right.cellWidget(i - 32, 1) is not None:
                    found_item = True
                    break
        if not found_item:
            self.set_data_bank()
            self.ui.btn_export_bank.setEnabled(True)
            self.ui.btn_save_bank.setEnabled(True)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This will overwrite the current data in the "
                        "table.\nIs that okay?")
            msg.setInformativeText("If you haven't saved your changes they "
                                   "will be lost.")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            value = msg.exec_()
            if value == QMessageBox.Yes:
                self.set_data_bank()
                self.get_local_patches()
                self.ui.btn_export_bank.setEnabled(True)
                self.ui.btn_save_bank.setEnabled(True)

    def save_bank(self):
        """ Saves a Bank to the backend application directory.
        Currently triggered via a button press.
        """
        # Ask for a name
        name, ok = QInputDialog().getText(self, "Save Bank",
                                          "Please enter a name for the Bank:")
        if ok:
            self.get_bank_data()
            with open(os.path.join(backend_path, "Banks", "{}.json".format(
                    name)),
                      "w") as f:
                f.write(json.dumps(self.data_banks))

    def export_bank(self):
        """ Saves a Bank to the backend application directory.
        Currently triggered via a button press.
        """

        if self.sd_card_root is None:
            msg = QMessageBox()
            msg.setIcon
            msg.setWindowTitle("No SD Path")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please specify your SD card path!")
            msg.setInformativeText("File -> Specify SD Card Location")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            # Ask for a name
            while True:
                name, ok = QInputDialog().getText(self, "Export Bank",
                                                  "Please enter a name for the "
                                                  "Bank:")
                if ok and name not in os.listdir(self.sd_card_root):
                    self.get_bank_data()
                    export.export_bank(self.data_banks, self.sd_card_root,
                                       name)
                    msg = QMessageBox()
                    msg.setWindowTitle("Success!")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("The Bank has been successfully exported to "
                                "the root of your SD card.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    break
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Directory exists")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("A directory with that name already exists.")
                    msg.setInformativeText("Would you like to overwrite it?")
                    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    value = msg.exec_()
                    if value == QMessageBox.Yes:
                        self.get_bank_data()
                        export.export_bank(self.data_banks, self.sd_card_root,
                                           name, True)
                        msg = QMessageBox()
                        msg.setWindowTitle("Success!")
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(
                            "The Bank has been successfully exported to "
                            "the root of your SD card.")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        break

    def remove_bank_item(self):
        """ Removes an item from one of the bank tables.
        Currently triggered via a button press.
        """

        for i in range(64):
            if i < 32:
                item = self.ui.table_bank_left.cellWidget(i, 1)
                if item is None:
                    continue
                elif item.objectName() == self.sender().objectName():
                    self.ui.table_bank_left.setItem(i, 0, QTableWidgetItem(
                        None))
                    self.ui.table_bank_left.setCellWidget(i, 1, None)
                    break
            else:
                item = self.ui.table_bank_right.cellWidget(i - 32, 1)
                if item is None:
                    continue
                elif item.objectName() == self.sender().objectName():
                    self.ui.table_bank_right.setItem(i - 32, 0,
                                                     QTableWidgetItem(None))
                    self.ui.table_bank_right.setCellWidget(i - 32, 1, None)
                    break

        for pch in self.data_banks:
            if pch["slot"] == i:
                self.data_banks.remove(pch)

        # Check to see if we should disable export and save buttons.
        found_item = False
        for i in range(64):
            if i < 32:
                if self.ui.table_bank_left.cellWidget(i, 1) is not None:
                    found_item = True
                    break
            else:
                if self.ui.table_bank_right.cellWidget(i - 32, 1) is not None:
                    found_item = True
                    break

        if not found_item:
            self.ui.btn_export_bank.setEnabled(False)
            self.ui.btn_save_bank.setEnabled(False)

    def get_bank_data(self):
        """ Gets the data from the current bank tables.
        """
        self.data_banks = []
        for i in range(64):
            if i < 32:
                temp = self.ui.table_bank_left.cellWidget(i, 1)
            else:
                temp = self.ui.table_bank_right.cellWidget(i - 32, 1)
            if temp is not None:
                self.data_banks.append({
                    "slot": i,
                    "id": temp.objectName()
                })

    def try_quit(self):
        """ Forces the application to close.
        Currently triggered via a menu action.
        """

        self.close()
