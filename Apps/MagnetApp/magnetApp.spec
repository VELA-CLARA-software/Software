# -*- mode: python -*-

block_cipher = None


a = Analysis(['magnetApp.py'],
             pathex=['D:\\VELA\\GIT Projects\\Software\\Apps\\MagnetApp'],
             binaries=[('H:\\Controllers\\bin\\stage', 'VELA_CLARA_Magnet_Control.pyd')],
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
          name='magnetApp',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
