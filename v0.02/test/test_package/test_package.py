#!/usr/bin/env python3

#######################################################################
# let's test v0.02
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-2-9
# Update: 2018-2-26
# Copyright: GPLv3
#
# Usage: py.test -v test_package.py
#
#######################################################################


import sys
from pprint import pprint
from semantic_db import *

#context = ContextList('in test the processor')
#context.print_universe()
logger.setLevel(logging.DEBUG)

#sys.exit(0)



def test_process_single_op_literal_1():
  r = process_single_op('friends')
  assert r == '.apply_op(context,"friends")'

def test_process_single_op_compound_1():
  r = process_single_op(['common', 'friends'])
  assert r == '.apply_sp_fn(common,context,"friends")'


def test_sw_file_1():
#  x = op_grammar('age |Julie> => |32> \n spelling |Julie> => |J> . |u> . |l> . |i> . |e> \n\n\n\n friends |Julie> #=> |Fred> + |Sam> + |Robert> ').sw_file()
  s = 'age |Julie> => |32> \n spelling |Julie> => |J> . |u> . |l> . |i> . |e> \n\n\n\n friends |Julie> #=> |Fred> + |Sam> + |Robert> '
  process_sw_file(context, s)
  context.print_multiverse()
  assert False

def test_recall_1():
  s = 'spelling |Julie>'
  r = extract_compound_sequence(context, s)
  assert str(r) == '|J> . |u> . |l> . |i> . |e>'

def test_context_load_1():
  context.load('sw-examples/fred-sam-friends.sw')
  context.print_universe()
  assert False

def test_process_sw_file_1():
  s = 'age |Emma> => |42>'
  process_sw_file(context, s)
  context.print_universe()
  assert False

def test_common_friends_1():
  s = 'common[friends] split |Fred Sam> '
  r = extract_compound_sequence(context, s)
  assert str(r) == '|Jack> + |Emma> + |Charlie>'

def test_self_learn_1():
  s = 'age |Bob> => 37 |_self>'
  process_sw_file(context, s)
  context.print_multiverse()
  assert False

def test_self_learn_2():
  s = 'age |Bob> => 32 |_self1>'
  process_sw_file(context, s)
  context.print_multiverse()
  assert False

def test_star_learn_1():
  s = 'foo (*) => |bah>'
  process_sw_file(context, s)
  context.print_multiverse()
  assert False

def test_star_learn_2():
  s = 'foo-2 (*,*) => |bah 2>'
  process_sw_file(context, s)
  context.print_multiverse(True)
  assert False


def test_context_sp_learn_1():
  context.sp_learn('op-a', '*', 'value a')
  context.print_universe()
  assert False

def test_context_sp_learn_2():
  context.sp_learn('op-b', '*,*', 'value b')
  context.print_universe(True)
  assert False

def test_context_sp_learn_3():
  context.sp_learn('op-c', '*,*', ket('_self1'))
  context.print_universe(True)
  assert False

def test_context_sp_learn_4():
  context.sp_learn('op-c', '*,*', ket('_self'))
  context.print_universe(True)
  assert False

def test_context_sp_learn_5():
  context.sp_learn('op-c', '*', ket('_self'))
  context.print_universe(True)
  assert False


def test_context_sp_recall_1():
  r = context.sp_recall('op-a', ['fish'])
  assert str(r) == '|value a>'

def test_context_sp_recall_2():
  r = context.sp_recall('op-b', ['fish', 'soup'])
  assert str(r) == '|value b>'


def test_star_learn_3():
  s = 'foo-star (*) => |_self>'
  process_sw_file(context, s)
  context.print_multiverse()
  assert False

def test_star_learn_4():
  s = 'foo-2-star (*,*) => |_self>'
  process_sw_file(context, s)
  context.print_multiverse(True)
  assert False

def test_apply_sp_1():
  s = 'apply(|op: friends>, |Fred>)'
  r = extract_compound_sequence(context, s)
  assert str(r) == '|Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>'  

def test_apply_sp_2():
  r = apply_sp(context, ket('op: friends'), ket('Fred'))
  assert str(r) == '|Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>'

def test_union_1():
  s = 'union(|a>, |b>)'
  r = extract_compound_sequence(context, s)
  assert str(r) == '|a> + |b>'


def test_fast_simm_1():
  x = ket('a') + ket('b') + ket('c')
  y = ket('b')
  r = fast_simm(x,y)
  assert r == 0.3333333333333333

def test_fast_simm_2():
  x = ket('a') + ket('b') + ket('c')
  y = ket('b') + ket('a')
  r = fast_simm(x,y)
  assert r == 0.6666666666666666

def test_print_table_1():
  context.load('sw-examples/fred-sam-friends.sw')
  x = ket('Fred') + ket('Sam')
  x.apply_sp_fn(old_pretty_print_table,context,"person,friends")
  assert False

def test_print_table_2():
  context.load('sw-examples/fred-sam-friends.sw')
  x = ket('Fred') + ket('Sam')
  x.apply_sp_fn(pretty_print_table,context,"person,friends")
  assert False


def test_extract_compound_sequence_1():
  rule = 'list-to-words |_self>'
  seq = ket('a') + ket('b')
  r = extract_compound_sequence(context, rule, [seq])
  assert str(r) == '|a and b>'

def test_extract_compound_sequence_2():
  rule = stored_rule('list-to-words |_self>')
  seq = ket('a') + ket('b')
  r = extract_compound_sequence(context, rule.rule, [seq])
  assert str(r) == '|a and b>'


def test_op_loading_1():
  context.load('sw-examples/test-operators.sw')
  context.print_universe()
  assert True

def test_op_sequence_1():
  context.load('sw-examples/test-operators.sw')
  s = '(op7) op6 |fish>'
  r = extract_compound_sequence(context, s)
  assert str(r) == '|op7: op6: fish>'

def test_op_sequence_2():
  context.load('sw-examples/test-operators.sw')
  s = 'op8 (op7) op6 |fish>'
  r = extract_compound_sequence(context, s)
  assert str(r) == ''

def test_op_sequence_3():
  context.load('sw-examples/test-operators.sw')
  s = 'op8 (op7)'
  r = extract_compound_sequence(context, s)
  assert str(r) == ''


def test_normalize_seq_len_1():
  x = ket('a',2) + ket('b',3.3)
  y = sequence('x') + ket('y') + ket('z')
  print(str(x))
  print(str(y))
  r1, r2 = normalize_seq_len(x, y)
  print(str(r1))
  print(str(r2))
  assert False


def test_predict_next_1():
  s = 'seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7>\n'
  s += 'seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>\n'
  s += 'seq |fact> => |1> . |2> . |6> . |24> . |120>'
  process_sw_file(context, s)
#  context.print_universe()
#  r = predict_next(context, sequence('2') + ket('3'), 'seq,3')
  r = predict_next(sequence('2') + ket('3'), context, 'seq,3')
  assert str(r) == ''

def test_predict_next_2():
  s = 'seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7>\n'
  s += 'seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>\n'
  s += 'seq |fact> => |1> . |2> . |6> . |24> . |120>'
  process_sw_file(context, s)
#  r = predict_next(context, sequence('6') + ket('2'), 'seq,3')
  r = predict_next(sequence('6') + ket('2'), context, 'seq,3')
  assert str(r) == ''

def test_predict_next_3():
  s = 'seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7>\n'
  s += 'seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>\n'
  s += 'seq |fact> => |1> . |2> . |6> . |24> . |120>'
  process_sw_file(context, s)
#  r = predict_next(context, sequence('2') + ket('5'), 'seq,3')
  r = predict_next(sequence('2') + ket('5'), context, 'seq,3')
  assert str(r) == ''


def test_multi_line_stored_rule_1():
  s = "tally-stored-food |*> #=> merge-value stored-food |_self>"
  r = op_grammar(s).stored_rule()
  context.print_universe()
  assert False

def test_multi_line_stored_rule_2():
  s = """tally-stored-food-2 |*> #=>
    merge-value stored-food |_self>

bah |x> => |fish>
"""
  r = op_grammar(s).multi_stored_rule()
  context.print_universe()
  assert False

def test_multi_line_stored_rule_3():
  s = """tally-stored-food-3 |*> #=>
    merge-value stored-food |_self>

bah |x> => |fish>
"""
  r = op_grammar(s).sw_file()
  context.print_universe()
  assert False


def test_multi_line_stored_rule_4():
  s = """process-if |reached home> #=>
    drop-the |food>
    lay |scent> => |no>
    type |walk> => |op: random>
    path |home> => |home>

"""
  r = op_grammar(s).sw_file()
  context.print_universe()
  assert False

def test_single_stored_rule_1():
  s = "foo |*> #=> |bah>"
  r = op_grammar(s).sw_file()
  context.print_universe()
  assert False

# yup, works!
#def test_multi_line_stored_rule_recall_1():
#  r = context.recall('process-if', 'reached home')
#  assert str(r) == ''


def test_multi_line_stored_rule_5():
  s = """

bah-a |*> #=>
    |fishy>
    |soupy>

"""
  r = op_grammar(s).sw_file()
  context.print_universe()
  assert False


def test_sw_file_load_1():
  context.load('sw-examples/test-multi-line.sw')
  context.print_universe()
  assert False

def test_process_sw_file_1():
  with open('sw-examples/test-multi-line.sw', 'r') as f:
    text = f.read()
    print('text: %s' % text)
    process_sw_file(context, text)
  assert True

def test_process_empty_string_1():
  s = ''
  process_sw_file(context, s)

def test_process_rule_line_multi_line_1():
  context.load('sw-examples/test-multi-line.sw')
  context.print_universe()
  s = 'foo |x>'
  r = process_input_line(context, s, ket())
  assert str(r) == '|bah>'

def test_process_stored_rule_1():
  context.load('sw-examples/test-multi-line.sw')
  context.print_universe()
  s = 'foo |x>'
  r = process_stored_rule(context, s, None)
  assert str(r) == '|bah>'


def test_stored_rule_line_1():
  s = 'type |walk> => |op: random>'
  r = op_grammar(s).stored_rule_line()
  assert str(r) == '|op: random>'

def test_stored_rule_line_2():
  s = 'age |Fred>'
  r = op_grammar(s).stored_rule_line()
  assert r == [('+', [['age'], 'Fred'])]

def test_stored_rule_line_3():
  s = """

-- a random comment

type |walk> => |op: return-home>
heading |ops> => |op: S>

type |walk>
"""
  r = process_stored_rule(context, s)
  context.print_universe()
  assert str(r) == 'fish'

def test_multi_value_stored_rules_1():
  s = """

foo (*,*) #=>
    the |result> => 3|__self1> + 5|__self2>

"""
  r = process_sw_file(context, s)
  context.print_universe()
  s = 'foo(|a>, |b>)'
  r = process_input_line(context, s, ket())
  assert str(r) == 'fish'  


def test_active_recall_1():
  context.learn('age', 'sam', '2')
  r = context.recall('age', ket('sam',3), True)
  assert str(r) == '3|2>'
