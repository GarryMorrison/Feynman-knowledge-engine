#!/usr/bin/env python3

#######################################################################
# learn chunked high order sequence HTM style
# yeah, we are learning a sequence of sequences
# not super useful yet, but it is a nice proof of concept of the idea
# the brain seems to use sequences of sequences (of sequences of sequences), so seemed interesting to implement it
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-09-15
# Update:
# Copyright: GPLv3
#
# Usage: ./learn-a-single-chunked-high-order-sequence.py
#
# Example 1:
# sa: load chunked-alphabet.sw
# sa: recall-sequence |alphabet>
# sa: recall-chunked-sequence |alphabet>
# sa: recall-sequence |alpha 1>
#
# Example 2:
# sa: load chunked-pi-sequence.sw
# sa: recall-chunked-sequence |pi>
#
#######################################################################

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *
context = new_context("chunked high order sequences")

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
#destination = "sw-examples/chunked-truncated-alphabet.sw"
#saved_destination = "sw-examples/chunked-truncated-alphabet--saved.sw"

#destination = "sw-examples/chunked-pi-sequence.sw"
#saved_destination = "sw-examples/chunked-pi-sequence--saved.sw"

destination = "sw-examples/chunked-alphabet.sw"
saved_destination = "sw-examples/chunked-alphabet--saved.sw"


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

#name = "alphabet"
#sequence = "A B C D E F G H".split()

name = "alphabet"
sequence = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

#name = "pi"
#sequence = "3 . 1 4 1 5 9 2 6 5 3 5 8 9 7 9".split()


chunk_len = 3                      # this is the length of the chunks. 3 seems like a good starting value.
chunk_name = "alpha"
chunked_data = [sequence[i:i + chunk_len] for i in range(0,len(sequence), chunk_len)]
middle_nodes = [chunk_name + " " + str(k) for k in range(len(chunked_data))]

print("chunked data:",chunked_data)
print("middle_nodes:",middle_nodes)
#sys.exit(0)

def encode_sequence(node, name, sequence, f):
  print("encode name:",name)
  print("encode sequence:",sequence)

  f.write("\n\n-- %s\n" % name)
  f.write("-- %s\n" % ", ".join(sequence))

  for k,element in enumerate(sequence):
    if k == 0:
#        f.write("sequence-number |node %s: *> => |sequence-%s>\n" % (node,node))
#        f.write("pattern |node %s: %s> => append-column[%s] encode |%s>\n" % (node,k,column_size,elements[k]))
#      f.write("start-node |%s> => append-column[%s] encode |%s>\n" % (name, column_size, sequence[k]))
#      f.write("pattern |node %s: %s> => random-column[%s] encode |%s>\n" % (node, k, column_size, sequence[k]))

      f.write("start-node |%s> => random-column[%s] encode |%s>\n" % (name, column_size, sequence[k]))
      f.write("pattern |node %s: %s> => start-node |%s>\n" % (node, k, name))

      if len(sequence) > 1:
        f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
      else:
        f.write("then |node %s: %s> => append-column[%s] encode |end of sequence>\n" % (node, k, column_size))
        break
    else:
      print("k:",k)
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k, node, k-1))
      f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
    if k + 2 >= len(sequence):
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k+1, node, k))
      f.write("then |node %s: %s> => append-column[%s] encode |end of sequence>\n" % (node, k+1, column_size))
      break


elements_dictionary = {}
with open(destination,'w') as f:
  f.write("full |range> => range(|1>,|%s>)\n" % total_bits)
  for element in sequence:
    if element not in elements_dictionary:
      elements_dictionary[element] = True
      print("elt:",element)
      f.write("encode |%s> => pick[%s] full |range>\n" % (element, bits))
  f.write("encode |end of sequence> => pick[%s] full |range>\n" % (bits))
  for element in middle_nodes:
    f.write("encode |%s> => pick[%s] full |range>\n" % (element, bits))

  node = 0
  encode_sequence(node, name, middle_nodes, f)  

  for idx,sequence in enumerate(chunked_data):
    node += 1
    name = middle_nodes[idx]
    encode_sequence(node, name, sequence, f)  


sys.exit(0)

context.load(destination)
context.save(saved_destination,False)
