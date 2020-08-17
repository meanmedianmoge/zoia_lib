import json
import os

from PySide2.QtWidgets import QMainWindow, QMessageBox, QInputDialog, \
    QPushButton

from zoia_lib.common import errors


class ZOIALibrarianLocal(QMainWindow):
    """
    """

    def __init__(self, ui, path, export, delete, window, sd, msg):
        """
        """

        super().__init__()

        self.ui = ui
        self.path = path
        self.export = export
        self.delete = delete
        self.window = window
        self.sd = sd
        self.msg = msg

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
                else:
                    # Operation was aborted.
                    break

    def create_expt_and_del_btns(self, btn, i, idx, ver, f1):
        """

        btn:
        i:
        idx:
        ver:
        f1:
        """

        if "[Multiple Versions]" in btn.text():
            expt = QPushButton("See Version\nHistory to\nexport!", self)
            expt.setEnabled(False)
        else:
            expt = QPushButton("Click me\nto export!", self)

        del_btn = QPushButton("X", self)

        if self.ui.back_btn_local.isEnabled():
            expt.setObjectName(idx + "_v" + ver)
            del_btn.setObjectName(idx + "_v" + ver)
        else:
            expt.setObjectName(idx)
            del_btn.setObjectName(idx)

        expt.setFont(self.ui.table_PS.horizontalHeader().font())
        expt.clicked.connect(self.initiate_export)
        self.ui.table_local.setCellWidget(i, 4, expt)

        del_btn.setFont(self.ui.table_PS.horizontalHeader().font())
        del_btn.clicked.connect(f1)
        self.ui.table_local.setCellWidget(i, 5, del_btn)

    def get_local_patches(self):
        """ Retrieves the metadata for patches that a user has previously
        downloaded and saved to their machine's backend.
        """

        curr_data = []
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
        return curr_data

