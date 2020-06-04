import unittest


class DeletionTest(unittest.TestCase):
    def test_delete_patch_normal(self):
        """ Attempt to delete a patch that is stored in the
        backend LibraryApp directory. The test ensures that
        the patch and metadata are deleted.
        """
        pass

    def test_delete_patch_version(self):
        """ Attempt to delete a patch that is stored in the
        backend LibraryApp directory. This specific patch is
        contained within a version directory. The test ensures
        that  the patch and metadata are deleted. It also
        ensures only the correct version of a patch is deleted.

        Should the deletion result in a version directory with only
        one version remaining, the patch and metadata should be
        moved back to the parent LibraryApp directory and the
        version directory should be deleted. The patch and metadata
        should be renamed appropriately.
        """
        pass
