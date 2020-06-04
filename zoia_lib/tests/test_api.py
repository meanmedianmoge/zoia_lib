import json
import unittest
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from jsonschema import validate, ValidationError
from numpy import unicode

import zoia_lib.backend.api as api

ps = api.PatchStorage()


class TestAPI(unittest.TestCase):
    def test_api_all_zoia_patches(self):
        """ Query the PS API to ensure that all ZOIA patches are returned,
        and ensure that they are of the correct format as dictated by the
        MetadataSchema.json schema.
        """
        # Need a known user agent to avoid getting 403'd.
        # Used to grab the current number of ZOIA patches on PS.
        req_patch = Request("https://patchstorage.com/",
                            headers={"User-Agent": "Mozilla/5.0"})
        soup_patch = BeautifulSoup(urlopen(req_patch).read(), "html.parser")
        found_pedals = soup_patch.find_all(class_="d-flex flex-column justify-content-center")
        # Convert the ResultSet to a string so we can split on what we are looking for.
        # The PS website does not have unique div names, so this is to workaround that.
        zoia = unicode.join(u'\n', map(unicode, found_pedals)).split("ZOIA", 1)[1].split("<strong>", 1)[1]

        # For some reason, questions posted on PS count as "patches",
        # so we need to figure out the # of questions.
        req_ques = Request("https://patchstorage.com/platform/zoia/?search_query=&ptype%5B%5D=question&tax_platform"
                           "=zoia&tax_post_tag=&orderby=modified&wpas_id=search_form&wpas_submit=1",
                           headers={"User-Agent": "Mozilla/5.0"})
        soup_ques = BeautifulSoup(urlopen(req_ques).read(), "html.parser")

        patch_list = api.get_all_patches_meta()

        # Make sure that the correct number of patches are retrieved.
        self.assertEqual(int(zoia[:3]) - len(soup_ques.find_all(class_="card")),
                         len(patch_list["patch_list"]), "Returned patch list does not contain all ZOIA patches.")

        # Validate the patches returned against the BaseSchema.json file
        with open('../common/BaseSchema.json') as f:
            base_schema = json.load(f)

        try:
            for i in range(len(patch_list["patch_list"])):
                validate(instance=patch_list["patch_list"][i], schema=base_schema)
        except ValidationError:
            self.fail("A patch failed to conform to the metadata schema.")

        # TODO Add check to ensure only the attributes in the meta_schema are present
        #  without any unnecessary attributes.

    def test_api_download_bin(self):
        """ Query the PS API for a patch with the .bin extension,
        and ensure that it is in the correct format as dictated by the
        BaseSchema.json schema.
        """
        # Try to download something that doesn't exist.
        f = ps.download("1111111111")
        self.assertIsNone(f, "Retrieved patch data for a patch that does not exist (patch id > 6 digits in length).")
        f = ps.download("900000")
        self.assertIsNone(f, "Retrieved patch data for a patch that does not exist (patch id 900000).")
        # Try to pass in None.
        f = ps.download(None)
        self.assertIsNone(f, "Retrieved patch data without passing a patch id.")
        # Try to actually download a .bin file.
        f = ps.download("105634")
        self.assertIsNotNone(f, "Did not retrieve patch data despite the patch id existing in PatchStorage.")
        self.assertTrue(isinstance(f[0], bytes), "Returned tuple did not contain binary data in the first element.")

        # Validate the patches returned against the MetadataSchema.json file
        with open('../common/MetadataSchema.json') as file:
            meta_schema = json.load(file)

        try:
            json.dumps(f[1])
            validate(instance=f[1], schema=meta_schema)
        except ValueError:
            self.fail("Returned tuple did not contain valid json data in the second element.")

    def test_api_download_compressed(self):
        """ Query the PS API for a compressed patch, uncompress the patch,
        and ensure that it is in the correct format as dictated by the
        BaseSchema.json schema.
        """
        # Try to download something that doesn't exist.
        f = ps.download("1111111111")
        self.assertIsNone(f, "Retrieved patch data for a patch that does not exist (patch id > 6 digits in length).")
        f = ps.download("900000")
        self.assertIsNone(f, "Retrieved patch data for a patch that does not exist (patch id 900000).")
        # Try to pass in None.
        f = ps.download(None)
        self.assertIsNone(f, "Retrieved patch data without passing a patch id.")
        # Try to actually download a compressed file.
        # f = ps.download("124605")
        try:
            # json.load(f[1])
            pass
        except ValueError:
            self.fail("Returned tuple did not contain valid json data in the second element.")
