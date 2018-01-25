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

valid_ket_chars = :x ?(x not in '<|>') -> x
naked_ket = '|' <valid_ket_chars*>:x '>' -> x
coeff_ket = (number | -> 1):value ws naked_ket:label -> (label, value)
signed_ket = ('-' | -> ''):sign ws (number | -> 1):value ws naked_ket:label -> (label, float(sign + str(value))) 

add_ket = ws '+' ws coeff_ket:k -> ('+', k)
sub_ket = ws '-' ws coeff_ket:k -> ('-', k)
merge_ket = ws '_' ws coeff_ket:k -> ('_', k)
seq_ket = ws '.' ws coeff_ket:k -> ('.', k)
ket_ops = (add_ket | sub_ket | merge_ket | seq_ket)

literal_sequence = ws signed_ket:left ws ket_ops*:right ws -> ket_calculate(left, right)
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
