# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\mainApp_2.py'],
             pathex=['C:\\Users\\wln24624\\Desktop\\v2 Monitor\\Icons'],
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
          name='mainApp_2',
          debug=False,
          strip=False,
          upx=True,
          console=True )
