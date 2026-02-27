import os
import glob
import subprocess
import pprint

libs_linux = [
    'libz.so'
]
libs_windows = [
    'libtidy*.dll'
]

def collect_libs_linux():
    result = {}
    ld_config_output_lines = subprocess.check_output(['ldconfig', '-p'], text=True).splitlines()
    for ld_config_line in ld_config_output_lines :
        ld_config_line_parts = ld_config_line.split(' => ')
        ld_config_line_file = ld_config_line_parts[0].strip()
        ld_config_line_file_path = ld_config_line_parts[-1].strip()
        for lib in libs_linux :
            found_lib = None
            if lib not in result and lib in ld_config_line_file :
                found_lib = os.path.realpath(ld_config_line_file_path)
                print("[INFO] Found with ldconfig :: ", (lib, found_lib))
            if found_lib is not None :
                result[lib] = found_lib

    pprint.pprint(result)
    return list(result.items())

def collect_libs_windows():
    result = {}
    search_paths = [
        r'C:\msys64\ucrt64\bin',
        os.environ.get('MSYSTEM_PREFIX', '') + r'\bin',
    ]
    search_paths.extend(os.environ.get('PATH', '').split(os.pathsep))
    for lib in libs_windows :
        found_lib = None
        for base in search_paths:
            if not os.path.exists(base):
                continue
            pattern = os.path.join(base, lib)
            dlls = glob.glob(pattern)
            if dlls:
                found_lib = dlls[0]
                print(f"[INFO] Found with search_paths :: ", (lib, found_lib))
                break
        if found_lib is not None :
            result[lib] = found_lib
        else :
            print("[WARNING] Could not find ", lib)
    pprint.pprint(result)
    return list(result.items())

def join_path(root_dir, file):
  return os.path.join(root_dir, file)


class PyInstallerInfo :
    def __init__(self) :
        self.current_dir = os.getcwd()

        self.disttools_dir = 'disttools'
        self.disttools_dir_full = join_path(self.current_dir, self.disttools_dir)

        self.project_root = self.current_dir
        self.resources_dir = os.path.join('ui', 'gtk', 'resources')
        self.resources_dir_full = join_path(self.project_root, self.resources_dir)

        self.gtksourceview_data = [
            (join_path(self.resources_dir_full, 'hex.lang'), self.resources_dir),
            (join_path(self.resources_dir_full, 'hex-theme.xml'), self.resources_dir),
            (join_path(self.resources_dir_full, 'solarized-dark.xml'), self.resources_dir),
            (join_path(self.resources_dir_full, 'xml.lang'), self.resources_dir),
        ]

    def get_analysis(self, pyinstaller_spec_analysis_func, collect_libs_func, runtime_hook_module) :
        self.a = pyinstaller_spec_analysis_func(
            [join_path(self.project_root, 'ooxmlbrowser')],
            pathex=[],
            binaries=map(lambda p : (p[1], '.'), collect_libs_func()),
            datas=self.gtksourceview_data,
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
            runtime_hooks=[join_path(self.disttools_dir_full, runtime_hook_module)],
            excludes= [],
            noarchive=False,
            optimize=0,
        )
# a.datas=[entry for entry in a.datas if not any(entry[0].startswith(exclude) for exclude in bin_excludes)] # entry[0].startswith(bin_excludes[0]))]
        return self.a

    def get_pyz(self, pyinstaller_spec_pyz_func) :
        self.pyz = pyinstaller_spec_pyz_func(self.a.pure)
        return self.pyz

    def get_exe(self, pyinstaller_spec_exe_func) :
        self.exe = pyinstaller_spec_exe_func(
            self.pyz,
            self.a.scripts,
            [],
            exclude_binaries=True,
            name='OOXmlBrowser',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
            icon=None,
        )
        return self.exe

    def get_collect(self, pyinstaller_spec_collect_func) :
        self.collect = pyinstaller_spec_collect_func(
            self.exe,
            self.a.binaries,
            self.a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='OOXmlBrowser',
        )
        return self.collect

