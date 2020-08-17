import json
import os

from PySide2.QtCore import QThreadPool
from PySide2.QtWidgets import QMainWindow, QMessageBox, QPushButton

from zoia_lib.backend.worker import Worker
from zoia_lib.common import errors


class ZOIALibrarianPS(QMainWindow):
    """ The ZOIALibrarianPS class is responsible for all
    activities contained within the PatchStorage View tab of the
    application.
    """

    def __init__(self, ui, api, path, msg, save):
        """ Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        api: Backend class to aid with PS API requests
        path: A String representing the path to the backend application
              directory.
        msg: A template QMessageBox.
        save: Backend class to aid with the downloading of classes.
        """

        super().__init__()

        self.data_PS = None
        self.ui = ui
        self.api = api
        self.path = path
        self.msg = msg
        self.save = save
        self.thread_pool = QThreadPool()
        self.cnt = 0
        self.fails = 0

    def reload_ps(self, f1):
        """ Reloads the PS table view to accurately reflect new uploads.
        Currently triggered via a menu action.
        """

        # Get the new patch metadata that we don't have (if any).
        self.ui.refresh_pch_btn.setEnabled(False)
        with open(os.path.join(self.path, "data.json"), "w") as f:
            f.write(json.dumps(self.api.get_all_patch_data_init()))
        self.ui.searchbar_PS.setText("")
        f1()
        self.ui.refresh_pch_btn.setEnabled(True)
        self.ui.statusbar.showMessage("Patch list refreshed!", timeout=5000)
        self.msg.setWindowTitle("Patches Refreshed")
        self.msg.setText("The PatchStorage patch list has been refreshed.")
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def metadata_init(self):
        """ Retrieves all PS metadata via API calls.
        """

        # Check for metadata in the user's backend.
        if "data.json" not in os.listdir(self.path):
            ps_data = self.api.get_all_patch_data_init()
        else:
            # Got previous metadata, need to ensure that there are no
            # new patches.
            with open(os.path.join(self.path, "data.json"),
                      "r") as f:
                data = json.loads(f.read())
            if len(data) == self.api.patch_count:
                # Assume no new patches; allow the user to refresh manually.
                self.data_PS = data
                return
            elif len(data) > self.api.patch_count:
                # Uh oh, some patches got deleted on PatchStorage.
                ps_data = self.api.get_all_patch_data_init()
            else:
                # Get the new patch metadata that we don't have.
                new_patches = self.api.get_newest_patches(len(data))
                ps_data = new_patches + data

        # Create/update the data file with the new data.
        with open(os.path.join(self.path, "data.json"),
                  "w") as f:
            f.write(json.dumps(ps_data))
            self.data_PS = ps_data

    def download_all_thread(self):
        """ Initializes a Worker thread to manage the downloading of
        all ZOIA patches currently hosted on PatchStorage.
        Currently triggered via a button press.
        """

        # Pass the function to execute
        worker = Worker(self.download_all)
        worker.signals.finished.connect(self.download_all_done)
        worker.signals.progress.connect(self.download_all_progress)

        # Execute
        self.thread_pool.start(worker)

    def download_all_progress(self, i):
        """ Progress update provided by the worker to display how
        many patches have been downloaded.

        i: The current patch that is being downloaded.
        """

        self.ui.statusbar.showMessage(
            "Trying to download patch #{} of {}".format(
                i + 1, self.ui.table_PS.rowCount()))

    def download_all_done(self):
        """ Notifies the user once all PatchStorage patches have been
        downloaded. Will also notify the user with the number of
        patches that failed to download and explain why they failed.
        """

        self.msg.setWindowTitle("Download Complete")
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Successfully downloaded {} patch(es)."
                         "".format(self.cnt))
        self.msg.setInformativeText("Did not download {} patch(es) because "
                                    "they are either .py files or use a "
                                    "compression algorithm other than .zip"
                                    "".format(self.fails))
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
        self.msg.setInformativeText(None)
        self.ui.statusbar.showMessage("", timeout=10)
        self.ui.btn_dwn_all.setEnabled(True)
        self.ui.refresh_pch_btn.setEnabled(True)
        self.ui.check_for_updates_btn.setEnabled(True)

    def download_all(self, progress_callback):
        """ Attempts to download all patches currently stored on
        PatchStorage. This method will ignore failures and continue
        on to the next patch until it has exhausted the list.
        """

        self.ui.btn_dwn_all.setEnabled(False)
        self.ui.refresh_pch_btn.setEnabled(False)
        self.ui.check_for_updates_btn.setEnabled(False)

        self.fails = 0
        self.cnt = 0

        for i in range(self.ui.table_PS.rowCount()):
            btn = self.ui.table_PS.cellWidget(i, 4)
            if btn.isEnabled():
                # Try to download the patch.
                try:
                    self.save.save_to_backend(self.api.download(
                        btn.objectName()))
                    btn.setEnabled(False)
                    btn.setText("Downloaded!")
                    self.cnt += 1
                except errors.SavingError:
                    self.fails += 1
            progress_callback.emit(i)

    def initiate_download(self):
        """ Attempts to download a patch from the PS API. Once the
        download completes, it will be saved to the backend application
        directory.
        Currently, only patches uploaded as .bin or .zip files will
        successfully download. Support for additional file formats will
        be implemented in subsequent releases.
        """

        self.ui.statusbar.showMessage("Starting download...",
                                      timeout=5000)

        # TODO Replace with FCFS thread scheduling
        try:
            self.save.save_to_backend(self.api.download(str(
                self.sender().objectName())))
            self.sender().setEnabled(False)
            self.sender().setText("Downloaded!")
            self.ui.statusbar.showMessage("Download complete!", timeout=5000)
        except errors.SavingError:
            self.msg.setWindowTitle("Invalid File Type")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Unfortunately, that patch is not in a "
                             "supported format.")
            self.msg.setInformativeText(
                "Supported formats are .bin and .zip")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setInformativeText(None)

    def create_dwn_btn(self, i, idx):
        """ Creates a download button for patches on the PatchStorage
        tab.

        i: The row for which the button will be inserted into.
        """

        # Prepare the button.
        dwn = QPushButton("Click me\nto download!", self)
        dwn.setObjectName(idx)
        dwn.setFont(self.ui.table_PS.horizontalHeader().font())
        dwn.clicked.connect(self.initiate_download)
        # Only enable it if we haven't already downloaded the patch.
        if idx in os.listdir(self.path):
            dwn.setEnabled(False)
            dwn.setText("Downloaded!")
        self.ui.table_PS.setCellWidget(i, 4, dwn)

    def get_data_ps(self):
        """ Getter method to get PS table data.
        """

        return self.data_PS
