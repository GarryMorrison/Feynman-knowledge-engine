#!/usr/bin/env python3

#######################################################################
# contract the MNIST task from 60k if-then machines down to 10
# testing a hunch that this might work better
# Haven't been able to think through if better or not, so experiment is the way to go.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-08-06
# Update:
# Copyright: GPLv3
#
# Usage: ./contract-mnist-if-then-machines.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = new_context("load mnist data")
context2 = new_context("output mnist if-then machines")

# load the data:
#context.load("sw-examples/image-phi-superpositions--train-60k--using-edge-enhanced-features--k_5--t_0_4.sw")
context.load("sw-examples/image-phi-superpositions--train-60k--using-edge-enhanced-features--k_5--t_0_4--train-log-phi.sw")
context.load("sw-examples/mnist-train-labels--edge-enhanced.sw")

# define the desired operator:
op = "train-log-phi-sp"


# the node dict:
node_dict = {}

count = 0

# walk the sw file:
for x in context.relevant_kets(op):             # find all relevant kets for op

  count += 1
  sp = context.recall(op,x).ket_sort()
  label = context.recall("train-label",x).the_label()
  if label not in node_dict:
    node_dict[label] = 0
  node_dict[label] += 1
  k = node_dict[label]

  context2.learn("pattern","node: %s: %s" % (label,str(k)),sp)
  context2.learn("then","node: %s: *" % (label),label)                 # yeah, we learn this over and over, but I don't currently care.
  print("sp:",sp)
  print("label:",label)
#  print("node dict:",node_dict)

#  if count > 15:
#    break

# define norm operators, just another tweak, that might or might not help our results:
for label,value in node_dict.items():
  label = ket(label)
  value = int(value)
  context2.learn("norm",label,label.multiply(1/value))

#context2.print_universe()
context2.save("sw-examples/mnist-contracted-if-then-machines.sw")

#print("node dict:",node_dict)

