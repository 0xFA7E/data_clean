
from os import remove
from data_clean.commands import Command
from data_clean.hashing import hash
class Cleanse(Command):
    def run(self):
        for file in self.files:
            if self.cleanse_file(file):
                self.stats.deleted += 1
                self.files.remove(file)
        return self.files


    def cleanse_file(self,filename: str) -> bool:
        """Check if a file must be deleted based on the hashlist"""
        file_hash = hash(filename)
        if self.debug:
            print(f'[!] Hash {file_hash}, filename {filename}')
        if file_hash in self.hashes:
            if self.verbose:
                print(f"[*] Found {filename} in hashlist[{hash}]. Marked for deletion")
            if not self.test:
                try:
                    remove(filename)
                    return True
                except Exception as error:
                    print(f"[!!] Could not delete {filename} because {error}")
                    return False
