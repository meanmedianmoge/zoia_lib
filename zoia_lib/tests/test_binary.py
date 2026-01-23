import io
import os
import unittest
import zipfile

from zoia_lib.backend.patch_binary import PatchBinary


class FormatTest(unittest.TestCase):
    def test_bin_formatter(self):
        """Extract patch information from binary file"""

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        test_dir = os.path.join(root_dir, "zoia_lib", "tests", "sample_files")
        sample_path = os.path.join(test_dir, "input_test.bin")

        with open(sample_path, "rb") as f:
            byt = f.read()

        parsed = PatchBinary().parse_data(byt)
        self.assertIsInstance(parsed, dict)
        self.assertIn("modules", parsed)
        self.assertTrue(parsed["modules"], "Parsed patch should include modules.")
        self.assertIn("pages_count", parsed)
        self.assertEqual(parsed["pages_count"], len(parsed["pages"]))
        self.assertIn("header_color_id", parsed["modules"][0])

    def test_zip_formatter(self):
        """Extract patch information from compressed drive"""

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        test_dir = os.path.join(root_dir, "zoia_lib", "tests", "sample_files")
        sample_path = os.path.join(test_dir, "sampleZIPBytes.bin")

        with open(sample_path, "rb") as f:
            zip_bytes = f.read()

        zf = zipfile.ZipFile(io.BytesIO(zip_bytes), "r")
        bin_entries = [name for name in zf.namelist() if name.endswith(".bin")]
        self.assertTrue(bin_entries, "Expected at least one .bin in sample zip.")
        byt = zf.read(bin_entries[0])

        parsed = PatchBinary().parse_data(byt)
        self.assertIsInstance(parsed, dict)
        self.assertIn("modules", parsed)
        self.assertTrue(parsed["modules"], "Parsed patch should include modules.")
