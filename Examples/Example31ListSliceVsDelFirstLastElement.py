""" Example31ListSliceVsDelFirstLastElement.py
"""
from inspect import (
   currentframe,
   getfile
)
from os.path import (
   abspath,
   dirname,
   join
)
from sys import path as syspath


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'SpeedIT'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)

from SpeedIT.BenchmarkIT import speedit_func_benchmark_list
from SpeedIT.MainCode import speed_it


example_lconf_section_str_long = r'''___SECTION :: BaseEXAMPLE

# Comment-Line: below: Main `Key :: Value Pair`
key1value_pair :: value1
# Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
key2value_pair ::
key3value_pair :: 1234
key4value_pair :: True
key5value_pair :: False
key6value_pair :: None
key7value_pair :: 1456.984
key8value_pair :: true
key9value_pair :: long sentence with different characters # \n * | , & @  https://translate.google.com/ translate ਅਨੁਵਾਦ çevirmek 翻訳する μεταφράζω


# Comment-Line: below is a Main `Key-Value-Mapping`
key10value_mapping
   # Comment-Line:  Key-Value-Mapping items: are `Key :: Value Pairs`
   mapping10_key1 :: False
   mapping10_key2 :: true
   mapping10_key3 :: 123456

   # Comment-Line:  Key-Value-Mapping item: `Key :: Value-List`
   - mapping10_key4_list :: 1,2

   # Comment-Line:  Key-Value-Mapping item: `Key-Value-List`
   - mapping10_key5_list
      1
      2

   # Comment-Line:  Key-Value-Mapping item: `List-Of-Lists`
   - mapping10_key6_list |x|y|
      1,3
      2,6

   # Comment-Line:  Key-Value-Mapping item: `List-Of-Lists`
   - mapping10_key7_list |a|b|c|
      1,2.0,3
      2,4.0,6

# Comment-Line: below is a Main `Key-Value-Mapping`
key11value_mapping
   # Comment-Line:  Key-Value-Mapping item: `Key :: Value Pairs`
   mapping11_key1 :: null

   # Comment-Line:  Key-Value-Mapping item: an other nested `Key-Value-Mapping`
   mapping11_key2_mapping
      # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pairs`
      mapping11_key2_nested_mapping_key1 :: city

      # Comment-Line:  nested Key-Value-Mapping item: `Repeated-Block-Identifier`
      * mapping11_key2_nested_mapping_key2_block_identifier

         # Comment-Line: `Block-Name1`
         sky_blue_blk_name1
            # Comment-Line:  Block items: `Key :: Value Pairs`
            blk_item_red :: 135
            blk_item_green :: 206
            blk_item_blue :: 235

         # Comment-Line: `Block-Name2`
         lavender_blk_name2
            # Comment-Line:  Block items: `Key :: Value Pairs`
            blk_item_red :: 230
            blk_item_green :: 230
            blk_item_blue :: 250

      # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pairs`
      mapping11_key2_nested_mapping_key3 :: car

      # Comment-Line: nested Key-Value-Mapping item: `Key-Value-List`
      - mapping11_key2_nested_mapping_key4_list
         # Comment-Line: List item
         value_list_item1
         value_list_item2


# Comment-Line: below is a Main `Key-Value-List`
- key12list
   # Comment-Line: List item
   value_list_item1
   value_list_item2

# Comment-Line: below is a Main `Key :: Value-List`
- key13value_pairlist :: 123,8945,278

# Comment-Line: below is a Main `List-Of-Lists` with 4 items: |Color Name|Red|Green|Blue|
- key14list_of_color_lists |Color Name|Red|Green|Blue|
   # Comment-Line: `List-Of-Lists` item lines (rows)
   forestgreen,   34,   139,  34
   brick,         156,  102,  31

# Comment-Line: below is a Main `Key :: Value-List` with an empty list: overwriting any defaults
- key15value_pairlist ::

# Comment-Line: below is a Main `Key-Value-List` with an empty list: overwriting any defaults
- key16value_pairlist

# Comment-Line: below is a Main `List-Of-Lists` with an empty list: overwriting any defaults
- key17value_pairlist |a|b|c|


# Comment-Line: below: `Repeated-Block-Identifier`
#  this will loose the order of the `Repeated Block-Names` after parsing
#  but any library must implement an option to loop over it in order as defined in the section
* RepeatedBlk1
   # Comment-Line: BLK_OBJ1 (Block-Name) uses all 8 possible - defined items
   BLK_OBJ1

      # Comment-Line: below Block-Item `Key-Value-Mapping` with all 4 defined items
      MyKey1_mapping
         blk_mapping_key1 :: some text
         blk_mapping_key2 :: 12345.99
         blk_mapping_key3 :: True

         # Comment-Line:  Block-Item `Key-Value-Mapping`: an other nested `Key-Value-Mapping`
         blk_mapping_key4
            nested_mapping_key1 :: franz
            # Comment-Line:  Block-Item  nested `Key-Value-Mapping` item: an other nested `Key-Value-Lists`
            - interests
               sport
               reading

            # Comment-Line:  Block-Item: an other deep nested `Repeated-Block-Identifier`
            * Nested Repeated Block Identifier
               # Comment-Line:  keys do not have to be a single word: below a Block-Name
               Nested Block Name1
                  block-item_key1 :: 12345.99
                  - block-item_key2_list :: False,True,True
                  # Comment-Line:  block-item_key3_list: `List-Of-Lists`
                  - block-item_key3_list |name|height_cm|weight_kg|
                     # Comment-Line: |name|height_cm|weight_kg|
                     Tim,     178,     86
                     John,    166,   67

      MyKey2 :: 789.9
      MyKey3 :: True

      # Comment-Line:  empty `Key :: Value Pairs`
      MyKey4 ::
      - MyKey5list :: test1,test2

      # Comment-Line: Block-Item `Key :: Value-List` with Empty List
      - MyKey6list ::

      # Comment-Line: Block-Item `Key :: Value-List`
      - MyKey7list :: True,False,False,True

      MyKey8 :: some text

   # Comment-Line: BLK_OBJ2 (Block-Name) of RepeatedBlk1: uses a subset of the defined items:
   # all others will be set to default values as implemented
   #    NOTE: Blocks are only set to defaults if a Block-Name is defined
   BLK_OBJ2

      # Comment-Line: below Block-Item `Key-Value-Mapping`: only some defined items
      MyKey1_mapping
         blk_mapping_key3 :: False

         # Comment-Line:  Block-Item `Key-Value-Mapping`: an other nested `Key-Value-Mapping`
         blk_mapping_key4
            nested_mapping_key1 :: julia
            # Comment-Line:  Block-Item  nested `Key-Value-Mapping` item: an other nested `Key-Value-Lists`
            - interests
               golf

            # Comment-Line:  Block-Item: an other deep nested `Repeated-Block-Identifier`
            * Nested Repeated Block Identifier
               # Comment-Line:  Block-Name: all values will use defaults
               Nested Block Name1
               # Comment-Line:  Block-Name: and defining an empty list: block-item_key2_list
               Nested Block Name2
                  - block-item_key2_list ::
                  # Comment-Line:  block-item_key3_list: `List-Of-Lists`: defining an empty list: just skip any item lines
                  - block-item_key3_list |name|height_cm|weight_kg|

      # Comment-Line: Block-Item `Key-Value-Lists`
      - MyKey7list
         True
         False
         True

   BLK_OBJ3
      # Comment-Line: below Block-Item `Key-Value-Mapping`
      MyKey1_mapping
         blk_mapping_key1 :: who is who
         blk_mapping_key2 :: 5678.89
         blk_mapping_key3 :: False

      # Comment-Line:  `Key :: Value Pairs`
      MyKey4 ::
      - MyKey5list :: test1,test2

   # Comment-Line: Repeated Block-Name: will be using all default values
   #    Note: Blocks are not having any default names: so the items are skipped
   BLK_OBJ4

___END
'''

example_lconf_section_str_short = r'''___SECTION :: BaseEXAMPLE
# Comment-Line: below: Main `Key :: Value Pair`
key1value_pair :: value1
# Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
key2value_pair ::
___END
'''

section_lines_long = example_lconf_section_str_long.splitlines()
section_lines_short = example_lconf_section_str_short.splitlines()

def slice_it_long():
   new_list = section_lines_long.copy()
   new_list = new_list[1:-1]
   #print(new_list)

def del_it_long():
   new_list = section_lines_long.copy()
   del new_list[0]
   del new_list[-1]
   #print(new_list)

def slice_it_short():
   new_list = section_lines_short.copy()
   new_list = new_list[1:-1]
   #print(new_list)

def del_it_short():
   new_list = section_lines_short.copy()
   del new_list[0]
   del new_list[-1]
   #print(new_list)
   
#slice_it_long()
#del_it_long()
#slice_it_short()
#del_it_short()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass
   func_dict = {
      'slice_it_long': (slice_it_long, [], {}),
      'del_it_long': (del_it_long, [], {}),
      'slice_it_short': (slice_it_short, [], {}),
      'del_it_short': (del_it_short, [], {}),
   }

   setup_line_list = [
      'from __main__ import section_lines_long, section_lines_short'
   ]

   check_run_sec = 1
   with open('result_output/Example31ListSliceVsDelFirstLastElement.py.txt', 'w') as file_:
      file_.write('\n\n Example31ListSliceVsDelFirstLastElement.py output\n\n')
      for count in range(5):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')

      #speed_it_result = speed_it(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=True)
      #file_.write('\n\n')
      #file_.write(speed_it_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
