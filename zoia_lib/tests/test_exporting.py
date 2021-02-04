import json
import os
import shutil
import unittest

import zoia_lib.backend.utilities as util

test_path = os.path.join(os.getcwd(), "zoia_lib", "tests")


class TestExporting(unittest.TestCase):
    """This class is responsible for testing the various patch
    exporting methods that are to be used by the application.

    Currently, the tests cover
    """

    def setUp(self):
        util.backend_path = test_path
        # Create a patch to export.
        sample_bytes = b"test"
        with open(os.path.join(test_path, "sample_files", "sampleJSON.json")) as f:
            sample_json = json.loads(f.read())
        util.save_to_backend((sample_bytes, sample_json))

    def tearDown(self):
        try:
            shutil.rmtree(os.path.join(test_path, "122661"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(test_path, "007_zoia_dream_mender.bin"))
        except FileNotFoundError:
            pass

    def test_export_to_sd_bin(self):
        """Attempts to export a patch that has been saved to
        the backend ZoiaLibraryApp directory to an SD card that has
        been inserted into the system.
        """

        # TODO Make this a lot more robust.
        util.export_patch_bin("122661", test_path, 7)

        self.assertTrue(
            "007_zoia_dream_mender.bin" in os.listdir(test_path),
            "Did not find a properly exported patch when it should"
            "have been created correctly.",
        )
