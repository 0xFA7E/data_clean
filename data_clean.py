import sys
from os.path import isfile
import argparse
import logging

from data_clean.hashing import read_hashes
from data_clean.logger import setup_logger
from data_clean.processing import files_from_dir
from data_clean.stats import Stats

DEFAULT_HASHFILE = "hashes.txt"


def parse_args() -> argparse.ArgumentParser:
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
    parser.add_argument("-H", "--hashfile", type=str,
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

    #set logger from verbosity
    setup_logger(args.verbose)
    
    if args.all:
        args.cleanse = True
        args.identify = True

    #set hashfile if not set
    if not args.hashfile:
        args.hashfile = DEFAULT_HASHFILE
    return args


def main():
    #parse arguments
    args = parse_args()    

    #Create stat tracking object
    stats = Stats()

    #Get List of Files to process
    files = []
    for names in args.location:
        if isfile(names):
            files.append(names)
        else:
            files = files_from_dir(names)

    if args.identify:
        pass

    if args.cleanse:
    #Read the hashes now so that were not trying to reopen the hash file everytime we process a file, probably a better way to do this
        hashes = read_hashes(args.hashfile) 
    
    if args.stats:
        print(f"{stats.changed} Changed files, {stats.deleted} Deleted files, {stats.unchanged} Unchanged files")


if __name__ == "__main__":
    main()
    logging.info("VERBOSE TEST")
    logging.warning("VERY VERBOSE TEST")
    logging.debug("Debug test")
