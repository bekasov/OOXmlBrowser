# -*- mode: python ; coding: utf-8 -*-

import os
import sys

def join_path(root_dir, file):
  return os.path.join(root_dir, file)

current_dir = os.getcwd()

disttools_dir = 'disttools'
disttools_dir_full = join_path(current_dir, disttools_dir)

sys.path.insert(0, disttools_dir_full)

from collect_binaries import collect_libs

project_root = current_dir
resources_dir = 'ui/gtk/resources'
resources_dir_full = join_path(project_root, resources_dir)

gtksourceview_data = [
    (join_path(resources_dir_full, 'hex.lang'), resources_dir),
    (join_path(resources_dir_full, 'hex-theme.xml'), resources_dir),
    (join_path(resources_dir_full, 'solarized-dark.xml'), resources_dir),
    (join_path(resources_dir_full, 'xml.lang'), resources_dir),
]

bin_excludes = [
  join_path('share', 'icons'),
  join_path('share', 'locale'),
  join_path('share', 'themes'),
]

a = Analysis(
    [join_path(project_root, 'ooxmlbrowser')],
    pathex=[],
    binaries=map(lambda p : (p[1], '.'), collect_libs()),
    datas=gtksourceview_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={
      "gi": {
          "themes": ["solarized-dark"],
          "icons": ["default"],
          "languages": ["en_GB"],
          "module-versions": {
              "Gtk": "4.0",
              "Gdk": "4.0",
              "GtkSource": "5"
          }
      },
    },
    runtime_hooks=[join_path(disttools_dir_full, 'runtime_hook.py')],
    excludes= [], # ['gi.repository.Gtk3'],
    noarchive=False,
    optimize=0,
)

# a.datas=[entry for entry in a.datas if not any(entry[0].startswith(exclude) for exclude in bin_excludes)] # entry[0].startswith(bin_excludes[0]))]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OOXmlBrowser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OOXmlBrowser',
)
