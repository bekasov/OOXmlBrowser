from gi.repository import Gtk

from service.FileSystemGraphTreeService import FileSystemGraphTreeService
from model.ISourceViewer import ISourceViewer
from ui.gtk3.GtkTreeViewer import GtkTreeViewer
from ui.LoadButton import LoadButton
from ui.gtk3.SourceView import SourceView
from service.SourceViewDisplay import SourceViewDisplay
from service.Utils import file_is_supported
from service.ZipFileGraphTreeService import ZipFileGraphTreeService


class BrowserContainer(Gtk.Paned):
    def __init__(self, parent: Gtk.Window, load_file: str = None):
        super().__init__()

        source_view: ISourceViewer = SourceView()

        self.tree_view = GtkTreeViewer(SourceViewDisplay(source_view))

        toolbar: Gtk.HeaderBar = Gtk.HeaderBar()
        toolbar.set_show_close_button(False)
        toolbar.pack_start(LoadButton(parent, on_file_choose=self.load_file))

        left_box: Gtk.Box = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)
        left_box.pack_start(toolbar, False, True, 0)

        scrolled_tree_view = Gtk.ScrolledWindow()
        scrolled_tree_view.add(self.tree_view.get_tree_view())

        left_box.pack_start(scrolled_tree_view, True, True, 0)

        scrolled_source_view = Gtk.ScrolledWindow()
        scrolled_source_view.add(source_view)

        self.pack1(left_box, True, True)
        self.pack2(scrolled_source_view, True, True)
        self.set_position(200)

        if load_file is not None:
            self.load_file(load_file)

    def load_file(self, file_path: str) -> None:
        self.tree_view.populate_file_system_tree_store(
            file_path,
            None,
            ZipFileGraphTreeService() if file_is_supported(file_path) else FileSystemGraphTreeService())
