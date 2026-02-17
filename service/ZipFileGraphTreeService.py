import zipfile
from model.IGraphTreeService import IGraphTreeService
from model.FileEntry import FileEntry


class ZipFileGraphTreeService(IGraphTreeService):
    root: FileEntry = None
    zip_file: zipfile.ZipFile = None

    def list_items(self, path: str):
        if self.root is None:
            self.root = FileEntry.create_root()

        if not self.root.is_folder():
            self.zip_file = zipfile.ZipFile(path)
            name_list = self.zip_file.namelist()
            for full_name in name_list:
                current_root: FileEntry = self.root
                full_name_parts = full_name.split("/")
                if full_name.endswith("/") and full_name_parts[-1] == '':
                    full_name_parts.pop()
                for file_name in full_name_parts:
                    current_file: FileEntry = current_root.get_child(file_name)
                    if current_file is None:
                        current_file = FileEntry(file_name)
                        current_root.add_child(current_file)
                    current_root = current_file

            return self.root

        path_parts = path.split("/")
        result = self.root
        for file_name in path_parts:
            result = result.get_child(file_name)

        return result

    def get_short_item_name(self, item: FileEntry) -> str:
        return item.file_name

    def get_full_item_name(self, item: FileEntry) -> str:
        return item.get_full_path()

    def is_item_folder(self, item: FileEntry) -> bool:
        return item.is_folder()

    def get_item_content(self, item: FileEntry) -> bytes:
        file_name: str = item.get_full_path()
        return self.zip_file.open(file_name).read()  # .decode("utf-8")
