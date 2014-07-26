""" Example implementation: <SPEED IT> combined: <BenchmarkIT, ProfileIT, LineMemoryProfileIT, DisassembleIT>
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

from SpeedIT.MainCode import speed_it

test_value = '~/etc/mypath'


# define SpeedIT functions
def example_startswith():
   if test_value.startswith('~/'):
      pass


def example_two_idx():
   if test_value[0] == '~' and test_value[1] == '/':
      pass


def example_slice():
   if test_value[:2] == '~/':
      pass


# example_startswith()
# example_two_idx()
# example_slice()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # Source

   # defining the: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'startswith': (example_startswith, [], {}),
      'two_idx': (example_two_idx, [], {}),
      'slice': (example_slice, [], {}),
   }

   setup_line_list = [
      'from __main__ import test_value'
   ]

   result = speed_it(
      func_dict,
      setup_line_list,
      enable_benchmarkit=True,
      enable_profileit=True,
      enable_linememoryprofileit=True,
      enable_disassembleit=True,
      use_func_name=False,
      output_in_sec=False,
      profileit__max_slashes_fileinfo=2,
      profileit__repeat=1,
      benchmarkit__with_gc=False,
      benchmarkit__check_too_fast=True,
      benchmarkit__rank_by='best',
      benchmarkit__run_sec=1,
      benchmarkit__repeat=3
   )

   with open('result_output/ReadmeExampleMainSpeedIT.txt', 'w') as file_:
      file_.write('\n\n ReadmeExampleMainSpeedIT.py output\n\n')
      file_.write(result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
