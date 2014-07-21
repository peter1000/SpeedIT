""" Example implementation: <DisassembleIT>
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

from SpeedIT.DisassembleIT import speedit_disassemble


def helper_fnouter(y_):
   return y_[1]


def example_pep265(data_):
   shuffle(data_)
   result = sorted(data_.items(), key=itemgetter(1))
   del result


def example_stupid(data_):
   shuffle(data_)
   result = [(key, value) for value, key in sorted([(value, key) for key, value in data_.items()])]
   del result


def example_list_expansion(data_):
   shuffle(data_)
   list_ = [(key, value) for (key, value) in data_.items()]
   result = sorted(list_, key=lambda y_: y_[1])
   del result


def example_generator(data_):
   shuffle(data_)
   list_ = ((key, value) for (key, value) in data_.items())
   result = sorted(list_, key=lambda y_: y_[1])
   del result


def example_lambda(data_):
   shuffle(data_)
   result = sorted(data_.items(), key=lambda y_: y_[1])
   del result


def example_formal_func_inner(data_):
   shuffle(data_)

   def fninner(x):
      return x[1]

   result = sorted(data_.items(), key=fninner)
   del result


def example_formal_func_outer(data_):
   shuffle(data_)
   result = sorted(data_.items(), key=helper_fnouter)
   del result


def example_argument_substitute_func(*args, **kwargs):
   xl = args
   yl = kwargs
   al = args[0]


def my_func(ab, mul=5):
   al = [1] * (10 ** 6)
   bl = [2] * (2 * 10 ** 7)
   del bl
   cl = ab * 123456 * mul
   gl = al
   del gl
   del cl


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # Source
   # https://github.com/thisismess/python-benchmark/blob/master/examples/benchmarkDictSorting.py
   data = dict(zip(range(1000), range(1000)))

   func_dict = {
      'example_pep265': (example_pep265, [data], {}),
      'example_stupid': (example_stupid, [data], {}),
      'example_list_expansion': (example_list_expansion, [data], {}),
      'example_generator': (example_generator, [data], {}),
      'example_lambda': (example_lambda, [data], {}),
      'example_formal_func_inner': (example_formal_func_inner, [data], {}),
      'example_formal_func_outer': (example_formal_func_outer, [data], {}),
      'example_argument_substitute_func': (example_argument_substitute_func, [10, 'example'], {'argument1': 'argument1_value', 'argument2': 'argument2_value'}),
      'my_func': (my_func, [27], {'mul': 100}),
   }

   with open('result_output/Example5DisassembleIT.txt', 'w') as file_:
      file_.write('\n\n Example5DisassembleIT.py output\n\n')
      file_.write(speedit_disassemble(func_dict, use_func_name=True))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
