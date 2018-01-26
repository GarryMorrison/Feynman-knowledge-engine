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

symbol_ket = ws op_symbol:symbol ws coeff_ket:k -> (symbol, k)
literal_sequence = ws signed_ket:left ws symbol_ket*:right ws -> ket_calculate(left, right)


positive_int = <digit+>:n -> int(n)
#S0 = ' '*
S1 = ' '+
op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.')
valid_op_name = op_start_char:first <op_char*>:rest -> first + rest
simple_op = valid_op_name:s -> s
#parameters = (number | simple_op | '\"\"' | '*'):p -> p
parameters = (number | simple_op | '\"\"' | '*'):p -> str(p)

minus = '-' -> -1
compound_op = simple_op:the_op '[' parameters:first (',' ws parameters)*:rest ']' -> [the_op] + [first] + rest
general_op = (compound_op | simple_op | number | '\"\"' ):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op, power)
op = (powered_op | general_op):the_op -> the_op
op_sequence = (ws op:first (S1 op)*:rest ws -> [first] + rest)
              | ws -> []

op_symbol = ('+' | '-' | '_' | '.')
symbol_op_sequence = ws op_symbol:symbol ws op_sequence:seq -> (symbol, seq)
bracket_ops = ws '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws (symbol_op_sequence+:rest ws ')' ws -> [(symbol, first)] + rest
                                          | ')' ws -> [(symbol, first)] )

# compound_superposition:
add_cs = ws '+' ws compound_superposition:k -> ('sp +',k)
sub_cs = ws '-' ws compound_superposition:k -> ('sp -',k)
merge_cs = ws '_' ws compound_superposition:k -> ('sp _',k)
seq_cs = ws '.' ws compound_superposition:k -> ('sp .',k)
cs_ops = (add_cs | sub_cs | merge_cs | seq_cs)
op_like_cs = ws ( bracket_ops:ops | op_sequence:ops ) ws compound_superposition:sp -> ('op_cs',ops,sp)
bracketk_cs = ws '(' compound_superposition:first ( ws ',' ws compound_superposition){0,3}:rest ')' ws -> [first] + rest

compound_superposition = ws ( bracket_ops | op_sequence ):ops ws ( naked_ket:first | bracketk_cs:first | op_like_cs:first )  ws (cs_ops+:rest ws -> [ops, first] + rest
                                                                                                                                                    | ws -> [ops, first] )



full_bracketk_cs = ws '(' full_compound_superposition:first ( ws ',' ws full_compound_superposition){0,3}:rest ')' ws -> [first] + rest
single_op_like_cs = ws ( bracket_ops:ops | op_sequence:ops ) ws single_compound_superposition:sp -> ('op_cs',ops,sp)
single_compound_superposition = ws ( bracket_ops | op_sequence ):ops ws ( naked_ket:first | full_bracketk_cs:first | single_op_like_cs:first ) ws -> [ops, first]

symbol_single_compound_superposition = ws op_symbol:symbol ws single_compound_superposition:sp -> (symbol, sp)
full_compound_superposition = ws (op_symbol | -> '+'):symbol single_compound_superposition:first ws symbol_single_compound_superposition*:rest ws -> [(symbol, first)] + rest

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



# compound superposition test cases:
def test_simple_ket_1():
  x = op_grammar(' |fish>').compound_superposition()
  assert x == [[], 'fish']

def test_simple_ket_2():
  x = op_grammar(' 3|fish>').compound_superposition()
  assert x == [[3], 'fish']

def test_symbol_ket_1():
  x = op_grammar(' -|fish>').compound_superposition()
  assert x == ''

def test_symbol_ket_2():
  x = op_grammar(' +|fish>').compound_superposition()
  assert x == ''

def test_symbol_ket_3():
  x = op_grammar(' _|fish>').compound_superposition()
  assert x == ''

def test_symbol_ket_4():
  x = op_grammar(' .|fish>').compound_superposition()
  assert x == ''

def test_simple_ket_4():
  x = op_grammar(' -2.5|fish>').compound_superposition()
  assert x == [[-2.5], 'fish']

def test_simple_ket_op_1():
  x = op_grammar(' op|fish>').compound_superposition()
  assert x == [['op'], 'fish']

def test_simple_ket_op_2():
  x = op_grammar(' op |fish>').compound_superposition()
  assert x == [['op'], 'fish']



# bracketk_cs test cases:
def test_bracket_1():
  x = op_grammar(' ( |x> ) ').bracketk_cs()
  assert x == ''

def test_bracket_2():
  x = op_grammar(' ( |x>, |y> ) ').bracketk_cs()
  assert x == ''

def test_bracket_3():
  x = op_grammar(' ( |x>,|y>,|z> ) ').bracketk_cs()
  assert x == ''

def test_bracket_4():
  x = op_grammar(' ( |x> ,|y>, |z>, |u>) ').bracketk_cs()
  assert x == ''

# designed to fail. Testing {0,3}
#def test_bracket_5():
#  x = op_grammar(' ( |x>,|y>,|z>,|u>,|v> ) ').bracketk_cs()
#  assert x == ''



# single compound superposition test cases:
def test_simple_ket_1():
  x = op_grammar(' |fish>').single_compound_superposition()
  assert x == [[], 'fish']

def test_simple_ket_2():
  x = op_grammar(' 3|fish>').single_compound_superposition()
  assert x == [[3], 'fish']

def test_symbol_ket_1():
  x = op_grammar(' -|fish>').single_compound_superposition()
  assert x == ''

def test_symbol_ket_2():
  x = op_grammar(' +|fish>').single_compound_superposition()
  assert x == ''

def test_symbol_ket_3():
  x = op_grammar(' _|fish>').single_compound_superposition()
  assert x == ''

def test_symbol_ket_4():
  x = op_grammar(' .|fish>').single_compound_superposition()
  assert x == ''

def test_simple_ket_4():
  x = op_grammar(' -2.5|fish>').single_compound_superposition()
  assert x == [[-2.5], 'fish']

def test_simple_ket_op_1():
  x = op_grammar(' op|fish>').single_compound_superposition()
  assert x == [['op'], 'fish']

def test_simple_ket_op_2():
  x = op_grammar(' op |fish>').single_compound_superposition()
  assert x == [['op'], 'fish']


# full compound superposition test cases:
def test_fcs_simple_ket_1():
  x = op_grammar(' |fish>').full_compound_superposition()
  assert x == [('+', [[], 'fish'])]

def test_fcs_simple_ket_2():
  x = op_grammar(' 3|fish>').full_compound_superposition()
  assert x == [('+', [[3], 'fish'])]

def test_fcs_symbol_ket_1():
  x = op_grammar(' -|fish>').full_compound_superposition()
  assert x == [('-', [[], 'fish'])]

def test_fcs_symbol_ket_2():
  x = op_grammar(' +|fish>').full_compound_superposition()
  assert x == [('+', [[], 'fish'])]

def test_fcs_symbol_ket_3():
  x = op_grammar(' _|fish>').full_compound_superposition()
  assert x == [('_', [[], 'fish'])]

def test_fcs_symbol_ket_4():
  x = op_grammar(' .|fish>').full_compound_superposition()
  assert x == [('.', [[], 'fish'])]

def test_fcs_simple_ket_4():
  x = op_grammar(' -2.5|fish>').full_compound_superposition()
  assert x == [('-', [[2.5], 'fish'])]

def test_fcs_simple_ket_op_1():
  x = op_grammar(' op|fish>').full_compound_superposition()
  assert x == [('+', [['op'], 'fish'])]

def test_fcs_simple_ket_op_2():
  x = op_grammar(' op |fish>').full_compound_superposition()
  assert x == [('+', [['op'], 'fish'])]

def test_fcs_ket_sum_1():
  x = op_grammar(' 3|x> + |y> - 3.2|z> _ |c> + |d> . |e> + |f>').full_compound_superposition()
  assert x == [('+', [[3], 'x']), ('+', [[], 'y']), ('-', [[3.2], 'z']), ('_', [[], 'c']), ('+', [[], 'd']), ('.', [[], 'e']), ('+', [[], 'f'])]

def test_fcs_ket_sum_with_ops_1():
  x = op_grammar(' -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> ').full_compound_superposition()
  assert x == [('-', [['op3', 'op2', 'op1'], 'x']), ('+', [[9.99], 'y']), ('_', [['op5', 'op4'], 'z']), ('.', [['op6'], 'e'])]

def test_cs_ket_bracket_1():
  x = op_grammar(' ( 3|x> + |y> - 3.2|z> _ |c> + |d> . |e> + |f> )').full_compound_superposition()
  print(x)
  assert x == [('+', [[], [[('+', [[3], 'x']), ('+', [[], 'y']), ('-', [[3.2], 'z']), ('_', [[], 'c']), ('+', [[], 'd']), ('.', [[], 'e']), ('+', [[], 'f'])]]])]

def test_fcs_ket_bracket_with_ops_1():
  x = op_grammar(' ( -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> )').full_compound_superposition()
  print(x)
  assert x == [('+', [[], [[('-', [['op3', 'op2', 'op1'], 'x']), ('+', [[9.99], 'y']), ('_', [['op5', 'op4'], 'z']), ('.', [['op6'], 'e'])]]])]

def test_cs_ket_bracket_1_ops():
  x = op_grammar(' -op3 op2 ( 3|x> + |y> - 3.2|z> _ |c> + |d> . |e> + |f> )').full_compound_superposition()
  print(x)
  assert x == [('-', [['op3', 'op2'], [[('+', [[3], 'x']), ('+', [[], 'y']), ('-', [[3.2], 'z']), ('_', [[], 'c']), ('+', [[], 'd']), ('.', [[], 'e']), ('+', [[], 'f'])]]])]

def test_fcs_ket_bracket_with_ops_1_ops():
  x = op_grammar(' fish( -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> )').full_compound_superposition()
  print(x)
  assert x == [('+', [['fish'], [[('-', [['op3', 'op2', 'op1'], 'x']), ('+', [[9.99], 'y']), ('_', [['op5', 'op4'], 'z']), ('.', [['op6'], 'e'])]]])]

def test_fcs_ket_bracket_2():
  x = op_grammar(' (|x>, |y>) ').full_compound_superposition()
  print(x)
  assert x == [('+', [[], [[('+', [[], 'x'])], [('+', [[], 'y'])]]])]

def test_fcs_ket_bracket_2_ops():
  x = op_grammar('_op3 op2 (|x>, |y>) ').full_compound_superposition()
  print(x)
  assert x == [('_', [['op3', 'op2'], [[('+', [[], 'x'])], [('+', [[], 'y'])]]])]

def test_fcs_brackets_ops_bracket_op():
  x = op_grammar(' op5 (1 - op4 ) op2 op1 (3|x> + 0.2|z>) ').full_compound_superposition()
  print(x)
  assert x == [('+', [['op5'], ('op_cs', [('+', [1]), ('-', ['op4'])], [['op2', 'op1'], [[('+', [[3], 'x']), ('+', [[0.2], 'z'])]]])])]

def test_fcs_bracket_ops():
  x = op_grammar(' (1 - op2 _ op3 op4 . op5 + op6) |x> ').full_compound_superposition()
  print(x)
  assert x == [('+', [[('+', [1]), ('-', ['op2']), ('_', ['op3', 'op4']), ('.', ['op5']), ('+', ['op6'])], 'x'])]

def test_fcs_bracket_ops_2():
  x = op_grammar(' (1 - op2 _ op3 op4 . op5 + op6) -|x> ').full_compound_superposition()
  print(x)
  assert x == ''

def test_fcs_bracket_ops_3():
  x = op_grammar(' (1 - op2 _ op3 op4 . op5 + op6) -3.7|x> ').full_compound_superposition()
  print(x)
  assert x == [('+', [[('+', [1]), ('-', ['op2']), ('_', ['op3', 'op4']), ('.', ['op5']), ('+', ['op6'])], ('op_cs', [-3.7], [[], 'x'])])]

def test_fcs_empty_bracket():
  x = op_grammar(" () (3|x> + |y>) ").full_compound_superposition()
  print(x)
  assert x == [('+', [[('+', [])], [[('+', [[3], 'x']), ('+', [[], 'y'])]]])]

def test_fcs_op_sentence():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> ").full_compound_superposition() 
  print(x)
  assert x == [('+', [[(3, 2), ['common', 'friends'], 'split'], 'Fred Sam'])]

def test_fcs_op_sentence_sum():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> + |mice> + (|cats> + |dogs>) + split |horse pony mare> ").full_compound_superposition()
  print(x)
  assert x == [('+', [[(3, 2), ['common', 'friends'], 'split'], 'Fred Sam']), ('+', [[], 'mice']), ('+', [[], [[('+', [[], 'cats']), ('+', [[], 'dogs'])]]]), ('+', [['split'], 'horse pony mare'])]

def test_fcs_op_sentence_sum_v2():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> _ |mice> - (|cats> + |dogs>) . split |horse pony mare> ").full_compound_superposition()
  print(x)
  assert x == [('+', [[(3, 2), ['common', 'friends'], 'split'], 'Fred Sam']), ('_', [[], 'mice']), ('-', [[], [[('+', [[], 'cats']), ('+', [[], 'dogs'])]]]), ('.', [['split'], 'horse pony mare'])]

def test_fcs_sentence_v3():
  x = op_grammar(" op8 (op7) op5 (op4 - op2) sp(split|x y> - |z>) ").full_compound_superposition()
  print(x)
  assert x == [('+', [['op8'], ('op_cs', [('+', ['op7'])], [['op5'], ('op_cs', [('+', ['op4']), ('-', ['op2'])], [['sp'], [[('+', [['split'], 'x y']), ('-', [[], 'z'])]]])])])]


