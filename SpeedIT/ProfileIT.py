""" Profile module
"""
from operator import itemgetter
from cProfile import Profile

from SpeedIT.ProjectErr import Err
from SpeedIT.Utils import (
   get_table_rst_formatted_lines,
   format_time,
)


def profile_it(func, func_positional_arguments, func_keyword_arguments, name):
   """ Returns a dictionary with the profile result: the function runs only once.

   .. note:: excludes a couple of not relative functions/methods

      - excludes: profiler.enable()
      - exclude: profiler.disable()
      - exclude: cProfile.Profile.runcall()

   Args:
      func (function):
      func_positional_arguments (list): positional arguments for the function
      func_keyword_arguments (dict): any keyword arguments for the function
      name: the name used for the output `name` part

   Returns:
      tuple: format: (summary_dict, table): table = list_of_dictionaries (sorted profile result lines dict)
   """
   profiler = Profile()

   profiler.enable()
   profiler.runcall(func, *func_positional_arguments, **func_keyword_arguments)
   profiler.disable()

   profiler.create_stats()
   total_calls = 0
   primitive_calls = 0
   total_time = 0
   table = []
   for func_tmp, (cc, nc, tt, ct, callers) in profiler.stats.items():
      temp_dict = {}
      temp_dict['number_of_calls'] = '{:,}'.format(cc) if cc == nc else '{:,}/{:,}'.format(cc, nc)
      temp_dict['func_time'] = tt
      temp_dict['func_cumulative_time'] = ct

      if func_tmp[0] == '~':
         # exclude the profiler.enable()/disable() functions
         if '_lsprof.Profiler' in func_tmp[2]:
            continue
         else:
            temp_dict['func_txt'] = func_tmp[2]
      else:
         # exclude: cProfile.py runcall()
         if func_tmp[2] == 'runcall':
            if 'cProfile' in func_tmp[0]:
               continue
         temp_dict['func_txt'] = '{}:{}({})'.format(func_tmp[0], func_tmp[1], func_tmp[2])

      table.append(temp_dict)

      total_calls += nc
      primitive_calls += cc
      total_time += tt
      if ("jprofile", 0, "profiler") in callers:
         raise Err('ERROR NOT SURE WHAT To DO HERE: SEE pstate.py: get_top_level_stats()', func)

   summary_dict = {
      'name': name,
      'total_calls': total_calls,
      'primitive_calls': primitive_calls,
      'total_time': total_time
   }

   return summary_dict, table


def speedit_func_profile_list(func_dict, out_put_in_sec=False, use_func_name=True):
   """ Returns a list of table lines for each function in func_dict: table format is conform with reStructuredText

   Args:
      func_dict (dict): mapping function names to functions
         value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      out_put_in_sec (int): if true the output is keep in seconds if false it is transformed to:
         second         (s)
         millisecond    (ms)  One thousandth of one second
         microsecond    (µs)  One millionth of one second
         nanosecond     (ns)  One billionth of one second
      use_func_name (bool): if True the function name will be used in the output `name` if False the `func_dict key` will be used in the the output `name`

   Returns:
      list: of a list of table lines for each function in func_dict: table format is conform with reStructuredText

         - rank: starts with the part which takes the longest
         - compare: % of the total execution time
         - func_time: the total time spent in the given function (and excluding time made in calls to sub-functions)
         - number_of_calls: the number of calls
         - func_txt: provides the respective data of each function
   """
   table_list = []
   for func_name, (function_, func_positional_arguments, func_keyword_arguments) in sorted(func_dict.items()):
      if use_func_name:
         name = getattr(function_, "__name__", function_)
      else:
         name = func_name
      summary_dict, table = profile_it(function_, func_positional_arguments, func_keyword_arguments, name)

      table = sorted(table, key=itemgetter('func_time'), reverse=True)
      compare_reference = summary_dict['total_time']
      if compare_reference == 0:
         # add ranking ect...
         for idx, dict_ in enumerate(table):
            dict_['compare'] = 'TOO-FAST-NOT-MEASURED'
            dict_['rank'] = '{:,}'.format(idx + 1)
            if out_put_in_sec:
               dict_['func_time'] = '{:.11f}'.format(dict_['func_time'])
            else:
               dict_['func_time'] = format_time(dict_['func_time'])
      else:
         # add ranking ect...
         for idx, dict_ in enumerate(table):
            dict_['compare'] = '{:,.3f}'.format((dict_['func_time'] * 100.0) / compare_reference)
            dict_['rank'] = '{:,}'.format(idx + 1)
            if out_put_in_sec:
               dict_['func_time'] = '{:.11f}'.format(dict_['func_time'])
            else:
               dict_['func_time'] = format_time(dict_['func_time'])

      header_mapping = [
         ('rank', 'rank'),
         ('compare %', 'compare'),
         ('func_time', 'func_time'),
         ('number_of_calls', 'number_of_calls'),
         ('func_txt', 'func_txt')
      ]

      # add Title Summary
      if out_put_in_sec:
         title_line = 'SpeedIT: `ProfileIT` name: <{}> total_calls: <{}> primitive_calls: <{}> total_time: <{:.11f}>'.format(summary_dict['name'], summary_dict['total_calls'], summary_dict['primitive_calls'], summary_dict['total_time'])
      else:
         title_line = 'SpeedIT: `ProfileIT` name: <{}> total_calls: <{}> primitive_calls: <{}> total_time: <{}>'.format(summary_dict['name'], summary_dict['total_calls'], summary_dict['primitive_calls'], format_time(summary_dict['total_time']))

      table_list.append(get_table_rst_formatted_lines(table, header_mapping, title_line))

   return table_list