import json
import os
import unittest

import zoia_lib.backend.utilities as util
import zoia_lib.common.errors as errors

test_path = os.path.join(os.getcwd(), "zoia_lib", "tests")


class TestSorting(unittest.TestCase):
    """ This class is responsible for testing the various patch
    sorting methods that are to be used by the application.

    Currently, the tests cover the following sorting methods:
     - By title
     - By author
     - By like count
     - By download count
     - By view count
     - By date modified
    """

    def test_sort_edge_cases(self):
        # Try to break the method.
        exc = errors.SortingError

        self.assertTrue(util.sort_metadata(None, None, None) is None,
                        "Expected None but got data in return.")
        self.assertRaises(exc, util.sort_metadata, -1, [{"Hi"}], False)
        self.assertTrue(util.sort_metadata(3, None, True) is None,
                        "Expected None but got data in return.")
        self.assertTrue(util.sort_metadata(4, [{"Hello"}], None) is None,
                        "Expected None but got data in return.")
        self.assertRaises(exc, util.sort_metadata, 5, "Nope", True)

    def test_title_sort(self):
        # Get the JSON metadata
        with open(os.path.join(test_path, "sample_files",
                               "sampleMetaSorting.json"), "r") as f:
            data = json.loads(f.read())

        # Sort by title in lexicographical order.
        util.sort_metadata(1, data, False)
        self.assertTrue(data[0]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 0")
        self.assertTrue(data[1]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 1")
        self.assertTrue(data[2]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 2")
        self.assertTrue(data[3]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 3")
        self.assertTrue(data[4]["title"] == "Upward",
                        "Sorted data did not have Upward in position 4")

        # Sort by title in reverse lexicographical order.
        util.sort_metadata(1, data, True)
        self.assertTrue(data[0]["title"] == "Upward",
                        "Sorted data did not have Upward in position 0")
        self.assertTrue(data[1]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 1")
        self.assertTrue(data[2]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 2")
        self.assertTrue(data[3]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 3")
        self.assertTrue(data[4]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 4")

    def test_author_sort(self):
        # Get the JSON metadata
        with open(os.path.join(test_path, "sample_files",
                               "sampleMetaSorting.json"), "r") as f:
            data = json.loads(f.read())

        # Sort by author in lexicographical order.
        # Verification is still by title, but that is for simplicity.
        util.sort_metadata(2, data, False)
        self.assertTrue(data[0]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 4")
        self.assertTrue(data[1]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 0")
        self.assertTrue(data[2]["title"] == "Upward",
                        "Sorted data did not have Upward in position 1")
        self.assertTrue(data[3]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 2")
        self.assertTrue(data[4]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 3")

        # Sort by author in reverse lexicographical order.
        util.sort_metadata(2, data, True)
        self.assertTrue(data[0]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 1")
        self.assertTrue(data[1]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 2")
        self.assertTrue(data[2]["title"] == "Upward",
                        "Sorted data did not have Upward in position 3")
        self.assertTrue(data[3]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 4")
        self.assertTrue(data[4]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 0")

    def test_like_count_sort(self):
        # Get the JSON metadata
        with open(os.path.join(test_path, "sample_files",
                               "sampleMetaSorting.json"), "r") as f:
            data = json.loads(f.read())

        util.sort_metadata(3, data, False)
        self.assertTrue(data[0]["title"] == "Upward",
                        "Sorted data did not have Upward in position 0")
        self.assertTrue(data[1]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 1")
        self.assertTrue(data[2]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 2")
        self.assertTrue(data[3]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 3")
        self.assertTrue(data[4]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 4")

        util.sort_metadata(3, data, True)
        self.assertTrue(data[0]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 0")
        self.assertTrue(data[1]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 1")
        self.assertTrue(data[2]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 2")
        self.assertTrue(data[3]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 3")
        self.assertTrue(data[4]["title"] == "Upward",
                        "Sorted data did not have Upward in position 4")

    def test_download_count_sort(self):
        # Get the JSON metadata
        with open(os.path.join(test_path, "sample_files",
                               "sampleMetaSorting.json"), "r") as f:
            data = json.loads(f.read())

        util.sort_metadata(4, data, False)
        self.assertTrue(data[0]["title"] == "Upward",
                        "Sorted data did not have Upward in position 0")
        self.assertTrue(data[1]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 1")
        self.assertTrue(data[2]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 2")
        self.assertTrue(data[3]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 3")
        self.assertTrue(data[4]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 4")

        util.sort_metadata(4, data, True)
        self.assertTrue(data[0]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 0")
        self.assertTrue(data[1]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 1")
        self.assertTrue(data[2]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 2")
        self.assertTrue(data[3]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 3")
        self.assertTrue(data[4]["title"] == "Upward",
                        "Sorted data did not have Upward in position 4")

    def test_view_count_sort(self):
        # Get the JSON metadata
        with open(os.path.join(test_path, "sample_files",
                               "sampleMetaSorting.json"), "r") as f:
            data = json.loads(f.read())

        util.sort_metadata(5, data, False)
        self.assertTrue(data[0]["title"] == "Upward",
                        "Sorted data did not have Upward in position 0")
        self.assertTrue(data[1]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 1")
        self.assertTrue(data[2]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 2")
        self.assertTrue(data[3]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 3")
        self.assertTrue(data[4]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 4")

        util.sort_metadata(5, data, True)
        self.assertTrue(data[0]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 0")
        self.assertTrue(data[1]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 1")
        self.assertTrue(data[2]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 2")
        self.assertTrue(data[3]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 3")
        self.assertTrue(data[4]["title"] == "Upward",
                        "Sorted data did not have Upward in position 4")

    def test_date_sort(self):
        # Get the JSON metadata
        with open(os.path.join(test_path, "sample_files",
                               "sampleMetaSorting.json"), "r") as f:
            data = json.loads(f.read())

        # Sort by date_modified in lexicographical order.
        # Verification is still by title, but that is for simplicity.
        util.sort_metadata(6, data, False)
        self.assertTrue(data[0]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 0")
        self.assertTrue(data[1]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 1")
        self.assertTrue(data[2]["title"] == "Upward",
                        "Sorted data did not have Upward in position 2")
        self.assertTrue(data[3]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 3")
        self.assertTrue(data[4]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 4")

        # Sort by date_modified in reverse lexicographical order.
        util.sort_metadata(6, data, True)
        self.assertTrue(data[0]["title"] == "Dream Bender",
                        "Sorted data did not have Dream Bender in position 0")
        self.assertTrue(data[1]["title"] == "LOVELESS",
                        "Sorted data did not have LOVELESS in position 1")
        self.assertTrue(data[2]["title"] == "Upward",
                        "Sorted data did not have Upward in position 2")
        self.assertTrue(data[3]["title"] == "GOLDFINGER (Golden Ratio)",
                        "Sorted data did not have GOLDFINGER in position 3")
        self.assertTrue(data[4]["title"] == "Subtle Knife",
                        "Sorted data did not have Subtle Knife in position 4")
