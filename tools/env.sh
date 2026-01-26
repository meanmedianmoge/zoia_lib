ARCHITECTURE="${1:-$(uname -m)}"
if [ "$ARCHITECTURE" = "x86_64" ]; then
    python -m venv venv_x86
    source venv_x86/bin/activate
else
    python -m venv venv
    source venv/bin/activate
fi

python -m pip install -r requirements.txt
python -m pip install pyinstaller pillow
python -m pip install tools/nodegraph/*.whl
