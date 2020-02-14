# -*- mode: python -*-


# from command line pyinstaller --onefile -w --icon=.\resources\Virtual_Cathode_Setup\blue_laser.ico -n "VC_Setup" VC_Setup.spec

block_cipher = None


a = Analysis(['mainApp.py'],
             pathex=['D:\\VELA\\GIT Projects\\Software\\Apps\\Virtual_Cathode_Setup\\v1'],
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
          name='VC_Setup',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
		  manifest=None,
          console=True , icon='resources\\Virtual_Cathode_Setup\\blue_laser.ico')