import json
import os

from PySide2.QtWidgets import QMainWindow, QMessageBox

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
            with open(os.path.join(self.path, "data.json"),
                      "w") as f:
                f.write(json.dumps(ps_data))
                self.data_PS = ps_data
        else:
            # Got previous metadata, need to ensure that there are no
            # new patches.
            with open(os.path.join(self.path, "data.json"),
                      "r") as f:
                data = json.loads(f.read())
            if len(data) == self.api.patch_count:
                # Assume no new patches; allow the user to refresh manually.
                self.data_PS = data
            elif len(data) > self.api.patch_count:
                # Uh oh, some patches got deleted on PatchStorage.
                ps_data = self.api.get_all_patch_data_init()
                with open(os.path.join(self.path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(ps_data))
                    self.data_PS = ps_data
            else:
                # Get the new patch metadata that we don't have.
                new_patches = self.api.get_newest_patches(len(data))
                data = new_patches + data
                with open(os.path.join(self.path, "data.json"),
                          "w") as f:
                    f.write(json.dumps(data))
                    self.data_PS = data

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
            self.msg.setInformativeText("Supported formats are .bin and .zip")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            self.msg.setInformativeText(None)

    def get_data_ps(self):
        """ Getter method to get PS table data.
        """

        return self.data_PS
