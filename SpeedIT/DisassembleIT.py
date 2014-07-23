""" Disassemble module
"""
from dis import Bytecode
from linecache import getlines
from os import path

from SpeedIT.ProjectErr import Err
from SpeedIT.Utils import (
   get_table_rst_formatted_lines
)


def _dis_it(func):
   """ Returns a dictionary with the disassembled result

   Args:
      func (function):

   Returns:
      list: table = list_of_dictionaries
   """
   table = []

   bytecode = Bytecode(func)
   code = bytecode.codeobj
   filename = code.co_filename
   if filename.endswith(('.pyc', '.pyo')):
      filename = filename[:-1]
   if not path.exists(filename):
      raise Err('_dis_it', 'ERROR: Could not find file: {}'.format(filename))
   all_lines = getlines(filename)

   for instr in bytecode:
      temp_dict = {}
      if instr.starts_line:
         temp_dict['starts_line'] = '{}'.format(instr.starts_line)
      else:
         temp_dict['starts_line'] = ''

      temp_dict['offset'] = '{}'.format(instr.offset)
      temp_dict['opname'] = '{}'.format(instr.opname)

      if instr.arg:
         temp_dict['arg'] = '{}'.format(instr.arg)
      else:
         temp_dict['arg'] = ''

      if instr.argval:
         temp_dict['argval'] = '{}'.format(instr.argval)
      else:
         temp_dict['argval'] = ''

      temp_dict['argrepr'] = '{}'.format(instr.argrepr)
      temp_dict['is_jump_target'] = '{}'.format(instr.is_jump_target)

      if instr.starts_line:
         temp_dict['line'] = all_lines[instr.starts_line - 1].strip()
      else:
         temp_dict['line'] = ''

      table.append(temp_dict)

   return table


def speedit_disassemble(func_dict, use_func_name=True):
   """ Returns one txt string for: table format is conform with reStructuredText

   .. note:: func_positional_arguments, func_keyword_arguments of the func_dict are not actually used but are required so it works similar to all `SpeedIT` modules

   Args:
      func_dict (dict): mapping function names to functions
         value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      use_func_name (bool): if True the function name will be used in the output `name` if False the `func_dict key` will be used in the the output `name`

   Returns:
      str: ready to print or write to file: table format is conform with reStructuredText

         - starts_line: line started by this opcode (if any), otherwise None
         - offset: start index of operation within bytecode sequence
         - opname: human readable name for operation
         - arg: numeric argument to operation (if any), otherwise None
         - argval: resolved arg value (if known), otherwise same as arg
         - argrepr: human readable description of operation argument
         - is_jump_target: True if other code jumps to here, otherwise False
         - line: code line
   """
   all_final_lines = []
   for func_name, (function_, func_positional_arguments, func_keyword_arguments) in sorted(func_dict.items()):
      if use_func_name:
         name = getattr(function_, "__name__", function_)
      else:
         name = func_name

      table = _dis_it(function_)

      header_mapping = [
         ('starts_line', 'starts_line'),
         ('offset', 'offset'),
         ('opname', 'opname'),
         ('arg', 'arg'),
         ('argval', 'argval'),
         ('argrepr', 'argrepr'),
         ('is_jump_target', 'is_jump_target'),
         ('line', 'line')
      ]

      # add Title Summary
      title_line = 'SpeedIT: `DisassembleIT` name: <{}> '.format(name)

      all_final_lines.extend(get_table_rst_formatted_lines(table, header_mapping, title_line))
      all_final_lines.extend([
         '',
         '',
      ])

   return '\n'.join(all_final_lines)
