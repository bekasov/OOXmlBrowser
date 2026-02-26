# -*- mode: python ; coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.getcwd())

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from disttools.collect_gtk import collect_gtk_libs


# gi_typelibs = collect_data_files('gi.repository')
# gi_overrides = collect_data_files('gi.overrides')

gtksourceview_data = [
    ('ui/gtk/resources/hex.lang', 'ui/gtk/resources'),
    ('ui/gtk/resources/hex-theme.xml', 'ui/gtk/resources'),
    ('ui/gtk/resources/solarized-dark.xml', 'ui/gtk/resources'),
    ('ui/gtk/resources/xml.lang', 'ui/gtk/resources'),
]

a = Analysis(
    ['ooxmlbrowser'],
    pathex=[],
    binaries=collect_gtk_libs(),
    datas=gtksourceview_data + gi_typelibs + gi_overrides,
    hiddenimports=[
        'gi', 'gi.repository', 'gi.repository.Gtk', 'gi.repository.GtkSource',
        'lxml', 'lxml.etree', 'cairo', 'gi.repository.Gdk', 'gi.repository.Gio',
        'gi.repository.GdkPixbuf', 'pytidylib', 'gi.repository.Pango',
        'gi.repository.PangoCairo', 'gi.overrides', 'gi.overrides.Gtk',
        'gi.overrides.Gdk', 'gi.overrides.Gio', 'gi.overrides.GtkSource',
        'gi.overrides.Pango', 'gi.overrides.cairo', 'gi.overrides.PangoCairo',
        'gi.repository.GObject', 'gi.overrides.GObject',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='OOXmlBrowser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
