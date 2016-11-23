#!/usr/bin/env python3

#######################################################################
# script to convert gm grammar file to well formed sw
# it's sequences and classes all the way down
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-11-21
# Update: 2016-11-22
# Copyright: GPLv3
#
# Usage: ./gm2sw.py source-file.gm
#
# Bah! Ugly code for now. But it seems to work.
# maybe eventually implement in parsley?
#
#######################################################################


import sys
from collections import OrderedDict

size = 2048
#size = 65536
bits = 10
column_size = 10

filename = sys.argv[1]

def process_class(s):
  s = s.strip()
  try:
    if s[0] != '{' or s[-1] != '}':
      return None
    elements = s[1:-1].split(',')
    return [x.strip() for x in elements]
  except:
    return None

def process_sequence(s):
  s = s.strip()
  try:
    elements = s.split('.')
    return [x.strip() for x in elements]
  except:
    return None

def build_dictionary(filename):
  class_dict = OrderedDict()
  sequence_dict = OrderedDict()

  with open(filename, 'r') as f:
    for line in f:
      line = line.strip()
      if len(line) > 0:
        try:
          head, tail = line.split(' = ')
          r = process_class(tail)
          if r is not None:                                 # class found
            class_dict[head] = r
          else:                                             # sequence found
            r = process_sequence(tail)
            sequence_dict[head] = r
        except:
          continue
  return class_dict, sequence_dict

class_dict, sequence_dict = build_dictionary(filename)

words = OrderedDict()
for key,value in class_dict.items():
  for seq in value:
    for x in process_sequence(seq):
      if x != '{}' and x not in class_dict and x not in sequence_dict:
        words[x] = True

#print("class:", class_dict)
#print("words:", words)
#print("sequence:", sequence_dict)
#print()

def encode_sequence(node, sequence, name = None):
  if name is not None:
    print("-- %s = %s" % (name, ".".join(sequence)))
  else:
    print("-- %s" % " . ".join(sequence))

  for k,element in enumerate(sequence):
    if k == 0:
#      print("sequence-name |node %s: *> => |%s>" % (node, name))
      print("pattern |node %s: %s> => random-column[%s] encode |%s>" % (node, k, column_size, sequence[k]))

      if len(sequence) > 1:
        print("then |node %s: %s> => random-column[%s] encode |%s>\n" % (node, k, column_size, sequence[k+1]))
      else:
        print("then |node %s: %s> => random-column[%s] encode |end of sequence>\n" % (node, k, column_size))
        break
    else:
      print("pattern |node %s: %s> => then |node %s: %s>" % (node, k, node, k-1))
      print("then |node %s: %s> => random-column[%s] encode |%s>\n" % (node, k, column_size, sequence[k+1]))
    if k + 2 >= len(sequence):
      print("pattern |node %s: %s> => then |node %s: %s>" % (node, k+1, node, k))
      print("then |node %s: %s> => random-column[%s] encode |end of sequence>\n" % (node, k+1, column_size))
      break

def old_define_class(name, the_class, node_table):
  print("-- %s = {%s}" % (name, ", ".join(the_class)))
  for k, seq in enumerate(the_class):
    print("start-node |%s: %s> => pattern |node %s: 0>" % (name, k, node_table[seq]))
  print()

def define_class(name, the_class, node_table):
  print("-- %s = {%s}" % (name, ", ".join(the_class)))
#  print("start-nodes |%s> => |%s>" % (name, "> + |".join(node_table)))
  for seq in the_class:
    print("start-nodes |%s> +=> |node %s: 0>" % (name, node_table[seq]))
  print()



# first, the encode step, starting with full range, and end-of-sequence:
print("full |range> => range(|1>,|%s>)" % size)
print("encode |end of sequence> => pick[%s] full |range>\n" % bits )

print("-- encode words:")
for w in words:
  print("encode |%s> => pick[%s] full |range>" % (w, bits))
print()

print("-- encode classes:")
for c in class_dict:
  print("encode |%s> => pick[%s] full |range>" % (c, bits))
print()

print("-- encode sequence names:")
for s in sequence_dict:
  print("encode |%s> => pick[%s] full |range>" % (s, bits))
print()


# next the low level sequences:
print("-- encode low level sequences:")
print("-- empty sequence")
print("pattern |node 0: 0> => random-column[10] encode |end of sequence>\n")

sequences_node_table = {}
sequences_node_table['{}'] = 0                          # hard wire in the empty sequence
node = 1
for class_name, class_value in class_dict.items():
  for seq in class_value:
    if seq not in sequences_node_table:
#      if seq != '{}' and seq not in class_dict and seq not in sequence_dict:
      if seq != '{}' and seq not in sequence_dict:
        r = process_sequence(seq)
        encode_sequence(node, r)
        sequences_node_table[seq] = node
        node += 1

# next the sequences of classes:
print("\n-- encode the sequences of classes:")
for seq_name, seq_value in sequence_dict.items():
#  print("name:", seq_name)
#  print("value:", seq_value)
  encode_sequence(node, seq_value, seq_name)
  sequences_node_table[seq_name] = node
  node += 1  

#print("node table:",sequences_node_table)

# next, we label the sequences of classes:
print("\n-- label the sentences:")
for seq_name, seq_value in sequence_dict.items():
  print("sentence |%s> => |node %s: 0>" % (seq_name, sequences_node_table[seq_name]))
print()

# next, define the classes:
print("\n-- define our classes:")
for class_name, class_value in class_dict.items():
#  print("name:", class_name)
#  print("value:", class_value)
  define_class(class_name, class_value, sequences_node_table)

