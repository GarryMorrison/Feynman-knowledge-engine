#!/usr/bin/env python3

#######################################################################
# learning chunked high order sequences
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-09-25
# Update:
# Copyright: GPLv3
#
# Usage: ./learn-chunked-high-order-sequences.py
#
# Example 1:
#
# Example 2:
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


destination = "sw-examples/chunked-alphabet-pi.sw"
#saved_destination = "sw-examples/spelling-dictionary--saved.sw"


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

name1 = "alphabet"
sequence1 = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

name2 = "pi"
sequence2 = "3 . 1 4 1 5 9 2 6 5 3 5 8 9 7 9 3 2 3 8 4 6".split()

data = [[name1,sequence1],[name2,sequence2]]

chunk_len = 3                      # this is the length of the chunks. 3 seems like a good starting value.


# map concepts to encode SDR's:
def encode_concepts(bits, sequence, elements_dictionary, f):
  for element in sequence:
    if element not in elements_dictionary:
      elements_dictionary[element] = True
      print("elt:",element)
      f.write("encode |%s> => pick[%s] full |range>\n" % (element, bits))


# learn a high-order sequence:
def encode_sequence(node, name, sequence, f):
  print("encode name:",name)
  print("encode sequence:",sequence)

  f.write("\n\n-- %s\n" % name)
  f.write("-- %s\n" % ", ".join(sequence))

  for k,element in enumerate(sequence):
    if k == 0:
      f.write("start-node |%s> => random-column[%s] encode |%s>\n" % (name, column_size, sequence[k]))
      f.write("pattern |node %s: %s> => start-node |%s>\n" % (node, k, name))

      if len(sequence) > 1:
        f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
      else:
#        f.write("then |node %s: %s> #=> append-column[%s] encode |end of sequence>\n" % (node, k, column_size))
        f.write("then |node %s: %s> => append-column[%s] encode |end of sequence>\n" % (node, k, column_size))
        break
    else:
      print("k:",k)
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k, node, k-1))
      f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
    if k + 2 >= len(sequence):
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k+1, node, k))
#      f.write("then |node %s: %s> #=> append-column[%s] encode |end of sequence>\n" % (node, k+1, column_size))
      f.write("then |node %s: %s> => append-column[%s] encode |end of sequence>\n" % (node, k+1, column_size))
      break

# learn a single chunked high-order sequence:
# NB: you can't invoke it more than once without encode collisions.
# I need a clean way to solve that problem!
#
def learn_chunked_sequence(name,sequence,chunk_len,destination):
  # some pre-processing:
  chunked_data = [sequence[i:i + chunk_len] for i in range(0,len(sequence), chunk_len)]
  middle_nodes = [" ".join(x) for x in chunked_data ]

  print("chunked data:",chunked_data)
  print("middle_nodes:",middle_nodes)

  # write it to file:
  with open(destination,'w') as f:
    # first, the random SDR encode step:
    f.write("full |range> => range(|1>,|%s>)\n" % total_bits)
    elements_dictionary = {}
    encode_concepts(bits, sequence, elements_dictionary, f)
    encode_concepts(bits, middle_nodes, elements_dictionary, f)
    f.write("encode |end of sequence> => pick[%s] full |range>\n" % (bits))

    # now learn the sequences of sequences:
    node = 0
    encode_sequence(node, name, middle_nodes, f)  
    for k,sequence in enumerate(chunked_data):
      node += 1
      name = middle_nodes[k]
      encode_sequence(node, name, sequence, f)  


# learn more than one chunked high-order sequence at a time:
# NB: this has to be a little more careful than the above version
#
def learn_chunked_sequences(data,chunk_len,destination,total_bits,bits):
  # write it to file:
  with open(destination,'w') as f:
    # first, the random SDR encode step:
    elements_dictionary = {}
    f.write("full |range> => range(|1>,|%s>)\n" % total_bits)
    f.write("encode |end of sequence> => pick[%s] full |range>\n" % (bits))
    for name,seq in data:

      # some pre-processing:
      chunked_data = [seq[i:i + chunk_len] for i in range(0,len(seq), chunk_len)]
      middle_nodes = [" ".join(x) for x in chunked_data ]

      print("chunked data:",chunked_data)
      print("middle_nodes:",middle_nodes)

      encode_concepts(bits, seq, elements_dictionary, f)
      encode_concepts(bits, middle_nodes, elements_dictionary, f)

    # now learn the sequences of sequences:
    node = 0
    for name,seq in data:
      # some pre-processing:
      chunked_data = [seq[i:i + chunk_len] for i in range(0,len(seq), chunk_len)]
      middle_nodes = [" ".join(x) for x in chunked_data ]

      encode_sequence(node, name, middle_nodes, f)
      node += 1
      for k,sequence in enumerate(chunked_data):
        node_name = middle_nodes[k]
        encode_sequence(node, node_name, sequence, f)
        node += 1


#learn_chunked_sequence(name,sequence,chunk_len,destination)
learn_chunked_sequences(data,chunk_len,destination,total_bits,bits)

sys.exit(0)

# load the knowledge into memory, then save out the result:
context.load(destination)
context.save(saved_destination,False)
