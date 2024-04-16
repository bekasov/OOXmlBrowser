class IGraphTreeService:

    def ListItems(self, path: str):
        pass

    def GetShortItemName(self, item) -> str:
        pass

    def GetFullItemName(self, item) -> str:
        pass

    def IsItemFolder(self, item) -> bool:
        pass

    def GetItemContent(self, item) -> bytes:
        pass
