import json
import os
import platform
from pathlib import Path

import zoia_lib.common.errors as errors
from zoia_lib.backend.api import PatchStorage

# Global variable to avoid the rerunning of determine_backend_path() unnecessarily.
backend_path = None
ps = PatchStorage()


def create_backend_directories():
    """ Creates the necessary directories that will
    store patch files, bank files, and metadata files.
    """
    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    # Prevent an error on Windows by checking to see if the directory already exists.
    if backend_path is not None and not os.path.exists(backend_path):
        os.mkdir(backend_path)
        os.mkdir(str(Path(backend_path + "/Banks")))


def determine_backend_path():
    """ Creates the appropriate backend directories
    for the application depending on the OS.
    """
    curr_os = platform.system()
    if curr_os == "Windows":
        back_path = os.path.join(os.getenv('APPDATA'), ".ZoiaLibraryApp")
    elif curr_os == "Darwin":
        back_path = os.path.join(str(Path.home()), "Library", "Application Support", ".ZoiaLibraryApp")
    elif curr_os == "Linux":
        back_path = os.path.join(str(Path.home()), ".local", "share", ".ZoiaLibraryApp")
    else:
        # Solaris/Chrome OS/Java OS?
        back_path = None

    return back_path


def save_to_backend(patch):
    """Attempts to save a simple binary patch and its metadata
    to the backend ZoiaLibraryApp directory.

    patch: A tuple containing the downloaded file
           data and the patch metadata, comes from ps.download(IDX).
           patch[0] is raw binary data, while patch[1] is json data.
    """
    # No need to determine it again if we have done so before.
    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    # Don't try to save a file when we are missing necessary information.
    if patch is None or patch[0] is None or patch[1] is None or backend_path is None \
            or not isinstance(patch[0], bytes) or not isinstance(patch[1], dict):
        raise errors.SavingError(patch)

    try:
        # Ensure that the data is in valid json format.
        json.dumps(patch[1])
    except ValueError:
        raise errors.SavingError(patch)

    patch_name = str(patch[1]['id'])
    pch = os.path.join(backend_path, "{}".format(patch_name))
    if not os.path.isdir(pch):
        os.mkdir(pch)

    if isinstance(patch[0], bytes):
        name_bin = os.path.join(backend_path, "{}.bin".format(patch_name))
        f = open(name_bin, "wb")
        f.write(patch[0])
        f.close()
        name_json = os.path.join(backend_path, "{}.json".format(patch_name))
        jf = open(name_json, "w")
        json.dump(patch[1], jf)
        jf.close()
    # TODO implement the compressed file format case.


def add_test_patch(name, idx):
    """Note: This method is for testing purposes
    and will be deleted once a release candidate
    is prepared.

    Adds a test patch that can be used for unit
    testing purposes.
    """
    # No need to determine it again if we have done so before.
    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    if os.path.sep in name:
        dr, name = name.split(os.path.sep)
        pch = os.path.join(backend_path, "{}".format(dr))
    else:
        pch = os.path.join(backend_path, "{}".format(name))

    if not os.path.isdir(pch):
        os.mkdir(pch)

    name_bin = os.path.join(pch, "{}.bin".format(name))
    f2 = open(name_bin, "wb")
    f2.write(b"Test")
    f2.close()
    name_json = os.path.join(pch, "{}.json".format(name))
    jf2 = open(name_json, "w")
    json.dump({"id": idx, "title": "Test", "created_at": "test"}, jf2)
    jf2.close()


def delete_patch(patch):
    """Attempts to delete a patch and its metadata from
    the backend ZoiaLibraryApp directory.

    patch: A string representing the patch to be deleted.
    """
    # No need to determine it again if we have done so before.
    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    if patch is None:
        raise errors.DeletionError(None)

    # Remove any file extension if it is included.
    if os.path.sep in patch:
        dr, patch = patch.split(os.path.sep)
    patch = patch.split(".")[0]

    # Try to delete the file and metadata file.
    try:
        # Should the patch directory not exist, a DeletionError is raised.
        new_path = os.path.join(backend_path, patch.split("_")[0])
        os.remove(os.path.join(new_path, patch + ".bin"))
        os.remove(os.path.join(new_path, patch + ".json"))
        if new_path is not None and len(os.listdir(new_path)) == 2:
            """ Special case: Deletion from a patch directory. Need to check if
            the patch directory only contains one patch, and if so, remove the 
            version suffix.
            """
            for left_files in os.listdir(new_path):
                try:
                    front = left_files.split("_")[0]
                    end = left_files.split(".")[1]
                    os.rename(os.path.join(new_path, left_files),
                              os.path.join(new_path, "{}.{}".format(front, end)))
                except FileNotFoundError:
                    raise errors.RenamingError(left_files)
        elif new_path is not None and len(os.listdir(new_path)) == 0:
            """ Special case: There are no more patches left in the patch
            directory. As such, the directory should be removed. 
            """
            os.rmdir(new_path)
    except FileNotFoundError:
        raise errors.DeletionError(patch)
