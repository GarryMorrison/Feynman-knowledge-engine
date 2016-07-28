#!/usr/bin/env python3

#######################################################################
# learn sequences HTM style
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-07-07
# Update: 2016-7-19
# Copyright: GPLv3
#
# Usage: ./learn-high-order-sequences.py
#
#######################################################################

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *
context = new_context("high order sequences")

# number of on bits:
bits = 40
#bits = 10

# total number of bits:
total_bits = 65536
#total_bits = 2048

# column size:
#column_size = 200
column_size = 10
#column_size = 5

# destination file:
#destination = "sw-examples/double-alphabet-high-order-sequences--40.sw"
#destination = "sw-examples/four-alphabet-high-order-sequences--40.sw"
#saved_destination = "sw-examples/four-alphabet-high-order-sequences--40--saved.sw"
#destination = "sw-examples/two-alphabet-high-order-sequences--10--200.sw"
#saved_destination = "sw-examples/two-alphabet-high-order-sequences--10--200--saved.sw"
destination = "sw-examples/triangle-alphabet--40--10.sw"
saved_destination = "sw-examples/triangle-alphabet--40--10--saved.sw"



# drop below threshold:
# use 0 for off
#t = 0
t = 0.01
#t = 0.1
#t = 0.05
#t = 0.3
#t = 0.5

t2 = 0.05

# data:
# maybe later load from file?
# NB: sequence elements don't have to be single letters. Anything separated by space will work fine.
#data = ["a b c d e", "A B C D E F G", "X B C Y Z x y z","one two three four five six seven"]
#data = ["count one two three four five six seven","Fibonacci one one two three five eight thirteen","factorial one two six twenty-four one-hundred-twenty"]
#data = ["A B C","X B Y"]
#data = ["a b c d e f g h i j k l m n o p q r s t u v w x y z"]
#data = ["a b c d e f g h i j k l phi m n o p q r s t u v w x y z", "A B C D E F G H I J K L phi M N O P Q R S T U V W X Y Z"]
#data = ["a b c d e f g h i j k l phi-0 m n o p q r s t u v w x y z", "A B C D E F G H I J K L phi-5 M N O P Q R S T U V W X Y Z","phi-0 phi-1 phi-2 phi-3 phi-4 phi-5"]
#data = ["a b c d e f g h i j k l m n o p q r s t u v w x y z", "a b c d e f g h i j k l m n o p q r s t u v w x y z"]
#data = ["a b c d e f g h i j k l m n o p q r s t u v w x y z", "a b c d e f g h i j k l m n o p q r s t u v w x y z", "a b c d e f g h i j k l m n o p q r s t u v w x y z", "a b c d e f g h i j k l m n o p q r s t u v w x y z"]
data = ["a b c d e f g h i j k l m n o p q r s t u v w x y z", "a b1 c1 d1 e1 f1 g1 h1 i1 j1 k1 l1 m1 n1 o1 p1 q1 r1 s1 t1 u1 v1 w1 x1 y1 z1", "z1 b2 c2 d2 e2 f2 g2 h2 i2 j2 k2 l2 m2 n2 o2 p2 q2 r2 s2 t2 u2 v2 w2 x2 y2 z"]

elements_dictionary = {}
max_len_sequence = 0
with open(destination,'w') as f:
  f.write("full |range> => range(|1>,|%s>)\n" % total_bits)
  for sequence in data:
    elements = sequence.strip().split(' ')
    for element in elements:
      if element not in elements_dictionary:
        elements_dictionary[element] = True
        print("elt:",element)
        f.write("encode |%s> => pick[%s] full |range>\n" % (element,bits))
    if len(elements) > max_len_sequence:
      max_len_sequence = len(elements)
  print()
  for node,sequence in enumerate(data):
    f.write("\n\n-- %s\n" % sequence)
    first_element = True
    elements = sequence.strip().split(' ')
    for k,element in enumerate(elements):
      if first_element:
        f.write("sequence-number |node %s: *> => |sequence-%s>\n" % (node,node))
#        f.write("pattern |node %s: %s> => append-column[%s] encode |%s>\n" % (node,k,column_size,elements[k]))
        f.write("pattern |node %s: %s> => random-column[%s] encode |%s>\n" % (node,k,column_size,elements[k]))
        f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node,k,column_size,elements[k+1]))
        first_element = False
      else:
        f.write("pattern |node %s: %s> => then |node %s: %s>\n" % (node,k,node,k-1))
        f.write("then |node %s: %s> => random-column[%s] encode |%s>\n\n" % (node,k,column_size,elements[k+1]))
        print("k:",k)
      if k + 2 >= len(elements):
        break

  # now define some useful operators:
  print("max len sequence:",max_len_sequence)

  # the input-encode operator:
  f.write("\ninput-encode |*> #=> append-column[%s] encode |_self>\n\n" % column_size)

  # the step-k operators:
  name = "drop-below[%s] similar-input[encode] extract-category " % str(t2)
  next = "then drop-below[%s] similar-input[pattern] " % str(t)
  middle = name + next
  step_list = []
  for k in range(max_len_sequence-1):
    step = "step-%s" % str(k+1)
    step_list.append(step)
    f.write("%s |*> #=> %sinput-encode |_self>\n" % (step,middle))
    middle += next

  # the table operator:
  f.write("\nthe-table |*> #=> table[ket,%s] rel-kets[encode] |>\n" % ",".join(step_list))

  # the which-sequence operator:
  f.write("\nwhich-sequence |*> #=> sequence-number drop-below[0.5] %s similar-input[pattern] input-encode |_self>\n" % column_size)

  # the which-sequence table operator:
  f.write("\nsequence-table |*> #=> table[ket,which-sequence] rel-kets[encode] |>\n")

context.load(destination)
context.save(saved_destination,False)
