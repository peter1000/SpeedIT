""" Example6NumpyBubbleSort.: taken from: https://github.com/numba/numba/tree/master/examples
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
import sys
from sys import path as syspath

try:
   import numpy
except ImportError as err:
   sys.exit('Example6NumpyBubbleSort: Can not run example. This example needs the package numpy to be installed: <{}>'.format(err))

SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'SpeedIT'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)

from SpeedIT.BenchmarkIT import speedit_func_benchmark_list
from SpeedIT.MainCode import speed_it


def bubblesort(x_):
   """ taken from: https://github.com/numba/numba/tree/master/examples
   """
   nl = x_.shape[0]
   for end in range(nl, 1, -1):
      for i in range(end - 1):
         cur = x_[i]
         if cur > x_[i + 1]:
            tmp = x_[i]
            x_[i] = x_[i + 1]
            x_[i + 1] = tmp
            # print("Iteration: {}".format(x_))


dtype = numpy.int64
x_numpy_arr = numpy.array(list(reversed(range(20))), dtype=dtype)


# define SpeedIT functions
def example_bubblesort_func():
   x0 = x_numpy_arr.copy()
   bubblesort(x0)


def example_bubblesort_direct():
   xl = x_numpy_arr.copy()
   nl = xl.shape[0]
   for end in range(nl, 1, -1):
      for i in range(end - 1):
         cur = xl[i]
         if cur > xl[i + 1]:
            tmp = xl[i]
            xl[i] = xl[i + 1]
            xl[i + 1] = tmp
            # print("Iteration: {}".format(xl))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_bubblesort_func': (example_bubblesort_func, [], {}),
      'example_bubblesort_direct': (example_bubblesort_direct, [], {})
   }

   setup_line_list = [
      'from __main__ import x_numpy_arr',
      'from __main__ import bubblesort'
   ]

   check_run_sec = 1
   with open('result_output/Example6NumpyBubbleSort.txt', 'w') as file_:
      file_.write('\n\n Example6NumpyBubbleSort.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
