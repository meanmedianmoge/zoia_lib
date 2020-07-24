import json
import os

from PySide2.QtWidgets import QTableWidgetItem, QPushButton


def set_data_sd(sd, ui, f1, f2):
    """ Sets the data for the SD card table.
    """

    # Cleanup the tables
    for i in range(32):
        ui.table_sd_left.setItem(i, 0, QTableWidgetItem(None))
        ui.table_sd_left.setCellWidget(i, 1, None)
        ui.table_sd_left.setCellWidget(i, 2, None)
        ui.table_sd_right.setItem(i, 0, QTableWidgetItem(None))
        ui.table_sd_right.setCellWidget(i, 1, None)
        ui.table_sd_right.setCellWidget(i, 2, None)

    # Make sure we have an sd_card_path to work with.
    if not os.path.isdir(sd):
        return

    for pch in os.listdir(sd):
        # Get the index
        index = pch.split("_")[0]
        if index[0] == "0":
            # Get the useful int index.
            index = int(index[1:3])

            push_btn = QPushButton("X")
            push_btn.setObjectName(str(index))
            push_btn.setFont(ui.table_PS.horizontalHeader().font())
            push_btn.clicked.connect(f1)
            import_btn = QPushButton("Click me to import!")
            import_btn.setObjectName(str(index))
            import_btn.setFont(ui.table_PS.horizontalHeader().font())
            import_btn.clicked.connect(f2)

            if index < 32:
                # Left sd table.
                ui.table_sd_left.setItem(index, 0, QTableWidgetItem(pch))
                ui.table_sd_left.setCellWidget(index, 1, push_btn)
                ui.table_sd_left.setCellWidget(index, 2, import_btn)
            else:
                # Right sd table.
                ui.table_sd_right.setItem(index - 32, 0, QTableWidgetItem(pch))
                ui.table_sd_right.setCellWidget(index - 32, 1, push_btn)
                ui.table_sd_right.setCellWidget(index - 32, 2, import_btn)


def set_data_bank(ui, path, f1, data):
    """ Populates the bank export tables with data.
    """

    # Cleanup the tables
    for i in range(32):
        ui.table_bank_left.setItem(i, 0, QTableWidgetItem(None))
        ui.table_bank_left.setItem(i, 1, QTableWidgetItem(None))
        ui.table_bank_left.setCellWidget(i, 1, None)
        ui.table_bank_right.setItem(i, 0, QTableWidgetItem(None))
        ui.table_bank_right.setItem(i, 1, QTableWidgetItem(None))
        ui.table_bank_right.setCellWidget(i, 1, None)

    # PyQt tables make zero sense.
    ui.table_bank_left.clearContents()
    ui.table_bank_right.clearContents()

    for pch in data:
        idx = pch["id"]
        slot = pch["slot"]
        ver = None
        if "_" not in idx:
            with open(os.path.join(path,
                                   idx, "{}.json".format(idx)), "r") as f:
                temp = json.loads(f.read())
        else:
            idx, ver = idx.split("_")
            with open(os.path.join(path,
                                   idx, "{}_{}.json".format(idx, ver)),
                      "r") as f:
                temp = json.loads(f.read())
        name = temp["files"][0]["filename"]
        rmv_button = QPushButton("Remove")
        rmv_button.setObjectName(str(temp["id"]))
        if ver is not None:
            rmv_button.setObjectName(str(temp["id"]) + "_" + ver)
        else:
            rmv_button.setObjectName(str(temp["id"]))
        rmv_button.clicked.connect(f1)
        if "_zoia_" in name and len(name.split("_", 1)[0]) == 3:
            name = name.split("_", 2)[2]
        elif len(name.split("_", 1)[0]) == 3:
            name = name.split("_", 1)[1]
        if slot < 10:
            name = "00{}_zoia_".format(slot) + name
        else:
            name = "0{}_zoia_".format(slot) + name
        if slot < 32:
            ui.table_bank_left.setItem(
                slot, 0, QTableWidgetItem(name))
            ui.table_bank_left.setCellWidget(
                slot, 1, rmv_button)
        else:
            ui.table_bank_right.setItem(
                slot - 32, 0, QTableWidgetItem(name))
            ui.table_bank_right.setCellWidget(
                slot - 32, 1, rmv_button)
