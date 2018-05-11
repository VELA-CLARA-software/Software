# -*- mode: python -*-

block_cipher = None


a = Analysis(['parasol.py'],
             pathex=['C:\\Documents\\GitHub\\Software\\Apps\\Parasol'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.binaries = a.binaries - [('mfc90.dll', None, None), ('mfc90u.dll', None, None),
                           ('libdfft_sub.H7JUQMC4GS7DN3IVX42HFJNOTBCNHRQU.gfortran-win32.dll', None, None),
                           ('libd_odr.2WJGGT6XFUIAAOYY5SE7NV6JL36EC5WH.gfortran-win32.dll', None, None),
                           ('libbanded5x.5UCGLP2PKOSYT6Q63AINYBWC45Y3SM5R.gfortran-win32.dll', None, None)]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='parasol',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='resources\\parasol\\Icons\\parasol.ico')
