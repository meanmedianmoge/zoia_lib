import json
import os

from PySide2.QtWidgets import QMainWindow

class ZOIALibrarianPS(QMainWindow):

    def __init__(self, ui, api, path):
        """
        """

        self.data_PS = None
        self.ui = ui
        self.api = api
        self.path = path

    def metadata_init(self):
        """
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

    def get_data_ps(self):
        """
        """
        return self.data_PS
