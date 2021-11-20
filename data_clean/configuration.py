from abc import ABC, abstractmethod
import argparse
from dataclasses import dataclass
@dataclass
class Config(ABC):
    test: bool = False
    verbose: bool = False
    very_verbose: bool = False
    debug: bool = False

    @abstractmethod
    def parse(self, **kwargs) -> None:
        ...

@dataclass
class ArgConfig(Config):
    def parse(self, args=argparse.ArgumentParser) -> None:
        if hasattr(args, 'test'):
            self.test = args.test
        if args.verbose:
            self.verbose = True
        if args.verbose >= 2:
            self.very_verbose = True
        if args.verbose >= 3:
            self.debug = True
        
