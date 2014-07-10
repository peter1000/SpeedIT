.. _RandomNotes:

************
Random Notes
************

:Author: peter1000
:Github: https://github.com/peter1000

.. contents::
:depth: 2


Adding A Project To The Python Path
===================================

If the `Project` is not installed in your python search path you may want to add it

   one way is to put a `PyProjects.pth` in the search path: e.g.

   .. code-block:: python

      >>> import sys
      >>> sys.path
      ['', '/usr/local/lib/python3.4/site-packages/pyenchant-1.6.5-py3.4.egg',
      '/usr/local/lib/python3.4/site-packages/Sphinx-1.3a0dev_20140326-py3.4.egg',
      '/usr/local/lib/python3.4/site-packages/snowballstemmer-1.1.0-py3.4.egg',
      '/usr/local/lib/python34.zip', '/usr/local/lib/python3.4',
      '/usr/local/lib/python3.4/plat-linux',
      '/usr/local/lib/python3.4/lib-dynload',
      '/usr/local/lib/python3.4/site-packages']
      >>>


   taken from setuptools `easy-install.pth`

   e.g. adding a file:  `PyProjects.pth` to e.g. /usr/local/lib/python3.4/site-packages

   .. code-block:: python

      import sys; sys.__plen = len(sys.path)
      /path/to/project1
      /path/to/project2
      import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)

|

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
