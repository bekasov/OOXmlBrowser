from pathlib import Path
import gi
gi.require_version("GtkSource", "5")
from gi.repository import GtkSource

def setup_hexdump_language():
    style_manager = GtkSource.StyleSchemeManager.get_default()
    styles_current_paths = style_manager.get_search_path() or []
    data_dir = Path(__file__).parent / 'resources'
    data_path = str(data_dir)
    if not data_dir.exists():
        print ('Resources folder with addtional highlighting was not found ' + data_path)
        return
    if data_dir not in styles_current_paths:
        style_manager.set_search_path(styles_current_paths + [data_path])

    lang_manager = GtkSource.LanguageManager.get_default()
    current_paths = lang_manager.get_search_path() or []

    if data_path not in current_paths:
        lang_manager.set_search_path(current_paths + [data_path])

setup_hexdump_language()

#style_manager = GtkSource.StyleSchemeManager.get_default()
#print(style_manager.get_scheme_ids())
#scheme = style_manager.get_scheme('ooxml-browser-hex-theme')
#if scheme:
#    print("ooxml-browser-hex-theme available")
#else:
#    print("fail to load theme")
#
#lang = GtkSource.LanguageManager.get_default().get_language('hex')
#print(lang.get_name() if lang else 'Not found')
