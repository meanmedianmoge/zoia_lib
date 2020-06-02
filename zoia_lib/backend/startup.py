import os
import pathlib
import platform
import sys

from PySide2.QtWidgets import QApplication
from pathlib import Path

from zoia_lib.UI.zoia_lib_ui import MainWindow


def create_backend_directories():
    """ Creates the necessary directories that will
    store patch files, bank files, and metadata files
    in the appropriate directory based on the OS.
    """
    curr_os = platform.system()
    if curr_os == "Windows":
        path = os.getenv('APPDATA')
    elif curr_os == "Darwin":
        path = pathlib.Path.home() / "Library/Application Support"
    elif curr_os == "Linux":
        path = pathlib.Path.home() / ".local/share"
    else:
        # Solaris/Chrome OS/Java?
        path = None

    if path is not None:
        Path(path + "/.LibraryApp").mkdir(parents=True, exist_ok=True)
        path = path + "/.LibraryApp"
        Path(path + "/Banks").mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Try to make the backend directories if need be.
    create_backend_directories()

    # Get the list of patches on PS to pass to the GUI
    # get_all_patches_meta

    # Launch the GUI.
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
