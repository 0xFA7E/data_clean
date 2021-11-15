def cleanse_file(filename: str, hashes: list, test: bool=False, verbose: bool = False, debug: bool = False):
    """Check if a file must be deleted based on the hashlist"""
    if debug:
        print(f'[!] Hash {hash}, filename {filename}')
    if hash in hashes:
        if verbose:
            print(f"[*] Found {filename} in hashlist[{hash}]. Marked for deletion")
        if not test:
            try:
                file.close()
                remove(filename)
                return True
            except Exception as error:
                print(f"[!!] Could not delete {filename} because {error}")
                return False
