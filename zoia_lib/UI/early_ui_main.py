import json
import os
from os.path import expanduser

from PySide2.QtGui import *
from PySide2.QtWidgets import *

import zoia_lib.UI.early_ui as ui_main
import zoia_lib.backend.api as api
import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors

ps = api.PatchStorage()
backend_path = util.get_backend_path()

style_sheet = """
    QPushButton
    {
        background: white;
        border: none;
        font-size: 13px;
        color: black;
    }
    """


class EarlyUIMain(QMainWindow):
    """ ** TEMPORARY FUNCTIONALITY SHOWCASE **

    The ThrowawayUIMain class represents the frontend for the
    application. It allows users to interact with the various backend
    functions available. These include searching, download, sorting,
    and exporting patches.

    Any changes made to the .ui file will not be reflected unless the
    following command is run from the UI directory:
        pyside2-uic.exe .\early.ui -o .\early_ui.py

    Known issues:
     - Version history is not implemented in the frontend. As such,
       exporting a patch with multiple version will fail.
     - Tables do not scale correctly.
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
                # TODO Don't just get all of the data again, figure out a way
                #  to determine which patches have been deleted and just remove
                #  those.
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

        # Variable initialization.
        self.search_data = None
        self.sd_card_path = None
        self.local_data = None
        self.search_local_data = None

        # Setup the tables, but only populate the PS API table
        # (The local table will populate once the user switches tabs).
        self.ui.table.setRowCount(len(self.data))
        self.ui.table.setColumnCount(5)
        self.set_data(False)
        self.ui.table.resizeColumnsToContents()
        self.ui.table.resizeRowsToContents()

        self.ui.table_2.setRowCount(len(self.data))
        self.ui.table_2.setColumnCount(6)

        self.ui.table_3.setHorizontalHeaderLabels(["SD Card"])
        self.ui.tab_sd.setEnabled(False)

        # Connect buttons and items to methods.
        self.ui.left_widget.currentChanged.connect(self.get_local_patches)
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
        self.ui.search_button_3.clicked.connect(self.search)
        self.ui.search_button_4.clicked.connect(self.search)
        self.ui.searchbar_3.returnPressed.connect(self.search)
        self.ui.searchbar_4.returnPressed.connect(self.search)

        # Font consistency.
        self.ui.table.setFont(QFont('Verdana', 10))
        self.ui.table_2.setFont(QFont('Verdana', 10))
        self.ui.text_browser.setFont(QFont('Verdana', 16))
        self.ui.text_browser_2.setFont(QFont('Verdana', 16))

        # Ensure the application starts as maximized.
        self.setFocusPolicy(Qt.StrongFocus)
        self.showMaximized()

    def get_local_patches(self):
        """ Gets a list of local patch metadata from the backend
        directory.

        TODO Expand this to accurately deal with version history
         (array in the array).
        """

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
            if self.sd_card_path is None:
                msg = QMessageBox()
                msg.setWindowTitle("No SD Path")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Please specify your SD card path!")
                msg.setInformativeText("File -> Specify SD Card Location")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.ui.left_widget.setCurrentIndex(1)
            else:
                self.set_data_sd()

    def set_data_sd(self):
        """ Sets the data for the PS table. This is done when the tab is
        returned to.
        """

        self.ui.table_3.clear()
        for pch in os.listdir(self.sd_card_path):
            # Get the index
            index = pch.split("_")[0]
            if index[1] == "0":
                # one digit
                index = int(index[2])
            else:
                # two digits
                index = int(index[1:3])
            self.ui.table_3.setItem(index, 0, QTableWidgetItem(pch))
        self.ui.table_3.setHorizontalHeaderLabels(["SD Card"])

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

            for j in range(1, len(data[i]["tags"])):
                tags += data[i]["tags"][j]["name"] + ", "

            if (len(data[i]["tags"])) > 1:
                btn_tag = QPushButton(data[i]["tags"][0]["name"]
                                      + " and " + str(len(data[i]["tags"])
                                                      - 1) + " more", self)
            else:
                btn_tag = QPushButton(data[i]["tags"][0]["name"], self)
            QToolTip.setFont(QFont('Verdana', 10))
            btn_tag.setToolTip(tags[:len(tags) - 2])
            btn_tag.setStyleSheet(style_sheet)
            btn_tag.setFont(QFont('Verdana', 10))
            self.ui.table.setCellWidget(i, 1, btn_tag)

            cat = ""

            for k in range(1, len(data[i]["categories"])):
                cat += data[i]["categories"][k]["name"] + ", "

            if (len(data[i]["categories"])) > 1:
                btn_cat = QPushButton(data[i]["categories"][0]["name"]
                                      + " and "
                                      + str(len(data[i]["categories"])
                                            - 1) + " more", self)
            else:
                btn_cat = QPushButton(data[i]["categories"][0]["name"], self)
            QToolTip.setFont(QFont('Verdana', 10))
            btn_cat.setToolTip(cat[:len(cat) - 2])
            btn_cat.setFont(QFont('Verdana', 10))
            btn_cat.setStyleSheet(style_sheet)
            self.ui.table.setCellWidget(i, 2, btn_cat)
            date = QTableWidgetItem(data[i]["updated_at"][:10])
            date.setTextAlignment(Qt.AlignCenter)
            self.ui.table.setItem(i, 3, date)
            dwn = QPushButton(str(data[i]["id"]), self)
            dwn.setFont(QFont('Verdana', 10))
            dwn.clicked.connect(self.initiate_download)

            if (str(data[i]["id"])) in os.listdir(backend_path):
                dwn.setEnabled(False)
                dwn.setText("Downloaded!")

            self.ui.table.setCellWidget(i, 4, dwn)
        self.ui.table.setHorizontalHeaderLabels(hor_headers)

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

            for j in range(1, len(data[i]["tags"])):
                tags += data[i]["tags"][j]["name"] + ", "

            if (len(data[i]["tags"])) > 1:
                btn_tag = QPushButton(data[i]["tags"][0]["name"]
                                      + " and " + str(len(data[i]["tags"])
                                                      - 1) + " more", self)
            else:
                btn_tag = QPushButton(data[i]["tags"][0]["name"], self)
            QToolTip.setFont(QFont('Verdana', 10))
            btn_tag.setToolTip(tags[:len(tags) - 2])
            btn_tag.setStyleSheet(style_sheet)
            btn_tag.setFont(QFont('Verdana', 10))
            self.ui.table_2.setCellWidget(i, 1, btn_tag)

            cat = ""
            for k in range(1, len(data[i]["categories"])):
                cat += data[i]["categories"][k]["name"] + ", "

            if (len(data[i]["categories"])) > 1:
                btn_cat = QPushButton(data[i]["categories"][0]["name"]
                                      + " and "
                                      + str(len(data[i]["categories"])
                                            - 1) + " more", self)
            else:
                btn_cat = QPushButton(data[i]["categories"][0]["name"], self)

            QToolTip.setFont(QFont('Verdana', 10))
            btn_cat.setToolTip(cat[:len(cat) - 2])
            btn_cat.setFont(QFont('Verdana', 10))
            btn_cat.setStyleSheet(style_sheet)
            self.ui.table_2.setCellWidget(i, 2, btn_cat)
            date = QTableWidgetItem(data[i]["updated_at"][:10])
            date.setTextAlignment(Qt.AlignCenter)
            self.ui.table_2.setItem(i, 3, date)
            expt = QPushButton(str(data[i]["id"]), self)
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
                                      timeout=2000)

        # TODO Replace with FCFS thread scheduling
        util.save_to_backend(ps.download(str(self.sender().text())))
        self.sender().setEnabled(False)
        self.sender().setText("Downloaded!")
        self.ui.statusbar.showMessage("Download complete!", timeout=2000)

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

        if self.sd_card_path is None:
            # No SD path.
            msg = QMessageBox()
            msg.setWindowTitle("No SD Path")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please specify your SD card path!")
            msg.setInformativeText("File -> Specify SD Card Location")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            while True:
                # Ask for a slot
                slot, ok = QInputDialog().getInt(self, "Patch Export",
                                                 "Slot number:",
                                                 minValue=0, maxValue=63)

                if slot >= 0 and ok:
                    self.ui.statusbar.showMessage("Patch be movin",
                                                  timeout=2000)
                    # Got a slot and the user hit "OK"
                    try:
                        util.export_patch_bin(self.sender().text(),
                                              self.sd_card_path, slot)
                        self.ui.statusbar.showMessage("Export complete!",
                                                      timeout=2000)
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
                                util.export_patch_bin(self.sender().text(),
                                                      self.sd_card_path, slot,
                                                      True)
                            except FileNotFoundError:
                                idx = str(self.sender().text()) + "_v1"
                                util.export_patch_bin(idx,
                                                      self.sd_card_path, slot,
                                                      True)
                            break
                        else:
                            continue
                    except FileNotFoundError:
                        idx = str(self.sender().text()) + "_v1"
                        util.export_patch_bin(idx,
                                              self.sd_card_path, slot,
                                              True)
                        break
                else:
                    # Operation was aborted.
                    break

    def initiate_delete(self):
        """ Attempts to delete a patch that is stored on a user's local
        filesystem.
        """

        msg = QMessageBox()
        msg.setWindowTitle("Delete")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Are you sure you want to delete this patch?\n"
                    "(This cannot be undone)")
        msg.setStandardButtons(QMessageBox.Yes |
                               QMessageBox.No)
        value = msg.exec_()
        if value == QMessageBox.Yes:
            util.delete_patch(self.sender().objectName())
            self.get_local_patches()
            self.set_data(False)
            self.set_data_local(False)

    def display_patch_info(self):
        """ Queries the PS API for additional patch information whenever
        a patch is selected in the PS table or local table. Information
        is displayed via HTML, which means it may be possible to embed
        videos via the use of <iframe>. However, this functionality is
        absent in the current implementation.
        Currently triggered via a radio button selection.
        """

        if self.ui.left_widget.currentIndex() == 0:
            temp = self.ui.text_browser
        elif self.ui.left_widget.currentIndex() == 1:
            temp = self.ui.text_browser_2

        if self.sender().isChecked() and \
                self.ui.left_widget.currentIndex() == 0:
            content = ps.get_patch_meta(self.sender().objectName())
            if content["preview_url"] == "":
                content["preview_url"] = "None provided"
            content["content"] = content["content"].replace("\n", "<br/>")
            temp.setText("<html><h3>"
                         + content["title"] + "</h3><u>Author:</u> "
                         + content["author"]["name"] + "<br/><u>Likes:</u> "
                         + str(content["like_count"])
                         + "<br/><u>Downloads:</u> "
                         + str(content["download_count"])
                         + "<br/><u>Views:</u> "
                         + str(content["view_count"]) + "<br/><u>Preview:</u> "
                         + content["preview_url"]
                         + "<br/><br/><u>Patch Notes:</u><br/>"
                         + content["content"] + "</html>")
        elif self.sender().isChecked() and \
                self.ui.left_widget.currentIndex() == 1:
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
            # I hate duplicating code, but due to the nature of radio buttons,
            # this needs to be duplicated here otherwise an error will get
            # thrown for every non-selected radio button. Since this is
            # temporary anyway, I'm not too worried about it.
            content["content"] = content["content"].replace("\n", "<br/>")
            temp.setText("<html><h3>"
                         + content["title"] + "</h3><u>Author:</u> "
                         + content["author"]["name"] + "<br/><u>Likes:</u> "
                         + str(content["like_count"])
                         + "<br/><u>Downloads:</u> "
                         + str(content["download_count"])
                         + "<br/><u>Views:</u> "
                         + str(content["view_count"]) + "<br/><u>Preview:</u> "
                         + content["preview_url"]
                         + "<br/><br/><u>Patch Notes:</u><br/>"
                         + content["content"] + "</html>")

    def reload_ps(self):
        """ Reloads the PS table view to accurately reflect new uploads.
        Currently triggered via a menu action.
        """

        # Get the new patch metadata that we don't have (if any).
        try:
            new_patches = ps.get_newest_patches(len(self.data))
            self.data = new_patches + self.data
            with open(os.path.join(backend_path, "data.json"), "w") as f:
                f.write(json.dumps(self.data))
            self.ui.searchbar_3.setText("")
            self.set_data(False)
        except TypeError:
            msg = QMessageBox()
            msg.setWindowTitle("No New Patches")
            msg.setIcon(QMessageBox.Information)
            msg.setText("No new patches were found to be on PatchStorage.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def sd_path(self):
        """ Allows the user to specify the path to their SD card via
        their OS file explorer dialog. Note, nothing is done to ensure
        that the location selected is actually an SD card.
        Currently triggered via a menu action.
        """

        input_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:',
                                                     expanduser("~"))
        if input_dir is not "" and os.path.isdir(input_dir):
            self.sd_card_path = str(input_dir)
            self.ui.tab_sd.setEnabled(True)

    def search(self):
        """ Initiates a data search for the metadata that is retrieved
        via the PS API or that is stored locally. The search will then
        set the table to display the returned query matches.
        Currently triggered via a button press.
        """

        if self.sender().objectName() == "search_button_3" or \
                self.sender().objectName() == "searchbar_3":
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
         (requires an override to how the sort pulls data).
        """

        # Determine how to sort the data.
        curr_sort = {
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
                                      timeout=2000)
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

    def try_quit(self):
        """ Forces the application to close.
        Currently triggered via a menu action.
        """

        self.close()
