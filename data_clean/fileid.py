from os import rename
import magic

from data_clean.commands import Command
class Identify(Command):
    def run(self):
        for file in self.files:
            if self.identify_file(file):
                self.stats.changed += 1

    def identify_file(self, filename: str) -> bool:
        """If we don't know what kind of file it is, find out, otherwise leave it alone. Return true if we changed it, false if we didnt"""
        if self.is_unknown(filename):
            ext = self.get_file_extension(filename)
            name = filename + ext
            if self.verbose:
                print("[*] " + name)
            if not self.test:
                try:
                    rename(filename, name)
                    return True
                except Exception as error:
                    print(f"[!] Could not rename {filename} because of error {error}")
        else:
            name = filename
            if self.debug:
                print(name)
        return False

    def get_file_extension(self, filename: str) -> str:
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

    def is_unknown(self, filename: str) -> bool:
        """Windows uses extensions to determine if it knows the filetype or not, so we only
        care here if there is no extension in the filename"""

        #strip out some nix styled relative addressing that may messup our filename checks
        if './' in filename:
            filename = filename.strip('./')

        if self.debug:
            print(f"[!] {filename}, {'.' not in filename}")

        return '.' not in filename
