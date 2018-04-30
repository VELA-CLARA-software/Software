# -*- mode: python -*-

block_cipher = None


a = Analysis(['mainApp.py'],
             pathex=['\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Stage\\Software\\Apps\\BYScIT\\v2'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='JammyDodger',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='resources\\byscitv2\\icon.ico')
