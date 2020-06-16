class ZoiaLibError(Exception):
    """Base Error Class for zoia_lib. Inherited by all other errors."""

    pass


class BadPathError(ZoiaLibError):
    """Class raised when the file path is not valid.

    Possible error codes:
     - 301: The path did not lead to a file or directory.
    """

    def __init__(self, path, error_code=0):
        if path is None:
            print(f'Expected a file path but got None instead.')
        elif error_code == 301:
            print(f'Path {path} did not lead to a file or directory.')
        else:
            # Default case. We don't want to see this.
            print(f'An unexpected error occurred when trying to use {path} '
                  f'as a file path.')


class DeletionError(ZoiaLibError):
    """ Class raised when a file could not
    be deleted from the backend directories.

    Possible error codes:
     - 401: Encountered a file extension when none was expected.
     - 402: Encountered a version extension when none was expected.
     - 403: Failed to encounter a file extension when one was expected.
    """

    def __init__(self, patch, error_code=0):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        elif error_code == 401:
            print(f'Patch {patch} contains a file extension, which is not'
                  f'applicable when a patch directory is being deleted.')
        elif error_code == 402:
            print(f'Patch {patch} contains a version extension, which is not'
                  f'applicable when a patch directory is being deleted.')
        elif error_code == 403:
            print(f'Patch {patch} does not contain a file extension, which is '
                  f'required when an SD card patch is being deleted.')
        else:
            # Default case. We do not want to get here.
            print(f'Could not delete the file {patch} from the backend '
                  f'ZoiaLibraryApp directory due to an expected error.')


class SavingError(ZoiaLibError):
    """Class raised when a file could not be
    saved to the backend directories.

    Possible error codes:
     - 501: Encountered a file extension that the method
            is not meant to deal with
     - 502: The JSON data was not in correct JSON format.
     - 503: The patch metadata was missing a "files" attribute when it
            was required.
     - 504: Saving of a patch was attempted, but since that patch was
            already saved in the backend, no saving occurred.
     - 505: A file extension was expected but none was encountered.
    """

    def __init__(self, patch, error_code=0):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        elif error_code == 501:
            print(f'Could not save the file {patch} because a file extension '
                  f'was encountered when none should have been supplied.')
        elif error_code == 502:
            print(f'Could not save the file {patch} because the JSON data '
                  f'was mal-formatted (i.e., it was not JSON compliant).')
        elif error_code == 503:
            print(f'Could not save the file {patch} because necessary '
                  f'\"files\" attribute was missing in the metadata.')
        elif error_code == 504:
            print(f'Could not save the file {patch} because the binary '
                  f'content has already been saved and still exists.')
        elif error_code == 505:
            print(f'Could not save the file {patch} because it lacked '
                  f'a file extension.')
        else:
            # Default case. We do not want to get here.
            print(f'Could not save the file {patch} from the backend '
                  f'due to an unexpected error.')


class RenamingError(ZoiaLibError):
    """Class raised when a file could not be renamed correctly.

    Possible error codes:
     - 601: The target name contained an illegal character.
    """

    def __init__(self, patch, error_code=0):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        elif error_code == 601:
            print(f'Could not rename the file {patch} correctly '
                  f'due to the target name containing an illegal character.')
        else:
            # Default case. We do not want to get here.
            print(f'Could not rename the file {patch} correctly '
                  f'due to an unexpected error.')

class ExportingError(ZoiaLibError):
    """Class raised when a file could not be exported correctly.

    Possible error codes:
     - 701: The slot identifier was not in the correct range.
    """

    def __init__(self, patch, slot, error_code=0):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        elif error_code == 701:
            print(f'Could not export the file {patch} correctly '
                  f'due to the slot number being greater than 63 '
                  f'(got {slot}).')
        else:
            # Default case. We do not want to get here.
            print(f'Could not export the file {patch} correctly '
                  f'due to an unexpected error.')
