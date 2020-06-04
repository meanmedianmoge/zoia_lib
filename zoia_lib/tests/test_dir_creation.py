import os
import shutil
import unittest

from zoia_lib.backend.startup import create_backend_directories
import zoia_lib.backend.utilities as util


class TestStartup(unittest.TestCase):
    def setUp(self):
        # Figure out what path to use.
        self.path = util.determine_backend_path()
        create_backend_directories()

    def tearDown(self):
        """ Remove the LibraryApp directory that was created during testing.

        **IMPORTANT**
        Do not run this test suite if you are using the LibraryApp as it is
        intended to be used normally. This will delete any patch/bank files.
        """
        shutil.rmtree(self.path + "\\.LibraryApp")

    def test_directory_init(self):
        """Ensures the application successfully creates
        the necessary directories in the expected folder
        based on the OS that is being used.

        # Windows: C:/Users/${User}/AppData/Roaming
        # Linux: ~/.local/share
        # macOS: ~/Library/Application Support
        TODO Research Solaris, Chrome OS, and Java OS to
             find out what directory path to use.
        """

        found_library = False
        found_bank = False

        for file in os.listdir(self.path):
            if file == ".LibraryApp":
                found_library = True
                for f in os.listdir(self.path + "\\.LibraryApp"):
                    if f == "Banks":
                        found_bank = True
                        break
                break

        # Ensure that the Library directory was found.
        self.assertTrue(found_library, "Did not find a LibraryApp directory in the expected directory: " +
                        self.path)
        # Ensure that the Banks directory was also found.
        self.assertTrue(found_bank, "Did not find a Bank directory nested under the LibraryApp directory.")

    def test_version_history_directory_creation(self):
        """ Attempt to save a patch that already exists
        to the LibraryApp folder.

        The test will validate the a new directory is created
        that takes the name of the patch id, and that the
        contents of the new directory contain the metadata
        and renamed patch files to conform to the version of
        each patch.
        """
        # Try to break the method.
        util.save_to_backend(None)
        incorrect_tuple = ("ERROR", "ERROR")
        util.save_to_backend(incorrect_tuple)

        path = ''
        correct = False

        for file in os.listdir(self.path + "\\.LibraryApp"):
            if file == "55555":
                path = self.path + file
                correct = True
                break
        self.assertFalse(correct, "Found a directory with the expected patch id of 55555 when it should not exist.")

        # Create a dummy patch with dummy metadata.
        # save_to_backend(f)
        # Try to save the same patch again without making any changes to the binary contents of the patch.
        # save_to_backend(f)
        # Try to save the same patch again after making a change to the binary contents of the patch.
        # the binary content magically changes with some excellent code here.
        # save_to_backend(f)

        # Ensure a directory was created.
        correct = False

        for file in os.listdir(self.path + "\\.LibraryApp"):
            if file == "55555":
                path = self.path + file
                correct = True
                break
        self.assertTrue(correct, "Did not find a directory with the expected patch id of 55555.")

        json_files = {}
        bin_files = {}

        for f in os.listdir(path + "\\55555"):
            if os.path.splitext(f) == ".bin":
                bin_files[len(bin_files)] = f
            elif os.path.splitext(f) == ".json":
                json_files[len(json_files)] = f

        self.assertEqual(len(json_files) + len(bin_files), 4, "Directory did not contain the expected number of files.")
        self.assertTrue(json_files[0] == "55555_v1.json", "File 55555_v1.json was not found.")
        self.assertTrue(json_files[1] == "55555_v1.json", "File 55555_v2.json was not found.")
        self.assertTrue(bin_files[0] == "55555_v1.json", "File 55555_v1.bin was not found.")
        self.assertTrue(bin_files[1] == "55555_v1.json", "File 55555_v2.bin was not found.")
