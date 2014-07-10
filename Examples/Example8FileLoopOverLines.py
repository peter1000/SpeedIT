""" Example8FileLoopOverLines
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


# define SpeedIT functions
def read_file_and_split_later():
   with open('Hamlet.txt', 'r') as file_:
      temp_txt = file_.read()
   for line in (temp_txt.split('\n')):
      pass


def read_file_for_line_in_file():
   with open('Hamlet.txt', 'r') as file_:
      for line in file_:
         pass


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'read_file_and_split_later': (read_file_and_split_later, [], {}),
      'read_file_for_line_in_file': (read_file_for_line_in_file, [], {}),
   }

   setup_line_list = [
   ]

   check_run_sec = 1
   with open('result_output/Example8FileLoopOverLines.txt', 'w') as file_:
      file_.write('\n\n Example8FileLoopOverLines.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
