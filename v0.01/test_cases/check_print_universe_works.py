#!/usr/bin/env python3

#######################################################################
# just check my new context.print_universe() and context.print_multiverse() works.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-12-03
# Update:
# Copyright: GPLv3
#
# Usage: ./check_print_universe_works.py
#
# in testing, looks right to me!
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

# check new_context class:
context = new_context("check print universe")

context.load("../sw-examples/fred-sam-friends.sw")
context.print_universe()
print("#########################")
context.print_multiverse()

# check context_list class:
C = context_list("check print universe")

C.load("../sw-examples/fib-play.sw")
C.print_universe()
print("########################")
C.print_multiverse()
