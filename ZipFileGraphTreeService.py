import zipfile
import typing
from typing import Self
from IGraphTreeService import IGraphTreeService


class File:
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


class ZipFileGraphTreeService(IGraphTreeService):
    root: File = None
    zip_file: zipfile.ZipFile = None

    def list_items(self, path: str):
        if self.root is None:
            self.root = File.create_root()

        if not self.root.is_folder():
            self.zip_file = zipfile.ZipFile(path)
            name_list = self.zip_file.namelist()
            for full_name in name_list:
                current_root = self.root
                full_name_parts = full_name.split("/")
                for file_name in full_name_parts:
                    current_file: File = current_root.get_child(file_name)
                    if current_file is None:
                        current_file = File(file_name)
                        current_root.add_child(current_file)
                    current_root = current_file

            return self.root

        path_parts = path.split("/")
        result = self.root
        for file_name in path_parts:
            result = result.get_child(file_name)

        return result

    def get_short_item_name(self, item: File) -> str:
        return item.file_name

    def get_full_item_name(self, item: File) -> str:
        return item.get_full_path()

    def is_item_folder(self, item: File) -> bool:
        return item.is_folder()

    def get_item_content(self, item: File) -> bytes:
        if item.is_folder():
            return "[" + item.get_full_path() + "]"
        return self.zip_file.open(item.get_full_path()).read()  # .decode("utf-8")


class ZipFileData:
    file_name: str
    is_directory: bool

    def __init__(self, file_name: str, is_directory: bool):
        self.file_name = file_name
        self.is_directory = is_directory
