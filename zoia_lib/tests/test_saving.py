import json
import os
import shutil
import unittest

import zoia_lib.backend.utilities as util
from zoia_lib.common import errors

test_path = os.path.join(os.getcwd(), "zoia_lib", "tests")


class TestSaving(unittest.TestCase):
    """This class is responsible for testing the various patch
    saving methods that are to be used by the application.

    Currently, the tests cover the saving of both .bin and .zip files
    originating from the PS API and from a local user's
    computer and SD card.
    """

    def setUp(self):
        util.backend_path = test_path
        with open(
            os.path.join(test_path, "sample_files", "019_zoia_testpatch.bin"), "wb"
        ) as f:
            f.write(b"Test")

    def tearDown(self):
        try:
            shutil.rmtree(os.path.join(test_path, "122661"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(test_path, "124436"))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(test_path, "sample_files", "019_zoia_testpatch.bin"))
        except FileNotFoundError:
            pass

    def test_save_patch_api_bin(self):
        """Attempts to save a regular binary patch to the
        backend ZoiaLibraryApp directory. This requires the
        creation of a patch directory to store the patch within,
        along with the accompanying metadata. This simulates a
        patch that originates from the PS API.
        """

        self.setUp()

        # Can't use the usual add_test_patch method since that
        # functionality is what we are trying to test.

        # Load the sample JSON data.
        with open(os.path.join(test_path, "sample_files", "sampleJSON.json")) as f:
            sample_json = json.loads(f.read())

        # Try to break the method
        exc = (FileNotFoundError, errors.SavingError)
        self.assertRaises(exc, util.save_to_backend, (None, None))
        self.assertRaises(exc, util.save_to_backend, ("I am not a patch", None))
        self.assertRaises(exc, util.save_to_backend, (None, "Still not a patch"))
        self.assertRaises(exc, util.save_to_backend, (b"Test", "Still not a patch"))
        self.assertRaises(
            exc,
            util.save_to_backend,
            (None, {"id": 22222, "title": "Test", "created_at": "test"}),
        )
        self.assertRaises(
            exc, util.save_to_backend, ("IamNotAPatch", "Still not a patch")
        )
        self.assertRaises(
            exc,
            util.save_to_backend,
            ("IamNotAPatch", {"id": 22222, "title": "Test", "created_at": "test"}),
        )

        # Try to save a sample patch to the backend
        # directory as if it originated from the PS API.
        util.save_to_backend((b"TestPatch", sample_json))

        # Make sure the patch directory got created.
        self.assertTrue(
            "122661" in os.listdir(test_path),
            "The patch directory for patch 122661 was not found.",
        )
        # Check the contents of the patch directory.
        path = os.path.join(test_path, "122661")
        self.assertTrue(
            "122661.bin" in os.listdir(path),
            'The expected patch file "122661.bin" was not ' "found.",
        )
        self.assertTrue(
            "122661.json" in os.listdir(path),
            'The expected patch file "122661.json" was not ' "found.",
        )

        # Try to same the same patch again
        # (should fail, since the binary has not changed).
        self.assertRaises(exc, util.save_to_backend, (b"TestPatch", sample_json))

        # Try to save a different patch with the same id (should
        # correctly make a new version since the binary has changed).
        util.save_to_backend((b"TestDifferentBinary", sample_json))
        # Check the contents of the patch directory and ensure the
        # revision numbers were updated correctly.
        for i in range(1, 3):
            self.assertTrue(
                "122661_v{}.bin".format(i) in os.listdir(path),
                'The expected patch file "122661_v{}.bin" was ' "not found.".format(i),
            )
            self.assertTrue(
                "122661_v{}.json".format(i) in os.listdir(path),
                'The expected patch file "122661_v{}.json" was ' "not found.".format(i),
            )
            with open(
                os.path.join(test_path, "122661", "122661_v{}.json".format(i)), "r"
            ) as f:
                jf = json.loads(f.read())

            self.assertTrue(
                jf["revision"] == i,
                "The expected revision number for "
                '"122661_v{}.json" was not found (Got {} and '
                "expected {}).".format(i, jf["revision"], i),
            )

        # Try to save a different patch with the same id again
        # (should correctly make a new version since the binary has changed).
        util.save_to_backend((b"TestDifferentBinaryAgain", sample_json))
        # Check the contents of the patch directory and ensure the
        # revision numbers were updated correctly.
        for i in range(1, 4):
            self.assertTrue(
                "122661_v{}.bin".format(i) in os.listdir(path),
                'The expected patch file "122661_v{}.bin" was ' "not found.".format(i),
            )
            self.assertTrue(
                "122661_v{}.json".format(i) in os.listdir(path),
                'The expected patch file "122661_v{}.json" was ' "not found.".format(i),
            )
            with open(
                os.path.join(test_path, "122661", "122661_v{}.json".format(i)), "r"
            ) as f:
                jf = json.loads(f.read())

            self.assertTrue(
                jf["revision"] == i,
                "The expected revision number for "
                '"122661_v{}.json" was not found (Got {} and '
                "expected {}).".format(i, jf["revision"], i),
            )

        self.tearDown()

    def test_save_patch_api_compressed(self):
        """Attempts to save a regular compressed patch to the
        backend ZoiaLibraryApp directory. This requires the
        creation of a patch directory to store the patch within,
        along with the accompanying metadata. This simulates a
        patch that originates from the PS API.
        """

        self.setUp()

        # Load the sample JSON data.
        with open(
            os.path.join(test_path, "sample_files", "sampleJSONZIP.json"), "r"
        ) as f:
            sample_json = json.loads(f.read())

        # Load the sample zip binary data
        with open(
            os.path.join(test_path, "sample_files", "sampleZIPBytes.bin"), "rb"
        ) as f:
            sample_bytes = f.read()

        # Try to save a sample patch to the backend directory as
        # if it originated from the PS API.
        util.save_to_backend((sample_bytes, sample_json))

        # Make sure the patch directory got created.
        self.assertTrue(
            "124436" in os.listdir(test_path),
            "The patch directory for patch 122661 was not found.",
        )
        # Check the contents of the patch directory and ensure
        # the revision numbers were updated correctly.
        for i in range(1, 11):
            self.assertTrue(
                "124436_v{}.bin".format(i)
                in sorted(os.listdir(os.path.join(test_path, "124436"))),
                'The expected patch file "124436_v{}.bin" was ' "not found.".format(i),
            )
            self.assertTrue(
                "124436_v{}.json".format(i)
                in sorted(os.listdir(os.path.join(test_path, "124436"))),
                'The expected patch file "124436_v{}.json" was ' "not found.".format(i),
            )
            with open(
                os.path.join(test_path, "124436", "124436_v{}.json".format(i)), "r"
            ) as f:
                jf = json.loads(f.read())

            self.assertTrue(
                jf["revision"] == i,
                "The expected revision number for "
                '"124436_v{}.json" was not found (Got {} and '
                "expected {}).".format(i, jf["revision"], i),
            )

        # Try to same the same patch again
        # (should fail, since the binary has not changed).
        with open(
            os.path.join(test_path, "sample_files", "sampleJSONZIP.json"), "r"
        ) as f:
            sample_json = json.loads(f.read())
        exc = (FileNotFoundError, errors.SavingError)
        self.assertRaises(exc, util.save_to_backend, (sample_bytes, sample_json))

        # TODO Test other compression algorithms

        self.tearDown()

    def test_save_patch_local_bin(self):
        """Attempts to save a regular binary patch to the
        backend ZoiaLibraryApp directory. This requires the
        creation of a patch directory to store the patch within,
        along with the accompanying metadata. This simulates a
        patch that originates from a user's machine or from an SD card.
        """

        self.setUp()

        # Try to break the method.
        exc = (FileNotFoundError, errors.SavingError)
        self.assertRaises(exc, util.import_to_backend, None)
        self.assertRaises(exc, util.import_to_backend, "I am not a patch")

        # Try to save an imported patch.
        util.import_to_backend(
            os.path.join(test_path, "sample_files", "019_zoia_testpatch.bin")
        )

        # Try to import it again (should fail, since it is already saved).
        self.assertRaises(
            exc,
            util.import_to_backend,
            os.path.join(test_path, "sample_files", "019_zoia_testpatch.bin"),
        )

        # Unfortunately, the id is random, so we need to find it to remove it.
        count = 0
        for file in os.listdir(test_path):
            if len(file) == 5:
                count += 1
                self.assertTrue(
                    len(os.listdir(os.path.join(test_path, file))) == 2,
                    "The locally imported patch did not "
                    "successfully create the two expected files "
                    "(.bin and .json).",
                )
                with open(
                    os.path.join(test_path, file, "{}.json".format(file)), "r"
                ) as f:
                    meta_check = json.loads(f.read())

                self.assertTrue(
                    "id" in meta_check, "JSON data didn't contain the id attribute."
                )
                self.assertTrue(
                    "created_at" in meta_check,
                    "JSON data didn't contain the created_at " "attribute.",
                )
                self.assertTrue(
                    "files" in meta_check,
                    "JSON data didn't contain the files " "attribute.",
                )
                self.assertTrue(
                    meta_check["files"][0]["filename"] == "019_zoia_testpatch.bin",
                    "The filename attribute did not match the " "expected file name.",
                )
                self.assertTrue(
                    "updated_at" in meta_check,
                    "JSON data didn't contain the updated_at " "attribute.",
                )
                self.assertTrue(
                    "title" in meta_check,
                    "JSON data didn't contain the title " "attribute.",
                )
                self.assertTrue(
                    "revision" in meta_check,
                    "JSON data didn't contain the revision " "attribute.",
                )
                # Cleanup
                shutil.rmtree(os.path.join(test_path, file))
                break

        self.assertTrue(
            count == 1,
            "Did not find exactly 1 patch directory"
            "with a 5-digit identification number.",
        )

        self.tearDown()

    def test_save_patch_local_compressed(self):
        """Attempts to save a regular compressed patch to the
        backend ZoiaLibraryApp directory. This requires the
        creation of a patch directory to store the patch within,
        along with the accompanying metadata. This simulates a
        patch that originates from a user's machine or from an SD card.
        """
        pass
