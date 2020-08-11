import os
import platform
from pathlib import Path


class Patch:
    """ The Patch class is the parent class all other patch-related
    classes inherit from. It is responsible for determining the correct
    backend path to use and using said path to create necessary backend
    directories required for the function of the ZOIA Librarian.
    """

    def __init__(self):
        """ Determines the path used for the backend directories,
        based on the OS a user is running.
        """

        self.back_path = {
            "windows": os.path.join(os.getenv('APPDATA'), ".ZoiaLibraryApp"),
            "darwin": os.path.join(str(Path.home()), "Library",
                                   "Application Support", ".ZoiaLibraryApp"),
            "linux": os.path.join(str(Path.home()), ".local", "share",
                                  ".ZoiaLibraryApp")
        }[platform.system().lower()]

    def _create_backend_directories(self):
        """ Creates the necessary directories that will
        store patch files, bank files, and metadata files.
        """

        # Prevent an error on Windows by checking to see
        # if the directory already exists.
        if self.back_path is not None and not os.path.exists(self.back_path):
            os.mkdir(self.back_path)
        if not os.path.exists(os.path.join(self.back_path, "Banks")):
            os.mkdir(os.path.join(self.back_path, "Banks"))

    def get_backend_path(self):
        """ Getter method to retrieve the backend path as
        determined by __init__()
        """

        return self.back_path
