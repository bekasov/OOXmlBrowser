#!/usr/bin/env python3

import glob
import os.path
import pathlib
import platform
import sys
import sysconfig

from cx_Freeze import Executable, setup


def get_non_python_libs():
    local_bin = os.path.join(sys.prefix, "bin")

    inst_root = []  # local paths of files "to put at freezed root"
    inst_lib = []  # local paths of files "to put at freezed 'lib' subdir"

    if 'mingw' in sysconfig.get_platform():
        # dll imported by dll dependencies expected to be auto-resolved later
        inst_root = [os.path.join(local_bin, 'libgtksourceview-4-0.dll')]

        # required for communicating multiple instances
        inst_lib.append(os.path.join(local_bin, 'gdbus.exe'))

        # gspawn-helper is needed for Gtk.show_uri function
        if platform.architecture()[0] == '32bit':
            inst_lib.append(os.path.join(local_bin, 'gspawn-win32-helper.exe'))
        else:
            inst_lib.append(os.path.join(local_bin, 'gspawn-win64-helper.exe'))

    return [
        (f, os.path.basename(f)) for f in inst_root # path to the lib in dev-env
    ] + [
        (f, os.path.join('lib', os.path.basename(f))) for f in inst_lib # path to run installed app
    ]


gtk_data_dirs = [
    'etc/fonts',
    'etc/gtk-3.0',
    'lib/gdk-pixbuf-2.0',
    'lib/girepository-1.0',
    'share/fontconfig',
    'share/glib-2.0',
    'share/gtksourceview-4',
    #'share/icons',
]

gtk_data_files = []
for data_dir in gtk_data_dirs:
    local_data_dir = os.path.join(sys.prefix, data_dir)

    for local_data_subdir, dirs, files in os.walk(local_data_dir):
        data_subdir = os.path.relpath(local_data_subdir, local_data_dir)
        gtk_data_files.append((
            os.path.join(data_dir, data_subdir),
            [os.path.join(local_data_subdir, file) for file in files],
        ))

manually_added_libs = {
    # add libgdk_pixbuf-2.0-0.dll manually to forbid auto-pulling of gdiplus.dll
    "libgdk_pixbuf-2.0-0.dll": os.path.join(sys.prefix, 'bin'),
    # librsvg is needed for SVG loading in gdkpixbuf
    "librsvg-2-2.dll": os.path.join(sys.prefix, 'bin'),
    "libxml2-2.dll": os.path.join(sys.prefix, 'bin'),
}

for lib, possible_path in manually_added_libs.items():
    local_lib = os.path.join(possible_path, lib)
    if os.path.isfile(local_lib):
        gtk_data_files.append((os.path.dirname(lib), [local_lib]))

build_exe_options = {
    "includes": ["gi", "lxml", "lxml.etree"],
    "excludes": ["tkinter"],
    "packages": ["gi", "weakref", "lxml", "lxml.etree"],
    "include_files": get_non_python_libs(),
    "bin_excludes": list(manually_added_libs.keys()),
    "zip_exclude_packages": [],
    "zip_include_packages": ["*"],
}

# Create our registry key, and fill with install directory and exe
registry_table = [
    ('OOXMLBrowserKLM', 2, r'SOFTWARE\OOXMLBrowser', '*', None, 'TARGETDIR'),
    ('OOXMLBrowserInstallDir', 2, r'SOFTWARE\OOXMLBrowser', 'InstallDir', '[TARGETDIR]', 'TARGETDIR'),
    ('OOXMLBrowserExecutable', 2, r'SOFTWARE\OOXMLBrowser', 'Executable', '[TARGETDIR]ooxmlbrowser.exe', 'TARGETDIR'),
]

# Provide the locator and app search to give MSI the existing install directory
# for future upgrades
reg_locator_table = [
    # ('OOXMLBrowserInstallDirLocate', 2, r'SOFTWARE\OOXMLBrowser', 'InstallDir', 0),
]
app_search_table = [
    # ('TARGETDIR', 'OOXMLBrowserInstallDirLocate')
]

msi_data = {
    'Registry': registry_table,
    'RegLocator': reg_locator_table,
    'AppSearch': app_search_table,
}

bdist_msi_options = {
    "upgrade_code": "{1d303789-b4e2-4d6e-9515-c301e155cd50}",
    "data": msi_data,
    "all_users": True,
    "add_to_path": True,
    # "install_icon": "data/icons/org.gnome.ooxmlbrowser.ico",
}

executable_options = {
    "script": "ooxmlbrowser",
    # "icon": "data/icons/org.gnome.ooxmlbrowser.ico",
}
console_executable_options = dict(executable_options)

if 'mingw' in sysconfig.get_platform():
    executable_options.update({
        "base": "Win32GUI",  # comment to build console version to see stderr
        "target_name": "ooxmlbrowser.exe",
        "shortcut_name": "ooxmlbrowser",
        "shortcut_dir": "ProgramMenuFolder",
    })
    console_executable_options.update({
        "target_name": "ooxmlbrowser-cmd.exe",
    })

setup(
    name="ooxmlbrowser",
    version="1.0.0",
    description='Office file intermal xml browser',
    author='Bekasov Gennady',
    author_email='bekasov.g@gmail.com',
    maintainer='Bekasov Gennady',
    url='https://github.com/bekasov/OOXmlBrowser',
    license='MIT',
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
        #  cx_freeze + bdist_dumb fails on non-empty prefix
        "install": {"prefix": "."},
        #  freezed binary doesn't use source files, they are only for humans
        "install_lib": {"compile": False},
    },
    executables=[
        Executable(**executable_options),
        Executable(**console_executable_options),
    ],
    packages=[],
    package_data={},
    scripts=['ooxmlbrowser'],
    data_files=gtk_data_files
)
