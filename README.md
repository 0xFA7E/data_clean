# identify_files
A small utility for mass identifying and renaming a list of unknown files(Mainly for Windows) based on Libmagic.
Inspired usecase is having recovered several hundred files with a utility like Recuva, but the filenames lack an extension
for windows to properly associate them with an application for opening. 

# usage
```
usage: file_identify.py [-h] [-v] [-r] [-t] location [location ...]

A utility for renaming unknown files in Windows according to its mimetype as
identified by Libmagic

positional arguments:
  location         Identify file(s) and changes the filename to nearest match

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbose    Increased output, -v for changed files, -vv for all files
  -r, --recursive  Recursively descend into subfolders
  -t, --test       Identify file(s) but do not change filename(s)
```
