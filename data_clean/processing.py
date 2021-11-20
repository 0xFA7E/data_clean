from os.path import isfile, join, isdir
from os import listdir
from typing import Optional


def files_from_dir(directory: str, recursive: bool = False, exclude: Optional[list[str]] = None) -> list[str]:
    """Takes a directory as a string and processes it for files to identify or delete, if recursive is set
    it will descend into those as well"""
    if not exclude:
        exclude = []
    files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f)) and join(directory,f) not in exclude]
    if recursive:
        # we're descending recursively but not checking for any looping redirects or anything, take care humans
        directories = [join(directory, dirs) for dirs in listdir(directory) if isdir(join(directory, dirs)) and join(directory,dirs) not in exclude]
        for d in directories:
            files.extend(files_from_dir(d, recursive=True))
    return files
