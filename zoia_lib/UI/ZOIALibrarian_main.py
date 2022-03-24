import json
import os
from os.path import expanduser

from PySide2 import QtCore
from PySide2.QtCore import QEvent, Qt, QThread
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QRadioButton,
    QDesktopWidget,
    QFileDialog,
)

import zoia_lib.UI.ZOIALibrarian as ui_main
import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors
from zoia_lib.UI.ZOIALibrarian_bank import ZOIALibrarianBank
from zoia_lib.UI.ZOIALibrarian_local import ZOIALibrarianLocal
from zoia_lib.UI.ZOIALibrarian_ps import ZOIALibrarianPS
from zoia_lib.UI.ZOIALibrarian_sd import ZOIALibrarianSD
from zoia_lib.UI.ZOIALibrarian_util import ZOIALibrarianUtil
from zoia_lib.backend.api import PatchStorage
from zoia_lib.backend.patch_binary import PatchBinary
from zoia_lib.backend.patch_delete import PatchDelete
from zoia_lib.backend.patch_export import PatchExport
from zoia_lib.backend.patch_save import PatchSave

api = PatchStorage()
save = PatchSave()
export = PatchExport()
delete = PatchDelete()
binary = PatchBinary()


class ZOIALibrarianMain(QMainWindow):
    """The ZOIALibrarian_Main class represents the frontend for the
    application. It allows users to interact with the various backend
    functions available. These include searching, downloading, sorting,
    and exporting patches; among other functions.
    Any changes made to the .ui file will not be reflected unless the
    following command is run from the UI directory:
        pyside2-uic.exe ZOIALibrarian.ui -o ZOIALibrarian.py
    Known issues:
     - Certain UI elements do not like font changes (headers, tabs, etc).
     - Deleting items in the Folders table will always delete the first entry
       if the item appears more than once.
    """

    def __init__(self):
        """Initializes the UI for the application. Currently, upon
        being launched for the first time, it uses ZOIALibrarianPS to query
        the PS API for all ZOIA patches and gets the metadata.
        Upon subsequent launches, it will search for previously stored
        metadata, compare it to the # of patches currently on PS,
        and either begin using the cached data, or get the most recent patches
        and add them to the cache; and subsequently start the application.

        Initialization consists of creating the helper UI classes, loading
        previously saved preferences regarding the application, and finally
        displaying the UI to the user beginning on the PatchStorage tab.
        """

        super().__init__()
        # Setup the UI using ZOIALibrarian.py
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.path = save.get_backend_path()

        # Message box init
        self.icon = QIcon(
            os.path.join(os.getcwd(), "zoia_lib", "UI", "resources", "logo.ico")
        )
        self.msg = QMessageBox()
        self.msg.setWindowIcon(self.icon)

        # Helper classes init
        self.util = ZOIALibrarianUtil(self.ui, self)
        self.sd = ZOIALibrarianSD(self.ui, save, self.msg, delete, self.util)
        self.bank = ZOIALibrarianBank(
            self.ui, self.path, self.sd, self.msg, self.util, self
        )
        self.ps = ZOIALibrarianPS(
            self.ui, api, self.path, self.msg, save, self.sort_and_set
        )
        self.local = ZOIALibrarianLocal(
            self.ui,
            self.path,
            self.sd,
            self.msg,
            self,
            export,
            delete,
            self.sort_and_set,
        )

        # Instance variables.
        self.patch_cache = []
        self.prev_sort = None
        self.search_data_PS = None
        self.search_data_local = None
        self.search_data_bank = None
        self.search_data_local_version = None
        self.search_data_bank_version = None
        self.table_title_size = None
        self.table_local_title_size = None
        self.table_bank_local_title_size = None
        self.ps_sizes = None
        self.local_sizes = None
        self.sd_sizes = None
        self.bank_sizes = None
        self.font = None
        self.local_pch_count = -1
        self.tab_1 = -1
        self.tab_3 = -1
        self.add_rating = None

        # Threads
        self.worker_mass = ImportMassWorker(self)
        self.worker_mass.signal.connect(self._mass_import_done)
        self.worker_mass_sd = ImportMassSDWorker(self)
        self.worker_mass_sd.signal.connect(self._mass_import_done)

        self.worker_version = ImportVersionWorker(self)
        self.worker_version.signal.connect(self._version_import_done)
        self.worker_version_sd = ImportVersionSDWorker(self)
        self.worker_version_sd.signal.connect(self._version_import_done)

        # self.worker_expander = DisplayExpandedRouting(self)
        # self.worker_expander.signal.connect(self.expand_patch_done)

        # Get the data necessary for the PS tab.
        self.ps.metadata_init()

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
        self.ui.btn_clear_bank.setEnabled(False)
        self.ui.btn_export_bank.setEnabled(False)
        self.ui.delete_folder_sd_btn.setEnabled(False)
        self.ui.set_export_dir_btn.setEnabled(True)
        self.ui.btn_load_bank.setEnabled(
            not len(os.listdir(os.path.join(self.path, "Folders"))) == 0
        )

        # Load preferences from previous sessions (if they exist)
        while os.path.exists(os.path.join(self.path, "pref.json")):
            # SD Card previously specified.
            with open(os.path.join(self.path, "pref.json"), "r") as f:
                data = json.loads(f.read())
            if data[0]["sd_root"] != "" and os.path.exists(data[0]["sd_root"]):
                self.sd.set_sd_root(data[0]["sd_root"])
                self.sd.set_export_path(os.path.join(self.sd.sd_root, "to_zoia"))
                self.ui.tab_sd.setEnabled(True)
                self.sd.sd_path(True, self.width())

            self.resize(data[0]["width"], data[0]["height"])

            # Font
            self.font = QFont(data[0]["font"], data[0]["font_size"])
            self.util.set_font(self.font)

            self.ps_sizes = data[1]
            self.local_sizes = data[2]
            self.sd_sizes = data[3]
            self.bank_sizes = data[4]

            # Version check
            if "col_5" not in self.local_sizes or "col_5" not in self.bank_sizes:
                os.remove(os.path.join(self.path, "pref.json"))
                self.add_rating = True
                self.reset_ui()
                break

            # PS Table
            # self.ui.splitter_PS.setSizes([self.ps_sizes["split_left"],
            #                               self.ps_sizes["split_right"]])
            self.ui.table_PS.setColumnWidth(0, self.ps_sizes["col_0"])
            self.ui.table_PS.setColumnWidth(1, self.ps_sizes["col_1"])
            self.ui.table_PS.setColumnWidth(2, self.ps_sizes["col_2"])
            self.ui.table_PS.setColumnWidth(3, self.ps_sizes["col_3"])

            # Local Table
            # self.ui.splitter_local.setSizes([self.local_sizes["split_left"],
            #                                  self.local_sizes["split_right"]])
            # self.ui.splitter_local_hori.setSizes([self.local_sizes["split_top"],
            #                                       self.local_sizes["split_bottom"]])
            self.ui.table_local.setColumnWidth(0, self.local_sizes["col_0"])
            self.ui.table_local.setColumnWidth(1, self.local_sizes["col_1"])
            self.ui.table_local.setColumnWidth(2, self.local_sizes["col_2"])
            self.ui.table_local.setColumnWidth(3, self.local_sizes["col_3"])
            self.ui.table_local.setColumnWidth(4, self.local_sizes["col_4"])
            self.ui.table_local.setColumnWidth(5, self.local_sizes["col_5"])

            # SD Tables
            # self.ui.splitter_sd_vert.setSizes([self.sd_sizes["split_top"],
            #                                    self.sd_sizes["split_bottom"]])
            # self.ui.splitter_sd_hori.setSizes([self.sd_sizes["split_left"],
            #                                    self.sd_sizes["split_right"]])
            self.ui.table_sd_left.setColumnWidth(0, self.sd_sizes["col_0"])
            self.ui.table_sd_left.setColumnWidth(1, self.sd_sizes["col_1"])
            self.ui.table_sd_right.setColumnWidth(0, self.sd_sizes["col_2"])
            self.ui.table_sd_right.setColumnWidth(1, self.sd_sizes["col_3"])

            # Folder Tables
            # self.ui.splitter_bank_tables.setSizes([self.bank_sizes["split_bank_left"],
            #                                        self.bank_sizes["split_bank_right"]])
            # self.ui.splitter_bank.setSizes([self.bank_sizes["split_left"],
            #                                 self.bank_sizes["split_middle"],
            #                                 self.bank_sizes["split_right"]])
            self.ui.table_bank_left.setColumnWidth(0, self.bank_sizes["col_0"])
            self.ui.table_bank_right.setColumnWidth(0, self.bank_sizes["col_1"])
            self.ui.table_bank_local.setColumnWidth(0, self.bank_sizes["col_2"])
            self.ui.table_bank_local.setColumnWidth(1, self.bank_sizes["col_3"])
            self.ui.table_bank_local.setColumnWidth(2, self.bank_sizes["col_4"])
            self.ui.table_bank_local.setColumnWidth(3, self.bank_sizes["col_5"])

            self.util.set_dark(data[5]["enabled"])
            self.util.set_row_inversion(data[6]["enabled"])
            break
        else:
            # No pref.json, use default values.
            self.add_rating = True
            self.reset_ui()

        # Update local patches if necessary
        if self.add_rating:
            self.local.metadata_init()

        # Connect buttons and items to methods.
        self.ui.tabs.currentChanged.connect(self.tab_switch)
        self.ui.actionAlternating_Row_Colours.triggered.connect(self.util.row_invert)
        self.ui.actionSort_by_title_A_Z.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_title_Z_A.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_date_new_old.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_date_old_new.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_likes_high_low.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_likes_low_high.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_views_high_low.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_views_low_high.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_downloads_high_low.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_downloads_low_high.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_author_A_Z.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_author_Z_A.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_rating_high_low.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_rating_low_high.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_category_high_low.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_category_low_high.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_tag_high_low.triggered.connect(self.sort_and_set)
        self.ui.actionSort_by_tag_low_high.triggered.connect(self.sort_and_set)
        self.ui.actionSpecify_SD_Card_Location.triggered.connect(
            lambda: self.sd.sd_path(False, self.width())
        )
        self.ui.actionFont.triggered.connect(lambda: self.util.change_font(""))
        self.ui.actionIncrease_Font_Size.triggered.connect(
            lambda: self.util.change_font("+")
        )
        self.ui.actionDecrease_Font_Size.triggered.connect(
            lambda: self.util.change_font("-")
        )
        self.ui.actionQuit.triggered.connect(self._try_quit)
        self.ui.check_for_updates_btn.clicked.connect(
            self.local.update_local_patches_thread
        )
        # self.ui.actionImport_Multiple_Patches.triggered.connect(
        #     self._mass_import_thread)
        self.ui.actionImport_Multiple_Patches.triggered.connect(
            self.import_multiple_menu
        )
        # self.ui.actionImport_Version_History_directory.triggered.connect(
        #     self._version_import_thread)
        self.ui.actionImport_Version_History_directory.triggered.connect(
            self.import_version_menu
        )
        self.ui.actionNavigate_to_local_backend.triggered.connect(self.util.open_local_backend)
        self.ui.refresh_pch_btn.clicked.connect(self.ps.reload_ps_thread)
        self.ui.update_patch_notes.clicked.connect(self.local.update_patch_notes)
        self.ui.actionImport_A_Patch.triggered.connect(self.import_patch)
        self.ui.actionReset_Sizes.triggered.connect(self.reset_ui)
        self.ui.actionDocumentation.triggered.connect(self.util.documentation)
        self.ui.actionFAQ.triggered.connect(self.util.faq)
        self.ui.actionTips_Tricks.triggered.connect(self.util.tips)
        self.ui.actionModule_Index.triggered.connect(self.util.mod_idx)
        self.ui.actionFirmware_Files.triggered.connect(self.util.firmware)
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
        self.ui.sd_tree.clicked.connect(self.sd.prepare_sd_view)
        self.ui.import_all_btn.clicked.connect(self._mass_import_thread_sd)
        self.ui.import_all_ver_btn.clicked.connect(self._version_import_thread_sd)
        self.ui.back_btn_local.clicked.connect(self.local.go_back)
        self.ui.back_btn_bank.clicked.connect(self.local.go_back)
        self.ui.btn_load_bank.clicked.connect(self.bank.load_bank)
        self.ui.btn_save_bank.clicked.connect(lambda: self.bank.save_bank(self))
        self.ui.btn_clear_bank.clicked.connect(self.bank.clear_bank)
        self.ui.btn_export_bank.clicked.connect(
            lambda: self.bank.export_bank(self.sd, export, self)
        )
        self.ui.delete_folder_sd_btn.clicked.connect(self.sd.delete_sd_item)
        self.ui.set_export_dir_btn.clicked.connect(self.sd.export_path)
        self.ui.actionToggle_Dark_Mode_2.triggered.connect(self.util.toggle_dark)
        self.ui.btn_dwn_all.clicked.connect(self.ps.download_all_thread)
        self.ui.btn_show_routing.clicked.connect(self.local.setup_exp)
        self.ui.back_btn.clicked.connect(self.local.viz_reset)
        self.ui.btn_next_page.clicked.connect(self.local.viz_page)
        self.ui.btn_prev_page.clicked.connect(self.local.viz_page)
        for i in range(40):
            btn = self.local.get_btn(i)
            btn.clicked.connect(self.local.viz_display)

        # Set the theme.
        self.util.toggle_dark()

        # Set the rows
        self.util.row_invert()

        # Font consistency.
        self.util.change_font(
            QFont("Verdana", 10)
            if self.font is None
            else data[0]["font"] + "%" + str(data[0]["font_size"])
        )

        # Modify the display sizes for some widgets.
        if self.ps_sizes is None:
            self.ui.splitter_PS.setSizes([self.width() * 0.55, self.width() * 0.45])
        else:
            self.ui.splitter_PS.setSizes(
                [self.ps_sizes["split_left"], self.ps_sizes["split_right"]]
            )
        if self.local_sizes is None:
            self.ui.splitter_local.setSizes([self.width() * 0.6, self.width() * 0.4])
            self.ui.splitter_local_hori.setSizes(
                [self.height() * 0.55, self.height() * 0.45]
            )
        else:
            self.ui.splitter_local.setSizes(
                [self.local_sizes["split_left"], self.local_sizes["split_right"]]
            )
            self.ui.splitter_local_hori.setSizes(
                [self.local_sizes["split_top"], self.local_sizes["split_bottom"]]
            )
        if self.sd_sizes is None:
            self.ui.splitter_sd_hori.setSizes([self.width() * 0.5, self.width() * 0.5])
            self.ui.splitter_sd_vert.setSizes(
                [self.height() * 0.4, self.height() * 0.6]
            )
        else:
            self.ui.splitter_sd_vert.setSizes(
                [self.sd_sizes["split_top"], self.sd_sizes["split_bottom"]]
            )
            self.ui.splitter_sd_hori.setSizes(
                [self.sd_sizes["split_left"], self.sd_sizes["split_right"]]
            )
        if self.bank_sizes is None:
            self.ui.splitter_bank.setSizes(
                [self.width() * 0.535, self.width() * 0.465, self.width() * 0]
            )
            self.ui.splitter_bank_tables.setSizes(
                [self.width() * 0.5, self.width() * 0.5]
            )
        else:
            self.ui.splitter_bank.setSizes(
                [
                    self.bank_sizes["split_left"],
                    self.bank_sizes["split_middle"],
                    self.bank_sizes["split_right"],
                ]
            )
            self.ui.splitter_bank_tables.setSizes(
                [
                    self.bank_sizes["split_bank_left"],
                    self.bank_sizes["split_bank_right"],
                ]
            )

        # Sort and set the data.
        self.sort_and_set()

        # Center the application on launch.
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def tab_switch(self):
        """Actions performed whenever a tab is switched to within the
        application.
        """

        # Reset the previous tag/cat (if it existed).
        self.local.set_prev_tag_cat(None)

        # Figure out what tab we switched to.
        if self.ui.tabs.currentIndex() == 1 or self.ui.tabs.currentIndex() == 3:
            # Only reload the table data if we need to (new # of patches).
            if (
                (
                    self.ui.tabs.currentIndex() == 1
                    and self.ui.table_local.rowCount() == 1
                )
                or (
                    self.ui.tabs.currentIndex() == 3
                    and self.ui.table_bank_local.rowCount() == 1
                )
                or self.local_pch_count == -1
                or self.local_pch_count != len(os.listdir(self.path))
                or self.tab_1 != self.tab_3
            ):
                # tab toggle to allow other table to refresh
                if (
                    self.local_pch_count != len(os.listdir(self.path))
                    and self.local_pch_count != -1
                ) or self.tab_1 != self.tab_3:
                    if self.ui.tabs.currentIndex() == 1:
                        self.tab_1 = 0
                    if self.ui.tabs.currentIndex() == 3:
                        self.tab_3 = 0

                    if self.tab_1 == self.tab_3:
                        self.tab_1 = -1
                        self.tab_3 = -1

                self.local.get_local_patches()
                self.local_pch_count = len(os.listdir(self.path))
            # Context cleanup
            if self.ui.tabs.currentIndex() == 3:
                self.ui.text_browser_bank.setText("")
            else:
                self.ui.text_browser_local.setText("")
                self.ui.page_label.setText("")
                self.ui.update_patch_notes.setEnabled(False)
                self.ui.text_browser_viz.setText("")
                self.ui.btn_prev_page.setEnabled(False)
                self.ui.btn_next_page.setEnabled(False)
                self.local.viz_disable()
        elif self.ui.tabs.currentIndex() == 2:
            # SD card tab, need to check if an SD card has been specified.
            if self.sd.get_sd_root() is None:
                self.msg.setWindowTitle("No SD Path")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Please specify your SD card path.")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                self.sd.sd_path(False, self.width())
                if self.sd.get_sd_root() is None:
                    # user cancelled without providing a path
                    self.ui.tabs.setCurrentIndex(1)
        elif self.ui.tabs.currentIndex() == 0 and self.ui.table_PS.rowCount() == 1:
            # We started the app with no internet, need to check if there
            # is a connection now and retry to get the patches.
            api_2 = PatchStorage()
            self.ps = ZOIALibrarianPS(
                self.ui, api_2, self.path, self.msg, save, self.sort_and_set
            )
            self.ps.metadata_init()

        # Local splitter fix, need to add set_ui for when using preferred
        # ui values instead of the default
        if self.ui.tabs.currentIndex() == 1:
            self.reset_ui(tab=1)

        self.sort_and_set()

    def set_data(self, search=False, version=False):
        """Sets the data for the various patch tables. This is done
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
            3: self.ui.table_bank_local,
        }[table_index]

        # Clear the contents of the table
        curr_table.clearContents()

        # Figure out the data we are using.
        data = {
            (0, True, False): self.search_data_PS,
            (0, False, False): self.ps.get_data_ps(),
            (1, True, True): self.search_data_local_version,
            (1, False, True): self.local.get_data_local_version(),
            (1, True, False): self.search_data_local,
            (1, False, False): self.local.get_data_local(),
            (3, True, True): self.search_data_bank_version,
            (3, False, True): self.local.get_data_bank_version(),
            (3, True, False): self.search_data_bank,
            (3, False, False): self.local.get_data_bank(),
        }[(table_index, search, version)]

        data_length = len(data)

        # Set the rows for the table.
        curr_table.setRowCount(data_length)

        # Iterate through the data so that we can set each row.
        for i in range(data_length):
            idx = str(data[i]["id"])
            title = data[i]["title"]
            # Button for the header "Title"
            btn_title = QRadioButton(title, self)
            # Wrap the title if it exceeds 24 characters in length.
            if len(title) > 24:
                temp = title.split(" ")
                count = 0
                title = ""
                for text in temp:
                    title += text + " "
                    count += len(text) + 1
                    if count > 24:
                        count = 0
                        title += "\n"
                btn_title.setText(title.rstrip())
            # Check to see if we are in a version directory.
            if (table_index == 1 and self.ui.back_btn_local.isEnabled()) or (
                table_index == 3 and self.ui.back_btn_bank.isEnabled()
            ):
                btn_title.setObjectName("{}_v{}".format(idx, str(data[i]["revision"])))
                btn_title.setText(
                    data[i]["files"][0]["filename"]
                    .split(".")[0]
                    .split("_zoia_")[-1]
                    .replace("_", " ")
                )
            # Check to see if we need to add the version text outside of
            # a version directory to show you can enter one.
            elif (table_index == 1 and not self.ui.back_btn_local.isEnabled()) or (
                table_index == 3 and not self.ui.back_btn_bank.isEnabled()
            ):
                if len(os.listdir(os.path.join(self.path, idx))) > 2:
                    btn_title.setText(title.rstrip() + "\n[Multiple Versions]")
                btn_title.setObjectName(idx)
            else:
                btn_title.setObjectName(idx)
            # Connect the button and insert into the table.
            btn_title.toggled.connect(self.display_patch_info)
            btn_title.setFont(self.ui.table_PS.font())
            curr_table.setCellWidget(i, 0, btn_title)

            # Text for the headers "Tags" and "Categories"
            for j in range(2):
                index = "tags" if j == 0 else "categories"
                text = ""
                length = len(data[i][index])
                if length > 2:
                    for k in range(0, length - 1):
                        text += data[i][index][k]["name"] + ", "
                    text += "and " + data[i][index][length - 1]["name"]
                elif length == 2:
                    text = (
                        data[i][index][0]["name"] + " and " + data[i][index][1]["name"]
                    )
                else:
                    try:
                        text = data[i][index][0]["name"]
                    except IndexError:
                        text = "No " + index

                text_item = QTableWidgetItem(text)
                text_item.setTextAlignment(Qt.AlignCenter)
                # Can only edit tags/cats in Local Storage View.
                if (
                    table_index == 1
                    and not self.ui.back_btn_local.isEnabled()
                    and len(os.listdir(os.path.join(self.path, idx))) > 2
                ):
                    text_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                curr_table.setItem(i, j + 1, text_item)

            # Text for the header "Date Modified"
            if table_index == 0 or table_index == 1:
                date = QTableWidgetItem(data[i]["updated_at"][:10])
                date.setTextAlignment(Qt.AlignCenter)
                date.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                curr_table.setItem(i, 3, date)

            # If we are on tab index 0, we need a "Download" header item.
            if table_index == 0:
                self.ps.create_dwn_btn(i, idx)

            # If we are on tab index 1, we need "Rating", "Export",
            # and "Delete" header items.
            if table_index == 1:
                self.local.create_rating_ticker(i, data[i]["rating"])
                self.local.create_expt_and_del_btns(
                    btn_title, i, idx, str(data[i]["revision"])
                )

            # Numerical rating for "Rating" header, which is
            # different in the Folders tab (non-editable).
            if table_index == 3:
                index = "rating"
                try:
                    if data[i][index] < 0 or data[i][index] > 5:
                        raise errors.SortingError(data[i][index], 901)
                    text = "{}".format(data[i][index])
                except KeyError:
                    text = ""

                text_item = QTableWidgetItem(text)
                text_item.setTextAlignment(Qt.AlignCenter)
                text_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                curr_table.setItem(i, 3, text_item)

                # Also need a "Add to Folder" header item.
                self.bank.create_add_btn(btn_title, i, idx)

        # Also set the title size and resize the columns.
        # Only use defaults if pref.json doesn't exist.
        if table_index == 0 and self.ps_sizes is None:
            curr_table.resizeColumnsToContents()
            curr_table.setColumnWidth(0, self.width() * 0.165)
            curr_table.setColumnWidth(1, self.width() * 0.135)
            curr_table.setColumnWidth(2, self.width() * 0.075)
            curr_table.setColumnWidth(3, self.width() * 0.075)
            self.ui.splitter_PS.setSizes([self.width() * 0.55, self.width() * 0.45])
            self.ps_sizes = {
                "col_0": curr_table.columnWidth(0),
                "col_1": curr_table.columnWidth(1),
                "col_2": curr_table.columnWidth(2),
                "col_3": curr_table.columnWidth(3),
                "split_left": self.ui.splitter_PS.sizes()[0],
                "split_right": self.ui.splitter_PS.sizes()[1],
            }

        elif table_index == 1 and self.local_sizes is None:
            curr_table.resizeColumnsToContents()
            curr_table.setColumnWidth(0, self.width() * 0.165)
            curr_table.setColumnWidth(1, self.width() * 0.125)
            curr_table.setColumnWidth(2, self.width() * 0.065)
            curr_table.setColumnWidth(3, self.width() * 0.075)
            curr_table.setColumnWidth(4, self.width() * 0.045)
            curr_table.setColumnWidth(5, self.width() * 0.065)
            self.local_sizes = {
                "col_0": curr_table.columnWidth(0),
                "col_1": curr_table.columnWidth(1),
                "col_2": curr_table.columnWidth(2),
                "col_3": curr_table.columnWidth(3),
                "col_4": curr_table.columnWidth(4),
                "col_5": curr_table.columnWidth(5),
                "split_left": self.ui.splitter_local.sizes()[0],
                "split_right": self.ui.splitter_local.sizes()[1],
                "split_top": self.ui.splitter_local_hori.sizes()[0],
                "split_bottom": self.ui.splitter_local_hori.sizes()[1],
            }

        elif table_index == 2 and self.sd_sizes is None:
            curr_table.resizeColumnsToContents()
            curr_table.setColumnWidth(0, self.width() * 0.25)
            curr_table.setColumnWidth(1, self.width() * 0.125)
            curr_table.setColumnWidth(2, self.width() * 0.25)
            curr_table.setColumnWidth(3, self.width() * 0.125)
            self.ui.splitter_sd_hori.setSizes([self.width() * 0.5, self.width() * 0.5])
            self.ui.splitter_sd_vert.setSizes([self.width() * 0.4, self.width() * 0.6])

            self.sd_sizes = {
                "col_0": curr_table.columnWidth(0),
                "col_1": curr_table.columnWidth(1),
                "col_2": curr_table.columnWidth(2),
                "col_3": curr_table.columnWidth(3),
                "split_top": self.ui.splitter_sd_hori.sizes()[0],
                "split_bottom": self.ui.splitter_sd_hori.sizes()[1],
                "split_left": self.ui.splitter_sd_vert.sizes()[0],
                "split_right": self.ui.splitter_sd_vert.sizes()[1],
            }

        elif table_index == 3 and self.bank_sizes is None:
            curr_table.resizeColumnsToContents()
            curr_table.setColumnWidth(0, self.width() * 0.16)
            curr_table.setColumnWidth(1, self.width() * 0.11)
            curr_table.setColumnWidth(2, self.width() * 0.0625)
            curr_table.setColumnWidth(3, self.width() * 0.035)
            self.ui.splitter_bank.setSizes(
                [self.width() * 0.535, self.width() * 0.465, self.width() * 0]
            )
            self.ui.splitter_bank_tables.setSizes(
                [self.width() * 0.5, self.width() * 0.5]
            )

            self.bank_sizes = {
                "col_0": curr_table.columnWidth(0),
                "col_1": curr_table.columnWidth(1),
                "col_2": curr_table.columnWidth(2),
                "col_3": curr_table.columnWidth(3),
                "col_4": curr_table.columnWidth(4),
                "col_5": curr_table.columnWidth(5),
                "split_left": self.ui.splitter_bank.sizes()[0],
                "split_middle": self.ui.splitter_bank.sizes()[1],
                "split_right": self.ui.splitter_bank.sizes()[2],
                "split_bank_left": self.ui.splitter_bank_tables.sizes()[0],
                "split_bank_right": self.ui.splitter_bank_tables.sizes()[1],
            }

        curr_table.resizeRowsToContents()

    def reset_ui(self, tab=None):
        """Resets the UI panels and tables to their default positions.
        Upon closing the application, pref.json will include the defaults.
        Currently triggered via a menu action.
        """

        if not tab:
            # Reset PS sizes
            self.ui.splitter_PS.setSizes([self.width() * 0.55, self.width() * 0.45])
            self.ui.table_PS.resizeColumnsToContents()
            self.ui.table_PS.setColumnWidth(0, self.width() * 0.165)
            self.ui.table_PS.setColumnWidth(1, self.width() * 0.135)
            self.ui.table_PS.setColumnWidth(2, self.width() * 0.075)
            self.ui.table_PS.setColumnWidth(3, self.width() * 0.075)

            # Reset local sizes
            self.ui.splitter_local.setSizes([self.width() * 0.6, self.width() * 0.4])
            self.ui.splitter_local_hori.setSizes(
                [self.height() * 0.55, self.height() * 0.45]
            )
            self.ui.table_local.resizeColumnsToContents()
            self.ui.table_local.setColumnWidth(0, self.width() * 0.165)
            self.ui.table_local.setColumnWidth(1, self.width() * 0.125)
            self.ui.table_local.setColumnWidth(2, self.width() * 0.065)
            self.ui.table_local.setColumnWidth(3, self.width() * 0.075)
            self.ui.table_local.setColumnWidth(4, self.width() * 0.045)
            self.ui.table_local.setColumnWidth(5, self.width() * 0.065)

            # Reset SD sizes
            self.ui.splitter_sd_hori.setSizes([self.width() * 0.5, self.width() * 0.5])
            self.ui.splitter_sd_vert.setSizes([self.height() * 0.4, self.height() * 0.6])
            self.ui.table_sd_left.setColumnWidth(0, self.width() * 0.25)
            self.ui.table_sd_left.setColumnWidth(1, self.width() * 0.125)
            self.ui.table_sd_right.setColumnWidth(0, self.width() * 0.25)
            self.ui.table_sd_right.setColumnWidth(1, self.width() * 0.125)

            # Reset bank sizes
            self.ui.splitter_bank.setSizes(
                [self.width() * 0.535, self.width() * 0.465, self.width() * 0]
            )
            self.ui.splitter_bank_tables.setSizes([self.width() * 0.5, self.width() * 0.5])
            self.ui.table_bank_left.setColumnWidth(0, self.width() * 0.14)
            self.ui.table_bank_right.setColumnWidth(0, self.width() * 0.14)
            self.ui.table_bank_local.setColumnWidth(0, self.width() * 0.16)
            self.ui.table_bank_local.setColumnWidth(1, self.width() * 0.11)
            self.ui.table_bank_local.setColumnWidth(2, self.width() * 0.0625)
            self.ui.table_bank_local.setColumnWidth(3, self.width() * 0.035)

        else:
            # Reset local sizes
            self.ui.splitter_local.setSizes([self.width() * 0.6, self.width() * 0.4])
            self.ui.splitter_local_hori.setSizes(
                [self.height() * 0.55, self.height() * 0.45]
            )
            self.ui.table_local.resizeColumnsToContents()
            self.ui.table_local.setColumnWidth(0, self.width() * 0.165)
            self.ui.table_local.setColumnWidth(1, self.width() * 0.125)
            self.ui.table_local.setColumnWidth(2, self.width() * 0.065)
            self.ui.table_local.setColumnWidth(3, self.width() * 0.075)
            self.ui.table_local.setColumnWidth(4, self.width() * 0.045)
            self.ui.table_local.setColumnWidth(5, self.width() * 0.065)

            # Reset bank sizes
            self.ui.splitter_bank.setSizes(
                [self.width() * 0.535, self.width() * 0.465, self.width() * 0]
            )
            self.ui.splitter_bank_tables.setSizes([self.width() * 0.5, self.width() * 0.5])
            self.ui.table_bank_left.setColumnWidth(0, self.width() * 0.14)
            self.ui.table_bank_right.setColumnWidth(0, self.width() * 0.14)
            self.ui.table_bank_local.setColumnWidth(0, self.width() * 0.16)
            self.ui.table_bank_local.setColumnWidth(1, self.width() * 0.11)
            self.ui.table_bank_local.setColumnWidth(2, self.width() * 0.0625)
            self.ui.table_bank_local.setColumnWidth(3, self.width() * 0.035)

        self.showMaximized()

    def display_patch_info(self):
        """Queries the PS API for additional patch information whenever
        a patch is selected in the PS table or local table. Information
        is displayed via HTML.
        Should the patch contain multiple versions, a call to
        display_patch_versions() is ran instead.
        Currently triggered via a radio button selection.
        """

        skip = False

        # The "sender" here is every radio button, so we need to see
        # which one is actually checked.
        if self.sender().isChecked():
            if (
                (self.ui.tabs.currentIndex() == 1 or self.ui.tabs.currentIndex() == 3)
                and "_" not in self.sender().objectName()
                and len(os.listdir(os.path.join(self.path, self.sender().objectName())))
                > 2
            ):
                # We are pointing to a version directory.
                self.display_patch_versions(self.ui.tabs.currentIndex() == 1)
                return
            # Get the name/version (if applicable).
            name = self.sender().objectName()
            ver = ""
            if "_" in name:
                name, ver = name.split("_")
            curr_browser = None
            # Special case, we are on the PS tab. We have a rolling patch cache
            # to reference so a user can't log multiple views on a patch.
            if self.ui.tabs.currentIndex() == 0:
                curr_browser = self.ui.text_browser_PS
                content = None
                # Try to find the selected item in the patch cache.
                for pch in self.patch_cache:
                    if str(pch["id"]) == name:
                        # Found it, no query needed.
                        content = pch
                        skip = True
                        break
                if content is None:
                    try:
                        # Didn't find it, need to query.
                        content = api.get_patch_meta(name)
                        # Add it to the cache for next time.
                        self.patch_cache.append(content)
                    except Exception as e:
                        # Let the user know the API failed.
                        self.ui.statusbar.showMessage(
                            "API connection failed.", timeout=5000
                        )
                        self.msg.setWindowTitle("API Error")
                        self.msg.setIcon(QMessageBox.Information)
                        self.msg.setText(
                            "Failed to retrieve the patch metadata "
                            "from PatchStorage."
                        )
                        self.msg.setDetailedText(str(e))
                        self.msg.setStandardButtons(QMessageBox.Ok)
                        self.msg.exec_()
                        self.msg.setDetailedText(None)
            else:
                # Get the context.
                viz_browser = None
                if self.ui.tabs.currentIndex() == 1:
                    curr_browser = self.ui.text_browser_local
                    viz_browser = self.ui.page_label
                    self.ui.update_patch_notes.setEnabled(True)
                    self.ui.text_browser_viz.setText("")
                elif self.ui.tabs.currentIndex() == 3:
                    curr_browser = self.ui.text_browser_bank
                self.local.set_local_selected(name)
                # Determine if we need to worry about a version extension.
                if ver != "":
                    self.local.set_local_selected("{}_{}".format(name, ver))
                try:
                    with open(os.path.join(self.path, name, name + ".json")) as f:
                        content = json.loads(f.read())
                except FileNotFoundError:
                    with open(
                        os.path.join(self.path, name, name + "_{}.json".format(ver))
                    ) as f:
                        content = json.loads(f.read())
                # We are on the Local Storage View, so set the viz up.
                if viz_browser is not None:
                    try:
                        with open(
                            os.path.join(self.path, name, name + ".bin"), "rb"
                        ) as f:
                            viz = binary.parse_data(f.read())
                    except FileNotFoundError:
                        with open(
                            os.path.join(self.path, name, name + "_{}.bin".format(ver)),
                            "rb",
                        ) as f:
                            viz = binary.parse_data(f.read())
                    self.local.setup_viz(viz)
                    self.ui.btn_show_routing.setEnabled(True)

            # Oh boy HTML code for the patch preview.
            if not skip:
                if content["preview_url"] == "":
                    content["preview_url"] = "None provided"
                else:
                    content["preview_url"] = (
                        "<a href=" + content["preview_url"] + ">Click here</a>"
                    )

                # Direct link to PS
                if (
                    "link" not in content
                    or content["link"] is None
                    or content["link"] == ""
                ):
                    content["self"] = content["title"]
                else:
                    content["self"] = """<a href="{}">{}</a>""".format(
                        content["link"], content["title"]
                    )

            if (
                "license" not in content
                or content["license"] is None
                or content["license"]["name"] == ""
            ):
                legal = "None provided"
            else:
                legal = content["license"]["name"]

            content["content"] = content["content"].replace("\n", "<br/>")

            # TODO Add artwork to HTML view.
            # Artwork needs to be downloaded ahead of time and then
            # pointed to, as QTextViews don't support downloading from
            # external sources. Maybe create a cache of images? Not
            # easily implementable without speed hitch.

            curr_browser.setHtml(
                """<html>
                <h3>{}</h3>
                <br/><u> Author:</u> {}
                <br/><u> Likes:</u> {}
                <br/><u> Downloads:</u> {}
                <br/><u> Views:</u> {}
                <br/><u> License:</u> {}
                <br/><u> Preview:</u> {}
                <br/><br/><u> Patch Notes:</u><br/> {}
            </html>""".format(
                    content["self"],
                    content["author"]["name"],
                    str(content["like_count"]),
                    str(content["download_count"]),
                    str(content["view_count"]),
                    legal,
                    content["preview_url"],
                    content["content"],
                )
            )

    def display_patch_versions(self, context):
        """Displays the contents of a patch that has multiple versions.
        Currently triggered via a button press.

        context: True for the Local Storage View tab, False for the
                 Folders tab.
        """
        if context:
            # Clean up the tab.
            self.local.set_prev_search(self.ui.searchbar_local.text())
            self.ui.text_browser_local.setText("")
            self.ui.page_label.setText("")
            self.ui.searchbar_local.setText("")
            self.ui.update_patch_notes.setEnabled(False)
            self.ui.back_btn_local.setEnabled(True)
            self.ui.back_btn.setEnabled(False)
            self.ui.btn_prev_page.setEnabled(False)
            self.ui.btn_next_page.setEnabled(False)
            self.local.viz_disable()
            # Prepare the table.
            self.local.get_version_patches(True, self.sender().objectName())
        else:
            # Clean up the tab.
            self.local.set_prev_search(self.ui.searchbar_bank.text())
            self.ui.text_browser_bank.setText("")
            self.ui.searchbar_bank.setText("")
            self.ui.back_btn_bank.setEnabled(True)
            # Prepare the table.
            self.local.get_version_patches(False, self.sender().objectName())

    def search(self):
        """Initiates a data search for the metadata that is retrieved
        via the PS API or that is stored locally. The search will then
        set the table to display the returned query matches.
        Currently triggered via a button press.
        """

        # Case 1: PS tab
        if self.ui.tabs.currentIndex() == 0 and self.ui.searchbar_PS.text() != "":
            self.search_data_PS = util.search_patches(
                self.ps.get_data_ps(), self.ui.searchbar_PS.text()
            )
            self.set_data(True)
        # Case 2: Local tab
        elif self.ui.tabs.currentIndex() == 1 and self.ui.searchbar_local.text() != "":
            # Case 2.1: No version
            # TODO: combine search results by adding the local + versions
            if not self.ui.back_btn_local.isEnabled():
                self.search_data_local = util.search_patches(
                    self.local.get_data_local(), self.ui.searchbar_local.text()
                )
                self.set_data(True)
            # Case 2.2: Version
            else:
                self.search_data_local_version = util.search_patches(
                    self.local.get_data_local_version(), self.ui.searchbar_local.text()
                )
                self.set_data(True, True)
        # Case 3: Bank tab
        elif self.ui.tabs.currentIndex() == 3 and self.ui.searchbar_bank.text() != "":
            # Case 3.1: No version
            if not self.ui.back_btn_bank.isEnabled():
                self.search_data_bank = util.search_patches(
                    self.local.get_data_bank(), self.ui.searchbar_bank.text()
                )
                self.set_data(True)
            # Case 3.2: Version
            else:
                self.search_data_bank_version = util.search_patches(
                    self.local.get_data_bank_version(), self.ui.searchbar_bank.text()
                )
                self.set_data(True, True)

    def sort_and_set(self):
        """Sorts and sets the metadata in a table depending on the
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
                "actionSort_by_downloads_low_high": (4, False),
                "actionSort_by_author_A_Z": (2, False),
                "actionSort_by_author_Z_A": (2, True),
                "actionSort_by_rating_high_low": (8, True),
                "actionSort_by_rating_low_high": (8, False),
                "actionSort_by_category_high_low": (9, False),
                "actionSort_by_category_low_high": (9, True),
                "actionSort_by_tag_high_low": (10, False),
                "actionSort_by_tag_low_high": (10, True),
            }[self.sender().objectName()]
            self.prev_sort = curr_sort
        except KeyError:
            curr_sort = self.prev_sort
        except AttributeError:
            if self.prev_sort is None:
                curr_sort = (6, True)
                self.prev_sort = curr_sort
            else:
                curr_sort = self.prev_sort

        table_index = self.ui.tabs.currentIndex()

        # Determine the context in which to perform the sort.
        # Case 1: A user forces a reload of the PS patch list.
        if (
            self.sender() is not None
            and self.sender().objectName() == "refresh_pch_btn"
        ):
            util.sort_metadata(curr_sort[0], self.ps.get_data_ps(), curr_sort[1])
            self.set_data(self.ui.searchbar_PS.text() != "")
        # Case 2: Sorting on the PatchStorage tab.
        # ->Case 2.1: Sorting on the PS tab with the search bar empty.
        elif table_index == 0 and self.ui.searchbar_PS.text() == "":
            util.sort_metadata(curr_sort[0], self.ps.get_data_ps(), curr_sort[1])
            self.set_data()
        # ->Case 2.2: Sorting on the PS tab with the search bar containing
        #             text.
        elif table_index == 0 and self.ui.searchbar_PS.text() != "":
            if self.search_data_PS is None:
                self.search_data_PS = self.ps.get_data_ps()
            util.sort_metadata(curr_sort[0], self.search_data_PS, curr_sort[1])
            self.set_data(True)
        # Case 3: Sorting on the Local Storage View tab.
        # ->Case 3.1: Sorting on the Local tab, no version, and an empty
        #             search bar
        elif (
            table_index == 1
            and self.ui.searchbar_local.text() == ""
            and not self.ui.back_btn_local.isEnabled()
        ):
            util.sort_metadata(curr_sort[0], self.local.get_data_local(), curr_sort[1])
            self.set_data()
        # ->Case 3.2: Local tab, no version, text in the search bar.
        elif (
            table_index == 1
            and self.ui.searchbar_local.text() != ""
            and not self.ui.back_btn_local.isEnabled()
        ):
            if self.search_data_local is None:
                self.search_data_local = self.local.get_data_local()
            util.sort_metadata(curr_sort[0], self.search_data_local, curr_sort[1])
            self.set_data(True)
        # ->Case 3.3: Local tab, it is a version, no text in the search bar.
        elif (
            table_index == 1
            and self.ui.searchbar_local.text() == ""
            and self.ui.back_btn_local.isEnabled()
        ):
            util.sort_metadata(7, self.local.get_data_local_version(), True)
            self.set_data(version=True)
        # ->Case 3.4: Local tab, it is a version, and text is in the search
        #             bar.
        elif (
            table_index == 1
            and self.ui.searchbar_local.text() != ""
            and self.ui.back_btn_local.isEnabled()
        ):
            if self.search_data_local_version is None:
                self.search_data_local_version = self.local.get_data_local_version()
            util.sort_metadata(7, self.search_data_local_version, True)
            self.set_data(True, True)
        # Case 4: Sorting on the Folders tab.
        # ->Case 4.1: Sorting on the Folders tab, no version, and an empty search
        #             bar.
        elif (
            table_index == 3
            and self.ui.searchbar_bank.text() == ""
            and not self.ui.back_btn_bank.isEnabled()
        ):
            util.sort_metadata(curr_sort[0], self.local.get_data_bank(), curr_sort[1])
            self.set_data()
        # ->Case 4.2: Bank tab, no version, text in the search bar.
        elif (
            table_index == 3
            and self.ui.searchbar_bank.text() != ""
            and not self.ui.back_btn_bank.isEnabled()
        ):
            if self.search_data_bank is None:
                self.search_data_bank = self.local.get_data_bank()
            util.sort_metadata(curr_sort[0], self.search_data_bank, curr_sort[1])
            self.set_data(True)
        # ->Case 4.3: Bank tab, it is a version, no text in the search bar.
        elif (
            table_index == 3
            and self.ui.searchbar_bank.text() == ""
            and self.ui.back_btn_bank.isEnabled()
        ):
            util.sort_metadata(7, self.local.get_data_bank_version(), True)
            self.set_data(version=True)
        # ->Case 4.4: Bank tab, it is a version, and text is in the search bar.
        elif (
            table_index == 3
            and self.ui.searchbar_bank.text() != ""
            and self.ui.back_btn_bank.isEnabled()
        ):
            if self.search_data_bank_version is None:
                self.search_data_bank_version = self.local.get_data_bank_version()
            util.sort_metadata(7, self.search_data_bank_version, True)
            self.set_data(True, True)

    def import_patch(self):
        """Attempts to import a patch into the librarian.
        Currently triggered via a menu action.
        """

        pch = QFileDialog.getOpenFileName(
            None, "Select a file", expanduser("~")
        )[0]
        # Didn't make a selection.
        if pch == "":
            return
        try:
            save.import_to_backend(pch)
            self.ui.statusbar.showMessage("Import complete.", timeout=5000)
            # self.msg.setWindowTitle("Import Complete")
            # self.msg.setText("The patch has been successfully imported.")
            # self.msg.exec_()
            # Reload the tables if we are currently displaying them.
            self.tab_switch()
            # if (
            #     self.ui.tabs.currentIndex() == 1
            #     and not self.ui.back_btn_local.isEnabled()
            # ) or (
            #     self.ui.tabs.currentIndex() == 3
            #     and not self.ui.back_btn_bank.isEnabled()
            # ):
            #     self.local.get_local_patches()
        # Let the user know of any errors that occurred.
        except errors.BadPathError:
            self.ui.statusbar.showMessage("Import failed.", timeout=5000)
            self.msg.setWindowTitle("No Patch Found")
            self.msg.setText("Incorrect file selected, importing failed.")
            self.msg.exec_()
        except errors.SavingError as e:
            e = str(e).split("(")[1].split(")")[0].split(",")[0].replace("'", "")
            # Prepare a message box.
            self.ui.statusbar.showMessage("Import not applicable.", timeout=5000)
            self.msg.setWindowTitle("Patch Already In Library")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "That patch exists within your locally "
                "saved patches as {}. \nNo importing has occurred.".format(e)
            )
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()

    def directory_select(self):
        """Allows the user to select a directory via their OS specific
        file explorer.

        return: The path of the directory chosen, as a string.
                Will be None if no directory is chosen.
        """

        # Let the user specify a directory.
        input_dir = QFileDialog.getExistingDirectory(
            None, "Select a directory", expanduser("~")
        )
        if input_dir == "":
            return None
        elif not os.path.isdir(input_dir):
            self.msg.setWindowTitle("Invalid Selection")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please select a directory.")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
        return input_dir

    def _mass_import_thread(self):
        """Initializes a Worker thread to manage the importing of
        patches as individual patches into the backend.
        Currently triggered via a menu action.
        TODO fix the menu action imports
        Fatal Python error: This thread state must be current when releasing
        """

        self.worker_mass.start()

    def _mass_import_thread_sd(self):
        """Initializes a Worker thread to manage the importing of
        patches as individual patches into the backend.
        Currently triggered via a button press.
        """

        self.worker_mass_sd.start()

    def _mass_import_done(self, imp_cnt, fail_cnt, fails):
        """Notifies the user once the mass import has completed.
        Will also notify the user with the number of patches that were
        successfully imported and the number of patches that were not
        imported.

        imp_cnt: The number of patches that were imported, as an int.
        fail_cnt: The number of patches that failed to import, as an
                  int.
        fails: The list of patches which failed to import.
        """

        # Prepare a popup for the user.
        self.msg.setWindowTitle("Import Complete")
        self.msg.setIcon(QMessageBox.Information)
        if imp_cnt > 0:
            self.ui.statusbar.showMessage("Import complete.", timeout=5000)
            self.msg.setText("Successfully imported {} patches.".format(imp_cnt))
        else:
            self.ui.statusbar.showMessage("Import failed.", timeout=5000)
            self.msg.setText("Did not import any patches.")
        if fail_cnt > 0:
            self.ui.statusbar.showMessage("Import partially complete.", timeout=5000)
            word = "was" if fail_cnt == 1 else "were"
            self.msg.setInformativeText(
                "{} {} already saved in the library and {} not imported.".format(
                    fail_cnt, word, word
                )
            )
            temp = "List of patches that failed to import: \n"
            for x in fails:
                temp += x + "\n"
            self.msg.setDetailedText(temp.strip("\n"))
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
        self.msg.setInformativeText(None)
        self.msg.setDetailedText(None)
        self.tab_switch()
        # if (
        #     self.ui.tabs.currentIndex() == 1 and not self.ui.back_btn_local.isEnabled()
        # ) or (
        #     self.ui.tabs.currentIndex() == 3 and not self.ui.back_btn_bank.isEnabled()
        # ):
        #     # Reload the table to show the new patches.
        #     self.local.get_local_patches()

    def _version_import_thread(self):
        """Initializes a Worker thread to manage the importing of
        patches as a version directory into the backend.
        Currently triggered via a menu action.
        TODO fix the menu-action imports
        Fatal Python error: This thread state must be current when releasing
        """

        self.worker_version.start()

    def _version_import_thread_sd(self):
        """Initializes a Worker thread to manage the importing of
        patches as a version directory into the backend.
        Currently triggered via a button press.
        """

        self.worker_version_sd.start()

    def _version_import_done(self, count, fail_cnt, fails):
        """Notifies the user once the version import has completed.
        Will also notify the user with the number of patches that failed
        to be imported if they already existed within the Librarian.
        Should be expanded to list which patches failed to import.

        count: The number of patches attempted to be imported, as an int.
        fail_cnt: The number of patches that failed to import, as an int.
        fails: The list of patches which failed to import.
        """

        # Prepare a popup for the user.
        if fail_cnt == 0:
            self.ui.statusbar.showMessage("Import complete.", timeout=5000)
            self.msg.setWindowTitle("Success")
            self.msg.setText("Successfully created a Version History.")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
        elif count > fail_cnt >= 1:
            self.ui.statusbar.showMessage("Import partially complete.", timeout=5000)
            self.msg.setWindowTitle("Warning")
            word = "was" if fail_cnt == 1 else "were"
            self.msg.setText(
                "Certain patches in the specified Version "
                "History already existed in the Librarian. "
                "Please delete them before attempting to "
                "import a version history if you would like "
                "them to appear."
            )
            self.msg.setInformativeText(
                "Successfully created a partial Version History. "
                "{} {} already saved in the library and {} not imported.".format(
                    fail_cnt, word, word
                )
            )
            temp = "List of patches that failed to import: \n"
            for x in fails:
                temp += x + "\n"
            self.msg.setDetailedText(temp.strip("\n"))
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setInformativeText(None)
            self.msg.setDetailedText(None)
        else:
            self.ui.statusbar.showMessage("Import failed.", timeout=5000)
            self.msg.setWindowTitle("Warning")
            word = "was" if fail_cnt == 1 else "were"
            self.msg.setText(
                "All patches in the specified Version "
                "History already existed in the Librarian. "
                "Please delete them before attempting to "
                "import a version history if you would like "
                "them to appear."
            )
            self.msg.setInformativeText(
                "Did not create a Version History. "
                "{} {} already saved in the library and {} not imported.".format(
                    fail_cnt, word, word
                )
            )
            temp = "List of patches that failed to import: \n"
            for x in fails:
                temp += x + "\n"
            self.msg.setDetailedText(temp.strip("\n"))
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setInformativeText(None)
            self.msg.setDetailedText(None)
        self.tab_switch()
        # if (
        #     self.ui.tabs.currentIndex() == 1 and not self.ui.back_btn_local.isEnabled()
        # ) or (
        #     self.ui.tabs.currentIndex() == 3 and not self.ui.back_btn_bank.isEnabled()
        # ):
        #     # Reload the table to show the new patches.
        #     self.local.get_local_patches()

    # def expand_patch_thread(self):
    #     """Initializes a Worker thread to load the expanded display
    #     of a given binary patch.
    #     """
    #
    #     # Disable the necessary buttons and start the thread.
    #     self.ui.btn_show_routing.setEnabled(False)
    #     self.ui.check_for_updates_btn.setEnabled(False)
    #     self.ui.refresh_pch_btn.setEnabled(False)
    #     self.ui.btn_dwn_all.setEnabled(False)
    #     self.ui.statusbar.showMessage("Generating the expanded view...")
    #     self.worker_expander.start()
    #
    # def expand_patch_done(self, msg):
    #     """"""
    #
    #     # Re-enable the buttons now that the thread is done.
    #     self.ui.btn_show_routing.setEnabled(True)
    #     self.ui.check_for_updates_btn.setEnabled(True)
    #     self.ui.refresh_pch_btn.setEnabled(True)
    #     self.ui.btn_dwn_all.setEnabled(True)

    def eventFilter(self, o, e):
        """Deals with events that originate from various widgets
        present in the GUI.

        o: The source object that triggered the event.
        e: The event that was triggered.
        """

        # SD card tab swap/move
        if o.objectName() == "table_sd_left" or o.objectName() == "table_sd_right":
            self.sd.events(o, e)
        # Bank tab swap/move
        elif (
            o.objectName() == "table_bank_local"
            or o.objectName() == "table_bank_left"
            or o.objectName() == "table_bank_right"
        ):
            self.bank.events(o, e)
        # Searching via searchbar
        elif (
            o.objectName() == "searchbar_PS"
            or o.objectName() == "searchbar_local"
            or o.objectName() == "searchbar_bank"
        ):
            if e.type() == QEvent.KeyRelease:
                if (
                    self.ui.searchbar_local.text() == ""
                    and self.ui.tabs.currentIndex() == 1
                    and not self.ui.back_btn_local.isEnabled()
                ):
                    self.local.get_local_patches()
                elif (
                    self.ui.searchbar_PS.text() == ""
                    and self.ui.tabs.currentIndex() == 0
                ):
                    self.sort_and_set()
                elif (
                    self.ui.searchbar_local.text() == ""
                    and self.ui.tabs.currentIndex() == 1
                    and self.ui.back_btn_local.isEnabled()
                ):
                    self.local.get_version_patches(True)
                elif (
                    self.ui.searchbar_bank.text() == ""
                    and self.ui.tabs.currentIndex() == 3
                    and not self.ui.back_btn_bank.isEnabled()
                ):
                    self.local.get_local_patches()
                elif (
                    self.ui.searchbar_bank.text() == ""
                    and self.ui.tabs.currentIndex() == 3
                    and self.ui.back_btn_bank.isEnabled()
                ):
                    self.local.get_version_patches(False)
                return True
        # Update tags/categories on Local tab.
        elif o.objectName() == "table_local":
            self.local.events(e)
        return False

    def import_multiple_menu(self):
        imp_cnt = 0
        fail_cnt = 0
        fails = []

        input_dir = self.directory_select()

        if not input_dir:
            return

        for pch in os.listdir(input_dir):
            if pch.split(".")[-1] == "bin":
                # Try to save the binary.
                try:
                    save.import_to_backend(os.path.join(input_dir, pch))
                    imp_cnt += 1
                except errors.SavingError as e:
                    fail_cnt += 1
                    e = (
                        str(e)
                        .split("(")[1]
                        .split(")")[0]
                        .split(",")[0]
                        .replace("'", "")
                    )
                    fails.append(e)

        return self._mass_import_done(imp_cnt, fail_cnt, fails)

    def import_version_menu(self):
        input_dir = self.directory_select()
        if not input_dir:
            return

        count, fail_cnt, fails = save.import_to_backend(input_dir, True)

        return self._version_import_done(count, fail_cnt, fails)

    def closeEvent(self, event):
        """Override the default close operation so certain application
        settings can be saved.
        """

        self.util.save_pref(
            self.width(), self.height(), self.sd.get_sd_root(), self.path
        )

    def _try_quit(self):
        """Forces the application to close.
        Currently triggered via a menu action.
        """

        # Save application settings and then exit.
        self.closeEvent(None)
        self.close()


class ImportMassWorker(QThread):
    """The ImportMassWorker class runs as a separate thread in the
    application to prevent application snag. This thread will attempt
    to import specified binary files into the backend as individual
    patches.
    """

    # UI communication
    signal = QtCore.Signal(int, int, list)

    def __init__(self, window):
        """Initializes the thread."""

        QThread.__init__(self)
        self.window = window

    def run(self):
        """Attempts to mass import any patches found within a target
        directory. Unlike import_patch, failing to import a patch will
        not create a message box. A message box will be displayed at the
        end indicating how many patches were and were not imported.
        Currently triggered via a button press or a menu action.
        """

        imp_cnt = 0
        fail_cnt = 0
        fails = []

        input_dir = self.window.directory_select()

        for pch in os.listdir(input_dir):
            if pch.split(".")[1] == "bin":
                # Try to save the binary.
                try:
                    save.import_to_backend(os.path.join(input_dir, pch))
                    imp_cnt += 1
                except errors.SavingError as e:
                    fail_cnt += 1
                    e = (
                        str(e)
                        .split("(")[1]
                        .split(")")[0]
                        .split(",")[0]
                        .replace("'", "")
                    )
                    fails.append(e)

        self.signal.emit(imp_cnt, fail_cnt, fails)


class ImportVersionWorker(QThread):
    """The ImportVersionWorker class runs as a separate thread in the
    application to prevent application snag. This thread will attempt
    to import specified binary files into the backend as a version
    history.
    """

    # UI communication
    signal = QtCore.Signal(int, int, list)

    def __init__(self, window):
        """Initializes the thread."""

        QThread.__init__(self)
        self.window = window

    def run(self):
        """Attempts to import a directory of patches as a version
        history within the application. Should any non-bin files be
        encountered, they will simply be ignored.
        Currently triggered via a button press or a menu action.
        """

        input_dir = self.window.directory_select()
        count, fail_cnt, fails = save.import_to_backend(input_dir, True)
        self.signal.emit(count, fail_cnt, fails)


class ImportMassSDWorker(QThread):
    """The ImportMassSDWorker class runs as a separate thread in the
    application to prevent application snag. This thread will attempt
    to import specified binary files into the backend as individual
    patches that reside on an SD card.
    """

    # UI communication
    signal = QtCore.Signal(int, int, list)

    def __init__(self, window):
        """Initializes the thread."""

        QThread.__init__(self)
        self.window = window

    def run(self):
        """Attempts to mass import any patches found within a target
        directory. Unlike import_patch, failing to import a patch will
        not create a message box. A message box will be displayed at the
        end indicating how many patches were and were not imported.
        Currently triggered via a button press or a menu action.
        """

        imp_cnt = 0
        fail_cnt = 0
        fails = []

        input_dir = self.window.sd.get_sd_path()

        for pch in os.listdir(input_dir):
            if pch.split(".")[1] == "bin":
                # Try to save the binary.
                try:
                    save.import_to_backend(os.path.join(input_dir, pch))
                    imp_cnt += 1
                except errors.SavingError as e:
                    fail_cnt += 1
                    e = (
                        str(e)
                        .split("(")[1]
                        .split(")")[0]
                        .split(",")[0]
                        .replace("'", "")
                    )
                    fails.append(e)

        self.signal.emit(imp_cnt, fail_cnt, fails)


class ImportVersionSDWorker(QThread):
    """The ImportVersionSDWorker class runs as a separate thread in the
    application to prevent application snag. This thread will attempt
    to import specified binary files into the backend as a version
    history that are located on an SD card.
    """

    # UI communication
    signal = QtCore.Signal(int, int, list)

    def __init__(self, window):
        """Initializes the thread."""

        QThread.__init__(self)
        self.window = window

    def run(self):
        """Attempts to import a directory of patches as a version
        history within the application. Should any non-bin files be
        encountered, they will simply be ignored.
        Currently triggered via a button press or a menu action.
        """

        input_dir = self.window.sd.get_sd_path()
        count, fail_cnt, fails = save.import_to_backend(input_dir, True)
        self.signal.emit(count, fail_cnt, fails)


# class DisplayExpandedRouting(QThread):
#     """The DisplayExpandedRouting class runs as a separate thread in the
#     application to prevent application snag. This thread will attempt
#     to display the expanded routing for a given binary file on the
#     Local Storage tab.
#     """
#
#     # UI communication
#     signal = QtCore.Signal(str)
#
#     def __init__(self, window):
#         """Initializes the thread."""
#
#         QThread.__init__(self)
#         self.window = window
#
#     def run(self):
#         """Attempts to display the expanded patch for a given binary file.
#         Currently triggered by a button press.
#         """
#
#         curr_viz = self.window.local.get_viz()
#         setup_exp(curr_viz)
#         self.signal.emit()
