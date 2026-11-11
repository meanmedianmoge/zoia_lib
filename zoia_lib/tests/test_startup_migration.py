import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from zoia_lib.interface.ZOIALibrarian_local import ZOIALibrarianLocal


class TestStartupMigration(unittest.TestCase):
    def test_unrelated_and_incomplete_folders_do_not_crash_startup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("sdcard", "123456"):
                folder = root / name
                folder.mkdir()
                (folder / "one.bin").write_bytes(b"one")
                (folder / "two.bin").write_bytes(b"two")
            for name, metadata in (("234567", {"files": []}), ("345678", {})):
                folder = root / name
                folder.mkdir()
                (folder / (name + ".json")).write_text(json.dumps(metadata))
                (folder / (name + ".bin")).write_bytes(b"patch")
            local = SimpleNamespace(path=directory, api=Mock())
            ZOIALibrarianLocal.alpha_to_beta(local)
            local.api.get_patch_meta.assert_not_called()
            self.assertEqual((root / "123456" / "one.bin").read_bytes(), b"one")

    def test_valid_legacy_patch_still_migrates(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "123456"
            folder.mkdir()
            metadata = folder / "123456.json"
            metadata.write_text(json.dumps({"files": [{"url": "https://example.invalid/alpha/patch.bin"}]}))
            (folder / "123456.bin").write_bytes(b"patch")
            current = {"files": [{"url": "https://example.invalid/beta/patch.bin"}]}
            local = SimpleNamespace(path=directory, api=Mock())
            local.api.get_patch_meta.return_value = current
            ZOIALibrarianLocal.alpha_to_beta(local)
            local.api.get_patch_meta.assert_called_once_with("123456")
            self.assertEqual(json.loads(metadata.read_text()), current)
