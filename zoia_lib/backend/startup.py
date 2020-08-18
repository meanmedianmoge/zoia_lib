""" After setting up a Python 3+ virtual environment and installing
the required packages specified in requirements.txt,
    pip install -r requirements.txt
you can run the application using the following command from the
root zoia_lib directory:
    python -m zoia_lib.backend.startup

Please note, this app is still in active development. Please stay
updated by visiting https://github.com/meanmedianmoge/zoia_lib/
"""
import os
import sys

from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QApplication, QSplashScreen

from zoia_lib.UI.ZOIALibrarian_main import ZOIALibrarianMain

# Entry point for the application.
from zoia_lib.backend.patch import Patch

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and display the splash screen
    img = QPixmap(
        os.path.join(os.getcwd(), "zoia_lib", "backend", "splash.png"))
    splash = QSplashScreen(img, Qt.WindowStaysOnTopHint)
    splash.show()

    # Create the backend directories (if need be).
    patch = Patch()

    # Show the window after it finishes setting up and close the splash.
    window = ZOIALibrarianMain()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())
