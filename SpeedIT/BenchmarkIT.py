""" Benchmark module: can also compare multiple functions
"""
import gc
from inspect import (
   signature,
   getsourcelines
)
from operator import itemgetter
from time import perf_counter

from SpeedIT.ProjectErr import Err
from SpeedIT.Utils import (
   format_time,
   get_table_rst_formatted_lines
)



def _helper_get_perf_counter_reference_time():
   """ Helper: Returns 2 times: the smallest difference of calling perf_counter() immediately after each other a couple of times

   Returns:
      float: 2 times the smallest difference of calling perf_counter() immediately after each other a couple of times
   """
   _result_time = 99999999999.0
   for y_ in range(50):
      for x_ in range(3000):
         temp_start = perf_counter()
         temp_time = perf_counter() - temp_start
         if temp_time < _result_time:
            _result_time = temp_time
   return _result_time * 2


class _TimeIT(object):
   """ Class for timing execution speed of function code.

   Partially based on code from python timeit.py

   This does not execute the original function but generates a new function which executes only the code body of 'func': `func code block`
   This avoids calling into the function itself

   Args:
      func (function):

         .. warning:: the `func` function may not have any return statements: but any inner function can have one

         OK

         .. code-block:: python

            def example_formal_func_inner(data_):
               shuffle(data_)
               def fninner(x):
                  return x[1]
               result = sorted(data_.items(), key=fninner)
               del result

         NOT OK

         .. code-block:: python

            def example_pep265(data_):
               shuffle(data_)
               result = sorted(data_.items(), key=itemgetter(1))
               return result

      func_positional_arguments (list): positional arguments for the function
      func_keyword_arguments (dict): any keyword arguments for the function
      setup_line_list (list): of strings with import lines needed by the functions any global data ect..
         this part is executed once before the actual `func code block` enters the loop

         .. warning:: no multiline string or indented code line

      check_too_fast(bool): if True and a code block is timed faster than a `Reference-Time` an Exception is raised.

         - Reference-Time: the smallest difference of calling perf_counter() immediately after each other a couple of times


         .. seealso:: _helper_get_perf_counter_reference_time()

      run_sec (float or -1 or None): seconds the `func code block` will be executed (looped over)

            - if run_sec is -1: then the generated function source code is only run once

            - if run_sec is None:  then the generated function source code is only printed
               this is mainly useful to see the exact final `func code block` which will be timed.

      name (str): the name used for the output `name` part

      perf_counter_reference_time (float): passed on see: _helper_get_perf_counter_reference_time()
   """

   def __init__(self, func, args_list, kwargs_dict, setup_line_list, check_too_fast, run_sec, name, perf_counter_reference_time):
      """ Constructor.  See class doc string.
      """
      self.func = func
      self.orig_func_name = getattr(self.func, "__name__", self.func)
      self.args_list = args_list.copy()
      self.kwargs_dict = kwargs_dict.copy()
      self.setup_line_list = setup_line_list
      self.check_too_fast = check_too_fast
      self.run_sec = run_sec
      self.name = name
      self.perf_counter_reference_time = perf_counter_reference_time
      if callable(self.func):
         _ns = {}
         self.src = self.__get_final_inner_function()
         if self.run_sec is not None and self.run_sec != -1 and self.run_sec < 0.1:
            raise Err('_TimeIT.__init__()', 'run_sec: <{:.1f}> must be at least <0.1 second> or <-1 to run it once> or <None to print the `func code block`>'.format(self.run_sec))

         _code = compile(self.src, 'benchmarkit-src', "exec")
         exec(_code, globals(), _ns)
         self.inner = _ns["inner"]
      else:
         raise ValueError('<func>: is not a `callable` type: <{}>'.format(self.func))


   def benchmark_it(self, with_gc):
      """ Returns timing result for the `func code block`

      .. note::
         By default, timeit() temporarily turns off garbage collection during the timing.
         The advantage of this approach is that it makes independent timings more comparable.
         This disadvantage is that GC may be an important component of the performance of the function being measured.
         If so, GC can be re-enabled as the with_gc=True

      Returns:
         dict: benchmark result: dict keys: loops, all_loops_time_sec, avg_loop_sec, best_loop_sec, worst_loop_sec

            - loops: how many times the  `func code block` was executed (looped over)
            - all_loops_time_sec: the total time in seconds for all loops:
               only loop times are counted not other times: depending on the `func code block` this can be about 25% of the total runtime
            - avg_loop_sec: average loop time in seconds: this should be mostly used as measure time:
               if there where only a very low number of loops - one might want to increase the `run_sec` and rerun it
            - two_best_loop_sec: time in seconds for the two fastest of all loops
            - two_worst_loop_sec: time in seconds for the two slowest of all loops

      Raises:
         SpeedIT.Err: example if `run_sec` is not <-1 run once>, <None only print> but less than 0.1
      """
      if self.run_sec is None:
         benchmark_result = self.src
      elif with_gc:
         gc_old = gc.isenabled()
         gc.enable()
         try:
            benchmark_result = self.inner()
            benchmark_result['name'] = self.name
         finally:
            if not gc_old:
               gc.disable()
      else:
         gc_old = gc.isenabled()
         gc.disable()
         try:
            benchmark_result = self.inner()
            benchmark_result['name'] = self.name
         finally:
            if gc_old:
               gc.enable()
      return benchmark_result

   def __get_final_inner_function(self):
      """ Returns a string of an generated inner function with the code body from: func

      Tries to generate a function with the 'code-body' from the passed on func as well as the args_list, kwargs_dict

      .. warnings:: the `func` function may not have any return statements: but any inner function can have one

      Returns:
         str: generated inner function

      Raises:
         SpeedIT.Err: example if an indentation is encountered which is not a multiple of the first found indentation
      """
      has_block_speedit = False
      _start_block_stripped_line = ''
      start_tag_block_speedit = 0
      end_tag_block_speedit = 0

      func_line, lnum = getsourcelines(self.func)
      sig = signature(self.func)
      indent_ = None
      func_def_indent = len(func_line[0]) - len(func_line[0].lstrip())
      func_body = func_line[1:]
      search_docstring = False

      # PREPARE: remove docstring and get final indentation
      first_none_docstring_idx = 0
      for idx, line_orig in enumerate(func_body):
         rstripped_line = line_orig.rstrip()
         if rstripped_line:
            stripped_codeline = rstripped_line.lstrip()
            if stripped_codeline[0] == '#':  # remove comment lines
               if not ('::SPEEDIT::' in stripped_codeline or '**SPEEDIT**' in stripped_codeline):
                  continue
            if search_docstring:
               if stripped_codeline[0:3] == '"""' or stripped_codeline[0:3] == "'''":
                  search_docstring = False
               continue
            else:
               codebody_indent = len(rstripped_line) - len(stripped_codeline)
               indent_ = codebody_indent - func_def_indent
               # Check if we have a docstring
               if stripped_codeline[0:3] == '"""' or stripped_codeline[0:3] == "'''":
                  search_docstring = True
                  continue
            first_none_docstring_idx = idx
            break

      # do the func code body
      adjusted_func_code_line = []
      for line_orig in func_body[first_none_docstring_idx:]:
         # remove empty
         if line_orig:
            # get indentation check it is a multiple of indent_
            rstrip_line = line_orig.rstrip()
            if rstrip_line:
               stripped_line = rstrip_line.lstrip()
               if stripped_line[0] == '#':  # remove comment lines: keep any with  ::SPEEDIT::
                  if '::SPEEDIT::' in stripped_line or '**SPEEDIT**' in stripped_line:
                     has_block_speedit = True
                  else:
                     continue
               line_indentation = len(rstrip_line) - len(stripped_line)
               if line_indentation % indent_ != 0:
                  raise Err('_TimeIT.get_final_inner_function', '<{}>: ERROR: indentation must be a multiple of the second function line: <{}>\n  seems we encountered a wrong indented line: line_indentation: <{}>\n {}'.format(self.orig_func_name, indent_, line_indentation, line_orig))
               line_indentation_level = int((line_indentation - func_def_indent) / indent_) + 1  # need one extra level

               if has_block_speedit:
                  if '::SPEEDIT::' in stripped_line:
                     if start_tag_block_speedit != end_tag_block_speedit:
                        # expected END Tag
                        raise Err('_TimeIT.get_final_inner_function', '<{}>: FUNCTION INNER TAG ERROR: has_block_speedit: <{}>\n  Expected an END-TAG <**SPEEDIT**>: \n {}'.format(self.orig_func_name, has_block_speedit, line_orig))
                     adjusted_func_code_line.append(('   ' * line_indentation_level) + '_speeit_prefix__stmt_inner_start = _speeit_prefix__perf_counter()  # ::SPEEDIT::START internally added')
                     start_tag_block_speedit += 1
                     _start_block_stripped_line = stripped_line
                  elif '**SPEEDIT**' in stripped_line:
                     if end_tag_block_speedit != start_tag_block_speedit - 1:
                        # expected START TAG
                        raise Err('_TimeIT.get_final_inner_function', '<{}>: FUNCTION INNER TAG ERROR: has_block_speedit: <{}>\n  Expected an START-TAG <::SPEEDIT::>: \n {}'.format(self.orig_func_name, has_block_speedit, line_orig))
                     # Do this inner result
                     adjusted_func_code_line.append(('   ' * line_indentation_level) + '_speeit_prefix__result_time += _speeit_prefix__perf_counter() - _speeit_prefix__stmt_inner_start  # **SPEEDIT**END internally added')
                     if self.check_too_fast:
                        adjusted_func_code_line.append(('   ' * line_indentation_level) + 'if _speeit_prefix__result_time < _speeit_prefix__check_reference_time: raise Exception("in function: <{}>'.format(self.orig_func_name) + ' code block: too fast to measure:\\n   code part: _speeit_prefix__result_time: <{:.11f}>  2 times _smallest_perf_counter_time: <{:.11f}>\\n  ' + '  _start_block_stripped_line: <{}>'.format(_start_block_stripped_line) + '".format(_speeit_prefix__result_time, _speeit_prefix__check_reference_time))  # SPEEDIT: internally added')
                     end_tag_block_speedit += 1
                  else:
                     adjusted_func_code_line.append(('   ' * line_indentation_level) + stripped_line)
               else:
                  adjusted_func_code_line.append(('   ' * line_indentation_level) + stripped_line)

      # CHECK: LAST END TAG
      # e.g. if a function body ends with an END-TAG this is not returned by: inspect.getsourcelines(self.func)
      if has_block_speedit:
         if start_tag_block_speedit != end_tag_block_speedit:
            # Do the last inner result: ADDING an END-TAG
            adjusted_func_code_line.append('      _speeit_prefix__result_time += _speeit_prefix__perf_counter() - _speeit_prefix__stmt_inner_start  # **SPEEDIT**END internally added')
            if self.check_too_fast:
               adjusted_func_code_line.append('      if _speeit_prefix__result_time < _speeit_prefix__check_reference_time: raise Exception("in function: <{}>'.format(self.orig_func_name) + ' code block: too fast to measure:\\n   code part: _speeit_prefix__result_time: <{:.11f}>  2 times _smallest_perf_counter_time: <{:.11f}>\\n  ' + '  _start_block_stripped_line: <{}>'.format(_start_block_stripped_line) + '".format(_speeit_prefix__result_time, _speeit_prefix__check_reference_time))  # SPEEDIT: internally added')

      # add the normal perf_counter time lines
      else:
         adjusted_func_code_line.insert(0, '      _speeit_prefix__stmt_inner_start = _speeit_prefix__perf_counter()  # ::SPEEDIT::START internally added')
         adjusted_func_code_line.append('      _speeit_prefix__result_time += _speeit_prefix__perf_counter() - _speeit_prefix__stmt_inner_start  # **SPEEDIT**END internally added')

         if self.check_too_fast:
            adjusted_func_code_line.append('      if _speeit_prefix__result_time < _speeit_prefix__check_reference_time: raise Exception("in function: <{}>'.format(self.orig_func_name) + ' code block: too fast to measure:\\n   code part: _speeit_prefix__result_time: <{:.11f}>  2 times _smallest_perf_counter_time: <{:.11f}>".format(_speeit_prefix__result_time, _speeit_prefix__check_reference_time))  # SPEEDIT: internally added')

      # Do the arguments
      final_param_line = []
      for param, value in sig.parameters.items():
         if value.kind == value.POSITIONAL_OR_KEYWORD:
            # check if we have a keyword
            if param in self.kwargs_dict:
               value_to_set = self.kwargs_dict.pop(param)
            else:  # use the positional
               value_to_set = self.args_list.pop(0)
            if isinstance(value_to_set, str):
               parameter_line = '{} = "{}"'.format(param, value_to_set)
            else:
               parameter_line = '{} = {}'.format(param, value_to_set)
            final_param_line.append(('   ' * 2) + parameter_line)
         elif value.kind == value.POSITIONAL_ONLY:
            value_to_set = self.args_list.pop(0)
            if isinstance(value_to_set, str):
               parameter_line = '{} = "{}"'.format(param, value_to_set)
            else:
               parameter_line = '{} = {}'.format(param, value_to_set)
            final_param_line.append(('   ' * 2) + parameter_line)
            # TODO: From docs: 3.4 Python has no explicit syntax for defining positional-only parameters, but many built-in and extension module functions (especially those that accept only one or two parameters) accept them.
            raise Err('_TimeIT.get_final_inner_function()', 'POSITIONAL_ONLY !! not sure what to do .. check in future if needed: param: <{}> value.kind: <{}>'.format(param, value.kind))
         elif value.kind == value.VAR_POSITIONAL:  # do the remaining POSITIONAL arguments
            parameter_line = '{} = {}'.format(param, self.args_list)
            final_param_line.append(('   ' * 2) + parameter_line)
         elif value.kind == value.KEYWORD_ONLY:
            if param in self.kwargs_dict:
               value_to_set = self.kwargs_dict.pop(param)
            else:  # use the default
               value_to_set = value.default
            if isinstance(value_to_set, str):
               parameter_line = '{} = "{}"'.format(param, value_to_set)
            else:
               parameter_line = '{} = {}'.format(param, value_to_set)
            final_param_line.append(('   ' * 2) + parameter_line)
         elif value.kind == value.VAR_KEYWORD:  # do the remaining KEYWORD arguments
            parameter_line = '{} = {}'.format(param, self.kwargs_dict)
            final_param_line.append(('   ' * 2) + parameter_line)
         else:
            continue

      # do self.setup_line_list
      final_setup_lines = []
      for setup_line in self.setup_line_list:
         setup_line = setup_line.strip()
         if setup_line:
            final_setup_lines.append('   ' + setup_line)

      final_inner_function_lines = [
         'def inner():  # orig function name: <{}>'.format(self.orig_func_name),
         '   from time import perf_counter as _speeit_prefix__perf_counter',
         '',
         '   _speeit_prefix__run_sec = {}'.format(self.run_sec),
         '',
         '   # ==================== START SETUP LINES ==================== #',
         '',
      ]

      final_inner_function_lines.extend(final_setup_lines)

      inner_function_lines_part2 = [
         '',
         '   # ==================== END SETUP LINES ==================== #',
         '',
         '   # The smallest difference of calling _speeit_prefix__perf_counter() immediately after each other a couple of times',
         '   _speeit_prefix__check_reference_time = {}'.format(self.perf_counter_reference_time),
         '   _speeit_prefix__loops = 0',
         '   _speeit_prefix__all_loops_time_sec = 0.0',
         '   _speeit_prefix__avg_loop_sec = 0.0',
         '   _speeit_prefix__best_loop_sec = 99999999999.0',
         '   _speeit_prefix__second_best_loop_sec = 99999999999.0',
         '   _speeit_prefix__worst_loop_sec = 0.0',
         '   _speeit_prefix__second_worst_loop_sec = 0.0',
         '   if _speeit_prefix__run_sec is None:',
         '      return {',
         '         "loops": _speeit_prefix__loops,',
         '         "all_loops_time_sec": _speeit_prefix__all_loops_time_sec,',
         '         "avg_loop_sec": _speeit_prefix__avg_loop_sec,',
         '         "best_loop_sec": _speeit_prefix__best_loop_sec,',
         '         "second_best_loop_sec": _speeit_prefix__second_best_loop_sec,',
         '         "worst_loop_sec": _speeit_prefix__worst_loop_sec,',
         '         "second_worst_loop_sec": _speeit_prefix__second_worst_loop_sec',
         '      }',
         '   elif _speeit_prefix__run_sec == -1:',
         '      # only run it once',
         '      _speeit_prefix__run_once = True',
         '   else:',
         '      _speeit_prefix__run_once = False',
         '   _speeit_prefix__main_start_time = _speeit_prefix__perf_counter()',
         '   while True:',
         '      _speeit_prefix__loops += 1',
         '      _speeit_prefix__result_time = 0',
         '',
         '      # ==================== START CODE BLOCK ==================== #',
         '',
      ]

      final_inner_function_lines.extend(inner_function_lines_part2)

      final_inner_function_lines.extend(final_param_line)
      final_inner_function_lines.extend(adjusted_func_code_line)

      inner_function_lines_rest = [
         '',
         '      # ==================== END CODE BLOCK ==================== #',
         '',
         '      _speeit_prefix__all_loops_time_sec += _speeit_prefix__result_time',
         '      if _speeit_prefix__result_time <= _speeit_prefix__best_loop_sec:',
         '         _speeit_prefix__second_best_loop_sec = _speeit_prefix__best_loop_sec',
         '         _speeit_prefix__best_loop_sec = _speeit_prefix__result_time',
         '      if _speeit_prefix__result_time >= _speeit_prefix__worst_loop_sec:',
         '         _speeit_prefix__second_worst_loop_sec = _speeit_prefix__worst_loop_sec',
         '         _speeit_prefix__worst_loop_sec = _speeit_prefix__result_time',
         '      if _speeit_prefix__run_once:',
         '         break',
         '      # check if we have to get out',
         '      if _speeit_prefix__perf_counter() - _speeit_prefix__main_start_time >= _speeit_prefix__run_sec:',
         '         break',
         '   _speeit_prefix__avg_loop_sec = _speeit_prefix__all_loops_time_sec / _speeit_prefix__loops',
         '   if _speeit_prefix__second_best_loop_sec == 99999999999.0:',
         '      _speeit_prefix__second_best_loop_sec = -1.0',
         '   if _speeit_prefix__second_worst_loop_sec == 0.0:',
         '      _speeit_prefix__second_worst_loop_sec = -1.0',
         '   return {',
         '      "loops": _speeit_prefix__loops,',
         '      "all_loops_time_sec": _speeit_prefix__all_loops_time_sec,',
         '      "avg_loop_sec": _speeit_prefix__avg_loop_sec,',
         '      "best_loop_sec": _speeit_prefix__best_loop_sec,',
         '      "second_best_loop_sec": _speeit_prefix__second_best_loop_sec,',
         '      "worst_loop_sec": _speeit_prefix__worst_loop_sec,',
         '      "second_worst_loop_sec": _speeit_prefix__second_worst_loop_sec',
         '   }',
         ''
      ]
      final_inner_function_lines.extend(inner_function_lines_rest)

      return '\n'.join(final_inner_function_lines)


def speedit_benchmark(func_dict, setup_line_list, use_func_name=True, output_in_sec=False, benchmarkit__with_gc=False, benchmarkit__check_too_fast=True, benchmarkit__rank_by='best', benchmarkit__run_sec=1, benchmarkit__repeat=3):
   """ Returns one txt string for the ready comparison table: format is conform with reStructuredText

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

      benchmark_result = BenchmarkIT.speedit_benchmark(func_dict, setup_line_list, benchmarkit__run_sec=1.0, output_in_sec=True, use_func_name=True, benchmarkit__with_gc=False, benchmarkit__repeat=3)

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

      benchmarkit__with_gc (bool): if True gc is kept on during timing: if False: turns off garbage collection during the timing

      benchmarkit__check_too_fast(bool): if True and aa code block is timed faster than a `Reference-Time` an Exception is raised.

         - Reference-Time: the smallest difference of calling perf_counter() immediately after each other a couple of times

         .. seealso:: _helper_get_perf_counter_reference_time()

      benchmarkit__rank_by (str): `best` or `average`

      benchmarkit__run_sec (float or -1 or None): the number of loops per run is scaled to approximately fit the benchmarkit__run_sec

            - if benchmarkit__run_sec is -1: then the generated function source code is only run once

            - if benchmarkit__run_sec is None:  then the generated function source code is only printed
               this is mainly useful to see the exact final `func code block` which will be timed.

      benchmarkit__repeat (int): how often everything is repeated
         This is a convenience variable that calls the whole setup repeatedly

   Returns:
      str: ready to print or write to file: table format is conform with reStructuredText

   Raises:
      SpeedIT.Err
   """
   if not func_dict:
      raise Err('speedit_benchmark()', 'At least one function must be defined in `func_dict`: <{}>'.format(func_dict))
   if benchmarkit__rank_by != 'best' and benchmarkit__rank_by != 'average':
      raise Err('speedit_benchmark()', '<benchmarkit__rank_by> must be one of: <best, average> We got: <{}>'.format(benchmarkit__rank_by))
   if benchmarkit__repeat < 1:
      raise Err('speedit_benchmark()', '<benchmarkit__repeat> must be greater than <0> We got: <{}>'.format(benchmarkit__repeat))


   all_final_lines = []

   # get once the perf_counter_reference_time
   perf_counter_reference_time = _helper_get_perf_counter_reference_time()

   if benchmarkit__run_sec is None:
      all_final_lines.extend([
         '================ RUN SECONDS:  benchmarkit__run_sec was defined as: None  (benchmarkit__run_sec=None) ================',
         '',
         ''
      ])
      # Run all only once and get the code
      for func_name, (function_, func_positional_arguments, func_keyword_arguments) in sorted(func_dict.items()):
         if use_func_name:
            name = getattr(function_, "__name__", function_)
         else:
            name = func_name
         benchmark_result = _TimeIT(function_, func_positional_arguments, func_keyword_arguments, setup_line_list, benchmarkit__check_too_fast, benchmarkit__run_sec, name, perf_counter_reference_time).benchmark_it(benchmarkit__with_gc)
         all_final_lines.extend([
            '===================== function name: <{}>'.format(func_name),
            '',
            benchmark_result,
            '',
            '',
         ])
   else:
      title_line = 'SpeedIT: `BenchmarkIT`  for: <{}> functions. benchmarkit__with_gc: <{}> benchmarkit__run_sec: <{}> '.format(len(func_dict), benchmarkit__with_gc, benchmarkit__run_sec)

      for repeat_all in range(benchmarkit__repeat):
         table = []
         for func_name, (function_, func_positional_arguments, func_keyword_arguments) in sorted(func_dict.items()):
            if use_func_name:
               name = getattr(function_, "__name__", function_)
            else:
               name = func_name
            benchmark_result = _TimeIT(function_, func_positional_arguments, func_keyword_arguments, setup_line_list, benchmarkit__check_too_fast, benchmarkit__run_sec, name, perf_counter_reference_time).benchmark_it(with_gc=benchmarkit__with_gc)
            table.append(benchmark_result)

         if benchmarkit__rank_by == 'best':
            table = sorted(table, key=itemgetter('best_loop_sec'))
            compare_reference = table[0]['best_loop_sec']
            for idx, dict_ in enumerate(table):
               dict_['compare'] = '{:,.3f}'.format((dict_['best_loop_sec'] / compare_reference) * 100.0)
               dict_['rank'] = '{:,}'.format(idx + 1)
               dict_['loops'] = '{:,}'.format(dict_['loops'])
               if output_in_sec:
                  dict_['avg_loop_sec'] = '{:.11f}'.format(dict_['avg_loop_sec'])
                  dict_['best_loop_sec'] = '{:.11f}'.format(dict_['best_loop_sec'])
                  if dict_['second_best_loop_sec'] == -1.0:
                     dict_['second_best_loop_sec'] = 'NOT-MEASURED'
                  else:
                     dict_['second_best_loop_sec'] = '{:.11f}'.format(dict_['second_best_loop_sec'])
                  dict_['worst_loop_sec'] = '{:.11f}'.format(dict_['worst_loop_sec'])
                  if dict_['second_worst_loop_sec'] == -1.0:
                     dict_['second_worst_loop_sec'] = 'NOT-MEASURED'
                  else:
                     dict_['second_worst_loop_sec'] = '{:.11f}'.format(dict_['second_worst_loop_sec'])
                  dict_['all_loops_time_sec'] = '{:.11f}'.format(dict_['all_loops_time_sec'])
               else:
                  dict_['avg_loop_sec'] = format_time(dict_['avg_loop_sec'])
                  dict_['best_loop_sec'] = format_time(dict_['best_loop_sec'])
                  dict_['second_best_loop_sec'] = format_time(dict_['second_best_loop_sec'])
                  dict_['worst_loop_sec'] = format_time(dict_['worst_loop_sec'])
                  dict_['second_worst_loop_sec'] = format_time(dict_['second_worst_loop_sec'])
                  dict_['all_loops_time_sec'] = format_time(dict_['all_loops_time_sec'])
         elif benchmarkit__rank_by == 'average':
            table = sorted(table, key=itemgetter('avg_loop_sec'))
            compare_reference = table[0]['avg_loop_sec']
            for idx, dict_ in enumerate(table):
               dict_['compare'] = '{:,.3f}'.format((dict_['avg_loop_sec'] / compare_reference) * 100.0)
               dict_['rank'] = '{:,}'.format(idx + 1)
               dict_['loops'] = '{:,}'.format(dict_['loops'])
               if output_in_sec:
                  dict_['avg_loop_sec'] = '{:.11f}'.format(dict_['avg_loop_sec'])
                  dict_['best_loop_sec'] = '{:.11f}'.format(dict_['best_loop_sec'])
                  if dict_['second_best_loop_sec'] == -1.0:
                     dict_['second_best_loop_sec'] = 'NOT-MEASURED'
                  else:
                     dict_['second_best_loop_sec'] = '{:.11f}'.format(dict_['second_best_loop_sec'])
                  dict_['worst_loop_sec'] = '{:.11f}'.format(dict_['worst_loop_sec'])
                  if dict_['second_worst_loop_sec'] == -1.0:
                     dict_['second_worst_loop_sec'] = 'NOT-MEASURED'
                  else:
                     dict_['second_worst_loop_sec'] = '{:.11f}'.format(dict_['second_worst_loop_sec'])
                  dict_['all_loops_time_sec'] = '{:.11f}'.format(dict_['all_loops_time_sec'])
               else:
                  dict_['avg_loop_sec'] = format_time(dict_['avg_loop_sec'])
                  dict_['best_loop_sec'] = format_time(dict_['best_loop_sec'])
                  dict_['second_best_loop_sec'] = format_time(dict_['second_best_loop_sec'])
                  dict_['worst_loop_sec'] = format_time(dict_['worst_loop_sec'])
                  dict_['second_worst_loop_sec'] = format_time(dict_['second_worst_loop_sec'])
                  dict_['all_loops_time_sec'] = format_time(dict_['all_loops_time_sec'])

         header_mapping = [
            ('name', 'name'),
            ('rank-{}'.format(benchmarkit__rank_by), 'rank'),
            ('compare %', 'compare'),
            ('num. loops', 'loops'),
            ('avg_loop', 'avg_loop_sec'),
            ('best_loop', 'best_loop_sec'),
            ('second_best_loop', 'second_best_loop_sec'),
            ('worst_loop', 'worst_loop_sec'),
            ('second_worst_loop', 'second_worst_loop_sec'),
            ('all_loops time', 'all_loops_time_sec')
         ]

         all_final_lines.extend(get_table_rst_formatted_lines(table, header_mapping, title_line))
         all_final_lines.extend([
            '',
            '',
         ])

   return '\n'.join(all_final_lines)
