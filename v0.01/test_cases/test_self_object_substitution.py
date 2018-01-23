#!/usr/bin/env python3

#######################################################################
# test the self_ket substitution problem, and try to find a fix!
# made progress. I now have two solutions, and I need to choose which is the best.
# One is build a full parse tree, and then insert the _self value in at "compile" time
# The other is to pass in a reference to ket_substitute, and change the reference value just before invoke time.
# Currently learning towards this second method.
# Quick testing shows almost no speed difference between the two.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-08-16
# Update:
# Copyright: GPLv3
#
# Usage: py.test -v test_self_object_substitution.py
#
#######################################################################


import sys
from parsley import makeGrammar
from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("the _self ket problem")

# define a simple grammar:
our_grammar = """
# number copied from here:
# http://parsley.readthedocs.org/en/latest/tutorial2.html
number = ('-' | -> ''):sign (intPart:ds (floatPart(sign ds)
                                        | -> int(sign + ds)))
digit = :x ?(x in '0123456789') -> x
digits = <digit*>
digit1_9 = :x ?(x in '123456789') -> x
intPart = (digit1_9:first digits:rest -> first + rest) | digit
floatPart :sign :ds = <('.' digits exponent?) | exponent>:tail
                     -> float(sign + ds + tail)
exponent = ('e' | 'E') ('+' | '-')? digits


# my parsley code:
S0 = ' '*
valid_ket_chars = anything:x ?(x not in '<|>') -> x
naked_ket = '|' <valid_ket_chars*>:x '>' -> x
coeff_ket = (number | -> 1):value S0 naked_ket:label -> (label,value)

add_ket = S0 '+' S0 coeff_ket:k -> ('+', k)
sub_ket = S0 '-' S0 coeff_ket:k -> ('-', k)
merge_ket = S0 '_' S0 coeff_ket:k -> ('_', k)
ket_ops = (add_ket | sub_ket | merge_ket )
literal_superposition = S0 coeff_ket:left S0 ket_ops*:right S0 -> [('+',left)] + right   


coeff_ket_v2 = (number | -> 1):value S0 naked_ket:label -> new_ket_substitute(label,value,self_object)

add_ket_v2 = S0 '+' S0 coeff_ket_v2:k -> ('+', k)
sub_ket_v2 = S0 '-' S0 coeff_ket_v2:k -> ('-', k)
merge_ket_v2 = S0 '_' S0 coeff_ket_v2:k -> ('_', k)
ket_ops_v2 = (add_ket_v2 | sub_ket_v2 | merge_ket_v2 )
literal_superposition_v2 = S0 coeff_ket_v2:left S0 ket_ops_v2*:right S0 -> ket_calculate(left,right)
"""

class reference(object):
  def __init__(self,value=None):
    if type(value) == str:                                # cast value to ket/sp type
      self.object = ket(value)
    elif type(value) in [ket,superposition]:
      self.object = value
    else:
      self.object = None

  def get(self):
    return self.object

  def set(self,value):
    if type(value) == str:                                # cast value to ket/sp type
      self.object = ket(value)
    if type(value) in [ket,superposition]:
      self.object = value


def new_ket_substitute(label,value,self_object):
  if label == "_self":
    if self_object.get() is not None:
      return self_object.get().multiply(value)
  return ket(label,value)

def ket_calculate(start,pairs):
  print("start:",str(start))
  print("pairs:",str(pairs))

  result = start
  for op, value in pairs:
    if op == '+':
      result += value
    elif op == '-':
      result += value.multiply(-1)
    elif op == '_':                                 # maybe handle the merge-labels bit in a cleaner way??
      head,tail = result.index_split(-1)            # how handle coeffs of merged pieces?
      result = head + ket(tail.the_label() + value.label)  # currently set to 1
  return result

# initialize the self_object:
self_object = reference()


# define the bindings dictionary:
bindings_dictionary = {
  "new_ket_substitute"      : new_ket_substitute,
  "self_object"             : self_object,
  "ket_calculate"           : ket_calculate,
}

# "compile" the grammar:
the_grammar = makeGrammar(our_grammar,bindings_dictionary)

# compile patterns of this shape:
# [('+', ('x', 3)), ('+', ('y', 1)), ('+', ('_self', 2.7)), ('-', ('d', 1))]
#
def compile_superposition(pairs,self_object=None):
  print("pairs:",str(pairs))

  if self_object is not None and type(self_object) == str:                   # cast string self_object to ket
    self_object = ket(self_object)

  result = superposition()
  for op, (label,value) in pairs:
    if label == "_self" and self_object is not None:
      the_ket = self_object.multiply(value)
    else:
      the_ket = ket(label,value)

    if op == '+':
      result += the_ket
    elif op == '-':
      result += the_ket.multiply(-1)
    elif op == '_':                                 # maybe handle the merge-labels bit in a cleaner way??
      head,tail = result.index_split(-1)            # how handle coeffs of merged pieces?
      result = head + ket(tail.the_label() + the_ket.label)  # currently set to 1
  return result


# test our rules:
def test_grammar_coeff_ket_compile():
  x = the_grammar("2.7|_self>").coeff_ket()
  y = compile_superposition([('+', x)], "fish")
  assert str(y) == "2.7|fish>"

def test_grammar_literal_sp_substitute_compile():
  x = the_grammar("3|x> + |y> + 2.7|_self> -|d>").literal_superposition()
  y = compile_superposition(x,ket("rats",3))
  assert str(y) == "3|x> + |y> + 8.1|rats> + -1|d>"


def test_grammar_coeff_ket_set_value():
  self_object.set("fish")
  x = the_grammar("2.7|_self>").coeff_ket_v2()
  assert str(x) == "2.7|fish>"

def test_grammar_literal_sp_substitute_set_value():
  self_object.set(ket("rats",3))
  x = the_grammar("3|x> + |y> + 2.7|_self> -|d>").literal_superposition_v2()
  assert str(x) == "3|x> + |y> + 8.1|rats> + -1|d>"


#k = 1000
k = 1

# let's time them:
start_time = time.time()      

for _ in range(k):
  test_grammar_coeff_ket_compile()
  test_grammar_literal_sp_substitute_compile()

end_time = time.time()
delta_time = end_time - start_time
print("\n  Time taken v1:",display_time(delta_time))


start_time = time.time()

for _ in range(k):
  test_grammar_coeff_ket_set_value()
  test_grammar_literal_sp_substitute_set_value()

end_time = time.time()
delta_time = end_time - start_time
print("\n  Time taken v2:",display_time(delta_time))

