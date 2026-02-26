# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--for_windows", action="store_true")
options = parser.parse_args()
for_windows = options.for_windows

sys.path.insert(0, os.path.dirname(SPEC))

import ooxmlbrowsercommonspec

installer = ooxmlbrowsercommonspec.PyInstallerInfo()
binary_libs_collector = ooxmlbrowsercommonspec.collect_libs_linux if not for_windows else ooxmlbrowsercommonspec.collect_libs_windows
runtime_hook_module = 'runtime_hook.py' if not for_windows else 'runtime_hook_windows.py'
a = installer.get_analysis(Analysis, binary_libs_collector, runtime_hook_module)
pyz = installer.get_pyz(PYZ)
exe = installer.get_exe(EXE)
coll = installer.get_collect(COLLECT)

