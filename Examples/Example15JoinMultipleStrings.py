""" Example15JoinMultipleStrings
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

string1 = 'TestName'
string2 = '500'
string3 = 'yellow'


# define SpeedIT functions
def example_3_string_join():
   final_string = ''.join(['name: ', string1, '; score: ', string2, '; car: ', string3])


def example_3_string_join_tuple():
   final_string = ''.join(('name: ', string1, '; score: ', string2, '; car: ', string3))


def example_3_string_plus():
   final_string = 'name: ' + string1 + '; score: ' + string2 + '; car: ' + string3


def example_3_string_format():
   final_string = 'name: {}; score: {}; car: {}'.format(string1, string2, string3)


def example_3_string_s_percentage():
   final_string = ('name: %s; score: %s; car: %s' % (string1, string2, string3))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_3_string_join': (example_3_string_join, [], {}),
      'example_3_string_join_tuple': (example_3_string_join_tuple, [], {}),
      'example_3_string_plus': (example_3_string_plus, [], {}),
      'example_3_string_format': (example_3_string_format, [], {}),
      'example_3_string_s_percentage': (example_3_string_s_percentage, [], {}),
   }

   setup_line_list = [
      'from collections import deque',
      'from __main__ import string1, string2, string3'
   ]

   check_run_sec = 1
   with open('result_output/Example15JoinMultipleStrings.txt', 'w') as file_:
      file_.write('\n\n Example15JoinMultipleStrings.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
