# This will install Chocolatey - a package manager for Windows.
# See https://chocolatey.org/ for more details.
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
#iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex

# Now use Chocolatey to install Miniconda for Python 2. We need the 32-bit (x86) version.
# More details: https://conda.io/docs/
# Anaconda is a fully-featured Python distribution. 
# Miniconda is a super-lite version; we can just add the bits that we need.
choco install miniconda --x86 -y

Write-Host "Finished installing Python."
Write-Host "Now close and reopen PowerShell, and run " -NoNewLine
Write-Host "setup-part2-python.ps1 " -ForegroundColor yellow -NoNewLine
Write-Host "to install packages required for VELA/CLARA software."
Write-Host "Press any key to exit..."
[void][System.Console]::ReadKey($true)
