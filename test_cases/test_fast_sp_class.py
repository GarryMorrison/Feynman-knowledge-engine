#!/usr/bin/env python3

#######################################################################
# test the sp class
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-11-25
# Update:
# Copyright: GPLv3
#
# Usage: py.test -v test_fast_sp_class.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("test fast superposition class")

def test_fast_sp_len_empty():
  r = fast_superposition()
  assert len(r) == 0

def test_fast_sp_len_empty_ket_empty():
  r = fast_superposition() + ket("",3) + ket("x",0.7) + ket("",13)
  assert len(r) == 1

def test_fast_sp_define():
  r = fast_superposition() + ket("x",3) + ket("y") + ket("x",0.2) + ket("z",5.7)
  assert str(r) == '3.2|x> + |y> + 5.7|z>'

def test_fast_sp_multiply():
  r = (fast_superposition() + ket("x",3) + ket("y") + ket("x",0.2) + ket("z",5.7)).multiply(4)
  assert str(r) == '12.8|x> + 4|y> + 22.8|z>'

