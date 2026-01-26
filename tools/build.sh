ARCHITECTURE="${1:-$(uname -m)}"
if [ "$ARCHITECTURE" = "x86_64" ]; then
    python3 -m venv venv_x86
    source venv_x86/bin/activate
else
    python3 -m venv venv
    source venv/bin/activate
fi

python tools/make_distro.py
cd distro

if [ "$ARCHITECTURE" = "x86_64" ]; then
    sed -i '' -E "s/^[[:space:]]*#?[[:space:]]*target_arch='x86_64'.*/    target_arch='x86_64',/" "zoia_lib_mac.spec"
else
    sed -i '' -E "s/^[[:space:]]*#?[[:space:]]*target_arch='x86_64'.*/    # target_arch='x86_64', # uncomment for Intel-based Mac/" "zoia_lib_mac.spec"
fi
python -m PyInstaller --clean --noconfirm zoia_lib_mac.spec
