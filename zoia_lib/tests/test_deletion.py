import os
import shutil
import unittest

import zoia_lib.common.errors as errors
from zoia_lib.backend.utilities import add_test_patch
from zoia_lib.backend.patch_delete import PatchDelete

test_path = os.path.join(os.getcwd(), "zoia_lib", "tests")

delete_pch = PatchDelete()


class TestDeletion(unittest.TestCase):
    """This class is responsible for testing the various deletion
    methods that are to be used on data stored in the backend
    application directory.

    Currently, the tests cover the deletion of
    locally stored patches, a specific local version of a patch, and the
    deletion of an entire patch directory.
    """

    def setUp(self):
        # Create a test patch to delete.
        add_test_patch("22222", 22222, delete_pch.back_path)

        # Create a secondary patch to ensure only the desired patch is deleted.
        add_test_patch("22223", 22223, delete_pch.back_path)

        # Create a version directory with 3 versions
        for i in range(1, 4):
            add_test_patch(
                os.path.join("22224", "22224_v{}".format(i)),
                22224,
                delete_pch.back_path,
            )

    def tearDown(self):
        # Clean up everything (in case it wasn't deleted properly).
        try:
            shutil.rmtree(os.path.join(test_path, "22222"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(test_path, "22222", "22222.bin"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(test_path, "22222", "22222.json"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(test_path, "22223"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(test_path, "22223", "22223.bin"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(test_path, "22223", "22223.json"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(test_path, "22224"))
        except FileNotFoundError:
            pass
        try:
            for i in range(1, 4):
                os.remove(os.path.join(test_path, "22224", "22224_v{}.bin".format(i)))
                os.remove(os.path.join(test_path, "22224", "22224_v{}.bin".format(i)))
        except FileNotFoundError:
            pass

    def test_delete_patch_normal_local(self):
        """Attempt to delete a patch that is stored in the
        backend ZoiaLibraryApp directory. The test ensures that
        the patch and metadata are deleted, along with the patch
        directory that contained the files.
        """

        self.setUp()

        # Try to break the method
        exc = (FileNotFoundError, errors.DeletionError, errors.BadPathError)
        self.assertRaises(exc, delete_pch.delete_patch, "IamNotAPatch")
        self.assertRaises(exc, delete_pch.delete_patch, None)

        # Try to delete a patch that exists.
        try:
            delete_pch.delete_patch("22222")
        except errors.DeletionError:
            self.fail("Failed to find patch 22222 to delete.")

        # Ensure the deletion removed both 22222.bin and 22222.json
        for file in os.listdir(test_path):
            self.assertFalse(
                file == "22222.bin" or file == "22222.json" or file == "22222",
                "Deletion did not properly remove both the "
                "22222 patch file, associated metadata, and "
                "patch directory",
            )

        # Check to make sure that no other files got deleted unexpectedly.
        self.assertFalse(
            "22223" not in os.listdir(test_path),
            "Deletion also removed 22223 patch directory when it " "should not have.",
        )
        self.assertFalse(
            "22224" not in os.listdir(test_path),
            "Deletion also removed 22224 patch directory when it " "should not have.",
        )

        path = os.path.join(test_path, "22224")

        for i in range(1, 4):
            self.assertTrue(
                "22224_v{}.bin".format(i) in os.listdir(path),
                "Deletion also removed patch file "
                '"22224_v{}.bin" when it should not '
                "have.".format(i),
            )
            self.assertTrue(
                "22224_v{}.json".format(i) in os.listdir(path),
                "Deletion also removed patch file "
                '"22224_v{}.json" when it should not '
                "have.".format(i),
            )

        self.tearDown()

    def test_delete_patch_version(self):
        """Attempt to delete a patch that is stored in the
        backend ZoiaLibraryApp directory. This specific patch is
        contained within a version directory. The test ensures
        that  the patch and metadata are deleted. It also
        ensures only the correct version of a patch is deleted.

        Should the deletion result in a version directory with only
        one version remaining, the patch and metadata should be
        correctly renamed to drop the version suffix.

        Note: SD cards do not support the idea of patch version
        histories. As such, this test only applied to the locally
        stored patches on a user's machine and not those on an SD card.
        """

        self.setUp()

        # Try to delete a version.
        try:
            delete_pch.delete_patch(os.path.join("22224", "22224_v1"))
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v1 to delete.")

        # Ensure the deletion removed both 22224_v1.bin and 22224_v1.json
        for file in os.listdir(os.path.join(test_path, "22224")):
            self.assertFalse(
                file == "22224_v1.bin" or file == "22224_v1.json",
                "Deletion did not properly remove both the "
                "22224_v1 patch file and associated metadata.",
            )

        # Delete another version (which leaves only one version of the patch.
        try:
            delete_pch.delete_patch("22224_v2")
        except errors.DeletionError:
            self.fail("Failed to find patch 22224_v2 to delete.")

        # Ensure the remaining version of the patch was renamed properly.
        files = os.listdir(os.path.join(test_path, "22224"))
        self.assertFalse(
            "22224_v3.bin" in files or "22224_v3.json" in files or "22224" in files,
            "Deletion did not properly result in the "
            "renaming of the singularly remaining "
            "patch version.",
        )

        # Check to make sure that no other files got deleted unexpectedly.
        self.assertFalse(
            "22222" not in os.listdir(test_path),
            "Deletion also removed 22222 patch directory when it " "should not have.",
        )
        self.assertFalse(
            "22223" not in os.listdir(test_path),
            "Deletion also removed 22223 patch directory when it " "should not have.",
        )

        self.tearDown()

    def test_delete_patch_directory(self):
        """Attempt to delete an entire patch directory from the
        backend application directory. Note the method being tested is
        aggressive and will delete a patch directory even if it still
        contains files.
        """

        self.setUp()

        # Try to break the method.
        exc = (FileNotFoundError, errors.DeletionError, errors.BadPathError)
        self.assertRaises(exc, delete_pch.delete_full_patch_directory, "IamNotAPatch")
        self.assertRaises(exc, delete_pch.delete_full_patch_directory, None)
        self.assertRaises(exc, delete_pch.delete_full_patch_directory, "22222.bin")
        self.assertRaises(exc, delete_pch.delete_full_patch_directory, "22224_v1.bin")
        self.assertRaises(exc, delete_pch.delete_full_patch_directory, "22224_v1")

        # Try to delete a patch directory.
        delete_pch.delete_full_patch_directory("22222")
        self.assertFalse(
            "22222" in os.listdir(test_path),
            "Deletion did not successfully remove patch " "directory 22222.",
        )
        # Try to delete it again.
        self.assertRaises(exc, delete_pch.delete_full_patch_directory, "22222")

        # Try to delete a patch directory with multiple patches
        # contained within.
        delete_pch.delete_full_patch_directory("22224")
        self.assertFalse(
            "22224" in os.listdir(test_path),
            "Deletion did not successfully remove patch " "directory 22224.",
        )

        path = os.path.join(test_path, "22224")

        try:
            for i in range(1, 4):
                self.assertTrue(
                    "22224_v{}.bin".format(i) in os.listdir(path),
                    "Deletion did not remove patch file " '"22224_v{}.bin".'.format(i),
                )
                self.assertTrue(
                    "22224_v{}.json".format(i) in os.listdir(path),
                    "Deletion did not remove patch file " '"22224_v{}.json".'.format(i),
                )
        except FileNotFoundError:
            pass

        self.tearDown()

    def test_delete_patch_normal_sd(self):
        """Attempt to delete a patch that is stored on an
        inserted SD card. Note that we cannot properly anticipate
        the case where a user removes the SD card while trying to
        delete a patch. In such cases, the SD will most likely be left
        in a corrupted state, but a DeletionError will be properly
        raised.
        """

        # In order to simulate this, we can just delete any patch using
        # the full path name and the appropriate method.
        self.setUp()

        # Try to break the method.
        exc = (FileNotFoundError, errors.DeletionError, errors.BadPathError)
        self.assertRaises(exc, delete_pch.delete_patch_sd, None)
        self.assertRaises(exc, delete_pch.delete_patch_sd, "IamNotAPatch")

        delete_pch.delete_patch_sd(22222, os.path.join(test_path, "22222", "22222.bin"))
        # Ensure it got deleted correctly.
        self.assertTrue("22222.bin" not in os.listdir(os.path.join(test_path, "22222")))
        # Try to delete it again.
        self.assertRaises(
            exc,
            delete_pch.delete_patch_sd,
            os.path.join(test_path, "22222", "22222.bin"),
        )
        # Try to delete a patch without the file extension.
        self.assertRaises(
            exc, delete_pch.delete_patch_sd, os.path.join(test_path, "22222", "22222")
        )

        self.tearDown()
