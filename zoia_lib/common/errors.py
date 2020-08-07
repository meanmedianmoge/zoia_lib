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
     - 404: Incorrect index provided for deletion purposes.
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
        elif error_code == 404:
            print(f'Expected an index of length 3, but got {patch} instead.')
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
     - 502: The patch metadata was missing a "files" attribute when it
            was required.
     - 503: Saving of a patch was attempted, but since that patch was
            already saved in the backend, no saving occurred.
     - 504: A file extension was expected but none was encountered.
     - 505: A directory was requested to be created, yet it already
            existed.
    """

    def __init__(self, patch, error_code=0):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        elif error_code == 501:
            print(f'Could not save the file {patch} because a file extension '
                  f'was encountered when none should have been supplied.')
        elif error_code == 502:
            print(f'Could not save the file {patch} because necessary '
                  f'\"files\" attribute was missing in the metadata.')
        elif error_code == 503:
            print(f'Could not save the file {patch} because the binary '
                  f'content has already been saved and still exists.')
        elif error_code == 504:
            print(f'Could not save the file {patch} because it lacked '
                  f'a file extension.')
        elif error_code == 505:
            print(f'Could not create a directory with id {patch} because it '
                  f'already existed.')
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
     - 702: Exporting would result in overwriting of data.
    """

    def __init__(self, patch, slot=-1, error_code=0):
        if patch is None:
            print(f'Expected a patch name but got None instead.')
        elif error_code == 701:
            print(f'Could not export the file {patch} correctly '
                  f'due to the slot number being greater than 63 '
                  f'(got {slot}).')
        elif error_code == 702:
            print(f'Exporting would result in overwriting of data,'
                  f'as a bank directory already existed on the SD'
                  f'card')
        elif error_code == 703:
            print(f'Exporting would create a conflict between two'
                  f'patches.')
        else:
            # Default case. We do not want to get here.
            print(f'Could not export the file {patch} correctly '
                  f'due to an unexpected error.')


class JSONError(ZoiaLibError):
    """Class raised when a file could not be exported correctly.

    Possible error codes:
     - 801: The JSON data was malformed.
    """

    def __init__(self, data, error_code=0):
        if data is None:
            print(f'Expected a JSON data but got None instead.')
        elif error_code == 801:
            print(f'Could not process {data} because the JSON data '
                  f'was mal-formatted (i.e., it was not JSON compliant).')
        else:
            # Default case. We do not want to get here.
            print(f'Could not process {data} correctly '
                  f'due to an unexpected error.')


class SortingError(ZoiaLibError):
    """Class raised when metadata could not be sorted correctly.

    Possible error codes:
     - 901: The mode was invalid.
     - 902: The data supplied was not a list.
    """
    def __init__(self, info, error_code=0):
        if info is None:
            print(f'Expected information but got None instead.')
        elif error_code == 901:
            print(f'Sorting mode {info} is invalid. Valid sorting modes '
                  f'occur between 1 and 6 inclusive.')
        elif error_code == 902:
            print(f'The supplied metadata {info} is not a list. Sorting '
                  f'can only occur on valid lists.')
        else:
            # Default case. We do not want to get here.
            print(f'Could not process {info} correctly '
                  f'due to an unexpected error.')


class SearchingError(ZoiaLibError):
    """Class raised when searching through metadata did not complete
    successfully.

    Possible error codes:
     - 1001: The mode was invalid.
     - 1002: The query supplied was not a list.
    """
    def __init__(self, info, error_code=0):
        if info is None:
            print(f'Expected information but got None instead.')
        elif error_code == 1001:
            print(f'The supplied metadata {info} is not a list. Searching '
                  f'can only occur on valid lists.')
        else:
            # Default case. We do not want to get here.
            print(f'Could not process {info} correctly '
                  f'due to an unexpected error.')
