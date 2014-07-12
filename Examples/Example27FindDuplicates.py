""" Example27FindDuplicates
"""
from collections import Counter
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


source__list = ['example0', 'example16', 'example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7', 'example8', 'example9', 'example10', 'example11', 'example12', 'example13', 'example14', 'example15', 'example16', 'example17', 'example25', 'example18', 'example19', 'example20', 'example21', 'example22', 'example23', 'example24', 'example25', 'example26', 'example27', 'example5', 'example28', 'example29']

def find_duplicates_1():
   # http://stackoverflow.com/questions/9835762/find-and-list-duplicates-in-python-list
   # adds all elements it doesn't know yet to seen and all other to seen_twice
   seen = set()
   seen_twice = set(item for item in source__list if item in seen or seen.add(item))
   #print(seen_twice)
   
   
def find_duplicates_2():
   seen_twice = (set([item for item in source__list if source__list.count(item) > 1]))
   #print(seen_twice)

def find_duplicates_3():
   seen_twice = [x_ for x_, y_ in Counter(source__list).items() if y_ > 1]
   #print(seen_twice)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'find_duplicates_1': (find_duplicates_1, [], {}),
      'find_duplicates_2': (find_duplicates_2, [], {}),
      'find_duplicates_3': (find_duplicates_3, [], {}),
   }

   setup_line_list = [
      'from collections import Counter',
      'from __main__ import source__list'
   ]

   check_run_sec = 5
   with open('result_output/Example27FindDuplicates.txt', 'w') as file_:
      file_.write('\n\n Example27FindDuplicates.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
