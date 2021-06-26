import os
import shutil
import unittest

import zoia_lib.backend.utilities as util
from zoia_lib.backend.patch_save import PatchSave
from zoia_lib.common import errors
from zoia_lib.backend.utilities import add_test_patch

save = PatchSave()

backend_path = util.determine_backend_path()


class TestDirectoryCreation(unittest.TestCase):
    """This class is responsible for testing the various directory
    creation methods that are to be used by the application.

    Currently, the tests cover the creation of the initial backend
    .ZoiaLibraryApp directory, along with the creation of patch
    directories within said .ZoiaLibraryApp directory.
    """

    def setUp(self):
        # Create a backend directory and another
        # directory for additional tests.
        save._create_backend_directories()
        save.back_path = os.path.join(
            os.getcwd(), "zoia_lib", "tests", ".ZoiaLibraryApp"
        )
        save._create_backend_directories()

    def tearDown(self):
        # Remove the testing ZoiaLibraryApp directory.
        # Leave the real backend directory alone.
        try:
            shutil.rmtree(
                os.path.join(os.getcwd(), "zoia_lib", "tests", ".ZoiaLibraryApp")
            )
        except FileNotFoundError:
            pass

    def test_directory_init(self):
        """Ensures the application successfully creates
        the necessary directories in the expected folder
        based on the OS that is being used.

        # Windows: C:/Users/${User}/AppData/Roaming
        # Linux: ~/.local/share
        # macOS: ~/.Library/Application Support
        TODO Research Solaris, Chrome OS, and Java OS to
             find out what directory path to use.
        """

        self.setUp()

        # Ensure that the Library directory was found.
        self.assertTrue(
            ".ZoiaLibraryApp" in os.listdir(backend_path.split(".")[0]),
            "Did not find a .ZoiaLibraryApp directory in the "
            "expected directory: {}".format(backend_path),
        )
        # Ensure that the Folders directory was also found.
        self.assertTrue(
            "Folders" in os.listdir(backend_path),
            "Did not find a Folders directory nested under the "
            ".ZoiaLibraryApp directory.",
        )

        self.tearDown()

    def test_version_history_directory_creation(self):
        """Attempt to save a patch that already exists
        to the LibraryApp folder.

        The test will validate that a new directory is created
        that takes the name of the patch id, and that the
        contents of the new directory contain the metadata
        and renamed patch files to conform to the version of
        each patch.
        """

        self.setUp()

        # Try to break the method with a NoneType
        exc = (FileNotFoundError, errors.SavingError)
        self.assertRaises(exc, save.save_to_backend, None)
        self.assertRaises(exc, save.save_to_backend, ("ERROR", "ERROR"))
        self.assertRaises(exc, save.save_to_backend, (None, "ERROR"))
        self.assertRaises(exc, save.save_to_backend, ("ERROR", None))

        # Make sure there is no directory
        path = os.path.join(os.getcwd(), "zoia_lib", "tests", ".ZoiaLibraryApp")
        self.assertFalse(
            "55555" in os.listdir(path),
            "Found a directory with the expected patch id of "
            "55555 when it should not exist.",
        )

        # Now add the directory and some patches
        # Create a dummy patch with dummy metadata.
        add_test_patch(os.path.join("55555", "55555_v1"), 55555, save.back_path)
        # Try to save the same patch again without making any changes to the
        # binary contents of the patch.
        add_test_patch(os.path.join("55555", "55555_v2"), 55555, save.back_path)
        # Try to save the same patch again after making a change to the
        # binary contents of the patch.
        with open(os.path.join(path, "55555", "55555_v1.bin"), "rb") as fb:
            binary = fb.read()
            binary += b"ed"
        with open(os.path.join(path, "55555", "55555_v1.bin"), "wb") as f:
            f.write(binary)

        # Ensure a directory was created.
        self.assertTrue(
            "55555" in os.listdir(path),
            "Did not find a directory with the expected patch id " "of 55555.",
        )

        path = os.path.join(path, "55555")

        self.assertTrue(
            len(os.listdir(path)) == 4,
            "Directory did not contain the expected number of " "files.",
        )

        for i in range(1, 3):
            self.assertTrue(
                "55555_v{}.bin".format(i) in os.listdir(path),
                'The expected patch file "55555_v{}.bin" ' "was not found.".format(i),
            )
            self.assertTrue(
                "55555_v{}.json".format(i) in os.listdir(path),
                'The expected patch file "55555_v{}.json" ' "was not found.".format(i),
            )

        self.tearDown()
