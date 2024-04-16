from IDisplayService import IDisplayService
from SourceView import SourceView
import lxml.etree as etree


class SourceViewDisplay(IDisplayService):
    source_view: SourceView

    def __init__(self, source_view: SourceView):
        self.source_view = source_view

    def display(self, content: bytes) -> None:

        ext = ".xml"
        try:
            x = etree.fromstring(content)
            content = etree.tostring(x, pretty_print=True, encoding="utf-8")
        except Exception:
            ext = ".txt"

        try:
            content = content.decode("utf-8")
        except Exception:
            content = "<[= Binary Data or Decode Error=]>"

        self.source_view.set_text(content, ext)

    def clear(self) -> None:
        self.source_view.set_text(None, None)

