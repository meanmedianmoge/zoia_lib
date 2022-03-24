import json
import os

from PySide2 import QtCore
from PySide2.QtCore import QThread
from PySide2.QtWidgets import QMainWindow, QMessageBox, QPushButton

from zoia_lib.common import errors


class ZOIALibrarianPS(QMainWindow):
    """The ZOIALibrarianPS class is responsible for all
    activities contained within the PatchStorage View tab of the
    application.
    """

    def __init__(self, ui, api, path, msg, save, f1):
        """Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        api: Backend class to aid with PS API requests
        path: A String representing the path to the backend application
              directory.
        msg: A template QMessageBox.
        save: Backend class to aid with the saving of patches.
        f1: Provides access to the sort_and_set() method located in the
            ZOIALibrarianMain class.
        """

        super().__init__()

        self.data_PS = None
        self.ui = ui
        self.api = api
        self.path = path
        self.msg = msg
        self.save = save
        self.sort_and_set = f1

        # Threads
        self.worker_dwn = DownloadAllWorker(self.ui, self.save, self.api)
        self.worker_dwn.signal.connect(self._download_all_done)
        self.worker_dwn.signal_2.connect(self._download_all_progress)

        self.worker_ps = ReloadPSWorker(self.path, self.api)
        self.worker_ps.signal.connect(self._reload_ps_done)

    def metadata_init(self):
        """Retrieves all PS metadata via API calls."""

        try:
            # Check for metadata in the user's backend.
            if "data.json" not in os.listdir(self.path):
                ps_data = self.api.get_all_patch_data_init()
            else:
                # Got previous metadata, need to ensure that there are no
                # new patches.
                with open(os.path.join(self.path, "data.json"), "r") as f:
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
            with open(os.path.join(self.path, "data.json"), "w") as f:
                f.write(json.dumps(ps_data))
                self.data_PS = ps_data

        except json.JSONDecodeError:
            # Existing data.json was empty, replace it
            ps_data = self.api.get_all_patch_data_init()
            # Create/update the data file with the new data.
            with open(os.path.join(self.path, "data.json"), "w") as f:
                f.write(json.dumps(ps_data))
                self.data_PS = ps_data

        except AttributeError:
            # Could not connect to API to determine patch count
            self.ui.statusbar.showMessage("API connection failed.", timeout=5000)
            self.msg.setWindowTitle("API Error")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "Failed to retrieve the patch count from PatchStorage."
            )
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.ui.tabs.setCurrentIndex(1)

        except Exception as e:
            # Other unknown API connection error.
            self.ui.statusbar.showMessage("API connection failed.", timeout=5000)
            self.msg.setWindowTitle("API Error")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "Failed to retrieve the patch metadata from PatchStorage."
            )
            self.msg.setDetailedText(str(e))
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setDetailedText(None)
            self.ui.tabs.setCurrentIndex(1)

    def reload_ps_thread(self):
        """Initializes a Worker thread to manage the refreshing of
        all ZOIA patches currently hosted on PatchStorage.
        Currently triggered via a button press.
        """

        # Disable the necessary buttons.
        self.ui.btn_dwn_all.setEnabled(False)
        self.ui.refresh_pch_btn.setEnabled(False)
        self.ui.statusbar.showMessage("Retrieving patches.", timeout=5000)

        # Execute
        self.worker_ps.start()

    def _reload_ps_done(self):
        """Notifies the user once all PatchStorage patches have been
        retrieved.
        """

        # Set the data and notify the user via a popup.
        self.ui.searchbar_PS.setText("")
        self.sort_and_set()
        self.ui.btn_dwn_all.setEnabled(True)
        self.ui.refresh_pch_btn.setEnabled(True)
        self.ui.statusbar.showMessage("Patch list refreshed.", timeout=5000)
        self.msg.setWindowTitle("Patches Refreshed")
        self.msg.setText("The PatchStorage patch list has been refreshed.")
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def download_all_thread(self):
        """Initializes a Worker thread to manage the downloading of
        all ZOIA patches currently hosted on PatchStorage.
        Currently triggered via a button press.
        """

        # Disable the necessary buttons.
        self.ui.btn_dwn_all.setEnabled(False)
        self.ui.refresh_pch_btn.setEnabled(False)
        self.ui.check_for_updates_btn.setEnabled(False)
        self.ui.searchbar_PS.setEnabled(False)

        # Execute
        self.worker_dwn.start()

    def _download_all_progress(self, i):
        """Progress update provided by the worker to display how
        many patches have been downloaded.

        i: The current patch that is being downloaded.
        """

        self.ui.statusbar.showMessage(
            "Trying to download patch #{} of {}".format(
                i + 1, self.ui.table_PS.rowCount()
            ),
            timeout=5000,
        )

    def _download_all_done(self, cnt, fails):
        """Notifies the user once all PatchStorage patches have been
        downloaded. Will also notify the user with the number of
        patches that failed to download and explain why they failed.

        cnt: The count of patches that downloaded successfully.
        fails: The count of patches that failed to download.
        """

        # Notify the user via a popup.
        self.ui.statusbar.showMessage(
            "All patches successfully downloaded.", timeout=5000
        )
        self.msg.setWindowTitle("Download Complete")
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Successfully downloaded {} patch(es)." "".format(cnt))
        self.msg.setInformativeText(
            "Did not download {} patch(es) because "
            "they are either .py files or use a "
            "compression algorithm other than .zip"
            "".format(fails)
        )
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
        self.msg.setInformativeText(None)

        # Re-enable the necessary UI components.
        self.ui.statusbar.showMessage("", timeout=10)
        self.ui.btn_dwn_all.setEnabled(True)
        self.ui.refresh_pch_btn.setEnabled(True)
        self.ui.check_for_updates_btn.setEnabled(True)
        self.ui.searchbar_PS.setEnabled(True)

    def initiate_download(self):
        """Attempts to download a patch from the PS API. Once the
        download completes, it will be saved to the backend application
        directory.
        Currently, only patches uploaded as .bin or .zip files will
        successfully download. .rar files can be downloaded if a user
        has WinRAR installed. Further compression methods can be added
        if users begin to use them on PatchStorage.
        """

        self.ui.statusbar.showMessage("Starting download.", timeout=5000)

        # TODO Replace with FCFS thread scheduling
        # Try to download the patch.
        try:
            self.save.save_to_backend(
                self.api.download(str(self.sender().objectName()))
            )
            self.sender().setEnabled(False)
            self.sender().setText("Downloaded")
            self.ui.statusbar.showMessage("Download complete.", timeout=5000)
        except errors.SavingError:
            # .py or .rar and the user doesn't have WinRAR installed.
            self.ui.statusbar.showMessage("Download failed.", timeout=5000)
            self.msg.setWindowTitle("Invalid File Type")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "Unfortunately, that patch is not in a " "supported format."
            )
            self.msg.setInformativeText("Supported formats are .bin and .zip")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setInformativeText(None)
        except Exception as e:
            # Let the user know the API failed.
            self.ui.statusbar.showMessage("API connection failed.", timeout=5000)
            self.msg.setWindowTitle("API Error")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Failed to download the patch from PatchStorage.")
            self.msg.setDetailedText(str(e))
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setDetailedText(None)

    def create_dwn_btn(self, i, idx):
        """Creates a download button for patches on the PatchStorage
        tab.

        i: The row for which the button will be inserted into.
        idx: The id for the patch the button is being created for.
        """

        # Prepare the button.
        dwn = QPushButton("Download \n patch", self)
        dwn.setObjectName(idx)
        dwn.setFont(self.ui.table_PS.horizontalHeader().font())
        dwn.clicked.connect(self.initiate_download)
        # Only enable it if we haven't already downloaded the patch.
        if idx in os.listdir(self.path):
            dwn.setEnabled(False)
            dwn.setText("Downloaded")
        self.ui.table_PS.setCellWidget(i, 4, dwn)

    def get_data_ps(self):
        """Getter method to get PS table data.

        return: The PatchStorage data as a list.
        """

        return self.data_PS


class DownloadAllWorker(QThread):
    """The DownloadAllWorker class runs as a separate thread in the
    application to prevent application snag. This thread will attempt
    to download every ZOIA patch currently hosted on PatchStorage.
    """

    # UI communication
    signal = QtCore.Signal(int, int)
    signal_2 = QtCore.Signal(int)

    def __init__(self, ui, save, api):
        """Initializes the thread.

        ui: The UI component of ZOIALibrarianMain.
        save: Backend class to aid with the saving of patches.
        api: Backend class to aid with PS API requests.
        """

        QThread.__init__(self)
        self.ui = ui
        self.save = save
        self.api = api

        self.fails = 0
        self.cnt = 0

    def run(self):
        """Attempts to download all patches currently stored on
        PatchStorage. This method will ignore failures and continue
        on to the next patch until it has exhausted the list.
        """

        try:
            self.fails = 0
            self.cnt = 0

            for i in range(self.ui.table_PS.rowCount()):
                btn = self.ui.table_PS.cellWidget(i, 4)
                if btn.isEnabled():
                    # Try to download the patch.
                    try:
                        self.save.save_to_backend(self.api.download(btn.objectName()))
                        btn.setEnabled(False)
                        btn.setText("Downloaded")
                        self.cnt += 1
                    except errors.SavingError:
                        self.fails += 1
                    self.signal_2.emit(i)
            self.signal.emit(self.cnt, self.fails)
        except Exception as e:
            # Let the user know the API failed.
            self.ui.statusbar.showMessage("API connection failed.", timeout=5000)
            self.msg.setWindowTitle("API Error")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Failed to download the patch from PatchStorage.")
            self.msg.setDetailedText(str(e))
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setDetailedText(None)


class ReloadPSWorker(QThread):
    """The ReloadPSWorker class runs as a separate thread in the
    application to prevent application snag. This thread will reload
    the PS patch list that is displayed on the PatchStorage View tab.
    """

    # UI communication
    signal = QtCore.Signal()

    def __init__(self, path, api):
        """Initializes the thread.

        path: A string to the backend .ZoiaLibraryApp directory.
        api: Backend class to aid with PS API requests.
        """

        QThread.__init__(self)
        self.path = path
        self.api = api

    def run(self):
        """Attempts to download all patches currently stored on
        PatchStorage. This method will ignore failures and continue
        on to the next patch until it has exhausted the list.
        """

        # Try to download the patch.
        try:
            with open(os.path.join(self.path, "data.json"), "w") as f:
                f.write(json.dumps(self.api.get_all_patch_data_init()))
            self.signal.emit()
        except Exception as e:
            # Let the user know the API failed.
            self.ui.statusbar.showMessage("API connection failed.", timeout=5000)
            self.msg.setWindowTitle("API Error")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Failed to download the patch from PatchStorage.")
            self.msg.setDetailedText(str(e))
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setDetailedText(None)
