# -*- mode: python -*-

block_cipher = None


a = Analysis(['mainApp.py'],
             pathex=['D:\\VELA\\GIT Projects\\Software\\Apps\\Virtual_Cathode_Setup\\virtual_cathode_setup_3'],
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
          name='Virtual_Cathode_App',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='resources\\Virtual_Cathode_App\\Virtual_Cathode_App.ico')