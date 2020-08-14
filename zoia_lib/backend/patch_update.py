import json
import os

from zoia_lib.backend import api
from zoia_lib.backend.patch import Patch
from zoia_lib.backend.patch_save import PatchSave
from zoia_lib.common import errors


class PatchUpdate(Patch):
    """ The PatchUpdate class is a child of the Patch class. It is
    responsible for patch and patch note updating operations.
    """

    def __init__(self):
        """ Initialize the class such that it has a reference to the
        backend path.
        """

        super().__init__()

    def update_data(self, idx, data, mode):
        """ Attempts to modify data to a patches metadata.

        idx: The id for the patch metadata that is to be modified.
        tag: A string representing the tag that is to be added. Does not
             necessarily need to be a single tag.
        mode: The type of data that is being added. Valid modes are:
              - 1 -> Modify the tags
              - 2 -> Modify the categories
              - 3 -> Modify the patch notes
        """

        index = {
            1: "tags",
            2: "categories",
            3: "content"
        }[mode]

        pch = idx
        if "_" in idx:
            idx = idx.split("_")[0]

        with open(os.path.join(self.back_path, idx, "{}.json".format(pch)),
                  "r") as f:
            temp = json.loads(f.read())
        temp[index] = data
        with open(os.path.join(self.back_path, idx, "{}.json".format(pch)),
                  "w") as f:
            f.write(json.dumps(temp))

    def check_for_updates(self):
        """ Upon startup, automatically retrieve the latest version of
        patches from PS, should any that have been previously downloaded
        are updated.

        This method will check the updated_at attribute of each downloaded
        patch, should this differ compared to what is returned by PS, a
        new patch will attempt to be saved. If the binary file is determined
        to be identical to the one stored within the backend, the saving is
        aborted at there was no update to the patch itself. Otherwise, a new
        version of the patch is added and saved within the patch directory.
        """

        meta = []

        for patch in os.listdir(self.back_path):
            # Only check for updates for patches hosted on PS
            # (denoted via the 6-digit ID numbers).
            if os.path.isdir(os.path.join(self.back_path, patch)) \
                    and len(patch) > 5 \
                    and len(
                os.listdir(os.path.join(self.back_path, patch))) > 2 \
                    and patch != "Banks" and patch != ".DS_Store":
                # Multiple versions, only need the latest.
                with open(os.path.join(self.back_path, patch,
                                       "{}_v1.json".format(patch)), "r") as f:
                    temp = json.loads(f.read())
            elif os.path.isdir(os.path.join(self.back_path, patch)) \
                    and len(patch) > 5:
                with open(os.path.join(self.back_path, patch,
                                       "{}.json".format(patch)), "r") as f:
                    temp = json.loads(f.read())
            else:
                continue
            meta_small = {
                "id": temp["id"],
                "updated_at": temp["updated_at"]
            }
            meta.append(meta_small)

        # Get a list of binary/metadata for all files that have been updated
        # on PatchStorage.
        ps = api.PatchStorage()
        pch_list = ps.get_potential_updates(meta)

        # Try to save the new binaries to the backend.
        save = PatchSave()
        for patch in pch_list:
            try:
                save.save_to_backend(patch[0])
            except errors.SavingError:
                # TODO If we fail to save, at least update the metadata.
                try:
                    with open(os.path.join(self.back_path, str(patch[1]["id"]),
                                           "{}.bin".format(
                                               str(patch[1]["id"]))),
                              "w") as f:
                        f.write(json.dumps(patch[1]))
                except FileNotFoundError:
                    with open(os.path.join(
                            self.back_path, str(patch[1]["id"]),
                                           "{}_v1.bin".format(
                                               str(patch[1]["id"]))),
                              "r") as f:
                        f.write(json.dumps(patch[1]))

        return len(pch_list)
