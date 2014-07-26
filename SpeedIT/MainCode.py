""" Main SpeedIT module
"""
from SpeedIT.BenchmarkIT import speedit_benchmark
from SpeedIT.DisassembleIT import speedit_disassemble
from SpeedIT.LineMemoryProfileIT import speedit_line_memory
from SpeedIT.ProfileIT import speedit_profile
from SpeedIT.ProjectErr import Err


def speed_it(func_dict, setup_line_list, enable_benchmarkit=True, enable_profileit=True, enable_linememoryprofileit=True, enable_disassembleit=True, use_func_name=True, output_in_sec=False, profileit__max_slashes_fileinfo=2, profileit__repeat=1, benchmarkit__with_gc=False, benchmarkit__check_too_fast=True, benchmarkit__rank_by='best', benchmarkit__run_sec=1, benchmarkit__repeat=3):
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

      enable_benchmarkit (bool):

      enable_profileit (bool):

      enable_linememoryprofileit (bool):

      enable_disassembleit (bool):

      use_func_name (bool): if True the function name will be used in the output `name` if False the `func_dict key` will be used in the the output `name`

      output_in_sec (int): if true the output is keep in seconds if false it is transformed to:
         second         (s)
         millisecond    (ms)  One thousandth of one second
         microsecond    (µs)  One millionth of one second
         nanosecond     (ns)  One billionth of one second

      profileit__max_slashes_fileinfo (int): to adjust max path levels in the profile info

      profileit__repeat (int): how often the function is repeated: the result will be the sum of all: similar to the code below

         .. code-block:: python

            for repeat in range(profileit__repeat):
               profiler.enable()
               profiler.runcall(func, *func_positional_arguments, **func_keyword_arguments)
               profiler.disable()

      benchmarkit__with_gc (bool): if True gc is kept on during timing: if False: turns off garbage collection during the timing

      benchmarkit__rank_by (str): `best` or `average`

      benchmarkit__run_sec (float or -1 or None): the number of loops per run is scaled to approximately fit the benchmarkit__run_sec

            - if benchmarkit__run_sec is -1: then the generated function source code is only run once

            - if benchmarkit__run_sec is None:  then the generated function source code is only printed
               this is mainly useful to see the exact final `func code block` which will be timed.

      benchmarkit__repeat (int): how often everything is repeated again
         This is a convenience variable that calls the whole setup repeatedly

   Returns:
      str: ready to print or write to file: table format is conform with reStructuredText
   """
   if not (enable_benchmarkit or enable_profileit or enable_linememoryprofileit or enable_disassembleit):
      raise Err('speed_it()', 'At least one of the modules must be enables: BenchmarkIT: <{}> ProfileIT: <{}> LineMemoryProfileIT: <{}> DisassembleIT: <{}>>'.format(enable_benchmarkit, enable_profileit, enable_linememoryprofileit, enable_disassembleit))

   result_txt = ''
   if enable_benchmarkit:
      result_txt += '\n\n\n================= BenchmarkIT ================= BenchmarkIT  ================= BenchmarkIT  =================\n\n'
      result_txt += speedit_benchmark(func_dict, setup_line_list, use_func_name=use_func_name, output_in_sec=output_in_sec, benchmarkit__with_gc=benchmarkit__with_gc, benchmarkit__check_too_fast=benchmarkit__check_too_fast, benchmarkit__rank_by=benchmarkit__rank_by, benchmarkit__run_sec=benchmarkit__run_sec, benchmarkit__repeat=benchmarkit__repeat)

   if enable_profileit:
      result_txt += '\n\n\n================= ProfileIT ================= ProfileIT  ================= ProfileIT  =================\n\n'
      result_txt += speedit_profile(func_dict, use_func_name=use_func_name, output_in_sec=output_in_sec, profileit__max_slashes_fileinfo=profileit__max_slashes_fileinfo, profileit__repeat=profileit__repeat)

   if enable_linememoryprofileit:
      result_txt += '\n\n\n================= LineMemoryProfileIT ================= LineMemoryProfileIT  ================= LineMemoryProfileIT  =================\n\n'
      result_txt += speedit_line_memory(func_dict, use_func_name=use_func_name)

   if enable_disassembleit:
      result_txt += '\n\n\n================= DisassembleIT ================= DisassembleIT  ================= DisassembleIT  =================\n\n'
      result_txt += speedit_disassemble(func_dict, use_func_name=use_func_name)

   return result_txt
