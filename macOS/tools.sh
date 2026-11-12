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
# build-app.sh defaults to this environment for the ARM64 App Store build.
VENV="$ROOT/venv"
if [[ ! -x "$VENV/bin/python" ]]; then
    # Homebrew under /usr/local may supply Intel Python even on an ARM host.
    # Use an explicit architecture request, independent of Homebrew's prefix.
    if ! command -v uv >/dev/null 2>&1; then
        export HOMEBREW_NO_AUTO_UPDATE=1
        brew install uv
    fi
    export UV_PYTHON_INSTALL_DIR="$ROOT/build/cloud-python"
    export UV_CACHE_DIR="$ROOT/build/cloud-uv-cache"
    PYTHON_REQUEST=cpython-3.11-macos-aarch64-none
    uv python install "$PYTHON_REQUEST" --no-bin
    # Discovery can filter by the uv process's architecture (Homebrew uv may
    # be Intel). Select the ARM installation directly, then test its runtime.
    ARM_PYTHONS=("$UV_PYTHON_INSTALL_DIR"/cpython-3.11.*-macos-aarch64-none/bin/python3.11)
    if [[ ${#ARM_PYTHONS[@]} != 1 || ! -x "${ARM_PYTHONS[0]}" ]]; then
        echo "error: Expected one downloaded ARM64 Python under $UV_PYTHON_INSTALL_DIR."
        exit 1
    fi
    BOOTSTRAP_PYTHON="${ARM_PYTHONS[0]}"
    if ! /usr/bin/arch -arm64 "$BOOTSTRAP_PYTHON" -c 'import platform; assert platform.machine() == "arm64", "Downloaded Python must execute as ARM64"'; then
        echo "error: ARM64 Python was downloaded to $BOOTSTRAP_PYTHON but cannot run on this worker."
        exit 1
    fi
    "$BOOTSTRAP_PYTHON" -m venv "$VENV"
fi
"$VENV/bin/python" -c 'import platform, sys; print("Build Python:", sys.executable, "base:", sys.base_prefix, "architecture:", platform.machine()); assert platform.machine() == "arm64" and sys.version_info >= (3, 11), "venv must use ARM64 Python 3.11+"'
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$ROOT/requirements.txt"
"$VENV/bin/python" -m pip install pyinstaller pillow
"$VENV/bin/python" -m pip install "$ROOT"/tools/nodegraph/*.whl
"$VENV/bin/python" -c 'import PyInstaller, PySide6, NodeGraphQt, requests, furl, jsonschema, rarfile'
