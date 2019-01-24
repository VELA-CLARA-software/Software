# -*- mode: python -*-

block_cipher = None


a = Analysis(['unitsConverter.py'],
             pathex=['c:\\anaconda32\\work\\Software\\Utils\\unitsConverter','c:\\anaconda32\\work\\Software\\Misc','c:\\anaconda32\\work\\Software\\Procedures\\Machine',
             "\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release", 'C:\\anaconda32\\envs\\py2qt4min\\Lib\\site-packages\\scipy\\extra-dll',],
             binaries=[],
             datas=[('./unitsConverter.ico','.')],
             hiddenimports=['VELA_CLARA_Magnet_Control','scipy._lib.messagestream', 'numpy', 'collections', 'six'],
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
          name='unitsConverter',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True)
