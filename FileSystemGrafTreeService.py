import os
import stat

from IGraphTreeService import IGraphTreeService


class FileSystemGrafTreeService(IGraphTreeService):
    path: str

    def list_items(self, path: str):
        self.path = path
        return os.listdir(path)

    def get_short_item_name(self, item):
        return item

    def get_full_item_name(self, item) -> str:
        return os.path.join(self.path, item)

    def is_item_folder(self, item) -> bool:
        itemMetaData = os.stat(self.get_full_item_name(item))
        return stat.S_ISDIR(itemMetaData.st_mode)
