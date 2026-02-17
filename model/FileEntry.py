import typing
from typing import Self


class FileEntry:
    file_name: str
    parent: Self
    children: typing.Dict[str, Self]

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.children = None
        self.parent = None

    def is_folder(self) -> bool:
        return self.children is not None

    def add_child(self, child: Self) -> None:
        if self.children is None:
            self.children = {}

        self.children[child.file_name] = child
        child.parent = self

    def get_child(self, file_name: str) -> Self:
        if self.children is None:
            return None

        if file_name not in self.children:
            return None

        return self.children[file_name]

    def get_full_path(self) -> str:
        result = self.file_name
        current_file = self
        while current_file.parent is not None and current_file.parent.file_name is not None:
            result = current_file.parent.file_name + "/" + result
            current_file = current_file.parent

        return result

    def __iter__(self):
        result = [] if self.children is None else list(self.children.values())
        s = sorted(result, key=lambda item: item.file_name.capitalize())
        return iter(sorted(s, key=lambda item: not item.is_folder()))

    @classmethod
    def create_root(cls) -> Self:
        return cls(None)
