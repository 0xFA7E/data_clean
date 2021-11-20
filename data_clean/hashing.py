from hashlib import md5
import re

def isValidHash(md5string):
    """check if provided string is valid format for md5"""
    md5format = re.compile('^[a-f0-9]{32}$')
    return md5format.match(md5string.strip())

def read_hashes(hashfile: str, verbose: bool = False) -> list:
    """generate the list of hashes based on provided hashfile"""
    hashes: list = []
    hashcount: int = 0
    with open(hashfile,'r',encoding='utf8') as file:
        for i in file.readlines():
            hashes.append(i.strip())
            hashcount += 1
    if verbose:
        print(f"Loaded {hashcount} hashes")
    return hashes

def hash_file(filename: str) -> str:
    try:

        with open(filename, 'rb') as f:
            file_hash = md5(f.read()).hexdigest()
    except FileNotFoundError:
        print(f"Error hashing {filename}. Seems to not exist anymore.")
        return None
    return file_hash
