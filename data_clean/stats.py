from dataclasses import dataclass

@dataclass
class Stats():
    deleted: int = 0
    changed: int = 0
    unchanged: int = 0