from typing import Protocol

class Command(Protocol):
    """A command to process a file with"""
    
    def execute(self):
        """run on the file"""