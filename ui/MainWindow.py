import sys

from gi.repository import Gtk
from ui.BrowserContainer import BrowserContainer
from ui.LoadButton import LoadButton
from service.Utils import file_is_supported


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="OOXML Browser")
        self.connect("destroy", Gtk.main_quit)

        self.set_border_width(5)
        self.set_default_size(800, 600)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "OOXML Browser"
        self.set_titlebar(hb)

        self.content_box: Gtk.Paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)

        hb.pack_start(LoadButton(self, on_files_choose=self.on_files_chose))

        self.add(self.content_box)

        args = sys.argv[1:]
        if len(args):
            self.on_files_chose(args)

    def on_files_chose(self, files):
        files_count = len(files) - 1
        for idx, file in enumerate(files):
            if not file_is_supported(file):
                continue
            browser = BrowserContainer(self, file)
            self.content_box.pack1(browser, True, True)
            if idx < files_count:
                self.content_box.set_position(200)
            next_pane = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
            next_pane.show()
            self.content_box.pack2(next_pane, True, True)
            self.content_box = next_pane
            browser.show_all()



