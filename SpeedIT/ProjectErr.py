""" Project Error
"""
from SpeedIT.Version import TESTED_HOST_OS


class Err(Exception):
   """ Prints an own raised ProjectError

   Args:
     errorType (str): Error type: to specify mostly from which part the error comes: e.g. CONFIG
     info (str): text info to print as message
   """

   def __init__(self, error_type, info):
      Exception.__init__(self, error_type, info)
      self.__error_type = error_type
      self.__info = info
      self.__txt = '''

========================================================================
SpeedIT-{} ERROR:


  {}

This `SpeedIT` was tested with:
  HOST OS: {}
========================================================================

'''.format(self.__error_type, self.__info, TESTED_HOST_OS)
      print(self.__txt)
