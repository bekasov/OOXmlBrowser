from model.ISourceViewer import ISourceViewer

from gi.repository import Gtk, GtkSource, Gio, GLib, Gdk


class GtkSourceViewer(GtkSource.View, ISourceViewer):
    __gtype_name__ = "GtkSourceViewer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.set_wrap_mode(Gtk.WrapMode.WORD)

        self.buffers = {}
        self.set_show_line_numbers(True)
        self.set_highlight_current_line(True)
        self.set_monospace(True)
        css_provider: Gtk.CssProvider = Gtk.CssProvider()
        css_provider.load_from_data(text="textview { font-family: Monospace; font-size: 14pt; }")
        Gtk.StyleContext.add_provider(self.get_style_context(), css_provider, 1)
        #self.setup_context_menu()

    def set_text(self, file_name: str, text: str, extension: str) -> None:
        if file_name not in self.buffers:
            self.buffers[file_name] = self._create_buffer()

        self.buffers[file_name].set_text(text if text is not None else "")
        if extension is not None:
            lang_manager = GtkSource.LanguageManager().get_default()
            language: GtkSource.Language = lang_manager.guess_language(extension) # , "text/plain")
            if language is not None :
                self.buffers[file_name].set_language(language)
            else :
                print('language for "' + extension + '" not found')

    def clear(self) -> None:
        self.buffers.clear()
        self.set_text(None, None, None)

    def _create_buffer(self) -> GtkSource.Buffer:
        result: GtkSource.Buffer = self.get_buffer()
        style_manager: GtkSource.StyleSchemeManager = GtkSource.StyleSchemeManager.get_default()
        scheme = style_manager.get_scheme('ooxml-browser-hex-theme')
        if scheme is not None :
            result.set_style_scheme(scheme)
        else :
            print("theme not found")
        return result

    def setup_context_menu(self):
        menu = Gio.Menu()
        menu.append("Copy", "win.copy")
        # menu.append_section(None, Gio.Menu())

        self.popover = Gtk.PopoverMenu.new_from_model(menu)
        self.popover.set_parent(self)
        self.popover.set_has_arrow(False)

        #click_controller = Gtk.GestureClick()
        #click_controller.set_button(3)
        #click_controller.connect("pressed", self.on_right_click)
        #self.add_controller(click_controller)

    def on_right_click(self, gesture, n_press, x, y):
        self.popover.set_pointing_to(Gdk.Rectangle())
        rect = Gdk.Rectangle()
        rect.x = int(x)
        rect.y = int(y)
        rect.width = 1
        rect.height = 1
        self.popover.set_pointing_to(rect)
        self.popover.popup()
