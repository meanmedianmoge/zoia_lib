import os
import shutil
import unittest

import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors

testing_path = os.getcwd()


class DeletionTest(unittest.TestCase):
    def setUp(self):
        util.backend_path = testing_path
        # Create a test patch to delete.
        util.add_test_patch("22222", 22222)

        # Create a secondary patch to ensure only the desired patch is deleted.
        util.add_test_patch("22223", 22223)

        # Create a version directory with 3 versions
        util.add_test_patch(os.path.join("22224", "22224_v1"), 22224)
        util.add_test_patch(os.path.join("22224", "22224_v2"), 22224)
        util.add_test_patch(os.path.join("22224", "22224_v3"), 22224)

    def tearDown(self):
        # Clean up everything (in case it wasn't deleted properly).
        try:
            shutil.rmtree(os.path.join(testing_path, "22222"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22222", "22222.bin"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22222", "22222.json"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(testing_path, "22223"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22223", "22223.bin"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22223", "22223.json"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(testing_path, "22224"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22224", "22224_v1.bin"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22224", "22224_v1.json"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22224", "22224_v2.bin"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22224", "22224_v2.json"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22224", "22224_v3.bin"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(testing_path, "22224", "22224_v3.json"))
        except FileNotFoundError:
            pass

    def test_delete_patch_normal_local(self):
        """ Attempt to delete a patch that is stored in the
        backend ZoiaLibraryApp directory. The test ensures that
        the patch and metadata are deleted, along with the patch
        directory that contained the files.
        """

        self.setUp()

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
        for file in os.listdir(testing_path):
            if file == "22222.bin" or file == "22222.json" or file == "22222":
                self.fail("Deletion did not properly remove both the 22222 patch file, "
                          "associated metadata, and patch directory")

        # Check to make sure that no other files got deleted unexpectedly.
        if "22223" not in os.listdir(testing_path):
            self.fail("Deletion also removed 22223 patch directory when it should not have.")
        if "22224" not in os.listdir(testing_path):
            self.fail("Deletion also removed 22224 patch directory when it should not have.")
        if "22224_v1.bin" not in os.listdir(os.path.join(testing_path, "22224")):
            self.fail("Deletion also removed the 22224_v1.bin when it should not have.")
        if "22224_v1.json" not in os.listdir(os.path.join(testing_path, "22224")):
            self.fail("Deletion also removed the 22224_v1.json when it should not have.")
        if "22224_v2.bin" not in os.listdir(os.path.join(testing_path, "22224")):
            self.fail("Deletion also removed the 22224_v2.bin when it should not have.")
        if "22224_v2.json" not in os.listdir(os.path.join(testing_path, "22224")):
            self.fail("Deletion also removed the 22224_v2.json when it should not have.")
        if "22224_v3.bin" not in os.listdir(os.path.join(testing_path, "22224")):
            self.fail("Deletion also removed the 22224_v3.bin when it should not have.")
        if "22224_v3.json" not in os.listdir(os.path.join(testing_path, "22224")):
            self.fail("Deletion also removed the 22224_v3.json when it should not have.")

        self.tearDown()

    def test_delete_patch_version(self):
        """ Attempt to delete a patch that is stored in the
        backend ZoiaLibraryApp directory. This specific patch is
        contained within a version directory. The test ensures
        that  the patch and metadata are deleted. It also
        ensures only the correct version of a patch is deleted.

        Should the deletion result in a version directory with only
        one version remaining, the patch and metadata should be
        correctly renamed to drop the version suffix.

        Note: SD cards do not support the idea of patch version histories.
        As such, this test only applied to the locally stored patches on
        a user's machine and not those on an SD card.
        """

        self.setUp()
        # Try to delete a version.
        try:
            util.delete_patch(os.path.join("22224", "22224_v1"))
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v1 to delete.")

        # Ensure the deletion removed both 22224_v1.bin and 22224_v1.json
        for file in os.listdir(os.path.join(testing_path, "22224")):
            if file == "22224_v1.bin" or file == "22224_v1.json":
                self.fail("Deletion did not properly remove both the 22224_v1 patch file and associated metadata.")

        # Delete another version (which leaves only one version of the patch.
        try:
            util.delete_patch("22224_v2")
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v2 to delete.")

        # Ensure the remaining version of the patch was renamed properly.
        for patch in os.listdir(os.path.join(testing_path, "22224")):
            if patch == "22224_v3.bin" or patch == "22224_v3.json" or patch == "22224":
                self.fail("Deletion did not properly result in the renaming of the singularly remaining patch version.")

        # Check to make sure that no other files got deleted unexpectedly.
        if "22222" not in os.listdir(testing_path):
            self.fail("Deletion also removed 22222 patch directory when it should not have.")
        if "22223" not in os.listdir(testing_path):
            self.fail("Deletion also removed 22223 patch directory when it should not have.")

        self.tearDown()

    def test_delete_patch_normal_sd(self):
        """ Attempt to delete a patch that is stored on an
        inserted SD card.
        """
        # TODO Buy an SD card adapter and get to work on this.
        pass
