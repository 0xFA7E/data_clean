from abc import ABC, abstractmethod
from typing import Optional
from data_clean.stats import Stats
from data_clean.configuration import Config
class Command(ABC):
    def __init__(self, files: list[str], config: Config, stats: Stats, hashes: Optional[list[str]] = list[str]):
        self.files = files
        self.stats = stats
        self.test = config.test
        self.verbose = config.verbose
        self.debug = config.debug
        self.hashes = hashes
        super().__init__()

    @abstractmethod
    def run(self) -> list[str]:
        pass
