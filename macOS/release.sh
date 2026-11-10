#!/bin/bash
# Developer ID distribution; credentials remain in the user's Keychain.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-}"
if [[ "$MODE" != "--check" && "$MODE" != "--release" ]]; then
    echo "Usage: bash macOS/release.sh --check | --release"
    echo "Set ZOIA_CODESIGN_IDENTITY, ZOIA_NOTARY_PROFILE, and (for --release) ZOIA_VERSION."
    exit 2
fi
IDENTITY="${ZOIA_CODESIGN_IDENTITY:-}"
PROFILE="${ZOIA_NOTARY_PROFILE:-ZOIA-notary}"
VERSION="${ZOIA_VERSION:-}"
if [[ "$IDENTITY" != 'Developer ID Application: '* ]]; then
    echo "error: Set ZOIA_CODESIGN_IDENTITY to a Developer ID Application identity."
    echo "Available signing identities:"
    security find-identity -v -p codesigning
    exit 1
fi
if ! security find-identity -v -p codesigning | /usr/bin/grep -F -- "\"$IDENTITY\"" >/dev/null; then
    echo "error: The requested Developer ID Application identity is not available in Keychain."
    exit 1
fi
# This verifies the profile and Apple's authentication before starting a build.
xcrun notarytool history --keychain-profile "$PROFILE" >/dev/null
if [[ "$MODE" == "--check" ]]; then
    echo "Developer ID identity and notarization credentials are ready."
    exit 0
fi
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
    echo "error: Set ZOIA_VERSION to a release version, for example 2.1.1."
    exit 1
fi
mkdir -p "$ROOT/build/releases"
RELEASE_DIR="$(mktemp -d "$ROOT/build/releases/$VERSION.XXXXXX")"
export ZOIA_CODESIGN_IDENTITY="$IDENTITY" ZOIA_VERSION="$VERSION"
export TEMP_DIR="$RELEASE_DIR/work" BUILT_PRODUCTS_DIR="$RELEASE_DIR/products"
bash "$ROOT/macOS/build-app.sh"
APP="$BUILT_PRODUCTS_DIR/ZOIA Librarian.app"
ARCH="$(lipo -archs "$APP/Contents/MacOS/ZOIA Librarian")"
if [[ -n "${ZOIA_TARGET_ARCH:-}" && "$ARCH" != "$ZOIA_TARGET_ARCH" ]]; then
    echo "error: Built architecture $ARCH does not match requested $ZOIA_TARGET_ARCH."
    exit 1
fi
if [[ "$ARCH" == 'x86_64 arm64' || "$ARCH" == 'arm64 x86_64' ]]; then
    ARCH=universal2
fi
codesign --verify --deep --strict --verbose=2 "$APP"
# Require an actual Developer ID signature with hardened runtime and timestamp.
SIGNATURE="$(codesign -d --verbose=4 "$APP" 2>&1)"
for REQUIRED in 'Authority=Developer ID Application:' 'runtime' 'Timestamp='; do
    if [[ "$SIGNATURE" != *"$REQUIRED"* ]]; then
        echo "error: Release signature is missing $REQUIRED"
        exit 1
    fi
done
UPLOAD="$RELEASE_DIR/notarization-upload.zip"
ditto -c -k --norsrc --noextattr --keepParent "$APP" "$UPLOAD"
# Save the submission ID even if Apple rejects the upload or the wait times out.
xcrun notarytool submit "$UPLOAD" --keychain-profile "$PROFILE" \
    --wait --timeout 30m --output-format json > "$RELEASE_DIR/notarization.json"
/usr/bin/plutil -extract status raw -o - "$RELEASE_DIR/notarization.json" | /usr/bin/grep -x Accepted >/dev/null || {
    echo "error: Apple has not accepted this submission. See $RELEASE_DIR/notarization.json"
    echo "Fetch details with: xcrun notarytool log <submission-id> --keychain-profile $PROFILE"
    exit 1
}
xcrun stapler staple "$APP"
xcrun stapler validate "$APP"
codesign --verify --deep --strict --verbose=2 "$APP"
spctl --assess --type execute --verbose=2 "$APP"
# A ZIP cannot be stapled. Recreate it from the app with the stapled ticket.
ZIP="$RELEASE_DIR/ZOIA-Librarian-$VERSION-macOS-$ARCH.zip"
ditto -c -k --norsrc --noextattr --keepParent "$APP" "$ZIP"
# Verify the delivered bundle after extraction, not only the source app.
VERIFY_DIR="$(mktemp -d "$RELEASE_DIR/extraction-check.XXXXXX")"
ditto -x -k "$ZIP" "$VERIFY_DIR"
codesign --verify --deep --strict "$VERIFY_DIR/ZOIA Librarian.app"
xcrun stapler validate "$VERIFY_DIR/ZOIA Librarian.app"
spctl --assess --type execute --verbose=2 "$VERIFY_DIR/ZOIA Librarian.app"
shasum -a 256 "$ZIP" > "$ZIP.sha256"
echo "Signed, notarized release: $ZIP"
echo "Checksum: $ZIP.sha256"
