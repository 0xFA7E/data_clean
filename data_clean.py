"""Main tool for cleaning up files namely for data recovery purposes"""

import sys
from os.path import isfile
import argparse
from typing import Tuple
from data_clean.cleanse import Cleanse
from data_clean.commands import Config
from data_clean.fileid import Identify

from data_clean.hashing import read_hashes
from data_clean.processing import files_from_dir
from data_clean.stats import Stats

DEFAULT_HASHFILE = "hashes.txt"

def parse_args() -> Tuple[argparse.ArgumentParser, Config]:
    """Parse arguments from the cmdline, return the parsed arguments and some configuration object stuff"""

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
    parser.add_argument("-D", "--dedupe", action="store_true",
                        help="Remove duplicated files")
    parser.add_argument("-H", "--hashfile", type=str,
                        help="hashlist to use in conjuction with --cleanse or --all")
    # Print the help message if no arguments
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    actions = [args.identify, args.cleanse, args.dedupe, args.all]
    if (not any(actions)):
    #no actions provided
        print("[!!] No actions provided, none taken!")
        sys.exit(1)

    if args.all:
        args.cleanse = True
        args.identify = True
        args.dedupe = True

    #set hashfile if not set
    if not args.hashfile:
        args.hashfile = DEFAULT_HASHFILE

    #convert verbose into Config object
    config = Config()
    if args.verbose >=1:
        config.verbose = True
    if args.verbose >=2:
        config.very_verbose = True
    if args.verbose >=3 :
        config.debug = True

    config.test = args.test
    config.dedupe = args.dedupe

    return args, config


def main():
    #parse arguments
    args, config = parse_args()

    #Create stat tracking object
    stats = Stats()

    #Get List of Files to process
    files = []
    for names in args.location:
        if isfile(names):
            files.append(names)
        else:
            files = files_from_dir(names)
    stats.num_of_files = len(files)

    #cleanse files first before identify
    #check for just dedupe removal
    if args.dedupe and not args.cleanse:
        cleanse = Cleanse(files=files, hashes=[], config=config, stats=stats)
        files = cleanse.run()
    #if dedupe is set regular cleanse will handle it too
    if args.cleanse:
        hashes = read_hashes(args.hashfile, config.verbose)
        cleanse = Cleanse(files=files, hashes=hashes, config=config, stats=stats)
        files = cleanse.run()

    if args.identify:
        identify = Identify(files=files, config=config, stats=stats)
        identify.run()


    if args.stats:
        print(f"{stats.changed} Changed files, {stats.deleted} Deleted files, {stats.unchanged} Unchanged files")


if __name__ == "__main__":
    main()
