#!/usr/bin/env python3

#######################################################################
# learn to spell using high order sequences HTM style
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-09-16
# Update:
# Copyright: GPLv3
#
# Usage: ./learn-to-spell.py
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

dictionary = "text/745550--common-words.txt"

destination = "sw-examples/spelling-dictionary.sw"
saved_destination = "sw-examples/spelling-dictionary--saved.sw"


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

def encode_concepts(bits, sequence, elements_dictionary, f):
  for element in sequence:
    if element not in elements_dictionary:
      elements_dictionary[element] = True
      print("elt:",element)
      f.write("encode |%s> => pick[%s] full |range>\n" % (element, bits))

def encode_sequence(node, name, sequence, f):
  print("encode name:",name)
  print("encode sequence:",sequence)

  f.write("\n\n-- %s\n" % name)
  f.write("-- %s\n" % ", ".join(sequence))

  for k,element in enumerate(sequence):
    if k == 0:
      f.write("first-letter |%s> => random-column[%s] encode |%s>\n" % (name, column_size, sequence[k]))
      f.write("pattern |node %s: %s> => first-letter |%s>\n" % (node, k, name))

      if len(sequence) > 1:
        f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
      else:
        f.write("then |node %s: %s> #=> append-column[%s] encode |end of sequence>\n" % (node, k, column_size))
        break
    else:
      print("k:",k)
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k, node, k-1))
      f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node, k, column_size, sequence[k+1]))
    if k + 2 >= len(sequence):
      f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node, k+1, node, k))
      f.write("then |node %s: %s> #=> append-column[%s] encode |end of sequence>\n" % (node, k+1, column_size))
      break


with open(destination,'w') as f:
  f.write("full |range> => range(|1>,|%s>)\n" % total_bits)
  elements_dictionary = {}
  with open(dictionary,'r') as g:
    for line in g:
      word = list(line.strip())                               # should strip out '<', '|', and '>' characters
      print("line:",line)
      encode_concepts(bits, word, elements_dictionary, f)
#      break
  f.write("encode |end of sequence> => pick[%s] full |range>\n" % (bits))

  node = 0
  with open(dictionary,'r') as g:
    for line in g:
      line = line.strip()                               # should strip out '<', '|', and '>' characters
      print("line:",line)
      word = list(line)
      encode_sequence(node, line, word, f)
      node += 1

sys.exit(0)
elements_dictionary = {}
with open(destination,'w') as f:
  f.write("full |range> => range(|1>,|%s>)\n" % total_bits)
  encode_concepts(bits, sequence, elements_dictionary, f)
  encode_concepts(bits, middle_nodes, elements_dictionary, f)
  f.write("encode |end of sequence> => pick[%s] full |range>\n" % (bits))

  node = 0
  encode_sequence(node, name, middle_nodes, f)  

  for idx,sequence in enumerate(chunked_data):
    node += 1
    name = middle_nodes[idx]
    encode_sequence(node, name, sequence, f)  


sys.exit(0)

context.load(destination)
context.save(saved_destination,False)
