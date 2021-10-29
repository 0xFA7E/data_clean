from hashlib import new
import re
import sys
import argparse
import io

def isValidHash(md5string):
    """check if provided string is valid format for md5"""
    md5format = re.compile('^[a-f0-9]{32}$')
    return md5format.match(md5string.strip())

def read_hashes(file):
    hashes = io.open(file,mode='r', encoding="utf-8")
    for i in file.readlines():
        if isValidHash(i):
            hashes.append(i+'\n')
    file.close()
    return hashes

def merge(files):
    """merge the md5 hashes for the provided files. Treats the first file as the reference"""
    hashcount = 0
    hashes = read_hashes(files[0])
    starthashcount = len(hashes)
    if args.verbose >= 1:
        print(f"Loaded {starthashcount} hashes")
    
    for i in files[1:]:
        newhashes = read_hashes(i)
        newhashcount = len(hashes)
        for n in newhashes:
            if n not in hashes:
                hashes.append(i)
        if args.verbose >= 1:
            print(f"Added {len(hashes)-newhashcount} new hashes from {i}")
    if args.stats:
        print(f"Added total of {len(hashes)-starthashcount} hashes.")
    
    return hashes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Supporting utility for merging hash collections")
    parser.add_argument("inputfiles", type=str, nargs="+",
                        help="Files to process")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increased output")
    parser.add_argument("-s", "--stats", action="store_true",
                        help="Print a summary of changes. Newly added hashes based on the first provided hashfile")
    parser.add_argument("-o","--output", type=str,
                        help="output file for results")

    # Print the help message if no arguments
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if len(args.inputfiles) < 2:
        print("[!!] Need more than 1 input files to merge")
        sys.exit(1)
    if not args.output:
        print("[!!] Need an output destination")
    
    hashes = merge(args.inputfiles)
    outfile = io.open(args.output, mode="w", encoding="utf-8")
    outfile.writelines(hashes)
