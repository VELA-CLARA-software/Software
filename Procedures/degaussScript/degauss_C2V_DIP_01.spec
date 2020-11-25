# -*- mode: python -*-

block_cipher = None


a = Analysis(['degaussC2V_DIP_01.py'],
             pathex=['C:\\Users\\wln24624\\Documents\\SOFTWARE\\VELA-CLARA-Software\\Software\\Procedures\\degaussScript'],
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
          name='degauss_C2V_DIP_01',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
