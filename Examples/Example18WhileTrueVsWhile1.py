""" Example18WhileTrueVsWhile1.
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

n_ = 100000


# define SpeedIT functions
def example_while_true():
   count = 0
   while True:
      count += 1
      if count == n_:
         break


def example_while_1():
   count = 0
   while 1:
      count += 1
      if count == n_:
         break


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_while_true': (example_while_true, [], {}),
      'example_while_1': (example_while_1, [], {}),
   }

   setup_line_list = [
      'from collections import deque',
      'from __main__ import n_'
   ]

   check_run_sec = 1
   with open('result_output/Example18WhileTrueVsWhile1.txt', 'w') as file_:
      file_.write('\n\n Example18WhileTrueVsWhile1.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
