#!/bin/bash
cd zoia_lib
source venv/bin/activate
python tools/build_distro.py

deactivate
pip install pyinstaller
pip install pillow

cd distro
pyinstaller --clean --noconfirm zoia_lib_mac.spec