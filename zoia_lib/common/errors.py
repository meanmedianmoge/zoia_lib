class ZoiaLibError(Exception):
    """Base Error Class for zoia_lib. Inherited by all other errors."""

    pass


class BadPathError(ZoiaLibError):
    """Class raised when the file path is not valid."""

    def __init__(self, path: str):
        print(f'Supplied path {path} is not a child of '
              f'current directory.')
