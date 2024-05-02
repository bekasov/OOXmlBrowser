import os

from gi.repository import Gtk

from IDisplayService import IDisplayService
from IGraphTreeService import IGraphTreeService
from gi.repository.GdkPixbuf import Pixbuf

from Utils import get_default_path


class GtkTreeViewer:
    tree_service: IGraphTreeService
    tree_store: Gtk.TreeStore
    tree_view: Gtk.TreeView
    file_path: str
    path_to_show: str
    text_displayer: IDisplayService

    def __init__(self, display: IDisplayService):
        self.text_displayer = display
        self.tree_store = Gtk.TreeStore(str, Pixbuf, str, object)
        self.tree_view = Gtk.TreeView(self.tree_store)

        file_column_text = Gtk.CellRendererText()
        file_column_image = Gtk.CellRendererPixbuf()
        self.file_column = Gtk.TreeViewColumn("File")
        self.file_column.pack_start(file_column_image, False)
        self.file_column.pack_start(file_column_text, True)
        self.file_column.add_attribute(file_column_text, "text", 0)
        self.file_column.add_attribute(file_column_image, "pixbuf", 1)
        self.tree_view.append_column(self.file_column)
        self.tree_view.connect("row-expanded", self.on_row_expanded)
        self.tree_view.connect("row-collapsed", self.on_row_collapsed)
        selection: Gtk.TreeSelection = self.tree_view.get_selection()
        selection.connect("changed", self.on_selection_changed)

    def on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            selected_item = model[treeiter][3]
            if self.tree_service.is_item_folder(selected_item):
                return

            self.text_displayer.display(self.tree_service.get_item_content(selected_item))

    def get_tree_view(self) -> Gtk.TreeView:
        return self.tree_view

    def populate_file_system_tree_store(self, path: str, parent=None, tree_service: IGraphTreeService = None):

        if tree_service:
            self.file_path = path
            self.tree_service = tree_service
            self.tree_store.clear()
            self.text_displayer.clear()
            self.path_to_show = get_default_path(path)
            self.file_column.set_title(os.path.split(path)[1])

        item_counter = 0

        # iterate over the items in the path
        for item in self.tree_service.list_items(path):
            item_is_folder = self.tree_service.is_item_folder(item)
            item_icon = Gtk.IconTheme.get_default().load_icon("folder" if item_is_folder else "text-html", 22, 0)
            full_name = self.tree_service.get_full_item_name(item)

            current_iter = self.tree_store.append(parent, [
                self.tree_service.get_short_item_name(item), item_icon, full_name, item
            ])

            if self.path_to_show and full_name == self.path_to_show:
                path: Gtk.TreePath = self.tree_store.get_path(current_iter)
                self.tree_view.get_selection().select_path(path)
                self.path_to_show = None

            # add dummy if current item was a folder
            if item_is_folder:
                self.tree_store.append(current_iter, [None, None, None, None])
            item_counter += 1
        # add the dummy node back if nothing was inserted before
        if item_counter < 1:
            self.tree_store.append(parent, [None, None, None, None])

        if tree_service:
            self.tree_view.expand_all()

    def on_row_expanded(self, tree_view, tree_iter, tree_path):
        # treeStore = treeView.get_model()
        new_path = self.tree_store.get_value(tree_iter, 2)
        self.populate_file_system_tree_store(new_path, tree_iter)
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
