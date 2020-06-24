import sys

from PySide2.QtWidgets import QApplication

import zoia_lib.backend.api as api
import zoia_lib.backend.utilities as util
from zoia_lib.UI.throwaway_ui_main import ThrowawayUIMain

if __name__ == "__main__":
    # Try to make the backend directories if need be.
    util.create_backend_directories()
    ps = api.PatchStorage()

    # Get the list of patches on PS to pass to the GUI
    # TODO Maybe we let the user do this with a button
    #  instead of doing it automatically?
    patch_list = ps.get_all_patch_data_min()["patch_list"]

    # Launch the GUI.
    app = QApplication(sys.argv)

    window = ThrowawayUIMain()
    window.show()

    sys.exit(app.exec_())
