import subprocess
import sys
import os


def setup_meld():

    meld_dir = os.path.dirname(__file__) + "/meld"

    # Import system hackery to import conf.py.in without copying it to
    # have a .py suffix. This is entirely so that we can run from a git
    # checkout without any user intervention.
    import importlib.machinery
    import importlib.util

    loader = importlib.machinery.SourceFileLoader(
        'meld.conf', os.path.join(meld_dir, 'meld/conf.py.in'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    import meld
    meld.conf = mod
    sys.modules['meld.conf'] = mod

    import meld.conf  # noqa: E402

    # Silence warnings on non-devel releases (minor version is divisible by 2)
    # is_stable = not bool(int(meld.conf.__version__.split('.')[1]) % 2)
    # if is_stable:
    #     import warnings
    #     warnings.simplefilter("ignore")

    meld.conf.uninstalled()
    from gi.repository import Gio, GtkSource

    resource_filename = meld.conf.APPLICATION_ID + ".gresource"
    resource_file = os.path.join(meld.conf.DATADIR, resource_filename)

    if not os.path.exists(resource_file):
        subprocess.call(
            [
                "glib-compile-resources",
                "--target={}".format(resource_file),
                "--sourcedir=meld/resources",
                "--sourcedir=data/icons/hicolor",
                "meld/resources/meld.gresource.xml",
            ],
            cwd=meld_dir
        )

    try:
        resources = Gio.resource_load(resource_file)
        Gio.resources_register(resources)
    except Exception:
        # Allow resources to be missing when running uninstalled
        pass

    style_path = os.path.join(meld.conf.DATADIR, "styles")
    GtkSource.StyleSchemeManager.get_default().append_search_path(style_path)

    # Just copy style schemes to the file ending expected by
    # GtkSourceView if we're uninstalled and they're missing
    for style in {'meld-base', 'meld-dark'}:
        path = os.path.join(
            style_path, '{}.style-scheme.xml'.format(style))
        if not os.path.exists(path):
            import shutil
            shutil.copyfile(path + '.in', path)

    schema_path = os.path.join(meld.conf.DATADIR, "org.gnome.meld.gschema.xml")
    compiled_schema_path = os.path.join(meld.conf.DATADIR, "gschemas.compiled")

    try:
        schema_mtime = os.path.getmtime(schema_path)
        compiled_mtime = os.path.getmtime(compiled_schema_path)
        have_schema = schema_mtime < compiled_mtime
    except OSError:
        have_schema = False

    if not have_schema:
        subprocess.call(["glib-compile-schemas", meld.conf.DATADIR], cwd=meld_dir)

    import meld.settings
    meld.settings.create_settings()



def load_third_party_libs():
    current_dir_path = os.path.dirname(__file__)
    libs = list(filter(lambda file: not file.startswith("__"), os.listdir(current_dir_path)))
    third_party_folder_name: str = current_dir_path.split("/")[-1]
    sys.path += list(map(lambda lib: third_party_folder_name + "/" + lib, libs))
    setup_meld()
