import os
import platform
from os.path import expanduser

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QTableWidgetItem, QPushButton, QFileDialog, \
    QFileSystemModel, QMessageBox, QTableWidgetSelectionRange, QMainWindow


class ZOIALibrarianSD(QMainWindow):
    """ The ZoiaLibrarianSD class is responsible for all
    activities contained within the SD Card View tab of the application.
    """

    def __init__(self, ui, f2, msg, delete):
        """ Initializes the class with the required parameters.
        """

        # Needed to make use of self.sender()
        super().__init__()

        # Variable init.
        self.ui = ui
        self.delete = delete
        self.sd_path_full = None
        self.sd_root = None
        self.can_export_bank = False
        self.f2 = f2
        self.msg = msg

    def sd_path(self, startup, width):
        """ Allows the user to specify the path to their SD card via
        their OS file explorer dialog. Note, nothing is done to ensure
        that the location selected is actually an SD card.
        Currently triggered via a menu action.
        """

        if not startup:
            input_dir = QFileDialog.getExistingDirectory(None,
                                                         'Select an SD Card:',
                                                         expanduser("~"))
            if input_dir is not "" and os.path.isdir(input_dir):
                if "/" in input_dir and platform.system().lower() == "windows":
                    # THIS IS NEEDED FOR WINDOWS.
                    # This comes from a bug with QFileDialog returning the
                    # wrong path separator on Windows for some odd reason.
                    input_dir = input_dir.split("/")[0]
                elif "/" in input_dir and platform.system().lower() != \
                        "windows":
                    # OSX case.
                    pass
                elif "\\" in input_dir:
                    input_dir = input_dir.split("\\")[0]
                elif "//" in input_dir:
                    input_dir = input_dir.split("//")[0]
                elif "\\\\" in input_dir:
                    input_dir = input_dir.split("\\\\")[0]
                else:
                    input_dir = input_dir.split(os.path.sep)[0]
                self.sd_root = str(input_dir)
                self.ui.tab_sd.setEnabled(True)
                self.can_export_bank = True
            else:
                self.ui.tab_sd.setEnabled(False)
                self.can_export_bank = False
                self.ui.tabs.setCurrentIndex(1)

        # Setup the SD card tree view for the SD Card tab.
        model = QFileSystemModel()
        model.setRootPath(self.sd_root)
        self.ui.sd_tree.setModel(model)
        self.ui.sd_tree.setRootIndex(model.setRootPath(self.sd_root))
        self.ui.sd_tree.setColumnWidth(0, width // 2)
        for i in range(1, 4):
            self.ui.sd_tree.setColumnHidden(i, True)

    def prepare_sd_view(self):
        """ Prepare the SD Card tab after an SD card location
        has been specified.
        """

        self.ui.import_all_btn.setEnabled(False)
        path = self.ui.sd_tree.currentIndex().data()
        temp = self.ui.sd_tree.currentIndex()
        while True:
            temp = temp.parent()
            if temp.data() is not None and self.sd_root \
                    not in temp.data():
                path = os.path.join(temp.data(), path)
                continue
            break

        self.sd_path_full = os.path.join(self.sd_root, path)

        self.set_data_sd()
        # If any patches populate the tables, enable the import all button.
        # TODO Find out if this can be determined without iterating through the
        #  entire table.
        for i in range(64):
            if i < 32:
                if self.ui.table_sd_left.item(i, 0).text() != "":
                    self.ui.import_all_btn.setEnabled(True)
                    break
            else:
                if self.ui.table_sd_right.item(i - 32, 0).text() != "":
                    self.ui.import_all_btn.setEnabled(True)
                    break
        self.ui.delete_folder_sd_btn.setEnabled(True)

    def set_data_sd(self):
        """ Sets the data for the SD card table.
        """

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

                rmv_btn = QPushButton("X", self)
                rmv_btn.setObjectName(str(index))
                rmv_btn.setFont(self.ui.table_PS.horizontalHeader().font())
                rmv_btn.clicked.connect(self.remove_sd)
                rmv_btn.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, "
                    "x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 19), "
                    "stop:1 rgba(255, 255, 255, 255));")
                import_btn = QPushButton("Click me to import!", self)
                import_btn.setObjectName(str(index))
                import_btn.setFont(self.ui.table_PS.horizontalHeader().font())
                import_btn.clicked.connect(self.f2)
                import_btn.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, "
                    "x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 19), "
                    "stop:1 rgba(255, 255, 255, 255));")

                if index < 32:
                    # Left sd table.
                    self.ui.table_sd_left.setItem(index, 0, QTableWidgetItem(
                        pch))
                    self.ui.table_sd_left.setCellWidget(index, 1, rmv_btn)
                    self.ui.table_sd_left.setCellWidget(index, 2, import_btn)
                else:
                    # Right sd table.
                    self.ui.table_sd_right.setItem(index - 32, 0,
                                                   QTableWidgetItem(pch))
                    self.ui.table_sd_right.setCellWidget(index - 32, 1,
                                                         rmv_btn)
                    self.ui.table_sd_right.setCellWidget(index - 32, 2,
                                                         import_btn)

    def delete_sd_item(self, delete):
        """ Deletes the currently selected directory from the SD card.
        Currently triggered via a button press.
        """

        if os.path.isdir(self.sd_path_full):
            self.msg.setWindowTitle("Warning")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText(
                "This will delete everything contained within the \n"
                "selected folder. This includes any files or "
                "additional\nfolders contained within.\n\n"
                "Do you wish to continue?")
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            val = self.msg.exec_()
            if val == QMessageBox.Yes:
                delete.delete_full_patch_directory(self.sd_path_full)
                self.prepare_sd_view()
        else:
            delete.delete_file(self.get_sd_path())
            self.prepare_sd_view()

        self.ui.sd_tree.clearSelection()
        self.ui.delete_folder_sd_btn.setEnabled(False)

    def move_patch_sd(self, src, dest):
        """ Attempts to move a patch from one SD card slot to another
        Currently triggered via a QTableWidget move event.

        src: The index the item originated from.
        dest: The index the item is being moved to.
        """

        self.ui.table_sd_left.clearSelection()
        self.ui.table_sd_right.clearSelection()

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
                    os.rename(os.path.join(self.sd_path_full, src_pch),
                              os.path.join(self.sd_path_full, dest
                                           + src_pch[3:]))
                    os.rename(os.path.join(self.sd_path_full, dest_pch),
                              os.path.join(self.sd_path_full, src
                                           + dest_pch[3:]))
                except FileExistsError:
                    # Swapping files that are named the same thing.
                    os.rename(os.path.join(self.sd_path_full, src_pch),
                              os.path.join(self.sd_path_full, "064"
                                           + src_pch[3:]))
                    # Swapping files that are named the same thing.
                    os.rename(os.path.join(self.sd_path_full, dest_pch),
                              os.path.join(self.sd_path_full, src
                                           + dest_pch[3:]))
                    os.rename(os.path.join(self.sd_path_full, "064"
                                           + src_pch[3:]),
                              os.path.join(self.sd_path_full, dest
                                           + src_pch[3:]))
                self.set_data_sd()
                dest = int(dest)
                for i in range(64):
                    if i == dest:
                        if i > 31:
                            self.ui.table_sd_right.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                        else:
                            self.ui.table_sd_left.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                return

        # We are doing a move.

        os.rename(os.path.join(self.sd_path_full, src_pch),
                  os.path.join(self.sd_path_full, dest + src_pch[3:]))

        dest = int(dest)
        for i in range(64):
            if i == dest:
                if i > 31:
                    self.ui.table_sd_right.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)
                else:
                    self.ui.table_sd_left.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)

        self.set_data_sd()

    def events(self, o, e):
        """ Handles events that relate to dragging and dropping entries
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

            dst_index = None

            if o.objectName() == "table_sd_left":
                src_index = self.ui.table_sd_left.currentRow()
            else:
                src_index = self.ui.table_sd_right.currentRow() + 32

            if (self.ui.table_sd_left.item(src_index, 0) is not None and
                self.ui.table_sd_left.item(src_index, 0).text() == "") \
                    or (self.ui.table_sd_right.item(src_index - 32, 0)
                        is not None and self.ui.table_sd_right.item(
                        src_index - 32, 0).text() == ""):
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
                                    self.move_patch_sd(i, dst_index)
                                    return True
                                else:
                                    return False
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
                    return False
                if src_index != dst_index:
                    self.move_patch_sd(src_index, dst_index)
                return True

    def remove_sd(self):
        """ Removes a patch that is stored on a user's SD card.
        Currently triggered via a button press.
        """

        row = self.sender().objectName()
        index = "00{}".format(row) if len(row) < 2 else "0{}".format(row)
        self.delete.delete_patch_sd(index, self.sd_path_full)
        self.set_data_sd()

    def get_sd_path(self):
        """ Gets the current SD card path.
        Will be None if it has not been determined.
        """

        return self.sd_path_full

    def get_sd_root(self):
        """ Gets the current SD card root.
        Will be None if it has not been determined.
        """

        return self.sd_root

    def get_can_export(self):
        """ Gets whether the application can export.
        Will be None if it has not been determined.
        """

        return self.can_export_bank

    def set_sd_root(self, path):
        """ Sets the current SD card root.
        """

        self.sd_root = path

    def set_export(self, val):
        """ Sets whether the application can export.
        """

        self.can_export_bank = val
