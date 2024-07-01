from model.IXmlFormatter import IXmlFormatter
import lxml.etree as etree


class EtreeXmlFormatter(IXmlFormatter):
    def convert_from_bytes(self, content: bytes, pretty: bool) -> (str, bool):
        try:
            x = etree.fromstring(content)
            return etree.tostring(x, pretty_print=pretty, encoding="utf-8"), True
        except Exception:
            pass

        return None, False
