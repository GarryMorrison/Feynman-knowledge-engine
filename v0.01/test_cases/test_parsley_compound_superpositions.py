#!/usr/bin/env python3

#######################################################################
# 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-10-15
# Update:
# Copyright: GPLv3
#
# Usage: py.test -v test_parsley_compound_superpositions.py
#
#######################################################################


import sys
from parsley import makeGrammar

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("parse compound superposition")

# operator parse:
our_operator_grammar = """
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
S1 = ' '+

#digit = :x ?(x in '0123456789') -> x
positive_int = <digit+>:n -> int(n)

# what about handle more than one dot char??
# fix eventually, but not super important for now
# what about minus sign?
simple_float = ('-' | -> ''):sign <(digit | '.')+>:n -> float_int(sign + n)

op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
# allow dot as an op char??
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.') -> x
literal_op = op_start_char:first <op_char*>:rest -> first + rest

parameters = (simple_float | literal_op | '\"\"' | '*')
compound_op = literal_op:the_op '[' parameters:first (',' parameters)*:rest ']' -> [the_op] + [first] + rest

#general_op = (compound_op | literal_op | simple_float | '\"\"' | '-'):the_op -> the_op
# hrmm.. having '-' in there breaks the bracket_op processing.
# is it vital?
general_op = (compound_op | literal_op | simple_float | '\"\"' ):the_op -> the_op

powered_op = general_op:the_op '^' positive_int:power -> (the_op,power)

op = (powered_op | general_op):the_op -> the_op

op_sequence = (S0 op:first (S1 op)*:rest S0 -> [first] + rest)
              | S0 -> []

add_sequence = S0 '+' S0 op_sequence:k -> ('+',k)
sub_sequence = S0 '-' S0 op_sequence:k -> ('-',k)
sequence_ops = (add_sequence | sub_sequence)

bracket_ops = S0 '(' op_sequence:first S0 (sequence_ops+:rest S0 ')' S0 -> [('+',first)] + rest
                                          | ')' S0 -> [('+',first)] )

valid_ket_chars = anything:x ?(x not in '<|>') -> x
naked_bra = '<' <valid_ket_chars*>:x '|' -> x
naked_ket = '|' <valid_ket_chars*>:x '>' -> x
#naked_projection = naked_ket:label1 naked_bra:label2 -> projection(label1,label2)
coeff_ket = (number | -> 1):value S0 naked_ket:label -> ket(label,value)
coeff_bra = (number | -> 1):value S0 naked_bra:label -> bra(label,value)
bra_coeff = naked_bra:label S0 (number | -> 1):value -> bra(label,value)

add_ket = S0 '+' S0 coeff_ket:k -> ('+', k)
sub_ket = S0 '-' S0 coeff_ket:k -> ('-', k)
merge_ket = S0 '_' S0 coeff_ket:k -> ('_', k)
sequence_ket = S0 '.' S0 coeff_ket:k -> ('.', k)

ket_ops = (add_ket | sub_ket | merge_ket | sequence_ket)

literal_superposition = S0 coeff_ket:left S0 (ket_ops+:right S0 -> ket_calculate(left,right)
                                          | -> left)

bracket_literal_superposition = S0 '(' literal_superposition:sp ')' S0 -> sp
bracket1_literal_superposition = '(' literal_superposition:sp1 ')' -> [sp1]
bracket2_literal_superposition = '(' literal_superposition:sp1 ',' literal_superposition:sp2 ')' -> [sp1,sp2]
bracket3_literal_superposition = '(' literal_superposition:sp1 ',' literal_superposition:sp2 ',' literal_superposition:sp3 ')' -> [sp1,sp2,sp3]
bracket4_literal_superposition =  '(' literal_superposition:sp1 ',' literal_superposition:sp2 ',' literal_superposition:sp3 ',' literal_superposition:sp4 ')' -> [sp1,sp2,sp3,sp4]

param1_fn = op_sequence:head bracket1_literal_superposition:tail -> [head,tail]
param2_fn = op_sequence:head bracket2_literal_superposition:tail -> [head,tail]
param3_fn = op_sequence:head bracket3_literal_superposition:tail -> [head,tail]
param4_fn = op_sequence:head bracket4_literal_superposition:tail -> [head,tail]


add_bra = S0 '+' S0 (bra_coeff | coeff_bra):k -> ('+', k)
sub_bra = S0 '-' S0 (bra_coeff | coeff_bra):k -> ('-', k)
#merge_bra = S0 '_' S0 bra_coeff:k -> ('_', k)
#sequence_bra = S0 '.' S0 bra_coeff:k -> ('.', k)

bra_ops = (add_bra | sub_bra)

literal_bra_superposition = S0 (bra_coeff | coeff_bra):left S0 (bra_ops+:right S0 -> bra_calculate(left,right)
                                                            | -> left)

#ket_like = (literal_superposition | bracket_literal_superposition | op_sequence bracket_literal_superposition | bracket_ops bracket_literal_superposition)
"""

# what happens if we have eg: "3.73.222751" (ie, more than one dot?)
def float_int(x):
  if float(x).is_integer():
    return str(int(x))
  return x

def ket_calculate(start,pairs,self_ket_label=None):
  result = start
  for op, value in pairs:
    if self_ket_label != None and value.label == "_self":
      value = ket(self_ket_label)
    if op == '+':
      result += value
    elif op == '-':
      result += value.multiply(-1)
    elif op == '_':                                 # maybe handle the merge-labels bit in a cleaner way??
      head,tail = result.index_split(-1)            # how handle coeffs of merged pieces?
      result = head + ket(tail.the_label() + value.label)  # currently set to 1
  return result

def bra_calculate(start,pairs,self_bra_label=None):
  result = start
  for op, value in pairs:
    if self_bra_label != None and value.label == "_self":
      value = bra(self_bra_label)
    if op == '+':
      result += value
    elif op == '-':
      result += value.multiply(-1)
  return result


op_grammar = makeGrammar(our_operator_grammar,{"float_int" : float_int,"ket" : ket, "bra" : bra, "ket_calculate" : ket_calculate, "bra_calculate" : bra_calculate})


# ('some-frog', 37)
def test_op_powered_op():
  x = op_grammar("some-frog^37").powered_op()
  assert str(x) == "('some-frog', 37)"

# ['foo', '""']
def test_op_compound_op_quotes():
  x = op_grammar("foo[\"\"]").compound_op()
  assert str(x) == '[\'foo\', \'""\']'

# ['foo', 'bah']
def test_op_compound_op_string():
  x = op_grammar("foo[bah]").compound_op()
  assert str(x) == "['foo', 'bah']"

# ['foo', '373', 'bah']
def test_op_compound_op_int_string():
  x = op_grammar("foo[373,bah]").compound_op()
  assert str(x) == "['foo', '373', 'bah']"


# 'foo'
def test_op_general_op():
  x = op_grammar("foo").general_op()
  assert str(x) == 'foo'

# ['foo', '3.1416']
def test_op_general_op_float():
  x = op_grammar("foo[3.1416]").general_op()
  assert str(x) == "['foo', '3.1416']"


# (['foo', '37', 'fish'], 13)
def test_op_powered_op_compound():
  x = op_grammar("foo[37,fish]^13").powered_op()
  assert str(x) == "(['foo', '37', 'fish'], 13)"


# (['foo', 'bah', '13.2'], 7)
def test_op_op():
  x = op_grammar("foo[bah,13.2]^7").op()
  assert str(x) == "(['foo', 'bah', '13.2'], 7)"

# ('foo', 2)
def test_op_op_foo_square():
  x = op_grammar("foo^2").op()
  assert str(x) == "('foo', 2)"


# []
def test_op_op_sequence_empty():
  x = op_grammar("").op_sequence()
  assert str(x) == "[]"

# []
def test_op_op_sequence_space():
  x = op_grammar("  ").op_sequence()
  assert str(x) == "[]"

# ['foo', 'bah', ['fish', 'x', 'y', '13.2'], (['select', '1', '3'], 2)]
def test_op_op_sequence_one():
  x = op_grammar("  foo bah fish[x,y,13.2] select[1,3]^2   ").op_sequence()
  assert str(x) == "['foo', 'bah', ['fish', 'x', 'y', '13.2'], (['select', '1', '3'], 2)]"

# ['33.2', '""', ['fish', 'foo'], ('3.14', 3), 'some-op', '-13.572']
def test_op_op_sequence_two():
  x = op_grammar(" 33.2  \"\" fish[foo] 3.14^3 some-op -13.572 ").op_sequence()
  assert str(x) == "['33.2', '\"\"', ['fish', 'foo'], ('3.14', 3), 'some-op', '-13.572']"



# hrmm... need tests with extra spaces in various positions.
# [('+', ['op'])]
def test_op_bracket_ops_one_op():
  x = op_grammar("(op)").bracket_ops()
  assert str(x) == "['op']"

# [('+', ['op3', ('op', 3), ['bah', 'fish'], '37'])]
def test_op_bracket_ops_one_op_sequence():
  x = op_grammar("(op3 op^3 bah[fish] 37)").bracket_ops()
  assert str(x) == "['op3', ('op', 3), ['bah', 'fish'], '37']"


# [('+', ['op']), ('+', ['op2'])]
def test_op_bracket_ops_two_op():
  x = op_grammar(" (op + op2)").bracket_ops()
  assert str(x) == ""

# [('+', ['op']), ('+', ['op2']), ('-', ['op3']), ('+', ['op4']), ('-', ['op5'])]
def test_op_bracket_ops_five_negative():
  x = op_grammar(" (op + op2 - op3 + op4 - op5)").bracket_ops()
  assert str(x) == ""

# [('+', ['op']), ('+', ['op2', 'op3', 'op4']), ('-', [('op5', 2), ['op4', 'fish'], 'op6']), ('-', ['op5'])]
def test_op_bracket_ops_big_negative_sequences():
  x = op_grammar("  (  op + op2 op3 op4 - op5^2 op4[fish] op6 - op5 )  ").bracket_ops()
  assert str(x) == ""

# 
def test_op_bracket_ops_negative_element():
  x = op_grammar("  ( op1 op2 + op3 op4 -3 op5 + op6 op7 )").bracket_ops()
  assert str(x) == ""


# 3.2|a> + |b> + 3.142|pi> + -1|d> + |z>
def test_op_literal_superposition():
  x = op_grammar(" 3.2|a> + |b> + 3.1415|pi> -|d> + |z> -3 |omega> ").literal_superposition()
  assert str(x) == ""

# 3.2|a> + |b> + 3.142|pi> + -1|d> + |z>
def test_op_bracket_literal_superposition():
  x = op_grammar(" ( 3.2|a> + |b> + 3.1415|pi> -|d> + |z>  ) ").bracket_literal_superposition()
  assert str(x) == ""



# "fish"
def test_op_naked_bra():
  x = op_grammar("<fish|").naked_bra()
  assert str(x) == ""

#
def test_op_naked_coeff_bra():
  x = op_grammar("<fish|").coeff_bra()
  assert str(x) == ""

#
def test_op_coeff_bra():
  x = op_grammar("37.15 <fish|").coeff_bra()
  assert str(x) == ""
 
#
def test_op_bra_coeff():
  x = op_grammar("<fish| 3.15").bra_coeff()
  assert str(x) == ""


#
def test_op_literal_bra_superposition():
  x = op_grammar("<pi| 3.141592 + <y| + <x|3 + <z|2").literal_bra_superposition()
  assert str(x) == ""

#
def test_op_literal_bra_superposition_mixed():
  x = op_grammar("3.15<pi| + 7 <y| + <x|3 + <z|2 + <u| ").literal_bra_superposition()
  assert str(x) == ""



#
def test_op_param2_fn():
  x = op_grammar("foo (3|x> + 7.3|y> + |z>,|a> + 0.2|b>)").param2_fn()
  assert str(x) == ""


#
def test_op_param2_fn_example_2():
  x = op_grammar("op3^2 op2 op1 foo (3|x> + 7.3|y> + |z>,|a> + 0.2|b>)").param2_fn()
  assert str(x) == ""


