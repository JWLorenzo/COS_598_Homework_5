from typing import Any


class Actor:

    def __init__(self, name: str, type: str, images: list[Any]) -> None:
        self.name: str = name
        self.type: str = type
        self.images: list[Any] = images
