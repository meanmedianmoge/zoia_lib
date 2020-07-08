import json
import os
from os.path import expanduser

from PySide2.QtCore import QEvent
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import zoia_lib.UI.early_ui as ui_main
import zoia_lib.backend.api as api
import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors

ps = api.PatchStorage()
backend_path = util.get_backend_path()


class EarlyUIMain(QMainWindow):
    """ ** TEMPORARY FUNCTIONALITY SHOWCASE **

    The EarlyUIMain class represents the frontend for the
    application. It allows users to interact with the various backend
    functions available. These include searching, download, sorting,
    and exporting patches.

    Any changes made to the .ui file will not be reflected unless the
    following command is run from the UI directory:
        pyside2-uic.exe .\early.ui -o .\early_ui.py

    Known issues:
     - Version history is not implemented in the frontend.
     - Importing is not implemented.
     - Bank creation, re-arranging, and exporting is not implemented.
     - The window icon does not display properly.
    """

    def __init__(self):
        """ Initializes the UI for the application. Currently, upon
        being launched for the first time, it queries the PS API for all
        ZOIA patches and gets the metadata. Upon subsequent launches,
        it will search for previously stored metadata, compare it to
        the # of patches currently on PS, and either begin using the
        cached data, or get the most recent patches and add them to the
        cache; and subsequently starting the application.
        """

        super(EarlyUIMain, self).__init__()
        # Setup the UI using throwaway.py
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)

        # Check for metadata in the user's backend.
        if "data.json" not in os.listdir(backend_path):
            ps_data = ps.get_all_patch_data_init()
            with open(os.path.join(backend_path, "data.json"),
                      "w") as f:
                f.write(json.dumps(ps_data))
                self.data = ps_data
        else:
            # Got previous metadata, need to ensure that there are no
            # new patches.
            with open(os.path.join(backend_path, "data.json"),
                      "r") as f:
                data = json.loads(f.read())
            if len(data) == ps.patch_count:
                # No new patches.
                self.data = data
            elif len(data) > ps.patch_count:
                # Uh oh, some patches got deleted on PatchStorage.
                ps_data = ps.get_all_patch_data_init()
                with open(os.path.join(backend_path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(ps_data))
                    self.data = ps_data
            else:
                # Get the new patch metadata that we don't have.
                new_patches = ps.get_newest_patches(len(data))
                data = new_patches + data
                with open(os.path.join(backend_path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(data))
                    self.data = data

        # Set the window icon
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "zoia_lib", "UI",
                                              "resources", "logo.ico")))

        # Variable initialization.
        self.search_data = None
        self.sd_card_root = None
        self.sd_card_path = None
        self.local_data = None
        self.search_local_data = None
        self.local_selected = None
        self.selected = None
        self.prev_tag_cat = None
        self.dark = False
        self.table_title_size = None
        self.table_2_title_size = None

        # Setup the tables, but only populate the PS API table
        # (The local table will populate once the user switches tabs).
        self.ui.table.setRowCount(len(self.data))
        self.set_data(False)

        self.ui.table_2.setRowCount(len(self.data))

        self.ui.table_3.setHorizontalHeaderLabels(["Patch", "Remove",
                                                   "Import"])
        self.ui.table_4.setHorizontalHeaderLabels(["Patch", "Remove",
                                                   "Import"])
        self.ui.table_3.setColumnWidth(0, 400)
        self.ui.table_3.setColumnWidth(1, 100)
        self.ui.table_4.setColumnWidth(0, 400)
        self.ui.table_4.setColumnWidth(1, 100)
        self.ui.tab_sd.setEnabled(False)

        # Connect buttons and items to methods.
        self.ui.left_widget.currentChanged.connect(self.get_local_patches)
        self.ui.actionAlternating_Row_Colours.triggered.connect(
            self.row_invert)
        self.ui.actionSort_by_title_A_Z.triggered.connect(self.sort)
        self.ui.actionSort_by_title_Z_A.triggered.connect(self.sort)
        self.ui.actionSort_by_date_new_old.triggered.connect(self.sort)
        self.ui.actionSort_by_date_old_new.triggered.connect(self.sort)
        self.ui.actionSort_by_likes_high_low.triggered.connect(self.sort)
        self.ui.actionSort_by_likes_low_high.triggered.connect(self.sort)
        self.ui.actionSort_by_views_high_low.triggered.connect(self.sort)
        self.ui.actionSort_by_views_low_high.triggered.connect(self.sort)
        self.ui.actionSort_by_downloads_high_low.triggered.connect(self.sort)
        self.ui.actionSort_by_downloads_low_high.triggered.connect(self.sort)
        self.ui.actionSpecify_SD_Card_Location.triggered.connect(self.sd_path)
        self.ui.actionCheck_For_Updates.triggered.connect(self.update)
        self.ui.actionReload_PatchStorage_patch_list.triggered.connect(
            self.reload_ps)
        self.ui.actionQuit.triggered.connect(self.try_quit)
        self.ui.update_patch_notes.clicked.connect(self.update_patch_notes)
        self.ui.actionImport_A_Patch.triggered.connect(self.import_patch)
        self.ui.actionToggle_Dark_Mode.triggered.connect(self.toggle_darkmode)
        self.ui.table_2.installEventFilter(self)
        self.ui.table_3.installEventFilter(self)
        self.ui.table_4.installEventFilter(self)
        self.ui.searchbar_3.returnPressed.connect(self.search)
        self.ui.searchbar_3.installEventFilter(self)
        self.ui.searchbar_4.installEventFilter(self)
        self.ui.searchbar_4.returnPressed.connect(self.search)
        self.ui.sd_tree.clicked.connect(self.prepare_sd_view)
        self.ui.import_all_btn.clicked.connect(self.mass_import)

        # Font consistency.
        self.ui.table.setFont(QFont('Verdana', 10))
        self.ui.table_2.setFont(QFont('Verdana', 10))
        self.ui.text_browser.setFont(QFont('Verdana', 16))
        self.ui.text_browser_2.setFont(QFont('Verdana', 16))

        # Modify the display sizes for some widgets.
        self.ui.splitter.setSizes([500, 500])
        self.ui.splitter_2.setSizes([500, 500])
        self.ui.splitter_3.setSizes([500, 500])
        self.ui.splitter_4.setSizes([500, 500])
        self.ui.splitter_5.setSizes([220, 780])

        # Ensure the application starts as maximized.
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui.update_patch_notes.setEnabled(False)
        self.ui.import_all_btn.setEnabled(False)
        self.sort()
        self.showMaximized()

    def get_local_patches(self):
        """ Gets a list of local patch metadata from the backend
        directory.

        TODO Expand this to accurately deal with version history
         (array in the array).
        """

        self.prev_tag_cat = None

        if self.ui.left_widget.currentIndex() == 1:
            self.local_data = []
            for patches in os.listdir(backend_path):
                if patches != "Banks" and patches != "data.json" and \
                        patches != '.DS_Store':
                    if len(os.listdir(os.path.join(backend_path,
                                                   patches))) == 2:
                        for pch in os.listdir(os.path.join(backend_path,
                                                           patches)):
                            if pch.split(".")[1] == "json":
                                with open(os.path.join(backend_path,
                                                       patches, pch)) as f:
                                    temp = json.loads(f.read())
                                self.local_data.append(temp)
                    else:
                        # Multiple versions, just do v1 for now.
                        for pch in os.listdir(os.path.join(backend_path,
                                                           patches)):
                            if pch.split(".")[1] == "json":
                                with open(os.path.join(backend_path,
                                                       patches, pch)) as f:
                                    temp = json.loads(f.read())
                                self.local_data.append(temp)
                                break
            self.set_data_local(False)
        elif self.ui.left_widget.currentIndex() == 2:
            # SD card tab
            if self.sd_card_root is None:
                msg = QMessageBox()
                msg.setWindowTitle("No SD Path")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Please specify your SD card path!")
                msg.setInformativeText("File -> Specify SD Card Location")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.ui.left_widget.setCurrentIndex(1)

    def prepare_sd_view(self):
        self.ui.import_all_btn.setEnabled(False)
        path = self.ui.sd_tree.currentIndex().data()
        temp = self.ui.sd_tree.currentIndex()
        while True:
            temp = temp.parent()
            if temp.data() is not None and self.sd_card_root \
                    not in temp.data():
                path = os.path.join(temp.data(), path)
            else:
                break
        self.sd_card_path = os.path.join(self.sd_card_root, path)
        self.set_data_sd()
        for i in range(64):
            if i < 32:
                if self.ui.table_3.item(i, 0).text() != "":
                    self.ui.import_all_btn.setEnabled(True)
                    break
            else:
                if self.ui.table_4.item(i - 32, 0).text() != "":
                    self.ui.import_all_btn.setEnabled(True)
                    break

    def set_data_sd(self):
        """ Sets the data for the PS table.
        Currently triggered via a mouse click.
        """
        for i in range(32):
            self.ui.table_3.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_3.setCellWidget(i, 1, None)
            self.ui.table_3.setCellWidget(i, 2, None)
            self.ui.table_4.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_4.setCellWidget(i, 1, None)
            self.ui.table_4.setCellWidget(i, 2, None)

        if not os.path.isdir(self.sd_card_path):
            return

        for pch in os.listdir(self.sd_card_path):
            # Get the index
            index = pch.split("_")[0]
            if index[0] == "0":
                if index[1] == "0":
                    # one digit
                    index = int(index[2])
                else:
                    # two digits
                    index = int(index[1:3])
                if index < 32:
                    self.ui.table_3.setItem(index, 0, QTableWidgetItem(pch))
                    push_button = QPushButton("X")
                    push_button.setObjectName(str(index))
                    push_button.setFont(QFont('Verdana', 10))
                    push_button.clicked.connect(self.remove_sd)
                    self.ui.table_3.setCellWidget(index, 1, push_button)
                    import_btn = QPushButton("Click me to import!")
                    import_btn.setObjectName(str(index))
                    import_btn.setFont(QFont('Verdana', 10))
                    import_btn.clicked.connect(self.import_patch)
                    self.ui.table_3.setCellWidget(index, 2, import_btn)
                else:
                    self.ui.table_4.setItem(index - 32, 0,
                                            QTableWidgetItem(pch))
                    push_button = QPushButton("X")
                    push_button.setObjectName(str(index))
                    push_button.setFont(QFont('Verdana', 10))
                    push_button.clicked.connect(self.remove_sd)
                    self.ui.table_4.setCellWidget(index - 32, 1, push_button)
                    self.ui.table_4.setCellWidget(index - 32, 1, push_button)
                    import_btn = QPushButton("Click me to import!")
                    import_btn.setObjectName(str(index))
                    import_btn.setFont(QFont('Verdana', 10))
                    import_btn.clicked.connect(self.import_patch)
                    self.ui.table_4.setCellWidget(index - 32, 2, import_btn)

    def set_data(self, search):
        """ Sets the data for the PS table. This is done when the app
        begins, whenever the tab is returned to, or whenever a search
        is initiated.
        """

        self.ui.table.clear()
        if search:
            data = self.search_data
        else:
            data = self.data
        self.ui.table.setRowCount(len(data))
        hor_headers = ["Title", "Tags", "Categories", "Date Modified",
                       "Download"]
        for i in range(len(data)):
            btn_title = QRadioButton(data[i]["title"], self)
            btn_title.setObjectName(str(data[i]["id"]))
            btn_title.toggled.connect(self.display_patch_info)
            self.ui.table.setCellWidget(i, 0, btn_title)
            tags = ""

            if len(data[i]["tags"]) > 2:
                for j in range(0, len(data[i]["tags"]) - 1):
                    tags += data[i]["tags"][j]["name"] + ", "
                tags = tags + "and " \
                       + data[i]["tags"][len(data[i]["tags"]) - 1]["name"]
            elif len(data[i]["tags"]) == 2:
                tags = data[i]["tags"][0]["name"] + " and " \
                       + data[i]["tags"][1]["name"]
            else:
                tags = data[i]["tags"][0]["name"]

            tag_item = QTableWidgetItem(tags)
            tag_item.setTextAlignment(Qt.AlignCenter)
            self.ui.table.setItem(i, 1, tag_item)

            cat = ""

            if len(data[i]["categories"]) > 2:
                for j in range(0, len(data[i]["categories"]) - 1):
                    cat += data[i]["categories"][j]["name"] + ", "
                cat = cat + "and " \
                      + data[i]["categories"][len(data[i]["categories"])
                                              - 1]["name"]
            elif len(data[i]["categories"]) == 2:
                cat = data[i]["categories"][0]["name"] + " and " \
                      + data[i]["categories"][1]["name"]
            else:
                cat = data[i]["categories"][0]["name"]

            cat_item = QTableWidgetItem(cat)
            cat_item.setTextAlignment(Qt.AlignCenter)
            self.ui.table.setItem(i, 2, cat_item)

            date = QTableWidgetItem(data[i]["updated_at"][:10])
            date.setTextAlignment(Qt.AlignCenter)
            self.ui.table.setItem(i, 3, date)
            dwn = QPushButton("Click me\nto download!", self)
            dwn.setFont(QFont('Verdana', 10))
            dwn.clicked.connect(self.initiate_download)
            dwn.setObjectName(str(data[i]["id"]))

            if (str(data[i]["id"])) in os.listdir(backend_path):
                dwn.setEnabled(False)
                dwn.setText("Downloaded!")

            self.ui.table.setCellWidget(i, 4, dwn)
        self.ui.table.setHorizontalHeaderLabels(hor_headers)
        self.ui.table.resizeColumnsToContents()
        if self.table_title_size is None:
            self.table_title_size = self.ui.table.columnWidth(0)
        else:
            self.ui.table.setColumnWidth(0, self.table_title_size)
        self.ui.table.setColumnWidth(1, 140)
        self.ui.table.setColumnWidth(2, 140)
        self.ui.table.resizeRowsToContents()

    def set_data_local(self, search):
        """ Sets the data for the PS table. This is done whenever the
        tab is returned to, or whenever a search is initiated.
        """

        self.ui.table_2.clear()
        if search:
            data = self.search_local_data
        else:
            data = self.local_data
        self.ui.table_2.setRowCount(len(data))
        hor_headers = ["Title", "Tags", "Categories", "Date Modified",
                       "Export", "Delete"]
        for i in range(len(data)):
            btn_title = QRadioButton(data[i]["title"], self)
            btn_title.setObjectName(str(data[i]["id"]))
            btn_title.toggled.connect(self.display_patch_info)
            self.ui.table_2.setCellWidget(i, 0, btn_title)
            tags = ""
            if len(data[i]["tags"]) > 2:
                for j in range(0, len(data[i]["tags"]) - 1):
                    tags += data[i]["tags"][j]["name"] + ", "
                tags = tags + "and " \
                       + data[i]["tags"][len(data[i]["tags"]) - 1]["name"]
            elif len(data[i]["tags"]) == 2:
                tags = data[i]["tags"][0]["name"] + " and " \
                       + data[i]["tags"][1]["name"]
            elif len(data[i]["tags"]) == 0:
                tags = "No tags"
            else:
                tags = data[i]["tags"][0]["name"]

            tag_item = QTableWidgetItem(tags)
            tag_item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_2.setItem(i, 1, tag_item)

            cat = ""

            if len(data[i]["categories"]) > 2:
                for j in range(0, len(data[i]["categories"]) - 1):
                    cat += data[i]["categories"][j]["name"] + ", "
                cat = cat + "and " + \
                      data[i]["categories"][len(data[i]["categories"])
                                            - 1]["name"]
            elif len(data[i]["categories"]) == 2:
                cat = data[i]["categories"][0]["name"] + " and " \
                      + data[i]["categories"][1]["name"]
            elif len(data[i]["categories"]) == 0:
                cat = "No categories"
            else:
                cat = data[i]["categories"][0]["name"]

            cat_item = QTableWidgetItem(cat)
            cat_item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_2.setItem(i, 2, cat_item)
            date = QTableWidgetItem(data[i]["updated_at"][:10])
            date.setTextAlignment(Qt.AlignCenter)
            self.ui.table_2.setItem(i, 3, date)
            expt = QPushButton("Click me\nto export!")
            expt.setObjectName(str(data[i]["id"]))
            expt.setFont(QFont('Verdana', 10))
            expt.clicked.connect(self.initiate_export)
            self.ui.table_2.setCellWidget(i, 4, expt)
            delete = QPushButton("X")
            delete.setObjectName(str(data[i]["id"]))
            delete.setFont(QFont('Verdana', 10))
            delete.clicked.connect(self.initiate_delete)
            self.ui.table_2.setCellWidget(i, 5, delete)
        self.ui.table_2.setHorizontalHeaderLabels(hor_headers)
        self.ui.table_2.resizeColumnsToContents()
        if self.table_2_title_size is None:
            self.table_2_title_size = self.ui.table_2.columnWidth(0)
        else:
            self.ui.table_2.setColumnWidth(0, self.table_2_title_size)
        self.ui.table_2.setColumnWidth(1, 140)
        self.ui.table_2.setColumnWidth(2, 140)
        self.ui.table_2.setColumnWidth(4, 100)
        self.ui.table_2.setColumnWidth(5, 100)
        self.ui.table_2.resizeRowsToContents()

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
            util.save_to_backend(ps.download(str(self.sender().objectName())))
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
        """ **TEMPORARY METHOD** - Will be removed once the UI is
                                   expanded.

        Attempts to export a patch saved in the backend to an SD
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
                                                 "Slot number:",
                                                 minValue=0, maxValue=63)

                if slot >= 0 and ok:
                    self.ui.statusbar.showMessage("Patch be movin",
                                                  timeout=5000)
                    # Got a slot and the user hit "OK"
                    try:
                        util.export_patch_bin(self.sender().objectName(),
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
                                util.export_patch_bin(
                                    self.sender().objectName(),
                                    os.path.join(self.sd_card_root, "to_zoia"),
                                    slot, True)
                                self.ui.statusbar.showMessage(
                                    "Export complete!", timeout=5000)
                            except FileNotFoundError:
                                idx = str(self.sender().objectName()) + "_v1"
                                util.export_patch_bin(idx, os.path.join(
                                    self.sd_card_root, "to_zoia"), slot, True)
                                self.ui.statusbar.showMessage(
                                    "Export complete!", timeout=5000)
                            break
                        else:
                            continue
                    except FileNotFoundError:
                        idx = str(self.sender().objectName()) + "_v1"
                        util.export_patch_bin(idx,
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

        # msg = QMessageBox()
        # msg.setWindowTitle("Delete")
        # msg.setIcon(QMessageBox.Information)
        # msg.setText("Are you sure you want to delete this patch?\n"
        #            "(This cannot be undone)")
        # msg.setStandardButtons(QMessageBox.Yes |
        #                       QMessageBox.No)
        # value = msg.exec_()
        # if value == QMessageBox.Yes:
        util.delete_patch(self.sender().objectName())
        self.get_local_patches()
        self.set_data(self.ui.searchbar_3.text() != "")
        self.search()
        self.set_data_local(self.ui.searchbar_4.text() != "")

    def remove_sd(self):
        """ Removes a patch that is stored on a user's SD card.
        Currently triggered via a button press.
        """
        index = self.sender().objectName()
        if len(index) < 2:
            # one digit
            index = "00{}".format(index)
        else:
            # two digits
            index = "0{}".format(index)
        for pch in os.listdir(self.sd_card_path):
            if pch[:3] == index:
                os.remove(os.path.join(self.sd_card_path, pch))
                self.set_data_sd()
                break

    def display_patch_info(self):
        """ Queries the PS API for additional patch information whenever
        a patch is selected in the PS table or local table. Information
        is displayed via HTML.
        Currently triggered via a radio button selection.
        """

        if self.sender().isChecked():
            temp = None
            if self.ui.left_widget.currentIndex() == 0:
                temp = self.ui.text_browser
                self.selected = str(self.sender().objectName())
                content = ps.get_patch_meta(self.sender().objectName())
            elif self.ui.left_widget.currentIndex() == 1:
                temp = self.ui.text_browser_2
                self.ui.update_patch_notes.setEnabled(True)
                self.local_selected = str(self.sender().objectName())
                try:
                    with open(os.path.join(backend_path,
                                           str(self.sender().objectName()),
                                           str(self.sender().objectName())
                                           + ".json")) as f:
                        content = json.loads(f.read())
                except FileNotFoundError:
                    with open(os.path.join(backend_path,
                                           str(self.sender().objectName()),
                                           str(self.sender().objectName())
                                           + "_v1.json")) as f:
                        content = json.loads(f.read())
            if content["preview_url"] == "":
                content["preview_url"] = "None provided"
            else:
                content["preview_url"] = "<a href=" + content["preview_url"] \
                                         + ">Click here</a>"
            if "license" not in content or content["license"] is None or \
                    content["license"]["name"] == "":
                license = "None provided"
            else:
                license = content["license"]["name"]
            content["content"] = content["content"].replace("\n", "<br/>")

            temp.setHtml("<html><h3>"
                         + content["title"] + "</h3><u>Author:</u> "
                         + content["author"]["name"] + "<br/><u>Likes:</u> "
                         + str(content["like_count"])
                         + "<br/><u>Downloads:</u> "
                         + str(content["download_count"])
                         + "<br/><u>Views:</u> "
                         + str(content["view_count"]) + "<br/><u>License:</u> "
                         + license + "<br/><u>Preview:</u> "
                         + content["preview_url"]
                         + "<br/><br/><u>Patch Notes:</u><br/>"
                         + content["content"] + "</html>")

    def reload_ps(self):
        """ Reloads the PS table view to accurately reflect new uploads.
        Currently triggered via a menu action.

        # TODO Fix this, shouldn't just query the whole thing again.
        """

        # Get the new patch metadata that we don't have (if any).
        self.data = ps.get_all_patch_data_init()
        with open(os.path.join(backend_path, "data.json"), "w") as f:
            f.write(json.dumps(self.data))
        self.ui.searchbar_3.setText("")
        self.set_data(False)
        self.sort()

    def sd_path(self):
        """ Allows the user to specify the path to their SD card via
        their OS file explorer dialog. Note, nothing is done to ensure
        that the location selected is actually an SD card.
        Currently triggered via a menu action.
        """

        input_dir = QFileDialog.getExistingDirectory(None, 'Select an SD Card:',
                                                     expanduser("~"))
        if input_dir is not "" and os.path.isdir(input_dir):
            if "/" in input_dir:
                input_dir = input_dir.split("/")[0]
            self.sd_card_root = str(input_dir)
            self.ui.tab_sd.setEnabled(True)

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

        if self.ui.left_widget.currentIndex() == 0:
            if self.ui.searchbar_3.text() == "":
                self.set_data(False)
            else:
                self.search_data = \
                    util.search_patches(self.data, self.ui.searchbar_3.text())
                self.set_data(True)
        else:
            if self.ui.searchbar_4.text() == "":
                self.set_data_local(False)
            else:
                self.search_local_data = \
                    util.search_patches(self.local_data,
                                        self.ui.searchbar_4.text())
                self.set_data_local(True)

    def sort(self):
        """ Sorts the metadata in a table depending on the option
        selection via the menu.
        Currently triggered via a menu action.

        TODO Use the QTableWidget sort method for improved speed
         (requires an override to know how the sort pulls data).
        """

        # Determine how to sort the data.
        if self.sender() is None:
            curr_sort = (6, True)
        else:
            curr_sort = {
                "actionSort_by_title_A_Z": (1, False),
                "actionSort_by_title_Z_A": (1, True),
                "actionSort_by_date_new_old": (6, True),
                "actionReload_PatchStorage_patch_list": (6, True),
                "actionSort_by_date_old_new": (6, False),
                "actionSort_by_likes_high_low": (3, True),
                "actionSort_by_likes_low_high": (3, False),
                "actionSort_by_views_high_low": (5, True),
                "actionSort_by_views_low_high": (5, False),
                "actionSort_by_downloads_high_low": (4, True),
                "actionSort_by_downloads_low_high": (4, False)
            }[self.sender().objectName()]

        # Determine the context in which to perform the sort.
        if self.ui.searchbar_3.text() == "" \
                and self.ui.left_widget.currentIndex() == 0:
            util.sort_metadata(curr_sort[0], self.data, curr_sort[1])
            self.set_data(False)
        elif self.ui.left_widget.currentIndex() == 0:
            util.sort_metadata(curr_sort[0], self.search_data, curr_sort[1])
            self.set_data(True)
        elif self.ui.searchbar_4.text() == "" \
                and self.ui.left_widget.currentIndex() == 1:
            util.sort_metadata(curr_sort[0], self.local_data, curr_sort[1])
            self.set_data_local(False)
        else:
            util.sort_metadata(curr_sort[0], self.search_local_data,
                               curr_sort[1])
            self.set_data_local(True)

    def update(self):
        """ Attempts to update any patch that is stored in the user's
        backend directory.

        TODO Test if this functions correctly.
        """

        self.ui.statusbar.showMessage("Checking for updates...",
                                      timeout=5000)
        count = util.check_for_updates()
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
            msg.setText("Successfully updated " + str(count) + " patches.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def row_invert(self):
        """ Either enables of disables alternating row colours for
        tables; depending on the previous state of the tables.
        Currently triggered via a menu action.
        """
        self.ui.table.setAlternatingRowColors(
            not self.ui.table.alternatingRowColors())
        self.ui.table_2.setAlternatingRowColors(
            not self.ui.table_2.alternatingRowColors())
        self.ui.table_3.setAlternatingRowColors(
            not self.ui.table_3.alternatingRowColors())
        self.ui.table_4.setAlternatingRowColors(
            not self.ui.table_4.alternatingRowColors())

    def update_patch_notes(self):
        """ Updates the patch notes for a patch that has been previously
        locally saved to a user's machine.
        Currently triggered via a button click.
        """
        text = self.ui.text_browser_2.toPlainText()
        try:
            text = text.split("Patch Notes:")[1]
            util.modify_data(self.local_selected, text, 3)
        except IndexError:
            util.modify_data(self.local_selected, "", 3)
        self.ui.statusbar.showMessage("Successfully updated patch notes.",
                                      timeout=5000)

    def import_patch(self):
        """ Attempts to import patches into the librarian.
        Currently triggered via a menu action.

        TODO Add the ability to import and entire directory of patches.
        """
        for sd_pch in os.listdir(self.sd_card_path):
            index = int(self.sender().objectName())
            if index < 10:
                index = "00{}".format(index)
            else:
                index = "0{}".format(index)
            if index == sd_pch[:3]:
                try:
                    util.import_to_backend(os.path.join(self.sd_card_path,
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
            util.import_to_backend(pch)
            if self.ui.left_widget.currentIndex() == 1:
                self.get_local_patches()
                self.set_data_local(self.ui.searchbar_4.text() != "")
            self.ui.statusbar.showMessage("Import complete!")
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
        for pch in os.listdir(self.sd_card_path):
            if pch[0] == "0" and pch.split(".")[1] == "bin" \
                    and "_zoia_" in pch:
                # At this point we have done everything to ensure it's a ZOIA
                # patch, save for binary analysis.
                try:
                    util.import_to_backend(os.path.join(self.sd_card_path,
                                                        pch))
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
            msg.setInformativeText("{} were already saved in the library "
                                   "and were not imported.".format(fail_cnt))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def move_patch_sd(self, src, dest):
        """ Attempts to move a patch from one SD card slot to another
        Currently triggered via a QTableWidget move event.

        src: The index the item originated from.
        dest: The index the item is being moved to.
        """

        self.ui.table_3.clearSelection()
        self.ui.table_4.clearSelection()

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
        print(src)
        print(dest)
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
                            self.ui.table_4.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                        else:
                            self.ui.table_3.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                return

        # We are doing a move.

        os.rename(os.path.join(self.sd_card_path, src_pch),
                  os.path.join(self.sd_card_path, dest + src_pch[3:]))

        dest = int(dest)
        for i in range(64):
            if i == dest:
                if i > 31:
                    self.ui.table_4.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)
                else:
                    self.ui.table_3.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)

        self.set_data_sd()

    def toggle_darkmode(self):
        """ Toggles dark mode for the application.
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
        """

        # SD card tab swap/move
        if o.objectName() == "table_3" or o.objectName() == "table_4":
            if e.type() == QEvent.ChildAdded:
                self.ui.table_3.hideColumn(1)
                self.ui.table_3.hideColumn(2)
                self.ui.table_4.hideColumn(1)
                self.ui.table_4.hideColumn(2)

            elif e.type() == QEvent.ChildRemoved:
                # We have dropped an item, so now we need to rename it
                # or swap it with the item that was previously in that
                # slot.
                self.ui.table_3.showColumn(1)
                self.ui.table_3.showColumn(2)
                self.ui.table_4.showColumn(1)
                self.ui.table_4.showColumn(2)

                dst_index = None

                if o.objectName() == "table_3":
                    source_index = self.ui.table_3.currentRow()
                else:
                    source_index = self.ui.table_4.currentRow() + 32

                if (self.ui.table_3.item(source_index, 0) is not None and
                    self.ui.table_3.item(source_index, 0).text() == "") or \
                    (self.ui.table_4.item(source_index - 32, 0) is not None and
                     self.ui.table_4.item(source_index - 32, 0).text() == ""):
                    # Then it is actually the destination
                    dst_index = source_index
                    # Find the item that just got "deleted"
                    for i in range(64):
                        if i < 32:
                            temp = self.ui.table_3.item(i, 0)
                        else:
                            temp = self.ui.table_4.item(i - 32, 0)
                        if temp.text() == "" and \
                                ("0{}_zoia_".format(i) in j for j in
                                 os.listdir(str(self.sd_card_path))
                                 or "00{}_zoia_".format(i) in j for j in
                                 os.listdir(str(self.sd_card_path))):
                            self.move_patch_sd(i, dst_index)
                            self.set_data_sd()
                            return True
                else:
                    for i in range(64):
                        if i < 32:
                            temp = self.ui.table_3.item(i, 0)
                        else:
                            temp = self.ui.table_4.item(i - 32, 0)
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
                        self.ui.table_3.removeRow(32)
                        self.ui.table_4.removeRow(32)
                        return False
                    self.move_patch_sd(source_index, dst_index)
                    return True
        elif o.objectName() == "searchbar_4" \
                or o.objectName() == "searchbar_3":
            if e.type() == QEvent.KeyRelease:
                self.search()
                return True
        elif o.objectName() == "table_2":
            if e.type() == QEvent.FocusIn:
                if self.prev_tag_cat is None:
                    self.get_local_patches()
                    self.set_data_local(self.ui.searchbar_4 == "")
                    return False
                else:
                    new_text = self.ui.table_2.item(self.prev_tag_cat[0],
                                                    self.prev_tag_cat[1]
                                                    ).text()
                    if new_text == self.prev_tag_cat[2] \
                            or self.ui.table_2.currentColumn() == 3:
                        self.get_local_patches()
                        self.set_data_local(self.ui.searchbar_4 == "")
                        return False
                    else:
                        self.update_tags_cats(new_text,
                                              self.prev_tag_cat[1] == 1,
                                              self.ui.table_2.cellWidget(
                                                  self.ui.table_2.currentRow(),
                                                  4)
                                              .objectName())
                        return True
            elif e.type() == QEvent.FocusOut:
                try:
                    if self.ui.table_2.currentColumn() != 3:
                        self.prev_tag_cat = (self.ui.table_2.currentRow(),
                                             self.ui.table_2.currentColumn(),
                                             self.ui.table_2.selectedItems()[0]
                                             .text())
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
                util.modify_data(idx, [], 1)
            else:
                util.modify_data(idx, [], 2)
        # Case 2 - Leftover text from when there are no tags/categories
        elif text == "No tags" or text == "No categories":
            pass
        # Case 3 - The text isn't empty and contains tags/categories
        else:
            # Tags/categories are separated by commas
            items = text.split(",")
            done = []
            for curr in items:
                if " and " in curr:
                    done.append({
                        "name": curr.split(" and ")[0]
                    })
                    curr = curr.split(" and ")[1]
                elif "and " in curr:
                    curr = curr.split("and ")[1]
                done.append({
                    "name": curr
                })
            if mode:
                util.modify_data(idx, done, 1)
            else:
                util.modify_data(idx, done, 2)
        self.get_local_patches()
        self.set_data_local(self.ui.searchbar_4 == "")

    def try_quit(self):
        """ Forces the application to close.
        Currently triggered via a menu action.
        """

        self.close()
