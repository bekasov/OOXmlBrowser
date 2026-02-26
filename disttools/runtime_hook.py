import os
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

gtk_path = os.path.join(base_path, 'lib')
girepo_path = os.path.join(base_path, 'lib/girepository-1.0')
data_path = os.path.join(base_path, 'share')

os.environ['GI_TYPELIB_PATH'] = girepo_path + ':' + os.environ.get('GI_TYPELIB_PATH', '')
os.environ['LD_LIBRARY_PATH'] = gtk_path + ':' + os.environ.get('LD_LIBRARY_PATH', '')
os.environ['GSETTINGS_SCHEMA_DIR'] = os.path.join(data_path, 'glib-2.0/schemas')
os.environ['GTK_EXE_PREFIX'] = base_path
os.environ['GTK_DATA_PREFIX'] = base_path
os.environ['GTK_PATH'] = base_path

os.environ['GDK_PIXBUF_MODULE_FILE'] = os.path.join(data_path, 'loaders.cache')
