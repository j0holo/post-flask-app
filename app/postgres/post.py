from dataclasses import dataclass
from time import time


@dataclass
class Post:
    id: int
    title: str
    slug: str
    author: int
    posted_at: time
    updated_at: time
    content: str