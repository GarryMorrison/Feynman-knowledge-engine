#!/usr/bin/env python3

#######################################################################
# convert sw files to dot format so they can be graphed with graphviz
# https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29
# http://www.graphviz.org/
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-12-02
# Update: 2015-12-03
# Copyright: GPLv3
#
# Usage: ./sw2dot.py in-file.sw [out-file.dot]
# then open file.dot with graphviz
#
# unfinished: handling more than 1 context in a file
#
#######################################################################


import sys
import os

if len(sys.argv) < 2:
  print("\nUsage: ./sw2dot.py in-file.sw [out-file.dot]\n")
  sys.exit(1)
in_file = sys.argv[1]

if len(sys.argv) == 3:
  out_file = sys.argv[2]
else:
  dest_dir = "graph-examples/"
  if not os.path.exists(dest_dir):
    print("Creating %s directory.\n" % dest_dir)
    os.makedirs(dest_dir)
  
  base = os.path.basename(in_file)
  out_file = dest_dir + base.replace('.sw','.dot')


from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("sw file to dot file")

context.load(in_file)
context.print_universe()


# open out_file:
f = open(out_file,'w')
f.write("digraph g {\n")


# now the context name:
if context.context_name() != "sw file to dot file":
  f.write("context -> context_name\n")
  f.write('context_name [label="%s"]\n' % context.context_name())  # bugs out if context_name() contains quote characters.


# walk the sw file:
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
    op_label = op.label[4:]
    arrow_type = "normal"

    sp = context.recall(op,x)
    if type(sp) == stored_rule:
      sp = ket(sp.rule)
      arrow_type = "box"

    if type(sp) == memoizing_rule:
      sp = ket(sp.rule)
      arrow_type = "tee"

    for y in sp:
      if y.label not in node_dict:
        y_node = "n" + str(k)
        node_dict[y.label] = y_node
        k += 1
      else:
        y_node = node_dict[y.label]
      f.write('%s -> %s [label="%s",arrowhead="%s"]\n' % (x_node,y_node,op_label,arrow_type))


# now write out the node labels:
for label in node_dict:
  node = node_dict[label]
  label = label.replace('"','\\"')                # escape quote characters.
  f.write('%s [label="%s"]\n' % (node,label))


# tidy up:
f.write("}\n")
f.close()
