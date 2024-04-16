#!/usr/bin/python
import gi

gi.require_version("Gtk", "3.0")

from GtkTreeViewHelper import GtkTreeViewer
from gi.repository import Gtk

window = Gtk.Window()
window.connect("delete-event", Gtk.main_quit)

tree_view = GtkTreeViewer()
tree_view.populateFileSystemTreeStore("/home/coop/Documents/_xlsx/Excel/excel-default.xlsx")
tree_view.populateFileSystemTreeStore("/home/coop/Documents/")

scrollView = Gtk.ScrolledWindow()
scrollView.add(tree_view.get_tree_view())

# append the scrollView to the window (this)
window.add(scrollView)

window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
