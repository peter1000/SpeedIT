""" Example23Primes
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


def primes(kmax):
   """ Taken from: http://docs.cython.org/src/tutorial/cython_tutorial.html#primes
   """
   p = [0] * 1000
   result = []
   if kmax > 1000:
      kmax = 1000
   k = 0
   n = 2
   while k < kmax:
      i = 0
      while i < k and n % p[i] != 0:
         i = i + 1
      if i == k:
         p[k] = n
         k = k + 1
         result.append(n)
      n = n + 1
   return result


# define SpeedIT functions
def example_direct_code_primes():
   """ Taken from: http://docs.cython.org/src/tutorial/cython_tutorial.html#primes
   """
   kmax = 1000
   p = [0] * 1000
   result = []
   if kmax > 1000:
      kmax = 1000
   k = 0
   n = 2
   while k < kmax:
      i = 0
      while i < k and n % p[i] != 0:
         i = i + 1
      if i == k:
         p[k] = n
         k = k + 1
         result.append(n)
      n = n + 1


def example_call_func_primes():
   primes(1000)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_direct_code_primes': (example_direct_code_primes, [], {}),
      'example_call_func_primes': (example_call_func_primes, [], {}),
   }

   setup_line_list = [
      'from __main__ import primes'
   ]

   check_run_sec = 1
   with open('result_output/Example23Primes.txt', 'w') as file_:
      file_.write('\n\n Example23Primes.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
