"""
    After setting up a Python 3+ virtual environment and installing
    the required packages specified in requirements.txt;
        pip install -r requirements.txt
    you can run the application using the following command from the
    root zoia_lib directory via a command terminal:
        python -m zoia_lib.backend.startup

    Please note, this app is still in active development. Please stay
    updated by visiting https://github.com/meanmedianmoge/zoia_lib/
"""
import os
import sys

from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QApplication, QSplashScreen, QStyleFactory

from zoia_lib.backend.utilities import meipass
from zoia_lib.UI.ZOIALibrarian_main import ZOIALibrarianMain

# Entry point for the application.
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set style
    app.setStyle(QStyleFactory.create("Fusion"))

    file_path = meipass(
        os.path.join(os.getcwd(), "zoia_lib", "UI", "resources", "splash.png")
    )

    # Create and display the splash screen
    img = QPixmap(file_path)
    splash = QSplashScreen(img, Qt.WindowStaysOnTopHint)
    splash.show()

    # Show the window after it finishes setting up and close the splash.
    window = ZOIALibrarianMain()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())
