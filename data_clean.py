import sys
from hashlib import md5
import magic
from os import close, listdir, rename, remove
from os.path import isfile, join, isdir
import argparse

changed = 0
unchanged = 0
deleted = 0
hashfile = "hashes.txt"
hashes = []

def read_hashes(hashfile):
    """generate the list of hashes based on provided hashfile"""
    global hashes
    hashcount = 0
    file = open(hashfile,'r')
    for i in file.readlines():
        hashes.append(i.strip())
        hashcount += 1
    file.close()
    if args.verbose >= 1:
        print(f"Loaded {hashcount} hashes")
    return hashes

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
    
    #strip out some nix styled relative addressing that may messup our filename checks
    if './' in filename:
        filename = filename.strip('./')

    if args.verbose >= 3:
        print(f"[!] {filename}, {'.' not in filename}")
    
    return '.' not in filename

def identify_file(filename):
    """If we don't know what kind of file it is, find out, otherwise leave it alone"""
    if is_unknown(filename):
        ext = get_file_extension(filename)
        name = filename + ext
        if args.verbose >= 1:
            print("[*] " + name)
        if not args.test:
            try:
                rename(filename, name)
                return True
            except Exception as error:
                print(f"[!] Could not rename {filename} because of error {error}")
    else:
        name = filename
        if args.verbose >= 2:
            print(name)
    return False

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
    global deleted
    global changed
    global unchanged
    """Process a filename and decide what actions to preform based on the arguments provided"""
    if(args.cleanse or args.all):
        cleansed = cleanse_file(filename)
        if cleansed:
            #we deleted the file, dont need to identify it
            deleted += 1
            return
    if (args.identify or args.all):
        renamed = identify_file(filename)
        if renamed:
            changed += 1
            return
    #we neither deleted or renamed anything
    unchanged += 1 
    return

def cleanse_file(filename):
    """Check if a file must be deleted based on the hashlist"""
    global hashes
    try:
        file = open(filename,'rb')
        hash = md5(file.read()).hexdigest()
    except Exception as error:
        print(f"[!!] Failed to get md5 of {filename} because {error}")
        return False
    if args.verbose >= 3:
        print(f'[!] Hash {hash}, filename {filename}')
    if hash in hashes:
        if args.verbose >= 1:
            print(f"[*] Found {filename} in hashlist[{hash}]. Marked for deletion")
        if not args.test:
            try:
                file.close()
                remove(filename)
                return True
            except Exception as error:
                print(f"[!!] Could not delete {filename} because {error}")
                return False

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

    if args.cleanse or args.all:
    #Read the hashes now so that were not trying to reopen the hash file everytime we process a file, probably a better way to do this
        if args.hashfile:
            hashfile = args.hashfile
        hashes = read_hashes(hashfile) 
    
    for names in args.location:
        if isfile(names):
            process_file(names)
        else:
            process_dir(names)
    if args.stats:
        print(f"{changed} Changed files, {deleted} Deleted files, {unchanged} Unchanged files")
