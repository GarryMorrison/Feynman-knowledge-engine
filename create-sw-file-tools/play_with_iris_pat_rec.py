#!/usr/bin/env python3

#######################################################################
# use sample iris data for testing pattern recognition
# 150 samples, of 3 types. So 50 of each. I think pick 40, and use 10 for test cases
# url: https://archive.ics.uci.edu/ml/datasets/Iris
#
# Author: Garry Morrison
# Date: 2015-03-12
# Update:
# Copyright: GPLv3
#
# Usage:
#
# described here: http://write-up.semantic-db.org/93-fixed-supervised-learning-of-iris-classes.html
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("iris pattern recognition")

data_file = "data/iris-data/bezdekIris.data"


def learn_data(C,filename):
  k = 0
  with open(filename,'r') as f:
    for line in f:
      try:
        sepal_len,sepal_width,petal_len,petal_width,iris_class = line.strip().split(',')
        k += 1
        node = ket("node-" + str(k))
# Doh! This is a stupid way to do the superposition!
#        r = ket("sepal-length: " +  sepal_len) + ket("sepal-width: " + sepal_width) + ket("petal-length: " + petal_len) + ket("petal-width: " + petal_width)
# improved:
        r = ket("sepal-length",sepal_len) + ket("sepal-width",sepal_width) + ket("petal-length",petal_len) + ket("petal-width",petal_width)
        if ((k - 1) % 50) < 40:              # learn training data set:
          C.learn("pattern",node,r)
          C.learn("M",node,iris_class)
        else:
          C.learn("input-pattern",node,r)    # learn test cases:
      except:
        continue

learn_data(C,data_file)

# save the results:
sw_file = "sw-examples/improved-iris-pattern-recognition.sw"
save_sw(C,sw_file)

