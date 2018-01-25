#!/usr/bin/env python3

#######################################################################
# let's slowly build our parser!
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-1-25
# Update: 2018-1-25
# Copyright: GPLv3
#
# Usage: py.test -v test_parser.py
#
#######################################################################


import sys
from parsley import makeGrammar
from pprint import pprint

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("parse compound superposition")
#context.load("sw-examples/fred-sam-friends.sw")
#context.load("sw-examples/test-operators.sw")



# operator parse:
our_working_grammar = """
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

valid_ket_chars = :x ?(x not in '<|>')
naked_ket = '|' <valid_ket_chars*>:x '>' -> x
coeff_ket = (number | -> 1):value ws naked_ket:label -> (label, value)
signed_ket = ('-' | -> ''):sign ws (number | -> 1):value ws naked_ket:label -> (label, float(sign + str(value))) 

add_ket = ws '+' ws coeff_ket:k -> ('+', k)
sub_ket = ws '-' ws coeff_ket:k -> ('-', k)
merge_ket = ws '_' ws coeff_ket:k -> ('_', k)
seq_ket = ws '.' ws coeff_ket:k -> ('.', k)
ket_ops = (add_ket | sub_ket | merge_ket | seq_ket)

literal_sequence = ws signed_ket:left ws ket_ops*:right ws -> ket_calculate(left, right)


positive_int = <digit+>:n -> int(n)
#S0 = ' '*
S1 = ' '+
op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.')
valid_op_name = op_start_char:first <op_char*>:rest -> first + rest
simple_op = valid_op_name:s -> s
#parameters = (number | simple_op | '\"\"' | '*'):p -> p
parameters = (number | simple_op | '\"\"' | '*'):p -> str(p)

compound_op = simple_op:the_op '[' parameters:first (',' ws parameters)*:rest ']' -> [the_op] + [first] + rest
general_op = (compound_op | simple_op | number | '\"\"' ):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op,power)
op = (powered_op | general_op):the_op -> the_op
op_sequence = (ws op:first (S1 op)*:rest ws -> [first] + rest)
              | ws -> []

add_op_sequence = ws '+' ws op_sequence:seq -> ('+', seq)
sub_op_sequence = ws '-' ws op_sequence:seq -> ('-', seq)
merge_op_sequence = ws '_' ws op_sequence:seq -> ('_', seq)
seq_op_sequence = ws '.' ws op_sequence:seq -> ('.', seq)
op_sequence_ops = (add_op_sequence | sub_op_sequence | merge_op_sequence | seq_op_sequence)
#bracket_ops = ws '(' op_sequence:first ws (op_sequence_ops+:rest ws ')' ws -> [('+', first)] + rest
#                                          | ')' ws -> [('+', first)] )
op_symbol = ('+' | '-' | '_' | '.')
bracket_ops = ws '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws (op_sequence_ops+:rest ws ')' ws -> [(symbol, first)] + rest
                                          | ')' ws -> [(symbol, first)] )

"""


def ket_calculate(start,pairs):
  print('pairs: %s' % (pairs))

  seq = sequence()
  sp = superposition(*start)
  for op, value in pairs:
    if op == '+':
      sp.add(*value)
    elif op == '-':
      sp.sub(*value)
    elif op == '_':     
      sp = sp.merge(superposition(*value))
    elif op == '.':
      seq += sp
      sp = superposition(*value)
  seq += sp
  return seq

bindings_dictionary = {
  "ket_calculate"           : ket_calculate,
}

op_grammar = makeGrammar(our_working_grammar, bindings_dictionary)

def test_coeff_ket():
  x = op_grammar('|fish>').coeff_ket()
  assert x == ('fish', 1)

def test_coeff_ket_coeff():
  x = op_grammar('3.721 |fish>').coeff_ket()
  assert x == ('fish', 3.721)


def test_literal_sequence():
  x = op_grammar('  2.7 |z>    ').literal_sequence()
  assert str(x) == '2.7|z>'

def test_negative_ket():
  x = op_grammar(' -3.141592|pi>').literal_sequence()
  assert str(x) == '-3.142|pi>'

def test_ket_clean_addition_1():
  x = op_grammar(' |a> +|b> + |c>+|d> ').literal_sequence()
  assert str(x) == '|a> + |b> + |c> + |d>'


def test_ket_subtraction_1():
  x = op_grammar(' |a> - 2|b>').literal_sequence()
  assert str(x) == '|a> + -2|b>'

def test_ket_subtraction_2():
  x = op_grammar(' -|a> + 2|b>').literal_sequence()
  assert str(x) == '-1|a> + 2|b>'


def test_sp_merge():
  x = op_grammar(' |a> + 2.1|b> + 3|c> _ 7.9|d> + |e> + |f>').literal_sequence()
  assert str(x) == '|a> + 2.1|b> + |cd> + |e> + |f>'

def test_seq_add():
  x = op_grammar(' |a> + 2.1|b> + 3|c> . 7.9|d> + |e> + |f>').literal_sequence()
  assert str(x) == '|a> + 2.1|b> + 3|c> . 7.9|d> + |e> + |f>'

def test_seq_add_multi():
  x = op_grammar(' |a> - 2.1|b> + 3|c> _ 7.9|d> . 29.9|e> + |f> . |fish> . |soup> + 13.2|pasta> ').literal_sequence()
  assert str(x) == '|a> + -2.1|b> + |cd> . 29.9|e> + |f> . |fish> . |soup> + 13.2|pasta>'

def test_seq_add_multi():
  x = op_grammar(' |a> - 2.1|b> + 3|c> _ 7.9|d> . 29.9|e> + |f> . |fish> . |soup> + 13.2|pasta> ').literal_sequence()
  x.display()
  assert True


# test operator parsing:
def test_simple_op():
  s = op_grammar('!equal-2?').simple_op()
  assert s == '!equal-2?'

def test_compound_op():
  x = op_grammar('fish[a,3.7,99]').compound_op()
  assert x == ['fish', 'a', '3.7', '99']

def test_compound_op_spaces():
  x = op_grammar('fish[a, 3.7, 99]').compound_op()
  assert x == ['fish', 'a', '3.7', '99']

def test_compound_op_spaces():
  x = op_grammar('fish[a, 3.7, 99]^7').powered_op()
  assert x == (['fish', 'a', '3.7', '99'], 7)

def test_op_sequence_space():
  x = op_grammar("  ").op_sequence()
  assert x == []

def test_op_sequence_simple_sequence():
  x = op_grammar(" foo bah fish ").op_sequence()
  assert x == ['foo', 'bah', 'fish']

# ['foo', 'bah', ['fish', 'x', 'y', '13.2'], (['select', '1', '3'], 2)]
def test_op_sequence_one():
  x = op_grammar("  foo bah fish[x,y,13.2] select[1,3]^2   ").op_sequence()
  assert x == ['foo', 'bah', ['fish', 'x', 'y', '13.2'], (['select', '1', '3'], 2)]

# ['33.2', '""', ['fish', 'foo'], ('3.14', 3), 'some-op', '-13.572']
def test_op_sequence_two():
  x = op_grammar(" 33.2  \"\" fish[foo] 3.14^3 some-op -13.572 ").op_sequence()
  assert x == [33.2, '""', ['fish', 'foo'], (3.14, 3), 'some-op', -13.572]

def test_bracket_ops_empty():
  x = op_grammar(' ( ) ').bracket_ops()
  assert x == [('+', [])]

def test_bracket_ops_simple():
  x = op_grammar(' (op2 - 2 op1) ').bracket_ops()
  assert x == [('+', ['op2']), ('-', [2, 'op1'])]

def test_bracket_ops_complex():
  x = op_grammar(' (op6^3 op5 + op4 op3[fish]^2 op2 - 2 op1) ').bracket_ops()
  assert x == [('+', [('op6', 3), 'op5']), ('+', ['op4', (['op3', 'fish'], 2), 'op2']), ('-', [2, 'op1'])]

def test_bracket_ops_merge_and_seq():
  x = op_grammar(' ( op6 op5 _ op4 . op3 op2 + op1 op - foo1^7 ) ').bracket_ops()
  assert x == [('+', ['op6', 'op5']), ('_', ['op4']), ('.', ['op3', 'op2']), ('+', ['op1', 'op']), ('-', [('foo1', 7)])]

def test_op_subtraction_1():
  x = op_grammar(' (op2 - 2 op1 )').bracket_ops()
  assert x == [('+', ['op2']), ('-', [2, 'op1'])]

def test_op_subtraction_2():
  x = op_grammar(' (-op2 + 2 op1)').bracket_ops()
  assert x == [('-', ['op2']), ('+', [2, 'op1'])]


