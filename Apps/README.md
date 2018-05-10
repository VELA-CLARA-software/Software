# Compiling to EXE using pyinstaller

I (@benshep) started using **pyinstaller** to package my files this week, and it was a bit hard at first but I got there in the end. Here, for the benefit of future generations, is the wisdom of my experience.

The **pyinstaller** command is something like (from inside your app folder):

```bat
pyinstaller --onefile --noconfirm -i resources\magnetTable\Icons\magnet.ico --windowed MagnetTable.py
```

What do the flags do I hear you cry? Well, `--onefile` will package all your files into one (as is the convention), `--noconfirm` will overwrite things without asking; `-i` gives your app a nice icon; and `--windowed` means that no console window will be shown. (You might want one if there's going to be important debugging information in it. But of course my code is completely bug-free.)

This will create a file called `MagnetTable.exe` in the `dist` folder. If you've got any resource files (icons and suchlike) you'll want to copy the `resource` folder into `dist`. Then copy everything under `dist` to the server.

## But my EXE files are huge!

Yes, they are.

Now this can really send you down a deep rabbit hole. But never fear! I've been down it and found the carrots for you. Skip the next paragraph if you don't want the boring explanation.

**Numpy** uses, at its heart, some fast vector libraries. If you use the ones provided by **Anaconda** (as I was naïvely doing), it'll install MKL. This is a monster created by Intel which does the fast vector stuff. There are alternatives though, notably **OpenBLAS**. If you use the **pip**-provided **numpy**, it will use **OpenBLAS** instead and your executable files will be magically reduced in size without losing any functionality or speed, and without you having to meet any rabbits.

Still with me? I found [this comment](https://github.com/pyinstaller/pyinstaller/issues/2270#issuecomment-384074743), leading to [this answer](https://stackoverflow.com/questions/43886822/pyinstaller-with-pandas-creates-over-500-mb-exe/48846546#48846546) which I will reproduce here. You need to create a conda environment but install **numpy** using **pip** like this. Open your **Anaconda Prompt** and type the following: (by default you'll be in `C:\Users\username`, but I don't think it matters where you are)

```bat
mkdir small-numpy
cd small-numpy
conda create -n small-numpy python=2
activate small-numpy
python -m pip install numpy scipy pyinstaller
conda install pyqt=4
```

You need to use **conda** to install **PyQt** since **pip** won't do it. That's OK. Don't forget to install any other packages you need (either with **pip** or **conda**) since you're in a clean conda environment.

Easy. Now you can navigate to your app folder, and use the **pyinstaller** command as detailed above. I got a reduction in file size from 74MB to 19MB using this method. That should make a big difference to start-up times.

I managed to shave off a couple of extra MB by removing another two DLL files, with apparently no adverse effects (i.e. my app still ran). After you've run **pyinstaller** once, it will create an `AppName.spec` file in your app folder. Open this and edit it. It's just a Python file. After the `a = Analysis( ... )` line, insert the following:

```python
a.binaries = a.binaries - [('mfc90.dll', None, None), ('mfc90u.dll', None, None)]
```

Now rerun the *pyinstaller* command, but type `AppName.spec` at the end instead of `AppName.py` (it will use the modified `.spec` file instead of generating its own).

## Including scipy

Adding scipy into your pyinstaller exe can be more difficult than expected. A simple recipe that has so far always worked for me (@titchjones) is the following:
1. Create your **spec** file as per the instructions above
2. In the spec file add the location of your scipy **extra-dll** directory to the **pathex** line - for instance: 
```bat
pathex=['C:\\anaconda32\\Lib\\site-packages\\scipy\\extra-dll'],
```
3. Add `'scipy._lib.messagestream'` to the hiddenimports section - i.e.:
```bat
hiddenimports=['scipy._lib.messagestream'],
```
4. Done!

#Compiling to exe using py2exe

I (@LouiseCowie) do it a different way - in py2exe. I got all this from two sources: the py2exe tutorial page http://www.py2exe.org/index.cgi/Tutorial, and this excellent blog post that fixed all the issues I had https://pythontips.com/2014/03/03/using-py2exe-the-right-way/ .

1. Install py2exe from https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/

2. Make a setup file and save it in the same location as your python script. I call mine setup.py.

To make "YourApp.py" into a bundled executable, it should look like this:

from distutils.core import setup
import py2exe
setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True,"includes":["sip"]}},
    windows = [{'script': "YourApp.py"}],
    zipfile = None,
)

3. Open the command prompt from the location of your python script and setup file. 

4. Run the command : python setup.py py2exe

5. Look in your dist folder and ta-dah! A bundled python executable file.