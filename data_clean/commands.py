from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from data_clean.stats import Stats

@dataclass
class Config():
    test: bool = False
    verbose: bool = False
    very_verbose: bool = False
    debug: bool = False
    dedupe: bool = False

class Command(ABC):
    def __init__(self, files: list[str], config: Config, stats: Stats, hashes: Optional[list[str]] = list[str]):
        self.files = files
        self.stats = stats
        self.test = config.test
        self.verbose = config.verbose
        self.debug = config.debug
        self.dedupe = config.dedupe
        self.hashes = hashes
        super().__init__()

    @abstractmethod
    def run(self) -> list[str]:
        pass
