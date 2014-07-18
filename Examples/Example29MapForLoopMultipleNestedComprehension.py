""" Example29MapForLoopMultipleNestedComprehension.py
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
   

def one_list_comprehension():
   final_row = [
      transform_func((orig_value.strip() if orig_value.strip() else replacement_value), orig_line) 
      if transform_func else 
      (orig_value.strip() if orig_value.strip() else replacement_value) 
      for transform_func, orig_value,replacement_value in zip(cur_transform_func, orig_line.split(','), column_replace_missing)
   ]
   #print(final_row)

def one_list_comprehension_no_zip():
   final_row = [
      cur_transform_func[idx]((orig_value.strip() if orig_value.strip() else column_replace_missing[idx]), orig_line) 
      if cur_transform_func[idx] else 
      (orig_value.strip() if orig_value.strip() else column_replace_missing[idx]) 
      for idx, orig_value in enumerate(orig_line.split(','))
   ]
   #print(final_row)
   
def nested_list_comprehension():
   final_row = [transform_func(item, orig_line) if transform_func else item for transform_func, item in zip(cur_transform_func, [orig_value.strip() if orig_value.strip() else replacement_value for orig_value, replacement_value in zip(orig_line.split(','), column_replace_missing)])]
  # #print(final_row)

def for_loop1():
   
   final_row = []
   for transform_func, orig_value, replacement_value in zip(cur_transform_func, orig_line.split(','), column_replace_missing):
      orig_value_stripped = orig_value.strip()
      final_value = orig_value_stripped if orig_value_stripped else replacement_value
      final_row.append(transform_func(final_value, orig_value)) if transform_func else final_row.append(final_value)
   #print(final_row)
   
   
def for_loop2():
   final_row = []
   for transform_func, orig_value, replacement_value in zip(cur_transform_func, orig_line.split(','), column_replace_missing):
      orig_value_stripped = orig_value.strip()
      final_row.append(transform_func(orig_value_stripped if orig_value_stripped else replacement_value, orig_value)) if transform_func else final_row.append(orig_value_stripped if orig_value_stripped else replacement_value)
   #print(final_row)
   
   
def for_loop3():
   final_row = []
   idx = 0
   for orig_value in orig_line.split(','):
      orig_value_stripped = orig_value.strip()
      transform_func = cur_transform_func[idx]
      final_row.append(transform_func(orig_value_stripped if orig_value_stripped else column_replace_missing[idx], orig_value)) if transform_func else final_row.append(orig_value_stripped if orig_value_stripped else column_replace_missing[idx])
      idx += 1
   #print(final_row)
   
   
def for_loop4():
   final_row = []
   idx = 0
   for orig_value in orig_line.split(','):
      orig_value_stripped = orig_value.strip()
      final_row.append(cur_transform_func[idx](orig_value_stripped if orig_value_stripped else column_replace_missing[idx], orig_value)) if cur_transform_func[idx] else final_row.append(orig_value_stripped if orig_value_stripped else column_replace_missing[idx])
      idx += 1
   #print(final_row)
   
def for_loop5_enumerate():
   final_row = []
   for idx, orig_value in enumerate(orig_line.split(',')):
      orig_value_stripped = orig_value.strip()
      final_row.append(cur_transform_func[idx](orig_value_stripped if orig_value_stripped else column_replace_missing[idx], orig_value)) if cur_transform_func[idx] else final_row.append(orig_value_stripped if orig_value_stripped else column_replace_missing[idx])
   #print(final_row)
   

def replacement_map(orig_value):
   return orig_value.strip()
   
def using_replacement_map():
   final_row = []
   idx = 0
   for orig_value_stripped in map(replacement_map, orig_line.split(',')):
      final_row.append(cur_transform_func[idx](orig_value_stripped if orig_value_stripped else column_replace_missing[idx], '')) if cur_transform_func[idx] else final_row.append(orig_value_stripped if orig_value_stripped else column_replace_missing[idx])
      idx += 1
   #print(final_row)



def replacement_map2(orig_value, replace_missing, transform_func):
   orig_value_stripped = orig_value.strip()
   final_value = orig_value_stripped if orig_value_stripped else replace_missing
   return transform_func(final_value, '') if transform_func else final_value
   
def using_replacement_map2():
   final_row =  map(replacement_map2, orig_line.split(','), column_replace_missing, cur_transform_func)
   #print(list(final_row))
   

   
def using_replacement_map3():
   def _inner(orig_value, replace_missing, transform_func):
      orig_value_stripped = orig_value.strip()
      final_value = orig_value_stripped if orig_value_stripped else replace_missing
      return transform_func(final_value, '') if transform_func else final_value
      
   final_row=  map(_inner, orig_line.split(','), column_replace_missing, cur_transform_func)
   #print(list(final_row))
   
def replacement_map4(orig_value, replace_missing, transform_func):
   orig_value_stripped = orig_value.strip()
   return transform_func(orig_value_stripped if orig_value_stripped else replace_missing, '') if transform_func else orig_value_stripped if orig_value_stripped else replace_missing
   
def using_replacement_map4():
   final_row =  map(replacement_map4, orig_line.split(','), column_replace_missing, cur_transform_func)
   #print(list(final_row))
   
#one_list_comprehension()
#one_list_comprehension_no_zip()
#nested_list_comprehension()

#for_loop1()
#for_loop2()
#for_loop3()
#for_loop4()
#for_loop5_enumerate()
#using_replacement_map()
#using_replacement_map2() 
#using_replacement_map3()
#using_replacement_map4()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass
   func_dict = {
      'two_list_comprehension': (two_list_comprehension, [], {}),
      'one_list_comprehension': (one_list_comprehension, [], {}),
      'one_list_comprehension_no_zip': (one_list_comprehension_no_zip, [], {}),
      'nested_list_comprehension': (nested_list_comprehension, [], {}),

      'for_loop1': (for_loop1, [], {}),
      'for_loop2': (for_loop2, [], {}),
      'for_loop3': (for_loop3, [], {}),
      'for_loop4': (for_loop4, [], {}),
      'for_loop5_enumerate': (for_loop5_enumerate, [], {}),
      'using_replacement_map': (using_replacement_map, [], {}),
      'using_replacement_map2': (using_replacement_map2, [], {}),
      'using_replacement_map3': (using_replacement_map3, [], {}),
      'using_replacement_map4': (using_replacement_map4, [], {}),
   }

   setup_line_list = [
      'from __main__ import lconf_to_int, orig_line, column_replace_missing, cur_transform_func, replacement_map, replacement_map2, replacement_map4'
   ]

   check_run_sec = 1
   with open('result_output/Example29MapForLoopMultipleNestedComprehension.py.txt', 'w') as file_:
      file_.write('\n\n Example29MapForLoopMultipleNestedComprehension.py.py output\n\n')
      for count in range(5):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
