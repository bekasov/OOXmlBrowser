from gi.repository import Gtk

from model.IXmlFormatter import IXmlFormatter
from model.ISourceViewer import ISourceViewer
from xmlformatter.EtreeXmlFormatter import EtreeXmlFormatter
from xmlformatter.TidyXmlFormatter import TidyXmlFormatter
from service.FileSystemGraphTreeService import FileSystemGraphTreeService
from service.SourceViewDisplay import SourceViewDisplay
from service.Utils import file_is_supported
from service.ZipFileGraphTreeService import ZipFileGraphTreeService
from ui.gtk.TreeViewer import TreeViewer
from ui.gtk.LoadButton import LoadButton
from ui.gtk.GtkSourceViewer import GtkSourceViewer


class BrowserContainer(Gtk.Paned):

    xml_formatter: IXmlFormatter = TidyXmlFormatter()

    def __init__(self, parent: Gtk.Window, file_to_load: str = None):
        super().__init__()

        source_view: ISourceViewer = GtkSourceViewer()

        self.tree_view = TreeViewer(SourceViewDisplay(source_view, self.xml_formatter))

        toolbar: Gtk.HeaderBar = Gtk.HeaderBar()
        toolbar.pack_start(LoadButton(parent, self.load_file, "Load"))

        left_box: Gtk.Box = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)
        left_box.append(toolbar)
        toolbar.set_vexpand(False)
        toolbar.set_hexpand(False)

        scrolled_tree_view = Gtk.ScrolledWindow()
        scrolled_tree_view.set_child(self.tree_view.get_tree_view())

        left_box.append(scrolled_tree_view)
        scrolled_tree_view.set_vexpand(True)
        scrolled_tree_view.set_hexpand(True)

        scrolled_source_view = Gtk.ScrolledWindow()
        scrolled_source_view.set_child(source_view)

        self.set_start_child(left_box)
        self.set_resize_start_child(True)
        self.set_shrink_start_child(True)
        self.set_end_child(scrolled_source_view)
        self.set_resize_end_child(True)
        self.set_shrink_end_child(True)
        self.set_position(200)

        if file_to_load is not None:
            self.load_file([file_to_load])

    def load_file(self, file_path) -> None:
        file_path = file_path[0]
        self.tree_view.populate_file_system_tree_store(
            file_path,
            None,
            ZipFileGraphTreeService() if file_is_supported(file_path) else FileSystemGraphTreeService())
