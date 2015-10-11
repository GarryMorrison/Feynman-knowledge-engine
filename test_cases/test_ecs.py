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

def test_ecs_literal_superposition():
  s = " |a> + 7|b> + 0.05|c> "
  assert ecs(s) == "|a> + 7|b> + 0.05|c>"

def test_ecs_literal_superposition_negative():
  s = " |a> -3|c> + |d>"
  assert ecs(s) == ""            # this one will be quite a while before being fixed!

def test_ecs_op_ket():
  s = "name |x>"
  assert ecs(s) == "|name-x>"

def test_ecs_op_int_ket_plus_op_ket():
  s = "name 2|x> + name|y>"
  assert ecs(s) == "2|name-x> + |name-y>"

def test_ecs_op_literal_superposition():
  s = "name (|x> + 7.3|y>)"
  assert ecs(s) == "|name-x> + 7.3|name-y>"

def test_ecs_op_name():
  s = "op name|x>"
  assert ecs(s) == "|op-name-x>"

def test_ecs_op_op():
  s = "op op |x>"
  assert ecs(s) == "|op-op-x>"

def test_ecs_op_squared():
  s = "op^2 |x>"
  assert ecs(s) == "|op-op-x>"

def test_ecs_union_literal_sp_literal_sp():
  s = "union(|a> + |b>,|c> + |d> + |e>)"
  assert ecs(s) == "|a> + |b> + |c> + |d> + |e>"

def test_ecs_union_op_ket_op_ket():
  s = "union(name|x>,op^2|x>)"
  assert ecs(s) == "|name-x> + |op-op-x>"

def test_ecs_union_literal_sp_float_op_ket():
  s = "union(2|a> + 7|b>,1.42 op|x>)"
  assert ecs(s) == "2|a> + 7|b> + 1.42|op-x>"

def test_ecs_mult_op_ket():
  s = "mult[7] name|x>"
  assert ecs(s) == "7|name-x>"

def test_ecs_int_op_ket():
  s = "7 name|x>"
  assert ecs(s) == "7|name-x>"

def test_ecs_op_float_op_ket():
  s = "op 5.2 name |x>"
  assert ecs(s) == "5.2|op-name-x>"

def test_ecs_op_float_ket():
  s = "name 3.142   |x>"
  assert ecs(s) == "3.142|name-x>"

def test_ecs_junk_ket():
  s = "junk |x>"             # junk |x> is not defined, so should return |> 
  assert ecs(s) == "|>"      

def test_ecs_junk_op_ket():
  s = "junk op |x>"
  assert ecs(s) == "|>"

def test_ecs_op_junk_ket():
  s = "op junk |x>"
  assert ecs(s) == "|>" 

def test_ecs_op_ket_plus_ket_plus_ket():  
  s = "fish|x> + |a> + |b>"
  assert ecs(s) == "|fish-x> + |a> + |b>"

def test_ecs_op_ket_plus_literal_sp():
  s = "fish |x> + (|a> + |b>)"
  assert ecs(s) == "|fish-x> + |a> + |b>"

def test_ecs_op_ket_plus_bracket_ket():
  s = "fish|y> + (|c>)"
  assert ecs(s) == "|fish-y> + |c>"

def test_ecs_bracket_ket_plus_op_ket():
  s = "(|c>) + fish|x>"
  assert ecs(s) == "|c> + |fish-x>"

def test_ecs_bracket_ket():
  s = "(|a>)"
  assert ecs(s) == "|a>"

def test_ecs_bracket_literal_sp():
  s = "(2.2|a> + |b> + 0.7|c>)"
  assert ecs(s) == "2.2|a> + |b> + 0.7|c>"

def test_ecs_float_bracket_literal_sp():
  s = "2.7(|a> + 2|b>)"
  assert ecs(s) == "2.7|a> + 5.4|b>"

def test_ecs_op_bracket_literal_sp():
  s = "op (0.2|x> + |y>)"
  assert ecs(s) == "0.2|op-x> + |op-y>"

def test_ecs_junk_bracket_literal_sp():
  s = "junk (0.2|x> + |y>)"
  assert ecs(s) == "|>"




# test parameter functions:
def test_ecs_range_no_datatype():
  s = "range (|13>,|17>)"
  assert ecs(s) == "|13> + |14> + |15> + |16> + |17>"

def test_ecs_range_no_datatype_step():
  s = "range (|13>,|27>,|5>)"
  assert ecs(s) == "|13> + |18> + |23>"

def test_ecs_range_no_datatype_step_negative_empty():
  s = "range (|13>,|27>,|-1>)"
  assert ecs(s) == "|>"

def test_ecs_range_no_datatype_step_negative():
  s = "range (|27>,|19>,|-1>)"
  assert ecs(s) == "|27> + |26> + |25> + |24> + |23> + |22> + |21> + |20> + |19>"

def test_ecs_range():
  s = "range (|n: 5>,|n: 8>)"
  assert ecs(s) == "|n: 5> + |n: 6> + |n: 7> + |n: 8>"

def test_ecs_range_step():
  s = "range(|n: 1>,|n: 10>,|n: 3>)"
  assert ecs(s) == "|n: 1> + |n: 4> + |n: 7> + |n: 10>"

def test_ecs_simm_ket():
  s = "simm(|a>+|b>,|b>+|c>+|d>)|g>"
  assert ecs(s) == "0.333|g>"

def test_ecs_simm_int_ket():
  s = "simm(|a>+|b>,|b>) 3|g>"
  assert ecs(s) == "1.5|g>"

def test_ecs_ket_simm():
  s = "ket-simm(|a>+|b>,|b>+|c>+|d>)"
  assert ecs(s) == "0.333|simm>"

def test_ecs_algebra():
  s = "7 algebra(|a> + 2| >,|^>,2| >)+3| >"
  assert ecs(s) == "7|a*a> + 28|a> + 31| >"

def test_ecs_algebra_plus_algebra():
  s = "algebra(|a>,|^>,|3>) + algebra(|b>,|^>,|2>)"
  assert ecs(s) == "|a*a*a> + |b*b>"

def test_ecs_tri_union_kets():
  s = "union(|a>,|b>,|c>)"
  assert ecs(s) == "|a> + |b> + |c>"

def test_ecs_tri_union_sp():
  s = "union(|a>+|b>,|c>,|d>+|e>)"
  assert ecs(s) == "|a> + |b> + |c> + |d> + |e>"

def test_ecs_union_compound_superposition():
  s = "union(|a>+|b>,7.2 fish(|x>+|y>))"
  assert ecs(s) == "|a> + |b> + 7.2|fish-x> + 7.2|fish-y>"

def test_ecs_arithmetic_no_datatype():
  s = "arithmetic(|3>,|*>,|5>)"
  assert ecs(s) == "|15>"

def test_ecs_arithmetic_datatype():
  s = "arithmetic(|n: 3>,|+>,|n: 5>)"
  assert ecs(s) == "|n: 8>"

def test_ecs_arithmetic_wrong_datatype():
  s = "arithmetic(|x: 3>,|+>,|y: 5>)"
  assert ecs(s) == "|>"

def test_ecs_arithmetic_unknown_operator():
  s = "arithmetic(|x: 3>,|&>,|x: 5>)"
  assert ecs(s) == "|>"

def test_ecs_superposition_multiply():
  s = "mult(2|a> + 3|b>,5|b> + 7.3|a>)"
  assert ecs(s) == "14.6|a> + 15|b>"
