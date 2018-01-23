#!/usr/bin/env python3

#######################################################################
# 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-10-11
# Update:
# Copyright: GPLv3
#
# Usage: py.test -v test_sigmoids.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("test sigmoids")

# hrmm... sigmoids are trivial.
# I'm not sure test cases are all that useful.
# Though testing these cases would be useful, but probably belong in ket and superposition test code:
#
# x.apply_sigmoid(clean)
# x.apply_sigmoid(threshold_filter,7)
# x.apply_sigmoid(sigmoid_in_range,3,5)
#
# BTW, this is a good test:
# sa: sigmoid-in-range[3,5] rank split |a b c d e f g h i j k l>
# 0|a> + 0|b> + 3|c> + 4|d> + 5|e> + 0|f> + 0|g> + 0|h> + 0|i> + 0|j> + 0|k> + 0|l>
#

