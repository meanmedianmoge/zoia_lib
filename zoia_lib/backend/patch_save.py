import datetime
import json
import os
import shutil
import zipfile

from zoia_lib.backend.patch import Patch
from zoia_lib.common import errors
from zoia_lib.backend.api import PatchStorage

ps = PatchStorage()


class PatchSave(Patch):
    """ The PatchSave class is a child of the Patch class. It is
    responsible for patch importing, saving, and decompressing.
    """

    def __init__(self):
        """ Initialize the class such that it has a reference to the
        backend path.
        """

        super().__init__()

    def save_to_backend(self, patch):
        """Attempts to save a simple binary patch and its metadata
        to the backend ZoiaLibraryApp directory. This method is meant
        to work for patches retrieved via the PS API. As such, it should
        only be called with the returned output from download() located
        in api.py. Other input will most likely cause a SavingError.

        For local patch importing, see import_to_backend().

        patch: A tuple containing the downloaded file
               data and the patch metadata, comes from ps.download(IDX).
               patch[0] is raw binary data, while patch[1] is json data.
        Raises a SavingError should the patch fail to save.
        Raises a RenamingError should the patch fail to be renamed.
        """

        # Don't try to save a file when we are missing necessary info.
        if patch is None or patch[0] is None \
                or patch[1] is None or self.back_path is None \
                or not isinstance(patch[0], bytes) \
                or not isinstance(patch[1], dict):
            raise errors.SavingError(None)

        try:
            # Ensure that the data is in valid json format.
            json.dumps(patch[1])
        except ValueError:
            raise errors.JSONError(patch[1], 801)

        pch_id = str(patch[1]['id'])
        if len(pch_id) == 5:
            # This is an imported patch. Unfortunately, we need to make sure
            # that its a unique binary by checking every patch currently
            # stored. TODO Use binary analysis to improve this process.
            for direc in os.listdir(self.back_path):
                if os.path.isdir(os.path.join(self.back_path, direc)) \
                        and direc != "Banks" and direc != "sample_files" \
                        and direc != ".DS_Store":
                    for files in os.listdir(
                            os.path.join(self.back_path, direc)):
                        if files.split(".")[1] == "bin":
                            with open(os.path.join(
                                    self.back_path, direc, files), "rb") as f:
                                data = f.read()
                            if patch[0] == data:
                                raise errors.SavingError(patch[1]["title"],
                                                         503)
        pch = os.path.join(self.back_path, "{}".format(pch_id))
        # Check to see if a directory needs to be made
        # (new patch, no version control needed yet).
        if not os.path.isdir(pch):
            os.mkdir(pch)
            if "files" in patch[1] \
                    and patch[1]["files"][0]["filename"].split(".")[
                1] != "bin":
                # If it isn't a straight bin additional work must be done.
                if patch[1]["files"][0]["filename"].split(".")[1] == "py":
                    # We are not responsible for .py files.
                    shutil.rmtree(os.path.join(self.back_path, pch))
                    raise errors.SavingError(patch[1], 501)
                else:
                    self.patch_decompress(patch)
            # Make sure the files attribute exists.
            elif "files" in patch[1] and isinstance(patch[0], bytes):
                name_bin = os.path.join(pch, "{}.bin".format(pch_id))
                with open(name_bin, "wb") as f:
                    f.write(patch[0])
                self.save_metadata_json(patch[1])
            else:
                # No files attribute,
                raise errors.SavingError(patch[1], 502)
        else:
            """ A directory already existed for this patch id, so 
            we need to check if this is a unique patch version 
            (otherwise there is no need to save it).
            """
            # Case 1: Check if this is a compressed patch download.
            if "files" in patch[1] \
                    and patch[1]["files"][0]["filename"].split(".")[1] \
                    != "bin":
                # We need to check the individual binary files to see which,
                # if any, differ from the ones currently stored.

                # Figure out which file compression is being used.
                if patch[1]["files"][0]["filename"].split(".")[1] == "zip":
                    # Create a temporary directory to store
                    # the extracted files.
                    os.mkdir(os.path.join(self.back_path, "temp"))
                    # Write the zip
                    zfile = os.path.join(self.back_path, "temp.zip")
                    with open(zfile, "wb") as zf:
                        zf.write(patch[0])
                    with zipfile.ZipFile(zfile, 'r') as zipObj:
                        # Extract all the contents into the temporary
                        # directory.
                        zipObj.extractall(os.path.join(self.back_path, "temp"))
                    # Ditch the zip
                    os.remove(zfile)
                    # For each binary file, call the method again
                    # and see if the data has been changed.
                    diff = False
                    for file in os.listdir(
                            os.path.join(self.back_path, "temp")):
                        try:
                            # We only care about .bin files.
                            if file.split(".")[1] == "bin":
                                with open(file, "rb") as bin_file:
                                    raw_bin = bin_file.read()
                                self.save_to_backend((raw_bin, patch[1]))
                                diff = True
                        except FileNotFoundError or errors.SavingError:
                            pass
                    # Cleanup and finish.
                    shutil.rmtree(os.path.join(self.back_path, "temp"))
                    if not diff:
                        # No files changed, so we should raise a SavingError
                        raise errors.SavingError(patch[1]["title"], 503)
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
                            # This exact binary is already saved onto the
                            # system.
                            raise errors.SavingError(patch[1]["title"], 503)
                    f.close()

            # If we get here, we have a unique patch, so we need to find
            # out what version # to give it.

            # Case 2: Only one version of the patch existed previously.
            if len(os.listdir(os.path.join(self.back_path, pch))) == 2:
                name_bin = os.path.join(pch, "{}_v1.bin".format(pch_id))
                with open(name_bin, "wb") as f:
                    f.write(patch[0])
                self.save_metadata_json(patch[1], 1)
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
            # Case 3: There were already multiple versions in the patch
            # directory.
            elif len(os.listdir(os.path.join(self.back_path, pch))) > 2:
                # Increment the version number for each file in the directory.
                try:
                    for file in reversed(
                            sorted(os.listdir(os.path.join(pch)))):
                        ver = int(file.split("v")[1].split(".")[0]) + 1
                        extension = file.split(".")[1]
                        os.rename(os.path.join(pch,
                                               "{}_v{}.{}".format(pch_id,
                                                                  str(ver - 1),
                                                                  extension)),
                                  os.path.join(pch,
                                               "{}_v{}.{}".format(pch_id,
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
                self.save_metadata_json(patch[1], 1)
            else:
                """ Getting here indicates that the amount of files in the 
                directory was less than 2 (which would imply some form of 
                corruption occurred). 
                """
                raise errors.SavingError(patch[1]["title"])

    def save_metadata_json(self, metadata, version=0):
        """ Saves metadata for patches to the backend directory.

        metadata: A string containing the JSON data that will be used for
                  the metadata file that is being created.
        version: Optional. If the patch needs a version suffix, this
                 parameter should be set to the appropriate version number.
                 Valid version numbers are > 0.
        """

        # Save the metadata.
        if version <= 0:
            name_json = os.path.join(self.back_path, str(metadata['id']),
                                     "{}.json".format(metadata["id"]))
        else:
            name_json = os.path.join(self.back_path, str(metadata['id']),
                                     "{}_v{}.json".format(metadata["id"],
                                                          version))

        # Update the revision number if need be.
        if version > 0:
            metadata["revision"] = version

        with open(name_json, "w") as jf:
            json.dump(metadata, jf)

    def import_to_backend(self, path, version=False):
        """Attempts to import a patch to the backend
        ZoiaLibraryApp directory. This method is meant to work
        for patches that originate from a local user's machine,
        or from a ZOIA formatted SD card. It will also import entire
        directories of patch should they exist on an SD card.

        Base metadata will be created from the available information
        of the patch, mostly derived of the name and any additional
        information that can be ascertained.

        path: The filepath that leads to the local patch that is
              being imported.
        version: True if the directory being imported should be treated
                 as a version directory.
        Raises a SavingError should the patch fail to save.
        """

        fails = 0

        if path is None:
            raise errors.SavingError(None)

        # TODO Add a binary check to ensure this is a ZOIA patch.

        # Get the file extension for the patch that is being imported.
        if not version and "." not in path:
            raise errors.SavingError(path)
        if not version:
            patch_name, ext = path.rsplit(".", 1)
        else:
            patch_name = path
            if patch_name[1] == ":":
                patch_name = patch_name.split(":")[-1]
            ext = "bin"
        patch_name = patch_name.split(os.path.sep)[-1]
        # PyQt5 bug where the path separator is incorrect on Windows
        patch_name = patch_name.split("/")[-1]

        title = patch_name

        # Strip ### if it exists.
        try:
            int(title[:3])
            title = title[3:]
        except ValueError:
            pass

        # Strip "_zoia_" if needed.
        if "_zoia_" in title and title[:6] == "_zoia_":
            title = title[6:]

        # Strip "zoia_" if needed.
        if "zoia_" in title and title[:5] == "zoia_":
            title = title[5:]

        # Clean up the title.
        title = title.replace("_", " ")
        title = title.strip()

        patch_id = self.generate_patch_id(path)

        count = 1 if not os.path.isdir(path) else len(os.listdir(path))
        for i in range(count):
            # Generate a random patch ID to use (must be 5 digits).
            if not version:
                patch_id = self.generate_patch_id(path)
            # Binary file, easiest case.
            # Get the bytes.
            if not version:
                if path.split(".")[-1] != "bin":
                    continue
                with open(path, "rb") as f:
                    temp_data = f.read()
            else:
                temp_path = os.path.join(path, os.listdir(path)[i])
                if temp_path.split(".")[-1] != "bin":
                    continue
                with open(temp_path, "rb") as f:
                    temp_data = f.read()
            # Prepare the JSON.
            js_data = {
                "id": patch_id,
                "created_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                    datetime.datetime.now()),
                "updated_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                    datetime.datetime.now()),
                "title": title,
                "revision": "1",
                "preview_url": "",
                "like_count": 0,
                "download_count": 0,
                "view_count": 0,
                "author": {
                    "name": ""
                },
                "files": [
                    {
                        "id": patch_id,
                        "filename": patch_name + "." + ext
                    }
                ],
                "categories": [],
                "tags": [],
                "content": "",
                "license": {
                    "name": ""
                }
            }
            if os.path.exists(os.path.join(self.back_path, "data.json")):
                with open(os.path.join(self.back_path, "data.json"), "r") as f:
                    data = json.loads(f.read())
                for pch in data:
                    if pch["title"] == js_data["title"]:
                        temp = ps.get_patch_meta(pch["id"])
                        js_data = temp
                        js_data["updated_at"] = \
                            datetime.datetime.fromtimestamp(
                            os.path.getmtime(path)).strftime(
                                '%Y-%m-%dT%H:%M:%S+00:00')
                        break
            if version:
                js_data["updated_at"] = \
                    datetime.datetime.fromtimestamp(
                        os.path.getmtime(temp_path)).strftime(
                        '%Y-%m-%dT%H:%M:%S+00:00')
                js_data["files"][0]["filename"] = os.listdir(path)[i]

            # Try to save the patch.
            if not version:
                self.save_to_backend((temp_data, js_data))
            else:
                try:
                    self.save_to_backend((temp_data, js_data))
                except errors.SavingError:
                    fails += 1
                    continue
        return fails

    @staticmethod
    def generate_patch_id(path):
        """ Generates a 5-digit patch ID for a supplied path.
        """

        patch_id = str(abs(hash(path)))
        if len(patch_id) > 5:
            patch_id = patch_id[:5]
        else:
            while len(patch_id) < 5:
                patch_id += "0"
        patch_id = int(patch_id)
        return patch_id

    def patch_decompress(self, patch):
        """ Method stub for decompressing files retrieved from the PS API.

        patch: A tuple containing the downloaded file
               data and the patch metadata, comes from ps.download(IDX).
               patch[0] is raw binary data, while patch[1] is json data.
        Raises a SavingError should the contents fail to save.
        Raises a RenamingError should the contents fail to be renamed.
        """

        patch_name = str(patch[1]['id'])

        pch = os.path.join(self.back_path, "{}".format(str(patch_name)))
        if not os.path.isdir(pch):
            os.mkdir(pch)

        if patch[1]["files"][0]["filename"].split(".")[-1] == "zip":
            # .zip files
            name_zip = os.path.join(pch, "{}.zip".format(patch_name))
            with open(name_zip, "wb") as f:
                f.write(patch[0])
            with zipfile.ZipFile(
                    os.path.join(pch, "{}.zip".format(patch_name)),
                    'r') as zipObj:
                # Extract all the contents into the patch directory
                zipObj.extractall(pch)
            # Ditch the zip
            os.remove(name_zip)
            to_delete = None

            for file in os.listdir(pch):
                if os.path.isdir(os.path.join(pch, file)):
                    to_delete = (os.path.join(pch, file))
                    pch = os.path.join(pch, file)

            i = 0
            for file in os.listdir(pch):
                if file.split(".")[1] == "bin":
                    i += 1
                    try:
                        name = file
                        # Rename the file to follow the conventional format
                        os.rename(os.path.join(pch, file),
                                  os.path.join(pch, "{}_v{}.bin".format(
                                      patch[1]["id"], i)))
                        patch[1]["files"][0]["filename"] = name
                        self.save_metadata_json(patch[1], i)
                    except FileNotFoundError or FileExistsError:
                        raise errors.RenamingError(patch, 601)
                else:
                    # Remove any additional files.
                    # TODO make this better. Shouldn't just delete
                    #  additional files. Especially .txt, would want to
                    #  add that to the content attribute in the JSON.
                    os.remove(os.path.join(pch, file))
            if to_delete is not None:
                for file in os.listdir(to_delete):
                    correct_pch = os.path.join(self.back_path,
                                               "{}".format(str(patch_name)))
                    shutil.copy(os.path.join(to_delete, file),
                                os.path.join(correct_pch))
                try:
                    shutil.rmtree(to_delete)
                except FileNotFoundError:
                    raise errors.RenamingError(patch)

        else:
            # Unexpected file extension encountered.
            # TODO Handle this case gracefully.
            print(patch)
            raise errors.SavingError(patch[1]["title"], 501)
