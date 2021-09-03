import json
import os

from zoia_lib.backend import api
from zoia_lib.backend.patch import Patch
from zoia_lib.backend.patch_save import PatchSave
from zoia_lib.common import errors


class PatchUpdate(Patch):
    """The PatchUpdate class is a child of the Patch class. It is
    responsible for patch and patch note updating operations.
    """

    def __init__(self):
        """Initialize the class such that it has a reference to the
        backend path.
        """

        super().__init__()

    def update_data(self, idx, data, mode):
        """Attempts to modify data to a patches metadata.

        idx: The id for the patch metadata that is to be modified.
        tag: A string representing the tag that is to be added. Does not
             necessarily need to be a single tag.
        mode: The type of data that is being added. Valid modes are:
              - 1 -> Modify the tags
              - 2 -> Modify the categories
              - 3 -> Modify the patch notes
              - 4 -> Modify the author
              - 5 -> Modify the patch title
              - 6 -> Modify the rating
        """

        # Lookup the right term to use.
        index = {
            1: "tags",
            2: "categories",
            3: "content",
            4: "author",
            5: "title",
            6: "rating",
        }[mode]

        # Get the patch name and id.
        pch = idx
        idx = idx.split("_")[0]

        # Update the key with the new data.
        with open(os.path.join(self.back_path, idx, "{}.json".format(pch)), "r") as f:
            temp = json.loads(f.read())
        # if mode == 4:
        #    temp[index]["name"] = data
        temp[index] = data
        with open(os.path.join(self.back_path, idx, "{}.json".format(pch)), "w") as f:
            f.write(json.dumps(temp))

    def check_for_updates(self):
        """Upon startup, automatically retrieve the latest version of
        patches from PS, should any that have been previously downloaded
        are updated.

        This method will check the updated_at attribute of each
        downloaded patch, should this differ compared to what is
        returned by PS, a new patch will attempt to be saved. If the
        binary file is determined to be identical to the one stored
        within the backend, the saving is aborted at there was no update
        to the patch itself. Otherwise, a new version of the patch is
        added and saved within the patch directory.

        return: A tuple containing the number of patches that updated as
                an int as the first element, and the names of the
                patches that updated in as strings in an array as the
                second element.
        """

        meta = []

        for patch in os.listdir(self.back_path):
            # Only check for updates for patches hosted on PS
            # (denoted via the 6-digit ID numbers).
            # Exclude any special dirs in the backend.
            if (
                os.path.isdir(os.path.join(self.back_path, patch))
                and len(patch) > 5
                and patch != "Banks"
                and patch != "Folders"
                and patch != ".DS_Store"
            ):
                # Split on number of versions in the dir.
                if (
                    len(os.listdir(os.path.join(self.back_path, patch))) > 2
                ):
                    # Multiple versions, only need the latest.
                    with open(
                        os.path.join(self.back_path, patch, "{}_v1.json".format(patch)), "r"
                    ) as f:
                        temp = json.loads(f.read())
                else:
                    # Just a single patch in the directory, easy.
                    with open(
                        os.path.join(self.back_path, patch, "{}.json".format(patch)), "r"
                    ) as f:
                        temp = json.loads(f.read())
            else:
                continue
            # Only need the id and updated_at for comparison purposes.
            meta_small = {"id": temp["id"], "updated_at": temp["updated_at"]}
            meta.append(meta_small)

        # Get a list of binary/metadata for all files that have been updated
        # on PatchStorage.
        ps = api.PatchStorage()
        pch_list = ps.get_potential_updates(meta)

        # Try to save the new binaries to the backend.
        save = PatchSave()
        pchs = []
        for patch in pch_list:
            try:
                save.save_to_backend(patch[0])
            except errors.SavingError:
                # Same binary, but patch notes are different, update those.
                idx = str(patch[1]["id"])
                try:
                    with open(
                        os.path.join(self.back_path, idx, "{}.bin".format(idx)), "w"
                    ) as f:
                        f.write(json.dumps(patch[1]))
                        pchs.append(patch[1]["title"])
                except FileNotFoundError:
                    with open(
                        os.path.join(self.back_path, idx, "{}_v1.bin".format(idx)), "r"
                    ) as f:
                        f.write(json.dumps(patch[1]))
                        pchs.append(patch[1]["title"])
            pchs.append(patch)

        # Pass the number of updates and titles of patches updated.
        return len(pch_list), pchs
