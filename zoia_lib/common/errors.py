class ZoiaLibError(Exception):
    """Base Error Class for zoia_lib. Inherited by all other errors."""

    pass


class BinaryError(ZoiaLibError):
    """Class raised when the binary could not be decoded.

    Possible error codes:
    - 101: Patch binary could not be read properly.
    """

    def __init__(self, patch, error_code_zoia=0):
        if patch is None:
            error_msg = f"Expected a patch object but got None instead."
        else:
            try:
                error_msg = {
                    101: f"Patch {patch} could not be decoded properly.",
                }[error_code_zoia]
            except KeyError:
                error_msg = (
                    f"Could not decode the binary file {patch} due "
                    f"to an unexpected error."
                )
        print(error_msg)


class UpdateError(ZoiaLibError):
    """Class raised when a patch could not be updated.

    Possible error codes:
    - 201: The patch index has multiple versions.
    """

    def __init__(self, idx, error_code_zoia=0):
        if idx is None:
            print(f"Expected a patch index but got None instead.")
        elif error_code_zoia == 201:
            print(f"Patch {idx} has multiple versions.")
        else:
            # Default case. We do not want to get here.
            print(
                f"Could not update the patch {idx} correctly "
                f"due to an unexpected error."
            )


class BadPathError(ZoiaLibError):
    """Class raised when the file path is not valid.

    Possible error codes:
     - 301: The path did not lead to a file or directory.
    """

    def __init__(self, path, error_code_zoia=0):
        if path is None:
            print(f"Expected a file path but got None instead.")
        elif error_code_zoia == 301:
            print(f"Path {path} did not lead to a file or directory.")
        else:
            # Default case. We don't want to see this.
            print(
                f"An unexpected error occurred when trying to use {path} "
                f"as a file path."
            )


class DeletionError(ZoiaLibError):
    """Class raised when a file could not
    be deleted from the backend directories.

    Possible error codes:
     - 401: Encountered a file extension when none was expected.
     - 402: Encountered a version extension when none was expected.
     - 403: Failed to encounter a file extension when one was expected.
    """

    def __init__(self, patch, error_code_zoia=0):
        if patch is None:
            error_msg = f"Expected a patch name but got None instead."
        else:
            try:
                error_msg = {
                    401: f"Patch {patch} contains a file extension, which is "
                    f"not valid when a patch directory is being deleted.",
                    402: f"Patch {patch} contains a version extension, which "
                    f"is not valid when a patch directory is being "
                    f"deleted.",
                    403: f"Patch {patch} does not contain a file extension, "
                    f"which is required when an SD card patch is being "
                    f"deleted.",
                }[error_code_zoia]
            except KeyError:
                error_msg = (
                    f"Could not delete the file {patch} from the "
                    f"backend ZoiaLibraryApp directory due to an "
                    f"unexpected error."
                )
        print(error_msg)


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
     - 506: Tried to download a compressed file that was not properly
            compressed in the format presented.
    """

    def __init__(self, patch, error_code_zoia=0):
        if patch is None:
            error_msg = f"Expected a patch name but got None instead."
        else:
            try:
                error_msg = {
                    501: f"Could not save the file {patch} because a file "
                    f"extension was encountered when none should have "
                    f"been supplied.",
                    502: f"Could not save the file {patch} because necessary "
                    f'"files" attribute was missing in the metadata.',
                    503: f"Could not save the file {patch} because the binary "
                    f"content has already been saved and still exists.",
                    504: f"Could not save the file {patch} because it lacked "
                    f"a file extension.",
                    505: f"Could not create a directory with id {patch} "
                    f"because it already existed.",
                    506: f"Could not save the file {patch} because the compression "
                    f"method was not executed properly.",
                }[error_code_zoia]
            except KeyError:
                error_msg = (
                    f"Could not save the file {patch} from the "
                    f"backend due to an unexpected error."
                )
        print(error_msg)


class RenamingError(ZoiaLibError):
    """Class raised when a file could not be renamed correctly.

    Possible error codes:
     - 601: The target name contained an illegal character.
    """

    def __init__(self, patch, error_code=0):
        if patch is None:
            print(f"Expected a patch name but got None instead.")
        elif error_code == 601:
            print(
                f"Could not rename the file {patch} correctly "
                f"due to the target name containing an illegal character."
            )
        else:
            # Default case. We do not want to get here.
            print(
                f"Could not rename the file {patch} correctly "
                f"due to an unexpected error."
            )


class ExportingError(ZoiaLibError):
    """Class raised when a file could not be exported correctly.

    Possible error codes:
     - 701: The slot identifier was not in the correct range.
     - 702: Exporting would result in overwriting of data.
    """

    def __init__(self, patch, slot=-1, error_code_zoia=0):
        if patch is None:
            error_msg = f"Expected a patch name but got None instead."
        else:
            try:
                error_msg = {
                    701: f"Could not export the file {patch} correctly "
                    f"due to the slot number being greater than 63 "
                    f"(got {slot}).",
                    702: f"Exporting would result in overwriting of data,"
                    f"as a directory already existed on the SD"
                    f"card",
                    703: f"Exporting would create a conflict between two" f"patches.",
                }[error_code_zoia]
            except KeyError:
                error_msg = (
                    f"Could not export the file {patch} correctly "
                    f"due to an unexpected error."
                )
        print(error_msg)


class JSONError(ZoiaLibError):
    """Class raised when a file could not be exported correctly.

    Possible error codes:
     - 801: The JSON data was malformed.
    """

    def __init__(self, data, error_code_zoia=0):
        if data is None:
            print(f"Expected a JSON data but got None instead.")
        elif error_code_zoia == 801:
            print(
                f"Could not process {data} because the JSON data "
                f"was mal-formatted (i.e., it was not JSON compliant)."
            )
        else:
            # Default case. We do not want to get here.
            print(f"Could not process {data} correctly " f"due to an unexpected error.")


class SortingError(ZoiaLibError):
    """Class raised when metadata could not be sorted correctly.

    Possible error codes:
     - 901: The mode was invalid.
     - 902: The data supplied was not a list.
     - 903: One or more passed parameters contained None.
    """

    def __init__(self, info, error_code_zoia=0):
        if info is None:
            error_msg = f"Expected information but got None instead."
        else:
            try:
                error_msg = {
                    901: f"Sorting mode {info} is invalid. Valid sorting "
                    f"modes occur between 1 and 10 inclusive.",
                    902: f"The supplied metadata {info} is not a list. "
                    f"Sorting can only occur on valid lists.",
                    903: f"The parameter list was invalid. Ensure that no "
                    f"parameters contain None as a value.",
                }[error_code_zoia]
            except KeyError:
                error_msg = (
                    f"Could not process {info} correctly due to an "
                    f"unexpected error."
                )
        print(error_msg)


class SearchingError(ZoiaLibError):
    """Class raised when searching through metadata did not complete
    successfully.

    Possible error codes:
     - 1001:  The query supplied was not a list.
     - 1002: One or more passed parameters contained None.
    """

    def __init__(self, info, error_code_zoia=0):
        if info is None:
            error_msg = f"Expected information but got None instead."
        else:
            try:
                error_msg = {
                    1001: f"The supplied metadata {info} is not a list. "
                    f"Searching can only occur on valid lists.",
                    1002: f"The parameter list was invalid. Ensure that no "
                    f"parameters contain None as a value.",
                }[error_code_zoia]
            except KeyError:
                error_msg = (
                    f"Could not process {info} correctly due to an "
                    f"unexpected error."
                )
        print(error_msg)
