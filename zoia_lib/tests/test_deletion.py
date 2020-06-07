import os
import shutil
import unittest

import zoia_lib.common.errors as errors
import zoia_lib.backend.utilities as util

backend_path = None
if backend_path is None:
    backend_path = util.determine_backend_path()


class DeletionTest(unittest.TestCase):

    def setUp(self):
        # Create a test patch to delete.
        util.add_test_patch("22222", 22222)

        # Create a secondary patch to ensure only the desired patch is deleted.
        util.add_test_patch("22223", 22223)

        # Create a version directory with 3 versions
        util.add_test_patch("22224/22224_v1", 22224)
        util.add_test_patch("22224/22224_v2", 22224)
        util.add_test_patch("22224/22224_v3", 22224)

    def tearDown(self):
        # Clean up everything (in case it wasn't deleted properly).
        try:
            shutil.rmtree(backend_path + "/22222")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22222/22222.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22222/22222.json")
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(backend_path + "/22223")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22223/22223.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22223/22223.json")
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(backend_path + "/22224")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22224/22224_v1.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22224/22224_v1.json")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22224/22224_v2.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22224/22224_v2.json")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22224/22224_v3.bin")
        except FileNotFoundError:
            pass
        try:
            os.remove(backend_path + "/22224/22224_v3.json")
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
        for file in os.listdir(backend_path + "/22222"):
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
            util.delete_patch("22224/22224_v1")
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v1 to delete.")

        # Ensure the deletion removed both 22224_v1.bin and 22224_v1.json
        for file in os.listdir(backend_path + "/22224"):
            if file == "22224_v1.bin" or file == "22224_v1.json":
                self.fail("Deletion did not properly remove both the 22224_v1 patch file and associated metadata.")

        # Delete another version (which leaves only one version of the patch.
        try:
            util.delete_patch("22224_v2")
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v2 to delete.")

        # Ensure the remaining version of the patch was renamed properly
        for patch in os.listdir(backend_path + "/22224"):
            if patch == "22224_v3.bin" or patch == "22224_v3.json" or patch == "22224":
                self.fail("Deletion did not properly move single patch version "
                          "to parent directory/delete version directory.")
