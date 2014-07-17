""" Example29NestedListComprehension
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


def lconf_to_int(int_str, extra_err_info):
   """ helper
   """
   if int_str:
      if int_str[0] == '-':
         if int_str[1:].isdigit():
            return int(int_str)
      elif int_str.isdigit():
         return int(int_str)
      raise Exception('int_str', 'int_str must contain only digits plus optional a leading - (minus sign) or EmptyString:  We got: <{}>\n    extra_err_info: {}'.format(int_str, extra_err_info))
   else:
      return ''
      
orig_line = '   2010,         , 15835945, 3000945'
 
column_replace_missing = ('-1', '-1', '-1', '-1')

cur_transform_func = (None, lconf_to_int, lconf_to_int, lconf_to_int)
               

def two_list_comprehension():
   final_value_list = [orig_value.strip() if orig_value.strip() else replacement_value for orig_value, replacement_value in zip(orig_line.split(','), column_replace_missing)]
   final_row = [transform_func(item, orig_line) if transform_func else item for transform_func, item in zip(cur_transform_func, final_value_list)]
   #print(final_row)
   

def nested_list_comprehension():
   final_row = [
      transform_func((orig_value.strip() if orig_value.strip() else replacement_value), orig_line) 
      if transform_func else 
      (orig_value.strip() if orig_value.strip() else replacement_value) 
      for transform_func, orig_value,replacement_value in zip(cur_transform_func, orig_line.split(','), column_replace_missing)
   ]
   #print(final_row)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'two_list_comprehension': (two_list_comprehension, [], {}),
      'nested_list_comprehension': (nested_list_comprehension, [], {}),
   }

   setup_line_list = [
      'from __main__ import lconf_to_int, orig_line, column_replace_missing, cur_transform_func '
   ]

   check_run_sec = 1
   with open('result_output/Example29NestedListComprehension.txt', 'w') as file_:
      file_.write('\n\n Example29NestedListComprehension.py output\n\n')
      for count in range(5):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
