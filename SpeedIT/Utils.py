""" Diverse Helper functions
"""
from SpeedIT.ProjectErr import Err


def format_time(time_):
   """ Returns a formatted time string in the Orders of magnitude (time)

   Args:
      time_: if -1.0 return 'NOT-MEASURED''

   Returns:
      str: formatted time: Orders of magnitude (time)
         second         (s)
         millisecond    (ms)  One thousandth of one second
         microsecond    (µs)  One millionth of one second
         nanosecond     (ns)  One billionth of one second
   """
   if time_ == -1.0:
      final_time_str = 'NOT-MEASURED'
   else:
      base = 1
      for unit in ['s', 'ms', 'us']:
         if time_ >= base:
            break
         base /= 1000
      else:
         unit = 'ns'
      final_time_str = '{:.2f} {}'.format(time_ / base, unit)
   return final_time_str


def get_table_max_columns_width(table, column_mapping):
   """ Returns a list with columns width

   Args:
      table (list): of dictionaries must correspond to column_mapping
      column_mapping (list):  of tuples: mapping of final table column names to actual `table keys`

         .. code-block:: python

            column_mapping = [
               ('name', 'name'),
               ('rank', 'rank'),
               ('avg_loop_time', 'avg_loop_time_best_run'),
               ('all_runs_avg_loop', 'all_runs_avg_loop_time')
            ]

   Returns:
      list: of integers - columns widths
   """
   columns_widths = [len(name) for name, not_used in column_mapping]
   for row in table:
      for idx, (not_used, dict_item_key) in enumerate(column_mapping):
         if isinstance(row[dict_item_key], str):
            value_length = len(row[dict_item_key])
         else:
            raise Err('get_max_columns_width', 'Code-Error: table rows: values must be strings\n    Got: <{}> value: <{}>\n        row: <{}>'.format(type(row[dict_item_key]), row[dict_item_key], row))
         if columns_widths[idx] < value_length:
            columns_widths[idx] = value_length
   return columns_widths


def get_table_rst_formatted_lines(table, header_mapping, title_line=''):
   """ Returns list of table lines: format is conform with reStructuredText

   Args:
      table (list): of dictionaries keys: must correspond to header_mapping
      header_mapping (list):  of tuples: mapping of final table header names to actual `table keys`

         .. code-block:: python

            header_mapping = [
               ('name', 'name'),
               ('rank', 'rank'),
               ('avg_loop_time', 'avg_loop_time_best_run'),
               ('all_runs_avg_loop', 'all_runs_avg_loop_time')
            ]

      title_line (str): an optional string for a title line

   Returns:
      list: table lines: format is conform with reStructuredText
   """
   final_row = []
   table_max_columns_width = get_table_max_columns_width(table, header_mapping)

   if title_line:
      length_title_line = len(title_line)
      total_table_max_columns_width = len('-+-'.join(['-' * width for width in table_max_columns_width]))
      if total_table_max_columns_width > length_title_line:
         diff_ = total_table_max_columns_width - length_title_line
         if diff_ % 2 == 0:
            to_add = int(diff_ / 2)
            title_line = '{}{}{}'.format(' ' * to_add, title_line, ' ' * to_add)
         else:
            to_add = int((diff_ + 1) / 2)
            title_line = '{}{}{}'.format(' ' * (to_add - 1), title_line, ' ' * to_add)
      elif total_table_max_columns_width < length_title_line:
         last_idx = len(table_max_columns_width) - 1
         table_max_columns_width[last_idx] = table_max_columns_width[last_idx] + length_title_line - total_table_max_columns_width

      # Main Title
      final_row.append('+-{}-+'.format('-' * len(title_line)))
      final_row.append('| {} |'.format(title_line))
   # Main Table
   final_row.append('+-{}-+'.format('-+-'.join(['-' * width for width in table_max_columns_width])))
   final_row.append('| {} |'.format(' | '.join(['{:>{width}}'.format(name_, width=table_max_columns_width[column_idx]) for column_idx, (name_, column_name) in enumerate(header_mapping)])))
   final_row.append('+={}=+'.format('=+='.join(['=' * size for size in table_max_columns_width])))
   for row in table:
      final_row.append('| {} |'.format(' | '.join(['{:>{width}}'.format(row[column_name], width=table_max_columns_width[column_idx]) for column_idx, (name_, column_name) in enumerate(header_mapping)])))
      final_row.append('+-{}-+'.format('-+-'.join(['-' * width for width in table_max_columns_width])))
   return final_row
