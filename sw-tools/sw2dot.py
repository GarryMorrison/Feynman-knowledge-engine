#!/usr/bin/env python3

#######################################################################
# convert sw files to dot format so they can be graphed with graphviz
# http://www.graphviz.org/
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-12-02
# Update:
# Copyright: GPLv3
#
# Usage: ./sw2dot.py in-file.sw out-file.dot
# then open file.dot with graphviz
#
# unfinished: handling more than 1 context in a file
#
#######################################################################


import sys

if len(sys.argv) < 3:
  print("\nUsage: ./sw2dot.py in-file.sw out-file.dot\n")
  sys.exit(1)
in_file = sys.argv[1]
out_file = sys.argv[2]

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("sw file to dot file")

context.load(in_file)
print(context.dump_universe())

f = open(out_file,'w')
f.write("digraph g {\n")

node_dict = {}
k = 0
for x in context.relevant_kets("*"):
  if x.label not in node_dict:
    x_node = "n" + str(k)
    node_dict[x.label] = x_node
    k += 1
  else:
    x_node = node_dict[x.label]
    
  for op in context.recall("supported-ops",x):
    op_label = 'label="' + op.label[4:] + '"'
    arrow_type = ',arrowhead="normal"'

    sp = context.recall(op,x)
    if type(sp) == stored_rule:
      sp = ket(sp.rule)
      arrow_type = ',arrowhead="box"'

    if type(sp) == memoizing_rule:
      sp = ket(sp.rule)
      arrow_type = ',arrowhead="tee"'

    for y in sp:
      if y.label not in node_dict:
        y_node = "n" + str(k)
        node_dict[y.label] = y_node
        k += 1
      else:
        y_node = node_dict[y.label]
      f.write(x_node + " -> " + y_node + ' [' + op_label + arrow_type + ']\n')

# now write out the node labels:
for label in node_dict:
  node = node_dict[label]
  label = label.replace('"','\\"')
  f.write(node + ' [label="' + label + '"]' + '\n')

f.write("}\n")
f.close()
