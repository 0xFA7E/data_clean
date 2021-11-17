from hashlib import md5

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
