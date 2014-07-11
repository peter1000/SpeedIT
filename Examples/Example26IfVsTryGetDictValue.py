""" Example26IfVsTryGetDictValue
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


# get a list of text lines to iterate over and split by double colon
source__dict1 = {'key4': 'value4', 'key3': 'value3', 'key6': 'value6', 'key5': 'value5', 'key8': 'value8', 'key7': 'value7', 'key9': 'value9', 'key0': 'value0', 'key2': 'value2', 'key1': 'value1'}

source__dict2 = {'key4': 'value4', 'key3': 'value3', 'key6': 'value6', 'key5a': 'value5a', 'key8': 'value8', 'key7': 'value7', 'key9': 'value9', 'key0': 'value0', 'key2': 'value2', 'key1': 'value1'}


# define some functions to compare different approaches
def get_dict_value__try():
   try:
      value = source__dict1['key5']
   except KeyError:
      value = 'missing: key5'
   #print('value: ', value)

   try:
      value = source__dict2['key5']
   except KeyError:
      value = 'missing: key5'
   #print('value: ', value)


def get_dict_value__if():
   if 'key5' in source__dict1:
      value = source__dict1['key5']
   else:
      value = 'missing: key5'
   #print('value: ', value)

   if 'key5' in source__dict2:
      value = source__dict2['key5']
   else:
      value = 'missing: key5'
   #print('value: ', value)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'get_dict_value__try': (get_dict_value__try, [], {}),
      'get_dict_value__if': (get_dict_value__if, [], {}),
   }

   setup_line_list = [
      'from __main__ import source__dict1, source__dict2'
   ]

   check_run_sec = 5
   with open('result_output/Example26IfVsTryGetDictValue.txt', 'w') as file_:
      file_.write('\n\n Example26IfVsTryGetDictValue.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
