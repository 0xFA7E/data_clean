from os.path import isfile
import sys
import argparse
from typing import Tuple
from data_clean.commands import Config
from data_clean.configuration import ArgConfig
from data_clean.hashing import hash_file
from data_clean.processing import files_from_dir

hashes = []
DEFAULT_HASHFILE = "collected_hashes.txt"

def parse_args() -> Tuple[argparse.ArgumentParser, Config]:
    parser = argparse.ArgumentParser(description="Supporting utility for collecting new hashes from systems")
    parser.add_argument("location", type=str, nargs="+",
                        help="File(s)/Directories to process")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increased output")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Recursively descend into subfolders.")
    parser.add_argument("-s", "--stats", action="store_true",
                        help="Print a summary of changes")
    parser.add_argument("-e", "--exclude", type=str, nargs="+",
                        help="List of directories to exclude from hashing")
    parser.add_argument("-o", "--output", type=str,
                        help="Output file to store hashes from. Default is collected_hashes.txt in current dir")
    parser.add_argument("-a","--append", action="store_true",
                        help="Append to output file instead of overwriting")

    # Print the help message if no arguments
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    if not args.output:
        args.output = DEFAULT_HASHFILE

    config = ArgConfig()
    config.parse(args)
    return args, config

def main():
    args, config = parse_args()
    if config.verbose:
        print("Searching for hashes...")

    if args.exclude:
        #will not recognize an excluded directory if trailing slashes added because dumb reasons.
        args.exclude = [i.rstrip('/') for i in args.exclude]

    for names in args.location:
        if isfile(names):
            file_hash = hash_file(names)
            if file_hash and file_hash not in hashes:
                hashes.append(file_hash+'\n')
        else:
            files = files_from_dir(names, recursive=args.recursive, exclude=args.exclude)
            for file in files:
                file_hash = hash_file(file)
                if file_hash not in hashes:
                    hashes.append(file_hash+'\n')


    if config.verbose:
        print("Done collecting, outputting now")

    try:
        if args.append:
            with open(args.output, "a", encoding="utf-8") as file:
                file.writelines(hashes)
        else:
            with open(args.output, "w", encoding="utf-8") as file:
                file.writelines(hashes)

    except Exception as error:
        print(f'Failed to write hashes to file {args.output} : {error}')
    if args.stats:
        print(f"{len(hashes)} Collected Hashes.")



if __name__ == "__main__":
    main()
   