
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gio, Gdk
from ui.gtk.MainWindow import MainWindow

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id='com.github.bekasov.ooxmlbrowser',
            flags=Gio.ApplicationFlags.HANDLES_OPEN
        )

        #copy_action = Gio.SimpleAction.new("copy", None)
        #copy_action.connect("activate", self.on_copy)
        #self.add_action(copy_action)

#    def on_copy(self, action, param):
#        view = self.get_current_source_view()
#        if view:
#            view.get_buffer().copy_clipboard(Gdk.Display.get_default().get_clipboard())

#    def get_current_source_view(self):
#        win = self.get_active_window()
#        if win and hasattr(win, 'get_current_source_view'):
#            return win.get_current_source_view()
#        return None

    def do_activate(self):
        win = MainWindow()
        win.set_application(self)
        win.present()

    def do_open(self, files, n_files, hint):
        self.do_activate()
        window = self.get_active_window()
        if window:
            file_paths = [f.get_path() for f in files]
            window.on_files_chose(file_paths)
