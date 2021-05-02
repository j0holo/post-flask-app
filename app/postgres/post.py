from dataclasses import dataclass
from time import time


@dataclass
class Post:
    id: int
    title: str
    slug: str
    author: str
    posted_at: time
    updated_at: time
    content: str