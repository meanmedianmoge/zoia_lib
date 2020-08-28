import json
import os

from PySide2 import QtCore
from PySide2.QtCore import QEvent, QThread
from PySide2.QtWidgets import QMainWindow, QMessageBox, QInputDialog, \
    QPushButton

from zoia_lib.backend.patch_update import PatchUpdate
from zoia_lib.common import errors

update = PatchUpdate()


class ZOIALibrarianLocal(QMainWindow):
    """ The ZOIALibrarianLocal class is responsible for all
    activities contained within the Local Storage View tab of the
    application, along with some activities contained within the Banks
    tab. This added responsibility is due to the fact that the Banks
    tab displays local patches that users can then use to create banks.
    In order to minimize code duplication, the code was merged into
    this class.
    """

    def __init__(self, ui, path, sd, msg, window, expt, delete, f1):
        """ Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        path: A String representing the path to the backend application
              directory.
        sd: Helper class to access UI-related SD methods.
        msg: A template QMessageBox.
        window: A reference to the main UI window for icon consistency.
        expt: Helper class to access backend exporting methods.
        delete: Helper class to access backend deletion methods.
        f1: Reference to ZOIALibrarianMain's sort_and_set function.
        """

        # Needed to make use of self.sender()
        super().__init__()

        # Variable init.
        self.ui = ui
        self.path = path
        self.sd = sd
        self.msg = msg
        self.window = window
        self.export = expt
        self.delete = delete
        self.sort_and_set = f1

        self.data_local = []
        self.data_local_version = []
        self.data_bank = []
        self.data_bank_version = []
        self.curr_ver = None
        self.prev_tag_cat = None
        self.prev_search = ""
        self.local_selected = None
        self.curr_page_viz = 0
        self.curr_viz = None

        # Thread
        self.worker_updates = UpdatesWorker()
        self.worker_updates.signal.connect(self.update_local_patches_done)

        # Disable the viz buttons
        self.ui.btn_next_page.setEnabled(False)
        self.ui.btn_prev_page.setEnabled(False)
        self.viz_disable()

    def create_expt_and_del_btns(self, btn, i, idx, ver):
        """ Creates the export and delete buttons that are displayed on
        the Local Storage View tab's QTableView. Each button is mapped
        to a respective function. Namely, initiate_export() and
        initiate_delete().

        btn: A reference to the QRadioButton associated with the current
             table row.
        i: The current row the buttons are being created for.
        idx: The id number associated with this row.
        ver: The version associated with this row (if it exists).
        """

        # Only enable exporting if there is a single version on the main page.
        if "[Multiple Versions]" in btn.text():
            ext_btn = QPushButton("See Version\nHistory to\nexport!", self)
            ext_btn.setEnabled(False)
        else:
            ext_btn = QPushButton("Click me\nto export!", self)

        del_btn = QPushButton("X", self)

        # We are in a version history view, so the buttons need the version
        # suffix.
        if self.ui.back_btn_local.isEnabled():
            name = "{}_v{}".format(idx, ver)
            ext_btn.setObjectName(name)
            del_btn.setObjectName(name)
        else:
            ext_btn.setObjectName(idx)
            del_btn.setObjectName(idx)

        # Connect the buttons and put them in the table.
        ext_btn.setFont(self.ui.table_PS.horizontalHeader().font())
        ext_btn.clicked.connect(self.initiate_export)
        self.ui.table_local.setCellWidget(i, 4, ext_btn)

        del_btn.setFont(self.ui.table_PS.horizontalHeader().font())
        del_btn.clicked.connect(self.initiate_delete)
        self.ui.table_local.setCellWidget(i, 5, del_btn)

    def get_local_patches(self):
        """ Retrieves the metadata for patches that a user has previously
        downloaded and saved to their machine's backend.
        """

        # Get the context.
        if self.ui.tabs.currentIndex() == 1:
            self.data_local = []
            curr_data = self.data_local
        else:
            self.data_bank = []
            curr_data = self.data_bank

        for patches in os.listdir(self.path):
            # Look for patch directories in the backend.
            if patches != "Banks" and patches != "data.json" and \
                    patches != '.DS_Store' and patches != "pref.json":
                for pch in os.listdir(os.path.join(self.path, patches)):
                    # Read the metadata so that we can set up the tables.
                    if pch.split(".")[-1] == "json":
                        with open(os.path.join(self.path, patches, pch)) as f:
                            temp = json.loads(f.read())
                        curr_data.append(temp)
                        break
        self.sort_and_set()

    def initiate_delete(self):
        """ Attempts to delete a patch that is stored on a user's local
        filesystem.
        """

        # Check to see if we are deleting in a version directory or not.
        if "_" not in self.sender().objectName():
            if not self.ui.back_btn_local.isEnabled() and \
                    len(os.listdir(os.path.join(
                        self.path, self.sender().objectName()))) > 2:
                self.delete.delete_full_patch_directory(
                    self.sender().objectName())
            else:
                self.delete.delete_patch(self.sender().objectName())
            self.get_local_patches()
        else:
            self.delete.delete_patch(
                os.path.join(self.curr_ver, self.sender().objectName()))
            self.get_version_patches(self.ui.tabs.currentIndex() == 1)

        # Reset the text browser.
        self.ui.text_browser_local.setText("")

        # Special case, we only have one patch in a version history after
        # a deletion.
        if self.ui.back_btn_local.isEnabled() \
                and self.ui.table_local.rowCount() == 1:
            self.get_local_patches()
            self.ui.back_btn_local.setEnabled(False)
            self.ui.searchbar_local.setText("")

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

        window: A reference to the main UI window for icon consistency.
        export: Helper class to access backend exporting methods.
        """

        # Exporting this way will only export to a directory named "to_zoia"
        # So we need to check if it exists. If it doesn't, we create it.
        if self.sd.get_sd_root() is None:
            # No SD path.
            self.msg.setWindowTitle("No SD Path")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please specify your SD card path!")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.sd.sd_path(False, self.window.width())
            self.msg.setInformativeText(None)
        else:
            if "to_zoia" not in os.listdir(self.sd.get_sd_root()):
                os.mkdir(os.path.join(self.sd.get_sd_root(), "to_zoia"))
            while True:
                # Ask for a slot
                slot, ok = QInputDialog().getInt(
                    self.window, "Patch Export", "Slot number:", minValue=0,
                    maxValue=63)
                if ok:
                    self.ui.statusbar.showMessage("Patch be movin",
                                                  timeout=5000)
                    # Got a slot and the user hit "OK"
                    try:
                        self.export.export_patch_bin(
                            self.sender().objectName(), os.path.join(
                                self.sd.get_sd_root(), "to_zoia"), slot)
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
                            self.export.export_patch_bin(
                                self.sender().objectName(),
                                os.path.join(self.sd.get_sd_root(),
                                             "to_zoia"), slot, True)
                            self.ui.statusbar.showMessage(
                                "Export complete!", timeout=5000)
                            break
                # Operation was aborted.
                break

    def get_version_patches(self, context, idx=None):
        """ Retrieves the versions of a patch that is locally stored to
        a user's backend local storage.

        context: True for the Local Storage View tab, False for the
                 Banks tab.
        idx: Optional. Used to specify which patch directory to access,
             Defaults to None. If it is None, the value stored in
             self.curr_ver is used in its place.
        """

        # Get the context.
        if idx is None:
            idx = self.curr_ver
        else:
            self.curr_ver = idx.split("_")[0]
        self.prev_tag_cat = None
        if context:
            self.data_local_version = []
            curr_data = self.data_local_version
        else:
            self.data_bank_version = []
            curr_data = self.data_bank_version

        # Get all of the patch versions into one place.
        for pch in os.listdir(os.path.join(self.path, idx)):
            if pch.split(".")[-1] == "json":
                # Got the metadata
                with open(os.path.join(self.path, idx, pch)) as f:
                    temp = json.loads(f.read())
                curr_data.append(temp)

        # Reload the table.
        self.ui.update_patch_notes.setEnabled(not context)
        self.sort_and_set()

    def update_local_patches_thread(self):
        """ Initializes a Worker thread to manage the updating of
        patches currently stored on a user's machine.
        Currently triggered via a button press.
        """

        # Disable the necessary buttons and start the thread.
        self.ui.check_for_updates_btn.setEnabled(False)
        self.ui.refresh_pch_btn.setEnabled(False)
        self.ui.btn_dwn_all.setEnabled(False)
        self.ui.statusbar.showMessage("Checking for updates...")
        self.worker_updates.start()

    def update_local_patches_done(self, count):
        """ Notifies the user once all local patches have been checked
        for updates. Will also notify the user of which patches were
        updated (should any actually update).

        count: An array, the first element contains the number of
               patches that updated, while the second element contains
               an array with the names of every patch that was updated.
        """

        # Check to see if we actually got an updates and let the user know.
        if count[0] == 0:
            self.msg.setWindowTitle("No Updates")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("All of the patches you have downloaded are "
                             "the latest version!")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
        else:
            self.msg.setWindowTitle("Updates")
            self.msg.setIcon(QMessageBox.Information)
            if count[0] == 1:
                self.msg.setText("Successfully updated 1 patch:")
                self.msg.setDetailedText("\t* {}".format(count[1][0]))
            else:
                self.msg.setText(
                    "Successfully updated {} patches:".format(count))
                text = ""
                for i in range(count[0]):
                    text += "\t* {}\n".format(count[1][i])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()

        # Re-enable the buttons now that the thread is done.
        self.ui.check_for_updates_btn.setEnabled(True)
        self.ui.refresh_pch_btn.setEnabled(True)
        self.ui.btn_dwn_all.setEnabled(True)

    def go_back(self):
        """ Returns to the default local patch screen.
        Currently triggered via a button press.
        """

        # Do the necessary cleanup depending on the context.
        if self.sender().objectName() == "back_btn_local":
            self.ui.searchbar_local.setText(self.prev_search)
            self.ui.text_browser_local.setText("")
            self.ui.page_label.setText("")
            self.ui.back_btn_local.setEnabled(False)
            self.ui.update_patch_notes.setEnabled(False)
            self.ui.btn_prev_page.setEnabled(False)
            self.ui.btn_next_page.setEnabled(False)
            self.viz_disable()
        elif self.sender().objectName() == "back_btn_bank":
            self.ui.searchbar_bank.setText(self.prev_search)
            self.ui.text_browser_bank.setText("")
            self.ui.back_btn_bank.setEnabled(False)
        # Sort and display the data.
        self.sort_and_set()

    def update_patch_notes(self):
        """ Updates the patch notes for a patch that has been previously
        locally saved to a user's machine.
        Currently triggered via a button click.
        """

        # Right now, we only update after Patch Notes:, ideally in the
        # future a user could update the author, title, etc.
        text = self.ui.text_browser_local.toPlainText()
        try:
            text = text.split("Patch Notes:")[1]
            update.update_data(self.local_selected, text.strip("\n"), 3)
        except IndexError:
            update.update_data(self.local_selected, "", 3)
        self.ui.statusbar.showMessage("Successfully updated patch notes.",
                                      timeout=5000)

    def update_tags_cats(self, text, mode, idx):
        """ Updates the tags or categories for a locally downloaded
        patch.

        text: The text used to discern tags and categories from.
        mode: True for tags update, False for categories update.
        idx: The id number associated with this row.
        """

        # Case 1 - The text is empty (i.e., delete everything)
        if text == "":
            update.update_data(idx, [], 1 if mode else 2)
            if not self.ui.back_btn_local.isEnabled():
                self.get_local_patches()
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
                    # They listed tags as "... and ..."
                    done.append({
                        "name": curr.split(" and ")[0]
                    })
                    curr = curr.split(" and ")[1]
                elif "and " in curr and curr[0:3] == "and":
                    curr = curr.split("and ")[1]
                done.append({
                    "name": curr
                })
            # Determine the context and update the metadata.
            if mode:
                update.update_data(idx, done, 1)
            else:
                update.update_data(idx, done, 2)

            # Reload the table to show the changes.
            if not self.ui.back_btn_local.isEnabled():
                self.get_local_patches()
            else:
                self.get_version_patches(True)
        self.prev_tag_cat = None

    def events(self, e):
        """ Handles events that relate updating the tags/categories
        for patches located in the Local Storage View tab's table.

        e: The event that was initiated.
        """

        if e.type() == QEvent.FocusIn:
            # We are updating a tag/category.
            if self.prev_tag_cat is None:
                return
            else:
                # Get the next text and if it differs, update the metadata.
                new_text = self.ui.table_local.item(
                    self.prev_tag_cat[0], self.prev_tag_cat[1]).text()
                if new_text == self.prev_tag_cat[2] \
                        or self.ui.table_local.currentColumn() == 3:
                    return
                else:
                    self.update_tags_cats(new_text, self.prev_tag_cat[1] == 1,
                                          self.ui.table_local.cellWidget(
                                              self.ui.table_local.currentRow(),
                                              4).objectName())
                    return
        elif e.type() == QEvent.FocusOut:
            try:
                # Figure out what the previous tag/cat was now that we are
                # no longer in edit mode.
                if self.ui.table_local.currentColumn() != 3:
                    self.prev_tag_cat = \
                        (self.ui.table_local.currentRow(),
                         self.ui.table_local.currentColumn(),
                         self.ui.table_local.selectedItems()[0].text())
                return
            except IndexError:
                return

    def setup_viz(self, viz):
        """ Prepares the patch visualizer once a patch has been
        selected.
        Currently triggered via a button press.

        viz: The parsed binary data that will be used in the visualizer.
        """

        self.ui.btn_next_page.setEnabled(True)
        self.ui.btn_prev_page.setEnabled(False)

        # Save the data for future method calls.
        self.curr_page_viz = 0
        self.curr_viz = viz

        self.ui.page_label.setText("<html><b>" + viz["name"] + "</b>  Page "
                                   + str(self.curr_page_viz) + "</html>")

        # Set the colors of the buttons
        self.set_viz()

    def viz_page(self):
        """ Either increases or decreases the current visualizer page,
        depending on which button was pressed.
        Currently triggered via a button press.
        """

        self.ui.text_browser_viz.setText("")

        # Decrease if prev, increase if next.
        if self.sender().objectName() == "btn_prev_page":
            self.curr_page_viz -= 1
        else:
            self.curr_page_viz += 1

        self.ui.btn_prev_page.setEnabled(not self.curr_page_viz == 0)

        # Load the viz for the new page.
        self.set_viz()

        # Update the page number.
        self.ui.page_label.setText("<html><b>" + self.curr_viz["name"]
                                   + "</b>  Page " + str(self.curr_page_viz)
                                   + "</html>")

    def viz_display(self):
        """ Displays additional information about a module that appears
        on the visualizer.
        Currently triggered via a button press.
        """

        btn_num = int(self.sender().objectName().split("_")[-1])
        for curr_module in self.curr_viz["modules"]:
            if curr_module["page"] == self.curr_page_viz and \
                    curr_module["position"] == btn_num:
                # Display the module info
                if curr_module["new_color"] == "":
                    color = curr_module["old_color"]
                else:
                    color = curr_module["new_color"]
                # Output the data for that module.
                self.ui.text_browser_viz.setText(
                    "<html><b><h2>" + curr_module["type"] + "</b></h2>"
                    + "<u>Color:</u> " + color + "<br/><u>"
                    + "Options 1:</u> " + str(curr_module["options_1"])
                    + "<br/><u>Options 2:</u> " + str(curr_module["options_2"])
                )

    def set_viz(self):
        """ Sets the visualizer for the current page of the patch.
        """

        # Reset the buttons.
        self.viz_disable()

        for curr_module in self.curr_viz["modules"]:
            # Setup the buttons for each module if we are on the correct page.
            if curr_module["page"] == self.curr_page_viz:
                curr_btn = self.get_btn(curr_module["position"])
                try:
                    color_hex = self._get_color_hex(curr_module["new_color"])
                except KeyError:
                    color_hex = self._get_color_hex(curr_module["old_color"])
                curr_btn.setStyleSheet("QPushButton{background-color:"
                                       + color_hex + ";"
                                       + "border: 1px solid #696969;}"
                                       + "QPushButton:hover{"
                                       + "border: 5px solid #000000;}")

                curr_btn.setEnabled(True)

    def viz_disable(self):
        """ Disables all internal visualizer buttons.
        """

        for i in range(40):
            curr_btn = self.get_btn(i)
            curr_btn.setEnabled(False)
            curr_btn.setStyleSheet("border: 1px solid #696969;"
                                   "background-color: gray;")

    @staticmethod
    def _get_color_hex(color):
        """ Lookup table to get the correct hex value for a given color.

        color: The color for which the hex value is being looked up.
        return: The correct hex value for the color as a string.
        """

        return {
            "Blue": "#0000FF",
            "Green": "#00FF00",
            "Red": "#FF0000",
            "Yellow": "#FFFF00",
            "Aqua": "#00FFFF",
            "Magenta": "#FF00FF",
            "White": "#FFFFFF",
            "Orange": "#FFA500",
            "Lima": "#BFFF00",
            "Surf": "#3627F6",
            "Sky": "#87CEEB",
            "Purple": "#A020F0",
            "Pink": "#FF007F",
            "Peach": "#FFE5B4",
            "Mango": "#FF8243"
        }[color]

    def get_btn(self, index):
        """ Lookup table to get the correct UI button for the visualizer

        index: The index that corresponds to the UI button.
        return:
        """

        return {
            0: self.ui.btn_0,
            1: self.ui.btn_1,
            2: self.ui.btn_2,
            3: self.ui.btn_3,
            4: self.ui.btn_4,
            5: self.ui.btn_5,
            6: self.ui.btn_6,
            7: self.ui.btn_7,
            8: self.ui.btn_8,
            9: self.ui.btn_9,
            10: self.ui.btn_10,
            11: self.ui.btn_11,
            12: self.ui.btn_12,
            13: self.ui.btn_13,
            14: self.ui.btn_14,
            15: self.ui.btn_15,
            16: self.ui.btn_16,
            17: self.ui.btn_17,
            18: self.ui.btn_18,
            19: self.ui.btn_19,
            20: self.ui.btn_20,
            21: self.ui.btn_21,
            22: self.ui.btn_22,
            23: self.ui.btn_23,
            24: self.ui.btn_24,
            25: self.ui.btn_25,
            26: self.ui.btn_26,
            27: self.ui.btn_27,
            28: self.ui.btn_28,
            29: self.ui.btn_29,
            30: self.ui.btn_30,
            31: self.ui.btn_31,
            32: self.ui.btn_32,
            33: self.ui.btn_33,
            34: self.ui.btn_34,
            35: self.ui.btn_35,
            36: self.ui.btn_36,
            37: self.ui.btn_37,
            38: self.ui.btn_38,
            39: self.ui.btn_39,
        }[index]

    def get_data_local(self):
        """ Gets the data for the patches in the Local Storage View tab
        table.
        """

        return self.data_local

    def get_data_local_version(self):
        """ Gets the version data for a patch in the Local Storage View
        tab table.
        """

        return self.data_local_version

    def get_data_bank(self):
        """ Gets the data for the patches in the Banks tab table.
        """

        return self.data_bank

    def get_data_bank_version(self):
        """ Gets the version data for a patch in the Banks tab table.
        """

        return self.data_bank_version

    def get_prev_tag_cat(self):
        """ Gets the previous tag/category text.
        Can be None if it has not been set.
        """

        return self.prev_tag_cat

    def set_prev_tag_cat(self, data):
        """ Sets the previous tag/category text.

        data: The previous tag/category text to be set.
        """

        self.prev_tag_cat = data

    def set_local_selected(self, data):
        """ Sets the previous locally selected item.

        data: The previous locally selected item to be set.
        """

        self.local_selected = data

    def set_prev_search(self, data):
        """ Sets the previous search term.

        data: The previous search term that will be set.
        """

        self.prev_search = data


class UpdatesWorker(QThread):
    """ The UpdatesWorker class runs as a separate thread in the
    application to prevent application snag. This thread will attempt
    to update every patches stored in the .ZoiaLibraryApp directory.
    """

    # UI communication
    signal = QtCore.Signal(list)

    def __init__(self):
        """ Initializes the thread.
        """

        QThread.__init__(self)

    def run(self):
        """ Attempts to update any patch that is stored in the user's
        backend directory.
        Currently triggered via a button press.
        """

        count = update.check_for_updates()
        self.signal.emit(count)
