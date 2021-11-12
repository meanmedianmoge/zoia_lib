import datetime
import json
import os
import platform
import shutil
import zipfile

import rarfile

from zoia_lib.backend.patch import Patch
from zoia_lib.common import errors
from zoia_lib.backend.api import PatchStorage
from zoia_lib.backend.patch_binary import PatchBinary
from zoia_lib.backend.utilities import hide_dotted_files, natural_key

pb = PatchBinary()
ps = PatchStorage()


class PatchSave(Patch):
    """The PatchSave class is a child of the Patch class. It is
    responsible for patch importing, saving, and decompressing.
    """

    def __init__(self):
        """Initialize the class such that it has a reference to the
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

        raise: SavingError should the patch fail to save.
        raise: RenamingError should the patch fail to be renamed.
        """

        # Don't try to save a file when we are missing necessary info.
        if (
            patch is None
            or patch[0] is None
            or patch[1] is None
            or self.back_path is None
            or not isinstance(patch[0], bytes)
            or not isinstance(patch[1], dict)
        ):
            raise errors.SavingError(None)

        try:
            # Ensure that the data is in valid json format.
            json.dumps(patch[1])
        except ValueError:
            raise errors.JSONError(patch[1], 801)

        pch_id = str(patch[1]["id"])
        if len(pch_id) == 5:
            # This is an imported patch. Unfortunately, we need to make sure
            # that its a unique binary by checking every patch currently
            # stored.
            for fld in os.listdir(self.back_path):
                if (
                    os.path.isdir(os.path.join(self.back_path, fld))
                    and fld != "Banks"
                    and fld != "Folders"
                    and fld != "sample_files"
                    and fld != ".DS_Store"
                ):
                    for files in os.listdir(os.path.join(self.back_path, fld)):
                        # Check every .bin file only.
                        if files.split(".")[-1] == "bin":
                            with open(
                                os.path.join(self.back_path, fld, files), "rb"
                            ) as f:
                                data = f.read()
                            if patch[0] == data:
                                with open(
                                    os.path.join(
                                        self.back_path,
                                        fld,
                                        files.split(".")[0] + ".json",
                                    ),
                                    "r",
                                ) as f:
                                    meta = json.load(f)
                                if "_v" in files:
                                    meta = meta["title"] + ": {}".format(
                                        patch[1]["files"][0]["filename"]
                                        .split(".")[0]
                                        .split("_zoia_")[-1]
                                        .replace("_", " ")
                                    )
                                else:
                                    meta = meta["title"]
                                raise errors.SavingError(meta, 503)

        pch = os.path.join(self.back_path, "{}".format(pch_id))
        # Check to see if a directory needs to be made
        # (new patch, no version control needed yet).
        if not os.path.isdir(pch):
            os.mkdir(pch)
            if (
                "files" in patch[1]
                and patch[1]["files"][0]["filename"].split(".")[-1] != "bin"
            ):
                # If it isn't a straight bin additional work must be done.
                if patch[1]["files"][0]["filename"].split(".")[-1] == "py":
                    # We are not responsible for .py files.
                    shutil.rmtree(os.path.join(self.back_path, pch))
                    raise errors.SavingError(patch[1], 501)
                else:
                    # Try to decompress the patch.
                    self._patch_decompress(patch)
            # Make sure the files attribute exists.
            elif "files" in patch[1]:
                name_bin = os.path.join(pch, "{}.bin".format(pch_id))
                with open(name_bin, "wb") as f:
                    f.write(patch[0])
                self.save_metadata_json(patch[1])
            else:
                # No files attribute,
                raise errors.SavingError(patch[1], 502)
        else:
            # A directory already existed for this patch id, so
            # we need to check if this is a unique patch version
            # (otherwise there is no need to save it).

            # Case 1: Check if this is a compressed patch import.
            if (
                "files" in patch[1]
                and patch[1]["files"][0]["filename"].split(".")[-1] != "bin"
            ):
                # We need to check the individual binary files to see which,
                # if any, differ from the ones currently stored.

                # Figure out which file compression is being used.
                if patch[1]["files"][0]["filename"].split(".")[-1] == "zip":
                    # Create a temporary directory to store
                    # the extracted files.
                    os.mkdir(os.path.join(self.back_path, "temp"))
                    # Write the zip
                    zfile = os.path.join(self.back_path, "temp.zip")
                    with open(zfile, "wb") as zf:
                        zf.write(patch[0])
                    with zipfile.ZipFile(zfile, "r") as zipObj:
                        # Extract all the contents into the temporary
                        # directory.
                        zipObj.extractall(os.path.join(self.back_path, "temp"))
                    # Ditch the zip
                    os.remove(zfile)
                elif patch[1]["files"][0]["filename"].split(".")[-1] == "rar":
                    # Create a temporary directory to store
                    # the extracted files.
                    os.mkdir(os.path.join(self.back_path, "temp"))
                    # Write the rar
                    rfile = os.path.join(self.back_path, "temp.zip")
                    with open(rfile, "wb") as rf:
                        rf.write(patch[0])
                    try:
                        with rarfile.RarFile(rfile, "r") as rar_obj:
                            # Extract all the contents into the temporary
                            # directory.
                            rar_obj.extractall(os.path.join(self.back_path, "temp"))
                    except rarfile.RarCannotExec:
                        # No WinRAR installed
                        os.remove(rfile)
                        raise errors.SavingError(patch[1]["title"])
                    # Ditch the rar
                    os.remove(rfile)
                else:
                    # If we get here we encountered a new compression algo.
                    # Logic needs to be added above to deal with it.
                    raise errors.SavingError(patch[1]["title"])
                # For each binary file, call the method again
                # and see if the data has been changed.
                diff = False
                for file in os.listdir(os.path.join(self.back_path, "temp")):
                    try:
                        # We only care about .bin files.
                        if file.split(".")[-1] == "bin":
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

            # If we get here, we are working with a .bin, so we
            # need to to see if the binary is already saved.
            for file in os.listdir(os.path.join(pch)):
                if file.split(".")[-1] == "bin":
                    with open(os.path.join(pch, file), "rb") as f:
                        if f.read() == patch[0]:
                            # This exact binary is already saved onto the
                            # system.
                            raise errors.SavingError(patch[1]["title"], 503)

            # If we get here, we have a unique patch, so we need to find
            # out what version # to give it.

            # Case 2: Only one version of the patch existed previously.
            if len(os.listdir(os.path.join(self.back_path, pch))) == 2:
                name_bin = os.path.join(pch, "{}_v2.bin".format(pch_id))
                with open(name_bin, "wb") as f:
                    f.write(patch[0])
                self.save_metadata_json(patch[1], 2)
                # Add the version suffix to the patch that was previously
                # in the directory.
                try:
                    os.rename(
                        os.path.join(pch, "{}.bin".format(pch_id)),
                        os.path.join(pch, "{}_v1.bin".format(pch_id)),
                    )
                    os.rename(
                        os.path.join(pch, "{}.json".format(pch_id)),
                        os.path.join(pch, "{}_v1.json".format(pch_id)),
                    )
                except FileNotFoundError or FileExistsError:
                    raise errors.RenamingError(patch, 601)
                # Update the revision number in the metadata.
                # (Used for sorting purposes).
                with open(os.path.join(pch, "{}_v1.json".format(pch_id)), "r") as f:
                    jf = json.loads(f.read())
                jf["revision"] = 1
                with open(os.path.join(pch, "{}_v1.json".format(pch_id)), "w") as f:
                    json.dump(jf, f)

            # Case 3: There were already multiple versions in the patch
            # directory.
            elif len(os.listdir(os.path.join(self.back_path, pch))) > 2:
                # Save as newest version
                fls = sorted(
                    sorted(os.listdir(pch), key=len), key=natural_key, reverse=True
                )
                latest = int(fls[0].split("_v")[-1].split(".")[0]) + 1
                name_bin = os.path.join(pch, "{}_v{}.bin".format(pch_id, latest))
                with open(name_bin, "wb") as f:
                    f.write(patch[0])
                self.save_metadata_json(patch[1], latest)
            else:
                """Getting here indicates that the amount of files in the
                directory was less than 2 (which would imply some form of
                corruption occurred).
                """
                raise errors.SavingError(patch[1]["title"])

    def save_metadata_json(self, metadata, version=0):
        """Saves metadata for patches to the backend directory.

        metadata: A string containing the JSON data that will be used for
                  the metadata file that is being created.
        version: Optional. If the patch needs a version suffix, this
                 parameter should be set to the appropriate version number.
                 Valid version numbers are > 0.
        """

        # Save the metadata.
        if version <= 0:
            name_json = os.path.join(
                self.back_path, str(metadata["id"]), "{}.json".format(metadata["id"])
            )
        else:
            name_json = os.path.join(
                self.back_path,
                str(metadata["id"]),
                "{}_v{}.json".format(metadata["id"], version),
            )

        # Update the revision number if need be.
        if version > 0:
            metadata["revision"] = version
        metadata["rating"] = 0

        with open(name_json, "w") as jf:
            json.dump(metadata, jf)

    def import_to_backend(self, path, version=False):
        """Attempts to import a patch to the backend .ZoiaLibraryApp
        directory. This method is meant to work for patches that
        originate from a local user's machine, or from a ZOIA formatted
        SD card. It will also import entire directories of patch should
        they exist on an SD card.

        Base metadata will be created from the available information
        of the patch, mostly derived of the name and any additional
        information that can be ascertained.

        path: The filepath that leads to the local patch that is
              being imported.
        version: True if the directory being imported should be treated
                 as a version directory.

        raise: SavingError should the patch fail to save.

        return: The number of patches that failed to import as an int.
        """

        fails = 0
        errs = []

        if path is None:
            raise errors.SavingError(None)

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
        # PySide2 bug where the path separator is incorrect on Windows :')
        if platform.system().lower() == "windows":
            patch_name = patch_name.split("\\")[-1]
        else:
            patch_name = patch_name.split(os.path.sep)[-1]

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

        # Get a 5-digit patch id for this patch.
        patch_id = self._generate_patch_id(path)

        if os.path.isdir(path):
            files = hide_dotted_files(path)
            count = len(files)
        else:
            files = [path]
            count = 1

        for i in range(count):
            if not version:
                # Since this is not a version, we need a unique id for each
                # patch.
                patch_id = self._generate_patch_id(files[i])
            # Get the bytes.
            temp_path = files[i]
            # if temp_path.split(".")[-1] != "bin":
            #     continue
            with open(temp_path, "rb") as f:
                temp_data = f.read()

            # Check if the patch is a valid ZOIA binary
            # try:
            #     pb.parse_data(temp_data)
            # except errors.BinaryError:
            #     fails += 1
            #     continue

            # Prepare the JSON.
            js_data = {
                "id": patch_id,
                "created_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                    datetime.datetime.now()
                ),
                "updated_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                    datetime.datetime.now()
                ),
                "title": title,
                "revision": "1",
                "preview_url": "",
                "rating": 0,
                "like_count": 0,
                "download_count": 0,
                "view_count": 0,
                "author": {"name": ""},
                "files": [
                    {"id": patch_id, "filename": "{}.{}".format(patch_name, ext)}
                ],
                "categories": [],
                "tags": [],
                "content": "",
                "license": {"name": ""},
            }
            if not version:
                if os.path.exists(os.path.join(self.back_path, "data.json")):
                    with open(os.path.join(self.back_path, "data.json"), "r") as f:
                        data = json.loads(f.read())
                    for pch in data:
                        if js_data["title"].lower() in pch["title"].lower():
                            temp = ps.get_patch_meta(pch["id"])
                            js_data = temp
                            js_data["files"] = [
                                {"id": pch["id"], "filename": "{}.{}".format(patch_name, ext)}
                            ]
                            js_data["updated_at"] = "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                                datetime.datetime.now()
                            )
                            break
            if version:
                js_data["updated_at"] = "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                    datetime.datetime.now()
                )
                js_data["files"][0]["filename"] = files[i].split("/")[-1]

            # Try to save the patch.
            if not version:
                self.save_to_backend((temp_data, js_data))
            else:
                try:
                    self.save_to_backend((temp_data, js_data))
                except errors.SavingError as e:
                    fails += 1
                    e = (
                        str(e)
                        .split("(")[1]
                        .split(")")[0]
                        .split(",")[0]
                        .replace("'", "")
                    )
                    errs.append(e)
                    continue

        return count - 1, fails, errs

    def _patch_decompress(self, patch):
        """Method stub for decompressing files retrieved from the PS
        API. Currently only supports .zip and .rar files.

        patch: A tuple containing the downloaded file
               data and the patch metadata, comes from ps.download().
               patch[0] is raw binary data, while patch[1] is json data.

        raise: SavingError should the contents fail to save.
        raise: RenamingError should the contents fail to be renamed.
        """

        patch_id = str(patch[1]["id"])

        pch = os.path.join(self.back_path, "{}".format(patch_id))
        if not os.path.isdir(pch):
            os.mkdir(pch)

        if patch[1]["files"][0]["filename"].split(".")[-1] == "zip":
            # .zip files
            name_zip = os.path.join(pch, "{}.zip".format(patch_id))
            with open(name_zip, "wb") as f:
                f.write(patch[0])
            with zipfile.ZipFile(
                os.path.join(pch, "{}.zip".format(patch_id)), "r"
            ) as zip_obj:
                # Extract all the contents into the patch directory
                zip_obj.extractall(pch)
            # Ditch the zip
            os.remove(name_zip)
            to_delete = None
        elif (
            patch[1]["files"][0]["filename"].split(".")[-1] == "rar"
            and platform.system().lower() != "darwin"
        ):
            # .rar files
            name_rar = os.path.join(pch, "{}.rar".format(patch_id))
            with open(name_rar, "wb") as f:
                f.write(patch[0])
            try:
                with rarfile.RarFile(
                    os.path.join(pch, "{}.rar".format(patch_id)), "r"
                ) as rar_obj:
                    # Extract all the contents into the patch directory
                    rar_obj.extractall(pch)
                # Ditch the rar
                os.remove(name_rar)
                to_delete = None
            except rarfile.BadRarFile:
                print("File is not properly compressed in the RAR format")
                try:
                    shutil.rmtree(pch)
                except FileNotFoundError:
                    pass
                raise errors.SavingError(patch[1]["title"], 506)
            except rarfile.RarCannotExec:
                print(
                    "As .rar compression is a commercial product, you must "
                    "download external software to download this patch "
                    "(i.e. You need WinRAR installed for this to work)."
                )
                try:
                    shutil.rmtree(pch)
                except FileNotFoundError:
                    pass
                raise errors.SavingError(patch[1]["title"], 501)
        else:
            # Unexpected file extension encountered.
            os.rmdir(pch)
            raise errors.SavingError(patch[1]["title"], 501)

        # Get to the uncompressed directory.
        for file in os.listdir(pch):
            if os.path.isdir(os.path.join(pch, file)) and len(os.listdir(pch)) == 1:
                to_delete = os.path.join(pch, file)
                pch = os.path.join(pch, file)
            elif os.path.isdir(os.path.join(pch, file)):
                # Oh boy they compressed it with a directory and some
                # stray files because they hate us.
                shutil.rmtree(os.path.join(pch, file))

        if len(os.listdir(pch)) == 1:
            # The compressed file only contained 1 patch.
            for file in os.listdir(pch):
                name = file
                os.rename(
                    os.path.join(pch, file),
                    os.path.join(pch, "{}.bin".format(patch_id)),
                )
                patch[1]["files"][0]["filename"] = name
                self.save_metadata_json(patch[1])
        else:
            # The compressed file contained more than 1 patch.
            i = 0
            for file in os.listdir(pch):
                if file.split(".")[-1] == "bin":
                    i += 1
                    try:
                        name = file
                        # Rename the file to follow the conventional format
                        os.rename(
                            os.path.join(pch, file),
                            os.path.join(pch, "{}_v{}.bin".format(patch_id, i)),
                        )
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
            # We need to cleanup.
            for file in os.listdir(to_delete):
                correct_pch = os.path.join(self.back_path, "{}".format(str(patch_id)))
                shutil.copy(os.path.join(to_delete, file), os.path.join(correct_pch))
            try:
                shutil.rmtree(to_delete)
            except FileNotFoundError:
                raise errors.RenamingError(patch)

    @staticmethod
    def _generate_patch_id(path):
        """Generates a 5-digit patch ID for a supplied path.
        The same string will hash to the same 5-digit identifier.

        return: A 5-digit hash number based on the path, as an int.
        """

        # Use the hash function to get the same result with the same
        # path.
        patch_id = str(abs(hash(path)))
        if len(patch_id) > 5:
            patch_id = patch_id[:5]
        else:
            # All local patches are 5 digits, so continue until we hit
            # that length.
            while len(patch_id) < 5:
                patch_id += "0"
        return int(patch_id)
