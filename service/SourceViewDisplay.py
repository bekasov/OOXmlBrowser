from model.ISourceViewer import ISourceViewer
from model.IDisplayService import IDisplayService

from model.IXmlFormatter import IXmlFormatter
from xmlformatter.EtreeXmlFormatter import EtreeXmlFormatter


class SourceViewDisplay(IDisplayService):
    source_view: ISourceViewer
    xml_converter: IXmlFormatter

    def __init__(self, source_view: ISourceViewer):
        self.source_view = source_view
        self.xml_converter = EtreeXmlFormatter()

    def display(self, content: bytes) -> None:
        ext = ".xml"
        text_content, success = self.xml_converter.convert_from_bytes(content, True)
        if not success:
            ext = ".txt"
            text_content = ""

        try:
            text_content = text_content.decode("utf-8")
        except Exception:
            text_content = "<[= Binary Data or Decode Error =]>"

        self.source_view.set_text(text_content, ext)

    def clear(self) -> None:
        self.source_view.set_text(None, None)

