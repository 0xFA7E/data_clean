from os import listdir
from os.path import isfile, join, isdir
from hashlib import md5
import sys
import argparse

hashes = []
hashfile = "collected_hashes.txt"

def hash_file(filename):
    """Add the hash of a file to the hash list"""
    global hashes
    try:
        file = open(filename,'rb')
        hash = md5(file.read()).hexdigest()
    except Exception as error:
        print(f"[!!] Failed to get md5 of {filename} because {error}")
        return False
    if hash+'\n' not in hashes:
        hashes.append(hash+'\n')
        if args.verbose >= 2:
            print(f"Found hash: {hash}")
    return

def hash_dir(directory):
    """Process directory for files to hash"""
    files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
    for file in files:
        hash_file(file)
    if not args.unrecursive:
        # we're descending recursively but not checking for any looping redirects or anything, take care humans
        directories = [join(directory, dirs) for dirs in listdir(directory) if isdir(join(directory, dirs))]
        #print(directories)
        #print(args.exclude)
        for d in directories:
            if d in args.exclude:
                if args.verbose >=1:
                    print(f"Skipping {d}")
                continue
            hash_dir(d)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Supporting utility for collecting new hashes from systems")
    parser.add_argument("location", type=str, nargs="+",
                        help="File(s)/Directories to process")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increased output")
    parser.add_argument("-u", "--unrecursive", action="store_true",
                        help="DONT recursively descend into subfolders. By default the tool aims to hash entire systems.")
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

    if args.verbose >=1:
        print("Searching for hashes...")

    if args.exclude:
        #will not recognize an excluded directory if trailing slashes added because dumb reasons.
        args.exclude = [i.rstrip('/') for i in args.exclude]

    for names in args.location:
        if isfile(names):
            hash_file(names)
        else:
            hash_dir(names)
    if args.verbose >= 1:
        print("Done collecting, outputting now")

    if args.output:
        hashfile = args.output
    
    try:
        if args.append:
            file = open(hashfile, "a")
        else:
            file = open(hashfile,"w")

        file.writelines(hashes)
    
    except Exception as error:
        print(f"Failed to write hashes to file {hashfile} : {error}")

    if args.stats:
        print(f"{len(hashes)} Collected Hashes.")
