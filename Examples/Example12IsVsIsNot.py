""" Example12IsVsIsNot
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

EmptyStr = ''
FiftyInt = 50

TempNone = None

TempNotNone = 1258

List_ = []


# define SpeedIT functions
def example_is():
   if isinstance(EmptyStr, dict) or isinstance(EmptyStr, list):
      pass
   else:
      pass

   if FiftyInt == 50:
      pass
   else:
      pass

   if List_:
      pass
   else:
      pass

   if TempNone is None:
      pass


def example_is_not():
   if not isinstance(EmptyStr, dict) and not isinstance(EmptyStr, list):
      pass
   else:
      pass

   if FiftyInt != 50:
      pass
   else:
      pass

   if not List_:
      pass
   else:
      pass

   if TempNotNone is not None:
      pass


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_is': (example_is, [], {}),
      'example_is_not': (example_is_not, [], {}),
   }

   setup_line_list = [
      'from __main__ import EmptyStr, FiftyInt, TempNone, TempNotNone, List_'
   ]

   check_run_sec = 1
   with open('result_output/Example12IsVsIsNot.txt', 'w') as file_:
      file_.write('\n\n Example12IsVsIsNot.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
