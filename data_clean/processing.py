from os.path import isfile, join, isdir
from os import listdir


def files_from_dir(directory: str, recursive: bool = False) -> list[str]:
    """Takes a directory as a string and processes it for files to identify or delete, if recursive is set
    it will descend into those as well"""
    files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
    if recursive:
        # we're descending recursively but not checking for any looping redirects or anything, take care humans
        directories = [join(directory, dirs) for dirs in listdir(directory) if isdir(join(directory, dirs))]
        for d in directories:
            files.extend(files_from_dir(d, recursive=True))
    return files
