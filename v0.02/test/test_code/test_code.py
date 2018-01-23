#!/usr/bin/env python3

#######################################################################
# code to test v0.02 the_semantic_db_code__next_gen.py
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-8-19
# Update: 23/1/2018
# Copyright: GPLv3
#
# Usage: py.test -v test_code__next_gen.py
#
#######################################################################


import sys

from the_semantic_db_code import *

context = context_list("semantic db code")

def test_empty_ket():
  x = ket()
  assert str(x) == '|>'

def test_string_ket():
  x = ket('fred')
  assert str(x) == '|fred>'

def test_string_int_ket():
  x = ket('fred',3)
  assert str(x) == '3|fred>'

def test_string_float_ket():
  x = ket('fred',3.141592)
  assert str(x) == '3.142|fred>'

def test_ket_addition():
  x = ket('fred', 3.2)
  y = ket('fred', 5)
  assert str(x + y) == '8.2|fred>'

def test_ket_addition_2():
  x = ket('fred')
  y = ket('sam',2.9)
  z = ket('hank')
  assert str(x + y + z) == '|fred> + 2.9|sam> + |hank>'

def test_ket_subtraction():
  x = ket('fred')
  y = ket('sam',2.9)
  assert str(x - y) == '|fred> + -2.9|sam>'

def test_superposition_init_sp():
  x = ket('fred')
  y = ket('sam',2.9)
  z = superposition(x + y)
  assert str(z) == '|fred> + 2.9|sam>'
  
def test_superposition_empty_ket_addition():
  x = ket()
  y = ket('fred')
  z = ket('sam')
  assert str(y + x + z) == '|fred> + |sam>'

def test_superposition_empty_ket_with_value_addition():
  x = ket('',3.1415)
  y = ket('fred')
  z = ket('sam')
  assert str(y + x + z) == '|fred> + |sam>'

