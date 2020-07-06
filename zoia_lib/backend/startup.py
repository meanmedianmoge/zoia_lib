""" After setting up a Python 3+ virtual environment and installing
the required packages specified in requirements.txt,
    pip install -r requirements.txt
you can run the application using the following command from the
root zoia_lib directory:
    python -m zoia_lib.backend.startup

Please note, this app is still in active development. Please stay updated
by visiting https://github.com/meanmedianmoge/zoia_lib/
"""
import os
import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QSplashScreen

from zoia_lib.UI.early_ui_main import EarlyUIMain
from zoia_lib.backend import utilities as util

# Entry point for the application.
if __name__ == "__main__":
    # Launch the GUI.
    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap(os.path.join(os.getcwd(), "zoia_lib", "backend",
                                      "splash.png"))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()

    # Try to make the backend directories if need be.
    util.create_backend_directories()

    window = EarlyUIMain()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())
