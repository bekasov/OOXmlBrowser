import re

from model.IXmlFormatter import IXmlFormatter
import lxml.etree as etree
import logging


class EtreeXmlFormatter(IXmlFormatter):
    def convert_from_bytes(self, content: bytes, pretty: bool) -> (str, bool):
        try:
            x = etree.fromstring(content)
            xml_str = etree.tostring(x, pretty_print=pretty, encoding="utf-8", with_tail=False)
            # return xml_str, True

            pattern = r'(xmlns(?::\w+)?="[^"]*")'

            formatted = re.sub(pattern, r'\1\n', xml_str.decode('utf-8'))
            formatted = re.sub(r'\n\s*(/?>)', r'\1', formatted)

            return formatted.encode('utf-8'), True
        except Exception as e:
            logging.exception("Error parsing xml")

        return None, False
