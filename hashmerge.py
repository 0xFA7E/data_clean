from hashlib import new
import sys
import argparse
import io

from data_clean.hashing import isValidHash

def read_hashes(file: str) -> list[str]:
    hashes = []
    with open(file, 'r', encoding='utf-8') as hashlist:
        for file_hash in hashlist.readlines():
            if isValidHash(file_hash):
                #newlines may be inconsistent so we strip em and then add one to normalize
                hashes.append(file_hash.strip()+'\n')
    return hashes

def merge(file: list[str], hashes: list[str]) -> list[str]:
    """merge the md5 hashes for the provided files."""
    newhashes = read_hashes(file)
    #if not hashes:
    #    if args.verbose >= 1:
    #        print(f"Added {len(newhashes)} hashes from {file}")
    #    return newhashes
    merged_hashes = list(set(hashes + newhashes))
    if args.verbose >= 1:
        print(f"Added {len(merged_hashes)-len(hashes)} hashes from {file}")
    return merged_hashes
#     hashcount = 0
#    for file_hash in newhashes:
#        if file_hash not in hashes:
#            hashes.append(file_hash)
#            hashcount += 1
#    if args.verbose >= 1:
#        print(f"Added {hashcount} hashes from {file}")
#    return hashes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Supporting utility for merging hash collections")
    parser.add_argument("inputfiles", type=str, nargs="+",
                        help="Files to process")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increased output")
    parser.add_argument("-s", "--stats", action="store_true",
                        help="Print a summary of changes.")
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
    
    hashes = []
    for file in args.inputfiles:
        hashes = merge(file, hashes)
    if args.stats:
        print(f"Added {len(hashes)} hashes total.")
    with open(args.output, 'w', encoding='utf8') as outfile:
        outfile.writelines(hashes)
