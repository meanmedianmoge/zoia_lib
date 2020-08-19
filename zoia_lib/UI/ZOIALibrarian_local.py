import json
import os

from PySide2.QtCore import QEvent
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

    def __init__(self, ui, path, sd, msg, f1):
        """
        """

        super().__init__()

        self.ui = ui
        self.path = path
        self.sd = sd
        self.msg = msg
        self.sort_and_set = f1
        self.data_local = []
        self.data_local_version = []
        self.data_bank = []
        self.data_bank_version = []
        self.curr_ver = None
        self.prev_tag_cat = None
        self.prev_search = ""
        self.local_selected = None

    def initiate_export(self, window, export):
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
        if self.sd.get_sd_root() is None:
            # No SD path.
            self.msg.setWindowTitle("No SD Path")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please specify your SD card path!")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.sd.sd_path(False, window.width())
            self.msg.setInformativeText(None)
        else:
            if "to_zoia" not in os.listdir(self.sd.get_sd_root()):
                os.mkdir(os.path.join(self.sd.get_sd_root(), "to_zoia"))
            while True:
                # Ask for a slot
                slot, ok = QInputDialog().getInt(
                    window, "Patch Export", "Slot number:", minValue=0,
                    maxValue=63)
                if ok:
                    self.ui.statusbar.showMessage("Patch be movin",
                                                  timeout=5000)
                    # Got a slot and the user hit "OK"
                    try:
                        export.export_patch_bin(
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
                            export.export_patch_bin(
                                self.sender().objectName(),
                                os.path.join(self.sd.get_sd_root(),
                                             "to_zoia"), slot, True)
                            self.ui.statusbar.showMessage(
                                "Export complete!", timeout=5000)
                            break
                else:
                    # Operation was aborted.
                    break

    def create_expt_and_del_btns(self, btn, i, idx, ver, window, expt, delete):
        """

        btn:
        i:
        idx:
        ver:
        window:
        expt:
        delete:
        """

        if "[Multiple Versions]" in btn.text():
            expt = QPushButton("See Version\nHistory to\nexport!", self)
            expt.setEnabled(False)
        else:
            expt = QPushButton("Click me\nto export!", self)

        del_btn = QPushButton("X", self)

        if self.ui.back_btn_local.isEnabled():
            name = "{}_v{}".format(idx, ver)
            expt.setObjectName(name)
            del_btn.setObjectName(name)
        else:
            expt.setObjectName(idx)
            del_btn.setObjectName(idx)

        expt.setFont(self.ui.table_PS.horizontalHeader().font())
        expt.clicked.connect(lambda: self.initiate_export(expt, window))
        self.ui.table_local.setCellWidget(i, 4, expt)

        del_btn.setFont(self.ui.table_PS.horizontalHeader().font())
        del_btn.clicked.connect(lambda: self.initiate_delete(delete))
        self.ui.table_local.setCellWidget(i, 5, del_btn)

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

    def get_version_patches(self, context, idx=None):
        """ Retrieves the versions of a patch that is locally stored to
        a user's backend local storage.
        context: True for the Local Storage View tab, False for the
                 Banks tab.
        """

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

        self.ui.update_patch_notes.setEnabled(not context)
        self.sort_and_set()

    def update_local_patches(self):
        """ Attempts to update any patch that is stored in the user's
        backend directory.
        Currently triggered via a button press.
        """

        self.ui.statusbar.showMessage("Checking for updates...",
                                      timeout=5000)
        count = update.check_for_updates()
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

    def go_back(self):
        """ Returns to the default local patch screen.
        Currently triggered via a button press.
        """

        # Do the necessary cleanup depending on the context.
        if self.sender().objectName() == "back_btn_local":
            self.ui.searchbar_local.setText(self.prev_search)
            self.ui.text_browser_local.setText("")
            self.ui.text_browser_viz.setText("")
            self.ui.back_btn_local.setEnabled(False)
            self.ui.update_patch_notes.setEnabled(False)
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
            else:
                self.get_version_patches(True)

    def events(self, e):
        """
        """

        if e.type() == QEvent.FocusIn:
            if self.prev_tag_cat is None:
                return False
            else:
                new_text = self.ui.table_local.item(
                    self.prev_tag_cat[0], self.prev_tag_cat[1]).text()
                if new_text == self.prev_tag_cat[2] \
                        or self.ui.table_local.currentColumn() == 3:
                    return False
                else:
                    self.update_tags_cats(new_text, self.prev_tag_cat[1] == 1,
                                          self.ui.table_local.cellWidget(
                                              self.ui.table_local.currentRow(),
                                              4).objectName())
                    return True
        elif e.type() == QEvent.FocusOut:
            try:
                if self.ui.table_local.currentColumn() != 3:
                    self.prev_tag_cat = \
                        (self.ui.table_local.currentRow(),
                         self.ui.table_local.currentColumn(),
                         self.ui.table_local.selectedItems()[0].text())
                return True
            except IndexError:
                return False

    def get_data_local(self):
        """
        """

        return self.data_local

    def get_data_local_version(self):
        """
        """

        return self.data_local_version

    def get_data_bank(self):
        """
        """

        return self.data_bank

    def get_data_bank_version(self):
        """
        """

        return self.data_bank_version

    def get_prev_tag_cat(self):
        """
        """

        return self.prev_tag_cat

    def set_prev_tag_cat(self, data):
        """
        """

        self.prev_tag_cat = data

    def set_local_selected(self, data):
        """
        """

        self.local_selected = data

    def set_prev_search(self, data):
        """
        """

        self.prev_search = data
