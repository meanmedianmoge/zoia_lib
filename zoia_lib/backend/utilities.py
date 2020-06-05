import json
import os
import pathlib
import platform
from pathlib import Path

import zoia_lib.common.errors as errors
from zoia_lib.backend.api import PatchStorage

ps = PatchStorage()
backend_path = None


def determine_backend_path():
    global backend_path
    if backend_path is None:
        curr_os = platform.system()
        if curr_os == "Windows":
            backend_path = os.getenv('APPDATA') + "\\.LibraryApp"
        elif curr_os == "Darwin":
            backend_path = pathlib.Path.home() / "Library\\Application Support\\.LibraryApp"
        elif curr_os == "Linux":
            backend_path = pathlib.Path.home() / ".local\\share\\.LibraryApp"
        else:
            # Solaris/Chrome OS/Java OS?
            backend_path = None

    return backend_path


def save_to_backend(patch):
    """Attempts to save a simple binary patch and its metadata
    to the backend LibraryApp directory.

    patch: A tuple containing the downloaded file
           data and the patch metadata.
    """
    global backend_path
    if backend_path is None:
        determine_backend_path()

    # Don't try to save a file when we are missing necessary information.
    if patch is None or patch[0] is None or patch[1] is None or backend_path is None:
        raise errors.SavingError()

    try:
        # Ensure that the data is in valid json format.
        json.dumps(patch[1])
    except ValueError:
        raise errors.SavingError()

    patch_name = str(patch[1]['id'])

    if isinstance(patch[0], bytes):
        name_bin = Path(backend_path + "\\" + patch_name + ".bin")
        f = open(name_bin, "wb")
        f.write(patch[0])
        f.close()
        name_json = Path(backend_path + "\\" + patch_name + ".json")
        jf = open(name_json, "w")
        json.dump(patch[1], jf)
        jf.close()
    # TODO implement the compressed file format case.


def delete_patch(patch):
    """Attempts to delete a patch and its metadata from
    the backend LibraryApp directory.

    patch: A string representing the patch to be deleted.
    """
    global backend_path
    if backend_path is None:
        determine_backend_path()

    if patch is None:
        raise errors.DeletionError(None)

    # Remove any file extension if it is included.
    patch = patch.split(".")[0]

    new_path = None

    # Check if the file to be deleted is in a version directory.
    patch_no_version = patch.split("_")[0]
    for file in os.listdir(backend_path):
        if file == patch_no_version:
            # We have hit a version directory.
            new_path = Path(backend_path + "\\" + file)
            break

    # Try to delete the file and metadata file.
    try:
        real_path = new_path if new_path is not None else backend_path
        os.remove(Path(str(real_path) + "\\" + patch + ".bin"))
        os.remove(Path(str(real_path) + "\\" + patch + ".json"))
        """ Special case: Deletion from a version directory. Need to check if
        the version directory only contains one patch, and if so, move the
        patch and metadata (also remove the version suffix) and delete the 
        version directory for said patch.
        """
        if new_path is not None and len(os.listdir(new_path)) <= 2:
            for left_files in os.listdir(new_path):
                try:
                    front = left_files.split("_")[0]
                    end = left_files.split(".")[1]
                    os.rename(Path(str(new_path) + "\\" + left_files),
                              Path(str(backend_path) + "\\" + front + "." + end))
                except FileNotFoundError:
                    raise errors.RenamingError(left_files)
            os.rmdir(new_path)

    except FileNotFoundError:
        raise errors.DeletionError(patch)
