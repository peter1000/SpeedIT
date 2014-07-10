.. _ProjectStyleGuide:

**************************
Project Python Style Guide
**************************

:Author: peter1000
:Github: https://github.com/peter1000

|

:Revision: `2014.06.06`

.. contents::
:depth: 3

These are general suggestions but not strict rules.

|


**Standing on the shoulders of giants**

Use proven concepts of other people and adapt them to one owns style.

- This includes previous proven concepts of coding style e.g.:

   - `Google Python Style Guide <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_ (2014.03.01)
   - `PEP 8 -- Style Guide for Python Code <http://legacy.python.org/dev/peps/pep-0008/>`_
   - `Melange PythonStyleGuide <http://code.google.com/p/soc/wiki/PythonStyleGuide>`_
   - `Khan Academy Docs PythonStyleGuide <https://sites.google.com/a/khanacademy.org/forge/for-developers/styleguide/python>`_
   - `pylearn API_coding_style <http://deeplearning.net/software/pylearn/v2_planning/API_coding_style.html>`_
   - `chromium python-style-guidelines <http://www.chromium.org/chromium-os/python-style-guidelines>`_


Python Style and Language Rules
===============================

Programs are much easier to maintain when all files have a consistent style. Here are the most important `Project Python Style` rules.


Naming
------

- **CapWords with any mixture of AllCAPS:**

   - Packages
   - Modules

- **lower_with_under:**

   - Functions
   - Instance Variables
   - Method Names
   - Function/Method Parameters
      Exception: if the Parameter name is predefined by an outside reference.
         e.g. by a config file key, dictionary key name ect..
   - Local Variables

- **CapWords:**

   - Classes
   - Exceptions

- **CAPS_WITH_UNDER:**

   - Top Level Constants: Constants are usually defined on a module level.

**Names to avoid**

- names with only 1 char

- Prepending a single underscore ``_`` is reserved to mark any name as weak "internal use" indicator (by convention).

- Prepending a double underscore ``__`` is reserved to make the variable or method 'private to its class' (using name mangling).

   - instance variable or
   - method effectively

**Exceptions TEST**
   `TEST` in any case combination may not be used for:

   - Directories
   - Files
   - Class/Methods/Function names
   - and are better avoided also for any Variable, Constant all together

   `Test` in any combination is reserved for **Tests**


+--------------------------------+------------------------------+----------------------------------------+
| **Type**                       | **Public**                   | **Internal**                           |
+--------------------------------+------------------------------+----------------------------------------+
| *Packages*                     | ``CapWords mixture AllCAPS`` |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Modules*                      | ``CapWords mixture AllCAPS`` |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Classes*                      | ``CapWords``                 |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Exceptions*                   | ``CapWords``                 |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Toplevel Constants*           | ``CAPS_WITH_UNDER``          |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Functions*                    | ``lower_with_under()``       |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Instance Variables*           | ``lower_with_under``         | ``__lower_with_under`` *(private)*     |
+--------------------------------+------------------------------+----------------------------------------+
| *Method Names*                 | ``lower_with_under()``       | ``__lower_with_under()`` *(private)*   |
| \ :sup:`\*`                    |                              |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Function/Method Parameters*   | ``lower_with_under``         |                                        |
| \ :sup:`\**`                   |                              |                                        |
+--------------------------------+------------------------------+----------------------------------------+
| *Local Variables*              | ``lower_with_under``         |                                        |
+--------------------------------+------------------------------+----------------------------------------+

:sup:`\*` Consider just using `direct access to public attributes` in preference to getters and setters, as function calls are expensive in Python, and ``property`` can be used later to turn attribute access into a function call without changing the access syntax.

:sup:`\**` Exception: if the Parameter name is predefined by an outside reference. e.g. by a config file key, dictionary key name ect..



.. note::

   Names which are expected to be imported should be very, very clear: in some cases even prefix them with the package name might be useful

   **Reason:** most of the time it is preferred to import functions, classes directly and not the module itself.

   .. seealso:: `Imports Formatting`_


Line length
-----------

**No maximum line length:** use own judgement and editors text wrapping if needed


Indentation
-----------

``3`` **spaces**


Strings
-------

- **single quote:** ``'``
   For all regular Strings (non-docstring) use only single quote  ``'``
   `REASON:` personal preference: seems to make the code cleaner

    .. note:: use for `it's` the full: `it is` and similar cases

   It is okay to use the double quote ``"`` character on a string to avoid the need to ``\`` escape within the string.

.. code-block:: python

   Yes:
      xyz = 'She said: "Take care!"'
      xyz = {'key1': 12}

.. code-block:: python

   No:
      xyz = 'She said: \'Take care!\'' (use the double quote ``"`` to avoid the need to ``\``)
      xyz = "She said: 'Take care!'"
      xyz = {"key1": 12}


- **triple double quotes:** ``"""`` for docstrings

.. code-block:: python

   Yes:
      def print_help():
         """ Prints the help info to the console
         """
         print('help')

.. code-block:: python

   No:
      def print_help():
         ''' Prints the help info to the console
         '''
         print('help')

- **Use the `format method` or for simple strings join them with `+`**

- **Use the % operator in selected cases only.**
   This is usually a bit faster than the `format method`

Use your best judgement to decide between + and % (or format) though.


- Avoid using the ``+`` and ``+=`` operators to accumulate a string within a loop.

   Since strings are immutable, this creates unnecessary temporary objects and results in quadratic rather than linear running time.

   Instead, add each substring to a list and ``''.join`` the list after the loop terminates (or, write each substring to a ``io.BytesIO`` buffer).

   .. code-block:: python

      Yes:
         items = ['<table>']
         for last_name, first_name in employee_list:
            items.append('<tr><td>{}, {}</td></tr>'.format(last_name, first_name))
            items.append('</table>')
         employee_table = ''.join(items)

   .. code-block:: python

      No:
         employee_table = '<table>'
         for last_name, first_name in employee_list:
            employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
            employee_table += '</table>'


- Use ``'''`` for multi-line strings for all non-docstring multi-line strings and use ``'`` for regular strings.
   Doc strings must use ``"""`` regardless. Note that it is often cleaner to use implicit line joining since multi-line strings do not flow with the indentation of the rest of the program:

   .. code-block:: python

      Yes:
         if item == -1:
            print('This is much nicer.\n'
            'Do it this way.\n')

   .. code-block:: python

      No:
         if item == -1:
            print('''This is pretty ugly.
      Consider each case if it is not better to use the above''')

- Option: sometimes it is better to use one long line and in the coding IDE apply line wrapping if needed.

   .. code-block:: python

      Yes:
         if item == -1:
            print('Sometimes it may be better to use one line.\nIf the whole txt needs to be read apply a line wrapper in your coding IDE.\n')


Imports Formatting
------------------

- All Imports - at the top of the file
   Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.

- In general one should never need more than one dot in the code: and it is usually preferred to import functions, classes ect.. directly

- Use **only absolute imports**: (even if the module is in the same package)

.. warning:: **Do NOT import 'whole packages'**


- **MODULES**
   one line per module

   - Use ``import x`` for importing modules.
   - Use ``from x import y`` where x is the package prefix and y is the module name with no prefix.
   - Use ``from x import y as z`` if two modules named y are to be imported or if y is an inconveniently long name.


   .. code-block:: python

      Yes:
         # Reference in code with just module name (preferred).
         from sound.effects import echo
         ...
         echo.EchoFilter(input, output, delay=0.7, atten=4)

         # Reference in code with given name
         import sound.effects.echo as sn_echo
         ...
         sn_echo.EchoFilter(input, output, delay=0.7, atten=4)

         from models.graphics import views as graphics_views
         from models.sounds import views as sounds_views

         #
         import auth_util                             # module import: importing the file auth_util.py
         import auth.oauth_credentials as  oauth_c    # module import: importing the file auth/oauth_credentials.py
         from auth import oauth_credentials           # module import: importing the file auth/oauth_credentials.py


   .. code-block:: python

      No:
         from sound import effects
         ...
         effects.echo.EchoFilter(input, output, delay=0.7, atten=4)

         import auth.oauth_credentials         # module import: importing the file auth/oauth_credentials.py ! NO: use from or add an as xx


- **CLASSES, FUNCTIONS, FIELDS/CONSTANTS**
   for multiple use parentheses around them: can be one line or multi-lines


   - Use ``import x.my_import`` where `my_import` is a: classes, functions, fields/constants.
      in rare cases where it is preferable to have also the module name

   - Use ``from x import my_import`` where `my_import` is a: classes, functions, fields/constants.

   - Use ``from x.y import my_import`` where x is the package prefix and y is the module name
                                                and `my_import` is a: classes, functions, fields/constants.

   - Use ``from x.y import my_import as z`` where `my_import` is a: classes, functions, fields/constants.
      - if two modules named `my_import` are to be imported
         - but in such case maybe consider importing the module
      - or if `my_import` is an inconveniently long name


   .. code-block:: python

      Yes:

         # in rare cases where it is preferable to have also the module name
         import sys.exit
         ...
         sys.exit('Warning: could not finish the update')

         # Reference in code by name
         from os.path import isdir
         ...
         isdir

         # multiple imports: use parentheses
         from os.path import (isdir, isfile)

         from os.path import (
            isdir,
            isfile,
            abspath
         )

         # Reference in code with given name
         from custom import very_long_function_name as my_func
         ...
         my_func(input, output, delay=0.7, atten=4)


   .. code-block:: python

      No:
         from os.path import isdir, isfile, abspath   # NO: for multiple use parentheses

         from os import (path, walk)  # NO: path is a module: each module import on a single line


**Imports should be grouped** in the following order: (blank line between each group)

- standard library imports
- related third party imports
- local application/library specific imports

- imports should be grouped by the import path

.. code-block:: python

   Yes:
      from os import path
      from os import walk
      import sys.exit            # or from sys import exit

      from pandas import (Series, DataFrame, Panel)
      from yaml import (load, dump)

      from MyFoo import bar_crazy_long_name as bar      # use `as` in such case if there is no name conflict (in own library consider using a shorter name in the first place)
      from MyFoo.bar import (baz, Quad)
      from MyFob import ar


**Absolute Imports**
   Use only absolute imports: (even if the module is in the same package)

.. code-block:: python

   Yes:
      from test.sibling import example

.. code-block:: python

   No:
      from .sibling import example


Function and Method Parameters
------------------------------

**Pass positional arguments positionally**

.. code-block:: python

   def work(voltage, state', action='go', type='Blue'):

.. code-block:: python

   Yes:
      work(120, False)
      work(120, False, action='force', type='Red')

.. code-block:: python

   No:
      work(120, False, 'force', 'Red')

**Pass keyword arguments by keyword.**
   Limit defaults to:

   - numbers
   - strings
   - boolean
   - None

   Do not use mutable objects as default values in the function or method definition.

.. code-block:: python

   Yes:
      def foo(a, b=None):
         if b is None:
            b = []
.. code-block:: python

   No:
      def foo(a, b=[]):
      ...
   No:
      def foo(a, b=time.time()):  # The time the module was loaded???
      ...
   No:
      def foo(a, b=FLAGS.my_thing):  # sys.argv has not yet been parsed...
      ...


Default Iterators and Operators
-------------------------------

Use default iterators and operators for types that support them: e.g. like:

- lists
- dictionaries
- files

The built-in types define iterator methods, too.
   Prefer these methods to methods that return lists, except that you should not mutate a container while iterating over it.

.. code-block:: python

   Yes:
      if substring in a string: ...
      for key in adict: ...
      if key not in adict: ...
      if obj in alist: ...
      for line in afile: ...
      for k, v in dict.iteritems(): ...

.. code-block:: python

   No:
      for key in adict.keys(): ...
      if not adict.has_key(key): ...
      for line in afile.readlines(): ..

Main Modules
------------

All main modules require a main method.
   Even a file meant to be used as a script should be importable and a mere import should not have the side effect of executing the script's main functionality. The main functionality should be in a main() function.

   .. code-block:: python

      if __name__ == 'main':
         main()

Main modules may optionally have a symlink without an extension that point to the .py file. In such a case all actual code should be in .py files.


Package __init__.py
-------------------

In general the `__init__.py` should be empty.

If you have code that you think every user of every function inside this directory needs to run first,
__init__.py may be appropriate, but you should also consider just creating a function that executes that code,
and running the function at the top level (that is, not indented) inside each file in your directory.
This makes it more obvious what's going on, and also makes it easier to special-case certain files if the need ever arises.

Using __init__.py to bring variables from sub-modules into the main module space totally defeats the point of having sub-modules in the first place; don’t do it.

**Exception for special cases:** example: bringing the __version__ into the main module space


True/False/None evaluations
---------------------------

Use the "implicit" false if at all possible. e.g.
   ``if foo:`` rather than ``if foo != []:``

Python evaluates certain values as false when in a boolean context.
A quick "rule of thumb" is that all "empty" values are considered false:

e.g. the following all evaluate as false in a boolean context

- 0
- None
- []
- {}
- ''


Conditions using Python booleans are easier to read and less error-prone. In most cases, they're also faster.

None
++++

- Never use ``==`` or ``!=`` to compare singletons like ``None``.
   Use ``is`` or ``is not``

- Beware of writing ``if x:`` when you really mean ``if x is not None:``
   when testing whether a variable or argument that defaults to None was set to some other value.
   The other value might be a value that's false in a boolean context!

Others
++++++

- Never compare a boolean variable to False using ``==``.
   Use ``if not x:`` instead.

- If you need to distinguish False from None then chain the expressions, such as
   ``if not x and x is not None:``.

- For sequences (strings, lists, tuples), use the fact that empty sequences are false

   .. code-block:: python

      Yes:
         if not seq:
         if seq:

         #is preferable

   .. code-block:: python

      No:
         if not len(seq):
         if len(seq):

- When handling integers, implicit false may involve more risk than benefit (i.e., accidentally handling None as 0). You may compare a value which is known to be an integer (and is not the result of len()) against the integer 0.

   .. code-block:: python

      Yes:
         if not users:
            print 'no users'

         if foo == 0:
            self.handle_zero()

         if i % 10 == 0:
            self.handle_multiple_of_ten()

   .. code-block:: python

      No:
         if len(users) == 0:
            print 'no users'

         if foo is not None and not foo:
            self.handle_zero()

         if not i % 10:
            self.handle_multiple_of_ten()


If vs. If Not evaluations
-------------------------

In general try to write ``if x == y`` instead of ``if x != y``

But use your own better judgement

.. code-block:: python

   Yes:
      if users:
         print 'users'
      else:
         raise UserError()

      if foo % 10 == 0:
         xs = 27
         xy = 58
         self.handle_multiple_of_ten()
      else:
         raise UserError()

.. code-block:: python

   No:
      if not users:
         raise UserError()
      print 'users'

      if foo % 10 != 0:
         raise UserError()
      else:
         xs = 27
         xy = 58
         self.handle_multiple_of_ten()


Blank Lines
-----------

**Use 1 Blank line**

   - as you judge appropriate within functions or methods.
   - in certain cases: between class methods (if they are very short)

**Use 2 Blank lines** between:

   - top-level definitions functions/classes
   - between class methods: except for very short once (judge individually)


Whitespace
----------

**No whitespace inside parentheses, brackets or braces**

.. code-block:: python

   Yes: spam(ham[1], {eggs: 2}, [])

.. code-block:: python

   No:  spam( ham[ 1 ], { eggs: 2 }, [ ] )

**No whitespace before a comma, semicolon, or colon. Do use whitespace after a comma, semicolon, or colon except at the end of the line**

.. code-block:: python

   Yes:
      if x == 4:
         print(x, y)
         x, y = y, x

.. code-block:: python

   No:
      if x == 4 :
         print(x , y)
         x , y = y , x

**No whitespace before the open parentheses/bracket that starts an argument list, indexing or slicing**

.. code-block:: python

   Yes: spam(1)

.. code-block:: python

   No:  spam (1)

.. code-block:: python

   Yes: dict['key'] = list[index]

.. code-block:: python

   No:  dict ['key'] = list [index]

**Surround binary operators with a single space on either side for**

- assignment (=),
- comparisons (==, <, >, !=, <>, <=, >=, in, not in, is, is not),
- and Booleans (and, or, not).

Use your better judgment for the insertion of spaces around arithmetic operators but always be consistent about whitespace on either side of a binary operator.

.. code-block:: python

   Yes: x == 1

.. code-block:: python

   No:  x<1

**Don't use spaces around the '=' sign when used to indicate a keyword argument or a default parameter value**

.. code-block:: python

   Yes: def complex(real, image=0.0): return magic(r=real, i=image)

.. code-block:: python

   No:  def complex(real, image = 0.0): return magic(r = real, i = image)

**Don't use spaces to vertically align tokens on consecutive lines**
 since it becomes a maintenance burden (applies to :, #, =, etc.):

.. code-block:: python

   Yes:
      foo = 1000  # comment
      long_name = 2  # comment that should not be aligned

      dictionary = {
         'foo': 1,
         'long_name': 2,
      }

.. code-block:: python

   No:
      foo       = 1000  # comment
      long_name = 2     # comment that should not be aligned

      dictionary = {
         'foo'      : 1,
         'long_name': 2,
      }


Semicolons
----------

**Do not use them**
   Do not terminate your lines with semi-colons and do not use semi-colons to put two commands on the same line.


Statements
----------

**Generally only one statement per line.**

However, you may put the result of a test on the same line: if it is obvious  what it does.

.. code-block:: python

   Yes:
      if foo: bar(foo)

.. code-block:: python

   No:
      if foo: bar(foo)
      else:   baz(foo)

.. code-block:: python

   Yes:
      xzy = True if foo else False


.. code-block:: python

   No:
      if foo: bar(foo)
      else:   baz(foo)

      try:               bar(foo)
      except ValueError: baz(foo)

      try:
          bar(foo)
      except ValueError: baz(foo)


|

Python docstring
================

Mainly `Follow Google docstring style <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Comments#Comments>`_


- modules, classes must have a docstring
- methods, function must have a docstring
   **Except**

   - not externally visible
   - very short
   - obvious


Functions and Methods
---------------------

As used in this section "function" applies to methods, function, and generators.

A docstring should give enough information to write a call to the function without reading the function's code. A docstring should describe the function's calling syntax and its semantics, not its implementation. For tricky code, comments alongside the code are more appropriate than using docstrings.

Certain aspects of a function should be documented in special sections, listed below. Each section begins with a heading line, which ends with a colon. Sections should be indented two spaces, except for the heading.

**Args:**
   List each parameter by name. A description should follow the name,
   and be separated by a colon and a space.
   The description should mention required type(s) and the meaning of
   the argument.

   If a function accepts \*foo (variable length argument lists) and/or
   \*\*bar (arbitrary keyword arguments), they should be listed as
   \*foo and \*\*bar.

**Returns:** (or **Yields:** for generators)
   Describe the type and semantics of the return value. If the function
   only returns None, this section is not required.

**Raises:**
   List all exceptions that are relevant to the interface.

.. code-block:: python

   def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
      """ Fetches rows from a Bigtable.

      Retrieves rows pertaining to the given keys from the Table instance
      represented by big_table.  Silly things may happen if
      other_silly_variable is not None.

      Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row to fetch.
        other_silly_variable: Another optional variable, that has a much longer name than the other args, and which does nothing.

      Returns:
        A dict mapping keys to the corresponding table row data fetched. Each row is represented as a tuple of strings. For
        example:

        {'Sega': ('Rigel VII', 'Preparer'),
        'Zim': ('Irk', 'Invader'),
        'Lor': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary, then that row was not found in the table.

      Raises:
        IOError: An error occurred accessing the bigtable.Table object.
      """
      pass


Classes
-------

Classes should have a doc string below the class definition describing the class.

**Attributes:**
   If your class has public attributes, they should be documented below the class definition in an `Attributes section`
   and follow the same formatting as a function's `Args section`.

.. code-block:: python

   class SampleClass(object):
      """ Summary of class here.

      Longer class information....
      Longer class information....

      Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
      """

      def __init__(self, likes_spam=False):
         """ Initializes SampleClass with blah."""
         self.likes_spam = likes_spam
         self.eggs = 0

      def public_method(self):
         """ Performs operation blah."""


Block and Inline Comments
-------------------------

The final place to have comments is in tricky parts of the code. If you're going to have to explain it at the next code review, you should comment it now.

- Complicated operations get a few lines of comments before the operations commence.
- Non-obvious ones get comments at the end of the line.
   To improve legibility, these comments should be at least 2 spaces away from the code.

.. code-block:: python

   # We use a weighted dictionary search to find out where i is in
   # the array.  We extrapolate position based on the largest num
   # in the array and the array size and then do binary search to
   # get the exact number.

   if i & (i-1) == 0:        # true iff i is a power of 2

- On the other hand, never describe the code. Assume the person reading the code knows Python (though not what you're trying to do) better than you do.

.. code-block:: python

   # BAD COMMENT: Now go through the b array and make sure whenever i occurs
   # the next element is i+1

|

Project Documentation Style: ReStructuredText - Sphinx Rules
============================================================

ReStructuredText Indentation
----------------------------

- Default Indentation: 3 spaces


Headings
--------

In order to write a headings, just underline it and optionally overline it too


**This convention is used:**

- PARTS: with overline
   `##`
- CHAPTERS: with overline
   `**`
- SECTIONS:
   `==`
- SUBSECTIONS:
   `--`
- SUBSUBSECTIONS:
   `++`


.. code-block:: text

   ###################
   This is a main PART
   ###################

   *****************
   This is a CHAPTER
   *****************

   This is a SECTION
   =================

   This is a SUBSECTIONS
   ---------------------

   This is a SUBSUBSECTIONS
   ++++++++++++++++++++++++


Bullet Lists
------------

Use **- (minus)** as bullet list indicator

|
|

Parting Words
-------------

TRY TO BE CONSISTENT.

But use common sense to break suggested guidelines if there are reasons to do so.
`Nothing is set in stone`

|

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
