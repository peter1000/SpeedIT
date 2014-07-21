""" Line memory module:
much of the code is based on: a reduced version of parts of: https://github.com/fabianp/memory_profiler
memory_profiler: License: Simplified BSD
"""
from inspect import getblock
from linecache import getlines
from os import (
   getpid,
   path
)
from sys import (
   settrace,
   gettrace
)

from psutil import Process

from SpeedIT.ProjectErr import Err
from SpeedIT.Utils import get_table_rst_formatted_lines


class LineMemoryProfiler(object):
   """ A profiler that records the amount of memory for each line

   This code is a reduced version of parts of: https://github.com/fabianp/memory_profiler
   License: Simplified BSD
   """

   def __init__(self):
      self.code_map = {}
      self.enable_count = 0
      self.max_mem = None
      self.prevline = None
      self._original_trace_function = gettrace()


   def __call__(self, func):
      """ Called when the instance is “called” as a function

      Args:
         func (function): function

      Returns:
         function: wrap_func
      """
      code = None
      try:
         code = func.__code__
      except AttributeError:
         Err('LineMemoryProfiler', 'Could not extract a code object for the object: <{!r}>'.format(func))
      if code not in self.code_map:
         self.code_map[code] = {}
      func_ = self.wrap_function(func)
      func_.__module__ = func.__module__
      func_.__name__ = func.__name__
      func_.__doc__ = func.__doc__
      func_.__dict__.update(getattr(func, '__dict__', {}))
      return func_


   def wrap_function(self, func):
      """ Wrap a function to profile it.

      Args:
         func (function): function

      Returns:
         function: wrap_func
      """

      def wrap_func(*args, **kwargs):
         """ inner wrap_func """
         if self.enable_count == 0:
            self._original_trace_function = gettrace()
            settrace(self.trace_memory_usage)
         self.enable_count += 1
         try:
            result = func(*args, **kwargs)
         finally:
            if self.enable_count > 0:
               self.enable_count -= 1
               if self.enable_count == 0:
                  settrace(self._original_trace_function)
         return result

      return wrap_func


   def trace_memory_usage(self, frame, event, arg):
      """Callback for sys.settrace

      Args:
         frame: frame is the current stack frame
         event: event is a string: 'call', 'line', 'return', 'exception', 'c_call', 'c_return', or 'c_exception'
         arg: arg depends on the event type.

      Returns:
         function: wrap_func
      """
      if event in ('call', 'line', 'return') and frame.f_code in self.code_map:
         if event != 'call':
            # "call" event just saves the lineno but not the memory
            process = Process(getpid())
            mem = process.memory_info()[0] / float(2 ** 20)
            # if there is already a measurement for that line get the max
            old_mem = self.code_map[frame.f_code].get(self.prevline, 0)
            self.code_map[frame.f_code][self.prevline] = max(mem, old_mem)
         self.prevline = frame.f_lineno

      if self._original_trace_function is not None:
         self._original_trace_function(frame, event, arg)

      return self.trace_memory_usage


def memory_profile_it(mem_profiler):
   """ Returns a dictionary with the memory profile result

   Args:
      mem_profiler (class): instance of `SpeedIT.MemIt.LineMemoryProfiler`

   Returns:
      tuple: format: (max_mem, table): table = list_of_dictionaries
   """
   memory_precision = 3
   table = []
   max_mem = 0
   for code in mem_profiler.code_map:
      lines = mem_profiler.code_map[code]
      if not lines:
         # .. measurements are empty ..
         continue
      filename = code.co_filename
      if filename.endswith(('.pyc', '.pyo')):
         filename = filename[:-1]
      if not path.exists(filename):
         print('\nmemory_profile_it() ERROR: Could not find file: {}'.format(filename))
         continue
      all_lines = getlines(filename)
      sub_lines = getblock(all_lines[code.co_firstlineno - 1:])

      mem_old = lines[min(lines.keys())]
      for line in range(code.co_firstlineno, code.co_firstlineno + len(sub_lines)):
         mem = 0.0
         mem_increment = 0.0
         if line in lines:
            mem = lines[line]
            if mem > max_mem:
               max_mem = mem
            mem_increment = mem - mem_old
            mem_old = mem
         dict_ = {
            'line_num': '{}'.format(line),
            'memory_usage': '{:.{}f} MiB'.format(mem, memory_precision),
            'increment_memory_usage': '{:.{}f} MiB'.format(mem_increment, memory_precision),
            'line': all_lines[line - 1].strip()
         }
         table.append(dict_)

   max_mem = '{:.{}f} MiB'.format(max_mem, memory_precision)
   return max_mem, table


def speedit_line_memory(func_dict, use_func_name=True):
   """ Returns one txt string for: table format is conform with reStructuredText

   Args:
      func_dict (dict): mapping function names to functions
         value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)

         .. note:: if there is a key: `loops` in the dictionary_of_keyword_arguments it will be overwritten with the value 1 to make it work with the main SpeedIT

      use_func_name (bool): if True the function name will be used in the output `name column` if False the `func_dict key` will be used in the the output `name column`

   Returns:
      str: ready to print or write to file: table format is conform with reStructuredText

         - line num: code line number
         - memory_usage: memory_usage
         - incr. memory_usage: increment_memory_usage
         - line: code line

   """
   all_final_lines = []
   header_mapping = [
      ('line num', 'line_num'),
      ('memory_usage', 'memory_usage'),
      ('incr. memory_usage', 'increment_memory_usage'),
      ('line', 'line'),
   ]

   for func_name, (function_, func_positional_arguments, func_keyword_arguments) in sorted(func_dict.items()):
      if use_func_name:
         name = getattr(function_, "__name__", function_)
      else:
         name = func_name
      profiler = LineMemoryProfiler()
      # in case we have a key: 'loops' - overwrite it with 1
      if 'loops' in func_keyword_arguments:
         func_keyword_arguments['loops'] = 1
      profiler(function_)(*func_positional_arguments, **func_keyword_arguments)
      max_mem, table = memory_profile_it(profiler)

      # add Title Summary
      title_line = 'SpeedIT: `LineMemoryProfileIT` name: <{}> max memory: <{}> '.format(name, max_mem)

      all_final_lines.extend(get_table_rst_formatted_lines(table, header_mapping, title_line))
      all_final_lines.extend([
         '',
         '',
      ])

   return '\n'.join(all_final_lines)
