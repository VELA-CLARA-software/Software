import glob, os

#os.chdir("/mydir")
for file in glob.glob("*.in.*"):
    print(file)
