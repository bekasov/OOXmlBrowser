import gi

from model.ISourceViewer import ISourceViewer

gi.require_version("GtkSource", "4")
from gi.repository import Gtk, GtkSource


class SourceView(GtkSource.View, ISourceViewer):
    __gtype_name__ = "SourceView"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_buffer: GtkSource.Buffer = self.get_buffer()
        style_manager: GtkSource.StyleSchemeManager = GtkSource.StyleSchemeManager.get_default()

        scheme = style_manager.get_scheme("solarized-dark")
        self.text_buffer.set_style_scheme(scheme)
        # nn = Gtk.IconTheme.get_default().list_icons()
        self.set_show_line_numbers(True)
        self.set_monospace(True)
        css_provider: Gtk.CssProvider = Gtk.CssProvider()
        css_provider.load_from_data(text="textview { font-family: Monospace; font-size: 14pt; }")
        Gtk.StyleContext.add_provider(self.get_style_context(), css_provider, 1)
        self.set_highlight_current_line(True)

        lang_manager = GtkSource.LanguageManager()
        language: GtkSource.Language = lang_manager.guess_language(".xml", "text/plain")
        self.text_buffer.set_language(language)

    def set_text(self, text: str, extension: str) -> None:
        self.text_buffer.set_text(text if text is not None else "")
