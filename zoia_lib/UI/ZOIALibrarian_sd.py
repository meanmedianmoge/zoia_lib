import os
import platform
from os.path import expanduser

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import (
    QTableWidgetItem,
    QPushButton,
    QFileDialog,
    QFileSystemModel,
    QMessageBox,
    QTableWidgetSelectionRange,
    QMainWindow,
)

from zoia_lib.common import errors


class ZOIALibrarianSD(QMainWindow):
    """The ZOIALibrarianSD class is responsible for all
    activities contained within the SD Card View tab of the application.
    """

    def __init__(self, ui, save, msg, delete, util):
        """Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        save: Helper class to access backend saving methods.
        msg: A template QMessageBox.
        delete: Helper class to access backend deletion methods.
        util: Helper class to access UI utility methods.
        """

        # Needed to make use of self.sender()
        super().__init__()

        # Variable init.
        self.ui = ui
        self.save = save
        self.msg = msg
        self.delete = delete
        self.util = util

        self.sd_path_full = None
        self.sd_root = None
        self.export_dir = None
        self.rows_left = []
        self.rows_right = []

    def sd_path(self, startup, width):
        """Allows the user to specify the path to their SD card via
        their OS file explorer dialog. Note, nothing is done to ensure
        that the location selected is actually an SD card.
        Currently triggered via a menu action.

        startup: True if this is being called during startup, False
                 otherwise.
        width: The width of the main window.
        """

        if not startup:
            input_dir = QFileDialog.getExistingDirectory(
                None, "Select an SD Card:", expanduser("~")
            )
            if input_dir != "" and os.path.isdir(input_dir):
                if "/" in input_dir and platform.system().lower() == "windows":
                    # THIS IS NEEDED FOR WINDOWS.
                    # This comes from a bug with QFileDialog returning the
                    # wrong path separator on Windows for some odd reason.
                    input_dir = input_dir.split("/")[0]
                elif "/" in input_dir:
                    # OSX case.
                    pass
                else:
                    input_dir = input_dir.split(os.path.sep)[0]
                self.sd_root = str(input_dir)
                self.export_dir = os.path.join(self.sd_root, "to_zoia")
                self.ui.tab_sd.setEnabled(True)
            else:
                self.ui.tab_sd.setEnabled(False)
                self.ui.tabs.setCurrentIndex(1)

        # Setup the SD card tree view for the SD Card tab.
        self.ui.statusbar.showMessage("SD card location successfully set.", timeout=5000)
        model = QFileSystemModel()
        model.setRootPath(self.sd_root)
        self.ui.sd_tree.setModel(model)
        self.ui.sd_tree.setRootIndex(model.setRootPath(self.sd_root))
        self.ui.sd_tree.setColumnWidth(0, width // 2)
        for i in range(1, 4):
            self.ui.sd_tree.setColumnHidden(i, True)

    def prepare_sd_view(self):
        """Prepare the SD Card tab after an SD card location
        has been specified.
        """

        self.ui.import_all_btn.setEnabled(False)
        self.ui.import_all_ver_btn.setEnabled(False)
        path = self.ui.sd_tree.currentIndex().data()
        temp = self.ui.sd_tree.currentIndex()
        # Get the top directory for a specified path.
        while True:
            temp = temp.parent()
            if temp.data() is not None and self.sd_root not in temp.data():
                path = os.path.join(temp.data(), path)
                continue
            break

        self.sd_path_full = os.path.join(self.sd_root, path)

        # Setup the tree widget.
        self._set_data_sd()
        self._has_item()

    def _has_item(self):
        """Determines whether the SD tables contain an entry.

        return: True if the SD tables contain an entry, False
                otherwise.
        """

        # Determine which buttons should be enabled.
        count = 0
        for i in range(32):
            if self.ui.table_sd_left.item(i, 0).text() != "":
                count += 1
            if self.ui.table_sd_right.item(i, 0).text() != "":
                count += 1
            if count > 1:
                break
        self.ui.import_all_btn.setEnabled(count > 0)
        self.ui.import_all_ver_btn.setEnabled(count > 1)
        self.ui.delete_folder_sd_btn.setEnabled(True)

    def _set_data_sd(self):
        """Sets the data for the SD card table."""

        # Cleanup the tables
        for i in range(32):
            self.ui.table_sd_left.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_sd_left.setCellWidget(i, 1, None)
            self.ui.table_sd_left.setCellWidget(i, 2, None)
            self.ui.table_sd_right.setItem(i, 0, QTableWidgetItem(None))
            self.ui.table_sd_right.setCellWidget(i, 1, None)
            self.ui.table_sd_right.setCellWidget(i, 2, None)

        # Make sure we have an sd_card_path to work with.
        if not os.path.isdir(self.sd_path_full):
            return

        for pch in os.listdir(self.sd_path_full):
            # Get the index
            index = pch.split("_")[0]
            if index[0] == "0":
                # Get the useful int index.
                index = int(index[1:3])

                import_btn = QPushButton("Import patch", self)
                import_btn.setObjectName(str(index))
                import_btn.setFont(self.ui.table_PS.horizontalHeader().font())
                import_btn.clicked.connect(self._import_patch_sd)
                rmv_btn = QPushButton("X", self)
                rmv_btn.setObjectName(str(index))
                rmv_btn.setFont(self.ui.table_PS.horizontalHeader().font())
                rmv_btn.clicked.connect(self._remove_sd)

                if index < 32:
                    # Left sd table.
                    self.ui.table_sd_left.setItem(index, 0, QTableWidgetItem(pch))
                    self.ui.table_sd_left.setCellWidget(index, 1, import_btn)
                    self.ui.table_sd_left.setCellWidget(index, 2, rmv_btn)
                else:
                    # Right sd table.
                    self.ui.table_sd_right.setItem(index - 32, 0, QTableWidgetItem(pch))
                    self.ui.table_sd_right.setCellWidget(index - 32, 1, import_btn)
                    self.ui.table_sd_right.setCellWidget(index - 32, 2, rmv_btn)

    def export_path(self):
        """Sets the directory patches are exported to when using the Local Storage
        tab's export function. By default this directory is 'to_zoia'.
        Currently triggered via a button press.
        """

        input_dir = QFileDialog.getExistingDirectory(
            None, "Select a directory:", expanduser(self.sd_root)
        )
        if input_dir != "" and os.path.isdir(input_dir):
            if "/" in input_dir and platform.system().lower() == "windows":
                # THIS IS NEEDED FOR WINDOWS.
                # This comes from a bug with QFileDialog returning the
                # wrong path separator on Windows for some odd reason.
                input_dir = input_dir.split("/")[0]
            elif "/" in input_dir:
                # OSX case.
                pass
            else:
                input_dir = input_dir.split(os.path.sep)[0]
            self.export_dir = str(input_dir)

            e = self.export_dir.split("/")[-1]
            self.ui.statusbar.showMessage("Export directory successfully set.", timeout=5000)
            self.msg.setWindowTitle("Export Directory Has Been Set")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Export directory has been set to {}.".format(e))
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()

    def _import_patch_sd(self):
        """Imports a single patch from an SD card into the Librarian.
        Will alert the user if the patch exists in the Librarian.
        Currently triggered via a button press.
        """

        # Only proceed if there is actually an SD path.
        if self.sd_path_full is not None:
            for sd_pch in os.listdir(self.sd_path_full):
                index = int(self.sender().objectName())
                if index < 10:
                    index = "00{}".format(index)
                else:
                    index = "0{}".format(index)
                if index == sd_pch[:3]:
                    # Try to import the patch and notify the user of the
                    # result via a popup.
                    try:
                        self.save.import_to_backend(
                            os.path.join(self.sd_path_full, sd_pch)
                        )
                        self.ui.statusbar.showMessage("Import complete.", timeout=5000)
                        # self.msg.setIcon(QMessageBox.Information)
                        # self.msg.setWindowTitle("Import Complete")
                        # self.msg.setText("The patch has been successfully imported.")
                        # self.msg.exec_()
                        return
                    except errors.SavingError as e:
                        # Prep the error message
                        e = (
                            str(e)
                            .split("(")[1]
                            .split(")")[0]
                            .split(",")[0]
                            .replace("'", "")
                        )
                        self.ui.statusbar.showMessage("Import failed.", timeout=5000)
                        self.msg.setWindowTitle("Patch Already In Library")
                        self.msg.setIcon(QMessageBox.Information)
                        self.msg.setText(
                            "That patch exists within your locally "
                            "saved patches as {}. \nNo importing has occurred.".format(
                                e
                            )
                        )
                        self.msg.setStandardButtons(QMessageBox.Ok)
                        self.msg.exec_()
                        return

    def delete_sd_item(self):
        """Deletes the currently selected directory from the SD card.
        Currently triggered via a button press.
        """

        # Give the user a chance to cancel if they hit the button by
        # mistake.
        if os.path.isdir(self.sd_path_full):
            self.msg.setWindowTitle("Warning")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText(
                "This will delete everything contained within the "
                "selected folder. This includes any files or "
                "additional folders contained within.\n\n"
                "Do you wish to continue?"
            )
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            val = self.msg.exec_()
            if val == QMessageBox.Yes:
                self.delete.delete_full_patch_directory(self.sd_path_full)
                self.ui.statusbar.showMessage("Selected SD folder has been deleted.", timeout=5000)
        else:
            self.delete.delete_file(self.get_sd_path())

        # Reload the tree view.
        self._set_data_sd()
        self._has_item()
        self.ui.sd_tree.clearSelection()
        self.ui.delete_folder_sd_btn.setEnabled(False)

    def _move_patch_sd(self, src, dest):
        """Attempts to move a patch from one SD card slot to another
        Currently triggered via a QTableWidget move event.

        src: The index the item originated from.
        dest: The index the item is being moved to.
        """

        self.ui.table_sd_left.clearSelection()
        self.ui.table_sd_right.clearSelection()

        if dest > 63:
            dest -= 64

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
        for pch in os.listdir(self.sd_path_full):
            if pch[:3] == src:
                src_pch = pch
            if pch[:3] == dest:
                dest_pch = pch
            if src_pch is not None and dest_pch is not None:
                # We are doing a swap.
                try:
                    os.rename(
                        os.path.join(self.sd_path_full, src_pch),
                        os.path.join(self.sd_path_full, dest + src_pch[3:]),
                    )
                    os.rename(
                        os.path.join(self.sd_path_full, dest_pch),
                        os.path.join(self.sd_path_full, src + dest_pch[3:]),
                    )
                except FileExistsError:
                    # Swapping files that are named the same thing.
                    os.rename(
                        os.path.join(self.sd_path_full, src_pch),
                        os.path.join(self.sd_path_full, "064" + src_pch[3:]),
                    )
                    # Swapping files that are named the same thing.
                    os.rename(
                        os.path.join(self.sd_path_full, dest_pch),
                        os.path.join(self.sd_path_full, src + dest_pch[3:]),
                    )
                    os.rename(
                        os.path.join(self.sd_path_full, "064" + src_pch[3:]),
                        os.path.join(self.sd_path_full, dest + src_pch[3:]),
                    )
                self._set_data_sd()
                dest = int(dest)
                for i in range(64):
                    if i == dest:
                        if i > 31:
                            self.ui.table_sd_right.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True
                            )
                        else:
                            self.ui.table_sd_left.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True
                            )
                return

        # We are doing a move.
        if src_pch is None:
            self._set_data_sd()
            return
        os.rename(
            os.path.join(self.sd_path_full, src_pch),
            os.path.join(self.sd_path_full, dest + src_pch[3:]),
        )

        # Clear the selections and reload the tables.
        dest = int(dest)
        for i in range(64):
            if i == dest:
                if i > 31:
                    self.ui.table_sd_right.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True
                    )
                else:
                    self.ui.table_sd_left.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True
                    )

        self._set_data_sd()

    def events(self, o, e):
        """Handles events that relate to dragging and dropping entries
        to/from the tables that are populated to contain the patches
        in a selected directory.

        o: The object that initiated the event.
        e: The event that was initiated.
        """

        if e.type() == QEvent.FocusAboutToChange:
            if o.objectName() == "table_sd_left":
                self.ui.table_sd_left.clearSelection()
            else:
                self.ui.table_sd_right.clearSelection()
        if e.type() == QEvent.ChildAdded:
            # Figure out which rows are selected.
            indexes = self.ui.table_sd_left.selectionModel().selectedRows()
            for index in sorted(indexes):
                self.rows_left.append(index)

            indexes = self.ui.table_sd_right.selectionModel().selectedRows()
            for index in sorted(indexes):
                self.rows_right.append(index)

            # Hide these rows so they can be dragged into.
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

            if self.sd_path_full is None:
                return

            dst_index = None

            if o.objectName() == "table_sd_left":
                src_index = self.ui.table_sd_left.currentRow()
            else:
                src_index = self.ui.table_sd_right.currentRow() + 32

            if (len(self.rows_left) <= 1 and len(self.rows_right) == 0) or (
                len(self.rows_right) <= 1 and len(self.rows_left) == 0
            ):
                # Single selection.
                self.rows_left = []
                self.rows_right = []
                if (
                    self.ui.table_sd_left.item(src_index, 0) is not None
                    and self.ui.table_sd_left.item(src_index, 0).text() == ""
                ) or (
                    self.ui.table_sd_right.item(src_index - 32, 0) is not None
                    and self.ui.table_sd_right.item(src_index - 32, 0).text() == ""
                ):
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
                            for pch in os.listdir(self.sd_path_full):
                                if "{}_zoia_".format(temp_index) in pch:
                                    if i != dst_index:
                                        self._move_patch_sd(i, dst_index)
                                    return
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
                        return
                    if src_index != dst_index:
                        self._move_patch_sd(src_index, dst_index)
                    return
            else:
                # Multiple selections
                self.util.multi_drag_drop(
                    self.rows_left,
                    self.rows_right,
                    self.ui.table_sd_left,
                    self.ui.table_sd_right,
                    self._move_patch_sd,
                )
                self.rows_left = []
                self.rows_right = []

    def _remove_sd(self):
        """Removes a patch that is stored on a user's SD card.
        Currently triggered via a button press.
        """

        # Get the row and delete it.
        row = self.sender().objectName()
        index = "00{}".format(row) if len(row) < 2 else "0{}".format(row)
        self.delete.delete_patch_sd(index, self.sd_path_full)
        self.ui.statusbar.showMessage("Patch deleted.", timeout=5000)

        # Reload the tables.
        self._set_data_sd()
        self.ui.table_sd_right.clearSelection()
        self.ui.table_sd_left.clearSelection()
        self._has_item()

    def get_sd_path(self):
        """Gets the current SD card path.
        Will be None if it has not been determined.

        return: The SD card path as a string.
        """

        return self.sd_path_full

    def get_sd_root(self):
        """Gets the current SD card root.
        Will be None if it has not been determined.

        return: The SD card root as a string.
        """

        return self.sd_root

    def get_export_path(self):
        """Gets the current default export dir.
        Will be None if it has not been determined.

        return: The default export dir as a string.
        """

        return self.export_dir

    def set_sd_root(self, path):
        """Sets the current SD card root.

        path: The path that will be set.
        """

        self.sd_root = path

    def set_export_path(self, path):
        """Sets the current export dir.

        path: The path that will be set.
        """

        self.export_dir = path
