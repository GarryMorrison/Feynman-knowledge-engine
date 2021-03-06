#!/usr/bin/env python3

#######################################################################
# test bra class
# 
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-10-18
# Update:
# Copyright: GPLv3
#
# Usage: py.test -v test_bra_class.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = new_context("unit tests for the bra class")


def test_bra_length_for_empty_bra():
  x = bra("",3)
  assert len(x) == 0

def test_bra_length():
  x = bra("fish")
  assert len(x) == 1


def test_equality():
  x = bra("b",5)
  y = bra("b",5)
  assert x == y


def test_bra_iteration():
  x = bra("a",3.2)
  for y in x:
    assert y == x


def test_bra_type():
  x = bra("a",3.71)
  assert type(x) == bra


def test_bra_display_empty():
  x = bra("",3.141592)
  assert x.display() == "3.142|>"

def test_bra_display_value_one():
  x = bra("a b ccc",1)
  assert x.display() == "<a b ccc|"






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




def test_bra_add_empty_empty():
  x = bra("",3) + bra("",0) + bra("",9)
  assert x.display() == "<|"

def test_bra_add_empty_empty_type():
  x = bra("",3) + bra("",0) + bra("",9)
  assert type(x) == bra_superposition

def test_bra_add_empty_pre():
  x = bra("",5.3) + bra("xyz",3.7)
  assert x.display() == "3.7|xyz>"

def test_bra_add_empty_post():
  x = bra("xyz",3.7) + bra("",3)
  assert x.display() == "3.7|xyz>"

def test_bra_add_a_a():
  x = bra("a") + bra("a",5.7) + bra("a",3)
  assert x.display() == "9.7|a>"

def test_bra_add_a_b():
  x = bra("a",2) + bra("b")
  assert x.display() == "2|a> + |b>"

def test_bra_add_a_b_type():
  x = bra("a",2) + bra("b")
  assert type(x) == bra_superposition




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


def test_ket_apply_bra():
  x = ket("a: b",3.2)
  assert x.apply_bra() == ""    # don't currently know what it should be


def test_ket_self_similar_op():
  context.load("../sw-examples/simple-shopping-basket.sw")
  result = ket("f").self_similar(context,"basket").multiply(100)
  assert result.display() == "100.0|f> + 50.0|user 2> + 16.667|user 1> + 8.333|user 4>"  # hrmm... what happened to float-to-int? Why 100.0?

def test_ket_similar_op():
  context.load("../sw-examples/simple-shopping-basket.sw")
  result = ket("f").similar(context,"basket").multiply(100)
  assert result.display() == "50.0|user 2> + 16.667|user 1> + 8.333|user 4>"


def test_ket_top_0():
  x = ket("a",3.7).top(0)
  assert x.display() == "0|>"

def test_ket_top_3():
  x = ket("a",3.7).top(3)
  assert x.display() == "3.7|a>"


def test_ket_pick_elt():
  x = ket("a",3.72).pick_elt()
  assert x.display() == "3.72|a>"

def test_ket_weighted_pick_elt():
  x = ket("a",3.72).weighted_pick_elt()
  assert x.display() == "3.72|a>"


def test_ket_is_not_empty_no():
  x = ket("",3).is_not_empty()
  assert x.display() == "|no>"

def test_ket_is_not_empty_yes():
  x = ket("x",3).is_not_empty()
  assert x.display() == "|yes>"


