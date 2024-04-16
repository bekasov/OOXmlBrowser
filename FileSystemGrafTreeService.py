import os
import stat

from IGraphTreeService import IGraphTreeService


class FileSystemGrafTreeService(IGraphTreeService):
    path: str

    def ListItems(self, path: str):
        self.path = path
        return os.listdir(path)

    def GetShortItemName(self, item):
        return item

    def GetFullItemName(self, item) -> str:
        return os.path.join(self.path, item)

    def IsItemFolder(self, item) -> bool:
        itemMetaData = os.stat(self.GetFullItemName(item))
        return stat.S_ISDIR(itemMetaData.st_mode)
