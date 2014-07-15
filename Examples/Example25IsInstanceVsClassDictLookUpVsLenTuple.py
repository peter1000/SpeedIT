""" Example25IsInstanceVsClassDictLookUpVsLenTuple
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


class ExampleC(dict):
   def __init__(self, data):
      dict.__init__(self, data)
      self.__dict__['check_type'] = 'EXAMPLE_class'
      
example_class = ExampleC({'key1': 1, 'key2': 2})
   
   
example_tuple1a = ('key', ('value', 'extravalue'))
example_tuple1b = ('key', 'value')

example_tuple2a = ('key', 'value', 'extravalue')
example_tuple2b = ('key', 'value')

def example_tuple_item_isinstance():
   if isinstance(example_tuple1a[1], tuple):
      result = 'FOUND'
   else:
      result = 'NOT FOUND'
   if isinstance(example_tuple1b[1], tuple):
      result = 'FOUND'
   else:
      result = 'NOT FOUND'

def example_len_tuple():
   if len(example_tuple2a) > 2:
      result = 'FOUND'
   else:
      result = 'NOT FOUND'
   if len(example_tuple2b) > 2:
      result = 'FOUND'
   else:
      result = 'NOT FOUND'

def example_class_isinstance():
   if isinstance(example_class, ExampleC):
      result = 'FOUND'
   else:
      result = 'NOT FOUND'
   if isinstance(example_class, tuple):
      result = 'FOUND'
   else:
      result = 'NOT FOUND'

def example_class_dict_lookup():
   if example_class.check_type == 'EXAMPLE_class':
      result = 'FOUND'
   else:
      result = 'NOT FOUND'
   if example_class.check_type == 'EXAMPLE_class_wrong':
      result = 'FOUND'
   else:
      result = 'NOT FOUND'


def example_class_dict_lookup_direct():
   if example_class.__dict__['check_type'] == 'EXAMPLE_class':
      result = 'FOUND'
   else:
      result = 'NOT FOUND'
   if example_class.__dict__['check_type'] == 'EXAMPLE_class_wrong':
      result = 'FOUND'
   else:
      result = 'NOT FOUND'
   
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, dict_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_tuple_item_isinstance': (example_tuple_item_isinstance, [], {}),
      'example_len_tuple': (example_len_tuple, [], {}),
      'example_class_isinstance': (example_class_isinstance, [], {}),
      'example_class_dict_lookup': (example_class_dict_lookup, [], {}),
      'example_class_dict_lookup_direct': (example_class_dict_lookup_direct, [], {}),
   }

   setup_line_list = [
      'from __main__ import example_tuple1a, example_tuple1b, example_tuple2a, example_tuple2b, ExampleC, example_class'
   ]

   check_run_sec = 1
   with open('result_output/Example25IsInstanceVsClassDictLookUpVsLenTuple.txt', 'w') as file_:
      file_.write('\n\n Example25IsInstanceVsClassDictLookUpVsLenTuple.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
