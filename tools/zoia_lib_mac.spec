# -*- mode: python -*-

import os

spec_root = os.path.abspath(SPECPATH)
block_cipher = None
app_name = 'ZOIA Librarian'
mac_icon = os.path.join(spec_root, 'logo.icns')
version = '2.0'

a = Analysis(
    ['startup.py'],
    pathex=[spec_root],
    binaries=[('orderedmultidict/__version__.py', 'orderedmultidict/')],
    datas=[('*.css', '.'), ('*.html', '.'), ('*.json', '.'), ('*.png', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    # target_arch='x86_64', # uncomment for Intel-based Mac
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name=app_name
)

app = BUNDLE(
    coll,
    name=app_name + '.app',
    icon=mac_icon,
    bundle_identifier='com.myidentifier',
    version=version,
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'LSFileQuarantineEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'My File Format',
                'CFBundleTypeIconFile': 'logo.icns',
                'LSItemContentTypes': ['com.example.myformat'],
                'LSHandlerRank': 'Owner',
		        'CFBundleTypeRole': 'Editor',
            }
        ]
    },
)
