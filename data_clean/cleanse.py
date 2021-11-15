
from os import remove
from data_clean.commands import Command
from data_clean.hashing import hash_file
class Cleanse(Command):
    def run(self):
        removed_files: list[str] = []
        for file in self.files:
            if self.cleanse_file(file):
                self.stats.deleted += 1
                removed_files.append(file)
        #there was a skipping bug if we removed an item during operation of files, so list comp to return clean list
        return [file for file in self.files if file not in removed_files]


    def cleanse_file(self,filename: str) -> bool:
        """Check if a file must be deleted based on the hashlist"""
        file_hash = hash_file(filename)
        if self.debug:
            print(f'[!] Hash {file_hash}, filename {filename}')
        if file_hash in self.hashes:
            if self.verbose:
                print(f"[*] Found {filename} in hashlist[{file_hash}]. Marked for deletion")
            if not self.test:
                try:
                    remove(filename)
                    return True
                except Exception as error:
                    print(f"[!!] Could not delete {filename} because {error}")
                    return False
            return False
        #if were dudplicating files we append the hash so the next instance of a file found will get cleansed
        if self.dedupe:
            self.hashes.append(file_hash)
        
        #Didnt find anything so exiting false
        return False
