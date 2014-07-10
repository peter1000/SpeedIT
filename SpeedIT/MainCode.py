""" Main SpeedIT module
"""
from SpeedIT.BenchmarkIT import speedit_func_benchmark_list
from SpeedIT.DisassembleIT import speedit_func_disassemble_list
from SpeedIT.LineMemoryProfileIT import speedit_func_line_memory_list
from SpeedIT.ProfileIT import speedit_func_profile_list


def speed_it(func_dict, setup_line_list, run_sec=0.1, out_put_in_sec=False, use_func_name=True):
   """ Returns one txt string for all: BenchmarkIT, ProfileIT, LineMemoryProfileIT: format is conform with reStructuredText

   Usage:

   .. code-block:: python

      func_dict = {
         'function_f1': (function_f1, [act_one_hamlet], {}),
         'function_f2': (function_f2, [act_one_hamlet], {}),
         'function_f3': (function_f3, [act_one_hamlet], {}),
      }

      setup_line_list = [
         'from random import shuffle',
         'from os.path import abspath, dirname, join',
         'MY_CONSTANT = 15'
      ]

   Args:
      func_dict (dict): mapping function names to functions
         value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      setup_line_list (list): of strings with import lines needed by the functions any global data ect..

         .. warning:: no multiline string or indented code line

      run_sec (float): the number of loops per run is scaled to approximately fit the run_sec
      out_put_in_sec (int): if true the output is keep in seconds if false it is transformed to: BenchmarkIT and ProfileIT
         second         (s)
         millisecond    (ms)  One thousandth of one second
         microsecond    (µs)  One millionth of one second
         nanosecond     (ns)  One billionth of one second
      use_func_name (bool): if True the function name will be used in the output `name column` if False the `func_dict key` will be used in the the output `name column`

   Returns:
      str: ready to print or write to file: table format is conform with reStructuredText
   """
   result_txt = ['\n\n\n================= BenchmarkIT ================= BenchmarkIT  ================= BenchmarkIT  =================\n\n\n']
   result_txt.extend(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=run_sec, out_put_in_sec=out_put_in_sec, use_func_name=use_func_name))

   result_txt.append('\n\n\n================= ProfileIT ================= ProfileIT  ================= ProfileIT  =================\n')
   for table in speedit_func_profile_list(func_dict, out_put_in_sec=out_put_in_sec, use_func_name=use_func_name):
      result_txt.append('\n\n')
      result_txt.extend(table)

   result_txt.append('\n\n\n================= LineMemoryProfileIT ================= LineMemoryProfileIT  ================= LineMemoryProfileIT  =================\n')
   for table in speedit_func_line_memory_list(func_dict, use_func_name=use_func_name):
      result_txt.append('\n\n')
      result_txt.extend(table)

   result_txt.append('\n\n\n================= DisassembleIT ================= DisassembleIT  ================= DisassembleIT  =================\n')
   for table in speedit_func_disassemble_list(func_dict, use_func_name=True):
      result_txt.append('\n\n')
      result_txt.extend(table)

   return '\n'.join(result_txt)
