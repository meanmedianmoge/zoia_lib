import json
import os
import platform

from PySide2.QtWidgets import QTableWidgetItem, QPushButton, QFileDialog, \
    QMessageBox, QInputDialog, QTableWidgetSelectionRange


class ZOIALibrarianBank:
    """

    """

    def __init__(self, path, msg, f1):
        """

        """

        self.f1 = f1
        self.data_banks = []
        self.path = path
        self.msg = msg

    def set_data_bank(self, ui, data):
        """ Populates the bank export tables with data.
        """

        # Cleanup the tables
        for i in range(32):
            ui.table_bank_left.setItem(i, 0, QTableWidgetItem(None))
            ui.table_bank_left.setItem(i, 1, QTableWidgetItem(None))
            ui.table_bank_left.setCellWidget(i, 1, None)
            ui.table_bank_right.setItem(i, 0, QTableWidgetItem(None))
            ui.table_bank_right.setItem(i, 1, QTableWidgetItem(None))
            ui.table_bank_right.setCellWidget(i, 1, None)

        # PyQt tables make zero sense.
        ui.table_bank_left.clearContents()
        ui.table_bank_right.clearContents()

        for pch in data:
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
            rmv_button = QPushButton("Remove")
            rmv_button.setObjectName(str(temp["id"]))
            if ver is not None:
                rmv_button.setObjectName(str(temp["id"]) + "_" + ver)
            else:
                rmv_button.setObjectName(str(temp["id"]))
            rmv_button.clicked.connect(self.f1)
            if "_zoia_" in name and len(name.split("_", 1)[0]) == 3:
                name = name.split("_", 2)[2]
            elif len(name.split("_", 1)[0]) == 3:
                name = name.split("_", 1)[1]
            if slot < 10:
                name = "00{}_zoia_".format(slot) + name
            else:
                name = "0{}_zoia_".format(slot) + name
            if slot < 32:
                ui.table_bank_left.setItem(
                    slot, 0, QTableWidgetItem(name))
                ui.table_bank_left.setCellWidget(
                    slot, 1, rmv_button)
            else:
                ui.table_bank_right.setItem(
                    slot - 32, 0, QTableWidgetItem(name))
                ui.table_bank_right.setCellWidget(
                    slot - 32, 1, rmv_button)

    def load_bank(self):
        """ Loads a Bank file that was previously saved to the
        backend directory.
        Currently triggered via a button press.
        """

        bnk_file = QFileDialog.getOpenFileName(
            None, "Select A Patch Bank:", os.path.join(self.path,
                                                       "Banks"))[0]
        if bnk_file is not "":
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

        with open(os.path.join(self.path, "Banks", bnk_file),
                  "r") as f:
            self.data_banks = json.loads(f.read())

        # TODO Deal with the case where a file is not found.
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

        if found_item:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(self.icon)
            msg.setText("This will overwrite the current data in the "
                        "table.\nIs that okay?")
            msg.setInformativeText("If you haven't saved your changes they "
                                   "will be lost.")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            value = msg.exec_()
            if value != QMessageBox.Yes:
                return
        self.set_data_bank(self.ui, self.data_banks)
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
            with open(
                    os.path.join(self.backend_path, "Banks", "{}.json".format(
                        name)),
                    "w") as f:
                f.write(json.dumps(self.data_banks))
            self.ui.btn_load_bank.setEnabled(True)

    def export_bank(self, ui, msg, sd, export):
        """ Saves a Bank to the backend application directory.
        Currently triggered via a button press.
        """

        if sd.get_sd_root() is None:
            msg.setWindowTitle("No SD Path")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please specify your SD card path!")
            msg.setInformativeText("File -> Specify SD Card Location")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            fails = []
            # Ask for a name
            while True:
                name, ok = QInputDialog().getText(self, "Export Bank",
                                                  "Please enter a name for "
                                                  "the Bank:")
                if ok and name not in os.listdir(sd.get_sd_root()):
                    ui.statusbar.showMessage("Patches be movin'",
                                             timeout=1000)
                    self.get_bank_data()
                    fails = export.export_bank(self.data_banks,
                                               sd.get_sd_root(), name)
                    break
                elif ok and name in os.listdir(sd.get_sd_root()):
                    msg.setWindowTitle("Directory exists")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("A directory with that name already exists.")
                    msg.setInformativeText("Would you like to overwrite it?")
                    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    value = msg.exec_()
                    if value == QMessageBox.Yes:
                        ui.statusbar.showMessage("Patches be movin'",
                                                 timeout=1000)
                        self.get_bank_data()
                        fails = export.export_bank(
                            self.data_banks, sd.get_sd_root(), name, True)
                        break
                else:
                    break
            if len(fails) == 0:
                msg.setWindowTitle("Success!")
                msg.setIcon(QMessageBox.Information)
                msg.setText("The Bank has been successfully exported "
                            "to the root of your SD card.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            else:
                msg.setWindowTitle("Some export failures")
                msg.setIcon(QMessageBox.Information)
                if len(fails) == len(self.data_banks):
                    msg.setText("Failed to export any patches because"
                                "they have all been deleted from the "
                                "ZOIA Librarian.")
                else:
                    msg.setText("Successful exports: {}\n"
                                "Failed exports: {}\n"
                                "Failures occur when the Bank "
                                "contains a patch that has been "
                                "deleted from the ZOIA Librarian."
                                "".format(len(self.data_banks)) - len(fails),
                                len(fails))
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
                    msg.setDetailedText(temp.strip("\n"))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

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
        self.set_data_bank(self.ui, self.backend_path,
                           self.data_banks)

        for i in range(64):
            if i == dest:
                if i > 31:
                    self.ui.table_bank_right.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)
                else:
                    self.ui.table_bank_left.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)

        self.get_bank_data()

    def get_data_banks(self):
        """

        """

        return self.data_banks
