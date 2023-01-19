The momentum calculation routine `calcMomentum` used by the `rf_sol_tracking` code is written in Fortran for speed, since it's an iterative calculation and difficult to vectorise. I can only apologise for this, it's caused a lot of pain. But it does run really really fast.

The code is in the `momentum_calc.f90` file. Here are the steps I used to compile it using the **f2py** package on Windows. We've now moved to Python 3, and I originally did this on Python 2, so I've rewritten the instructions. Pay careful attention to version numbers.

1. I used Python 3.9, and I found that the simplest thing to do was to install [Miniconda3](https://docs.conda.io/en/latest/miniconda.html). Sub-steps for using Miniconda:
   1. Download [Miniconda3 Windows 64-bit](https://docs.conda.io/en/latest/miniconda.html).
   2. Open a Miniconda3 prompt (Start > start typing "miniconda").
   3. Create a new environment: `conda create -n py39`
   4. Activate it: `conda activate py39`
   5. Install Python 3.9, Numpy, and Scipy. There are probably other things you need too. For now, `conda install python=3.9 numpy scipy`
2. **f2py** is part of Numpy, so you shouldn't need to install it separately.
3. Install the MinGW64 port of GCC (GNU Compiler Collection), including **gfortran**. I used the **GCC 12.1.0 + LLVM/Clang/LLD/LLDB 14.0.6** download (it was the latest release at the time) available [here](https://winlibs.com/#download-release) (via [this page](https://www.mingw-w64.org/downloads/#mingw-builds)). You need the Win64 version. Just extract the archive to `C:\mingw64` (so that this folder has `bin`, `include`, `lib` subfolders etc).
4. Install a Microsoft Visual C++ compiler. You need to use the same one that Python was compiled with (this is shown when you start Python, it's the bit that looks like `MSC v.1916 64 bit (AMD64)`). For Python 3.9, use [Visual Studio Professional 2019](https://visualstudio.microsoft.com/vs/older-downloads/) (v16.7). When installing, you just need to check the box marked **Desktop development with C++**.
5. Open a command prompt (the Anaconda prompt if you have it). Run `C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat`. This sets up compiler paths and suchlike.
6. Add the MinGW64 binaries directory to the path. You can do this temporarily in the Command Prompt window using `set path=%path%;C:\mingw64\bin`.
7. Run **f2py** to compile the code. In the `Parasol` folder: `f2py -c --fcompiler=gnu95 --compiler=mingw32 -m calcMomentum momentum_calc.f90`. To see all the logs, run `set DISTUTILS_DEBUG=1` first.
8. Some warnings may be displayed; you can safely ignore them. You should end up with a file called `calcMomentum.cp39-win_amd64.pyd` in the Parasol folder. A simple test can be carried out by running `python rf_sol_tracking.py`.

For Linux, it's a lot easier. Assuming Numpy is already installed, just do `f2py -c -m calcMomentum momentum_calc.f90`. This will build a `calcMomentum.so` file that can be used on Linux.

Here is the output from **f2py** for reference.

```dos
(py39) C:\Users\bjs54\GitHub\Software\Apps\Parasol>f2py -c --fcompiler=gnu95 --compiler=mingw32 -m calcMomentum momentum_calc.f90
running build
running config_cc
INFO: unifing config_cc, config, build_clib, build_ext, build commands --compiler options
running config_fc
INFO: unifing config_fc, config, build_clib, build_ext, build commands --fcompiler options
running build_src
INFO: build_src
INFO: building extension "calcMomentum" sources
INFO: f2py options: []
INFO: f2py:> C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentummodule.c
creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9
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
          t,gamma_dash,gamma,beta,p = calcmomentum(freq,phase,gamma_start,dz,gamma_tilde_dash,phase_offset)
    Wrote C/API module "calcMomentum" to file "C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentummodule.c"
    Fortran 90 wrappers are saved to "C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentum-f2pywrappers2.f90"
INFO:   adding 'C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.c' to sources.
INFO:   adding 'C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9' to include_dirs.
copying C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\f2py\src\fortranobject.c -> C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9
copying C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\f2py\src\fortranobject.h -> C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9
INFO:   adding 'C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentum-f2pywrappers2.f90' to sources.
INFO: build_src: building npy-pkg config files
running build_ext
dllwrap: WARNING: dllwrap is deprecated, use gcc -shared or ld -shared instead

INFO: customize Mingw32CCompiler
INFO: customize Mingw32CCompiler using build_ext
INFO: customize Gnu95FCompiler
INFO: Found executable C:\mingw64\bin\gfortran.exe
INFO: customize Gnu95FCompiler using build_ext
INFO: building 'calcMomentum' extension
INFO: compiling C sources
INFO: C compiler: gcc -g -DDEBUG -DMS_WIN64 -O0 -Wall -Wstrict-prototypes

creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users
creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54
creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata
creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local
creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local\temp
creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local\temp\tmp62j12s6s
creating C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local\temp\tmp62j12s6s\src.win-amd64-3.9
INFO: compile options: '-DNPY_DISABLE_OPTIMIZATION=1 -D__MSVCRT_VERSION__=0x1916 -IC:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9 -IC:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -c'
INFO: gcc -g -DDEBUG -DMS_WIN64 -O0 -Wall -Wstrict-prototypes -DNPY_DISABLE_OPTIMIZATION=1 -D__MSVCRT_VERSION__=0x1916 -IC:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9 -IC:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -c C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentummodule.c -o C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local\temp\tmp62j12s6s\src.win-amd64-3.9\calcmomentummodule.o
INFO: gcc -g -DDEBUG -DMS_WIN64 -O0 -Wall -Wstrict-prototypes -DNPY_DISABLE_OPTIMIZATION=1 -D__MSVCRT_VERSION__=0x1916 -IC:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9 -IC:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -c C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.c -o C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local\temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.o
In file included from In file included from
ers\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/ndarraytypes.h:1960
                 from ,
                 from C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/ndarrayobject.h:12C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/ndarrayobject.h:12,
                 from
                 from C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/arrayobject.h:5
py39\lib\site-packages\numpy\core\include/numpy/arrayobject.h:5
                 from ,
                 from C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.h:13C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.h:13,
                 from ,
                 from C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentummodule.c:20C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.c:2:
:
C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/npy_1_7_deprecated_api.h:14:9:C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/npy_1_7_deprecated_api.h:14:9:  note: note: ''#pragma message: C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/npy_1_7_deprecated_api.h(14) : Warning Msg: Using deprecated NumPy API, disable it with #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION#pragma message: C:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include/numpy/npy_1_7_deprecated_api.h(14) : Warning Msg: Using deprecated NumPy API, disable it with #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION'
   14 | #pragma '
   14 | #pragma messagemessage(_WARN___LOC__"Using deprecated NumPy API, disable it with " \
      |         (_WARN___LOC__"Using deprecated NumPy API, disable it with " \
      |         ^~~~~~~^~~~~~~

C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.c: In function 'fortran_doc':
C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.c:322:52: warning: unknown conversion type character 'z' in format [-Wformat=]
  322 |             "fortranobject.c: fortran_doc: len(p)=%zd>%zd=size:"
      |                                                    ^
C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.c:322:56: warning: unknown conversion type character 'z' in format [-Wformat=]
  322 |             "fortranobject.c: fortran_doc: len(p)=%zd>%zd=size:"
      |                                                        ^
C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.c:322:13: warning: too many arguments for format [-Wformat-extra-arg
]
  322 |             "fortranobject.c: fortran_doc: len(p)=%zd>%zd=size:"
      |             ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
INFO: compiling Fortran sources
INFO: Fortran f77 compiler: C:\mingw64\bin\gfortran.exe -Wall -g -ffixed-form -fno-second-underscore -O3 -funroll-loops
Fortran f90 compiler: C:\mingw64\bin\gfortran.exe -Wall -g -fno-second-underscore -O3 -funroll-loops
Fortran fix compiler: C:\mingw64\bin\gfortran.exe -Wall -g -ffixed-form -fno-second-underscore -Wall -g -fno-second-underscore -O3 -funroll-loops
INFO: compile options: '-IC:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9 -IC:\Users\bjs54\Miniconda3\envs\py39\lib\site-packages\numpy\core\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -IC:\Users\bjs54\Miniconda3\envs\py39\include -c'
INFO: gfortran.exe:f90: momentum_calc.f90
momentum_calc.f90:56:2:

   56 |         do j = 1, size(gamma_tilde_dash,1)
      |         1
Warning: Nonconforming tab character at (1) [-Wtabs]
momentum_calc.f90:58:2:

   58 |         end do
      |         1
Warning: Nonconforming tab character at (1) [-Wtabs]
INFO: gfortran.exe:f90: C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentum-f2pywrappers2.f90
INFO: C:\mingw64\bin\gfortran.exe -Wall -g -Wall -g -shared C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local\temp\tmp62j12s6s\src.win-amd64-3.9\calcmomentummodule.o C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\users\bjs54\appdata\local\temp\tmp62j12s6s\src.win-amd64-3.9\fortranobject.o C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\momentum_calc.o C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\Release\Users\bjs54\AppData\Local\Temp\tmp62j12s6s\src.win-amd64-3.9\calcMomentum-f2pywrappers2.o -Lc:\mingw64\lib -Lc:\mingw64\lib\gcc\x86_64-w64-mingw32\12.2.0 -LC:\Users\bjs54\Miniconda3\envs\py39\libs -LC:\Users\bjs54\Miniconda3\envs\py39\PCbuild\amd64 -lpython39 -lgfortran -o .\calcMomentum.cp39-win_amd64.pyd
Removing build directory C:\Users\bjs54\AppData\Local\Temp\tmp62j12s6s
```
