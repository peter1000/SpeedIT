""" Example11JoinDictionaries
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

value_dict1 = {'slot1': 'value1', 'slot2': 'value2', 'slot3': 'value3', 'slot4': 'value4', 'slot5': 'value5'}
value_dict2 = {'test-90': 90, 'test-34': 34, 'test-76': 76, 'test-46': 46, 'test-89': 89, 'test-22': 22, 'test-85': 85, 'test-5': 5, 'test-45': 45, 'test-24': 24, 'test-47': 47, 'test-6': 6, 'test-65': 65, 'test-21': 21, 'test-70': 70, 'test-7': 7, 'test-18': 18, 'test-86': 86, 'test-50': 50, 'test-12': 12, 'test-52': 52, 'test-26': 26, 'test-3': 3, 'test-75': 75, 'test-71': 71, 'test-29': 29, 'test-13': 13, 'test-31': 31, 'test-42': 42, 'test-82': 82, 'test-96': 96, 'test-99': 99, 'test-40': 40, 'test-32': 32, 'test-9': 9, 'test-93': 93, 'test-14': 14, 'test-33': 33, 'test-66': 66, 'test-67': 67, 'test-58': 58, 'test-94': 94, 'test-73': 73, 'test-92': 92, 'test-54': 54, 'test-87': 87, 'test-72': 72, 'test-8': 8, 'test-57': 57, 'test-91': 91, 'test-51': 51, 'test-30': 30, 'test-2': 2, 'test-97': 97, 'test-63': 63, 'test-39': 39, 'test-10': 10, 'test-98': 98, 'test-49': 49, 'test-43': 43, 'test-81': 81, 'test-35': 35, 'test-41': 41, 'test-28': 28, 'test-83': 83, 'test-68': 68, 'test-95': 95, 'test-62': 62, 'test-38': 38, 'test-88': 88, 'test-15': 15, 'test-1': 1, 'test-20': 20, 'test-53': 53, 'test-48': 48, 'test-56': 56, 'test-0': 0, 'test-16': 16, 'test-19': 19, 'test-74': 74, 'test-69': 69, 'test-61': 61, 'test-55': 55, 'test-4': 4, 'test-25': 25, 'test-44': 44, 'test-78': 78, 'test-64': 64, 'test-79': 79, 'test-36': 36, 'test-27': 27, 'test-59': 59, 'test-60': 60, 'test-23': 23, 'test-77': 77, 'test-37': 37, 'test-84': 84, 'test-11': 11, 'test-17': 17, 'test-80': 80}


def join2dict_for_key_value():
   final_dict = {}
   for key, value in value_dict1.items():
      final_dict[key] = value
   for key, value in value_dict2.items():
      final_dict[key] = value
      # print(final_dict)


def join2dict_update():
   final_dict = {}
   final_dict.update(value_dict1)
   final_dict.update(value_dict2)
   # print(final_dict)


def join2dict_create_new_dict():
   final_dict = {}
   final_dict = dict(final_dict, **value_dict1)
   final_dict = dict(final_dict, **value_dict2)
   # print(final_dict)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'join2dict_for_key_value': (join2dict_for_key_value, [], {}),
      'join2dict_update': (join2dict_update, [], {}),
      'join2dict_create_new_dict': (join2dict_create_new_dict, [], {}),
   }

   setup_line_list = [
      'from __main__ import value_dict1, value_dict2',
   ]

   check_run_sec = 1
   with open('result_output/Example11JoinDictionaries.txt', 'w') as file_:
      file_.write('\n\n Example11JoinDictionaries.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
