import sys

from gi.repository import Gtk, Gdk
from ui.gtk.BrowserContainer import BrowserContainer
from ui.gtk.LoadButton import LoadButton
from service.Utils import file_is_supported


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Tree")
        self.connect("close-request", self.on_close_request)

        #self.set_border_width(5)
        self.set_default_size(1400, 800)

        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)
#        shortcut_controller = Gtk.ShortcutController()
#        self.add_controller(shortcut_controller)
#        close_action = Gtk.CallbackAction.new(lambda widget, args: self.close())
#        trigger = Gtk.KeyvalTrigger.new(Gdk.KEY_Escape, 0)
#        shortcut = Gtk.Shortcut.new(trigger, close_action)
#        shortcut_controller.add_shortcut(shortcut)

        hb = Gtk.HeaderBar()
        hb.set_title_widget(Gtk.Label(label="OOXML Browser"))
        self.set_titlebar(hb)

        self.content_box: Gtk.Paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)

        hb.pack_start(LoadButton(self, self.on_files_chose, "Add"))

        self.set_child(self.content_box)

        args = sys.argv[1:]
        if len(args):
            self.on_files_chose(args)

    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.close()

    def on_close_request(self, a):
        app = self.get_application()
        if app is not None:
            app.quit()
        return True

    def on_files_chose(self, files):
        files_count = len(files) - 1
        for idx, file in enumerate(files):
            if not file_is_supported(file):
                continue
            browser = BrowserContainer(self, file)
            self.content_box.set_start_child(browser)
            self.content_box.set_resize_start_child(True)
            self.content_box.set_shrink_start_child(True)
            if idx < files_count:
                self.content_box.set_position(200)
            next_pane = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
            next_pane.show()
            self.content_box.set_end_child(next_pane)
            self.content_box.set_resize_end_child(True)
            self.content_box.set_shrink_end_child(True)
            self.content_box = next_pane
            browser.show()


    def run(self):
        self.show()
        self.present()

