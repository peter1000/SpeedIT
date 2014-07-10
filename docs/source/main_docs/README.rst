.. _README:

***************
SpeedIT: README
***************

**SpeedIT: A Collection of: Benchmark-IT, Profile-IT, Line-Memory-Profile-IT, Disassemble-IT.**

.. contents::
   :depth: 3


HTML Documentation
==================

HTML documentation of the project is hosted at: `SpeedIT-HTML documentation <http://speedit.readthedocs.org/>`_


System Requirements
===================

:ref:`RequiredSoftware`   (in  `development-source: 'docs/source/main_docs'`)


Installation
------------

1. python packages might be available from pypi: to be installed with: pip/pip3

   `pip installing packages <http://pip.readthedocs.org/en/latest/user_guide.html#installing-packages>`_

   .. code-block:: sh

      $ sudo pip3 install SpeedIT

2. or run the standard package installation from the source folder:

   .. code-block:: sh

      $ python3 setup.py install

3. or use the top-level Makefile from the `development-source: 'root folder'`: to see all options run:

   .. code-block:: sh

      $ make

4. or add the folder to the python path: see **RandomNotes**   (in `development-source: 'info folder'`)


Build the Documentation
-----------------------

MAIN plus API documentation in `development-source: 'docs folder'`

**To build: run the `development-source: top-level` Makefile**

.. code-block:: sh

   $ make docs

Resulting `html documentation` will be in:
   /docs/SpeedIT-DOCUMENTATION/html/index.html


Getting Started
===============

- Generate the documentation or read the .rst files

- Run any tests: in the `development-source: top-level` (root) project folder execute:

   .. code-block:: sh

      $ make tests

- Check out any `Examples folder`, `SpeedCheck folder`, `Tests folder`


Main Info
=========

SpeedIT is a small collection of 4 modules: BenchmarkIT, ProfileIT, LineMemoryProfileIT, DisassembleIT and additional the combined: MainCode module


BenchmarkIT
-----------

.. note:: full version of the following example is in the `development-source: Examples` folder: `ReadmeExampleBenchmarkIT.py`


.. code-block:: python

   # Import: BenchmarkIT
   from SpeedIT.BenchmarkIT import speedit_func_benchmark_list

   # get a list of text lines to iterate over and split by double colon
   source_list1 = [
      '1 Double :: is the ultimate tool for telecommuting.',
      '    _menu',
      '        _id :: file',
      '        # CommentLine starts with # and can be included',
      '        _value :: File',
      '        _popup',
      '            _menuitem',
      '                _value1 :: New',
      '                _onclick1 CreateNewDoc()',
      '                _value2 :: Open',
      '                _onclick2 :: OpenDoc()',
      '                _value3 :: Close',
      '                _onclick3 :: CloseDoc()',
      '    # CommentLine starts with # and can be included',
      '    _Help :: About',
      '    Old Version'
      '     test is not ok'
      '     https://github.com/peter1000',
   ]


- define some code to compare different approaches

.. code-block:: python

   # define some functions to compare different approaches
   def split_catch_error():
      for str_ in source_list1:
         try:
            name, txt = str_.split('::', 1)
            #print('name: ', name, ' txt: ', txt)
         except ValueError:
            pass


   def split_check_first_notfound():
      for str_ in source_list1:
         if '::' in str_:
            name, txt = str_.split('::', 1)
            #print('name: ', name, ' txt: ', txt)

- defining the BenchmarkIT: `func_dict mapping`: this defines which function is really included in the BenchmarkIT run

.. code-block:: python

   # defining the: func_dict mapping
   func_dict = {
      #  value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'split_catch_error': (split_catch_error, [], {}),
      'split_check_first_notfound': (split_check_first_notfound, [], {}),
   }


- defining the BenchmarkIT: `setup_line_list`: this is a list of strings for imports, variables ect to be setup before any of the functions runs

.. code-block:: python

   # defining any: setup_line_list
   setup_line_list = [
      'from __main__ import source_list1',
   ]

- run the BenchmarkIT:

.. code-block:: python

   # run BenchmarkIT and print the result to the terminal or write it to file
   benchmark_result = speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=1, out_put_in_sec=False, use_func_name=True)
   print(benchmark_result)

   with open('result_output/ReadmeExampleBenchmarkIT.txt', 'w') as file_:
      file_.write('\n\n ReadmeExampleBenchmarkIT.py output\n\n')
      file_.write('\n'.join(benchmark_result))


**RESULT** is a table which format is conform with reStructuredText


+--------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                      SpeedIT: `speedit_func_benchmark_list`  for: <2> functions. run_sec: <1>                                          |
+----------------------------+------+-----------+------------+----------+-----------+------------------+------------+-------------------+----------------+
|                       name | rank | compare % | num. loops | avg_loop | best_loop | second_best_loop | worst_loop | second_worst_loop | all_loops time |
+============================+======+===========+============+==========+===========+==================+============+===================+================+
| split_check_first_notfound |    1 |   100.000 |    123,421 |  7.39 us |   7.04 us |          7.08 us |   50.89 us |          37.59 us |      911.76 ms |
+----------------------------+------+-----------+------------+----------+-----------+------------------+------------+-------------------+----------------+
|          split_catch_error |    2 |   307.788 |     42,259 | 22.74 us |  21.82 us |         21.82 us |   61.33 us |          59.04 us |      960.87 ms |
+----------------------------+------+-----------+------------+----------+-----------+------------------+------------+-------------------+----------------+

*Short explanation of result:*

- compare %: takes the `avg_loop time` of the best function

   - the best of all `avg_loop time` is set as 100 % and the other test are compared to that

- loops: are the loops used

- The next five are here to get a feeling of the extremes and how accurate the results my be

   - best_loop: the fastest of all loops

   - second_best_loop: the second fastest of all loops

   - worst_loop: the slowest of all loops

   - second_worst_loop: the second slowest of all loops

   - all_loops time: is the time it took for all loops to run

   - **Example Above**

      - without the extra data one would only know that the average loop was 3 times faster if one checks first if the split item exists

      - BUT as one can see the fastest of the `split_catch_error: 21.82 us` is still more than double so fast than the slowest of the 'split_check_first_notfound: 50.89 us'


ProfileIT
---------

Uses pythons cProfiler: *most of the things are similar to what we saw above.*

.. note:: full versions example is in the `development-source: Examples` folder:  `ReadmeExampleProfileIT.py`


- run the ProfileIT:

   - in general similar to `BenchmarkIT` except the `setup_line_list` is not needed

.. code-block:: python

   # run ProfileIT and print the result to the terminal or write it to file
   profile_result = speedit_func_profile_list(func_dict, out_put_in_sec=False, use_func_name=True)
   for table in profile_result:
      print('\n\n')
      print('\n'.join(table))

   with open('result_output/Example3ProfileIT.txt', 'w') as file_:
      file_.write('\n\n Example3ProfileIT.py output\n\n')
      for table in profile_result:
         file_.write('\n\n')
         file_.write('\n'.join(table))


**RESULT** is for each function a separate table which format is conform with reStructuredText

function 1

+-------------------------------------------------------------------------------------------------------------+
| SpeedIT: `profile` name: <split_catch_error> total_calls: <17> primitive_calls: <17> total_time: <44.00 us> |
+------+-----------+-----------+-----------------+------------------------------------------------------------+
| rank | compare % | func_time | number_of_calls |                                                   func_txt |
+======+===========+===========+=================+============================================================+
|    1 |    75.000 |  33.00 us |               1 |            ReadmeExampleProfileIT.py:52(split_catch_error) |
+------+-----------+-----------+-----------------+------------------------------------------------------------+
|    2 |    25.000 |  11.00 us |              16 |                          <method 'split' of 'str' objects> |
+------+-----------+-----------+-----------------+------------------------------------------------------------+

function 2

+----------------------------------------------------------------------------------------------------------------------+
| SpeedIT: `profile` name: <split_check_first_notfound> total_calls: <10> primitive_calls: <10> total_time: <16.00 us> |
+------+-----------+-----------+-----------------+---------------------------------------------------------------------+
| rank | compare % | func_time | number_of_calls |                                                            func_txt |
+======+===========+===========+=================+=====================================================================+
|    1 |    68.750 |  11.00 us |               1 |            ReadmeExampleProfileIT.py:61(split_check_first_notfound) |
+------+-----------+-----------+-----------------+---------------------------------------------------------------------+
|    2 |    31.250 |   5.00 us |               9 |                                   <method 'split' of 'str' objects> |
+------+-----------+-----------+-----------------+---------------------------------------------------------------------+


*Short explanation of result:*

- compare %: takes the `func_time` starting with the slowest part and displays
             how many % it took based on the whole execution time


LineMemoryProfileIT
-------------------

A profiler that records the amount of memory for each line
This code is based on parts of: https://github.com/fabianp/memory_profiler


.. note:: full versions example is in the `development-source: Examples` folder: named **Example4LineMemoryProfileI.py**


DisassembleIT
-------------

Uses pythons `dis`


.. note:: full versions example is in the `development-source: Examples` folder: named **Example5DisassembleIT.py**


SpeedIT
-------

**MainCode.speed_it** function for easy combined: <BenchmarkIT, ProfileIT, LineMemoryProfileIT, DisassembleIT>


Code Examples
=============

for code examples see the files in folder: `development-source: Examples`


Getting Help
============

No help is provided. You may try to open a new `issue` at github but it is uncertain if anyone will look at it.

|
|

`SpeedIT` is distributed under the terms of the BSD 3-clause license.
Consult LICENSE.rst or http://opensource.org/licenses/BSD-3-Clause.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
