class ZoiaLibError(Exception):
    """Base Error Class for zoia_lib. Inherited by all other errors."""

    pass


class BadPathError(ZoiaLibError):
    """Class raised when the file path is not valid."""

    def __init__(self, path: str):
        print(f'Path {path} did not lead to a file or directory.')


class SavingError(ZoiaLibError):
    """Class raised when a file could not be saved to the backend directories."""

    def __init__(self, patch: str):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        else:
            print(f'Could not save the file {patch} from the backend ZoiaLibraryApp directory due '
                  f'to a data formatting error (was the JSON and binary valid?)')


class DeletionError(ZoiaLibError):
    """Class raised when a file could not be deleted from the backend directories."""

    def __init__(self, patch: str):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        else:
            print(f'Could not delete the file {patch} from the backend ZoiaLibraryApp directory.')


class RenamingError(ZoiaLibError):
    """Class raised when a file could not be renamed correctly."""

    def __init__(self, patch: str):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        else:
            print(f'Could not rename the file {patch} correctly (did the target name contain an illegal character?)')
