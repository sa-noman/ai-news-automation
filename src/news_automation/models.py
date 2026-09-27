from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Article:
    title: str
    link: str
    description: str = ""
    source: str = ""
    published: str = ""
    category: str = "Other"
    summary: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
