""" Example implementation: <LineMemoryProfileIT>
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

from SpeedIT.LineMemoryProfileIT import speedit_line_memory


def my_func(ab, mul=5):
   al = [1] * (10 ** 6)
   bl = [2] * (2 * 10 ** 7)
   del bl
   cl = ab * 123456 * mul
   gl = al
   del gl
   del cl


def my_func2():
   a = [1] * (10 ** 6)
   b = [2] * (2 * 10 ** 7)
   del b
   del a


def example_argument_substitute_func(*args, **kwargs):
   xl = args
   yl = kwargs
   al = args[0]


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass
   func_dict = {
      'my_func': (my_func, [27], {'mul': 100}),
      'my_func2': (my_func2, [], {}),
      'example_argument_substitute_func': (example_argument_substitute_func, [10, 'example'], {'argument1': 'argument1_value', 'argument2': 'argument2_value', 'loops': 1})
   }

   with open('result_output/Example4LineMemoryProfileIT2.txt', 'w') as file_:
      file_.write('\n\n Example4LineMemoryProfileIT2.py output\n\n')
      file_.write(speedit_line_memory(func_dict))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
