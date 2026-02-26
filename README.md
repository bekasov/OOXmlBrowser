# OOXML Browser

[![Build Linux](https://github.com/bekasov/OOXmlBrowser/actions/workflows/build-linux.yml/badge.svg)](https://github.com/bekasov/OOXmlBrowser/actions/workflows/build-linux.yml)
[![Build Windows](https://github.com/bekasov/OOXmlBrowser/actions/workflows/build-windows.yml/badge.svg)](https://github.com/bekasov/OOXmlBrowser/actions/workflows/build-windows.yml)
[![Hits-of-Code](https://hitsofcode.com/github/bekasov/OOXmlBrowser?branch=master&exclude=)](https://hitsofcode.com/github/bekasov/OOXmlBrowser/view?branch=master&exclude=)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**OOXML Browser** is a visual tool for developers that allows you to explore the internal structure of Office Open XML files (DOCX, XLSX, PPTX). It is built with **GTK4** and **GtkSourceView5**, provides XML syntax highlighting, pretty‑printing, and a hex viewer for binary files with customizable color schemes.

## Features

- Browse the internal file tree of OOXML packages
- Syntax‑highlighted XML viewing with GtkSourceView
- Automatic XML formatting with namespace line‑breaking (via `tidylib` or `lxml`)
- Support for opening multiple files
- Hex dump viewer for non‑XML files with colored address, byte and ASCII regions
- Custom color scheme (extends `solarized-dark` with hex‑specific colors)
- Global Esc key to close the window

## Requirements

### System Dependencies (Linux)

To run from source, you need the following packages installed:

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install libgtk-4-dev libgtksourceview-5-dev libgirepository-2.0-dev \
                 gobject-introspection libcairo2-dev python3-dev \
                 gir1.2-gtk-4.0 gir1.2-gtksource-5 gir1.2-glib-2.0 tidy
```

**Fedora**
```bash
sudo dnf install gtk4-devel gtksourceview5-devel gobject-introspection-devel \
                 cairo-devel python3-devel libtidy
```

**Arch**
```bash
sudo pacman -S gtk4 gtksourceview5 gobject-introspection cairo python tidy
```

### System Dependencies (Windows)
For running from source on Windows, you need to set up MSYS2 with UCRT64 environment and install the required packages:
```bash
pacman -Syu
pacman -S mingw-w64-ucrt-x86_64-gtk4 mingw-w64-ucrt-x86_64-gtksourceview5 \
          mingw-w64-ucrt-x86_64-python-lxml mingw-w64-ucrt-x86_64-python-gobject \
          mingw-w64-ucrt-x86_64-cairo mingw-w64-ucrt-x86_64-python-pip \
          mingw-w64-ucrt-x86_64-tidy mingw-w64-ucrt-x86_64-gobject-introspection
```

### Python Dependencies
- Python 3.8 or newer
- GTK 4
- GtkSourceView 5
- PyGObject
- Pycairo
- Pytidylib
- Lxml (optional)

It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running from Source
```bash
./ooxmlbrowser [file1] [file2] ...
```


