import os
import sys
from pathlib import Path

from PySide2.QtWidgets import QApplication

import zoia_lib.backend.api as api
import zoia_lib.backend.utilities as util
from zoia_lib.UI.zoia_lib_ui import MainWindow


def create_backend_directories():
    """ Creates the necessary directories that will
    store patch files, bank files, and metadata files
    in the appropriate directory based on the OS.
    """
    backend_path = util.determine_backend_path()

    if backend_path is not None:
        os.mkdir(backend_path)
        os.mkdir(str(Path(backend_path + "/Banks")))


if __name__ == "__main__":
    # Try to make the backend directories if need be.
    create_backend_directories()
    ps = api.PatchStorage()

    # Get the list of patches on PS to pass to the GUI
    # Maybe we let the user do this with a button instead of doing it automatically?
    # get_all_patches_meta()

    # Launch the GUI.
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
