class ZoiaLibError(Exception):
    """Base Error Class for zoia_lib. Inherited by all other errors."""

    pass


class BadPathError(ZoiaLibError):
    """Class raised when the file path is not valid."""

    def __init__(self, path: str):
        print(f'Path {path} did not lead to a file or directory.')


class SavingError(ZoiaLibError):
    """Class raised when a file could not be saved to the backend directories."""

    def __init__(self):
        print(f'Could not save the file to the backend LibraryApp directory.')


class DeletionError(ZoiaLibError):
    """Class raised when a file could not be deleted from the backend directories."""

    def __init__(self, patch: str):
        print(f'Could not delete the file {patch} from the backend LibraryApp directory.')
