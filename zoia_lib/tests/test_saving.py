import json
import os
import shutil
import tempfile
from pathlib import Path
import unittest

from zoia_lib.backend.patch_save import PatchSave
from zoia_lib.backend import utilities as util
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
        self.save = PatchSave()
        self.save.back_path = test_path
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
        self.assertRaises(exc, self.save.save_to_backend, (None, None))
        self.assertRaises(exc, self.save.save_to_backend, ("I am not a patch", None))
        self.assertRaises(exc, self.save.save_to_backend, (None, "Still not a patch"))
        self.assertRaises(exc, self.save.save_to_backend, (b"Test", "Still not a patch"))
        self.assertRaises(
            exc,
            self.save.save_to_backend,
            (None, {"id": 22222, "title": "Test", "created_at": "test"}),
        )
        self.assertRaises(
            exc, self.save.save_to_backend, ("IamNotAPatch", "Still not a patch")
        )
        self.assertRaises(
            exc,
            self.save.save_to_backend,
            ("IamNotAPatch", {"id": 22222, "title": "Test", "created_at": "test"}),
        )

        # Try to save a sample patch to the backend
        # directory as if it originated from the PS API.
        self.save.save_to_backend((b"TestPatch", sample_json))

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
        self.assertRaises(exc, self.save.save_to_backend, (b"TestPatch", sample_json))

        # Try to save a different patch with the same id (should
        # correctly make a new version since the binary has changed).
        self.save.save_to_backend((b"TestDifferentBinary", sample_json))
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
        self.save.save_to_backend((b"TestDifferentBinaryAgain", sample_json))
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
        self.save.save_to_backend((sample_bytes, sample_json))

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
        self.assertRaises(exc, self.save.save_to_backend, (sample_bytes, sample_json))

        # TODO Test other compression algorithms

        self.tearDown()

    def test_import_patch_local_bin(self):
        """Import a local/SD binary, generate metadata, and reject duplicates."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            library = root / "library"
            library.mkdir()
            source = root / "019_zoia_testpatch.bin"
            original_bytes = (Path(test_path) / "sample_files" / "input_test.bin").read_bytes()
            source.write_bytes(original_bytes)
            self.save.back_path = str(library)

            self.save.import_to_backend(str(source), disable_auto_ps_link=True)

            patches = list(library.iterdir())
            self.assertEqual(len(patches), 1)
            patch_dir = patches[0]
            patch_id = patch_dir.name
            self.assertTrue(patch_id.isdigit())
            self.assertEqual(len(patch_id), 5)
            self.assertEqual(
                {file.name for file in patch_dir.iterdir()},
                {patch_id + ".bin", patch_id + ".json"},
            )
            self.assertEqual((patch_dir / (patch_id + ".bin")).read_bytes(), original_bytes)
            metadata = json.loads((patch_dir / (patch_id + ".json")).read_text())
            self.assertEqual(str(metadata["id"]), patch_id)
            self.assertEqual(metadata["title"], "testpatch")
            self.assertEqual(metadata["files"][0]["filename"], source.name)
            self.assertEqual(metadata["revision"], "1")
            for key in ("created_at", "updated_at", "downloaded_at"):
                self.assertIsInstance(metadata[key], str)
                self.assertTrue(metadata[key])

            with self.assertRaises(errors.SavingError) as duplicate:
                self.save.import_to_backend(str(source), disable_auto_ps_link=True)
            self.assertEqual(duplicate.exception.error_code, 503)
            self.assertEqual(list(library.iterdir()), patches)
            self.assertEqual(source.read_bytes(), original_bytes)
            self.assertEqual((patch_dir / (patch_id + ".bin")).read_bytes(), original_bytes)
