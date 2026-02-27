import os

supported_extensions_data = {
    ".xlsx": "xl/styles.xml", ".docx": "word/styles.xml", ".pptx": "ppt/tableStyles.xml", ".xlsm": "xl/styles.xml"
}


def file_is_supported(file_path: str) -> bool:
    return any(get_filter(file_path))


def get_default_path(file_path: str) -> str:
    return supported_extensions_data[list(get_filter(file_path))[0]]


def get_filter(file_path: str):
    return filter(lambda extension: extension_filter(file_path, extension), supported_extensions_data.keys())


def extension_filter(file_path: str, extension: str) -> bool:
    return file_path.endswith(extension)


def get_extension(file_path: str) -> str:
    file_path = file_path.split('/')[-1]
    filename, file_extension = os.path.splitext(file_path)
    if filename.startswith('.') and (file_extension is None or file_extension == '') :
        file_extension = filename
    return file_extension
