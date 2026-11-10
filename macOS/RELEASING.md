# Developer ID releases

This workflow distributes the original Python/Qt desktop app outside the Mac
App Store. It requires Apple Developer Program membership and Xcode. It does
not publish a GitHub release or upload to your website automatically.

## One-time setup on your Mac

1. In **Xcode → Settings → Accounts**, select your developer account and team,
   then **Manage Certificates → + → Developer ID Application**. If that option
   is unavailable, ask your team's Account Holder to create the certificate.
   The certificate and its private key must be installed in your login Keychain.
   An **Apple Development** certificate cannot replace it.
2. Run `security find-identity -v -p codesigning` and copy the complete
   `Developer ID Application: … (TEAMID)` identity name.
3. Store notarization credentials locally, using your Apple ID, Team ID, and an
   app-specific password generated through your Apple Account:

   ```sh
   xcrun notarytool store-credentials ZOIA-notary
   ```

   Follow the interactive prompts. Do not paste passwords, private keys, or
   certificate exports into chat or commit them to the repository.
4. Install build dependencies from the repository root if needed:

   ```sh
   bash tools/env.sh
   ```

## Xcode Cloud dependency setup

`ci_scripts/ci_post_clone.sh`, beside the Xcode project, runs `macOS/tools.sh`
after checkout to install Homebrew Python 3.11 and dependencies. It creates the ignored
`venv` directory used by `build-app.sh`, including PyInstaller and the bundled
NodeGraphQt wheel. The Cloud setup is contained in `macOS`; the local
`tools/env.sh` workflow is unchanged. Commit the hook and `macOS/tools.sh`, then start
a new Cloud build from that commit. Remove any Cloud `ZOIA_PYTHON` override
that points to a path on your local Mac so the build uses the default environment.

The hook prepares dependencies; Developer ID signing and notarization still
use the release workflow below.

## Build a release

From the repository root, replacing the identity below with yours:

```sh
export ZOIA_CODESIGN_IDENTITY='Developer ID Application: Your Name (TEAMID)'
export ZOIA_NOTARY_PROFILE='ZOIA-notary'
export ZOIA_VERSION='2.1.1'
bash macOS/release.sh --check
bash macOS/release.sh --release
```

`ZOIA_VERSION` controls the bundle's release version. Update the application's
own displayed version as part of preparing the corresponding source release;
this script does not edit source files. Set `ZOIA_PYTHON` to an absolute
interpreter path to use an environment other than `venv/bin/python`.

The script builds in a new directory under `build/releases`, signs the embedded
Python/Qt binaries and application using PyInstaller with hardened runtime and
a secure timestamp, verifies signatures, uploads a ZIP to Apple, and waits up
to 30 minutes. After acceptance, it staples and validates the ticket, checks
Gatekeeper, and creates a fresh ZIP containing the stapled application plus a
SHA-256 checksum file. ZIP creation excludes AppleDouble metadata, and the
extracted application must pass signature, ticket, and Gatekeeper checks. It stops on failures and never falls back to an ad-hoc
signature for releases. The local Xcode Run build remains ad-hoc unless you
explicitly set `ZOIA_CODESIGN_IDENTITY`.

Signed Intel builds (and universal builds containing Intel code) enable
`com.apple.security.cs.allow-unsigned-executable-memory` for Python's
`ctypes`/libffi callbacks. Without it, Intel Python can hang during import before
the splash screen appears. Other hardened-runtime exceptions remain disabled.
This is a Developer ID build, without App Sandbox. Test startup as well as
signature validation: notarization alone does not establish runtime correctness.

## If notarization fails or times out

Keep the release directory. `notarization.json` contains Apple's response and
submission ID. Inspect the result without uploading a duplicate:

```sh
xcrun notarytool info SUBMISSION_ID --keychain-profile ZOIA-notary
xcrun notarytool log SUBMISSION_ID --keychain-profile ZOIA-notary notary-log.json
```

A timeout does not cancel Apple's processing. If the submission is later
accepted, use its existing app under `products/ZOIA Librarian.app`:

```sh
xcrun stapler staple '/path/to/release/products/ZOIA Librarian.app'
xcrun stapler validate '/path/to/release/products/ZOIA Librarian.app'
codesign --verify --deep --strict '/path/to/release/products/ZOIA Librarian.app'
spctl --assess --type execute --verbose=2 '/path/to/release/products/ZOIA Librarian.app'
ditto -c -k --norsrc --noextattr --keepParent '/path/to/release/products/ZOIA Librarian.app' '/path/to/ZOIA-Librarian-macOS.zip'
shasum -a 256 '/path/to/ZOIA-Librarian-macOS.zip' > '/path/to/ZOIA-Librarian-macOS.zip.sha256'
```

## Distribution

Download the final ZIP through a browser and test launching it, patch import,
export, PatchStorage access, and SD card operations before publishing. Test on
the oldest macOS version you intend to support. The archive targets the Python
environment's architecture; it is not automatically a universal Intel/Apple
Silicon build.

For an Intel release, set `ZOIA_PYTHON` to the absolute path of
`venv_x86/bin/python` and set `ZOIA_TARGET_ARCH=x86_64` before running the release
script. All bundled native dependencies must contain an Intel slice. The build
checks the resulting executable's architecture before notarization and names
the ZIP using that architecture.

Attach the final `ZOIA-Librarian-…-macOS-….zip` and `.sha256` file to a GitHub
release or host them on your website. Do not distribute `notarization-upload.zip`,
which was created before stapling. Provide the GPL license, corresponding source,
and required dependency notices with your release.

References: [Apple notarization workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow)
and [PyInstaller macOS signing](https://pyinstaller.org/en/stable/feature-notes.html#macos-binary-code-signing).
