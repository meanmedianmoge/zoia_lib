import json
import os
import shutil

from zoia_lib.backend.patch import Patch
from zoia_lib.backend.utilities import generate_blank_patch
from zoia_lib.common import errors


class PatchExport(Patch):
    """The PatchExport class is a child of the Patch class.
    It is responsible for all patch exporting operations.
    """

    def __init__(self):
        """Initialize the class such that it has a reference to the
        backend path.
        """

        super().__init__()

    def export_patch_bin(self, patch, dest, slot=-1, overwrite=False):
        """Attempts to export a patch from the application to the
        specified supplied path. Normally, this will be a user's SD
        card, but it could be used for a location on a user's machine
        as well.
        This method is specifically for the exporting of .bin patch
        files.

        patch: A string representing the patch that is to be exported.
               This does not need a file extension, but supplying one
               will not cause the method to fail.
        dest: A string representing the destination that the patch will
              be exported to.
        slot: Optional. If a patch is being exported to an SD card, set
              this to the desired slot that you wish to see the patch
              appear in on a ZOIA. Valid slot numbers are 0 - 63. Should
              the slot be negative, a slot identifier will not be added
              to the name.
        overwrite: Optional. This should be set to True when the export
                   will conflict with a file that is already in the
                   dest, but the user has specified that it is okay to
                   overwrite said file.

        raise: BadPathError if path did not lead to a file.
        raise: ExportingError if an invalid slot number is provided or
               shutil is unable to copy the file over to the dest.
        """

        # Check to see if there is already another patch with that slot #
        # in the destination.
        if not overwrite:
            for pch in os.listdir(dest):
                if pch[:3] == "00{}".format(slot) or pch[:3] == "0{}".format(slot):
                    name = pch[9:].split(".")[0].replace("_", " ").title()
                    raise errors.ExportingError(name, 703)
        else:
            # Delete the previous patch that occupied the slot.
            for pch in os.listdir(dest):
                if pch[:3] == "00{}".format(slot) or pch[:3] == "0{}".format(slot):
                    os.remove(os.path.join(dest, pch))
                    break

        # Prepare the name of the patch. We need to access the metadata.
        # Extract the patch id from the supplied patch parameter.
        patch = patch.split(".")[0]
        idx = patch.split(".")[0]
        idx = idx.split("_")[0]

        # Get the metadata for this patch.
        try:
            with open(
                os.path.join(self.back_path, idx, "{}.json".format(patch)), "r"
            ) as f:
                metadata = json.loads(f.read())
        except FileNotFoundError:
            raise errors.BadPathError(301)

        # Extract the filename attribute.
        name = metadata["files"][0]["filename"]
        # Check to see if the patch author included a ZOIA prefix.
        # (and drop it from the name).
        if "_" in name and len(name.split("_")[0]) == 3:
            try:
                float(name.split("_")[0])
                name = name[4:]
            except ValueError:
                pass
        try:
            if -1 < slot < 10:
                # one digit
                name = "00{}_".format(slot) + name
            elif slot >= 10 < 64:
                # two digits
                name = "0{}_".format(slot) + name
            elif slot < 0:
                # No slot, not going to an sd card, no need for digits.
                pass
            else:
                # Incorrect slot number provided.
                raise errors.ExportingError(slot, 701)
        except FileNotFoundError or FileExistsError:
            pass

        # Add the file extension if need be.
        if "." not in patch:
            patch += ".bin"

        # If the dest is not a directory, create one.
        if not os.path.isdir(dest):
            os.mkdir(dest)

        # Rename the patch and export.
        try:
            shutil.copy(
                os.path.join(self.back_path, idx, patch), os.path.join(dest, name)
            )
        except FileNotFoundError or FileExistsError:
            raise errors.ExportingError(patch)

    def export_bank(self, bank, dest, name, overwrite=False):
        """Exports an entire bank to be ready for use on a ZOIA.
        Ideally, this is used to export a bank from a local user's
        machine to an SD card.

        bank: The bank data to be processed.
        dest: A string representing the path to the backend destination.
        name: The name of the bank directory that will be created.
        overwrite: Optional. This should be set to True when the export
                   will conflict with a directory that is already in the
                   dest, but the user has specified that it is okay to
                   overwrite said file.

        return: An array of slot numbers for patches that failed to
                export.
        """

        fail_list = []

        # Prepare a destination directory (remove the previous if
        # overwrite is true).
        if overwrite and name in os.listdir(dest):
            shutil.rmtree(os.path.join(dest, name))
        os.mkdir(os.path.join(dest, name))

        # Process the bank and add each to the bank directory.
        for pch in bank:
            try:
                self.export_patch_bin(pch["id"], os.path.join(dest, name), pch["slot"])
            except errors.BadPathError:
                fail_list.append(pch["slot"])

        # If we failed to export any patches, remove the directory
        # we just created.
        if len(fail_list) == len(bank):
            os.rmdir(os.path.join(dest, name))
        else:
            # Fill in the empty slots, including ones which failed (if any).
            if len(bank) - len(fail_list) < 64:
                slots = sorted([pch["slot"] for pch in bank])
                empty = list(set([x for x in range(0, 64)]) - set(slots))
                empty = empty + fail_list

                for slot in empty:
                    try:
                        if -1 < slot < 10:
                            # one digit
                            blank_name = "00{}_zoia_.bin".format(slot)
                        elif slot >= 10 < 64:
                            # two digits
                            blank_name = "0{}_zoia_.bin".format(slot)
                        elif slot < 0:
                            # No slot, not going to an sd card, no need for digits.
                            pass
                        else:
                            # Incorrect slot number provided.
                            raise errors.ExportingError(slot, 701)
                    except FileNotFoundError or FileExistsError:
                        pass

                    with open(os.path.join(dest, name, blank_name), "wb") as f:
                        f.write(generate_blank_patch())

        return fail_list
