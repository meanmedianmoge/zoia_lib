import os
import shutil

from zoia_lib.backend.patch import Patch
from zoia_lib.common import errors


class PatchDelete(Patch):
    """The PatchDelete class is a child of the Patch class. It is
    responsible for patch deletion operations.
    """

    def __init__(self):
        """Initialize the class such that it has a reference to the
        backend path.
        """

        super().__init__()

    def delete_patch(self, patch):
        """Attempts to delete a patch and its metadata from
        the backend ZoiaLibraryApp directory.

        patch: A string representing the path to the patch to be
               deleted.

        raise: RenamingError if the file could not be renamed
               correctly.
        raise: BadPathError if patch was not a valid path.
        """

        if patch is None:
            raise errors.DeletionError(None)

        # Remove any file extension if it is included.
        if os.path.sep in patch:
            patch = patch.split(os.path.sep)[-1]
        patch = patch.split(".")[0]

        # Try to delete the file and metadata file.
        try:
            # Should the patch directory not exist, a BadPathError is raised.
            new_path = os.path.join(self.back_path, patch.split("_")[0])
            os.remove(os.path.join(new_path, patch + ".bin"))
            os.remove(os.path.join(new_path, patch + ".json"))
            if new_path is not None and len(os.listdir(new_path)) == 2:
                # If there aren't multiple patches left, drop the version
                # extension on the remaining patch.
                for left_files in os.listdir(new_path):
                    try:
                        os.rename(
                            os.path.join(new_path, left_files),
                            os.path.join(
                                new_path,
                                "{}.{}".format(
                                    left_files.split("_")[0], left_files.split(".")[-1]
                                ),
                            ),
                        )
                    except FileNotFoundError or FileExistsError:
                        raise errors.RenamingError(left_files, 601)
            elif new_path is not None and len(os.listdir(new_path)) == 0:
                # Special case: There are no more patches left in the
                # patch directory. As such, the directory should be removed.
                os.rmdir(new_path)
        except FileNotFoundError:
            raise errors.BadPathError(patch, 301)

    def delete_full_patch_directory(self, patch_dir):
        """Forces the deletion of an entire patch directory, should
        one exist.

        Please note that this method will not attempt to correct invalid
        input. Please ensure that the patch parameter is exclusively the
        name of the patch directory that will be deleted.

        patch_dir: A string representing the patch directory to be deleted.

        raise: DeletionError if patch_dir is malformed.
        raise: BadPathError if patch_dir does not lead to a patch.
        """

        if patch_dir is None:
            raise errors.DeletionError(None)

        try:
            shutil.rmtree(os.path.join(self.back_path, patch_dir))
        except FileNotFoundError:
            # Couldn't find the patch directory that was passed.
            raise errors.BadPathError(patch_dir, 301)

    @staticmethod
    def delete_patch_sd(index, sd_path):
        """Attempts to delete a patch located on an inserted SD card.

        This method relies on the user leaving the SD card inserted
        while the deletion occurs. Otherwise, corruption is likely
        to occur. In such situations, either a DeletionError, or
        BadPathError may be raised.

        index: The index number that will be searched for among the
               patches currently present in the supplied sd_path. Should
               a patch be found that matches the passed index, it will
               be deleted.
        sd_path: A string representing the path to the inserted SD card.

        raise: BadPatchError if path does not lead to a patch.
        raise: DeletionError if patch_dir is malformed, cannot find a
               a patch to delete, or the SD card is removed during
               deletion.
        """

        if sd_path is None:
            raise errors.DeletionError(None)

        if len(index) != 3:
            raise errors.DeletionError(index, 404)

        # Delete the patch.
        try:
            for pch in os.listdir(sd_path):
                if pch[:3] == index:
                    os.remove(os.path.join(sd_path, pch))
                    break
        except FileNotFoundError:
            # Couldn't find the patch at the supplied path.
            raise errors.BadPathError(sd_path, 301)

    @staticmethod
    def delete_file(path):
        """Deletes a file at the specified path.

        path: The path at which the file to be deleted is located.

        raise: BadPathError if path did not lead to a file.
        """

        # Delete the patch.
        try:
            os.remove(path)
        except FileNotFoundError:
            # Couldn't find the file at the supplied path.
            raise errors.BadPathError(path, 301)
