The momentum calculation routine `calcMomentum` used by the `rf_sol_tracking` code is written in Fortran for speed, since it's an iterative calculation and difficult to vectorise. The code is in the `momentum_calc.f90` file. Here are the steps I used to compile it using the **f2py** package on Windows.

1. **f2py** is part of Numpy, so you shouldn't need to install it separately.
2. Install the MinGW32 port of GCC (GNU Compiler Collection), including **gfortran**.
3. Install a Microsoft Visual C++ compiler. I followed the instructions in [this answer](https://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat?noredirect=1&lq=1#18045219) and installed [Visual Studio C++ 2008](http://download.microsoft.com/download/A/5/4/A54BADB6-9C3F-478D-8657-93B3FC9FE62D/vcsetup.exe) since my Python (Miniconda2, Python 2.7.12) was compiled with it.
4. Open a command prompt. Run `"C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat"`.
5. Run **f2py** to compile the code. In the `magnet-table` folder: `python "C:\Program Files (x86)\Miniconda2\Scripts\f2py.py" -c --fcompiler=gnu95 -m calcMomentum momentum_calc.f90`

For Linux, it's a lot easier. Assuming Numpy is already installed, just do `f2py -c -m calcMomentum momentum_calc.f90`. This will build a `calcMomentum.so` file that can be used on Linux.

Here is the output from **f2py** for reference.

```dos
C:\Documents\GitHub\Software\magnet-table>py -2 "C:\Program Files (x86)\Miniconda2\Scripts\f2py.py"  -c --fcompiler=gnu95 -m calcMomentum momentum_calc.f90
running build
running config_cc
unifing config_cc, config, build_clib, build_ext, build commands --compiler options
running config_fc
unifing config_fc, config, build_clib, build_ext, build commands --fcompiler options
running build_src
build_src
building extension "calcMomentum" sources
f2py options: []
f2py:> c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentummodule.c
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7
Reading fortran codes...
        Reading file 'momentum_calc.f90' (format:free)
Post-processing...
        Block: calcMomentum
                        Block: calcmomentum
In: :calcMomentum:momentum_calc.f90:calcmomentum
get_parameters: got "name 'atan' is not defined" on '4.0*atan(1.0)'
Post-processing (stage 2)...
Building modules...
        Building module "calcMomentum"...
                Creating wrapper for Fortran subroutine "calcmomentum"("calcmomentum")...
                Constructing wrapper function "calcmomentum"...
                  t,gamma_dash,gamma,beta,p = calcmomentum(freq,phase,gamma_start,dz,gamma_tilde_dash)
        Wrote C/API module "calcMomentum" to file "c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentummodule.c"
        Fortran 77 wrappers are saved to "c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentum-f2pywrappers.f"
  adding 'c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\fortranobject.c' to sources.
  adding 'c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7' to include_dirs.
copying C:\Program Files (x86)\Miniconda2\lib\site-packages\numpy\f2py\src\fortranobject.c -> c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7
copying C:\Program Files (x86)\Miniconda2\lib\site-packages\numpy\f2py\src\fortranobject.h -> c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7
  adding 'c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentum-f2pywrappers.f' to sources.
build_src: building npy-pkg config files
running build_ext
customize MSVCCompiler
customize MSVCCompiler using build_ext
customize Gnu95FCompiler
Found executable C:\MinGW\bin\gfortran.exe
customize Gnu95FCompiler using build_ext
building 'calcMomentum' extension
compiling C sources
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs
creating c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7
C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\BIN\cl.exe /c /nologo /Ox /MD /W3 /GS- /DNDEBUG /arch:SSE2 -Ic:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7 -I"C:\Program Files (x86)\Miniconda2\lib\site-packages\numpy\core\include" -I"C:\Program Files (x86)\Miniconda2\include" -I"C:\Program Files (x86)\Miniconda2\PC" /Tcc:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentummodule.c /Foc:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentummodule.obj
C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\BIN\cl.exe /c /nologo /Ox /MD /W3 /GS- /DNDEBUG /arch:SSE2 -Ic:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7 -I"C:\Program Files (x86)\Miniconda2\lib\site-packages\numpy\core\include" -I"C:\Program Files (x86)\Miniconda2\include" -I"C:\Program Files (x86)\Miniconda2\PC" /Tcc:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\fortranobject.c /Foc:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\fortranobject.obj
compiling Fortran sources
Fortran f77 compiler: C:\MinGW\bin\gfortran.exe -Wall -g -ffixed-form -fno-second-underscore -O3 -funroll-loops
Fortran f90 compiler: C:\MinGW\bin\gfortran.exe -Wall -g -fno-second-underscore -O3 -funroll-loops
Fortran fix compiler: C:\MinGW\bin\gfortran.exe -Wall -g -ffixed-form -fno-second-underscore -Wall -g -fno-second-underscore -O3 -funroll-loops
compile options: '-Ic:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7 -I"C:\Program Files (x86)\Miniconda2\lib\site-packages\numpy\core\include" -I"C:\Program Files (x86)\Miniconda2\include" -I"C:\Program Files (x86)\Miniconda2\PC" -c'
gfortran.exe:f90: momentum_calc.f90
gfortran.exe:f77: c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentum-f2pywrappers.f
copying c:\mingw\lib\gcc\mingw32\5.3.0\libgfortran.a -> c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\gfortran.lib
copying c:\mingw\lib\gcc\mingw32\5.3.0\libgcc.a -> c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\gcc.lib
copying c:\mingw\lib\libmingw32.a -> c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\mingw32.lib
copying c:\mingw\lib\libmingwex.a -> c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\mingwex.lib
C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\BIN\link.exe /DLL /nologo /INCREMENTAL:NO /LIBPATH:c:\mingw\lib\gcc\mingw32\5.3.0 /LIBPATH:c:\mingw\lib /LIBPATH:"C:\Program Files (x86)\Miniconda2\libs" /LIBPATH:"C:\Program Files (x86)\Miniconda2\PCbuild" /LIBPATH:"C:\Program Files (x86)\Miniconda2\PC\VS9.0" /LIBPATH:c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release /LIBPATH:"C:\Program Files (x86)\Miniconda2\libs" /LIBPATH:"C:\Program Files (x86)\Miniconda2\PCbuild" /LIBPATH:"C:\Program Files (x86)\Miniconda2\PC\VS9.0" gfortran.lib gcc.lib mingw32.lib mingwex.lib /EXPORT:initcalcMomentum c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentummodule.obj c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\fortranobject.obj c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\momentum_calc.o c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentum-f2pywrappers.o /OUT:.\calcMomentum.pyd  /IMPLIB:c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentum.lib /MANIFESTFILE:c:\users\bjs5403\appdata\local\temp\tmp9pvtzs\Release\users\bjs5403\appdata\local\temp\tmp9pvtzs\src.win32-2.7\calcMomentum.pyd.manifest
Removing build directory c:\users\bjs5403\appdata\local\temp\tmp9pvtzs
```
