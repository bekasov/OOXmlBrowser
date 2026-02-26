import os
import subprocess
import pprint

libs = [
    'libz.so'
]

#libs = [
#    'gtk-4.so',
#    'gtksourceview-5',
#    'gdk_pixbuf-2.0',
#    'pango-1.0',
#    'pangocairo-1.0',
#    'gio-2.0',
#    'gobject-2.0',
#    'glib-2.0',
#    'cairo',
#    'cairo-gobject',
#    'harfbuzz',
#    'fribidi',
#    'atk-1.0',
#    'epoxy',
#    'x11',
#    'xcb',
#    'xcb-render',
#    'xcb-shm',
#    'png16',
#    'z',
#    'bz2',
#    'lzma',
#    'fontconfig',
#    'freetype',
#    'expat',
#    'ffi',
#    'pcre2-8',
#    'mount',
#    'blkid',
#]

exludes = [
    'libwebkit2gtk'
]

def find_library_by_pkg_config(libname):
    try:
        path = subprocess.check_output(['pkg-config', '--libs-only-L', libname], text=True)
        if path:
            libdir = path.strip().replace('-L', '')
            for f in os.listdir(libdir):
                if f.startswith('lib' + libname) and f.endswith('.so'):
                    print("pkg-config found: " + libdir + " / " + f)
                    return os.path.join(libdir, f)
    except:
        pass
    return None

def collect_libs():
    binaries = {}
    not_found = []
    ld_config_output_lines = subprocess.check_output(['ldconfig', '-p'], text=True).splitlines()
    for ld_config_line in ld_config_output_lines :
        ld_config_line_parts = ld_config_line.split(' => ')
        ld_config_line_file = ld_config_line_parts[0].strip()
        ld_config_line_file_path = ld_config_line_parts[-1].strip()
        for lib in libs :
            found_lib = None
            if lib not in binaries and lib in ld_config_line_file :
                found_lib = os.path.realpath(ld_config_line_file_path)
                print("found with ldconfig :: ", (lib, found_lib))
            if found_lib is not None :
                binaries[lib] = found_lib
                
#            path = None
#            if lib in ld_config_line:
#                path = ld_config_line.split(' => ')[-1].strip()
#
#            if path is None:
#                path = find_library_by_pkg_config(lib)
#
#            if path:
#                binaries.append((path, 'lib'))
#            else:
#                print("Not found: " + lib)

    if len(not_found) :
        print(not_found)
    pprint.pprint(binaries)
    return list(binaries.items())

if __name__ == "__main__":
    collect_libs()
