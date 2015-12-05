#!/usr/bin/env python3

#######################################################################
# convert sw files to dot format so they can be graphed with graphviz
# https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29
# http://www.graphviz.org/pdf/dotguide.pdf
# http://www.graphviz.org/
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-12-02
# Update: 2015-12-03
# Copyright: GPLv3
#
# Usage: ./sw2dot-v2.py in-file.sw [out-file.dot]
# then open out-file.dot with graphviz
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
  f.write('"context" -> "%s"\n' % context.context_name())  # bugs out if context_name() contains quote characters. 


# walk the sw file:
for x in context.relevant_kets("*"):             # find all kets in the sw file
  x_node = x.label.replace('"','\\"')            # escape quote characters.
    
  for op in context.recall("supported-ops",x):   # find the supported operators for a given ket
    op_label = op.label[4:]
    arrow_type = "normal"

    sp = context.recall(op,x)                    # find the superposition for a given operator applied to the given ket
    if type(sp) == stored_rule:
      sp = ket(sp.rule)
      arrow_type = "box"

    if type(sp) == memoizing_rule:
      sp = ket(sp.rule)
      arrow_type = "tee"

    for y in sp:
      y_node = y.label.replace('"','\\"')                # escape quote characters.
      f.write('"%s" -> "%s" [label="%s",arrowhead=%s]\n' % (x_node,y_node,op_label,arrow_type))


# tidy up:
f.write("}\n")
f.close()
