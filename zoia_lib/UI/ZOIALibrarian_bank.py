import json
import os
import platform

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import (
    QTableWidgetItem,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QTableWidgetSelectionRange,
    QMainWindow,
)


class ZOIALibrarianBank(QMainWindow):
    """The ZOIALibrarianBank class is responsible for most
    activities contained within the Folders tab of the application.
    """

    def __init__(self, ui, path, sd,  msg, util, window):
        """Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        path: A String representing the path to the backend application
              directory.
        sd: Helper class to access UI-related SD methods.
        msg: A template QMessageBox.
        util: Helper class to access multi drag/drop.
        window: A reference to the main UI window for icon consistency.
        """

        # Needed to make use of self.sender()
        super().__init__()

        self.ui = ui
        self.path = path
        self.sd = sd
        self.msg = msg
        self.util = util
        self.window = window

        self.data_banks = []
        self.rows_left = []
        self.rows_right = []

    def create_add_btn(self, btn, i, idx):
        """Creates an add button for patches on the Bank
        tab's Local Storage table.

        btn: A reference to the QRadioButton associated with the current
             table row.
        i: The current row the buttons are being created for.
        idx: The id number associated with this row.
        """

        # Prepare the button.
        if "[Multiple Versions]" in btn.text():
            mv_btn = QPushButton("Move patches \n to folder", self)
            mv_btn.setEnabled(True)
        else:
            mv_btn = QPushButton("Move patch \n to folder", self)

        mv_btn.setObjectName(idx)
        mv_btn.setFont(self.ui.table_bank_local.horizontalHeader().font())
        mv_btn.clicked.connect(self.click_to_add)
        # if idx in self.data_bank:
        #     add.setEnabled(False)
        #     add.setText("Already in bank")
        self.ui.table_bank_local.setCellWidget(i, 4, mv_btn)

    def _set_data_bank(self):
        """Populates the bank export tables with data."""

        # Cleanup the tables
        for i in range(32):
            self.ui.table_bank_left.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_bank_left.setCellWidget(i, 1, None)
            self.ui.table_bank_right.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_bank_right.setCellWidget(i, 1, None)

        # PyQt tables make zero sense, so this clear is needed as well.
        self.ui.table_bank_left.clearContents()
        self.ui.table_bank_right.clearContents()

        # Setup the entries in each bank table.
        for pch in self.data_banks:
            idx = pch["id"]
            slot = pch["slot"]
            ver = None

            # Check for a version extension.
            if "_" not in idx:
                try:
                    with open(
                        os.path.join(self.path, idx, "{}.json".format(idx)), "r"
                    ) as f:
                        temp = json.loads(f.read())
                except FileNotFoundError:
                    continue
            else:
                idx, ver = idx.split("_")
                try:
                    with open(
                        os.path.join(self.path, idx, "{}_{}.json".format(idx, ver)), "r"
                    ) as f:
                        temp = json.loads(f.read())
                except FileNotFoundError:
                    continue

            # Prep the remove button.
            name = temp["files"][0]["filename"]
            rmv_btn = QPushButton("X")
            idx = str(temp["id"])
            rmv_btn.setObjectName(idx)
            rmv_btn.setFont(self.ui.table_PS.horizontalHeader().font())
            if ver is not None:
                rmv_btn.setObjectName("{}_{}".format(idx, ver))
            else:
                rmv_btn.setObjectName(idx)
            rmv_btn.clicked.connect(self._remove_bank_item)

            # Drop the _zoia_ prefix or a ### prefix if needed.
            if "_zoia_" in name and len(name.split("_", 1)[0]) == 3:
                name = name.split("_", 2)[2]
            elif len(name.split("_", 1)[0]) == 3:
                try:
                    int(name.split("_", 1)[0])
                    name = name.split("_", 1)[1]
                except ValueError:
                    pass

            # Drop the zoia_ prefix some users have been using.
            if "zoia_" == name[:5]:
                name = name[5:]

            # Prepare the correct prefix depending on the slot.
            if slot < 10:
                name = "00{}_zoia_".format(slot) + name
            else:
                name = "0{}_zoia_".format(slot) + name

            # Determine the correct table for the bank item, depending
            # on the slot.
            if slot < 32:
                self.ui.table_bank_left.setItem(slot, 0, QTableWidgetItem(name))
                self.ui.table_bank_left.setCellWidget(slot, 1, rmv_btn)
            else:
                self.ui.table_bank_right.setItem(slot - 32, 0, QTableWidgetItem(name))
                self.ui.table_bank_right.setCellWidget(slot - 32, 1, rmv_btn)

    def clear_bank(self):
        """Clears the bank tables for a clean slate.
        Currently triggered via a button press.
        """

        # Cleanup the tables
        for i in range(32):
            self.ui.table_bank_left.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_bank_left.setCellWidget(i, 1, None)
            self.ui.table_bank_right.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_bank_right.setCellWidget(i, 1, None)

        # PyQt tables make zero sense, so this clear is needed as well.
        self.ui.table_bank_left.clearContents()
        self.ui.table_bank_right.clearContents()

        self.ui.btn_export_bank.setEnabled(False)
        self.ui.btn_save_bank.setEnabled(False)
        self.ui.btn_clear_bank.setEnabled(False)
        self._get_bank_data()
        self.ui.statusbar.showMessage("Folder cleared.", timeout=5000)

    def load_bank(self):
        """Loads a Bank file that was previously saved to the
        backend directory.
        Currently triggered via a button press.
        """

        # PySide2 file selectors are bad and occasionally wrong, so try
        # all of them to be safe.
        bnk_file = QFileDialog.getOpenFileName(
            None, "Select a Patch Folder:", os.path.join(self.path, "Folders")
        )[0]
        if bnk_file != "":
            if "/" in bnk_file and platform.system().lower() == "windows":
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

        # Open the saved bank JSON.
        with open(os.path.join(self.path, "Folders", bnk_file), "r") as f:
            self.data_banks = json.loads(f.read())
        self.ui.statusbar.showMessage("Loading folder.", timeout=5000)

        # Make sure the user understands that any items currently in the
        # tables will be deleted.
        if self._has_item():
            self.msg.setWindowTitle("Warning")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText(
                "Are you sure you want to overwrite " "the current data in the table?"
            )
            self.msg.setInformativeText(
                "If you haven't saved your changes they will be lost."
            )
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            value = self.msg.exec_()
            if value != QMessageBox.Yes:
                return
            self.msg.setInformativeText(None)

        # Keep track of patches that fail to load (because they have been
        # deleted from the backend by the user).
        fails = []
        for pch in self.data_banks:
            if "_" in pch["id"] and os.path.exists(
                os.path.join(self.path, pch["id"].split("_")[0])
            ):
                if (pch["id"] + ".bin") not in os.listdir(
                    os.path.join(self.path, pch["id"].split("_")[0])
                ):
                    fails.append(pch)
                    self.data_banks.remove(pch)
            elif pch["id"] not in os.listdir(self.path):
                fails.append(pch)
                self.data_banks.remove(pch)

        # Notify the user of the patches that failed to load. No way to know
        # which since we don't save that info in the bank JSONs.
        if len(fails) != 0:
            self.ui.statusbar.showMessage("Some patches failed to load.", timeout=5000)
            self.msg.setWindowTitle("Warning")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText(
                "One or more patches failed to load as they have "
                "been deleted from the ZOIA Librarian. Please "
                "reacquire them to have them load."
            )
            self.msg.setInformativeText(
                "Unfortunately, there is no way to retrieve which specific "
                "patches were deleted."
            )
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setInformativeText(None)

        # Prepare the bank tables.
        self._set_data_bank()
        self.ui.btn_export_bank.setEnabled(True)
        self.ui.btn_save_bank.setEnabled(True)
        self.ui.btn_clear_bank.setEnabled(True)

    def save_bank(self, window):
        """Saves a Bank to the backend application directory.
        Currently triggered via a button press.

        window: A reference to the main UI window for icon consistency.
        """

        # Ask for a name
        name, ok = QInputDialog().getText(
            window, "Save Folder", "Please enter a name for the Folder:"
        )
        if ok:
            self._get_bank_data()
            if "{}.json".format(name) in os.listdir(os.path.join(self.path, "Folders")):
                # There's already a bank with that name.
                self.msg.setWindowTitle("Folder Exists")
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.setText("A Folder with that name already exists.")
                self.msg.setInformativeText("Would you like to overwrite it?")
                self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                value = self.msg.exec_()
                if value == QMessageBox.No:
                    return
                self.msg.setInformativeText(None)

            # Save the bank
            with open(
                os.path.join(self.path, "Folders", "{}.json".format(name)), "w"
            ) as f:
                f.write(json.dumps(self.data_banks))

            # Let the user know when the saving is done.
            self.ui.statusbar.showMessage("Successfully saved the folder.", timeout=5000)
            # self.msg.setWindowTitle("Folder Saved")
            # self.msg.setIcon(QMessageBox.Information)
            # self.msg.setText("The Folder has been saved successfully.")
            # self.msg.setStandardButtons(QMessageBox.Ok)
            # self.msg.exec_()
            self.ui.btn_load_bank.setEnabled(True)

    def export_bank(self, sd, export, window):
        """Saves a Bank to the backend application directory.
        Currently triggered via a button press.

        sd: A path to a user's SD card.
        export: Helper class to access backend exporting methods.
        window: A reference to the main UI window for icon consistency.
        """

        if sd.get_sd_root() is None:
            self.msg.setWindowTitle("No SD Path")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please specify your SD card path.")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.sd.sd_path(False, self.ui.table_sd_left.width() * 2)
        else:
            fails = []
            # Ask for a name
            name, ok = QInputDialog.getText(
                window, "Export Folder", "Please enter a name for the Folder:"
            )
            if ok and name not in os.listdir(sd.get_sd_root()):
                # Export the bank.
                self.ui.statusbar.showMessage("Exporting patches.", timeout=5000)
                self._get_bank_data()
                fails = export.export_bank(self.data_banks, sd.get_sd_root(), name)
            elif ok and name in os.listdir(sd.get_sd_root()):
                # Already have that directory on the SD, need to check if they
                # want to overwrite it.
                self.msg.setWindowTitle("Folder exists")
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.setText("A Folder with that name already exists.")
                self.msg.setInformativeText("Would you like to overwrite it?")
                self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                value = self.msg.exec_()
                self.msg.setInformativeText(None)
                if value == QMessageBox.Yes:
                    self.ui.statusbar.showMessage("Exporting patches.", timeout=5000)
                    self._get_bank_data()
                    fails = export.export_bank(
                        self.data_banks, sd.get_sd_root(), name, True
                    )
                else:
                    return
            else:
                return

            if len(fails) == 0:
                # No failed exports, let the user know.
                self.ui.statusbar.showMessage("Export complete.", timeout=5000)
                # self.msg.setWindowTitle("Success")
                # self.msg.setIcon(QMessageBox.Information)
                # self.msg.setText(
                #     "The Folder has successfully been exported to the "
                #     "SD card directory: {}.".format(name)
                # )
                # self.msg.setStandardButtons(QMessageBox.Ok)
                # self.msg.exec_()
            else:
                # Some patches were deleted since they were added to the
                # bank tables, so they failed to export, let the user know.
                self.msg.setWindowTitle("Some export failures")
                self.msg.setIcon(QMessageBox.Information)
                if len(fails) == len(self.data_banks):
                    self.ui.statusbar.showMessage("Export failed.", timeout=5000)
                    self.msg.setText(
                        "Failed to export any patches because they have"
                        "all been deleted from the ZOIA Librarian."
                    )
                else:
                    self.ui.statusbar.showMessage("Export complete.", timeout=5000)
                    self.msg.setText(
                        "Patches have been exported to the SD card "
                        "directory: {}.".format(name)
                    )
                    self.msg.setInformativeText(
                        "Successful exports: {} \n"
                        "Failed exports: {}".format(
                            len(self.data_banks) - len(fails), len(fails)
                        )
                    )
                    temp = "List of patches that failed to export:\n"
                    for slot in fails:
                        if slot < 32:
                            temp += self.ui.table_bank_left.item(slot, 0).text() + "\n"
                        else:
                            temp += (
                                self.ui.table_bank_right.item(slot - 32, 0).text()
                                + "\n"
                            )
                    self.msg.setDetailedText(temp.strip("\n"))
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                self.msg.setDetailedText(None)
                self.msg.setInformativeText(None)

    def _get_bank_data(self):
        """Gets the data from the current bank tables."""

        self.data_banks = []
        # Check each row of both tables and add them to data_banks.
        for i in range(32):
            temp_left = self.ui.table_bank_left.cellWidget(i, 1)
            if temp_left is not None:
                self.data_banks.append({"slot": i, "id": temp_left.objectName()})
        for i in range(32):
            temp_right = self.ui.table_bank_right.cellWidget(i, 1)
            if temp_right is not None:
                self.data_banks.append({"slot": i + 32, "id": temp_right.objectName()})

    def _move_patch_bank(self, src, dest):
        """Attempts to move a patch from one bank slot to another
        Currently triggered via a QTableWidget move event.

        src: The index the item originated from.
        dest: The index the item is being moved to.
        """

        self.ui.table_bank_left.clearSelection()
        self.ui.table_bank_right.clearSelection()

        swap = False

        if dest > 63:
            dest -= 64

        # Setup the new item.
        try:
            if src < 32:
                idx = self.ui.table_bank_left.cellWidget(src, 1).objectName()
            else:
                idx = self.ui.table_bank_right.cellWidget(src - 32, 1).objectName()
        except AttributeError:
            # Got two empty rows, ignore them.
            return

        for pch in self.data_banks:
            if dest == pch["slot"]:
                # We are doing a swap.
                swap = True
                break
        if swap:
            # Get the other item.
            if dest < 32:
                idx_dest = self.ui.table_bank_left.cellWidget(dest, 1).objectName()
            else:
                idx_dest = self.ui.table_bank_right.cellWidget(
                    dest - 32, 1
                ).objectName()

            # Get the old values out.
            for pch in self.data_banks:
                if pch["slot"] == src or pch["slot"] == dest:
                    self.data_banks.remove(pch)

            # Add the new values in.
            self.data_banks.append({"slot": dest, "id": idx})
            self.data_banks.append({"slot": src, "id": idx_dest})
        else:
            # We are doing a move.
            self.data_banks.append({"slot": dest, "id": idx})

            # Remove the source copy of the patch.
            for pch in self.data_banks:
                if pch["slot"] == src:
                    self.data_banks.remove(pch)
                    break

        # Set the data.
        self._set_data_bank()

        for i in range(64):
            if i == dest:
                if i > 31:
                    self.ui.table_bank_right.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True
                    )
                else:
                    self.ui.table_bank_left.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True
                    )

        # Reload the data in the tables.
        self._get_bank_data()
        self.ui.btn_save_bank.setEnabled(len(self.data_banks) > 0)
        self.ui.btn_export_bank.setEnabled(len(self.data_banks) > 0)
        self.ui.btn_clear_bank.setEnabled(len(self.data_banks) > 0)

    def click_to_add(self):
        """Used when manually adding patches to the Bank table.
        Currently triggered by a button press.
        """

        # Get the patch(es) which we're moving over
        src = self.ui.table_bank_local.indexAt(self.sender().pos()).row()
        idx = self.ui.table_bank_local.cellWidget(src, 0).objectName()

        # Resort the bank list
        self._get_bank_data()

        # Find an open slot in the bank
        if self.data_banks:
            occupied = [False] * 64
            for pch in self.data_banks:
                occupied[pch["slot"]] = True
            try:
                drop_index = occupied.index(False)
            except ValueError:
                # Trying to move patches to a full bank
                slot, ok = QInputDialog().getInt(
                    self.window,
                    "Folder Full",
                    "Select a slot to overwrite. \n\n"
                    "Note that if you're moving a version history, \n"
                    "multiple patches will be overwritten.",
                    0,
                    minValue=0,
                    maxValue=63,
                )
                if ok:
                    drop_index = slot
                else:
                    self.ui.statusbar.showMessage("Patch move failed.", timeout=5000)
                    self.msg.setWindowTitle("Folder Full")
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.setText(
                        "No patches were moved. "
                        "Try dragging and dropping to a slot to overwrite."
                    )
                    self.msg.setStandardButtons(QMessageBox.Ok)
                    self.msg.exec_()
                    return
        else:
            drop_index = 0
            # Need to enable the buttons now that there is a
            # patch in the tables.
            self.data_banks = []
            self.ui.btn_save_bank.setEnabled(True)
            self.ui.btn_export_bank.setEnabled(True)
            self.ui.btn_clear_bank.setEnabled(True)

        if (
            "_" not in idx and len(os.listdir(os.path.join(self.path, idx))) == 2
        ) or "_" in idx:
            # Not working within a version directory.
            # Just a single patch
            self.data_banks.append({"slot": drop_index, "id": idx})

        else:
            # An entire version directory was selected.
            pch_num = int((len(os.listdir(os.path.join(self.path, idx))) / 2) - 1)
            if drop_index + pch_num > 63:
                self._set_data_bank()
                self.ui.statusbar.showMessage("Patch move failed.", timeout=5000)
                self.msg.setWindowTitle("No Space")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(
                    "The version history contains {} patches, "
                    "so it must be moved to slot {} or lower.".format(
                        pch_num + 1, 63 - pch_num
                    )
                )
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
            else:
                # Remove all of the patches that are in the way.
                if self.data_banks is None:
                    self.data_banks = []
                    self.ui.btn_save_bank.setEnabled(True)
                    self.ui.btn_export_bank.setEnabled(True)
                    self.ui.btn_clear_bank.setEnabled(True)
                else:
                    for pch in self.data_banks:
                        for i in range(drop_index, drop_index + pch_num):
                            if pch["slot"] == i:
                                self.data_banks.remove(pch)
                # Add all of the version patches
                for i in range(1, pch_num + 2):
                    self.data_banks.append(
                        {"slot": drop_index + i - 1, "id": "{}_v{}".format(idx, i)}
                    )

        self._set_data_bank()

    def events(self, o, e):
        """Handles events that relate to dragging and dropping entries
        to/from the tables that are populated to contain the patches
        in a selected directory.

        o: The object that initiated the event.
        e: The event that was initiated.
        """

        if o.objectName() == "table_bank_local":
            if e.type() == QEvent.ChildAdded:
                # Hide the columns the user can't drop patches into.
                self.ui.table_bank_left.hideColumn(1)
                self.ui.table_bank_right.hideColumn(1)
            elif e.type() == QEvent.ChildRemoved:
                # Once the item has been dropped we can show the columns again.
                self.ui.table_bank_left.showColumn(1)
                self.ui.table_bank_right.showColumn(1)

                # Get the current row that was dragged.
                selected_rows = self.ui.table_bank_local.selectionModel().selectedRows()

                drop_index = None
                for src in selected_rows:
                    src = src.row()
                    # src = self.ui.table_bank_local.currentRow()
                    # We need to find out where we dragged the item to.
                    if not drop_index:
                        for i in range(32):
                            if self.ui.table_bank_left.item(i, 1) is not None:
                                drop_index = i
                                break
                            if self.ui.table_bank_right.item(i, 1) is not None:
                                drop_index = i + 32
                                break

                    if drop_index is not None:
                        # We actually dragged it over.
                        idx = self.ui.table_bank_local.cellWidget(src, 0).objectName()
                        if (
                            "_" not in idx
                            and len(os.listdir(os.path.join(self.path, idx))) == 2
                        ) or "_" in idx:
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
                                self.ui.btn_clear_bank.setEnabled(True)

                            self.data_banks.append({"slot": drop_index, "id": idx})
                            drop_index += 1
                        else:
                            # An entire version directory was dragged over.
                            pch_num = int(
                                (len(os.listdir(os.path.join(self.path, idx))) / 2) - 1
                            )
                            if drop_index + pch_num > 63:
                                self._set_data_bank()
                                self.ui.statusbar.showMessage("Patch move failed.", timeout=5000)
                                self.msg.setWindowTitle("No Space")
                                self.msg.setIcon(QMessageBox.Information)
                                self.msg.setText(
                                    """
                                    The version history contains {} patches,
                                    so it must be dragged to slot {} or lower
                                """.format(
                                        pch_num + 1, 63 - pch_num
                                    )
                                )
                                self.msg.setStandardButtons(QMessageBox.Ok)
                                self.msg.exec_()
                            else:
                                # Remove all of the patches that are in the way.
                                if self.data_banks is None:
                                    self.data_banks = []
                                    self.ui.btn_save_bank.setEnabled(True)
                                    self.ui.btn_export_bank.setEnabled(True)
                                    self.ui.btn_clear_bank.setEnabled(True)
                                else:
                                    for pch in self.data_banks:
                                        for i in range(
                                            drop_index, drop_index + pch_num
                                        ):
                                            if pch["slot"] == i:
                                                self.data_banks.remove(pch)
                                # Add all of the version patches
                                for i in range(1, pch_num + 2):
                                    self.data_banks.append(
                                        {
                                            "slot": drop_index + i - 1,
                                            "id": "{}_v{}".format(idx, i),
                                        }
                                    )
                                drop_index += pch_num + 1
                        self._set_data_bank()
                    else:
                        # Delete phantom rows.
                        self.ui.table_bank_left.setRowCount(32)
                        self.ui.table_bank_right.setRowCount(32)
                    self._get_bank_data()
                    self.ui.btn_save_bank.setEnabled(len(self.data_banks) > 0)
                    self.ui.btn_export_bank.setEnabled(len(self.data_banks) > 0)
                    self.ui.btn_clear_bank.setEnabled(len(self.data_banks) > 0)
        else:
            if e.type() == QEvent.FocusAboutToChange:
                if o.objectName() == "table_bank_left":
                    self.ui.table_bank_left.clearSelection()
                else:
                    self.ui.table_bank_right.clearSelection()
            elif e.type() == QEvent.ChildAdded:
                self.ui.table_bank_left.hideColumn(1)
                self.ui.table_bank_right.hideColumn(1)

                # Figure out which rows are selected.
                indexes = self.ui.table_bank_left.selectionModel().selectedRows()
                for index in sorted(indexes):
                    self.rows_left.append(index)

                indexes = self.ui.table_bank_right.selectionModel().selectedRows()
                for index in sorted(indexes):
                    self.rows_right.append(index)
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

                if (len(self.rows_left) <= 1 and len(self.rows_right) == 0) or (
                    len(self.rows_right) <= 1 and len(self.rows_left) == 0
                ):
                    # Single selection.
                    self.rows_left = []
                    self.rows_right = []
                    if (
                        src_index < 32 and self.ui.table_bank_left.item(src_index, 0)
                    ) is None or (
                        src_index > 31
                        and self.ui.table_bank_right.item(src_index - 32, 0) is None
                    ):
                        # Then it is actually the destination
                        dst_index = src_index
                        # Find the item that just got "deleted"
                        for i in range(64):
                            if i < 32:
                                temp = self.ui.table_bank_left.item(i, 0)
                                temp2 = self.ui.table_bank_left.cellWidget(i, 1)
                            else:
                                temp = self.ui.table_bank_right.item(i - 32, 0)
                                temp2 = self.ui.table_bank_right.cellWidget(i - 32, 1)
                            if temp is None and temp2 is not None:
                                self._move_patch_bank(i, dst_index)
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
                            self.ui.table_bank_left.setRowCount(32)
                            self.ui.table_bank_right.setRowCount(32)
                            return
                        if src_index != dst_index:
                            self._move_patch_bank(src_index, dst_index)
                        return
                else:
                    # Multiple selections, see util since logic is the same
                    # for bank and sd tables (single selection uses different
                    # logic).
                    self.util.multi_drag_drop(
                        self.rows_left,
                        self.rows_right,
                        self.ui.table_bank_left,
                        self.ui.table_bank_right,
                        self._move_patch_bank,
                    )
                    self.rows_left = []
                    self.rows_right = []

    def _remove_bank_item(self):
        """Removes an item from one of the bank tables.
        Currently triggered via a button press.
        """

        # Figure out which table the item is located in.
        # Known bug, this will always delete the first entry of an item
        # if multiple exist. Correcting this breaks the tables on macOS,
        # so best just to leave it alone for now.
        self.ui.statusbar.showMessage("Patch removed from Folder.", timeout=5000)
        for i in range(32):
            item_left = self.ui.table_bank_left.cellWidget(i, 1)
            item_right = self.ui.table_bank_right.cellWidget(i, 1)
            if (
                item_left is not None
                and item_left.objectName() == self.sender().objectName()
            ):
                curr_table = self.ui.table_bank_left
                break
            elif (
                item_right is not None
                and item_right.objectName() == self.sender().objectName()
            ):
                curr_table = self.ui.table_bank_right
                break

        # Clear the item and determine if buttons need to be disabled.
        curr_table.setItem(i, 0, QTableWidgetItem(None))
        curr_table.setCellWidget(i, 1, None)
        curr_table.clearSelection()

        # Reload the tables.
        item = self._has_item()
        self.ui.btn_export_bank.setEnabled(item)
        self.ui.btn_save_bank.setEnabled(item)
        self.ui.btn_clear_bank.setEnabled(item)
        self._get_bank_data()

    def _has_item(self):
        """Determines whether the Bank tables contain an entry.

        return: True if the Bank tables contain an entry, False
                otherwise.
        """

        # Check to see if we should disable export and save buttons.
        for i in range(32):
            if (
                self.ui.table_bank_left.cellWidget(i, 1) is not None
                or self.ui.table_bank_right.cellWidget(i, 1) is not None
            ):
                return True
        return False
