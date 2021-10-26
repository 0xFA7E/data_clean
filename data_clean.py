import sys

import magic
from os import listdir, rename
from os.path import isfile, join, isdir
import argparse

changed = 0
unchanged = 0
deleted = 0
hashlist = "hashes.txt"

def get_file_extension(filename):
    """we leverage Libmagic for actual filetype identification and grab a viable mimetype
    to use as an extension. This may not be perfect for all filetypes, but ought to be
    'good enough' to get you close. Of course if the file is some obscure proprietary stuff
    then oh well"""

    try:
        filetype = magic.from_file(filename, mime=True)
        ext = filetype.split('/')[1]
        if ext == "plain":
            # Libmagic returns basic text as "plain" so lets call it txt instead
            ext = "txt"
        return '.' + ext

    except Exception as error:
        # I actually have no clue what kind of error libmagic can throw, but lets catch all
        # just in case so the entire script doesnt die on one naughty file
        print(f"[!!] Libmagic encountered error processing {filename} with error {error}")
        return ""


def is_unknown(filename):
    """Windows uses extensions to determine if it knows the filetype or not, so we only
    care here if there is no extension in the filename"""
    return '.' not in filename


def identify_file(filename):
    """If we don't know what kind of file it is, find out, otherwise leave it alone"""
    global changed
    global unchanged
    if is_unknown(filename):
        ext = get_file_extension(filename)
        name = filename + ext
        if args.verbose >= 1:
            print("[*] " + name)
        if not args.test:
            try:
                rename(filename, name)
                changed += 1
            except Exception as error:
                print(f"[!] Could not rename {filename} because of error {error}")
        else:
            unchanged += 1
    else:
        name = filename
        unchanged += 1
        if args.verbose >= 2:
            print(name)
    return name


def process_dir(directory):
    """Takes a directory as a string and processes it for files to identify or delete, if recursive is set
    it will descend into those as well"""
    files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
    for file in files:
        process_file(file)
    if args.recursive:
        # we're descending recursively but not checking for any looping redirects or anything, take care humans
        directories = [join(directory, dirs) for dirs in listdir(directory) if isdir(join(directory, dirs))]
        for d in directories:
            process_dir(d)

def process_file(filename):
    """Process a filename and decide what actions to preform based on the arguments provided"""
    if (args.identify or args.all):
        identify_file(filename)
    if(args.cleanse or args.all):
        cleanse_file(filename)
    return

def cleanse_file(filename):
    """Check if a file must be deleted based on the hashlist"""
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A utility for cleaning up data pulled from file recovery\
                                                software. Can identify files with unknown extentions with Libmagic\
                                                and delete some system files based on a list of hashes.")
    parser.add_argument("location", type=str, nargs="+",
                        help="File(s)/Directories to process")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increased output, -v for changed files, -vv for all files")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Recursively descend into subfolders")
    parser.add_argument("-t", "--test", action="store_true",
                        help="Process but do not make changes.")
    parser.add_argument("-s", "--stats", action="store_true",
                        help="Print a summary of changes")
    parser.add_argument("-a","--all", action="store_true",
                        help="Preform both identify and cleansing operations")
    parser.add_argument("-i", "--identify", action="store_true",
                        help="Identify Mode. Rename file extensions based on Libmagic")
    parser.add_argument("-c", "--cleanse", action="store_true",
                        help="Delete junk files by comparing to a hashlist. Default is hashes.txt")
    parser.add_argument("-H", "--hashlist", action="store_true",
                        help="hashlist to use in conjuction with --cleanse or --all")
    # Print the help message if no arguments
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if (not args.identify and not args.cleanse and not args.all):
    #no actions provided
        print("[!!] No actions provided, none taken!")
        sys.exit(1)
    for names in args.location:
        if isfile(names):
            process_file(names)
        else:
            process_dir(names)
    if args.stats:
        print(f"{changed} Changed files, {deleted} Deleted files, {unchanged} Unchanged files")
