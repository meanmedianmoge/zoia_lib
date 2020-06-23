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
    # Example:
    #  - Download and save the patch with id 122661 to an SD card
    #    in drive G to ZOIA slot 8
    #try:
    #    util.save_to_backend(ps.download("122661"))
    #except errors.SavingError:
    #    pass
    #try:
    #    util.export_patch_bin("122661", os.path.join("G:", "to_zoia"), 8)
    #except errors.ExportingError:
    #    pass

    # Launch the GUI.
    app = QApplication(sys.argv)

    window = ThrowawayUIMain()
    window.show()

    sys.exit(app.exec_())
