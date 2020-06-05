import json
import os
import shutil
import unittest
from pathlib import Path

import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors


def add_test_patch(name, idx):
    name_bin = Path(name + ".bin")
    f2 = open(name_bin, "wb")
    f2.write(b"Test")
    f2.close()
    name_json = Path(name + ".json")
    jf2 = open(name_json, "w")
    json.dump({"id": idx, "title": "Test", "created_at": "test"}, jf2)
    jf2.close()


class DeletionTest(unittest.TestCase):
    def setUp(self):
        # Point to a local path for testing purposes.
        util.backend_path = os.getcwd()

        # Create a test patch to delete.
        add_test_patch("22222", 22222)

        # Create a secondary patch to ensure only the desired patch is deleted.
        add_test_patch("22223", 22223)

        # Create a version directory with 3 versions
        os.mkdir("22224")
        add_test_patch("22224\\22224_v1", 22224)
        add_test_patch("22224\\22224_v2", 22224)
        add_test_patch("22224\\22224_v3", 22224)

    def tearDown(self):
        # Clean up everything (in case it wasn't deleted properly).
        try:
            os.remove("22222.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove("22222.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("22223.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove("22223.json")
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree("22224")
        except FileNotFoundError:
            pass
        try:
            os.remove("22224.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove("22224.json")
        except FileNotFoundError:
            pass

    def test_delete_patch_normal(self):
        """ Attempt to delete a patch that is stored in the
        backend LibraryApp directory. The test ensures that
        the patch and metadata are deleted.
        """
        # Try to break the method
        exc = (FileNotFoundError, errors.DeletionError)
        self.assertRaises(exc, util.delete_patch, "IamNotAPatch")

        self.assertRaises(exc, util.delete_patch, None)

        # Try to delete a patch that exists.
        try:
            util.delete_patch("22222")
        except errors.DeletionError:
            self.fail("Failed to find patch 22222 to delete.")

        # Ensure the deletion removed both 22222.bin and 22222.json
        for file in os.listdir(os.getcwd()):
            if file == "22222.bin" or file == "22222.json":
                self.fail("Deletion did not properly remove both the 22222 patch file and associated metadata.")

    def test_delete_patch_version(self):
        """ Attempt to delete a patch that is stored in the
        backend LibraryApp directory. This specific patch is
        contained within a version directory. The test ensures
        that  the patch and metadata are deleted. It also
        ensures only the correct version of a patch is deleted.

        Should the deletion result in a version directory with only
        one version remaining, the patch and metadata should be
        moved back to the parent LibraryApp directory and the
        version directory should be deleted. The patch and metadata
        should be renamed appropriately.
        """
        # Try to delete a version.
        try:
            util.delete_patch("22224_v1")
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v1 to delete.")

        # Ensure the deletion removed both 22224_v1.bin and 22224_v1.json
        for file in os.listdir(Path(os.getcwd() + "\\22224")):
            if file == "22224_v1.bin" or file == "22224_v1.json":
                self.fail("Deletion did not properly remove both the 22224_v1 patch file and associated metadata.")

        # Delete another version (which leaves only one version of the patch.
        try:
            util.delete_patch("22224_v2")
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v2 to delete.")

        # Ensure the remaining version of the patch was moved out of the version directory.
        for patch in os.listdir(Path(os.getcwd())):
            if patch == "22224_v3.bin" or patch == "22224_v3.json" or patch == "22224":
                self.fail("Deletion did not properly move single patch version "
                          "to parent directory/delete version directory.")
