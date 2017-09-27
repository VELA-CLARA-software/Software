# -*- mode: python -*-

block_cipher = None


a = Analysis(['mainApp_2.py'],
             pathex=['C:\\Users\\wln24624\\Desktop\\v2 Monitor\\EXE'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
			 
a.datas += [ ('schem.png', '.\\schem.png', 'DATA')]
a.datas += [ ('Quadrupoles.png', '.\\Quadrupoles.png', 'DATA')]
a.datas += [ ('Dipoles.png', '.\\Dipoles.png', 'DATA')]
a.datas += [ ('Correctors.png', '.\\Correctors.png', 'DATA')]
a.datas += [ ('Solenoids.png', '.\\Solenoids.png', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          debug=False,
          strip=False,
          upx=True,
		  name='Ozwald',
          console=True, icon='oz_S9U_1.ico' )
