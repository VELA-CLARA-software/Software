# -*- mode: python -*-

block_cipher = None


a = Analysis(['MagnetTable.py'],
             pathex=['C:\\Documents\\GitHub\\Software\\Apps\\MagnetTable'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.binaries = a.binaries - [('mfc90.dll', None, None), ('mfc90u.dll', None, None)]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='MagnetTable',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='resources\\magnetTable\\Icons\\magnet.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MagnetTable')
