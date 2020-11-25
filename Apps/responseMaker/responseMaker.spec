# -*- mode: python -*-

block_cipher = None


a = Analysis(['responseMaker.py'],
             pathex=['c:\\anaconda32\\Work\\Software\\Apps\\responseMaker'],
             binaries=[
              (r"C:\anaconda32\envs\py3qt5min\Lib\site-packages\epics\clibs\win32\ca.dll", 'epics/clibs/ca.dll'),
              (r"C:\anaconda32\envs\py3qt5min\Lib\site-packages\epics\clibs\win32\carepeater.exe", 'epics/clibs/carepeater.exe'),
              (r"C:\anaconda32\envs\py3qt5min\Lib\site-packages\epics\clibs\win32\Com.dll",'epics/clibs/Com.dll')
             ],
             datas=[
             (r"C:\anaconda32\envs\py3qt5min\Lib\site-packages\epics\clibs\win32\Com.dll",'.'),
             (r"C:\anaconda32\envs\py3qt5min\Lib\site-packages\epics\clibs\win32\ca.dll", '.'),
             ],
             hiddenimports=['epics'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.binaries = a.binaries - [('mfc90.dll', None, None), ('mfc90u.dll', None, None)]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='responseMaker',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
