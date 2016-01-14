#!/usr/bin/env python3

#######################################################################
# 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-01-14
# Update:
# Copyright: GPLv3
#
# Usage: ./check_list_2_sp_works.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

#context = context_list("test list_2_sp code")
context = new_context("test list_2_sp code")

# define some example lists:
list1 = [2,3,5,7,11,13]
list2 = ["cat","dog","horse","rat","mouse","lion","horse"]
list3 = ["a","b",37,2.1828,"a","fish","a",37]

# test list_2_sp code:
print(list_2_sp(list1))
print(list_2_sp(list2))
print(list_2_sp(list3))
#sys.exit(0)

# test learn code:
context.learn("list-of","small primes",list1)
context.learn("list-of","common animals",list2)
context.learn("list-of","test elements",list3)

# see what we have learnt:
context.print_universe()

