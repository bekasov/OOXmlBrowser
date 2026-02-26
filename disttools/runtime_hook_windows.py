import os
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    dll_path = os.path.join(base_path, 'lib')
    if os.path.exists(dll_path):
        os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

typelib_paths = [
    os.path.join(base_path, 'girepository-1.0'),
    os.path.join(base_path, 'lib', 'girepository-1.0')
]
existing = [p for p in typelib_paths if os.path.exists(p)]
if existing:
    os.environ['GI_TYPELIB_PATH'] = os.pathsep.join(existing)
