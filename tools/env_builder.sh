SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SPEC_FILE="$SCRIPT_DIR/zoia_lib_mac.spec"

# ARM64 Mac Environment Builder Script
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install pyinstaller pillow

# git clone -b zgraph6 https://github.com/meanmedianmoge/NodeGraphQt.git

cd ../NodeGraphQt
python setup.py install

cd ../zoia_lib
python tools/build_distro.py
sed -i '' -E "s/^[[:space:]]*#?[[:space:]]*target_arch='x86_64'.*/    # target_arch='x86_64', # uncomment for Intel-based Mac/" "$SPEC_FILE"
python -m PyInstaller --clean --noconfirm zoia_lib_mac.spec

# Intel Mac Environment Builder Script
arch -x86_64 python3 -m venv venv_x86
source venv_x86/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller pillow

# git clone -b zgraph6 https://github.com/meanmedianmoge/NodeGraphQt.git

cd ../NodeGraphQt
python setup.py install

cd ../zoia_lib/distro
sed -i '' -E "s/^[[:space:]]*#?[[:space:]]*target_arch='x86_64'.*/    target_arch='x86_64',/" "$SPEC_FILE"
python -m PyInstaller --clean --noconfirm zoia_lib_mac.spec
