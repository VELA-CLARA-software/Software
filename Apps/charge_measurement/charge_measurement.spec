# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['charge_measurement.py'],
             pathex=['E:\\VELA-CLARA-software\\Software\\Apps\\charge_measurement', '\\\\192.168.83.14\\claranet\\test\\CATAP\\bin\\', '\\\192.168.83.14\\claranet\\test\\Controllers\\bin\\python3_x64'],
             binaries=[ ( '\\\\192.168.83.14\\claranet\\test\\CATAP\\bin\\', '.' ) ],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt4'],
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
          [],
          name='charge_measurement',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
