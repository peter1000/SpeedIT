.. _LongDescription:

********************
SpeedIT: Description
********************

.. rubric:: SpeedIT:
.. rubric:: A Collection of: Benchmark-IT, Profile-IT, Line-Memory-Profile-IT, Disassemble-IT.

.. contents::
   :depth: 3


HTML Documentation
==================

HTML documentation of the project is hosted at: `SpeedIT-HTML documentation <http://speedit.readthedocs.org/>`_

Or `Package Documentation <http://pythonhosted.org//SpeedIT/>`_


Main Info
=========

SpeedIT is a small collection of 4 modules: BenchmarkIT, ProfileIT, LineMemoryProfileIT, DisassembleIT and additional the combined: MainCode module


SpeedIT
-------

**MainCode.speed_it** function for easy combined: <BenchmarkIT, ProfileIT, LineMemoryProfileIT, DisassembleIT>



To use it one needs to define a couple of functions to `benchmark`


1. import speed_it
++++++++++++++++++

.. code-block:: python

   from SpeedIT.MainCode import speed_it


2. define some code to `Speed-IT`
+++++++++++++++++++++++++++++++++

.. code-block:: python

   test_value = '~/etc/mypath'

   # define SpeedIT functions
   def example_startswith():
      if test_value.startswith('~/'):
         pass

   def example_two_idx():
      if test_value[0] == '~' and test_value[1] == '/':
         pass

   def example_slice():
      if test_value[:2] == '~/':
         pass


3. define the function mapping
++++++++++++++++++++++++++++++

This is a dictionary with key(names) and a tuple per function:

- value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)

.. note::  if use_func_name=False the key(names) are used in the output if True the real function name is used

.. code-block:: python

   # defining the: func_dict mapping
   func_dict = {
      # value format: tuple (function, list_of_positional_arguments, dictionary_of_keyword_arguments)
      'startswith': (example_startswith, [], {}),
      'two_idx': (example_two_idx, [], {}),
      'slice': (example_slice, [], {}),
   }


4. define the setup_line_list
+++++++++++++++++++++++++++++

This is a list with all needed code to setup so that the functions can run: e.g. imports, global variables

.. code-block:: python

   setup_line_list = [
      'from __main__ import test_value'
   ]


5. run speed-it and write result to file
++++++++++++++++++++++++++++++++++++++++


For the available options see the API-DOC or source code

.. code-block:: python

   result = speed_it(
      func_dict,
      setup_line_list,
      enable_benchmarkit=True,
      enable_profileit=True,
      enable_linememoryprofileit=True,
      enable_disassembleit=True,
      use_func_name=False,
      output_in_sec=False,
      profileit__max_slashes_fileinfo=2,
      profileit__repeat=1,
      benchmarkit__with_gc=False,
      benchmarkit__check_too_fast=True,
      benchmarkit__rank_by='best',
      benchmarkit__run_sec=1,
      benchmarkit__repeat=3
   )

   with open('result_output/ReadmeExampleMainSpeedIT.txt', 'w') as file_:
      file_.write('\n\n ReadmeExampleMainSpeedIT.py output\n\n')
      file_.write(result)


BenchmarkIT
-----------

.. note:: full versions example is in the `development-source: Examples` folder: `Example2aBenchmarkIT.py` and `Example2bBenchmarkIT.py`

BenchmarkIT supports also timing of only selected code parts within a function using Comment lines with a START/END TAG.

.. code-block:: python

   START-TAG: # ::SPEEDIT::
   END-TAG:   # **SPEEDIT**


.. note:: adding some description after the START-TAG: # ::SPEEDIT:: can help to distinguish in some error messages

The code below will report the combined time of the code part between `# ::SPEEDIT::`  and  `# **SPEEDIT**`

   - in the case below skipping the time spent in `shuffle(data)`

.. code-block:: python

   def example_multiple_subcode_blocks():
      # ::SPEEDIT:: data
      data = dict(zip(range(1000), range(1000)))
      # **SPEEDIT**
      shuffle(data)
      # ::SPEEDIT:: sorted
      result = sorted(data.items(), key=itemgetter(1))
      del result
      # **SPEEDIT**





+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
|                           SpeedIT: `BenchmarkIT`  for: <3> functions. benchmarkit__with_gc: <False> benchmarkit__run_sec: <1>                             |
+-------------------------+-----------+-----------+------------+-----------+-----------+------------------+------------+-------------------+----------------+
|                    name | rank-best | compare % | num. loops |  avg_loop | best_loop | second_best_loop | worst_loop | second_worst_loop | all_loops time |
+=========================+===========+===========+============+===========+===========+==================+============+===================+================+
| multiple_subcode_blocks |         1 |   100.000 |        481 | 612.10 us | 604.81 us |        605.08 us |  739.61 us |         723.65 us |      294.42 ms |
+-------------------------+-----------+-----------+------------+-----------+-----------+------------------+------------+-------------------+----------------+
|   single_subcode_blocks |         2 |   236.732 |        449 |   1.58 ms |   1.43 ms |          1.44 ms |    2.98 ms |           2.97 ms |      707.21 ms |
+-------------------------+-----------+-----------+------------+-----------+-----------+------------------+------------+-------------------+----------------+
|          whole_function |         3 |   337.108 |        482 |   2.08 ms |   2.04 ms |          2.04 ms |    2.24 ms |           2.12 ms |         1.00 s |
+-------------------------+-----------+-----------+------------+-----------+-----------+------------------+------------+-------------------+----------------+


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

   - all_loops time: is the time for all loops combined: because of overhead this is often lower than the `benchmarkit__run_sec` set

      - also consider that if one times only selected code parts within a function: using START/END TAGS `all_loops` time might be much lower
         as it reports the measured time and not the total execution time


.. note:: from https://docs.python.org/3.4/library/timeit.html repeat

   It’s tempting to calculate mean and standard deviation from the result vector and report these. However, this is not very useful.
   In a typical case, the lowest value gives a lower bound for how fast your machine can run the given code snippet;
   higher values in the result vector are typically not caused by variability in Python’s speed, but by other processes interfering
   with your timing accuracy. So the min() of the result is probably the only number you should be interested in.
   After that, you should look at the entire vector and apply common sense rather than statistics.


ProfileIT
---------

Uses pythons cProfiler:

.. note:: full versions example is in the `development-source: Examples` folder:  `Example3ProfileIT.py`

**RESULT** is for each function a separate table which format is conform with reStructuredText


+--------------------------------------------------------------------------------------------------------------------------------+
| `ProfileIT` name: <example_lambda> profileit__repeat: <2> || total_calls: <8767> primitive_calls: <8767> total_time: <6.12 ms> |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
| rank | compare % | func_time | number_of_calls |                                                                      func_txt |
+======+===========+===========+=================+===============================================================================+
|    1 |    36.664 |   2.24 ms |           1,998 |                                       lib/python3.4/random.py:220(_randbelow) |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    2 |    25.740 |   1.57 ms |               2 |                                          lib/python3.4/random.py:258(shuffle) |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    3 |    20.392 |   1.25 ms |               2 |                                                      <built-in method sorted> |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    4 |     8.782 | 537.00 us |           2,761 |                            <method 'getrandbits' of '_random.Random' objects> |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    5 |     4.513 | 276.00 us |           2,000 |                                             Example3ProfileIT.py:60(<lambda>) |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    6 |     2.829 | 173.00 us |           1,998 |                                        <method 'bit_length' of 'int' objects> |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    7 |     1.063 |  65.00 us |               2 |                                       Example3ProfileIT.py:58(example_lambda) |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    8 |     0.016 |   1.00 us |               2 |                                                         <built-in method len> |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+
|    9 |     0.000 |   0.00 ns |               2 |                                            <method 'items' of 'dict' objects> |
+------+-----------+-----------+-----------------+-------------------------------------------------------------------------------+


*Short explanation of result:*

- this is a combined result for all runs specified by: profileit__repeat

- compare %: takes the `func_time` starting with the slowest part and displays
             how many % it took based on the whole execution time (100 %)


LineMemoryProfileIT
-------------------

A profiler that records the amount of memory for each line
This code is based on parts of: https://github.com/fabianp/memory_profiler


.. note:: full versions example is in the `development-source: Examples` folder: named **Example4LineMemoryProfileI.py**


DisassembleIT
-------------

Uses pythons `dis`


.. note:: full versions example is in the `development-source: Examples` folder: named **Example5DisassembleIT.py**


Code Examples
=============

for code examples see the files in folder: `development-source: Examples`


Projects using SpeedIT
======================

`projects` which make use of: **SpeedIT**

`ReOBJ <https://github.com/peter1000/ReOBJ>`_  (R(estricted) E(xtended) Objects. Simple, reasonable fast, restricted/extended python objects.)

|
|

`SpeedIT` is distributed under the terms of the BSD 3-clause license.
Consult LICENSE.rst or http://opensource.org/licenses/BSD-3-Clause.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
