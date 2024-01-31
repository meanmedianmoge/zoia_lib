#!/bin/bash
git clone -b zgraph6 https://github.com/meanmedianmoge/NodeGraphQt.git

cd NodeGraphQt
python setup.py install

cd ../zoia_lib
pip install -r requirements.txt