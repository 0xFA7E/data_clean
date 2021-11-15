from dataclasses import dataclass

@dataclass
class Stats():
    num_of_files: int = 0
    deleted: int = 0
    changed: int = 0

    @property
    def unchanged(self) -> int:
        return self.num_of_files - self.deleted - self.changed
