# -*- mode: python -*-

import os

spec_root = os.path.abspath(SPECPATH)
block_cipher = None
app_name = 'ZOIA Librarian'
icon = os.path.join(spec_root, 'logo.ico')
version = '2.0'

a = Analysis(['startup.py'],
             pathex=['C:\\Users\\m.moger\\source\\Projects\\zoia_lib\env\\Lib\\site-packages'],
             binaries=[('C:\\Users\m.moger\\source\\Projects\\zoia_lib\\distro\\orderedmultidict\\__version__.py', '.\\orderedmultidict\\')],
             datas=[('*.css', '.'), ('*.html', '.'), ('*.json', '.'), ('*.png', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
	  a.binaries,
	  a.zipfiles,
	  a.datas,
          name=app_name,
          debug=False,
          strip=False,
          upx=True,
          console=False,
	  icon=icon)
