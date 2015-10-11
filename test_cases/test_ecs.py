#!/usr/bin/env python3

#######################################################################
# code to test extract-compound-superposition code
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-09-27
# Update:
# Copyright: GPLv3
#
# Usage: py.test -v test_ecs.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("test extract-compound-superposition code")

# learn some example knowledge:
C.learn("foo","x",ket("a") + ket("b") + ket("c") + ket("d"))
C.learn("bah","y",ket("b") + ket("d",0.3))
C.learn("foo","y",ket("u") + ket("v",13))
C.learn("","z",ket("dot"))
C.learn("bah","d",ket("done"))
C.learn("name","x","name-x")
C.learn("name","y","name-y")
C.learn("op","name-x","op-name-x")
C.learn("op","x","op-x")
C.learn("op","op-x","op-op-x")
C.learn("fish","x","fish-x")
C.learn("fish","y","fish-y")
C.learn("op","fish-y","op-fish-y")
C.learn("op","y","op-y")
print(C.dump_universe())

def ecs(s):
  return extract_compound_superposition(C,s)[0].display()

def test_ecs_naked_ket():
  s = " |y> "
  assert ecs(s) == "|y>"

def test_ecs_int_coeff_ket():
  s = " 3|z> "
  assert ecs(s) == "3|z>"

def test_ecs_float_coeff_ket():
  s = " 3.141592|pi> "
  assert ecs(s) == "3.142|pi>"

