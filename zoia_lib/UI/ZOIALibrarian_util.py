from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFontDialog
import os
import json


def change_font(name, ui):
    """ Changes the font used throughout the application.
    Currently triggered via a menu action.
    """

    # Get the context.
    if name == "":
        # Case 1: Default Change Font menu option.
        ok, f = QFontDialog.getFont()
        start = False
    elif name == "+" or name == "-":
        # Case 2: Increase/Decrease font size menu option.
        temp = ui.table_PS.font()
        f_size = temp.pointSize() + 2 if name == "+" else temp.pointSize() - 2
        temp = temp.toString().split(",")[0]
        f = QFont(temp, f_size)
        ok, start = True, False
    else:
        if type(name) == str:
            # Case 3.1: Init with pref.json
            temp = name.split("%")
            f = QFont(temp[0], int(temp[1]))
        else:
            # Case 3.2: Init without pref.json (first launch).
            f = name
        ok, start = True, True
    if ok:
        # Change the font for everything (within reason).
        new_font = f
        big_font = QFont(f.toString().split(",")[0], f.pointSize() + 6)

        ui.table_PS.setFont(new_font)
        ui.table_PS.horizontalHeader().setFont(new_font)
        ui.table_local.setFont(new_font)
        ui.table_local.horizontalHeader().setFont(new_font)
        ui.table_sd_left.setFont(new_font)
        ui.table_sd_left.horizontalHeader().setFont(new_font)
        ui.table_sd_left.verticalHeader().setFont(new_font)
        ui.table_sd_right.setFont(new_font)
        ui.table_sd_right.horizontalHeader().setFont(new_font)
        ui.table_sd_right.verticalHeader().setFont(new_font)
        ui.table_bank_local.setFont(new_font)
        ui.table_bank_local.horizontalHeader().setFont(new_font)
        ui.table_bank_left.setFont(new_font)
        ui.table_bank_left.horizontalHeader().setFont(new_font)
        ui.table_bank_left.verticalHeader().setFont(new_font)
        ui.table_bank_right.setFont(new_font)
        ui.table_bank_right.horizontalHeader().setFont(new_font)
        ui.table_bank_right.verticalHeader().setFont(new_font)
        ui.tabs.setFont(new_font)
        ui.text_browser_PS.setFont(big_font)
        ui.text_browser_local.setFont(big_font)
        ui.text_browser_bank.setFont(big_font)

        if not start:
            for i in range(ui.table_PS.rowCount()):
                ui.table_PS.cellWidget(i, 0).setFont(new_font)
                ui.table_PS.cellWidget(i, 4).setFont(new_font)
            if ui.table_local.cellWidget(0, 0) is not None:
                for i in range(ui.table_local.rowCount()):
                    ui.table_local.cellWidget(i, 0).setFont(new_font)
                    ui.table_local.cellWidget(i, 4).setFont(new_font)
                    ui.table_local.cellWidget(i, 5).setFont(new_font)
            for i in range(32):
                if ui.table_sd_left.cellWidget(i, 1) is not None:
                    ui.table_sd_left.cellWidget(i, 1).setFont(new_font)
                if ui.table_sd_left.cellWidget(i, 2) is not None:
                    ui.table_sd_left.cellWidget(i, 2).setFont(new_font)
                if ui.table_sd_right.cellWidget(i, 1) is not None:
                    ui.table_sd_right.cellWidget(i, 1).setFont(new_font)
                if ui.table_sd_right.cellWidget(i, 2) is not None:
                    ui.table_sd_right.cellWidget(i, 2).setFont(new_font)
                if ui.table_bank_left.cellWidget(i, 1) is not None:
                    ui.table_bank_left.cellWidget(i, 1).setFont(new_font)
                if ui.table_bank_left.cellWidget(i, 2) is not None:
                    ui.table_bank_left.cellWidget(i, 2).setFont(new_font)
                if ui.table_bank_right.cellWidget(i, 1) is not None:
                    ui.table_bank_right.cellWidget(i, 1).setFont(new_font)
                if ui.table_bank_right.cellWidget(i, 2) is not None:
                    ui.table_bank_right.cellWidget(i, 2).setFont(new_font)
            if ui.table_bank_local.cellWidget(0, 0) is not None:
                for i in range(ui.table_bank_local.rowCount()):
                    ui.table_bank_local.cellWidget(i, 0).setFont(new_font)


def save_pref(w, h, sd, ui, path):
    """ Saves and writes the state of a UI window to pref.json
    """

    # Capture the necessary specs on exit.
    window = {
        "width": w,
        "height": h,
        "font": ui.table_PS.horizontalHeader().font().toString().split(",")[0],
        "font_size": ui.table_PS.horizontalHeader().font().pointSize(),
        "sd_root": "" if sd is None else sd
    }
    ps_sizes = {
        "col_0": ui.table_PS.columnWidth(0),
        "col_1": ui.table_PS.columnWidth(1),
        "col_2": ui.table_PS.columnWidth(2),
        "col_3": ui.table_PS.columnWidth(3),
        "split_left": ui.splitter_PS.sizes()[0],
        "split_right": ui.splitter_PS.sizes()[1]
    }
    local_sizes = {
        "col_0": ui.table_local.columnWidth(0),
        "col_1": ui.table_local.columnWidth(1),
        "col_2": ui.table_local.columnWidth(2),
        "col_3": ui.table_local.columnWidth(3),
        "col_4": ui.table_local.columnWidth(4),
        "col_5": ui.table_local.columnWidth(5),
        "split_left": ui.splitter_local.sizes()[0],
        "split_right": ui.splitter_local.sizes()[1]
    }
    sd_sizes = {
        "col_0": ui.table_sd_left.columnWidth(0),
        "col_1": ui.table_sd_left.columnWidth(1),
        "col_2": ui.table_sd_right.columnWidth(0),
        "col_3": ui.table_sd_right.columnWidth(1),
        "split_top": ui.splitter_sd_vert.sizes()[0],
        "split_bottom": ui.splitter_sd_vert.sizes()[1],
        "split_left": ui.splitter_sd_hori.sizes()[0],
        "split_right": ui.splitter_sd_hori.sizes()[1]
    }
    bank_sizes = {
        "col_0": ui.table_bank_left.columnWidth(0),
        "col_1": ui.table_bank_right.columnWidth(0),
        "col_2": ui.table_bank_local.columnWidth(0),
        "col_3": ui.table_bank_local.columnWidth(1),
        "col_4": ui.table_bank_local.columnWidth(2),
        "split_left": ui.splitter_bank.sizes()[0],
        "split_middle": ui.splitter_bank.sizes()[1],
        "split_right": ui.splitter_bank.sizes()[2],
        "split_bank_left": ui.splitter_bank_tables.sizes()[0],
        "split_bank_right": ui.splitter_bank_tables.sizes()[1]
    }

    with open(os.path.join(path, "pref.json"), "w") as f:
        f.write(json.dumps([window, ps_sizes, local_sizes,
                            sd_sizes, bank_sizes]))
