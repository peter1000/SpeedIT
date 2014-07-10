""" Example7IterSplitlines
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

# using txt from: http://www.william-shakespeare.info/act1-script-text-hamlet.htm
# get a text to iterate over and split by lines
act_one_hamlet = r'''
Script / Text of Act I Hamlet

ACT I
SCENE I. Elsinore. A platform before the castle.

FRANCISCO at his post. Enter to him BERNARDO
BERNARDO
Who's there?
'''


# define some functions to compare different approaches
def f1():
   """ Example taken from: http://stackoverflow.com/questions/3054604/iterate-over-the-lines-of-a-string
   """
   return iter(act_one_hamlet.splitlines())


def f2():
   """ Example taken from: http://stackoverflow.com/questions/3054604/iterate-over-the-lines-of-a-string
   """
   retval = ''
   for char in act_one_hamlet:
      retval += char if not char == '\n' else ''
      if char == '\n':
         yield retval
         retval = ''
   if retval:
      yield retval


def f3():
   """ Example taken from: http://stackoverflow.com/questions/3054604/iterate-over-the-lines-of-a-string
   """
   prevnl = -1
   while True:
      nextnl = act_one_hamlet.find('\n', prevnl + 1)
      if nextnl < 0:
         break
      yield act_one_hamlet[prevnl + 1:nextnl]
      prevnl = nextnl


# define speed_it functions
def function_f1():
   result = list(f1())
   del result


def function_f2():
   result = list(f2())
   del result


def function_f3():
   result = list(f3())
   del result


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'function_f1': (function_f1, [], {}),
      'function_f2': (function_f2, [], {}),
      'function_f3': (function_f3, [], {}),
   }

   setup_line_list = [
      'from __main__ import act_one_hamlet, f1, f2, f3'
   ]

   check_run_sec = 1
   with open('result_output/Example7IterSplitlines.txt', 'w') as file_:
      file_.write('\n\n Example7IterSplitlines.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
