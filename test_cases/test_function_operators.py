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
# Usage: py.test -v test_function_operators.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("test function operators")

def test_fn_ket_length_empty():
  x = ket("",3.14)
  assert ket_length(x).display() == "|number: 0>"

def test_fn_ket_length():
  x = ket("abcdefg",3.14)
  assert ket_length(x).display() == "|number: 7>"


def test_fn_apply_value_empty():
  x = ket("")
  assert apply_value(x).display() == "|>"

def test_fn_apply_value_float():
  x = ket("price: 3.70")
  assert apply_value(x).display() == "3.7|price: 3.70>"

def test_fn_apply_value():
  x = ket("just: strings: here")
  assert apply_value(x).display() == x.display()

def test_fn_apply_value_float_coeff():
  x = ket("price: 3.70",2)
  assert apply_value(x).display() == "7.4|price: 3.70>"


def test_fn_extract_category_empty():
  x = ket("",3)
  assert extract_category(x).display() == "3|>"

def test_fn_extract_category_one():
  x = ket("a",3)
  assert extract_category(x).display() == "3|>"

def test_fn_extract_category_two():
  x = ket("a: b",3)
  assert extract_category(x).display() == "3|a>"

def test_fn_extract_category_three():
  x = ket("a: b: c",3)
  assert extract_category(x).display() == "3|a: b>"


def test_fn_extract_value_empty():
  x = ket("",3)
  assert extract_value(x).display() == "3|>"

def test_fn_extract_value_one():
  x = ket("a",3)
  assert extract_value(x).display() == "3|a>"

def test_fn_extract_value_two():
  x = ket("a: b",3)
  assert extract_value(x).display() == "3|b>"

def test_fn_extract_value_three():
  x = ket("a: b: c",3)
  assert extract_value(x).display() == "3|c>"


# TODO:
# put the next two on the blog:
# http://write-up.semantic-db.org/49-a-big-collection-of-function-operators.html
#
def test_fn_find_leading_category_empty():
  x = ket("",3)
  assert find_leading_category(x).display() == "3|>"

def test_fn_find_leading_category_one():
  x = ket("a",3)
  assert find_leading_category(x).display() == "3|a>"

def test_fn_find_leading_category_two():
  x = ket("a: b",3)
  assert find_leading_category(x).display() == "3|a>"

def test_fn_find_leading_category_three():
  x = ket("a: b: c",3)
  assert find_leading_category(x).display() == "3|a>"


def test_fn_remove_leading_category_empty():
  x = ket("",3)
  assert remove_leading_category(x).display() == "3|>"

def test_fn_remove_leading_category_one():
  x = ket("a",3)
  assert remove_leading_category(x).display() == "3|a>"

def test_fn_remove_leading_category_two():
  x = ket("a: b",3)
  assert remove_leading_category(x).display() == "3|b>"

def test_fn_remove_leading_category_three():
  x = ket("a: b: c",3)
  assert remove_leading_category(x).display() == "3|b: c>"

def test_fn_remove_leading_category_five():
  x = ket("a: b: c: d: e",3)
  assert remove_leading_category(x).display() == "3|b: c: d: e>"



def test_fn_category_depth_empty():
  x = ket("",5)
  assert category_depth(x).display() == "|number: 0>"

def test_fn_category_depth_one():
  x = ket("a",5)
  assert category_depth(x).display() == "|number: 1>"

def test_fn_category_depth_two():
  x = ket("a: b",5)
  assert category_depth(x).display() == "|number: 2>"

def test_fn_category_depth_three():
  x = ket("a: b: c",5)
  assert category_depth(x).display() == "|number: 3>"

def test_fn_category_depth_seven():
  x = ket("a: b: c: d: e: f: g",5)
  assert category_depth(x).display() == "|number: 7>"



def test_fn_expand_hierarchy_empty():
  x = ket("",7)
  assert expand_hierarchy(x).display() == "|>"

def test_fn_expand_hierarchy():
  x = ket("a: b: c: d: e",7)
  assert expand_hierarchy(x).display() == "7|a> + 7|a: b> + 7|a: b: c> + 7|a: b: c: d> + 7|a: b: c: d: e>"


def test_fn_pop_float_empty():
  x = ket("",3)
  assert pop_float(x).display() == "3|>"

def test_fn_pop_float_float_label():
  x = ket("3.2")
  assert pop_float(x).display() == "3.2| >" # NB: | > and not |>.

def test_fn_pop_float_float_coeff():
  x = ket("7",5.1)
  assert pop_float(x).display() == "35.7| >"

def test_fn_pop_float_category_float():
  x = ket("x: 3.14159265")
  assert pop_float(x).display() == "3.142|x>"

def test_fn_pop_float_category_float_float_coeff():
  x = ket("x: y: 2",5.1)
  assert pop_float(x).display() == "10.2|x: y>"

def test_fn_pop_float_not_float():
  x = ket("x: y: z",13.2)
  assert pop_float(x).display() == "13.2|x: y: z>"

def test_fn_pop_float_superposition():
  x = ket("number: 3.2") + ket("number: 5") + ket("number: 0.3",2) 
#  assert pop_float(x).display() == "8.8|number>"
  assert x.apply_fn(pop_float).display() == "8.8|number>"


def test_fn_push_float_empty():
  x = ket("",3.7)
  assert push_float(x).display() == "0|>"

def test_fn_push_float_coeff_float():
  x = ket(" ",3.7)
  assert push_float(x).display() == "|3.7>"

def test_fn_push_float_no_coeff():
  x = ket("x")
  assert push_float(x).display() == "|x: 1>"

def test_fn_push_float_coeff_label():
  x = ket("x",13)
  assert push_float(x).display() == "|x: 13>"

def test_fn_push_float_no_coeff():
  x = ket("x: y: z",21.72312345)
  assert push_float(x).display() == "|x: y: z: 21.72312345>"

