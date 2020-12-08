# -*- mode: python -*-

block_cipher = None

#'VELA_CLARA_Magnet_Control',
#'VELA_CLARA_BPM_Control',
#'VELA_CLARA_LLRF_Control',
#'VELA_CLARA_Charge_Control',
#'VELA_CLARA_Camera_Control',
#'VELA_CLARA_Screen_Control',

a = Analysis(['mainApp.py'],
             pathex=["C:\Users\jkj62\Documents\GitHub\Software\Apps\CTRApp",
             "C:\Users\jkj62\Documents\GitHub",
             "C:\Users\jkj62\.conda\envs\py2qt4min\\Lib\\site-packages\\scipy\\extra-dll",
             "C:\Users\jkj62\.conda\envs\py2qt4min\Lib\site-packages\zmq",
             "\\\\claraserv3\\claranet\\test\\Controllers\\bin\\Release",
             ],
             binaries=[],
             datas=[("C:\Users\jkj62\.conda\envs\py2qt4min\Lib\site-packages\epics\clibs\win32\ca.dll", '.'),
             ("C:\Users\jkj62\.conda\envs\py2qt4min\Lib\site-packages\epics\clibs\win32\Com.dll",'.'),
             ],
             hiddenimports=['socket', 'epics', 'epics.clibs', 'numpy', 'collections', 'six', 'scipy._lib.messagestream', 'zmq', 'dict_to_h5',
             'Software.Procedures.qt',
             'Software.Procedures.Machine.signaller',
             'Software.Procedures.linacTiming',
             'Software.Procedures.qt',
             'Software.Utils.dict_to_h5',
             ],
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
          name='CTRAppv0.1',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True,)