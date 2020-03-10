
import os
import unittest

from zoia_lib.renumber import Renumber

# Renumber changes the pwd so we save where we started here.
THIS_DIR = os.path.dirname(__file__)
TEST_RELATIVE_PATH = 'test_files/'
RENUMBER_RELATIVE_PATH = 'zoia_lib/tests/test_files/'
PATH = os.path.join(THIS_DIR, TEST_RELATIVE_PATH)
TEST_FILE_NAMES = [
    '018_zoia_Afterneath_V4.bin',
    '057_zoia_Fading_Dream1_1.bin'
]


class TestRenumber(unittest.TestCase):

    def setUp(self):
        [open(os.path.join(PATH, f), 'a').close() for f in TEST_FILE_NAMES]

    def tearDown(self):
        [os.remove(os.path.join(PATH, f)) for f in os.listdir(PATH)]

    def test_renumber_alpha(self):
        renumber = Renumber(path=RENUMBER_RELATIVE_PATH)
        # reorder test files
        renumber.renumber(sort='alpha')
        # get results
        # os.listdir() does not return directory contents in any order.
        # the list comprehension is to exclude any hidden files (.DS_Store)
        result = sorted([f for f in os.listdir(PATH) if not f.startswith('.')])
        expected_result = [
            '000_zoia_Afterneath_V4.bin',
            '001_zoia_Fading_Dream1_1.bin'
        ]
        self.assertListEqual(result, expected_result)

    def test_renumber_alpha_invert(self):
        renumber = Renumber(path=RENUMBER_RELATIVE_PATH)
        # reorder test files
        renumber.renumber(sort='alpha_invert')
        # get results
        # os.listdir() does not return directory contents in any order.
        # the list comprehension is to exclude any hidden files (.DS_Store)
        result = sorted([f for f in os.listdir(PATH) if not f.startswith('.')])
        expected_result = [
            '000_zoia_Fading_Dream1_1.bin',
            '001_zoia_Afterneath_V4.bin'
        ]
        self.assertListEqual(result, expected_result)

    def test_handles_duplicate_filenames(self):
        # add some more files including dupes
        test_filenames = [
            '007_zoia_Afterneath_V4.bin',
            '056_zoia_Fading_Dream1_1.bin',
            '003_zoia_some_other_file_name.bin',
            '004_zoia_file_name.bin'
        ]
        [open(os.path.join(PATH, f), 'a').close() for f in test_filenames]
        renumber = Renumber(path=RENUMBER_RELATIVE_PATH)
        renumber.renumber(sort='alpha')
        # os.listdir() does not return directory contents in any order.
        # the list comprehension is to exclude any hidden files (.DS_Store)
        result = sorted([f for f in os.listdir(PATH) if not f.startswith('.')])
        expected = [
            '000_zoia_Afterneath_V4.bin',
            '001_zoia_Afterneath_V4.bin',
            '002_zoia_Fading_Dream1_1.bin',
            '003_zoia_Fading_Dream1_1.bin',
            '004_zoia_file_name.bin',
            '005_zoia_some_other_file_name.bin'
        ]
        self.assertListEqual(result, expected)

    def test_handles_dupes_after_multiple_sorts(self):
        test_filenames = [
            '007_zoia_Afterneath_V4.bin',
            '056_zoia_Fading_Dream1_1.bin',
            '003_zoia_some_other_file_name.bin',
            '004_zoia_file_name.bin'
        ]
        [open(os.path.join(PATH, f), 'a').close() for f in test_filenames]
        renumber = Renumber(path=RENUMBER_RELATIVE_PATH)
        renumber.renumber(sort='alpha')
        renumber.renumber(sort='alpha')
        result = sorted([f for f in os.listdir(PATH) if not f.startswith('.')])
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
        renumber = Renumber(path=RENUMBER_RELATIVE_PATH)
        # reorder test files
        renumber.renumber(sort='random')
        # os.listdir() does not return directory contents in any order.
        # the list comprehension is to exclude any hidden files (.DS_Store)
        result = sorted([f for f in os.listdir(PATH) if not f.startswith('.')])
        # we can't assert that the results are truly random, but we can
        # at least make sure the numbering worked :)
        self.assertEqual('000', result[0].split('_')[0])
        self.assertEqual('001', result[1].split('_')[0])
