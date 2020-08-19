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

        # Can't use a dict here because it will fail on macOS.
        self.back_path = None
        curr_os = platform.system().lower()
        if curr_os == "windows":
            self.back_path = os.path.join(
                os.getenv('APPDATA'), ".ZoiaLibraryApp")
        elif curr_os == "darwin":
            self.back_path = os.path.join(
                str(Path.home()), "Library", "Application Support",
                ".ZoiaLibraryApp")
        elif curr_os == "linux":
            self.back_path = os.path.join(
                str(Path.home()), ".local", "share", ".ZoiaLibraryApp")
        else:
            # Solaris/Chrome OS/Java OS?
            self.back_path = None

        # Create the backend directories if needed.
        self._create_backend_directories()

    def _create_backend_directories(self):
        """ Creates the necessary directories that will store
        patch files, bank files, and metadata files.
        """

        # Prevent an error on Windows by checking to see
        # if the directory already exists.
        if self.back_path is not None and not os.path.exists(self.back_path):
            os.mkdir(self.back_path)
        if self.back_path is not None and not \
                os.path.exists(os.path.join(self.back_path, "Banks")):
            os.mkdir(os.path.join(self.back_path, "Banks"))

    def get_backend_path(self):
        """ Getter method to retrieve the backend path as
        determined by __init__()

        return: A string representing the OS specific backend path.
        """

        return self.back_path
