#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${ZOIA_PYTHON:-$ROOT/venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
    echo "error: Python environment missing. Run bash tools/env.sh from $ROOT, or set ZOIA_PYTHON in Xcode Build Settings."
    exit 1
fi
"$PYTHON" -c 'import PyInstaller, PySide6, NodeGraphQt, requests, furl, jsonschema, rarfile' || {
    echo "error: Install desktop dependencies with bash tools/env.sh before building."
    exit 1
}
WORK="${TEMP_DIR:-$ROOT/build/xcode}/zoia-packaging"
# During archive, BUILT_PRODUCTS_DIR contains an Xcode-owned app symlink.
# Package into its actual installation directory so PyInstaller does not try
# to replace that symlink with a bundle directory.
PRODUCTS="${TARGET_BUILD_DIR:-${BUILT_PRODUCTS_DIR:-$ROOT/build/xcode/Products}}"
mkdir -p "$WORK" "$PRODUCTS"
"$PYTHON" "$ROOT/tools/make_distro.py" --source "$ROOT/zoia_lib" --dest "$WORK/source"
cd "$WORK/source"
ZOIA_STAGING="$WORK/source" "$PYTHON" -m PyInstaller --noconfirm \
    --workpath "$WORK/pyinstaller" --distpath "$PRODUCTS" "$ROOT/macOS/ZOIALibrarian.spec"
