#!/usr/bin/env python3

#######################################################################
# let's slowly build our parser!
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-1-25
# Update: 2018-2-4
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
context.load("sw-examples/fred-sam-friends.sw")
context.load("sw-examples/test-operators.sw")

logger.setLevel(logging.DEBUG)


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
fraction = number:numerator (ws '/' ws number | -> 1):denominator -> float_int(numerator/denominator)
#S0 = ' '*
S1 = ' '+
op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.')
valid_op_name = op_start_char:first <op_char*>:rest -> first + rest
simple_op = valid_op_name:s -> s
#parameters = (number | simple_op | '\"\"' | '*'):p -> p
parameters = (fraction | simple_op | '\"\"' | '*'):p -> str(p)

minus = '-' -> -1
compound_op = simple_op:the_op '[' parameters:first (',' ws parameters)*:rest ']' -> [the_op] + [first] + rest
general_op = (compound_op | simple_op | number | '\"\"' ):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op, power)
op = (powered_op | general_op):the_op -> the_op
op_sequence = (ws op:first (S1 op)*:rest ws -> [first] + rest)
              | ws -> []

op_symbol = ('+' | '-' | '__' | '.' | '_')
symbol_op_sequence = ws op_symbol:symbol ws op_sequence:seq -> (symbol, seq)
#bracket_ops = ws '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws (symbol_op_sequence+:rest ws ')' ws -> [(symbol, first)] + rest
#                                          | ')' ws -> [(symbol, first)] )
bracket_ops = ws '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws symbol_op_sequence*:rest ws ')' ws -> [[(symbol, first)] + rest]
bracketed_bracket_ops = ws '(' ws (bracket_ops | bracketed_bracket_ops):s ws ')' ws -> s

# compound_superposition:
add_cs = ws '+' ws compound_superposition:k -> ('sp +',k)
sub_cs = ws '-' ws compound_superposition:k -> ('sp -',k)
merge_cs = ws '_' ws compound_superposition:k -> ('sp _',k)
seq_cs = ws '.' ws compound_superposition:k -> ('sp .',k)
cs_ops = (add_cs | sub_cs | merge_cs | seq_cs)
op_like_cs = ws ( bracket_ops | op_sequence ):ops ws compound_superposition:sp -> ('op_cs', ops, sp)
bracketk_cs = ws '(' compound_superposition:first ( ws ',' ws compound_superposition){0,3}:rest ')' ws -> [first] + rest

compound_superposition = ws ( bracket_ops | op_sequence ):ops ws ( naked_ket:first | bracketk_cs:first | op_like_cs:first )  ws (cs_ops+:rest ws -> [ops, first] + rest
                                                                                                                                                    | ws -> [ops, first] )



full_bracketk_cs = ws '(' full_compound_superposition:first ( ws ',' ws full_compound_superposition){0,3}:rest ')' ws -> [first] + rest
single_op_like_cs = ws ( bracket_ops:ops | op_sequence:ops ) ws single_compound_superposition:sp -> ('op_cs',ops,sp)
single_compound_superposition = ws ( bracket_ops | bracketed_bracket_ops | op_sequence ):ops ws ( naked_ket:first | full_bracketk_cs:first | single_op_like_cs:first ) ws -> [ops, first]

symbol_single_compound_superposition = ws op_symbol:symbol ws single_compound_superposition:sp -> (symbol, sp)
full_compound_superposition = ws (op_symbol | -> '+'):symbol single_compound_superposition:first ws symbol_single_compound_superposition*:rest ws -> [(symbol, first)] + rest

compiled_compound_superposition = full_compound_superposition:sp -> compile_compound_superposition(sp)
compiled_compound_sequence = full_compound_superposition:sp -> compile_compound_sequence(sp)
"""

def float_int(x):
  if x.is_integer():
    return int(x)
  return x

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
      sp.merge_sp(superposition(*value))
    elif op == '.':
      seq += sp
      sp = superposition(*value)
  seq += sp
  return seq

def compile_compound_superposition(compound_superposition):
  print("cs: ",end='')
  pprint(compound_superposition)

  seq = sequence()
  sp = superposition()
  for sp2 in compound_superposition:
    symbol, (ops, object) = sp2
    print("symbol: ",end='')
    pprint(symbol)
    print('ops: ', end = '')
    pprint(ops)
    print("object: ",end='')
    pprint(object)

    the_sp = superposition()
    if type(object) is str:                                       # found a ket
      the_sp = superposition(object)

    if len(ops) > 0:
      python_code = "".join(process_single_op(op) for op in reversed(ops))
      logger.debug('python code: %s' % python_code)
      the_sp = eval('the_sp' + python_code)                        # yeah, risk of injection attacks. Need better approach!!

    if symbol == '+':
      sp.add_sp(the_sp)
    elif symbol == '-':
      sp.sub_sp(the_sp)
    elif symbol == '_':
      sp.merge_sp(the_sp)
    elif symbol == '.':
      seq += sp
      sp = the_sp
  seq += sp
  return seq    

def my_print(name, value=''):
  #return
  if value is '':
    print(name)
  else:
    print(name + ': ', end='')
    pprint(value)
    
def process_operators(ops, seq):
  if len(ops) == 0:
    return seq
  python_code = ''
  for op in reversed(ops):
    if type(op) is list and op[0][0] in ['+', '-', '_', '.']:       # is there a better way to select out bracket_ops?
      print('bracket_ops found')
      new_seq = sequence()
      for new_op in op:
        my_print('new op', new_op)

        symbol, ops = new_op
        my_print('symbol', symbol)
        my_print('ops', ops)

        the_seq = process_operators(ops, seq)
        my_print('the_seq', str(the_seq))

        if symbol == '+':
          new_seq.add_seq(the_seq)
        elif symbol == '-':
          new_seq.sub_seq(the_seq)
        elif symbol == '_':
          new_seq.merge_seq(the_seq)
        elif symbol == '__':
          new_seq.merge_seq(the_seq, ' ')
        elif symbol == '.':
          new_seq += the_seq
        my_print('new_seq', str(new_seq))
      seq = new_seq
      #continue
    else:
      python_code += process_single_op(op)
  logger.debug('process_operators: python code: %s' % python_code)
  if len(python_code) > 0:
     seq = eval('seq' + python_code)
  return seq

def compile_compound_sequence(compound_sequence):
  print("cs: ",end='')
  pprint(compound_sequence)

  seq = sequence([])
  for seq2 in compound_sequence:
    symbol, (ops, object) = seq2
    my_print('symbol', symbol)
    my_print('ops', ops)
    my_print('object', object)

    distribute = False
    the_seq = sequence([])
    if type(object) is str:                                       # found a ket
      the_seq = sequence(superposition(object))

    elif type(object) is list:
      my_print('bracketk_cs found')
      distribute = True
      if len(ops) == 0 or type(ops[-1]) is not str:
        if len(object) == 1:
          the_seq = compile_compound_sequence(object[0])
        else:
          the_seq = sequence([])                                     # probably don't need this branch.
      else:
        seq_list = [compile_compound_sequence(x) for x in object]
        str_seq_list = [str(x) for x in seq_list]
        my_print('str_seq_list', str_seq_list)
        fnk = ops[-1]                                                # need to check type(fnk) is str.
        new_ops = ops[:-1]
        my_print('fnk', fnk)
        my_print('new_ops', new_ops)

        if len(object) == 1 and fnk not in whitelist_table_1:
          the_seq = seq_list[0]
        else:
          python_code = ''
          if len(seq_list) == 1:                                    # 1-parameter function:
            if fnk in whitelist_table_1:
              python_code = "%s(*seq_list)" % whitelist_table_1[fnk]
          if len(seq_list) == 2:                                    # 2-parameter function:
            if fnk in whitelist_table_2:
              python_code = "%s(*seq_list)" % whitelist_table_2[fnk]
          elif len(seq_list) == 3:                                  # 3-parameter function:
            if fnk in whitelist_table_3:
              python_code = "%s(*seq_list)" % whitelist_table_3[fnk]
          elif len(seq_list) == 4:                                  # 4-parameter function:
            if fnk in whitelist_table_4:
              python_code = "%s(*seq_list)" % whitelist_table_4[fnk]
          if len(python_code) > 0:
            my_print("whitelist_table: python code", python_code)
            the_seq = eval(python_code)
          ops = new_ops
#            ops = new_ops

    elif type(object) is tuple:
      prefix, tuple_ops, tuple_rest = object
      if prefix != 'op_cs':
        logger.warning('wrong prefix: %s' % prefix)
      my_print('tuple_ops', tuple_ops)
      my_print('tuple_rest', tuple_rest)
      if tuple_rest[0] == []:
        new_tuple_object = [('+', [tuple_ops, tuple_rest[1]])]
        my_print('new_tuple_object', new_tuple_object)
        the_seq = compile_compound_sequence(new_tuple_object)
      else:
        new_tuple_object = [('+', tuple_rest)]
        tuple_seq = compile_compound_sequence(new_tuple_object)
        the_seq = process_operators(tuple_ops, tuple_seq)

    else:
      logger.warning('unknown object type!')

    my_print('\n----------\nfinal')
    my_print('ops', ops)
    my_print('the_seq', str(the_seq))
    my_print('distribute', distribute)
    my_print('----------\n')
    the_seq = process_operators(ops, the_seq)

    if symbol == '+':
      seq.add_seq(the_seq)
    elif symbol == '-':
      seq.sub_seq(the_seq)
    elif symbol == '_':
      if not distribute:
        seq.merge_seq(the_seq)
      if distribute:
        seq.distribute_merge_seq(the_seq)
    elif symbol == '__':
      if not distribute:
        seq.merge_seq(the_seq, ' ')
      if distribute:
        seq.distribute_merge_seq(the_seq, ' ')
    elif symbol == '.':
      seq += the_seq
  return seq


bindings_dictionary = {
  'ket_calculate'                  : ket_calculate,
  'compile_compound_superposition' : compile_compound_superposition,
  'compile_compound_sequence'      : compile_compound_sequence,
  'float_int'                      : float_int,
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
#  assert str(x) == '|a> + 2.1|b> + |cd> + |e> + |f>'
#  assert str(x) == '|a> + 2.1|b> + 3|cd> + |e> + |f>'
  assert str(x) == '|a> + 2.1|b> + 23.7|cd> + |e> + |f>'

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
  #assert x == [('+', [])]
  assert x == [[('+', [])]]

def test_bracket_ops_simple():
  x = op_grammar(' (op2 - 2 op1) ').bracket_ops()
  #assert x == [('+', ['op2']), ('-', [2, 'op1'])]
  assert x == [[('+', ['op2']), ('-', [2, 'op1'])]]

def test_bracket_ops_complex():
  x = op_grammar(' (op6^3 op5 + op4 op3[fish]^2 op2 - 2 op1) ').bracket_ops()
  #assert x == [('+', [('op6', 3), 'op5']), ('+', ['op4', (['op3', 'fish'], 2), 'op2']), ('-', [2, 'op1'])]
  assert x == [[('+', [('op6', 3), 'op5']), ('+', ['op4', (['op3', 'fish'], 2), 'op2']), ('-', [2, 'op1'])]]

def test_bracket_ops_merge_and_seq():
  x = op_grammar(' ( op6 op5 _ op4 . op3 op2 + op1 op - foo1^7 ) ').bracket_ops()
  #assert x == [('+', ['op6', 'op5']), ('_', ['op4']), ('.', ['op3', 'op2']), ('+', ['op1', 'op']), ('-', [('foo1', 7)])]
  assert x == [[('+', ['op6', 'op5']), ('_', ['op4']), ('.', ['op3', 'op2']), ('+', ['op1', 'op']), ('-', [('foo1', 7)])]]

def test_op_subtraction_1():
  x = op_grammar(' (op2 - 2 op1 )').bracket_ops()
  #assert x == [('+', ['op2']), ('-', [2, 'op1'])]
  assert x == [[('+', ['op2']), ('-', [2, 'op1'])]]

def test_op_subtraction_2():
  x = op_grammar(' (-op2 + 2 op1)').bracket_ops()
  #assert x == [('-', ['op2']), ('+', [2, 'op1'])]
  assert x == [[('-', ['op2']), ('+', [2, 'op1'])]]



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
  assert x == [[[], 'x']]

def test_bracket_2():
  x = op_grammar(' ( |x>, |y> ) ').bracketk_cs()
  assert x == [[[], 'x'], [[], 'y']]

def test_bracket_3():
  x = op_grammar(' ( |x>,|y>,|z> ) ').bracketk_cs()
  assert x == [[[], 'x'], [[], 'y'], [[], 'z']]

def test_bracket_4():
  x = op_grammar(' ( |x> ,|y>, |z>, |u>) ').bracketk_cs()
  assert x == [[[], 'x'], [[], 'y'], [[], 'z'], [[], 'u']]

# designed to fail. Testing {0,3}
#def test_bracket_5():
#  x = op_grammar(' ( |x>,|y>,|z>,|u>,|v> ) ').bracketk_cs()
#  assert x == ''


def test_bracket_bracket_1():
  x = op_grammar(' (( |x> )) ').bracketk_cs()
  assert x == [[[], [[[], 'x']]]]

def test_bracket_bracket_2():
  x = op_grammar(' (( |x>, |y> )) ').bracketk_cs()
  assert x == [[[], [[[], 'x'], [[], 'y']]]]

def test_bracket_bracket_3():
  x = op_grammar(' (( |x>,|y>,|z> ) )').bracketk_cs()
  assert x == [[[], [[[], 'x'], [[], 'y'], [[], 'z']]]]

def test_bracket_bracket_4():
  x = op_grammar(' (  ( |x> ,|y>, |z>, |u>) )').bracketk_cs()
  assert x == [[[], [[[], 'x'], [[], 'y'], [[], 'z'], [[], 'u']]]]




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
  #assert x == [('+', [['op5'], ('op_cs', [('+', [1]), ('-', ['op4'])], [['op2', 'op1'], [[('+', [[3], 'x']), ('+', [[0.2], 'z'])]]])])]
  assert x == [('+', [['op5'], ('op_cs', [[('+', [1]), ('-', ['op4'])]], [['op2', 'op1'], [[('+', [[3], 'x']), ('+', [[0.2], 'z'])]]])])]

def test_fcs_bracket_ops():
  x = op_grammar(' (1 - op2 _ op3 op4 . op5 + op6) |x> ').full_compound_superposition()
  print(x)
  #assert x == [('+', [[('+', [1]), ('-', ['op2']), ('_', ['op3', 'op4']), ('.', ['op5']), ('+', ['op6'])], 'x'])]
  assert x == [('+', [[[('+', [1]), ('-', ['op2']), ('_', ['op3', 'op4']), ('.', ['op5']), ('+', ['op6'])]], 'x'])]

def test_fcs_bracket_ops_2():
  x = op_grammar(' (1 - op2 _ op3 op4 . op5 + op6) -|x> ').full_compound_superposition()
  print(x)
  assert x == ''

def test_fcs_bracket_ops_3():
  x = op_grammar(' (1 - op2 _ op3 op4 . op5 + op6) -3.7|x> ').full_compound_superposition()
  print(x)
  #assert x == [('+', [[('+', [1]), ('-', ['op2']), ('_', ['op3', 'op4']), ('.', ['op5']), ('+', ['op6'])], ('op_cs', [-3.7], [[], 'x'])])]
  assert x == [('+', [[[('+', [1]), ('-', ['op2']), ('_', ['op3', 'op4']), ('.', ['op5']), ('+', ['op6'])]], ('op_cs', [-3.7], [[], 'x'])])]

def test_fcs_empty_bracket():
  x = op_grammar(" () (3|x> + |y>) ").full_compound_superposition()
  print(x)
  #assert x == [('+', [[('+', [])], [[('+', [[3], 'x']), ('+', [[], 'y'])]]])]
  assert x == [('+', [[[('+', [])]], [[('+', [[3], 'x']), ('+', [[], 'y'])]]])]

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
  #assert x == [('+', [['op8'], ('op_cs', [('+', ['op7'])], [['op5'], ('op_cs', [('+', ['op4']), ('-', ['op2'])], [['sp'], [[('+', [['split'], 'x y']), ('-', [[], 'z'])]]])])])]
  assert x == [('+', [['op8'], ('op_cs', [[('+', ['op7'])]], [['op5'], ('op_cs', [[('+', ['op4']), ('-', ['op2'])]], [['sp'], [[('+', [['split'], 'x y']), ('-', [[], 'z'])]]])])])]


# compile compound superposition test cases:
def test_cfcs_simple_ket_1():
  x = op_grammar(' |fish>').compiled_compound_superposition()
  assert str(x) == '|fish>'

def test_cfcs_simple_ket_2():
  x = op_grammar(' 3|fish>').compiled_compound_superposition()
  assert str(x) == '3|fish>'

def test_cfcs_symbol_ket_1():
  x = op_grammar(' -|fish>').compiled_compound_superposition()
  assert str(x) == '-1|fish>'

def test_cfcs_symbol_ket_2():
  x = op_grammar(' +|fish>').compiled_compound_superposition()
  assert str(x) == '|fish>'

def test_cfcs_symbol_ket_3():
  x = op_grammar(' _|fish>').compiled_compound_superposition()
  assert str(x) == '|fish>'

def test_cfcs_symbol_ket_4():
  x = op_grammar(' .|fish>').compiled_compound_superposition()
  assert str(x) == '|> . |fish>'

def test_cfcs_simple_ket_4():
  x = op_grammar(' -2.5|fish>').compiled_compound_superposition()
  assert str(x) == '-2.5|fish>'

def test_cfcs_simple_ket_op_1():
  x = op_grammar(' op|fish>').compiled_compound_superposition()
  assert str(x) == '|op: fish>'

def test_cfcs_simple_ket_op_2():
  x = op_grammar(' op |fish>').compiled_compound_superposition()
  assert str(x) == '|op: fish>'


# [('+', [[3], 'x']), ('+', [[], 'y']), ('-', [[3.2], 'z']), ('_', [[], 'c']), ('+', [[], 'd']), ('.', [[], 'e']), ('+', [[], 'f'])]
def test_cfcs_ket_sum_1():
  x = op_grammar(' 3|x> + |y> - 3.2|z> _ |c> + |d> . |e> + |f>').compiled_compound_superposition()
  assert str(x) == '3|x> + |y> + -3.2|zc> + |d> . |e> + |f>'

def test_cfcs_ket_sum_2():
  x = op_grammar(' 3|x> + |y> + -3.2|zc> + |d> . |e> + |f>').compiled_compound_superposition()
  assert str(x) == '3|x> + |y> + -3.2|zc> + |d> . |e> + |f>'
  x.display()
  assert True

# [('-', [['op3', 'op2', 'op1'], 'x']), ('+', [[9.99], 'y']), ('_', [['op5', 'op4'], 'z']), ('.', [['op6'], 'e'])]
def test_cfcs_ket_sum_with_ops_1():
  x = op_grammar(' -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> ').compiled_compound_superposition()
  assert str(x) == '-1|op3: op2: op1: x> + 9.99|yop5: op4: z> . |op6: e>'

# [('+', [[], [[('-', [['op3', 'op2', 'op1'], 'x']), ('+', [[9.99], 'y']), ('_', [['op5', 'op4'], 'z']), ('.', [['op6'], 'e'])]]])]
def test_fcs_ket_bracket_with_ops_1():
  x = op_grammar(' ( -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> )').compiled_compound_superposition()
  assert str(x) == ''


# compile compound sequence test cases:
def test_cfcseq_simple_ket_1():
  x = op_grammar(' |fish>').compiled_compound_sequence()
  assert str(x) == '|fish>'

def test_cfcseq_simple_ket_2():
  x = op_grammar(' 3|fish>').compiled_compound_sequence()
  assert str(x) == '3|fish>'

def test_cfcseq_symbol_ket_1():
  x = op_grammar(' -|fish>').compiled_compound_sequence()
  assert str(x) == '-1|fish>'

def test_cfcseq_symbol_ket_2():
  x = op_grammar(' +|fish>').compiled_compound_sequence()
  assert str(x) == '|fish>'

def test_cfcseq_symbol_ket_3():
  x = op_grammar(' _|fish>').compiled_compound_sequence()
  assert str(x) == '|fish>'

def test_cfcseq_symbol_ket_4():
  x = op_grammar(' .|fish>').compiled_compound_sequence()
  assert str(x) == ''

def test_cfcseq_simple_ket_4():
  x = op_grammar(' -2.5|fish>').compiled_compound_sequence()
  assert str(x) == '-2.5|fish>'

def test_cfcseq_simple_ket_op_1():
  x = op_grammar(' op|fish>').compiled_compound_sequence()
  assert str(x) == '|op: fish>'

def test_cfcseq_simple_ket_op_2():
  x = op_grammar(' op |fish>').compiled_compound_sequence()
  assert str(x) == '|op: fish>'

# [('+', [[3], 'x']), ('+', [[], 'y']), ('-', [[3.2], 'z']), ('_', [[], 'c']), ('+', [[], 'd']), ('.', [[], 'e']), ('+', [[], 'f'])]
def test_cfcseq_ket_sum_1():
  x = op_grammar(' 3|x> + |y> - 3.2|z> _ |c> + |d> . |e> + |f>').compiled_compound_sequence()
  x.display()
  assert str(x) == '3|x> + |y> + -3.2|zc> + |d> . |e> + |f>'

def test_cfcseq_ket_sum_2():
  x = op_grammar(' 3|x> + |y> + -3.2|zc> + |d> . |e> + |f>').compiled_compound_sequence()
  assert str(x) == '3|x> + |y> + -3.2|zc> + |d> . |e> + |f>'
  x.display()
  assert True

# [('-', [['op3', 'op2', 'op1'], 'x']), ('+', [[9.99], 'y']), ('_', [['op5', 'op4'], 'z']), ('.', [['op6'], 'e'])]
def test_cfcseq_ket_sum_with_ops_1():
  x = op_grammar(' -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> ').compiled_compound_sequence()
  assert str(x) == '-1|op3: op2: op1: x> + 9.99|yop5: op4: z> . |op6: e>'

# [('+', [[], [[('-', [['op3', 'op2', 'op1'], 'x']), ('+', [[9.99], 'y']), ('_', [['op5', 'op4'], 'z']), ('.', [['op6'], 'e'])]]])]
def test_cfcseq_ket_bracket_with_ops_1():
  x = op_grammar(' ( -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> )').compiled_compound_sequence()
  assert str(x) == '-1|op3: op2: op1: x> + 9.99|yop5: op4: z> . |op6: e>'

def test_cfcseq_ket_sum_with_brackets_3():
  x = op_grammar(' ((   ( -op3 op2 op1 |x> + 9.99|y> _ op5 op4 |z> . op6 |e> )))').compiled_compound_sequence()
  assert str(x) == '-1|op3: op2: op1: x> + 9.99|yop5: op4: z> . |op6: e>'

def test_cfcseq_op_brackets_1():
  x = op_grammar(' op1 ( |x> + 9.99|y> . |z> _ |a> + |b> ) ').compiled_compound_sequence()
  x.display()
  assert str(x) == '|op1: x> + 9.99|op1: y> . |op1: za> + |op1: b>'



def test_cfcseq_tuple_op_1():
  x = op_grammar('(op2 op1) |x> + |y> - |z>   ' ).compiled_compound_sequence()
  assert str(x) == '|op2: op1: x> + |y> + -1|z>'

def test_cfcseq_tuple_op_2():
  x = op_grammar('(- op2 op1) |x> + |y> - |z>   ' ).compiled_compound_sequence()
  assert str(x) == '-1|op2: op1: x> + |y> + -1|z>'

def test_cfcseq_tuple_op_3():
  x = op_grammar('- (op2 op1) |x> + |y> - |z>   ' ).compiled_compound_sequence()
  assert str(x) == '-1|op2: op1: x> + |y> + -1|z>'

def test_cfcseq_tuple_op_4():
  x = op_grammar('(- op4 + op3 _ op2 . op1) |x>   ' ).compiled_compound_sequence()
  assert str(x) == '-1|op4: x> + |op3: xop2: x> . |op1: x>'

def test_cfcseq_tuple_op_4_bracket():
  x = op_grammar(' ((- op4 + op3 _ op2 . op1)) |x>   ' ).compiled_compound_sequence()
  assert str(x) == '-1|op4: x> + |op3: xop2: x> . |op1: x>'


def test_cfcseq_tuple_op_4_op():
  x = op_grammar('op5 (- op4 + op3 _ op2 . op1) |x>   ' ).compiled_compound_sequence()
  assert str(x) == '-1|op5: op4: x> + |op5: op3: xop2: x> . |op5: op1: x>'

def test_cfcseq_tuple_op_4_bracket_op():
  x = op_grammar(' op5((- op4 + op3 _ op2 . op1)) |x>   ' ).compiled_compound_sequence()
  assert str(x) == '-1|op5: op4: x> + |op5: op3: xop2: x> . |op5: op1: x>'


def test_cfcseq_tuple_op_object():
  x = op_grammar('(op3 op2) op1 |x> ' ).compiled_compound_sequence()
  assert str(x) == '|op3: op2: op1: x>'


def test_cfcseq_powered_op_1():
  x = op_grammar(' op1^3 |x> ').compiled_compound_sequence()
  assert str(x) == '|op1: op1: op1: x>'

def test_simple_op():
  x = op_grammar(' op1 |x> ').compiled_compound_sequence()
  assert str(x) == '|op1: x>'

def test_cfcseq_tuple_ops():
  x = op_grammar(' op6 (op5 op4) op3 (op2) op1 |x> . op3|y> + op7|z> ').compiled_compound_sequence()
  assert str(x) == '|op6: op5: op4: op3: op2: op1: x> . |op3: y> + |op7: z>'


def test_cfcseq_op_sentence_sum():
  x = op_grammar(' 3^2 common[friends] split |Fred Sam> + |mice> + (|cats> + |dogs>) + split |horse pony mare> ').compiled_compound_sequence()
  print(x)
  assert str(x) == '9|Jack> + 9|Emma> + 9|Charlie> + |mice> + |cats> + |dogs> + |horse> + |pony> + |mare>'

def test_cfcseq_op_sentence_sum_v2():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> _ |mice> - (|cats> + |dogs>) . split |horse pony mare> ").compiled_compound_sequence()
  print(x)
  assert str(x) == '9|Jack> + 9|Emma> + 9|Charliemice> + -1|cats> + -1|dogs> . |horse> + |pony> + |mare>'

def test_cfcseq_op_sentence_short():
  x = op_grammar(' 3^2 common[friends] split |Fred Sam> ').compiled_compound_sequence()
  print(x)
  assert str(x) == '9|Jack> + 9|Emma> + 9|Charlie>'

def test_cfcseq_simple_bracket_op():
  x = op_grammar(' (op) |x> ').compiled_compound_sequence()
  assert str(x) == '|op: x>'

def test_cfcseq_simple_bracket_op_multi_2():
  x = op_grammar(' ((op)) |x> ').compiled_compound_sequence()
  assert str(x) == '|op: x>'

def test_cfcseq_simple_bracket_op_multi_5():
  x = op_grammar(' (( (((op)) ))  )|x> ').compiled_compound_sequence()
  assert str(x) == '|op: x>'



def test_cfcseq_op_sequence_1():
  x = op_grammar("  foo bah fish[x,y,13.2] select[1,3]^2  |x> ").compiled_compound_sequence()
  assert str(x) == ''

def test_cfcseq_empty_bracket():
  x = op_grammar(' (|x> , |y> , |z>) ').compiled_compound_sequence()
  assert str(x) == '|>'

def test_cfcseq_op_bracket_1():
  x = op_grammar(' fnk (|x> , |y> , |z>) ').compiled_compound_sequence()
  assert str(x) == '|>'

def test_cfcseq_op_bracket_2():
  x = op_grammar(' op1 fnk (|x> , |y> , |z>) ').compiled_compound_sequence()
  assert str(x) == '|op1: >'

def test_cfcseq_op_bracket_union():
  x = op_grammar(' op1 union (|x> , |y> , |z>) ').compiled_compound_sequence()
  assert str(x) == '|op1: x> + |op1: y> + |op1: z>'

def test_cfcseq_bracket_union():
  x = op_grammar(' union (|x> , |y> , |z>) ').compiled_compound_sequence()
  assert str(x) == '|x> + |y> + |z>'

def test_cfcseq_bracket_union_sequence():
  x = op_grammar(' union (|x> , |y> . |z>) ').compiled_compound_sequence()
  assert str(x) == '|x> + |y> . |z>'

def test_cfcseq_bracket_intersection_sequence():
  x = op_grammar(' intersection (|x> , |y> . |z>) ').compiled_compound_sequence()
  assert str(x) == '|> . |>'


# not sure we want the next three to make sense:
def test_cfcseq_bracket_union_sequence_multi_bracket():
  x = op_grammar(' union ((((|x> , |y> . |z>) ) ) ) ').compiled_compound_sequence()
  assert str(x) == '|>'

def test_cfcseq_bracket_intersection_sequence_multi_bracket():
  x = op_grammar(' intersection ((|x> , |y> . |z>)) ').compiled_compound_sequence()
  assert str(x) == '|>'

def test_cfcseq_bracket_union_sequence_multi_bracket():
  x = op_grammar(' sp ((((|x> , |y> . |z>) ) ) ) ').compiled_compound_sequence()
  assert str(x) == '|sp>'


# variants that should make sense:
def test_cfcseq_bracket_union_sequence_multi_bracket_wrapper():
  x = op_grammar(' (((union(|x> , |y> . |z>) ) ) ) ').compiled_compound_sequence()
  assert str(x) == '|x> + |y> . |z>'

def test_cfcseq_bracket_intersection_sequence_multi_bracket_wrapper():
  x = op_grammar(' ((intersection (|x> , |y> . |z>))) ').compiled_compound_sequence()
  assert str(x) == '|> . |>'

def test_cfcseq_bracket_union_sequence_multi_bracket_sp():
  x = op_grammar(' sp ((((|x> + |y> . |z>) ) ) ) ').compiled_compound_sequence()
  assert str(x) == '|sp> + |x> + |y> . |z>'




def test_cfcseq_bracket_intersection_split():
  x = op_grammar(' intersection (2.5 split|x y z> , 3 split|a x b>) ').compiled_compound_sequence()
  assert str(x) == '2.5|x>'

def test_cfcseq_bracket_intersection_union():
  x = op_grammar(' union (2.5 split|x y z> , 3 split|a x b>) ').compiled_compound_sequence()
  assert str(x) == '3|x> + 2.5|y> + 2.5|z> + 3|a> + 3|b>'

def test_cfcseq_split_ket():
  x = op_grammar(' 2.5 split |x y z> ').compiled_compound_sequence()
  assert str(x) == '2.5|x> + 2.5|y> + 2.5|z>'

def test_cfcseq_op_empty():
  x = op_grammar(' op1 |> ').compiled_compound_sequence()
  assert str(x) == '|op1: >'

def test_cfcseq_op_simple():
  x = op_grammar(' op1 |a> ').compiled_compound_sequence()
  assert str(x) == '|op1: a>'

def test_cfcseq_apply_op_empty():
  x = ket('').apply_op(context, 'op1')
  assert str(x) == '|op1: >'

def test_cfcseq_apply_op_simple():
  x = ket('a').apply_op(context, 'op1')
  assert str(x) == '|op1: a>'

def test_cfcseq_sequence_apply_op_empty_1():
  x = sequence().apply_op(context, 'op1')
  assert str(x) == '|op1: >'

def test_cfcseq_sequence_apply_op_empty_2():
  x = sequence('').apply_op(context, 'op1')
  assert str(x) == '|op1: >'

def test_cfcseq_sequence_apply_op_empty_3():
  x = sequence([]).apply_op(context, 'op1')
  assert str(x) == '|op1: >'


def test_cfcseq_sequence_apply_op_simple():
  x = sequence('a').apply_op(context, 'op1')
  assert str(x) == '|op1: a>'


def test_grammar_compound_superposition_sp_ket():
  x = op_grammar(' sp |x> ').compiled_compound_sequence()
  assert str(x) == '|sp: x>'

def test_grammar_compound_superposition_sp_bracket_ket():
  x = op_grammar(' sp (|x>) ').compiled_compound_sequence()
  assert str(x) == '|sp> + |x>'
  
def test_grammar_compound_superposition_sp_bracket_sp():
  x = op_grammar(' sp (|x> + |y> + |z>) ').compiled_compound_sequence()
  assert str(x) == '|sp> + |x> + |y> + |z>'  

def test_grammar_compound_superposition_naked_fn2():
  x = op_grammar(' ( |x>,|y> ) ').compiled_compound_sequence()
  assert str(x) == '|>'



# test multiple brackets:
def test_grammar_compound_superposition_sp_bracket_ket_bracket():
  x = op_grammar(' sp ( (|x>)) ').compiled_compound_sequence()
  assert str(x) == '|sp> + |x>'

def test_grammar_compound_superposition_sp_bracket_sp_bracket():
  x = op_grammar(' sp ((|x> + |y> + |z>)) ').compiled_compound_sequence()
  assert str(x) == '|sp> + |x> + |y> + |z>'

def test_grammar_compound_superposition_naked_fn2_bracket():
  x = op_grammar(' (( |x>,|y> ) )').compiled_compound_sequence()
  assert str(x) == '|>'


def test_grammar_compound_superposition_sp_bracket_ket_bracket_multi():
  x = op_grammar(' sp ((( (|x>)) ) ) ').compiled_compound_sequence()
  assert str(x) == '|sp> + |x>'

def test_grammar_compound_superposition_sp_bracket_sp_bracket_multi():
  x = op_grammar(' sp (((((|x> + |y> + |z>))))) ').compiled_compound_sequence()
  assert str(x) == '|sp> + |x> + |y> + |z>'

def test_grammar_compound_superposition_naked_fn2_bracket_multi():
  x = op_grammar(' (((( |x>,|y> ) )))').compiled_compound_sequence()
  assert str(x) == '|>'



def test_grammar_compound_superposition_bracket_sp_big_brackets():
  x = op_grammar(' ( |x> + 0.5|y> + 2.7|z> ) + ((|fish> + (|cats> + |dogs>)) + |mice>) + |rats> ').compiled_compound_sequence()
  assert str(x) == '|x> + 0.5|y> + 2.7|z> + |fish> + |cats> + |dogs> + |mice> + |rats>'

def test_grammar_compound_superposition_bracket_sp_big_brackets_merge():
  x = op_grammar(' ( |x> + 0.5|y> + 2.7|z> ) + ((|fish> _ (|cats> + |dogs>)) + |mice>) + |rats> ').compiled_compound_sequence()
  assert str(x) == '|x> + 0.5|y> + 2.7|z> + |fishcats> + |fishdogs> + |mice> + |rats>'

def test_grammar_compound_superposition_bracket_sp_big_brackets_subtract():
  x = op_grammar(' ( |x> + 0.5|y> + 2.7|z> ) + ((|fish> - (|cats> + |dogs>)) + |mice>) + |rats> ').compiled_compound_sequence()
  assert str(x) == '|x> + 0.5|y> + 2.7|z> + |fish> + -1|cats> + -1|dogs> + |mice> + |rats>'


def test_ket_bracket_merge():
  x = op_grammar(' |fish> _ |cats> + |dogs> ').compiled_compound_sequence()
  assert str(x) == '|fishcats> + |dogs>'

def test_ket_bracket_merge_bracket():
  x = op_grammar(' |fish> _ (|cats> + |dogs>) ').compiled_compound_sequence()
  assert str(x) == '|fishcats> + |fishdogs>'

def test_ket_bracket_merge_union_bracket():
  x = op_grammar(' |fish> _ union(|cats>, |dogs>) ').compiled_compound_sequence()
  assert str(x) == '|fishcats> + |fishdogs>'


def test_common_friends():
  x = op_grammar(' common[friends] (|Fred> + |Sam>) ').compiled_compound_sequence()
  assert str(x) == '|Jack> + |Emma> + |Charlie>'


def test_double_merge():
  x = op_grammar(' op1 |x> __ op3 op2 |y> __ |z> ').compiled_compound_sequence()
  assert str(x) == '|op1: x op3: op2: y z>'

def test_double_merge_single():
  x = op_grammar(' op1 |x> __ op3 op2 |y> __ |z> _ |fish> ').compiled_compound_sequence()
  assert str(x) == '|op1: x op3: op2: y zfish>'

def test_temperature_conversion_1():
  x = op_grammar(' |F:> __ round[2] plus[32] times-by[9/5] extract-value |C: 37> ').compiled_compound_sequence()
  assert str(x) == '|F: 98.6>'

def test_temperature_conversion_2():
  x = op_grammar(' |F:> __ round[2] minus[459.67] times-by[9/5] extract-value |K: 200> ').compiled_compound_sequence()
  assert str(x) == '|F: -99.67>'
