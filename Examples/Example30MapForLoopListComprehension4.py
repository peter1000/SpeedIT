""" Example30MapForLoopListComprehension4.py
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
 
number_items = 4

def one_list_comprehension():
   final_row = [lconf_to_int(orig_value.strip(), orig_line) for orig_value in orig_line.split(',')]
   #print(final_row)

def for_loop():
   final_row = []
   idx = 0
   for orig_value in orig_line.split(','):
      orig_value_stripped = orig_value.strip()
      final_row.append(lconf_to_int(orig_value_stripped, orig_value))
      idx += 1
   #print(final_row)


def replacement_map(orig_value, transform_func):
   return transform_func(orig_value.strip(), '')
   
def using_replacement_map():
   final_row =  map(replacement_map, orig_line.split(','),  [lconf_to_int] * number_items)
   #print(list(final_row))


#one_list_comprehension()
#for_loop()
#using_replacement_map()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass
   func_dict = {
      'one_list_comprehension': (one_list_comprehension, [], {}),
      'for_loop': (for_loop, [], {}),
      'using_replacement_map': (using_replacement_map, [], {}),
   }

   setup_line_list = [
      'from __main__ import orig_line, number_items, lconf_to_int, replacement_map'
   ]

   check_run_sec = 1
   with open('result_output/Example30MapForLoopListComprehension4.py.txt', 'w') as file_:
      file_.write('\n\n Example30MapForLoopListComprehension4.py.py output\n\n')
      for count in range(5):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      #speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      #file_.write('\n\n')
      #file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
