from gi.repository import Gtk


class LoadButton(Gtk.Button):
    def __init__(self, parent_window: Gtk.Window, on_files_choose=None, on_file_choose=None, label=None):
        super().__init__(label=("Load" if on_files_choose is None else "Add") if label is None else label)
        self.parent_window = parent_window
        self.on_file_choose = on_file_choose
        self.on_files_choose = on_files_choose
        self.connect("clicked", self.on_button_clicked)

    def on_button_clicked(self, widget):
        dialog:Gtk.FileChooserDialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self.parent_window, action=Gtk.FileChooserAction.OPEN)
        dialog.set_select_multiple(self.on_files_choose is not None)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            if self.on_file_choose is not None:
                self.on_file_choose(dialog.get_filename())
            if self.on_files_choose is not None:
                self.on_files_choose(dialog.get_filenames())

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Excel files")
        filter_text.add_pattern("*.xlsx")
        dialog.add_filter(filter_text)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Word files")
        filter_text.add_pattern("*.docx")
        dialog.add_filter(filter_text)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Power Point files")
        filter_text.add_pattern("*.pptx")
        dialog.add_filter(filter_text)
