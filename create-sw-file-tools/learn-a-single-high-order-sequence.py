#!/usr/bin/env python3

#######################################################################
# learn a single high order sequence HTM style
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-09-15
# Update: 
# Copyright: GPLv3
#
# Usage: ./learn-a-single-high-order-sequence.py
#
# Example:
# sa: load truncated-alphabet.sw
# sa: recall-sequence |alphabet>
#
#######################################################################

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *
context = new_context("high order sequences")

# number of on bits:
#bits = 40
bits = 10

# total number of bits:
#total_bits = 65536
total_bits = 2048

# column size:
#column_size = 200
column_size = 10
#column_size = 5

# destination file:
destination = "sw-examples/truncated-alphabet.sw"
saved_destination = "sw-examples/truncated-alphabet--saved.sw"


# drop below threshold:
# use 0 for off
t = 0
#t = 0.01
#t = 0.1
#t = 0.05
#t = 0.3
#t = 0.5

#t2 = 0.05
t2 = 0

name = "alphabet"
sequence = "A B C D E F".split()


elements_dictionary = {}
with open(destination,'w') as f:
  f.write("full |range> => range(|1>,|%s>)\n" % total_bits)
  for element in sequence:
    if element not in elements_dictionary:
      elements_dictionary[element] = True
      print("elt:",element)
      f.write("encode |%s> => pick[%s] full |range>\n" % (element,bits))
  f.write("encode |end of sequence> => pick[%s] full |range>\n" % (bits))
  print()

  f.write("\n\n-- %s\n" % name)
  f.write("-- %s\n" % " ".join(sequence))

  node = 0
  for k,element in enumerate(sequence):
    if k == 0:
#        f.write("sequence-number |node %s: *> => |sequence-%s>\n" % (node,node))
#        f.write("pattern |node %s: %s> => append-column[%s] encode |%s>\n" % (node,k,column_size,elements[k]))
      f.write("start-node |%s> => append-column[%s] encode |%s>\n" % (name, column_size, sequence[k]))
      f.write("pattern |node %s: %s> => random-column[%s] encode |%s>\n" % (node, k, column_size, sequence[k]))
      f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
    else:
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k, node, k-1))
      f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
      print("k:",k)
    if k + 2 >= len(sequence):
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k+1, node, k))
      f.write("then |node %s: %s> => append-column[%s] encode |end of sequence>\n\n" % (node, k+1, column_size))
      break

sys.exit(0)

context.load(destination)
context.save(saved_destination,False)
