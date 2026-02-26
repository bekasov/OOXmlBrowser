import logging

from model.IXmlFormatter import IXmlFormatter
from tidylib import tidy_document


class TidyXmlFormatter(IXmlFormatter):
    def convert_from_bytes(self, content: bytes, pretty: bool) -> (str, bool):
        options = {
            'input-xml': 1,
            'indent': 1,
            'indent-attributes': 1,
            'indent-spaces': 2,
            'wrap': 0,
            'output-xml': 1,
            'add-xml-decl': 0,
            'tidy-mark': 0,
            'quiet': 1,
        }
        try:
            formatted, errors = tidy_document(content.decode('utf-8'), options=options)
            return formatted.encode('utf-8'), errors
        except Exception as e:
            logging.exception("Error parsing xml")

        return None, False
