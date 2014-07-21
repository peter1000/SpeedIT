""" ReadmeExampleBenchmarkIT
"""
from inspect import (
   currentframe,
   getfile
)
from os.path import (
   abspath,
   dirname,
   join
)
from sys import path as syspath


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'SpeedIT'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)

from SpeedIT.BenchmarkIT import speedit_benchmark


# get a list of text lines to iterate over and split by double colon
source_list1 = [
   '1 Double :: is the ultimate tool for telecommuting.',
   '    _menu',
   '        _id :: file',
   '        # CommentLine starts with # and can be included',
   '        _value :: File',
   '        _popup',
   '            _menuitem',
   '                _value1 :: New',
   '                _onclick1 CreateNewDoc()',
   '                _value2 :: Open',
   '                _onclick2 :: OpenDoc()',
   '                _value3 :: Close',
   '                _onclick3 :: CloseDoc()',
   '    # CommentLine starts with # and can be included',
   '    _Help :: About',
   '    Old Version'
   '     test is not ok'
   '     https://github.com/peter1000',
]


# define some functions to compare different approaches
def split_catch_error():
   for str_ in source_list1:
      try:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)
      except ValueError:
         pass


def split_check_first_notfound():
   for str_ in source_list1:
      if '::' in str_:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining the: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'split_catch_error': (split_catch_error, [], {}),
      'split_check_first_notfound': (split_check_first_notfound, [], {}),
   }

   # defining any: setup_line_list
   setup_line_list = [
      'from __main__ import source_list1',
   ]

   with open('result_output/ReadmeExampleBenchmarkIT.txt', 'w') as file_:
      file_.write('\n\n ReadmeExampleBenchmarkIT.py output\n\n')
      file_.write(speedit_benchmark(func_dict, setup_line_list, use_func_name=True, output_in_sec=False, with_gc=False, rank_by='average', run_sec=1, repeat=2))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
