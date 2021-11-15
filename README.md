# data_clean
A utility for cleaning up data pulled from file recovery software. Can identify files with unknown extentions with Libmagic and delete some system files based on a list of hashes.

Inspired usecase is having recovered several hundred files with a utility like Recuva, but the filenames lack an extension
for windows to properly associate them with an application for opening. 

Currently updating to add the ability to remove system and other junk files based on a hashlist gathered from other systems. Hence the project rename. 

# TODO

1. Update usage

2. Implement empty folder deletion

3. Deduplicate files

4. Refactor hashcollector+hashmerge

5. Investigate feasibility of parallelization(would def rework whole structure)

6. Collect more file hashes from various systems to make more robust cleaning. 
  5a. Include utility to collect hashes for more rapid harvesting from new systems

7. Setup dev branch

# usage
Note: Usage here is outdated as project is being updated. Refer to program help for more information.

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
  -s, --stats      Print a summary of changes

```
# Hash Collection List

This is a non-exhaustive list of OSes/Software that has currently had hashes collected from.

```
MacOS Catalina 10.15.7
MacOs Mavericks 10.9.5
Windows 7 Home
Windows 10 Home
```