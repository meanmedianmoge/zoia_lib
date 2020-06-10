import os
import shutil
import unittest

import zoia_lib.backend.utilities as util
from zoia_lib.common import errors

user_backend_path = util.determine_backend_path()


class TestStartup(unittest.TestCase):
    def setUp(self):
        # Create a backend directory and another directory for additional tests.
        util.create_backend_directories()
        util.backend_path = os.path.join(os.getcwd(), ".ZoiaLibraryApp")
        util.create_backend_directories()

    def tearDown(self):
        """ Remove the testing ZoiaLibraryApp directory.
        Leave the real backend directory alone.
        """
        shutil.rmtree(os.path.join(os.getcwd(), ".ZoiaLibraryApp"))

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

        found_library = False
        found_bank = False

        for file in os.listdir(user_backend_path.split(".")[0]):
            if file == ".ZoiaLibraryApp":
                found_library = True
                for f in os.listdir(user_backend_path):
                    if f == "Banks":
                        found_bank = True
                        break
                break

        # Ensure that the Library directory was found.
        self.assertTrue(found_library, "Did not find a ZoiaLibraryApp directory in the expected directory: " +
                        user_backend_path)
        # Ensure that the Banks directory was also found.
        self.assertTrue(found_bank, "Did not find a Banks directory nested under the LibraryApp directory.")

    def test_version_history_directory_creation(self):
        """ Attempt to save a patch that already exists
        to the LibraryApp folder.

        The test will validate that a new directory is created
        that takes the name of the patch id, and that the
        contents of the new directory contain the metadata
        and renamed patch files to conform to the version of
        each patch.
        """

        # Try to break the method with a NoneType
        patch = None
        correct = False
        try:
            util.save_to_backend(patch)
            correct = True
        except errors.SavingError:
            pass
        self.assertFalse(correct, "Was able to save a patch that is a NoneType")

        # Try to break the method with malformed tuple
        patch = ("ERROR", "ERROR")
        correct = False
        try:
            util.save_to_backend(patch)
            correct = True
        except errors.SavingError:
            pass
        self.assertFalse(correct, "Was able to save a patch with incorrect inputs")

        # Make sure there is no directory
        path = os.path.join(os.getcwd(), ".ZoiaLibraryApp")
        correct = False
        for file in os.listdir(path):
            if file == "55555":
                correct = True
                break
        self.assertFalse(correct, "Found a directory with the expected patch id of 55555 when it should not exist.")

        # Now add the directory and some patches
        # Create a dummy patch with dummy metadata.
        util.add_test_patch(os.path.join("55555", "55555_v1"), 55555)
        # Try to save the same patch again without making any changes to the binary contents of the patch.
        util.add_test_patch(os.path.join("55555", "55555_v2"), 55555)
        # Try to save the same patch again after making a change to the binary contents of the patch.
        fb = open(os.path.join(path, "55555", "55555_v1.bin"), "rb")
        binary = fb.read()
        binary += b'ed'
        fb.close()
        with open(os.path.join(path, "55555", "55555_v1.bin"), "wb") as f:
            f.write(binary)

        # Ensure a directory was created.
        correct = False

        for file in os.listdir(path):
            if file == "55555":
                correct = True
                break

        self.assertTrue(correct, "Did not find a directory with the expected patch id of 55555.")
        self.assertTrue(len(os.listdir(os.path.join(path, "55555"))) == 4,
                        "Directory did not contain the expected number of files.")

        for i in range(1, 3):
            self.assertTrue("55555_v{}.bin".format(i) in os.listdir(os.path.join(path, "55555")),
                            "The expected patch file \"55555_v{}.bin\" was not found.".format(i))
            self.assertTrue("55555_v{}.json".format(i) in os.listdir(os.path.join(path, "55555")),
                            "The expected patch file \"55555_v{}.json\" was not found.".format(i))
