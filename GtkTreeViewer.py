import zipfile

from gi.repository import Gtk

from FileSystemGrafTreeService import FileSystemGrafTreeService
from IDisplayService import IDisplayService
from IGraphTreeService import IGraphTreeService
from gi.repository.GdkPixbuf import Pixbuf

from ZipFileGraphTreeService import ZipFileGraphTreeService


class GtkTreeViewer(Gtk.TreeView):
    tree_service: IGraphTreeService
    tree_store: Gtk.TreeStore
    tree_view: Gtk.TreeView
    file_path: str
    text_displayer: IDisplayService

    def __init__(self, display: IDisplayService):
        self.text_displayer = display
        self.tree_store = Gtk.TreeStore(str, Pixbuf, str, object)
        self.tree_view = Gtk.TreeView(self.tree_store)

        file_column_text = Gtk.CellRendererText()
        file_column_image = Gtk.CellRendererPixbuf()
        file_column = Gtk.TreeViewColumn("File")
        file_column.pack_start(file_column_image, False)
        file_column.pack_start(file_column_text, True)
        file_column.add_attribute(file_column_text, "text", 0)
        file_column.add_attribute(file_column_image, "pixbuf", 1)
        self.tree_view.append_column(file_column)
        self.tree_view.connect("row-expanded", self.on_row_expanded)
        self.tree_view.connect("row-collapsed", self.on_row_collapsed)
        select = self.tree_view.get_selection()
        select.connect("changed", self.on_selection_changed)

    def on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            selected_item = model[treeiter][3]
            if self.tree_service.IsItemFolder(selected_item):
                return

            print("You selected", selected_item.get_full_path())
            self.text_displayer.display(self.tree_service.GetItemContent(selected_item))

    def get_tree_view(self) -> Gtk.TreeView:
        return self.tree_view

    def populateFileSystemTreeStore(self, path: str, parent=None, init=True):

        if init:
            self.file_path = path
            self.tree_service = ZipFileGraphTreeService() if path.endswith(".xlsx") else FileSystemGrafTreeService()
            self.tree_store.clear()
            self.text_displayer.clear()

        item_counter = 0

        # iterate over the items in the path
        for item in self.tree_service.ListItems(path):
            item_is_folder = self.tree_service.IsItemFolder(item)
            item_icon = Gtk.IconTheme.get_default().load_icon("folder" if item_is_folder else "text-html", 22, 0)
            current_iter = self.tree_store.append(parent, [self.tree_service.GetShortItemName(item), item_icon, self.tree_service.GetFullItemName(item), item])
            # add dummy if current item was a folder
            if item_is_folder:
                self.tree_store.append(current_iter, [None, None, None, None])
            item_counter += 1
        # add the dummy node back if nothing was inserted before
        if item_counter < 1:
            self.tree_store.append(parent, [None, None, None, None])

    def on_row_expanded(self, tree_view, tree_iter, tree_path):
        # treeStore = treeView.get_model()
        new_path = self.tree_store.get_value(tree_iter, 2)
        self.populateFileSystemTreeStore(new_path, tree_iter, False)
        self.tree_store.remove(self.tree_store.iter_children(tree_iter))

    def on_row_collapsed(self, tree_view, tree_iter, tree_path):
        current_child_iter = self.tree_store.iter_children(tree_iter)
        while current_child_iter:
            # remove the first child
            self.tree_store.remove(current_child_iter)
            # refresh the iterator of the next child
            current_child_iter = self.tree_store.iter_children(tree_iter)
        # append dummy node
        self.tree_store.append(tree_iter, [None, None, None, None])
