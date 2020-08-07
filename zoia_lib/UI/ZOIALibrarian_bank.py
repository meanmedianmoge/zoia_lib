import json
import os
import platform

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QTableWidgetItem, QPushButton, QFileDialog, \
    QMessageBox, QInputDialog, QTableWidgetSelectionRange, QMainWindow


class ZOIALibrarianBank(QMainWindow):
    """ The ZOIALibrarianBank class is responsible for all
    activities contained within the Banks tab of the application.
    """

    def __init__(self, ui, path, msg):
        """ Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        path: A String representing the path to the backend application
              directory.
        msg: A template QMessageBox.
        """

        # Needed to make use of self.sender()
        super().__init__()

        self.ui = ui
        self.path = path
        self.msg = msg
        self.data_banks = []
        self.rows_left = []
        self.rows_right = []

    def set_data_bank(self):
        """ Populates the bank export tables with data.
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
                with open(os.path.join(self.path,
                                       idx, "{}.json".format(idx)), "r") as f:
                    temp = json.loads(f.read())
            else:
                idx, ver = idx.split("_")
                with open(os.path.join(self.path,
                                       idx, "{}_{}.json".format(idx, ver)),
                          "r") as f:
                    temp = json.loads(f.read())
            name = temp["files"][0]["filename"]
            rmv_btn = QPushButton("Remove")
            rmv_btn.setObjectName(str(temp["id"]))
            rmv_btn.setFont(self.ui.table_PS.horizontalHeader().font())
            if ver is not None:
                rmv_btn.setObjectName(str(temp["id"]) + "_" + ver)
            else:
                rmv_btn.setObjectName(str(temp["id"]))
            rmv_btn.clicked.connect(self.remove_bank_item)
            if "_zoia_" in name and len(name.split("_", 1)[0]) == 3:
                name = name.split("_", 2)[2]
            elif len(name.split("_", 1)[0]) == 3:
                try:
                    int(name.split("_", 1)[0])
                    name = name.split("_", 1)[1]
                except ValueError:
                    pass
            if "zoia_" == name[:5]:
                name = name[5:]
            if slot < 10:
                name = "00{}_zoia_".format(slot) + name
            else:
                name = "0{}_zoia_".format(slot) + name
            if slot < 32:
                self.ui.table_bank_left.setItem(
                    slot, 0, QTableWidgetItem(name))
                self.ui.table_bank_left.setCellWidget(
                    slot, 1, rmv_btn)
            else:
                self.ui.table_bank_right.setItem(
                    slot - 32, 0, QTableWidgetItem(name))
                self.ui.table_bank_right.setCellWidget(
                    slot - 32, 1, rmv_btn)

    def load_bank(self):
        """ Loads a Bank file that was previously saved to the
        backend directory.
        Currently triggered via a button press.
        """

        bnk_file = QFileDialog.getOpenFileName(
            None, "Select A Patch Bank:", os.path.join(self.path, "Banks"))[0]
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

        with open(os.path.join(self.path, "Banks", bnk_file), "r") as f:
            self.data_banks = json.loads(f.read())

        fails = []
        for pch in self.data_banks:
            if pch["id"] not in os.listdir(self.path):
                fails.append(pch)
                self.data_banks.remove(pch)

        if len(fails) != 0:
            self.msg.setWindowTitle("Warning")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText("One or more patches failed to load as they have "
                             "been deleted from the ZOIA Librarian. Please "
                             "reacquire them to have them load.")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()

        if self.has_item():
            self.msg.setWindowTitle("Warning")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText("This will overwrite the current data in the "
                             "table.\nIs that okay?")
            self.msg.setInformativeText(
                "If you haven't saved your changes they will be lost.")
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            value = self.msg.exec_()
            if value != QMessageBox.Yes:
                return
        self.set_data_bank()
        self.ui.btn_export_bank.setEnabled(True)
        self.ui.btn_save_bank.setEnabled(True)

    def save_bank(self):
        """ Saves a Bank to the backend application directory.
        Currently triggered via a button press.
        """

        # Ask for a name
        name, ok = QInputDialog().getText(
            self, "Save Bank", "Please enter a name for the Bank:")
        if ok:
            self.get_bank_data()
            if "{}.json".format(name) in \
                    os.listdir(os.path.join(self.path, "Banks")):
                self.msg.setWindowTitle("Bank exists")
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.setText(
                    "A Bank with that name already exists.")
                self.msg.setInformativeText(
                    "Would you like to overwrite it?")
                self.msg.setStandardButtons(
                    QMessageBox.Yes | QMessageBox.No)
                value = self.msg.exec_()
                if value == QMessageBox.No:
                    return
            with open(os.path.join(self.path, "Banks", "{}.json".format(name)),
                      "w") as f:
                f.write(json.dumps(self.data_banks))
            self.ui.btn_load_bank.setEnabled(True)

    def export_bank(self, sd, export):
        """ Saves a Bank to the backend application directory.
        Currently triggered via a button press.

        sd: A path to a user's SD card.
        """

        if sd.get_sd_root() is None:
            self.msg.setWindowTitle("No SD Path")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please specify your SD card path!")
            self.msg.setInformativeText("File -> Specify SD Card Location")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
        else:
            fails = []
            # Ask for a name
            while True:
                name, ok = QInputDialog().getText(
                    self, "Export Bank", "Please enter a name for the Bank:")
                if ok and name not in os.listdir(sd.get_sd_root()):
                    self.ui.statusbar.showMessage("Patches be movin'",
                                                  timeout=1000)
                    self.get_bank_data()
                    fails = export.export_bank(self.data_banks,
                                               sd.get_sd_root(), name)
                    break
                elif ok and name in os.listdir(sd.get_sd_root()):
                    self.msg.setWindowTitle("Directory exists")
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.setText(
                        "A directory with that name already exists.")
                    self.msg.setInformativeText(
                        "Would you like to overwrite it?")
                    self.msg.setStandardButtons(
                        QMessageBox.Yes | QMessageBox.No)
                    value = self.msg.exec_()
                    if value == QMessageBox.Yes:
                        self.ui.statusbar.showMessage("Patches be movin'",
                                                      timeout=1000)
                        self.get_bank_data()
                        fails = export.export_bank(
                            self.data_banks, sd.get_sd_root(), name, True)
                        break
                else:
                    break
            self.msg.setInformativeText("")
            if len(fails) == 0:
                self.msg.setWindowTitle("Success!")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("The Bank has been successfully exported "
                                 "to the root of your SD card.")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
            else:
                self.msg.setWindowTitle("Some export failures")
                self.msg.setIcon(QMessageBox.Information)
                if len(fails) == len(self.data_banks):
                    self.msg.setText("Failed to export any patches because"
                                     "they have all been deleted from the "
                                     "ZOIA Librarian.")
                else:
                    self.msg.setText("Successful exports: {}\nFailed exports: "
                                     "{}\nFailures occur when the Bank "
                                     "contains a patch that has been deleted "
                                     "from the ZOIA Librarian".format(
                        len(self.data_banks)) - len(fails), len(fails))
                    temp = "Here is a list of patches that failed to export:\n"
                    for slot in fails:
                        if slot < 32:
                            temp += \
                                self.ui.table_bank_left.item(slot, 0).text() \
                                + "\n"
                        else:
                            temp += \
                                self.ui.table_bank_right.item(
                                    slot - 32, 0).text() + "\n"
                    self.msg.setDetailedText(temp.strip("\n"))
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                self.msg.setDetailedText(None)

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

    def move_patch_bank(self, src, dest):
        """ Attempts to move a patch from one bank slot to another
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
        self.ui.btn_save_bank.setEnabled(len(self.data_banks) > 0)
        self.ui.btn_export_bank.setEnabled(len(self.data_banks) > 0)

    def events(self, o, e):
        """ Handles events that relate to dragging and dropping entries
        to/from the tables that are populated to contain the patches
        in a selected directory.

        o: The object that initiated the event.
        e: The event that was initiated.
        """

        if o.objectName() == "table_bank_local":
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
                            self.path, idx))) == 2) or "_" in idx:
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
                            self.path, idx))) / 2) - 1)
                        if drop_index + pch_num > 63:
                            self.set_data_bank()
                            self.msg.setWindowTitle("No Space")
                            self.msg.setIcon(QMessageBox.Information)
                            self.msg.setText(
                                "The version directory contain {} "
                                "patches, so it must be dragged to "
                                "slot {} or lower.".format(pch_num +
                                                           1, 63 -
                                                           pch_num))
                            self.msg.setStandardButtons(QMessageBox.Ok)
                            self.msg.exec_()
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
                else:
                    # Check for phantom rows to delete.
                    while self.ui.table_bank_left.rowCount() > 32 or \
                            self.ui.table_bank_right.rowCount() > 32:
                        self.ui.table_bank_left.removeRow(32)
                        self.ui.table_bank_right.removeRow(32)
                self.get_bank_data()
                self.ui.btn_save_bank.setEnabled(len(self.data_banks) > 0)
                self.ui.btn_export_bank.setEnabled(len(self.data_banks) > 0)
        else:
            if e.type() == QEvent.FocusAboutToChange:
                if o.objectName() == "table_bank_left":
                    self.ui.table_bank_left.clearSelection()
                else:
                    self.ui.table_bank_right.clearSelection()
            elif e.type() == QEvent.ChildAdded:
                # Figure out which rows are selected.
                indexes = \
                    self.ui.table_bank_left.selectionModel().selectedRows()
                for index in sorted(indexes):
                    self.rows_left.append(index)

                indexes = \
                    self.ui.table_bank_right.selectionModel().selectedRows()
                for index in sorted(indexes):
                    self.rows_right.append(index)

                self.ui.table_bank_left.hideColumn(1)
                self.ui.table_bank_right.hideColumn(1)

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

                if (len(self.rows_left) <= 1 and len(self.rows_right) == 0) \
                        or (len(self.rows_right) <= 1 and len(self.rows_left)
                            == 0):
                    # Single selection.
                    self.rows_left = []
                    self.rows_right = []
                    if (src_index < 32 and self.ui.table_bank_left.item(
                            src_index, 0)) is None \
                            or (
                            src_index > 31 and self.ui.table_bank_right.item(
                        src_index - 32, 0) is None):
                        # Then it is actually the destination
                        dst_index = src_index
                        # Find the item that just got "deleted"
                        for i in range(64):
                            if i < 32:
                                temp = self.ui.table_bank_left.item(i, 0)
                                temp2 = self.ui.table_bank_left.cellWidget(i,
                                                                           1)
                            else:
                                temp = self.ui.table_bank_right.item(i - 32, 0)
                                temp2 = self.ui.table_bank_right.cellWidget(
                                    i - 32, 1)
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
                else:
                    # Multiple selections
                    first_item = None
                    first_item_index = -1
                    if len(self.rows_left) > 1 and len(self.rows_right) == 0:
                        for i in sorted(self.rows_left):
                            i = i.row()
                            i = int('%d' % i)
                            temp = self.ui.table_bank_left.item(i, 0)
                            if temp is not None and temp.text() != "":
                                first_item = temp
                                first_item_index = i
                                break
                        first_item_text = first_item.text()
                        for i in range(64):
                            if i < 32:
                                temp_left = self.ui.table_bank_left.item(i, 0)
                                temp_right = None
                            else:
                                temp_right = self.ui.table_bank_right.item(
                                    i - 32, 0)
                                temp_left = None
                            if (temp_left is not None and i != first_item_index
                                and temp_left.text() == first_item_text) or (
                                    temp_right is not None and temp_right.text()
                                    == first_item_text):
                                # We found the first item!
                                row = sorted(self.rows_left)[-1].row()
                                row = int('%d' % row)
                                for j in range(first_item_index, row + 1):
                                    if j == first_item_index:
                                        i = i + (j - first_item_index)
                                    else:
                                        i += 1
                                    if i > 31:
                                        temp1 = self.ui.table_bank_left.item(j,
                                                                             0)
                                        temp2 = self.ui.table_bank_right.item(
                                            i - 32,
                                            0)
                                    else:
                                        temp1 = self.ui.table_bank_left.item(j,
                                                                             0)
                                        temp2 = self.ui.table_bank_left.item(i,
                                                                             0)
                                    if temp1 is None and temp2 is None:
                                        continue
                                    elif temp1 is None and temp2 is not None:
                                        self.move_patch_bank(i, j)
                                    elif temp1 is not None and temp2 is None or \
                                            temp1 is not None and temp2 is not \
                                            None:
                                        self.move_patch_bank(j, i)
                                    elif temp1 is None and temp2 is not None:
                                        self.move_patch_bank(i, j)
                    else:
                        for i in sorted(self.rows_right):
                            i = i.row()
                            i = int('%d' % i)
                            temp = self.ui.table_bank_right.item(i, 0)
                            if temp is not None and temp.text() != "":
                                first_item = temp
                                first_item_index = i + 32
                                break
                        first_item_text = first_item.text()
                        for i in range(64):
                            if i < 32:
                                temp_left = self.ui.table_bank_left.item(i, 0)
                                temp_right = None
                            else:
                                temp_right = self.ui.table_bank_right.item(
                                    i - 32, 0)
                                temp_left = None
                            if (temp_right is not None
                                and i != first_item_index and temp_right.text()
                                == first_item_text) or \
                                    (temp_left is not None and temp_left.text()
                                     == first_item_text):
                                # We found the first item!
                                row = sorted(self.rows_right)[-1].row()
                                row = int('%d' % row) + 32
                                for j in range(first_item_index, row + 1):
                                    if j == first_item_index:
                                        i = i + (j - first_item_index)
                                    else:
                                        i += 1
                                    if i > 31:
                                        temp1 = self.ui.table_bank_right.item(
                                            j - 32,
                                            0)
                                        temp2 = self.ui.table_bank_left.item(
                                            i - 32,
                                            0)
                                    else:
                                        temp1 = self.ui.table_bank_right.item(
                                            j - 32,
                                            0)
                                        temp2 = self.ui.table_bank_right.item(
                                            i,
                                            0)
                                    if temp1 is None and temp2 is None:
                                        continue
                                    elif temp1 is None and temp2 is not None:
                                        self.move_patch_bank(i, j)
                                    elif temp1 is not None and temp2 is None or \
                                            temp1 is not None and temp2 is not None:
                                        self.move_patch_bank(j, i)
                                    elif temp1 is None and temp2 is not None:
                                        self.move_patch_bank(i, j)
                    self.rows_left = []
                    self.rows_right = []
                    while self.ui.table_bank_left.rowCount() > 32:
                        self.ui.table_bank_left.removeRow(32)
                    while self.ui.table_bank_right.rowCount() > 32:
                        self.ui.table_bank_right.removeRow(32)

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
                    self.ui.table_bank_right.clearSelection()
                    break
            else:
                item = self.ui.table_bank_right.cellWidget(i - 32, 1)
                if item is None:
                    continue
                elif item.objectName() == self.sender().objectName():
                    self.ui.table_bank_right.setItem(i - 32, 0,
                                                     QTableWidgetItem(None))
                    self.ui.table_bank_right.setCellWidget(i - 32, 1, None)
                    self.ui.table_bank_right.clearSelection()
                    break

        for pch in self.data_banks:
            if pch["slot"] == i:
                self.data_banks.remove(pch)

        item = self.has_item()
        self.ui.btn_export_bank.setEnabled(item)
        self.ui.btn_save_bank.setEnabled(item)

    def has_item(self):
        """ Determines whether the Bank tables contain an entry.

        Return: True if the Bank tables contain an entry, False
                otherwise.
        """

        # Check to see if we should disable export and save buttons.
        item = False
        for i in range(64):
            if i < 32 and self.ui.table_bank_left.cellWidget(i, 1) is not None:
                item = True
                break
            elif self.ui.table_bank_right.cellWidget(i - 32, 1) is not None:
                item = True
                break
        return item
