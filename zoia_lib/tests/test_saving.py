import json
import os
import shutil
import unittest

import zoia_lib.backend.utilities as util
from zoia_lib.common import errors

testing_path = os.getcwd()


class TestSorting(unittest.TestCase):
    def setUp(self):
        util.backend_path = testing_path

    def tearDown(self):
        try:
            shutil.rmtree(os.path.join(testing_path, "122661"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(testing_path, "124436"))
        except FileNotFoundError:
            pass

    def test_save_patch_api_bin(self):
        """ Attempts to save a regular binary patch to the
        backend ZoiaLibraryApp directory. This requires the
        creation of a patch directory to store the patch within,
        along with the accompanying metadata. This simulates a
        patch that originates from the PS API.
        """
        # Can't use the usual add_test_patch method since that
        # functionality is what we are trying to test.

        # Load the sample JSON data.
        f = open(os.path.join(os.getcwd(), "sample_files", "sampleJS.json"))
        sample_json = json.loads(f.read())
        f.close()

        # Try to break the method
        exc = (FileNotFoundError, errors.SavingError)
        self.assertRaises(exc, util.save_to_backend, (None, None))
        self.assertRaises(exc, util.save_to_backend, ("I am not a patch", None))
        self.assertRaises(exc, util.save_to_backend, (None, "Still not a patch"))
        self.assertRaises(exc, util.save_to_backend, (b"Test", "Still not a patch"))
        self.assertRaises(exc, util.save_to_backend, (None, {"id": 22222, "title": "Test", "created_at": "test"}))
        self.assertRaises(exc, util.save_to_backend, ("IamNotAPatch", "Still not a patch"))
        self.assertRaises(exc, util.save_to_backend,
                          ("IamNotAPatch", {"id": 22222, "title": "Test", "created_at": "test"}))

        # Try to save a sample patch to the backend directory as if it originated from the PS API.
        util.save_to_backend((b"TestPatch", sample_json))

        # Make sure the patch directory got created.
        self.assertTrue("122661" in os.listdir(testing_path), "The patch directory for patch 122661 was not found.")
        # Check the contents of the patch directory.
        self.assertTrue("122661.bin" in os.listdir(os.path.join(testing_path, "122661")),
                        "The expected patch file \"122661.bin\" was not found.")
        self.assertTrue("122661.json" in os.listdir(os.path.join(testing_path, "122661")),
                        "The expected patch file \"122661.json\" was not found.")

        # Try to same the same patch again (should fail, since the binary has not changed).
        self.assertRaises(exc, util.save_to_backend, (b"TestPatch", sample_json))

        # Try to save a different patch with the same id (should correctly make a new version since the binary has
        # changed).
        util.save_to_backend((b"TestDifferentBinary", sample_json))
        for i in range(1, 3):
            self.assertTrue("122661_v{}.bin".format(i) in os.listdir(os.path.join(testing_path, "122661")),
                        "The expected patch file \"122661_v{}.bin\" was not found.".format(i))
            self.assertTrue("122661_v{}.json".format(i) in os.listdir(os.path.join(testing_path, "122661")),
                        "The expected patch file \"122661_v{}.json\" was not found.".format(i))

        # TODO Verify the revision numbers were properly updated.

        # Try to save a different patch with the same id (should correctly make a new version since the binary has
        # changed).
        util.save_to_backend((b"TestDifferentBinaryAgain", sample_json))
        for i in range(1, 4):
            self.assertTrue("122661_v{}.bin".format(i) in os.listdir(os.path.join(testing_path, "122661")),
                        "The expected patch file \"122661_v{}.bin\" was not found.".format(i))
            self.assertTrue("122661_v{}.json".format(i) in os.listdir(os.path.join(testing_path, "122661")),
                        "The expected patch file \"122661_v{}.json\" was not found.".format(i))

        # TODO Verify the revision numbers were properly updated.

    def test_save_patch_api_compressed(self):
        """ Attempts to save a regular compressed patch to the
        backend ZoiaLibraryApp directory. This requires the
        creation of a patch directory to store the patch within,
        along with the accompanying metadata. This simulates a
        patch that originates from the PS API.
        """
        # Load the sample JSON data.
        f = open(os.path.join(os.getcwd(), "sample_files", "sampleJSZIP.json"), "r")
        sample_json = json.loads(f.read())
        f.close()

        # Load the sample zip binary data
        f = open(os.path.join(os.getcwd(), "sample_files", "sampleZIPBytes.bin"), "rb")
        sample_bytes = f.read()
        f.close()

        # Try to save a sample patch to the backend directory as if it originated from the PS API.
        util.save_to_backend((sample_bytes, sample_json))

        # Make sure the patch directory got created.
        self.assertTrue("124436" in os.listdir(testing_path), "The patch directory for patch 122661 was not found.")
        # Check the contents of the patch directory.
        for i in range(1, 10):
            self.assertTrue("124436_v{}.bin".format(i) in os.listdir(os.path.join(testing_path, "124436")),
                            "The expected patch file \"124436_v{}.bin\" was not found.".format(i))
            self.assertTrue("124436_v{}.json".format(i) in os.listdir(os.path.join(testing_path, "124436")),
                            "The expected patch file \"124436_v{}.json\" was not found.".format(i))
        # TODO fix the bytes so it doesn't cause the test to fail.
