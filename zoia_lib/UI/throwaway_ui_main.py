import os
from threading import Thread

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, \
    QToolTip, QAbstractItemView, QWidget, QVBoxLayout

import zoia_lib.backend.api as api
import zoia_lib.backend.utilities as util

ps = api.PatchStorage()
backend_path = util.get_backend_path()

style_sheet = """
    QPushButton
    {
        background: white;
        border: none;
        font-size: 16px;
        color: black;
    }
    """


class ThrowawayUIMain(QWidget):

    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.data = ps.get_all_patch_data_min()["patch_list"]
        self.layout = QVBoxLayout()
        self.create_table()
        self.setWindowTitle("ZOIA Librarian")
        self.showMaximized()

    def create_table(self):
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(5)
        self.set_data()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def set_data(self):
        hor_headers = ["Title", "Tags", "Categories", "Date Modified", "Download"]
        for i in range(len(self.data)):
            self.table.setItem(i, 0, QTableWidgetItem(self.data[i]["title"]))
            tags = ""
            for j in range(1, len(self.data[i]["tags"])):
                tags += self.data[i]["tags"][j]["name"] + ", "
            tags = tags[:len(tags) - 2]
            if (len(self.data[i]["tags"])) > 1:
                btn_tag = QPushButton(self.data[i]["tags"][0]["name"]
                                      + " and " + str(len(self.data[i]["tags"])
                                                      - 1) + " more", self)
            else:
                btn_tag = QPushButton(self.data[i]["tags"][0]["name"], self)
            QToolTip.setFont(QFont('SansSerif', 11))
            btn_tag.setToolTip(tags)
            btn_tag.setStyleSheet(style_sheet)
            self.table.setCellWidget(i, 1, btn_tag)

            cat = ""
            for k in range(1, len(self.data[i]["categories"])):
                cat += self.data[i]["categories"][k]["name"] + ", "
            cat = cat[:len(cat) - 2]
            if (len(self.data[i]["categories"])) > 1:
                btn_cat = QPushButton(self.data[i]["categories"][0]["name"]
                                      + " and "
                                      + str(len(self.data[i]["categories"])
                                            - 1) + " more", self)
            else:
                btn_cat = QPushButton(self.data[i]["categories"][0]["name"], self)
            QToolTip.setFont(QFont('SansSerif', 11))
            btn_cat.setToolTip(cat)
            btn_cat.setStyleSheet(style_sheet)
            self.table.setCellWidget(i, 2, btn_cat)

            self.table.setItem(i, 3, QTableWidgetItem(self.data[i]["updated_at"][:10]))
            dwn = QPushButton(str(self.data[i]["id"]), self)
            dwn.clicked.connect(self.initiate_download)
            if (str(self.data[i]["id"])) in os.listdir(backend_path):
                dwn.setEnabled(False)
                dwn.setText("Downloaded!")
            self.table.setCellWidget(i, 4, dwn)
        self.table.setHorizontalHeaderLabels(hor_headers)

    def initiate_download(self):
        print("Starting download.")
        idx = str(self.sender().text())
        self.sender().setText("Downloading...")
        self.sender().show()
        thread = Thread(target=self.download_and_save(idx, self.sender()))
        thread.start()
        thread.join()

    @staticmethod
    def download_and_save(idx, btn):
        data = ps.download(idx)
        util.save_to_backend(data)
        btn.setEnabled(False)
        btn.setText("Downloaded!")
