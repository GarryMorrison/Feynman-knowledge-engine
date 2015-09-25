#!/usr/bin/env python3

#######################################################################
# ket class is pretty boring, but a good place to start with tests
# eg, provides a nice framework for testing the more interesting superposition class
# and after that, the fast_superposition class
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-09-25
# Update:
# Copyright: closed for now
#
# Usage: py.test -v test_ket_class.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("unit tests for the ket class")

def test_ket_length_for_empty_ket():
  x = ket("",3)
  assert len(x) == 0

def test_ket_length():
  x = ket("fish")
  assert len(x) == 1

def test_equality():
  x = ket("b",5)
  y = ket("b",5)
  assert x == y

def test_ket_iteration():
  x = ket("a",3.2)
  for y in x:
    assert y == x

def test_ket_type():
  x = ket("a",3.71)
  assert type(x) == ket

def test_ket_display_value_one():
  x = ket("a b ccc",1)
  assert x.display() == "|a b ccc>"

def test_ket_display_value_integer():
  x = ket("aa",73)
  assert x.display() == "73|aa>"

def test_ket_display_value_float_pi_round_3():
  x = ket("pi",3.141592)
  assert x.display() == "3.142|pi>"

def test_ket_display_value_float_pi_exact():
  x = ket("pi",3.141592)
  assert x.display(True) == "3.141592|pi>"

