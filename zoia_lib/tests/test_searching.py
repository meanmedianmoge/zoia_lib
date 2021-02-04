import json
import os
import shutil
import unittest

import zoia_lib.backend.utilities as util
from zoia_lib.common import errors

test_path = os.path.join(os.getcwd(), "zoia_lib", "tests")
data = None


# TODO Once done, explicitly call setUp and tearDown in each unittest
#  also don't forget to change the test_path


class TestSearching(unittest.TestCase):
    """This class is responsible for testing the various patch
    searching capabilities that are to be used by the application.

    Currently, the tests cover the following search types:
     - Search by title
     - Search by author
     - Search by tag
     - Search by category
     - Search by date modified (updated_at attribute)
    """

    def setUp(self):
        global data
        util.backend_path = test_path

        # Get the JSON metadata
        with open(os.path.join(test_path, "sample_files", "sampleMeta.json"), "r") as f:
            data = json.loads(f.read())

        for meta in data:
            util.save_to_backend((b"Test", meta))

    def tearDown(self):
        try:
            shutil.rmtree(os.path.join(test_path, "104273"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(test_path, "121123"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(test_path, "122243"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(test_path, "124566"))
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(os.path.join(test_path, "126563"))
        except FileNotFoundError:
            pass

    def test_search_edge_cases(self):
        """Test the edge cases of the searching method should it
        encounter unexpected input.
        """

        # Try to break the method.
        exc = errors.SearchingError

        self.assertTrue(
            util.search_patches(None, None) is None,
            "Expected None but got data in return.",
        )
        self.assertRaises(exc, util.search_patches, "Hi", "Yee")
        self.assertTrue(
            util.search_patches(None, "Hi") is None,
            "Expected None but got data in return.",
        )
        self.assertTrue(
            util.search_patches("", None) is None,
            "Expected None but got data in return.",
        )

    def test_title_search(self):
        """Attempts to search a dataset for a title attribute.
        This data must be collected beforehand, but that specific
        functionality is not being tested here.
        """

        global data

        # Normal search.
        result = util.search_patches(data, "loveless")

        self.assertTrue(
            result[0]["title"] == "LOVELESS",
            "Expected to find the patch titled LOVELESS but " "did not.",
        )
        self.assertTrue(
            len(result) == 1,
            "Returned search result should have " "only contained 1 result.",
        )

        # Normal search with a less precise search term.
        result = util.search_patches(data, "love")

        self.assertTrue(
            result[0]["title"] == "LOVELESS",
            "Expected to find the patch titled LOVELESS but " "did not.",
        )
        self.assertTrue(
            len(result) == 1,
            "Returned search result should have " "only contained 1 result.",
        )

        # Very low precision search. Multiple results expectd.
        result = util.search_patches(data, "lo")

        self.assertTrue(
            result[0]["title"] == "Dream Bender",
            "Expected to find the patch titled Dream Benders but " "did not.",
        )
        self.assertTrue(
            result[1]["title"] == "LOVELESS",
            "Expected to find the patch titled loveless but " "did not.",
        )
        self.assertTrue(
            len(result) == 2,
            "Returned search result should have " "only contained 2 result.",
        )

        # Try to search with a case mix.
        result = util.search_patches(data, "LOVEless")

        self.assertTrue(
            result[0]["title"] == "LOVELESS",
            "Expected to find the patch titled loveless but " "did not.",
        )
        self.assertTrue(
            len(result) == 1,
            "Returned search result should have " "only contained 1 result.",
        )

        # Only the ending.
        result = util.search_patches(data, "less")

        self.assertTrue(
            result[0]["title"] == "LOVELESS",
            "Expected to find the patch titled loveless but " "did not.",
        )
        self.assertTrue(
            len(result) == 1,
            "Returned search result should have " "only contained 1 result.",
        )

        # Try a different title
        result = util.search_patches(data, "dream")

        self.assertTrue(
            result[0]["title"] == "Dream Bender",
            "Expected to find the patch titled Dream Bender but " "did not.",
        )
        self.assertTrue(
            len(result) == 1,
            "Returned search result should have " "only contained 1 result.",
        )

    def test_author_search(self):
        """Attempts to search a dataset for an author attribute.
        This data must be collected beforehand, but that specific
        functionality is not being tested here.
        """

        global data

        pass

    def test_tag_search(self):
        """Attempts to search a dataset for a tag item.
        This data must be collected beforehand, but that specific
        functionality is not being tested here.
        """

        global data

        pass

    def test_category_search(self):
        """Attempts to search a dataset for a category item.
        This data must be collected beforehand, but that specific
        functionality is not being tested here.
        """

        global data

        pass

    def test_date_modified_search(self):
        """Attempts to search a dataset for a updated_at attribute.
        This data must be collected beforehand, but that specific
        functionality is not being tested here.
        """

        global data

        pass
