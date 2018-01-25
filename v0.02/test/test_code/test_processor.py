#!/usr/bin/env python3

#######################################################################
# code to test v0.02 the_semantic_db_processor.py
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-1-25
# Update: 2018-1-25
# Copyright: GPLv3
#
# Usage: py.test -v test_processor.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("semantic db code")
context.load("sw-examples/fred-sam-friends.sw")    # currently fails to load.
#context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
#context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
context.print_multiverse()
#sys.exit(0)

def test_extract_literal_superposition():
  s = '|a> + 2|b> + 3.22|c>'
  x, null = extract_literal_superposition(s)
  assert str(x) == '|a> + 2|b> + 3.22|c>'

# not sure why this one works
# it doesn't. Just looks like it does.
# ket inside of x is actually 
# a> + 2|b> + 3.22|c
def test_extract_non_clean_superposition():
  s = '|a> + 2|b> + 3.22|c>'
  x = extract_clean_superposition(s)
  assert str(x) == ''

def test_extract_clean_superposition():
  s = '|a> + |b> + |c> + |b> + |a> + |a>'
  x = extract_clean_superposition(s)
  assert str(x) == '3|a> + 2|b> + |c>'

def test_extract_compount_superposition():
  s = '|a> + 2|b> + 3.22|c>'
  x, null = extract_compound_superposition(context, s)
  assert str(x) == '|a> + 2|b> + 3.22|c>'

def test_parse_rule_line():
  s = 'happy |fred> => |yes>'
  context = new_context('test parse rule line')
  parse_rule_line(context, s)
  context.print_universe()
  assert True

