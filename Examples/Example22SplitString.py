""" Example22SplitString
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

from SpeedIT.BenchmarkIT import speedit_func_benchmark_list
from SpeedIT.MainCode import speed_it

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

source_list2 = [
   '1 Double is the ultimate tool for telecommuting.',
   '    _menu    no',
   '        _id    file',
   '        # CommentLine      starts with # and can be included',
   '        _value    File',
   '        _popup     yes',
   '            _menuitem      something',
   '                _value1    New',
   '                _onclick1    CreateNewDoc()',
   '                _value2    Open',
   '                _onclick2    OpenDoc()',
   '                _value3    Close',
   '                _onclick3    CloseDoc()',
   '    # CommentLine      starts with # and can be included',
   '    _Help    About',
   '    Old Version    yes'
   '     test is     not ok'
   '     web      https://github.com/peter1000',
]

source_list3 = [
   '1 Double :: is the ultimate tool for telecommuting.',
   '    _menu :: no',
   '        _id :: file',
   '        # CommentLine  ::  starts with # and can be included',
   '        _value :: File',
   '        _popup  :: yes',
   '            _menuitem  ::  something',
   '                _value1 :: New',
   '                _onclick1 :: CreateNewDoc()',
   '                _value2 :: Open',
   '                _onclick2 :: OpenDoc()',
   '                _value3 :: Close',
   '                _onclick3 :: CloseDoc()',
   '    # CommentLine  ::  starts with # and can be included',
   '    _Help :: About',
   '    Old Version :: yes'
   '     test is ::  not ok'
   '     web  ::  https://github.com/peter1000',
]


def split_catch_error_half_match():
   for str_ in source_list1:
      try:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)
      except ValueError:
         pass


def split_check_first_notfound_half_match():
   for str_ in source_list1:
      if '::' in str_:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)


def split_catch_error_no_match():
   for str_ in source_list2:
      try:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)
      except ValueError:
         pass


def split_check_first_notfound_no_match():
   for str_ in source_list2:
      if '::' in str_:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)


def split_catch_error_all_match():
   for str_ in source_list3:
      try:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)
      except ValueError:
         pass


def split_check_first_notfound_all_match():
   for str_ in source_list3:
      if '::' in str_:
         name, txt = str_.split('::', 1)
         # print('name: ', name, ' txt: ', txt)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'split_catch_error_half_match': (split_catch_error_half_match, [], {}),
      'split_check_first_notfound_half_match': (split_check_first_notfound_half_match, [], {}),
      'split_catch_error_no_match': (split_catch_error_no_match, [], {}),
      'split_check_first_notfound_no_match': (split_check_first_notfound_no_match, [], {}),
      'split_catch_error_all_match': (split_catch_error_all_match, [], {}),
      'split_check_first_notfound_all_match': (split_check_first_notfound_all_match, [], {}),
   }

   setup_line_list = [
      'from __main__ import source_list1, source_list2, source_list3',
   ]

   check_run_sec = 1
   with open('result_output/Example22SplitString.txt', 'w') as file_:
      file_.write('\n\n Example22SplitString.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
