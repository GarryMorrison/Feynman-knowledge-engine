#!/usr/bin/env python3

#######################################################################
# learn sequences HTM style
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-07-07
# Update:
# Copyright: GPLv3
#
# Usage: ./learn-high-order-sequences.py
#
#######################################################################


# number of on bits:
bits = 40

# total number of bits:
total_bits = 65536

# column size:
column_size = 11

# destination file:
destination = "sw-examples/high-order-sequences.sw"

# drop below threshold:
# use 0 for off
#t = 0.01
#t = 0.1
#t = 0.05
t = 0.3

# data:
# maybe later load from file?
# NB: sequence elements don't have to be single letters. Anything separated by space will work fine.
#data = ["a b c d e", "A B C D E F G", "X B C Y Z x y z","one two three four five six seven"]
data = ["count one two three four five six seven","fib one one two three five eight thirteen","fact one two six twenty-four one-hundred-twenty"]

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
        f.write("pattern |node %s: %s> => append-column[%s] encode |%s>\n" % (node,k,column_size,elements[k]))
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
  name = "similar-input[encode] extract-category "
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


