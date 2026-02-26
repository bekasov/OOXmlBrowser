from gi.repository import Gtk, Gio, GLib


class LoadButton(Gtk.Button):
    def __init__(self, parent_window: Gtk.Window, on_files_choose=None, label=None):
        super().__init__(label=label)
        self.parent_window = parent_window
        self.on_files_choose = on_files_choose
        click_gesture = Gtk.GestureClick()
        click_gesture.connect("pressed", self.on_button_clicked)
        self.add_controller(click_gesture)
        # button = Gtk.Button()
        icon = Gtk.Image.new_from_icon_name("document-open-symbolic")
        self.set_child(icon)

    def on_button_clicked(self, widget, e, r, t):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Select OOXML files")
        dialog.set_modal(True)
        # dialog.set_select_multiple(True)
        self.add_filters(dialog)
        dialog.open_multiple(self.parent_window, None, self.on_dialog_complete)

    def on_dialog_complete(self, dialog, result):
        try:
            files = dialog.open_multiple_finish(result)
            if files and self.on_files_choose is not None:
                file_paths = [f.get_path() for f in files]
                self.on_files_choose(file_paths)
        except GLib.Error as e:
            if e.matches(Gtk.DialogError.quark(), Gtk.DialogError.DISMISSED):
                pass
            else:
                print(f"Files choising error")

    def add_filters(self, dialog):
        filters = Gio.ListStore.new(Gtk.FileFilter)

        filter_excel = Gtk.FileFilter()
        filter_excel.set_name("Excel files (*.xlsx)")
        filter_excel.add_pattern("*.xlsx")
        filters.append(filter_excel)

        filter_word = Gtk.FileFilter()
        filter_word.set_name("Word files (*.docx)")
        filter_word.add_pattern("*.docx")
        filters.append(filter_word)

        filter_ppt = Gtk.FileFilter()
        filter_ppt.set_name("PowerPoint files (*.pptx)")
        filter_ppt.add_pattern("*.pptx")
        filters.append(filter_ppt)

        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        filters.append(filter_all)

        dialog.set_filters(filters)
