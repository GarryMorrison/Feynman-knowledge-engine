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
# Copyright: GPLv3
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


# I don't even know if I still need/use long_display().
def test_ket_long_display_value_one():
  x = ket("a b",1)
  assert x.long_display() == "a b"

def test_ket_long_display_value_float_pi():
  x = ket("pi",3.141592)
  assert x.long_display() == "3.142    pi"


def test_ket_readable_display_empty_label():
  x = ket("",5.3)
  assert x.readable_display() == ""

def test_ket_readable_display_value_one():
  x = ket("ab",1)
  assert x.readable_display() == "ab"

def test_ket_readable_display_integer():
  x = ket("x",531)
  assert x.readable_display() == "531 x"

def test_ket_readable_display_float():
  x = ket("x",3.14159265)
  assert x.readable_display() == "3.14 x"


def test_ket_transpose():
  x = ket("xyz",3.72)
  y = bra("xyz",3.72)
  assert x.transpose() == y


def test_ket_add_empty_ket_pre():
  x = ket("",5.3) + ket("xyz",3.7)
  assert x.display() == "3.7|xyz>"

def test_ket_add_empty_ket_post():
  x = ket("xyz",3.7) + ket("",3)
  assert x.display() == "3.7|xyz>"

def test_ket_add_a_a():
  x = ket("a") + ket("a",5.7) + ket("a",3)
  assert x.display() == "9.7|a>"

def test_ket_add_a_b():
  x = ket("a",2) + ket("b")
  assert x.display() == "2|a> + |b>"

def test_ket_add_a_b_type():
  x = ket("a",2) + ket("b")
  assert type(x) == superposition


def test_ket_clean_add_empty_ket_pre():
  x = ket("",5.3).clean_add(ket("xyz",3.7))
  assert x.display() == "3.7|xyz>"

def test_ket_clean_add_empty_ket_post():
  x = ket("xyz",3.7).clean_add(ket("",3))
  assert x.display() == "3.7|xyz>"

def test_ket_clean_add_a_a():
  x = ket("a",5.7).clean_add(ket("a"))
  assert x.display() == "5.7|a>"

def test_ket_clean_add_a_b():
  x = ket("a",2).clean_add(ket("b",7.2))
  assert x.display() == "2|a> + 7.2|b>"

def test_ket_clean_add_a_a_a_b():
  x = ket("a").clean_add(ket("a") + ket("a",3) + ket("b",3.1415))
  assert x.display() == "|a> + 3.142|b>"

