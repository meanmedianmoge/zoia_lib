import json
import os
import platform
import zipfile
from pathlib import Path

import zoia_lib.backend.api as api
import zoia_lib.common.errors as errors

# Global variable to avoid the rerunning of determine_backend_path() unnecessarily.
backend_path = None
ps = api.PatchStorage()


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


def patch_decompress(patch):
    """ Method stub for decompressing files retrieved from the PS
    API. Should be expanded to work with files imported into the
    application and should correctly update the metadata for each
    based on the date modified of each file. (Newest version should
    be the .bin file with the most recent date modified).

    patch: A tuple containing the downloaded file
           data and the patch metadata, comes from ps.download(IDX).
           patch[0] is raw binary data, while patch[1] is json data.
    """
    # No need to determine it again if we have done so before.
    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    patch_name = str(patch[1]['id'])

    pch = os.path.join(backend_path, "{}".format(str(patch_name)))
    if not os.path.isdir(pch):
        os.mkdir(pch)

    if patch[1]["files"][0]["filename"].split(".")[1] == "zip":
        # .zip files
        name_zip = os.path.join(pch, "{}.zip".format(patch_name))
        f = open(name_zip, "wb")
        f.write(patch[0])
        f.close()
        with zipfile.ZipFile(os.path.join(pch, "{}.zip".format(patch_name)), 'r') as zipObj:
            # Extract all the contents into the patch directory
            zipObj.extractall(pch)
        # Ditch the zip
        os.remove(name_zip)
        i = 0
        for file in os.listdir(pch):
            if file.split(".")[1] == "bin":
                i += 1
                # Rename the file to follow the conventional format
                # TODO Change this rename the file based on the date modified.
                os.rename(os.path.join(pch, file),
                          os.path.join(pch, "{}_v{}.bin".format(patch[1]["id"], i)))
                patch[1]["revision"] = str(i)
                save_metadata_json(patch, i)
    else:
        # Unexpected file extension encountered.
        # TODO Handle this case gracefully.
        raise errors.SavingError(patch[1]["title"])


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

    if isinstance(patch[0], bytes) and patch[1]["files"][0]["filename"].split(".")[1] == "bin":
        name_bin = os.path.join(pch, "{}.bin".format(patch_name))
        f = open(name_bin, "wb")
        f.write(patch[0])
        f.close()
        save_metadata_json(patch)
    else:
        # Might be a compressed file.
        patch_decompress(patch)


def save_metadata_json(patch, version=0):
    """ Method stub for saving metadata. Should be expanded to work
    for patches that do not originate from the PS API.

    patch: A tuple containing the downloaded file
           data and the patch metadata, comes from ps.download(IDX).
           patch[0] is raw binary data, while patch[1] is json data.
    version: Optional. If the patch needs a version suffix, this parameter
             should be set to the appropriate version number. Valid version
             numbers are > 0.
    """
    # No need to determine it again if we have done so before.
    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()
    # Save the metadata.
    if version == 0:
        name_json = os.path.join(backend_path, str(patch[1]['id']), "{}.json".format(patch[1]["id"]))
    else:
        name_json = os.path.join(backend_path, str(patch[1]['id']), "{}_v{}.json".format(patch[1]["id"], version))
    jf = open(name_json, "w")
    json.dump(patch[1], jf)
    jf.close()


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
