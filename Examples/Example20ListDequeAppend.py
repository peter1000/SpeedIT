""" Example20ListDequeAppend
"""
from collections import deque
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

test_list1 = ['test-0', 'test-1', 'test-2', 'test-3', 'test-4', 'test-5', 'test-6', 'test-7', 'test-8', 'test-9', 'test-10', 'test-11', 'test-12', 'test-13', 'test-14', 'test-15', 'test-16', 'test-17', 'test-18', 'test-19', 'test-20', 'test-21', 'test-22', 'test-23', 'test-24', 'test-25', 'test-26', 'test-27', 'test-28', 'test-29', 'test-30', 'test-31', 'test-32', 'test-33', 'test-34', 'test-35', 'test-36', 'test-37', 'test-38', 'test-39', 'test-40', 'test-41', 'test-42', 'test-43', 'test-44', 'test-45', 'test-46', 'test-47', 'test-48', 'test-49', 'test-50', 'test-51', 'test-52', 'test-53', 'test-54', 'test-55', 'test-56', 'test-57', 'test-58', 'test-59', 'test-60', 'test-61', 'test-62', 'test-63', 'test-64', 'test-65', 'test-66', 'test-67', 'test-68', 'test-69', 'test-70', 'test-71', 'test-72', 'test-73', 'test-74', 'test-75', 'test-76', 'test-77', 'test-78', 'test-79', 'test-80', 'test-81', 'test-82', 'test-83', 'test-84', 'test-85', 'test-86', 'test-87', 'test-88', 'test-89', 'test-90', 'test-91', 'test-92', 'test-93', 'test-94', 'test-95', 'test-96', 'test-97', 'test-98', 'test-99']

final_list1 = []
final_list2 = []
final_list3 = []
final_deque1 = deque([])
final_deque2 = deque([])


# define SpeedIT functions
def example_deque_append_left():
   for item in test_list1:
      final_deque1.appendleft(item)
      # print(final_deque1)


def example_list_insert_left():
   for item in test_list1:
      final_list1.insert(0, item)
      # print(final_list1)


def example_list_left_append_reverse():
   for item in test_list1:
      final_list2.append(item)
   final_list2.reverse()
   # print(final_list2)


def example_deque_append_right():
   for item in test_list1:
      final_deque2.append(item)
      # print(final_deque2)


def example__list_append_right():
   for item in test_list1:
      final_list3.append(item)
      # print(final_list3)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'example_deque_append_left': (example_deque_append_left, [], {}),
      'example_list_insert_left': (example_list_insert_left, [], {}),
      'example_list_left_append_reverse': (example_list_left_append_reverse, [], {}),
      'example_deque_append_right': (example_deque_append_right, [], {}),
      'example__list_append_right': (example__list_append_right, [], {}),
   }

   setup_line_list = [
      'from collections import deque',
      'from __main__ import test_list1, final_list1, final_list2, final_list3, final_deque1, final_deque2',
   ]

   check_run_sec = 1
   with open('result_output/Example20ListDequeAppend.txt', 'w') as file_:
      file_.write('\n\n Example20ListDequeAppend.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()