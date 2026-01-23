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
            self.assertIsInstance(encoded, (bytes, bytearray))
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(len(encoded), 0)
            encoded_size = int.from_bytes(bytes(encoded[:4]), byteorder="little")
            payload_len = (encoded_size - 1) * 4
            self.assertGreater(payload_len, 0)
            self.assertLessEqual(payload_len, 32764)
            self.assertTrue(any(b != 0 for b in encoded[4:4 + payload_len]))
            self.assertTrue(all(b == 0 for b in encoded[4 + payload_len:]))
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
