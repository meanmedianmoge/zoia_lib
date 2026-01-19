import os
import unittest

from zoia_lib.backend.patch_binary import PatchBinary
from zoia_lib.backend.patch_encode import PatchEncoder


class EncodeDecodeRoundtripTest(unittest.TestCase):
    def test_roundtrip_bin_matches_source(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        test_dir = os.path.join(root_dir, "zoia_lib", "tests", "sample_files")
        sample_path = os.path.join(test_dir, "input_test.bin")

        with open(sample_path, "rb") as f:
            original = f.read()

        decoded = PatchBinary().parse_data(original)
        output_path = os.path.join(test_dir, "output_test.bin")
        try:
            encoded = PatchEncoder().encode(decoded, output_path=output_path)
            self.assertEqual(
                original,
                bytes(encoded),
                "Re-encoded binary did not match original sample patch.",
            )
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
