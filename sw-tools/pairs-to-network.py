#!/usr/bin/env python3

#######################################################################
# convert list of network edges to BKO notation
# save this as a sw file, and then we can use the fast_k_classifier.py code on it.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-16
# Update:
# Copyright: GPLv3
#
# Usage: ./pairs-to-network.py 1-2,1-3,1-5,1-9,1-10,1-14,1-16,1-17,2-3,2-4,2-6,2-10,2-11,2-15,2-17
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = new_context("pairs to network")

data = sys.argv[1]
print("data:",data)

for pair in data.split(','):
  head,tail = pair.split('-')
  print("head:",head)
  print("tail:",tail)

  # learn them:
  context.add_learn("op",head,tail)
  context.add_learn("op",tail,head)

context.print_universe()

