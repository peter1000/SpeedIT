""" Example24ClearDictVsNew
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

test_dict1 = {'test-83': 'test-16', 'test-37': 'test-62', 'test-26': 'test-73', 'test-10': 'test-89', 'test-82': 'test-17', 'test-56': 'test-43', 'test-33': 'test-66', 'test-4': 'test-95', 'test-28': 'test-71', 'test-16': 'test-83', 'test-2': 'test-97', 'test-29': 'test-70', 'test-60': 'test-39', 'test-89': 'test-10', 'test-51': 'test-48', 'test-46': 'test-53', 'test-71': 'test-28', 'test-3': 'test-96', 'test-98': 'test-1', 'test-65': 'test-34', 'test-8': 'test-91', 'test-76': 'test-23', 'test-18': 'test-81', 'test-34': 'test-65', 'test-21': 'test-78', 'test-0': 'test-99', 'test-42': 'test-57', 'test-80': 'test-19', 'test-93': 'test-6', 'test-36': 'test-63', 'test-73': 'test-26', 'test-87': 'test-12', 'test-86': 'test-13', 'test-95': 'test-4', 'test-35': 'test-64', 'test-53': 'test-46', 'test-39': 'test-60', 'test-41': 'test-58', 'test-62': 'test-37', 'test-5': 'test-94', 'test-72': 'test-27', 'test-31': 'test-68', 'test-75': 'test-24', 'test-24': 'test-75', 'test-66': 'test-33', 'test-49': 'test-50', 'test-13': 'test-86', 'test-14': 'test-85', 'test-38': 'test-61', 'test-63': 'test-36', 'test-96': 'test-3', 'test-12': 'test-87', 'test-22': 'test-77', 'test-61': 'test-38', 'test-7': 'test-92', 'test-52': 'test-47', 'test-20': 'test-79', 'test-1': 'test-98', 'test-90': 'test-9', 'test-43': 'test-56', 'test-68': 'test-31', 'test-15': 'test-84', 'test-84': 'test-15', 'test-99': 'test-0', 'test-23': 'test-76', 'test-97': 'test-2', 'test-59': 'test-40', 'test-79': 'test-20', 'test-6': 'test-93', 'test-67': 'test-32', 'test-91': 'test-8', 'test-47': 'test-52', 'test-17': 'test-82', 'test-77': 'test-22', 'test-27': 'test-72', 'test-50': 'test-49', 'test-19': 'test-80', 'test-69': 'test-30', 'test-54': 'test-45', 'test-48': 'test-51', 'test-58': 'test-41', 'test-70': 'test-29', 'test-45': 'test-54', 'test-88': 'test-11', 'test-78': 'test-21', 'test-9': 'test-90', 'test-32': 'test-67', 'test-11': 'test-88', 'test-25': 'test-74', 'test-57': 'test-42', 'test-94': 'test-5', 'test-30': 'test-69', 'test-92': 'test-7', 'test-81': 'test-18', 'test-44': 'test-55', 'test-74': 'test-25', 'test-64': 'test-35', 'test-55': 'test-44', 'test-40': 'test-59', 'test-85': 'test-14'}


def example_dict_clear():
   test_dict1.clear()


def example_dict_clear_new_empty():
   test_dict = []


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, dict_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_dict_clear': (example_dict_clear, [], {}),
      'example_dict_clear_new_empty': (example_dict_clear_new_empty, [], {}),
   }

   setup_line_list = [
      'from __main__ import test_dict1'
   ]

   check_run_sec = 1
   with open('result_output/Example24ClearDictVsNew.txt', 'w') as file_:
      file_.write('\n\n Example24ClearDictVsNew.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
