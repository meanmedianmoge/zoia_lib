import datetime
import json
import os
import platform
import random
import shutil
import zipfile
from pathlib import Path

import zoia_lib.common.errors as errors

# Global variable to avoid the rerunning of
# determine_backend_path() unnecessarily.
backend_path = None


def create_backend_directories():
    """ Creates the necessary directories that will
    store patch files, bank files, and metadata files.
    """

    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    # Prevent an error on Windows by checking to see
    # if the directory already exists.
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
        back_path = os.path.join(str(Path.home()), "Library",
                                 "Application Support", ".ZoiaLibraryApp")
    elif curr_os == "Linux":
        back_path = os.path.join(str(Path.home()), ".local", "share",
                                 ".ZoiaLibraryApp")
    else:
        # Solaris/Chrome OS/Java OS?
        back_path = None

    return back_path


def patch_decompress(patch):
    """ Method stub for decompressing files retrieved from the PS API.

    patch: A tuple containing the downloaded file
           data and the patch metadata, comes from ps.download(IDX).
           patch[0] is raw binary data, while patch[1] is json data.
    Raises a SavingError should the contents fail to save.
    Raises a RenamingError should the contents fail to be renamed.
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
        with open(name_zip, "wb") as f:
            f.write(patch[0])
        with zipfile.ZipFile(os.path.join(pch, "{}.zip".format(patch_name)),
                             'r') as zipObj:
            # Extract all the contents into the patch directory
            zipObj.extractall(pch)
        # Ditch the zip
        os.remove(name_zip)
        i = 0
        for file in os.listdir(pch):
            if file.split(".")[1] == "bin":
                i += 1
                try:
                    # Rename the file to follow the conventional format
                    # TODO Change this to rename the file based on the
                    #  date modified.
                    os.rename(os.path.join(pch, file),
                              os.path.join(pch, "{}_v{}.bin".format(
                                  patch[1]["id"], i)))
                    save_metadata_json(patch[1], i)
                except FileNotFoundError or FileExistsError:
                    raise errors.RenamingError(patch, 601)
            else:
                # Remove any additional files.
                # TODO make this better. Shouldn't just delete
                #  additional files.
                os.remove(os.path.join(pch, file))
    else:
        # Unexpected file extension encountered.
        # TODO Handle this case gracefully.
        raise errors.SavingError(patch[1]["title"], 501)


def import_to_backend(path):
    """Attempts to import a patch to the backend
    ZoiaLibraryApp directory. This method is meant to work
    for patches that originate from a local user's machine,
    or from a ZOIA formatted SD card.

    Base metadata will be created from the available information
    of the patch, mostly derived of the name and any additional
    information that can be ascertained.

    path: The filepath that leads to the local patch that is
          being imported.
    Raises a SavingError should the patch fail to save.
    """

    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    if path is None:
        raise errors.SavingError(None)

    # Get the file extension for the patch that is being imported.
    if "." not in path:
        raise errors.SavingError(path)
    patch_name, ext = path.split(".")
    patch_name = patch_name.split("/")[-1]
    # Generate a random patch ID to use (must be 5 digits).
    while True:
        patch_id = str(random.randint(10000, 99999))
        if patch_id not in os.listdir(backend_path):
            break
    if "_zoia_" in patch_name:
        patch_name = patch_name.split("_zoia_")[1]
    # Binary file, easiest case.
    # Get the bytes.
    with open(path, "rb") as f:
        temp_data = f.read()
    # Prepare the JSON.
    js_data = {
        "id": patch_id,
        "created_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
            datetime.datetime.now()),
        "updated_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
            datetime.datetime.now()),
        "title": patch_name,
        "revision": "1",
        "files": [
            {
                "id": patch_id,
                "filename": patch_name + "." + ext
            }
        ]
    }
    # Try to save the patch.
    save_to_backend((temp_data, js_data))


def save_to_backend(patch):
    """Attempts to save a simple binary patch and its metadata
    to the backend ZoiaLibraryApp directory. This method is meant
    to work for patches retrieved via the PS API. As such, it should
    only be called with the returned output from download() located
    in api.py. Other input will most likely case a SavingError.

    For local patch importing, see import_to_backend().

    patch: A tuple containing the downloaded file
           data and the patch metadata, comes from ps.download(IDX).
           patch[0] is raw binary data, while patch[1] is json data.
    Raises a SavingError should the patch fail to save.
    Raises a RenamingError should the patch fail to be renamed.
    """

    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    # Don't try to save a file when we are missing necessary info.
    if patch is None or patch[0] is None \
            or patch[1] is None or backend_path is None \
            or not isinstance(patch[0], bytes) \
            or not isinstance(patch[1], dict):
        raise errors.SavingError(None)

    try:
        # Ensure that the data is in valid json format.
        json.dumps(patch[1])
    except ValueError:
        raise errors.SavingError(patch[1]["title"], 502)

    pch_id = str(patch[1]['id'])
    pch = os.path.join(backend_path, "{}".format(pch_id))
    # Check to see if a directory needs to be made (new patch,
    # no version control needed yet).
    if not os.path.isdir(pch):
        os.mkdir(pch)
        if "files" in patch[1] \
                and patch[1]["files"][0]["filename"].split(".")[1] != "bin":
            # If it isn't a straight bin additional work must be done.
            patch_decompress(patch)
        # Make sure the files attribute exists.
        elif "files" in patch[1] and isinstance(patch[0], bytes):
            name_bin = os.path.join(pch, "{}.bin".format(pch_id))
            with open(name_bin, "wb") as f:
                f.write(patch[0])
            save_metadata_json(patch[1])
        else:
            # No files attribute,
            raise errors.SavingError(patch[1]["title"], 503)
    else:
        """ A directory already existed for this patch id, so 
        we need to check if this is a unique patch version 
        (otherwise there is no need to save it).
        """
        # Case 1: Check if this is a compressed patch download.
        if "files" in patch[1] \
                and patch[1]["files"][0]["filename"].split(".")[1] != "bin":
            # We need to check the individual binary files to see which,
            # if any, differ from the ones currently stored.

            # Figure out which file compression is being used.
            if patch[1]["files"][0]["filename"].split(".")[1] == "zip":
                # Create a temporary directory to store
                # the extracted files.
                os.mkdir(os.path.join(backend_path, "temp"))
                # Write the zip
                zfile = os.path.join(backend_path, "temp.zip")
                with open(zfile, "wb") as zf:
                    zf.write(patch[0])
                with zipfile.ZipFile(zfile, 'r') as zipObj:
                    # Extract all the contents into the temporary directory.
                    zipObj.extractall(os.path.join(backend_path, "temp"))
                # Ditch the zip
                os.remove(zfile)
                # For each binary file, call the method again
                # and see if the data has been changed.
                diff = False
                for file in os.listdir(os.path.join(backend_path, "temp")):
                    try:
                        # We only care about .bin files.
                        if file.split(".")[1] == "bin":
                            with open(file, "rb") as bin_file:
                                raw_bin = bin_file.read()
                            save_to_backend((raw_bin, patch[1]))
                            diff = True
                    except FileNotFoundError or errors.SavingError:
                        pass
                # Cleanup and finish.
                shutil.rmtree(os.path.join(backend_path, "temp"))
                if not diff:
                    # No files changed, so we should raise a SavingError
                    raise errors.SavingError(patch[1]["title"], 504)
                return
            else:
                # TODO Cover the other compression cases.
                raise errors.SavingError(patch[1]["title"])

        # If we get here, we are working with a .bin, so we
        # need to to see if the binary is already saved.
        for file in os.listdir(os.path.join(pch)):
            if file.split(".")[1] == "bin":
                with open(os.path.join(pch, file), "rb") as f:
                    if f.read() == patch[0]:
                        # This exact binary is already saved onto the system.
                        raise errors.SavingError(patch[1]["title"], 504)
                f.close()

        # If we get here, we have a unique patch, so we need to find
        # out what version # to give it.

        # Case 2: Only one version of the  patch  existed previously.
        if len(os.listdir(os.path.join(backend_path, pch))) == 2:
            name_bin = os.path.join(pch, "{}_v1.bin".format(pch_id))
            with open(name_bin, "wb") as f:
                f.write(patch[0])
            save_metadata_json(patch[1], 1)
            try:
                os.rename(os.path.join(pch, "{}.bin".format(pch_id)),
                          os.path.join(pch, "{}_v2.bin".format(pch_id)))
                os.rename(os.path.join(pch, "{}.json".format(pch_id)),
                          os.path.join(pch, "{}_v2.json".format(pch_id)))
            except FileNotFoundError or FileExistsError:
                raise errors.RenamingError(patch, 601)
            with open(os.path.join(pch, "{}_v2.json".format(pch_id)),
                      "r") as f:
                jf = json.loads(f.read())
            jf["revision"] = 2
            with open(os.path.join(pch, "{}_v2.json".format(pch_id)),
                      "w") as f:
                json.dump(jf, f)
        # Case 3: There were already multiple versions in the patch directory.
        elif len(os.listdir(os.path.join(backend_path, pch))) > 2:
            # Increment the version number for each file in the directory.
            try:
                for file in reversed(sorted(os.listdir(os.path.join(pch)))):
                    ver = int(file.split("v")[1].split(".")[0]) + 1
                    extension = file.split(".")[1]
                    os.rename(os.path.join(pch, "{}_v{}.{}".format(pch_id,
                                                                   str(ver
                                                                       - 1),
                                                                   extension)),
                              os.path.join(pch, "{}_v{}.{}".format(pch_id,
                                                                   str(ver),
                                                                   extension)))
                    # Update the revision number in each metadata file
                    with open(os.path.join(pch,
                                           "{}_v{}.json".format(pch_id,
                                                                str(ver))),
                              "r") as f:
                        jf = json.loads(f.read())

                    jf["revision"] = ver

                    with open(os.path.join(pch,
                                           "{}_v{}.json".format(pch_id,
                                                                str(ver))),
                              "w") as f:
                        json.dump(jf, f)

            except FileNotFoundError or FileExistsError:
                raise errors.SavingError(patch)
            # Save the newest version
            name_bin = os.path.join(pch, "{}_v1.bin".format(pch_id))
            with open(name_bin, "wb") as f:
                f.write(patch[0])
            save_metadata_json(patch[1], 1)
        else:
            """ Getting here indicates that the amount of files in the 
            directory was less than 2 (which would imply some form of 
            corruption occurred). 
            """
            raise errors.SavingError(patch[1]["title"])


def save_metadata_json(metadata, version=0):
    """ Method stub for saving metadata. Should be expanded to work
    for patches that do not originate from the PS API.

    metadata: A string containing the JSON data that will be used for
              the metadata file that is being created.
    version: Optional. If the patch needs a version suffix, this
             parameter should be set to the appropriate version number.
             Valid version numbers are > 0.
    """

    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    # Save the metadata.
    if version <= 0:
        name_json = os.path.join(backend_path, str(metadata['id']),
                                 "{}.json".format(metadata["id"]))
    else:
        name_json = os.path.join(backend_path, str(metadata['id']),
                                 "{}_v{}.json".format(metadata["id"], version))

    # Update the revision number if need be.
    if version > 0:
        metadata["revision"] = version

    with open(name_json, "w") as jf:
        json.dump(metadata, jf)


def add_test_patch(name, idx):
    """Note: This method is for testing purposes
    and will be deleted once a release candidate
    is prepared.

    Adds a test patch that can be used for unit
    testing purposes.

    name: The name of the patch, to be used for the title attribute
          in the JSON metadata.
    idx: The id number to be used for the patch.
    """

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
    with open(name_bin, "wb") as f:
        f.write(b"Test")
    name_json = os.path.join(pch, "{}.json".format(name))
    with open(name_json, "w") as jf:
        json.dump({"id": idx, "title": "Test", "created_at": "test"}, jf)


def delete_patch(patch):
    """Attempts to delete a patch and its metadata from
    the backend ZoiaLibraryApp directory.

    patch: A string representing the patch to be deleted.
    Raises a RenamingError if the file could not be renamed correctly.
    Raises a BadPathError if patch was not a valid path.
    """

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
        # Should the patch directory not exist,
        # a BadPathError is raised.
        new_path = os.path.join(backend_path, patch.split("_")[0])
        os.remove(os.path.join(new_path, patch + ".bin"))
        os.remove(os.path.join(new_path, patch + ".json"))
        if new_path is not None and len(os.listdir(new_path)) == 2:
            """ Special case: Deletion from a patch directory. Need to 
            check if the patch directory only contains one patch, and if 
            so, remove the version suffix.
            """
            for left_files in os.listdir(new_path):
                try:
                    front = left_files.split("_")[0]
                    end = left_files.split(".")[1]
                    os.rename(os.path.join(new_path, left_files),
                              os.path.join(new_path,
                                           "{}.{}".format(front, end)))
                except FileNotFoundError or FileExistsError:
                    raise errors.RenamingError(left_files, 601)
        elif new_path is not None and len(os.listdir(new_path)) == 0:
            # Special case: There are no more patches left in the
            # patch directory. As such, the directory should be removed.
            os.rmdir(new_path)
    except FileNotFoundError:
        raise errors.BadPathError(patch, 301)


def delete_full_patch_directory(patch_dir):
    """ Forces the deletion of an entire patch directory, should
    one exist.
    Please note that this method will not attempt to correct invalid
    input. Please ensure that the patch parameter is exclusively the
    name of the patch directory that will be deleted.

    patch_dir: A string representing the patch directory to be deleted.
    Raises a DeletionError if patch_dir is malformed.
    Raises a BadPathError if patch_dir does not lead to a patch.
    """

    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    if patch_dir is None:
        raise errors.DeletionError(None)

    if len(patch_dir.split(".")) > 1:
        # There shouldn't be a file extension.
        raise errors.DeletionError(patch_dir, 401)
    if len(patch_dir.split("_")) > 1:
        # There shouldn't be a version extension.
        raise errors.DeletionError(patch_dir, 402)

    try:
        shutil.rmtree(os.path.join(backend_path, patch_dir))
    except FileNotFoundError:
        # Couldn't find the patch directory that was passed.
        raise errors.BadPathError(patch_dir, 301)


def delete_patch_sd(path):
    """ Attempts to delete a patch located on an inserted, ZOIA
    formatted, SD card.

    This method relies on the user leaving the SD card inserted
    while the deletion occurs. Otherwise, corruption is likely
    to occur.

    path: A string representing the path to the patch on the inserted
          SD card. This path must include the name of the file to be
          deleted, otherwise the method will not know which file to
          delete and a DeletionError will be raised.
    Raises BadPatchError if path does not lead to a patch.
    Raises a DeletionError if patch_dir is malformed, cannot find a
    a patch to delete, or the SD card is removed during deletion.
    """

    global backend_path
    if backend_path is None:
        backend_path = determine_backend_path()

    if path is None:
        raise errors.DeletionError(None)

    if not len(path.split(".")) > 1:
        # There should be a file extension.
        raise errors.DeletionError(path, 403)

    # Delete the patch.
    try:
        os.remove(path)
    except FileNotFoundError:
        # Couldn't find the patch at the supplied path.
        raise errors.BadPathError(path, 301)
