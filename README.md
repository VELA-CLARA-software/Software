# Software
A place to store software tools for VELA/CLARA

# Installation
Many of these tools are written using Python. The standard toolset consists of:
- Python 2.7 32-bit
- PyQt4
- pyqtgraph
- numpy
- scipy

On Windows, you can use a standard Python distribution (like [WinPython](http://winpython.github.io/) or [Anaconda](https://www.continuum.io/downloads)) - these packages both have everything you need to get started.

If you'd prefer a lightweight installation, you can do the following:
- Open a PowerShell prompt in administrator mode (Start > start typing PowerShell > right-click Windows PowerShell > Run as administrator).
- Run the command `\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\GitHub_repo\setup-part1-conda.ps1`. This will install [Chocolatey](https://chocolatey.org/) (a package manager) and then Miniconda.
- Close and reopen PowerShell as admin again (to pick up changes to PATH).
- Run the command `\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\GitHub_repo\setup-part2-python.ps1`. This will install some standard packages:
 - PyQt4
 - SciPy
 - Numpy
 - VELA/CLARA hardware controllers

You can now install any of the software tools directly from the GitHub repository using the following command (from an admin command prompt). For instance, for the Magnet Table app:

`pip install git+https://github.com/VELA-CLARA-software/Software.git#subdirectory=magnet-table`

To install all the apps at once (at least, all the ones that have a `setup.py` file), run the following script under an admin command prompt:

`\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\GitHub_repo\setup-part3-all-apps.ps1`

Now, you can run the magnet table from Python:

`python -m magnet-table`
