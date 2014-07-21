""" Main SpeedIT module
"""
from SpeedIT.BenchmarkIT import speedit_benchmark
from SpeedIT.DisassembleIT import speedit_disassemble
from SpeedIT.LineMemoryProfileIT import speedit_line_memory
from SpeedIT.ProfileIT import speedit_profile


def speed_it(func_dict, setup_line_list, use_func_name=True, output_in_sec=False, with_gc=False, rank_by='best', run_sec=1, repeat=3):
   """ Returns one txt string for all: Benchmark-IT, Profile-IT, Line-Memory-Profile-IT, Disassemble-IT: format is conform with reStructuredText

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

      use_func_name (bool): if True the function name will be used in the output `name` if False the `func_dict key` will be used in the the output `name`

      output_in_sec (int): if true the output is keep in seconds if false it is transformed to:
         second         (s)
         millisecond    (ms)  One thousandth of one second
         microsecond    (µs)  One millionth of one second
         nanosecond     (ns)  One billionth of one second

      with_gc (bool): used by `BenchmarkIT`: if True gc is kept on during timing: if False: turns off garbage collection during the timing

      rank_by (str): used by `BenchmarkIT`: `best` or `average`

      run_sec (float or -1 or None): used by `BenchmarkIT`: the number of loops per run is scaled to approximately fit the run_sec

            - if run_sec is -1: then the generated function source code is only run once

            - if run_sec is None:  then the generated function source code is only printed
               this is mainly useful to see the exact final `func code block` which will be timed.      output_in_sec (int): if true the output is keep in seconds if false it is transformed to: BenchmarkIT and ProfileIT

      repeat (int): used by `BenchmarkIT`: how often everything is repeated again
         This is a convenience variable that calls the whole setup repeatedly

   Returns:
      str: ready to print or write to file: table format is conform with reStructuredText
   """
   result_txt = '\n\n\n================= BenchmarkIT ================= BenchmarkIT  ================= BenchmarkIT  =================\n\n\n'
   result_txt += speedit_benchmark(func_dict, setup_line_list, use_func_name=use_func_name, output_in_sec=output_in_sec, with_gc=with_gc, rank_by=rank_by, run_sec=run_sec, repeat=repeat)

   result_txt += '\n\n\n================= ProfileIT ================= ProfileIT  ================= ProfileIT  =================\n'
   result_txt += speedit_profile(func_dict, use_func_name=use_func_name, output_in_sec=output_in_sec)

   result_txt += '\n\n\n================= LineMemoryProfileIT ================= LineMemoryProfileIT  ================= LineMemoryProfileIT  =================\n'
   result_txt += speedit_line_memory(func_dict, use_func_name=use_func_name)

   result_txt += '\n\n\n================= DisassembleIT ================= DisassembleIT  ================= DisassembleIT  =================\n'
   result_txt += speedit_disassemble(func_dict, use_func_name=use_func_name)

   return result_txt
