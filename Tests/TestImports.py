""" tests all modules for syntax correctness and internal imports
"""
from glob import glob
from importlib import import_module
from inspect import (
   getfile,
   currentframe
)
from os import walk
from os.path import (
   abspath,
   dirname,
   join,
   split
)
from sys import path as syspath


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'SpeedIT'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


def test_all_imports():
   """ Tests: all modules for syntax correctness and internal imports
   """
   print('::: TEST: test_all_imports()')
   chars_to_cut = len(PROJECT_ROOT) + 1
   full_modules_path = []
   for root, dirnames, filenames in walk(ROOT_PACKAGE_PATH):
      full_modules_path.extend(glob(root + '/*.py'))
   for full_path in full_modules_path:
      packagepath, modulepath = split(full_path)
      package = packagepath[chars_to_cut:].replace('/', '.')
      if '__' not in package:   # skip packages with '__' e.g. __pycache__
         module_full_name = '{}.{}'.format(package, modulepath[:-3])
         import_module(module_full_name)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   test_all_imports()
