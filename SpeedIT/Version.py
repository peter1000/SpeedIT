""" Version And Diverse Info

   **Module CONSTANTS:**
      __version__ `str` - the released version (last release)

      RELEASE_DATE `str` - the date of the last release

      SHORT_VERSION `str` - the main version is the: __version__ stripped of the last part: e.g. used by sphinx conf.py

      TESTED_HOST_OS `str` - Keeps track of the **HOST SYSTEM** used to develop/test

      __title__ `str` -

      __copyright__ str -

      __license__ `str` -

      __author__ `str` -
"""
__version__ = '4.0.0'
RELEASE_DATE = '2014.07.21'
SHORT_VERSION = __version__.rsplit('.', 1)[0]

TESTED_HOST_OS = 'Linux Ubuntu 13.10'

__title__ = 'SpeedIT: A Collection of: Benchmark-IT, Profile-IT, Line-Memory-Profile-IT, Disassemble-IT.'
__copyright__ = '(c) 2014 `peter1000` https://github.com/peter1000'
__license__ = 'BSD 3-clause license: Consult LICENSE.rst'
__author__ = '`peter1000` https://github.com/peter1000'
