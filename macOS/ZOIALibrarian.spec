# Build the established flattened desktop distribution, using PyInstaller 6 APIs.
import os
import platform
from pathlib import Path

source = Path(os.environ['ZOIA_STAGING'])
identity = os.environ.get('ZOIA_CODESIGN_IDENTITY') or None
version = os.environ.get('ZOIA_VERSION', '2.1')
build_number = os.environ.get('CI_BUILD_NUMBER') or os.environ.get('CURRENT_PROJECT_VERSION', '1')
minimum_macos = os.environ.get('MACOSX_DEPLOYMENT_TARGET', '15.6')
app_store = os.environ.get('ZOIA_APP_STORE', 'NO') == 'YES'
nonexempt_encryption = os.environ.get('ZOIA_USES_NONEXEMPT_ENCRYPTION') or 'NO'
if nonexempt_encryption not in ('YES', 'NO'):
    raise SystemExit('ZOIA_USES_NONEXEMPT_ENCRYPTION must be YES or NO')
target_arch = os.environ.get('ZOIA_TARGET_ARCH') or None
entitlements = None
if app_store:
    if target_arch not in (None, 'arm64'):
        raise SystemExit('App Store builds require ZOIA_TARGET_ARCH=arm64')
    target_arch = 'arm64'
    entitlements = str(Path(SPECPATH) / 'app-store-entitlements.plist')
    # Sandbox file access is granted by native macOS open/save panels. Change
    # only the flattened staging copy, leaving local and Developer ID code alone.
    for staged_module in source.glob('*.py'):
        text = staged_module.read_text(encoding='utf-8')
        if 'QFileDialog.DontUseNativeDialog' in text:
            staged_module.write_text(
                text.replace('QFileDialog.DontUseNativeDialog', 'QFileDialog.Option(0)'),
                encoding='utf-8',
            )
elif identity and (target_arch or platform.machine()) in ('x86_64', 'universal2'):
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
bundle_info = {'NSHighResolutionCapable': True,
               'CFBundleVersion': build_number,
               'LSMinimumSystemVersion': minimum_macos,
               'LSApplicationCategoryType': 'public.app-category.music',
               'NSPrincipalClass': 'NSApplication'}
if app_store:
    bundle_info['ITSAppUsesNonExemptEncryption'] = nonexempt_encryption == 'YES'
app = BUNDLE(collection, name='ZOIA Librarian.app',
             icon=str(source / 'logo.icns'), bundle_identifier='com.zoialibrarian.desktop',
             version=version, info_plist=bundle_info)
