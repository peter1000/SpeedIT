""" Example10GetLineIndent
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

source = '''_____START :: PlotMA
whatever1 :: nothing1
whatever2 :: nothing2
whatever3
   Not_sure
   1234
- MAs
   MA0
      Period :: 10
      MAShift :: 0
      Method :: 1
      AppliedTo :: 0
      LineStyle :: 0
      LineWidth :: 1
      Color :: Lime
   MA1
      Period :: 21
      MAShift :: 0
      Method :: 1
      AppliedTo :: 0
      LineStyle :: 0
      LineWidth :: 1
      Color :: Aqua
   MA2
      Period :: 50
      MAShift :: 0
      Method :: 0
      AppliedTo :: 0
      LineStyle :: 0
      LineWidth :: 2
      Color :: DarkViolet
- STOKs
   STOK0
      Period :: 50
      Method
         llll
         ffff
         eee
- Fibs
_____END'''

source_lines = source.splitlines()


def get_indent_with_len():
   for line in source_lines:
      final_line = line.lstrip()
      cur_indent = len(line) - len(line.lstrip())
      # print('cur_indent: ', cur_indent , ' : ', final_line)


def get_indent_with_idx():
   cur_indent = 0
   for line in source_lines:
      if line[0] != ' ':
         cur_indent = 0
      elif line[3] != ' ':
         cur_indent = 3
      elif line[6] != ' ':
         cur_indent = 6
      elif line[9] != ' ':
         cur_indent = 9
      final_line = line[cur_indent:]
      # print('cur_indent: ', cur_indent , ' : ', final_line)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'get_indent_with_len': (get_indent_with_len, [], {}),
      'get_indent_with_idx': (get_indent_with_idx, [], {}),
   }

   setup_line_list = [
      'from __main__ import source_lines',
   ]

   check_run_sec = 1
   with open('result_output/Example10GetLineIndent.txt', 'w') as file_:
      file_.write('\n\n Example10GetLineIndent.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      file_.write('\n\n')
      file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
