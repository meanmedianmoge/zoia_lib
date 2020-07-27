import os
import platform
from os.path import expanduser

from PySide2.QtWidgets import QTableWidgetItem, QPushButton, QFileDialog, \
    QFileSystemModel, QMessageBox, QTableWidgetSelectionRange


class ZOIALibrarianSD:
    """

    """

    def __init__(self, f1, f2, msg):
        """

        """

        self.sd_path_full = None
        self.sd_root = None
        self.can_export_bank = False
        self.f1 = f1
        self.f2 = f2
        self.msg = msg

    def sd_path(self, ui, startup, width):
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
                ui.tab_sd.setEnabled(True)
                self.can_export_bank = True
            else:
                ui.tab_sd.setEnabled(False)
                self.can_export_bank = False
                ui.tabs.setCurrentIndex(1)

        # Setup the SD card tree view for the SD Card tab.
        model = QFileSystemModel()
        model.setRootPath(self.sd_root)
        ui.sd_tree.setModel(model)
        ui.sd_tree.setRootIndex(model.setRootPath(self.sd_root))
        ui.sd_tree.setColumnWidth(0, width // 4)

    def prepare_sd_view(self, ui):
        """ Prepare the SD Card tab after an SD card location
        has been specified.
        """

        ui.import_all_btn.setEnabled(False)
        path = ui.sd_tree.currentIndex().data()
        temp = ui.sd_tree.currentIndex()
        while True:
            temp = temp.parent()
            if temp.data() is not None and self.sd_root \
                    not in temp.data():
                path = os.path.join(temp.data(), path)
                continue
            break

        self.sd_path_full = os.path.join(self.sd_root, path)

        self.set_data_sd(ui)
        # If any patches populate the tables, enable the import all button.
        # TODO Find out if this can be determined without iterating through the
        #  entire table.
        for i in range(64):
            if i < 32:
                if ui.table_sd_left.item(i, 0).text() != "":
                    ui.import_all_btn.setEnabled(True)
                    break
            else:
                if ui.table_sd_right.item(i - 32, 0).text() != "":
                    ui.import_all_btn.setEnabled(True)
                    break
        ui.delete_folder_sd_btn.setEnabled(True)

    def set_data_sd(self, ui):
        """ Sets the data for the SD card table.
        """

        # Cleanup the tables
        for i in range(32):
            ui.table_sd_left.setItem(i, 0, QTableWidgetItem(None))
            ui.table_sd_left.setCellWidget(i, 1, None)
            ui.table_sd_left.setCellWidget(i, 2, None)
            ui.table_sd_right.setItem(i, 0, QTableWidgetItem(None))
            ui.table_sd_right.setCellWidget(i, 1, None)
            ui.table_sd_right.setCellWidget(i, 2, None)

        # Make sure we have an sd_card_path to work with.
        if not os.path.isdir(self.sd_path_full):
            return

        for pch in os.listdir(self.sd_path_full):
            # Get the index
            index = pch.split("_")[0]
            if index[0] == "0":
                # Get the useful int index.
                index = int(index[1:3])

                push_btn = QPushButton("X")
                push_btn.setObjectName(str(index))
                push_btn.setFont(ui.table_PS.horizontalHeader().font())
                push_btn.clicked.connect(self.f1)
                import_btn = QPushButton("Click me to import!")
                import_btn.setObjectName(str(index))
                import_btn.setFont(ui.table_PS.horizontalHeader().font())
                import_btn.clicked.connect(self.f2)

                if index < 32:
                    # Left sd table.
                    ui.table_sd_left.setItem(index, 0, QTableWidgetItem(pch))
                    ui.table_sd_left.setCellWidget(index, 1, push_btn)
                    ui.table_sd_left.setCellWidget(index, 2, import_btn)
                else:
                    # Right sd table.
                    ui.table_sd_right.setItem(index - 32, 0,
                                              QTableWidgetItem(pch))
                    ui.table_sd_right.setCellWidget(index - 32, 1, push_btn)
                    ui.table_sd_right.setCellWidget(index - 32, 2, import_btn)

    def delete_sd_item(self, ui, delete):
        """ Deletes the currently selected directory from the SD card.
        Currently triggered via a button press.
        """

        if os.path.isdir(self.sd_path_full):
            self.msg.setWindowTitle("Warning")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText("This will delete everything contained within the \n"
                        "selected folder. This includes any files or"
                        "additional \n folders contained within. \n"
                        "Do you wish to continue?")
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            val = self.msg.exec_()
            if val == QMessageBox.Yes:
                delete.delete_full_patch_directory(self.sd_path_full)
                self.prepare_sd_view(ui)
        else:
            delete.delete_file(self.get_sd_path())
            self.prepare_sd_view(ui)

        ui.sd_tree.clearSelection()
        ui.delete_folder_sd_btn.setEnabled(False)

    def move_patch_sd(self, ui, src, dest):
        """ Attempts to move a patch from one SD card slot to another
        Currently triggered via a QTableWidget move event.

        src: The index the item originated from.
        dest: The index the item is being moved to.
        """

        ui.table_sd_left.clearSelection()
        ui.table_sd_right.clearSelection()

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
                self.set_data_sd(ui)
                dest = int(dest)
                for i in range(64):
                    if i == dest:
                        if i > 31:
                            ui.table_sd_right.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                        else:
                            ui.table_sd_left.setRangeSelected(
                                QTableWidgetSelectionRange(i, 0, i, 0), True)
                return

        # We are doing a move.

        os.rename(os.path.join(self.sd_path_full, src_pch),
                  os.path.join(self.sd_path_full, dest + src_pch[3:]))

        dest = int(dest)
        for i in range(64):
            if i == dest:
                if i > 31:
                    ui.table_sd_right.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)
                else:
                    ui.table_sd_left.setRangeSelected(
                        QTableWidgetSelectionRange(i, 0, i, 0), True)

        self.set_data_sd(ui)

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


