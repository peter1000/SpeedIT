""" Example14Join2Strings
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

string1 = 'Sections of both opened throughout the late 1990s. Highway 416 was commemorated'
string2 = ' as the Veterans Memorial Highway on the 54th anniversary of D-Day in 1998.'


# define SpeedIT functions
def example_2_string_join():
   final_string = ''.join([string1, string2])


def example_2_string_join_tuple():
   final_string = ''.join((string1, string2))


def example_2_string_plus():
   final_string = string1 + string2


def example_2_string_format():
   final_string = '{}{}'.format(string1, string2)


def example_2_string_s_percentage():
   final_string = ('%s%s,' % (string1, string2))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_2_string_join': (example_2_string_join, [], {}),
      'example_2_string_join_tuple': (example_2_string_join_tuple, [], {}),
      'example_2_string_plus': (example_2_string_plus, [], {}),
      'example_2_string_format': (example_2_string_format, [], {}),
      'example_2_string_s_percentage': (example_2_string_s_percentage, [], {}),
   }

   setup_line_list = [
      'from collections import deque',
      'from __main__ import string1, string2'
   ]

   check_run_sec = 1
   with open('result_output/Example14Join2Strings.txt', 'w') as file_:
      file_.write('\n\n Example14Join2Strings.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
