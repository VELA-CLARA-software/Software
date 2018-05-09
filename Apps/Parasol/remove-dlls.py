# Intended to be inserted into the parasol.spec file, after the a = Analysis( ... ) line
# Remove some DLLs not required for this program to reduce pyinstaller final file size
# If something breaks, try commenting out these lines

a.binaries = a.binaries - [('mfc90.dll', None, None), ('mfc90u.dll', None, None),
                           ('libdfft_sub.H7JUQMC4GS7DN3IVX42HFJNOTBCNHRQU.gfortran-win32.dll', None, None),
                           ('libd_odr.2WJGGT6XFUIAAOYY5SE7NV6JL36EC5WH.gfortran-win32.dll', None, None),
                           ('libbanded5x.5UCGLP2PKOSYT6Q63AINYBWC45Y3SM5R.gfortran-win32.dll', None, None)]
