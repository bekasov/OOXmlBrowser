from gi.repository import Gtk, GtkSource
# from meld.sourceview import MeldSourceView
from meld.filediff import FileDiff


class SourceView:
    __gtype_name__ = "SourceView"

    def __init__(self, *args, **kwargs):
        builder: Gtk.Builder = Gtk.Builder()
        builder.extend_with_template()
        builder.
        self.view = FileDiff(num_panes=2)
        # super().__init__(*args, **kwargs)

        # self.text_buffer: GtkSource.Buffer = self.get_buffer()
        # manager: GtkSource.StyleSchemeManager = GtkSource.StyleSchemeManager.get_default()
        # re= manager.get_scheme_ids()

        # scheme = manager.get_scheme("solarized-dark")
        # self.text_buffer.set_style_scheme(scheme)
        # nn = Gtk.IconTheme.get_default().list_icons()
        # self.set_show_line_numbers(True)
        # self.set_monospace(True)
        # css_provider: Gtk.CssProvider = Gtk.CssProvider()
        # css_provider.load_from_data(text="textview { font-family: Monospace; font-size: 14pt; }")
        # Gtk.StyleContext.add_provider(self.get_style_context(), css_provider, 1)
        # self.set_highlight_current_line(True)

    def set_text(self, text: str, extension: str) -> None:
        # manager = GtkSource.LanguageManager()
        # language: GtkSource.Language = manager.guess_language(extension if extension is not None else ".txt", "text/plain")
        # if language is not None:
        #     self.text_buffer.set_language(language)
        # self.text_buffer.set_text(text if text is not None else "")
        self.view.get_buffer().set_text(text if text is not None else "")

    def get_view(self):
        return self.view
