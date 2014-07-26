""" ReadmeExample1BenchmarkIT.py implementation: <BenchmarkIT>
"""
from inspect import (
   currentframe,
   getfile
)
from operator import itemgetter
from os.path import (
   abspath,
   dirname,
   join
)
from random import shuffle
from sys import path as syspath


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'SpeedIT'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)

from SpeedIT.BenchmarkIT import speedit_benchmark


def example_whole_function():
   data = dict(zip(range(1000), range(1000)))
   shuffle(data)
   result = sorted(data.items(), key=itemgetter(1))
   del result


def example_single_subcode_blocks():
   data = dict(zip(range(1000), range(1000)))
   # ::SPEEDIT:: shuffle
   shuffle(data)
   # **SPEEDIT**
   result = sorted(data.items(), key=itemgetter(1))
   del result


def example_multiple_subcode_blocks():
   # ::SPEEDIT:: data
   data = dict(zip(range(1000), range(1000)))
   # **SPEEDIT**
   shuffle(data)
   # ::SPEEDIT:: sorted
   result = sorted(data.items(), key=itemgetter(1))
   del result
   # **SPEEDIT**


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   func_dict = {
      'whole_function': (example_whole_function, [], {}),
      'single_subcode_blocks': (example_single_subcode_blocks, [], {}),
      'multiple_subcode_blocks': (example_multiple_subcode_blocks, [], {}),
   }

   setup_line_list = [
      'from random import shuffle',
   ]

   result = speedit_benchmark(
      func_dict, setup_line_list,
      use_func_name=False,
      output_in_sec=False,
      benchmarkit__with_gc=False,
      benchmarkit__check_too_fast=True,
      benchmarkit__rank_by='best',
      benchmarkit__run_sec=1,       # None(do the function final run code), -1(run it only once) or execution run sec.
      benchmarkit__repeat=3
   )

   with open('result_output/Example2aBenchmarkIT.txt', 'w') as file_:
      file_.write('\n\n Example2aBenchmarkIT.py output\n\n')
      file_.write(result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
