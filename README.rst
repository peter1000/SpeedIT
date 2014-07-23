.. _LongDescription:

********************
SpeedIT: Description
********************

.. rubric:: SpeedIT:
.. rubric:: A Collection of: Benchmark-IT, Profile-IT, Line-Memory-Profile-IT, Disassemble-IT.

.. note:: `SpeedIT as of version 4.0 (20140721)` is not backwards compatible

.. contents::
   :depth: 3


HTML Documentation
==================

HTML documentation of the project is hosted at: `SpeedIT-HTML documentation <http://speedit.readthedocs.org/>`_

Or `Package Documentation <http://pythonhosted.org//SpeedIT/>`_


Main Info
=========

SpeedIT is a small collection of 4 modules: BenchmarkIT, ProfileIT, LineMemoryProfileIT, DisassembleIT and additional the combined: MainCode module


BenchmarkIT
-----------

.. note:: full version of the following example is in the `development-source: Examples` folder: `ReadmeExampleBenchmarkIT.py`


.. code-block:: python

   # Import: BenchmarkIT
   from SpeedIT.BenchmarkIT import speedit_benchmark

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

   with open('result_output/ReadmeExampleBenchmarkIT.txt', 'w') as file_:
      file_.write('\n\n ReadmeExampleBenchmarkIT.py output\n\n')
      file_.write(speedit_benchmark(func_dict, setup_line_list, use_func_name=True, output_in_sec=False, with_gc=False, rank_by='best', run_sec=1, repeat=2))

**RESULT** is a table which format is conform with reStructuredText


+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                           SpeedIT: `BenchmarkIT`  for: <2> functions. with_gc: <False> run_sec: <1>                                            |
+----------------------------+--------------+-----------+------------+----------+-----------+------------------+------------+-------------------+----------------+
|                       name | rank-average | compare % | num. loops | avg_loop | best_loop | second_best_loop | worst_loop | second_worst_loop | all_loops time |
+============================+==============+===========+============+==========+===========+==================+============+===================+================+
| split_check_first_notfound |            1 |   100.000 |    112,675 |  8.10 us |   7.60 us |          7.60 us |   50.05 us |          32.67 us |      912.39 ms |
+----------------------------+--------------+-----------+------------+----------+-----------+------------------+------------+-------------------+----------------+
|          split_catch_error |            2 |   275.092 |     42,877 | 22.28 us |  20.70 us |         20.81 us |   79.46 us |          52.45 us |      955.12 ms |
+----------------------------+--------------+-----------+------------+----------+-----------+------------------+------------+-------------------+----------------+



**Short explanation of result:**

- compare %: Depends on the setting for `rank_by`

   - rank_by='best': takes the function with the fastest `best_loop time` and set it as 100 % and the other test are compared to that
   - rank_by='average': takes the function with the fastest `avg_loop time` and set it as 100 % and the other test are compared to that

- loops: are the loops used

- The next five are here to get a feeling of the extremes and how accurate the results might be

   - best_loop: the fastest of all loops

   - second_best_loop: the second fastest of all loops

   - worst_loop: the slowest of all loops

   - second_worst_loop: the second slowest of all loops

   - all_loops time: is the time it took for all loops to run

   - *Example Above*

      - without the extra data one would only know that the average loop was approximately 3 times faster if one checks first if the split item exists

      - BUT as one can see the fastest of the `split_catch_error: 20.70 us` is still more nearly double so fast than the slowest of the 'split_check_first_notfound: 50.05 us'

      .. note:: from https://docs.python.org/3.4/library/timeit.html repeat

         It’s tempting to calculate mean and standard deviation from the result vector and report these. However, this is not very useful. 
         In a typical case, the lowest value gives a lower bound for how fast your machine can run the given code snippet; 
         higher values in the result vector are typically not caused by variability in Python’s speed, but by other processes interfering 
         with your timing accuracy. So the min() of the result is probably the only number you should be interested in. 
         After that, you should look at the entire vector and apply common sense rather than statistics.


ProfileIT
---------

Uses pythons cProfiler: *most of the things are similar to what we saw above.*

.. note:: full versions example is in the `development-source: Examples` folder:  `ReadmeExampleProfileIT.py`


- run the ProfileIT:

   - in general similar to `BenchmarkIT` except the `setup_line_list` is not needed

.. code-block:: python


   with open('result_output/ReadmeExampleProfileIT.txt', 'w') as file_:
      file_.write('\n\n ReadmeExampleProfileIT.py output\n\n')
      file_.write(speedit_profile(func_dict, output_in_sec=False, use_func_name=True, max_slashes_profile_info=2))


**RESULT** is for each function a separate table which format is conform with reStructuredText

function 1

+---------------------------------------------------------------------------------------------------------------+
| SpeedIT: `ProfileIT` name: <split_catch_error> total_calls: <17> primitive_calls: <17> total_time: <83.00 us> |
+------+-----------+-----------+-----------------+--------------------------------------------------------------+
| rank | compare % | func_time | number_of_calls |                                                     func_txt |
+======+===========+===========+=================+==============================================================+
|    1 |    75.904 |  63.00 us |               1 |              ReadmeExampleProfileIT.py:50(split_catch_error) |
+------+-----------+-----------+-----------------+--------------------------------------------------------------+
|    2 |    24.096 |  20.00 us |              16 |                            <method 'split' of 'str' objects> |
+------+-----------+-----------+-----------------+--------------------------------------------------------------+

function 2

+------------------------------------------------------------------------------------------------------------------------+
| SpeedIT: `ProfileIT` name: <split_check_first_notfound> total_calls: <10> primitive_calls: <10> total_time: <26.00 us> |
+------+-----------+-----------+-----------------+-----------------------------------------------------------------------+
| rank | compare % | func_time | number_of_calls |                                                              func_txt |
+======+===========+===========+=================+=======================================================================+
|    1 |    65.385 |  17.00 us |               1 |              ReadmeExampleProfileIT.py:59(split_check_first_notfound) |
+------+-----------+-----------+-----------------+-----------------------------------------------------------------------+
|    2 |    34.615 |   9.00 us |               9 |                                     <method 'split' of 'str' objects> |
+------+-----------+-----------+-----------------+-----------------------------------------------------------------------+


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


Projects using SpeedIT
======================

`projects` which make use of: **SpeedIT**

`ReOBJ <https://github.com/peter1000/ReOBJ>`_  (R(estricted) E(xtended) Objects. Simple, reasonable fast, restricted/extended python objects.)

`LCONF <https://github.com/peter1000/LCONF>`_  (L(ight) CONF(iguration): A simple human-readable data serialization format for dynamic configuration.)

|
|

`SpeedIT` is distributed under the terms of the BSD 3-clause license.
Consult LICENSE.rst or http://opensource.org/licenses/BSD-3-Clause.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
