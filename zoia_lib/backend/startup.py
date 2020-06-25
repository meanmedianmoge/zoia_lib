import sys

from PySide2.QtWidgets import QApplication

from zoia_lib.UI.throwaway_ui_main import ThrowawayUIMain
from zoia_lib.backend import utilities as util

# Entry point for the application.
if __name__ == "__main__":
    # Try to make the backend directories if need be.
    util.create_backend_directories()

    # Launch the GUI.
    app = QApplication(sys.argv)

    window = ThrowawayUIMain()
    window.show()

    sys.exit(app.exec_())
