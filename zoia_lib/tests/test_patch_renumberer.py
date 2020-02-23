
import os
import unittest

from zoia_lib.patch_renumberer import Renumber

# Renumber changes the pwd so we save where we started here.
START_PATH = os.getcwd()
TEST_PATH = 'zoia_lib/tests/test_files/'
TEST_FILE_NAMES = [
    '018_zoia_Afterneath_V4.bin',
    '057_zoia_Fading_Dream1_1.bin'
]


class TestRenumber(unittest.TestCase):

    def setUp(self):
        os.chdir(START_PATH)
        # save starting directory
        # create dummy files
        [open(f'{TEST_PATH}{f}', 'a').close() for f in TEST_FILE_NAMES]

    def tearDown(self):
        # reset directory
        os.chdir(START_PATH)
        os.chdir(TEST_PATH)
        # remove renamed files -- this is pretty janky if the path isn't right!
        [os.remove(f)for f in os.listdir()]

    def test_renumber_alpha(self):
        renumber = Renumber(path=TEST_PATH)
        # reorder test files
        renumber.renumber(sort='alpha')
        # get results
        result = sorted(os.listdir())
        expected_result = [
            '000_zoia_Afterneath_V4.bin',
            '001_zoia_Fading_Dream1_1.bin'
        ]
        self.assertListEqual(result, expected_result)

    def test_handles_duplicate_filenames(self):
        # add some more files including dupes
        test_filenames = [
            '007_zoia_Afterneath_V4.bin',
            '056_zoia_Fading_Dream1_1.bin'
            '003_zoia_some_other_file_name.bin',
            '004_zoia_file_name.bin'
        ]
        [open(f'{TEST_PATH}{f}', 'a').close() for f in test_filenames]
        renumber = Renumber(path=TEST_PATH)
        renumber.renumber(sort='alpha')
        result = sorted(os.listdir())
        expected = [
            '000_zoia_Afterneath_V4.bin',
            '001_zoia_Afterneath_V4.bin',
            '002_zoia_Fading_Dream1_1.bin',
            '003_zoia_Fading_Dream1_1.bin',
            '004_zoia_file_name.bin',
            '005_zoia_some_other_file_name.bin'
        ]
        self.assertListEqual(result, expected)

    def test_renumber_random(self):
        renumber = Renumber(path=TEST_PATH)
        # reorder test files
        renumber.renumber(sort='random')
        # get results
        result = sorted(os.listdir())
        # we can't assert that the results are truly random, but we can
        # at least make sure the numbering worked :)
        self.assertEqual('000', result[0].split('_')[0])
        self.assertEqual('001', result[1].split('_')[0])
