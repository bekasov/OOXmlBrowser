from model.ISourceViewer import ISourceViewer
from model.IDisplayService import IDisplayService

from model.IXmlFormatter import IXmlFormatter
from service.Utils import get_extension


class SourceViewDisplay(IDisplayService):
    source_view: ISourceViewer
    xml_converter: IXmlFormatter

    def __init__(self, source_view: ISourceViewer, xml_converter: IxmlFormatter):
        self.source_view = source_view
        self.xml_converter = xml_converter

    def display(self, file_name: str, content: bytes) -> None:
        ext: str = get_extension(file_name)
        text_content = content
        if ext != ".bin":
            text_content, success = self.xml_converter.convert_from_bytes(content, True)
            if success:
                ext = ".xml"
            try:
                text_content = text_content.decode("utf-8")
            except Exception:
                text_content = SourceViewDisplay.hexdump(text_content)
                ext = ".hex"
        else:
            text_content = SourceViewDisplay.hexdump(text_content)
            ext = ".hex"

        self.source_view.set_text(file_name, text_content, ext)

    def clear(self) -> None:
        self.source_view.clear()

    @staticmethod
    def hexdump(data, bytes_per_line=16) -> str:
        if isinstance(data, str):
            data = data.encode('utf-8')
        result = []
        for i in range(0, len(data), bytes_per_line):
            chunk = data[i:i+bytes_per_line]
            address = f"{i:08x}"
            hex_part = ' '.join(f"{b:02x}" for b in chunk)
            if len(chunk) < bytes_per_line:
                hex_part = hex_part.ljust(bytes_per_line * 3 - 1)
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            result.append(f"{address}  {hex_part}  | {ascii_part} |")
        return '\n'.join(result)

