#!/usr/bin/env python3

#######################################################################
# let's slowly build our parser!
# v2
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-2-4
# Update: 2018-2-6
# Copyright: GPLv3
#
# Usage: py.test -v test_parser_v2.py
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

op_symbol = ('+' | '-' | '__' | '.' | '_')
symbol_ket = ws op_symbol:symbol ws coeff_ket:k -> (symbol, k)
literal_sequence = ws signed_ket:left ws symbol_ket*:right ws -> ket_calculate(left, right)


positive_int = <digit+>:n -> int(n)
fraction = number:numerator (ws '/' ws number | -> 1):denominator -> float_int(numerator/denominator)
#S0 = ' '*
ws = ' '*
S1 = ' '+
op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.')
simple_op = op_start_char:first <op_char*>:rest -> first + rest
parameters = (fraction | simple_op | '\"\"' | '*'):p -> str(p)

compound_op = simple_op:the_op '[' parameters:first (',' ws parameters)*:rest ']' -> ['c_op', the_op] + [first] + rest
#function_op = simple_op:the_op '(' ws literal_sequence:first (',' ws literal_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
function_op = simple_op:the_op '(' ws full_compound_sequence:first (',' ws full_compound_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
#function_op = simple_op:the_op ws '(' ws full_compound_sequence:first (',' ws full_compound_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
general_op = (bracket_ops | compound_op | function_op | simple_op | number | '\"\"' ):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op, power)

op = (powered_op | general_op):the_op -> the_op
op_sequence = (ws op:first (S1 op)*:rest ws -> [first] + rest)
              | ws -> []
symbol_op_sequence = ws op_symbol:symbol ws op_sequence:seq -> (symbol, seq)
#bracket_ops = '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws symbol_op_sequence*:rest ws ')' -> [[(symbol, first)] + rest]
bracket_ops = '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws symbol_op_sequence*:rest ws ')' -> [(symbol, first)] + rest

#single_compound_sequence = op_sequence:ops naked_ket:first -> [ops, first]
#single_compound_sequence = op_sequence:ops (naked_ket | -> ''):first -> [ops, first]
bracket_sequence = '(' ws full_compound_sequence:seq ws ')' -> seq
single_compound_sequence = op_sequence:ops (naked_ket | bracket_sequence | -> ''):first -> [ops, first]

symbol_single_compound_sequence = ws op_symbol:symbol ws single_compound_sequence:seq -> (symbol, seq)
full_compound_sequence = ws (op_symbol | -> '+'):symbol single_compound_sequence:first ws symbol_single_compound_sequence*:rest ws -> [(symbol, first)] + rest

compiled_compound_sequence = full_compound_sequence:seq -> compile_compound_sequence(seq)

new_line = ('\r\n' | '\r' | '\n')
#char = :c ?(is_not_newline(c)) -> c
char = ~new_line anything
string = <char*>:s -> s
#string = <~new_line anything>*:s -> "".join(s)
object = (naked_ket | '(*)' | '(*,*)' | '(*,*,*)' ):obj -> obj
stored_rule = ws (simple_op | -> ''):prefix_op ws object:obj ws ('#=>' | '!=>'):rule ws string:s -> learn_stored_rule(context, prefix_op, obj, rule, s)
#memoizing_rule = ws (simple_op | -> ''):prefix_op ws object:obj ws '!=>' ws string:s -> learn_memoizing_rule(context, prefix_op, obj, s)
learn_rule =  ws (simple_op | -> ''):prefix_op ws object:obj ws ('=>' | '+=>'):rule ws compiled_compound_sequence:seq -> learn_standard_rule(context, prefix_op, obj, rule, seq)
recall_rule = ws (simple_op | "\'\'" ):prefix_op ws object:obj -> recall_rule(context, prefix_op, obj)

sw_file = (learn_rule | stored_rule | new_line)*
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
    elif op == '__':
      sp.merge_sp(superposition(*value), ' ')
    elif op == '.':
      seq += sp
      sp = superposition(*value)
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
    if type(op) is list:                                      # found either a compound-op, a function-op or bracket-ops
      my_print('op[0]', op[0])
      if op[0] is 'c_op':
        my_print('compound_op')
        python_code = process_single_op(op[1:])
        if len(python_code) > 0:
          seq = eval('seq' + python_code)
      elif op[0] is 'f_op':
        my_print('function_op')
        null, fnk, *data = op
        my_print('fnk', fnk)
        my_print('data', data)

        python_code = ''
        if len(data) == 1:                                    # 1-parameter function:
          if fnk in whitelist_table_1:
            python_code = "%s(*seq_list)" % whitelist_table_1[fnk]
          else:
            the_seq = compile_compound_sequence(data[0])
            seq = process_operators([fnk], the_seq)
        if len(data) == 2:                                    # 2-parameter function:
          if fnk in whitelist_table_2:
            python_code = "%s(*seq_list)" % whitelist_table_2[fnk]
        elif len(data) == 3:                                  # 3-parameter function:
          if fnk in whitelist_table_3:
            python_code = "%s(*seq_list)" % whitelist_table_3[fnk]
        elif len(data) == 4:                                  # 4-parameter function:
          if fnk in whitelist_table_4:
            python_code = "%s(*seq_list)" % whitelist_table_4[fnk]
        if len(python_code) > 0:
          my_print("whitelist_table: python code", python_code)
          seq_list = [compile_compound_sequence(x) for x in data]
          str_seq_list = [str(x) for x in seq_list]
          my_print('str_seq_list', str_seq_list)
          seq = eval(python_code)
          python_code = ''
      elif op[0][0] in ['+', '-', '_', '.']:
        my_print('bracket ops')
        my_print('bracket ops seq', str(seq))
        version_1 = True
        if version_1:
          new_seq = sequence([])
          for bracket_op in op:
            my_print('bracket_op', bracket_op)
            symbol, bracket_ops = bracket_op
            my_print('symbol', symbol)
            my_print('bracket_ops', bracket_ops)
            the_seq = process_operators(bracket_ops, seq)

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
        else:                                                         # finish this branch!
          for sp in seq:                                              # haven't handled sequences yet. eg, (op3 _ op2) (|x> . |y> + |z>)
            r = sequence([])
            for x in sp:
              new_seq = sequence([])
              for bracket_op in op:
                my_print('bracket_op', bracket_op)
                symbol, bracket_ops = bracket_op
                my_print('symbol', symbol)
                my_print('bracket_ops', bracket_ops)
                the_seq = process_operators(bracket_ops, x)
         
                if symbol == '+':
                  new_seq.add_seq(the_seq)
                elif symbol == '-':
                  new_seq.sub_seq(the_seq)
                elif symbol == '_':
                  new_seq.merge_seq(the_seq)                           # do we need distributed_merge_seq here too? I suspect yes. 
                elif symbol == '__':
                  new_seq.merge_seq(the_seq, ' ')
                elif symbol == '.':
                  new_seq += the_seq
                my_print('new_seq', str(new_seq))
              r.add_seq(new_seq)
            seq = r
    elif type(op) is tuple:                                            # powered op found.
      tuple_op, power = op
      my_print('tuple_op', tuple_op)
      my_print('power', power)
      for _ in range(power):                                           # is there a better way to implement this?
        seq = process_operators([tuple_op], seq)
    else:
      python_code = process_single_op(op)
      if len(python_code) > 0:
        seq = eval('seq' + python_code)
  return seq


def compile_compound_sequence(compound_sequence):
  my_print('cs', compound_sequence)

  seq = sequence([])
  for seq2 in compound_sequence:
    symbol, (ops, object) = seq2
    my_print('symbol', symbol)
    my_print('ops', ops)
    my_print('object', object)

    distribute = True
    the_seq = sequence([])
    if type(object) is str:                                       # found a ket
      the_seq = sequence(superposition(object))

    if type(object) is list:
      my_print('fish')
      the_seq = compile_compound_sequence(object)
      distribute = True

    my_print('\n----------\nfinal')
    my_print('ops', ops)
    my_print('the_seq', str(the_seq))
    my_print('distribute', distribute)
    my_print('----------\n')
    the_seq = process_operators(ops, the_seq)
    #my_print('really final the_seq', str(the_seq))


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

def learn_stored_rule(context, op, one, rule, s):
  my_print('op', op)
  my_print('one', one)
  my_print('rule', rule)
  my_print('s', s)
  if rule == '#=>':
    context.learn(op, one, stored_rule(s))
  elif rule == '!=>':
    context.learn(op, one, memoizing_rule(s))
#  context.print_universe()

def learn_standard_rule(context, op, one, rule, seq):
  my_print('op', op)
  my_print('one', one)
  my_print('rule', rule)
  my_print('seq', str(seq))
  if rule == '=>':
    context.learn(op, one, seq)
  elif rule == '+=>':
    context.add_learn(op, one, seq)
#  context.print_universe()

def recall_rule(context, op, one):
  return context.recall(op, one)
#  return ket(one).apply_op(context, op)


def is_not_newline(c):
  return c not in ['\r', '\n']

bindings_dictionary = {
  'ket_calculate'                  : ket_calculate,
  'compile_compound_sequence'      : compile_compound_sequence,
  'float_int'                      : float_int,
  'learn_stored_rule'              : learn_stored_rule,
#  'learn_memoizing_rule'           : learn_memoizing_rule,
  'learn_standard_rule'            : learn_standard_rule,
  'recall_rule'                    : recall_rule,
  'context'                        : context,
  'is_not_newline'                 : is_not_newline,
}

op_grammar = makeGrammar(our_working_grammar, bindings_dictionary)




# now test our parser:

def test_seq_add_multi():
  x = op_grammar(' |a> - 2.1|b> + 3|c> _ 7.9|d> . 29.9|e> + |f> . |fish> __ |soup> + 13.2|pasta> ').literal_sequence()
  assert str(x) == '|a> + -2.1|b> + 23.7|cd> . 29.9|e> + |f> . |fish soup> + 13.2|pasta>'

def test_function_op_1():
  x = op_grammar('such-that( |a>, |b> + 2|c>, 3|d> . 1.7|e>)').function_op()
#  assert [str(y) for y in x] == ['such-that', '|a>', '|b> + 2|c>', '3|d> . 1.7|e>']
  #assert x == ['such-that', [('+', [[], 'a'])], [('+', [[], 'b']), ('+', [[2], 'c'])], [('+', [[3], 'd']), ('.', [[1.7], 'e'])]]
  assert x == ['f_op', 'such-that', [('+', [[], 'a'])], [('+', [[], 'b']), ('+', [[2], 'c'])], [('+', [[3], 'd']), ('.', [[1.7], 'e'])]]

def test_general_op_1():
  x = op_grammar('such-that( |a>, |b> + 2|c>, 3|d> . 1.7|e>)').general_op()
#  assert [str(y) for y in x] == ['such-that', '|a>', '|b> + 2|c>', '3|d> . 1.7|e>']
  #assert x == ['such-that', [('+', [[], 'a'])], [('+', [[], 'b']), ('+', [[2], 'c'])], [('+', [[3], 'd']), ('.', [[1.7], 'e'])]]
  assert x == ['f_op', 'such-that', [('+', [[], 'a'])], [('+', [[], 'b']), ('+', [[2], 'c'])], [('+', [[3], 'd']), ('.', [[1.7], 'e'])]]

def test_general_op_2():
  x = op_grammar('select[1,3]').general_op()
  #assert x == ['select', '1', '3']
  assert x == ['c_op', 'select', '1', '3']

def test_op_sequence_1():
  x = op_grammar('op4 select[1,3]^2 such-that(|a>, |b>) op1').op_sequence()
  print(x)
  assert True

def test_bracket_ops_1():
  x = op_grammar('(op3 op2 + op1 _ op)').bracket_ops()
  #assert x == [[('+', ['op3', 'op2']), ('+', ['op1']), ('_', ['op'])]]
  assert x == [('+', ['op3', 'op2']), ('+', ['op1']), ('_', ['op'])]

def test_op_sequence_2():
  x = op_grammar(' (op3 op2 + op1 _ op) ').op_sequence()
  #assert x == [[[('+', ['op3', 'op2']), ('+', ['op1']), ('_', ['op'])]]]
  assert x == [[('+', ['op3', 'op2']), ('+', ['op1']), ('_', ['op'])]]

def test_op_sequence_3():
  x = op_grammar(' op8 op7^3 (op6 . op5)^2 op4 (op3 + op2 _ op1) ').op_sequence()
  print(x)
  #assert x == ['op8', ('op7', 3), ([[('+', ['op6']), ('.', ['op5'])]], 2), 'op4', [[('+', ['op3']), ('+', ['op2']), ('_', ['op1'])]]]
  assert x == ['op8', ('op7', 3), ([('+', ['op6']), ('.', ['op5'])], 2), 'op4', [('+', ['op3']), ('+', ['op2']), ('_', ['op1'])]]

def test_op_sequence_4():
  x = op_grammar('(op3 + op2 _ op1) select[1,3] ').op_sequence()
  print(x)
  #assert x == [[[('+', ['op3']), ('+', ['op2']), ('_', ['op1'])]], ['select', '1', '3']]
  #assert x == [[[('+', ['op3']), ('+', ['op2']), ('_', ['op1'])]], ['c_op', 'select', '1', '3']]
  assert x == [[('+', ['op3']), ('+', ['op2']), ('_', ['op1'])], ['c_op', 'select', '1', '3']]

def test_op_sequence_5():
  x = op_grammar(' op8 op7^3 (op6 . op5)^2 op4 (op3 + op2 _ op1) select[1,3] such-that(|_seq>) ').op_sequence()
  print(x)
  assert True


def test_single_compound_sequence_1():
  x = op_grammar(' op3  op2 op1 |x>').single_compound_sequence()
  assert x == [['op3', 'op2', 'op1'], 'x']

def test_single_compound_sequence_2():
  x = op_grammar(' 3|x>').single_compound_sequence()
  assert x == [[3], 'x']

def test_single_compound_sequence_3():
  x = op_grammar(' select[1,2]^3  op2 op1 3.14|pi>').single_compound_sequence()
  #assert x == [[(['select', '1', '2'], 3), 'op2', 'op1', 3.14], 'pi']
  assert x == [[(['c_op', 'select', '1', '2'], 3), 'op2', 'op1', 3.14], 'pi']

def test_full_compound_sequence_1():
  x = op_grammar(' select[1,2]^3  op2 op1 3.14|pi>').full_compound_sequence()
  #assert x == [('+', [[(['select', '1', '2'], 3), 'op2', 'op1', 3.14], 'pi'])]
  assert x == [('+', [[(['c_op', 'select', '1', '2'], 3), 'op2', 'op1', 3.14], 'pi'])]

def test_full_compound_sequence_2():
  x = op_grammar(' |a> - 2.1|b> + 3|c> _ 7.9|d> . 29.9|e> + |f> . |fish> __ |soup> + 13.2|pasta> ').full_compound_sequence()
  print(x)
  assert x == [('+', [[], 'a']), ('-', [[2.1], 'b']), ('+', [[3], 'c']), ('_', [[7.9], 'd']), ('.', [[29.9], 'e']), ('+', [[], 'f']), ('.', [[], 'fish']), ('__', [[], 'soup']), ('+', [[13.2], 'pasta'])]



# do we want this to parse??
def test_full_compound_sequence_naked_union_1():
  x = op_grammar(' union(|a>, |b>)').full_compound_sequence()
  print(x)
  #assert x == [('+', [[['union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], ''])]
  assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], ''])]

def test_full_compound_sequence_union_2():
  x = op_grammar(' union(|a>, |b>) |>  ').full_compound_sequence()
  print(x)
  #assert x == [('+', [[['union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], ''])]
  assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], ''])]

def test_full_comound_sequence_union_union():
  x = op_grammar(' union(|a>, |b>) + union(|c>,|d>) ').full_compound_sequence()
  print(x)
  #assert x == [('+', [[['union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], '']), ('+', [[['union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], ''])]
  assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], '']), ('+', [[['f_op', 'union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], ''])]

def test_full_comound_sequence_union_ket_union_ket():
  x = op_grammar(' union(|a>, |b>)|fish> + union(|c>,|d>) |soup>').full_compound_sequence()
  print(x)
  #assert x == [('+', [[['union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], 'fish']), ('+', [[['union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], 'soup'])]
  assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], 'fish']), ('+', [[['f_op', 'union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], 'soup'])]

def test_full_comound_sequence_union_union_ket():
  x = op_grammar(' union(|a>, |b>) + union(|c>,|d>) |soup>').full_compound_sequence()
  print(x)
  #assert x == [('+', [[['union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], '']), ('+', [[['union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], 'soup'])]
  assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], '']), ('+', [[['f_op', 'union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], 'soup'])]

def test_full_comound_sequence_union_ket_union():
  x = op_grammar(' union(|a>, |b>)|fish> + union(|c>,|d>) ').full_compound_sequence()
  print(x)
  #assert x == [('+', [[['union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], 'fish']), ('+', [[['union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], ''])]
  assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], 'fish']), ('+', [[['f_op', 'union', [('+', [[], 'c'])], [('+', [[], 'd'])]]], ''])]

def test_full_compound_sequence_bracket_union_union():
  x = op_grammar(' ( union(|a>, |b>) + union(|c>,|d>)) |soup>').full_compound_sequence()
  print(x)
  #assert x == [('+', [[[[('+', [['union', [('+', [[], 'a'])], [('+', [[], 'b'])]]]), ('+', [['union', [('+', [[], 'c'])], [('+', [[], 'd'])]]])]]], 'soup'])]
  #assert x == [('+', [[[[('+', [['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]]), ('+', [['f_op', 'union', [('+', [[], 'c'])], [('+', [[], 'd'])]]])]]], 'soup'])]
  assert x == [('+', [[[('+', [['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]]), ('+', [['f_op', 'union', [('+', [[], 'c'])], [('+', [[], 'd'])]]])]], 'soup'])]

def test_full_compound_sequence_brackets():
  x = op_grammar(' op8 op7^3 op4 (((op3 + op2 . op1))) op |fish> ').full_compound_sequence()
  print(x)
  #assert x == [('+', [['op8', ('op7', 3), 'op4', [[('+', [[[('+', [[[('+', ['op3']), ('+', ['op2']), ('.', ['op1'])]]])]]])]], 'op'], 'fish'])]
  assert x == [('+', [['op8', ('op7', 3), 'op4', [('+', [[('+', [[('+', ['op3']), ('+', ['op2']), ('.', ['op1'])]])]])], 'op'], 'fish'])]



# now test our compiler:
def test_compiler_naked_ket():
  x = op_grammar(' |fish> ').compiled_compound_sequence()
  assert str(x) == '|fish>'

def test_compiler_coeff_ket():
  x = op_grammar(' 3.14|fish> ').compiled_compound_sequence()
  assert str(x) == '3.14|fish>'

def test_compiler_op_ket():
  x = op_grammar(' op1 |fish> ').compiled_compound_sequence()
  assert str(x) == '|op1: fish>'

def test_compiler_op_power():
  x = op_grammar(' op1^3 |fish> ').compiled_compound_sequence()
  assert str(x) == '|op1: op1: op1: fish>'

def test_compiler_literal_sequence():
  x = op_grammar(' |a> - 2.1|b> + 3|c> _ 7.9|d> . 29.9|e> + |f> . |fish> __ |soup> + 13.2|pasta>  ').compiled_compound_sequence()
  assert str(x) == '|a> + -2.1|b> + 23.7|cd> . 29.9|e> + |f> . |fish soup> + 13.2|pasta>'

def test_compiler_union_1():
  x = op_grammar(' union(|a>, 2|b> . 3|c>) |null> ').compiled_compound_sequence()
  assert str(x) == '|a> + 2|b> . 3|c>'

def test_compiler_select_1():
  x = op_grammar(' select[1,3] |null> ').compiled_compound_sequence()
  assert str(x) == '|null>'

def test_compiler_select_friends():
  x = op_grammar(' select[1,3] friends |Fred> ').compiled_compound_sequence()
  assert str(x) == '|Jack> + |Harry> + |Ed>'

def test_compiler_op_union_1():
  x = op_grammar(' op1 union(|a>, 2|b> . 3|c>) |null> ').compiled_compound_sequence()
  assert str(x) == '|op1: a> + 2|op1: b> . 3|op1: c>'

def test_compiler_simple_op_bracket_1():
  x = op_grammar(' op1(|x> + |y>) ').compiled_compound_sequence()
  assert str(x) == '|op1: x> + |op1: y>'

def test_compiler_simple_op_bracket_2():
  x = op_grammar(' op1 (|x> + |y>) ').compiled_compound_sequence()
  assert str(x) == '|op1: x> + |op1: y>'


def test_compiler_bracket_ops_1():
  x = op_grammar(' (op3 op2 + op1 __ op) |x> ').compiled_compound_sequence()
  assert str(x) == '|op3: op2: x> + |op1: x op: x>'

def test_compiler_bracket_ops_2():
  x = op_grammar(' (((op3 op2 + op1 __ op))) |x> ').compiled_compound_sequence()
  assert str(x) == '|op3: op2: x> + |op1: x op: x>'

def test_compiler_long_op_sequence_1():
  x = op_grammar(' op8 op7^3 op4 (op3 + op2 . op1) op |fish> ').compiled_compound_sequence()
  assert str(x) == '|op8: op7: op7: op7: op4: op3: op: fish> + |op8: op7: op7: op7: op4: op2: op: fish> . |op8: op7: op7: op7: op4: op1: op: fish>'

def test_compiler_short_op_sequence_1():
  x = op_grammar('  (op3 + op2 . op1) op |fish> ').compiled_compound_sequence()
  assert str(x) == '|op3: op: fish> + |op2: op: fish> . |op1: op: fish>'

def test_compiler_long_op_sequence_1():
  x = op_grammar(' op8 op7^3 op4 ((((op3 + op2 . op1)))) op |fish> ').compiled_compound_sequence()
  assert str(x) == '|op8: op7: op7: op7: op4: op3: op: fish> + |op8: op7: op7: op7: op4: op2: op: fish> . |op8: op7: op7: op7: op4: op1: op: fish>'


def test_common_friends():
  x = op_grammar(' common[friends] (|Fred> + |Sam>) ').compiled_compound_sequence()
  assert str(x) == '|Jack> + |Emma> + |Charlie>'

def test_single_sequence():
  x = op_grammar(' (|Fred> + |Sam>) ').compiled_compound_sequence()
  assert str(x) == '|Fred> + |Sam>'  

def test_single_ket():
  x = op_grammar(' |Fred> + |Sam> ').compiled_compound_sequence()
  assert str(x) == '|Fred> + |Sam>'



def test_temperature_conversion_1():
  x = op_grammar(' |F:> __ round[2] plus[32] times-by[9/5] extract-value |C: 37> ').compiled_compound_sequence()
  assert str(x) == '|F: 98.6>'

def test_temperature_conversion_2():
  x = op_grammar(' |F:> __ round[2] minus[459.67] times-by[9/5] extract-value |K: 200> ').compiled_compound_sequence()
  assert str(x) == '|F: -99.67>'

def test_ket_bracket_merge_union_bracket():
  x = op_grammar(' |fish> __ union(|cats>, |dogs>) ').compiled_compound_sequence()
  assert str(x) == '|fish cats> + |fish dogs>'

def test_bracket_sp_big_brackets_subtract():
  x = op_grammar(' ( |x> + 0.5|y> + 2.7|z> ) + ((|fish> - (|cats> + |dogs>)) + |mice>) + |rats> ').compiled_compound_sequence()
  assert str(x) == '|x> + 0.5|y> + 2.7|z> + |fish> + -1|cats> + -1|dogs> + |mice> + |rats>'

#def test_superposition_naked_fn2_bracket_multi():
#  x = op_grammar(' (((( |x>,|y> ) )))').compiled_compound_sequence()
  #assert str(x) == ''
  # parse error. I guess that is fine. Maybe tweak later.

def test_op_sentence_sum():
  x = op_grammar(' 3^2 common[friends] split |Fred Sam> + |mice> + (|cats> + |dogs>) + split |horse pony mare> ').compiled_compound_sequence()
  print(x)
  assert str(x) == '9|Jack> + 9|Emma> + 9|Charlie> + |mice> + |cats> + |dogs> + |horse> + |pony> + |mare>'

def test_op_sentence_sum_v2():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> _ |mice> - (|cats> + |dogs>) . split |horse pony mare> ").compiled_compound_sequence()
  print(x)
  assert str(x) == '9|Jack> + 9|Emma> + 9|Charliemice> + -1|cats> + -1|dogs> . |horse> + |pony> + |mare>'

def test_tuple_op_4_bracket_op():
  x = op_grammar(' op5((- op4 + op3 __ op2 . op1)) |x>   ' ).compiled_compound_sequence()
  assert str(x) == ''

def test_tuple_op_4_bracket_op_2():
  x = op_grammar(' op5 ((- op4 + op3 __ op2 . op1)) |x>   ' ).compiled_compound_sequence()
  assert str(x) == '-1|op5: op4: x> + |op5: op3: x op2: x> . |op5: op1: x>'

def test_distributed_merge_1():
  x = op_grammar(' |fish> __ (|cats> + |dogs>) ').compiled_compound_sequence()
  assert str(x) == '|fish cats> + |fish dogs>'

def test_distributed_merge_2():
  x = op_grammar(' |fish> __ (((|cats> + |dogs>))) ').compiled_compound_sequence()
  assert str(x) == '|fish cats> + |fish dogs>'

def test_distributed_merge_3():
  x = op_grammar(' |fish> __ split |cats dogs> ').compiled_compound_sequence()
  assert str(x) == '|fish cats> + |fish dogs>'

def test_distributed_merge_4():
  x = op_grammar(' |fish> __ union( |cats> ,  |dogs> ) ').compiled_compound_sequence()
  assert str(x) == '|fish cats> + |fish dogs>'

def test_distributed_merge_5():
  x = op_grammar(' |fish> __ |cats> + |dogs> ').compiled_compound_sequence()
  assert str(x) == '|fish cats> + |dogs>'



def test_distributed_minus_1():
  x = op_grammar(' |fish> - (|cats> + |dogs>) ').compiled_compound_sequence()
  assert str(x) == '|fish> + -1|cats> + -1|dogs>'

def test_distributed_minus_2():
  x = op_grammar(' |fish> - (((|cats> + |dogs>))) ').compiled_compound_sequence()
  assert str(x) == '|fish> + -1|cats> + -1|dogs>'

def test_distributed_minus_3():
  x = op_grammar(' |fish> - split |cats dogs> ').compiled_compound_sequence()
  assert str(x) == '|fish> + -1|cats> + -1|dogs>'

def test_distributed_minus_4():
  x = op_grammar(' |fish> - union( |cats> ,  |dogs> ) ').compiled_compound_sequence()
  assert str(x) == '|fish> + -1|cats> + -1|dogs>'

def test_distributed_minus_5():
  x = op_grammar(' |fish> - |cats> + |dogs> ').compiled_compound_sequence()
  assert str(x) == '|fish> + -1|cats> + |dogs>'


def test_bracket_ops_merge_1():
  x = op_grammar(' (op3 __ op2) op1 |x> ').compiled_compound_sequence()
  assert str(x) == '|op3: op1: x op2: op1: x>'

def test_bracket_ops_merge_2():
  x = op_grammar(' (op3 __ op2) op1 (|x> + |y>) ').compiled_compound_sequence()
  assert str(x) == ''

def test_bracket_ops_merge_3():
  x = op_grammar(' (op3 __ op2) (|x> + |y>) ').compiled_compound_sequence()
  assert str(x) == ''

def test_bracket_ops_merge_4():
  x = op_grammar(' (op3 __ op2) split |x y> ').compiled_compound_sequence()
  assert str(x) == ''


def test_bracket_ops_minus_1():
  x = op_grammar(' (op3 - op2) |x> ').compiled_compound_sequence()
  assert str(x) == ''

def test_bracket_ops_minus_2():
  x = op_grammar(' (op3 - op2) (|x> + |y>) ').compiled_compound_sequence()
  assert str(x) == ''

def test_bracket_ops_dot_1():
  x = op_grammar(' (op3 . op2) |x> ').compiled_compound_sequence()
  assert str(x) == ''

def test_bracket_ops_dot_2():
  x = op_grammar(' (op3 . op2) (|x> + |y>) ').compiled_compound_sequence()
  assert str(x) == ''

def test_bracket_ops_dot_3():
  x = op_grammar(' (op3 . op2) split |x y> ').compiled_compound_sequence()
  assert str(x) == ''


def test_tuple_op_1():
  x = op_grammar(' op1^3 |x> ').compiled_compound_sequence()
  assert str(x) == ''

def test_tuple_op_2():
  x = op_grammar('  (  ( op1 ))^3 |x> ').compiled_compound_sequence()
  assert str(x) == ''


# test learn rules:
def test_learn_stored_rule_1():
  x = op_grammar('op |ket> #=> |bah> ').stored_rule()
  assert False

def test_learn_stored_rule_2():
  x = op_grammar(' |ket> #=> |foo> ').stored_rule()
  assert False

def test_learn_memoizing_rule_1():
  x = op_grammar(' measure |system> !=> some |state> ').stored_rule()            #memoizing_rule()
  assert False

def test_learn_standard_rule_1():
  x = op_grammar(' age |Fred> => |37> ').learn_rule()
  assert False

def test_learn_standard_rule_2():
  x = op_grammar(' spell |Fred> => |F> . |r> . |e> . |d> ').learn_rule()
  assert False


def test_string_parse_1():
  x = op_grammar(' some random string ').string()
  assert x == ' some random string '

# this is meant to fail:
#def test_string_parse_2():
#  x = op_grammar(' some random string \n ').string()
#  assert x == ''

def test_object_1():
  x = op_grammar('|Fred>').object()
  assert x == 'Fred'

def test_object_2():
  x = op_grammar('|*>').object()
  assert x == '*'

def test_object_3():
  x = op_grammar('(*,*)').object()
  assert x == '(*,*)'

def test_sw_file_1():
  x = op_grammar('age |Julie> => |32> \n spell-out |Julie> => |J> . |u> . |l> . |i> . |e> \n\n\n\n friends |Julie> #=> |Fred> + |Sam> + |Robert> ').sw_file()
  context.print_universe()
  assert False

def test_recall_rule_1():
  x = op_grammar('spell-out|Julie>').recall_rule()
  assert str(x) == ''

def test_recall_compiled_sequence_1():
  x = op_grammar('spell-out|Julie>').compiled_compound_sequence()
  assert str(x) == ''

def test_recall_compiled_sequnece_2():
  x = op_grammar('friends|Fred>').compiled_compound_sequence()
  assert str(x) == ''

