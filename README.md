
About OOXML Browser
==========

OOXML Browser is a visual tool targeted at developers. It helps you
browse content of an OOXML-standard based office files.

OOXML Browser is licensed under the Expat licence.


Requirements
------------

* Python 3.6
* pycairo (Python3 bindings for cairo without GObject layer)
* PyGObject 3.30 (Python3 bindings for GObject introspection)
* gsettings-desktop-schemas

And following packages with GObject introspection:

* GLib 2.36
* Pango
* PangoCairo
* GTK+ 3.20
* GtkSourceView 4.0

Running
-------

```sh
$ ./ooxmlbrowser [ooxmlfile-1] .. [ooxmlfile-n] 
```

Prepare to run with MSYS2
-------------------------

```sh
pacman -S mingw-w64-ucrt-x86_64-gtk3
pacman -S mingw-w64-ucrt-x86_64-python-lxml
pacman -S mingw-w64-ucrt-x86_64-gtksourceview4
pacman -S mingw-w64-ucrt-x86_64-python3-gobject
```

Prepare to build with MSYS2
-------------------------

```sh
pacman -S mingw-w64-ucrt-x86_64-python-cx-freeze
```

To build with MSYS2, run
```sh
python3 setup_win32.py bdist
```
