class IGraphTreeService:

    def list_items(self, path: str):
        pass

    def get_short_item_name(self, item) -> str:
        pass

    def get_full_item_name(self, item) -> str:
        pass

    def is_item_folder(self, item) -> bool:
        pass

    def get_item_content(self, item) -> bytes:
        pass
