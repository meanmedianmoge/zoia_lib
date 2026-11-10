#!/bin/bash
# Prepare the Python environment for Xcode Cloud packaging.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Use a managed Python instead of the older interpreter supplied with Xcode.
export HOMEBREW_NO_AUTO_UPDATE=1
brew install python@3.11
BOOTSTRAP_PYTHON="$(brew --prefix python@3.11)/bin/python3.11"
# build-app.sh defaults to this path on both Intel and Apple Silicon workers.
VENV="$ROOT/venv"
"$BOOTSTRAP_PYTHON" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$ROOT/requirements.txt"
"$VENV/bin/python" -m pip install pyinstaller pillow
"$VENV/bin/python" -m pip install "$ROOT"/tools/nodegraph/*.whl
"$VENV/bin/python" -c 'import PyInstaller, PySide6, NodeGraphQt, requests, furl, jsonschema, rarfile'
