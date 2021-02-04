import io
import unittest
import zipfile

from zoia_lib.backend import api, patch_binary

ps = api.PatchStorage()


class FormatTest(unittest.TestCase):
    def test_bin_formatter(self):
        """Extract patch information from binary file"""

        f = ps.download("105634")
        self.assertTrue(
            isinstance(f[0], bytes),
            "Returned tuple did not contain binary data in the first element.",
        )
        self.assertTrue(
            isinstance(f[1], dict),
            "Returned tuple did not contain json data in the second element.",
        )

        size, name, n_mod = patch_binary.formatter(f[0])
        self.assertTrue(size == 908, "Binary size not returning as expected")
        self.assertTrue(
            name == "Am I Conscious", "Binary name not returning as expected"
        )
        self.assertTrue(n_mod == 31, "Binary n_mod not returning as expected")

    def test_zip_formatter(self):
        """Extract patch information from compressed drive"""

        f = ps.download("124436")

        # Given "z", a bytes object containing a ZIP file,
        # extract the data therein
        zf = zipfile.ZipFile(io.BytesIO(f[0]), "r")
        for name, info in zip(zf.namelist(), zf.infolist()):
            if ".txt" in name:
                continue
            byt = zf.read(info)
            # print(zf.read(fileinfo).decode('latin-1'))
            size, name, n_mod = patch_binary.formatter(byt)

            self.assertTrue(size == 2123, "Binary size not returning as expected")
            self.assertTrue(name == "Juniper", "Binary name not returning as expected")
            self.assertTrue(n_mod == 75, "Binary n_mod not returning as expected")
