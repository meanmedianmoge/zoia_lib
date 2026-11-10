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
if [[ "${ZOIA_APP_STORE:-NO}" == YES ]]; then
    "$PYTHON" -c 'import platform; assert platform.machine() == "arm64", "App Store builds require an ARM64 Python environment on Apple Silicon"'
fi
WORK="${TEMP_DIR:-$ROOT/build/xcode}/zoia-packaging"
# Install only the app in Xcode's target directory. PyInstaller also emits a
# COLLECT folder; including it makes Xcode classify the archive as generic.
# BUILT_PRODUCTS_DIR can contain an Xcode-owned app symlink during archive.
PRODUCTS="${TARGET_BUILD_DIR:-${BUILT_PRODUCTS_DIR:-$ROOT/build/xcode/Products}}"
mkdir -p "$WORK" "$PRODUCTS"
"$PYTHON" "$ROOT/tools/make_distro.py" --source "$ROOT/zoia_lib" --dest "$WORK/source"
cd "$WORK/source"
ZOIA_STAGING="$WORK/source" "$PYTHON" -m PyInstaller --noconfirm \
    --workpath "$WORK/pyinstaller" --distpath "$WORK/dist" "$ROOT/macOS/ZOIALibrarian.spec"
if [[ "${ZOIA_APP_STORE:-NO}" == YES ]]; then
    APP_ARCH="$(lipo -archs "$WORK/dist/ZOIA Librarian.app/Contents/MacOS/ZOIA Librarian")"
    if [[ "$APP_ARCH" != arm64 ]]; then
        echo "error: App Store executable must be ARM64-only, got: $APP_ARCH"
        exit 1
    fi
fi
ditto "$WORK/dist/ZOIA Librarian.app" "$PRODUCTS/ZOIA Librarian.app"
