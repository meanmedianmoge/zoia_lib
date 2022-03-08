#!/bin/bash
git clone https://github.com/jchanvfx/NodeGraphQt.git

cd NodeGraphQt
python setup.py install

cd ../zoia_lib
pip install -r requirements.txt