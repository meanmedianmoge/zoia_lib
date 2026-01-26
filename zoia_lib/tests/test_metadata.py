import json
import os
import shutil
import unittest

from zoia_lib.backend.patch_save import PatchSave


test_path = os.path.join(os.getcwd(), "zoia_lib", "tests", "tmp_meta")


class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.save = PatchSave()
        self.save.back_path = test_path
        os.makedirs(test_path, exist_ok=True)

        with open(
            os.path.join(os.getcwd(), "zoia_lib", "tests", "sample_files", "sampleJSON.json")
        ) as f:
            self.sample_json = json.loads(f.read())

        os.makedirs(os.path.join(test_path, str(self.sample_json["id"])), exist_ok=True)

    def tearDown(self):
        try:
            shutil.rmtree(test_path)
        except FileNotFoundError:
            pass

    def test_metadata_creation(self):
        metadata = json.loads(json.dumps(self.sample_json))
        self.save.save_metadata_json(metadata)
        meta_path = os.path.join(
            test_path,
            str(self.sample_json["id"]),
            "{}.json".format(self.sample_json["id"]),
        )
        self.assertTrue(os.path.exists(meta_path))

        with open(meta_path, "r") as f:
            saved = json.loads(f.read())

        self.assertIn("rating", saved)
        self.assertIn("downloaded_at", saved)
        self.assertEqual(saved["rating"], 0)

        metadata = json.loads(json.dumps(self.sample_json))
        self.save.save_metadata_json(metadata, version=2)
        meta_path = os.path.join(
            test_path,
            str(self.sample_json["id"]),
            "{}_v2.json".format(self.sample_json["id"]),
        )
        with open(meta_path, "r") as f:
            saved_versioned = json.loads(f.read())
        self.assertEqual(saved_versioned["revision"], 2)
