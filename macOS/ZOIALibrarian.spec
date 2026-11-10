# Build the established flattened desktop distribution, using PyInstaller 6 APIs.
import os
import platform
from pathlib import Path

source = Path(os.environ['ZOIA_STAGING'])
identity = os.environ.get('ZOIA_CODESIGN_IDENTITY') or None
version = os.environ.get('ZOIA_VERSION', '2.1')
target_arch = os.environ.get('ZOIA_TARGET_ARCH') or None
entitlements = None
if identity and (target_arch or platform.machine()) in ('x86_64', 'universal2'):
    entitlements = str(Path(SPECPATH) / 'intel-entitlements.plist')
a = Analysis(
    [str(source / 'startup.py')],
    pathex=[str(source)],
    datas=[(str(path), '.') for pattern in ('*.css', '*.html', '*.json', '*.png', '*.ui')
           for path in source.glob(pattern)],
    hiddenimports=['orderedmultidict.__version__'],
    excludes=['PyQt5', 'PyQt6', 'PySide2'],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='ZOIA Librarian',
          console=False, strip=False, upx=False, codesign_identity=identity,
          target_arch=target_arch, entitlements_file=entitlements)
collection = COLLECT(exe, a.binaries, a.datas, name='ZOIA Librarian', strip=False, upx=False)
app = BUNDLE(collection, name='ZOIA Librarian.app',
             icon=str(source / 'logo.icns'), bundle_identifier='com.zoialibrarian.desktop',
             version=version, info_plist={'NSHighResolutionCapable': True,
                                       'NSPrincipalClass': 'NSApplication'})
