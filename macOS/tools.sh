#!/bin/bash
# Prepare the Python environment for Xcode Cloud packaging.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Xcode's ARCHS cannot convert an Intel Python environment to ARM.
if ! /usr/bin/arch -arm64 /usr/bin/true 2>/dev/null; then
    echo "error: ARM64 App Store packaging requires an Apple Silicon build host. This worker cannot execute ARM64 Python."
    exit 1
fi
if [[ "$(uname -m)" != arm64 ]]; then
    exec /usr/bin/arch -arm64 /bin/bash "$0" "$@"
fi
if [[ -x /opt/homebrew/bin/brew ]]; then
    export PATH="/opt/homebrew/bin:$PATH"
fi

# Use a managed Python instead of the older interpreter supplied with Xcode.
export HOMEBREW_NO_AUTO_UPDATE=1
brew install python@3.11
BOOTSTRAP_PYTHON="$(brew --prefix python@3.11)/bin/python3.11"
"$BOOTSTRAP_PYTHON" -c 'import platform; assert platform.machine() == "arm64", "App Store setup requires native ARM64 Python; check the Homebrew installation"'
# build-app.sh defaults to this environment for the ARM64 App Store build.
VENV="$ROOT/venv"
"$BOOTSTRAP_PYTHON" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$ROOT/requirements.txt"
"$VENV/bin/python" -m pip install pyinstaller pillow
"$VENV/bin/python" -m pip install "$ROOT"/tools/nodegraph/*.whl
"$VENV/bin/python" -c 'import PyInstaller, PySide6, NodeGraphQt, requests, furl, jsonschema, rarfile'
