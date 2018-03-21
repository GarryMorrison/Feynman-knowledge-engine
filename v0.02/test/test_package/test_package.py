#!/usr/bin/env python3

#######################################################################
# let's test v0.02
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 9/2/2018
# Update: 21/3/2018
# Copyright: GPLv3
#
# Usage: py.test -v test_package.py
#
#######################################################################


import sys
from pprint import pprint
from semantic_db import *

# context = ContextList('in test the processor')
# context.print_universe()
logger.setLevel(logging.DEBUG)


# sys.exit(0)


# deprecated:
# def test_process_single_op_literal_1():
#  r = deprecated_process_single_op('friends')
#  assert r == '.apply_op(context,"friends")'

# deprecated:
# def test_process_single_op_compound_1():
#  r = deprecated_process_single_op(['common', 'friends'])
#  assert r == 'fish'


def test_sw_file_1():
    #  x = op_grammar('age |Julie> => |32> \n spelling |Julie> => |J> . |u> . |l> . |i> . |e> \n\n\n\n friends |Julie> #=> |Fred> + |Sam> + |Robert> ').sw_file()
    s = 'age |Julie> => |32> \n spelling |Julie> => |J> . |u> . |l> . |i> . |e> \n\n\n\n friends |Julie> #=> |Fred> + |Sam> + |Robert> '
    process_sw_file(context, s)
    context.print_multiverse()
    assert True


def test_recall_1():
    s = 'spelling |Julie>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|J> . |u> . |l> . |i> . |e>'


def test_context_load_1():
    context.load('sw-examples/fred-sam-friends.sw')
    context.print_universe()
    assert True


def test_process_sw_file_1():
    s = 'age |Emma> => |42>'
    process_sw_file(context, s)
    context.print_universe()
    s = 'age |Emma>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|42>'


def test_common_friends_1():
    s = 'common[friends] split |Fred Sam> '
    r = extract_compound_sequence(context, s)
    assert str(r) == '|Jack> + |Emma> + |Charlie>'


def test_self_learn_1():
    s = 'age |Bob> => 37 |_self>'
    process_sw_file(context, s)
    context.print_multiverse()
    s = 'age |Bob>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '37|Bob>'


def test_self_learn_2():
    s = 'age |Bob> => 32 |_self1>'
    process_sw_file(context, s)
    context.print_multiverse()
    s = 'age |Bob>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '32|Bob>'


def test_star_learn_1():
    s = 'foo (*) => |bah>'
    process_sw_file(context, s)
    context.print_multiverse()
    s = 'foo (|a> + 2|b> . |c>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|bah>'  # weird! Currently returns |bah> . |bah>. Fix!


def test_star_learn_2():
    s = 'foo-2 (*,*) => |bah 2>'
    process_sw_file(context, s)
    context.print_multiverse(True)
    s = 'foo-2(|a> + 2|b> . |c>, |x> . 3|y> )'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|bah 2>'


def test_context_seq_fn_learn_1():
    context.seq_fn_learn('op-a', '*', 'value a')
    context.print_universe()
    r = context.seq_fn_recall('op-a', ['fish'])
    assert str(r) == '|value a>'


def test_context_seq_fn_learn_2():
    context.seq_fn_learn('op-b', '*,*', 'value b')
    context.print_universe(True)
    r = context.seq_fn_recall('op-b', ['fish', 'soup'])
    assert str(r) == '|value b>'


def test_context_seq_fn_learn_3():
    # context.seq_fn_learn('op-c', '*,*', ket('_self1'))
    context.seq_fn_learn('op-c', '*,*', stored_rule('|_self1>'))
    context.print_universe(True)
    r = context.seq_fn_recall('op-c', ['fish', 'soup'], active=True)
    assert str(r) == '|fish>'


def test_context_seq_fn_learn_4():
    # context.seq_fn_learn('op-c', '*,*', ket('_self'))
    context.seq_fn_learn('op-c', '*,*', stored_rule('|_self>'))
    context.print_universe(True)
    r = context.seq_fn_recall('op-c', ['more', 'soup'], active=True)
    assert str(r) == '|more>'


def test_context_seq_fn_learn_5():
    # context.seq_fn_learn('op-c', '*', ket('_self'))
    context.seq_fn_learn('op-c', '*', stored_rule('|_self>'))
    context.print_universe(True)
    r = context.seq_fn_recall('op-c', ['soup'], active=True)
    assert str(r) == '|soup>'


def test_context_seq_fn_recall_1():
    r = context.seq_fn_recall('op-a', ['fish'])
    assert str(r) == '|value a>'


def test_context_seq_fn_recall_2():
    r = context.seq_fn_recall('op-b', ['fish', 'soup'])
    assert str(r) == '|value b>'


# not sure these two add anything new. So, switched them off.
def test_star_learn_3():
    s = 'foo-star (*) => |_self>'
    process_sw_file(context, s)
    context.print_multiverse()
    assert True


def test_star_learn_4():
    s = 'foo-2-star (*,*) => |_self>'
    process_sw_file(context, s)
    context.print_multiverse(True)
    assert True


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


def test_superposition_simm_1():
    x = ket('a') + ket('b') + ket('c')
    y = ket('b')
    r = superposition_simm(x, y)
    assert r == 0.3333333333333333


def test_superposition_simm_2():
    x = ket('a') + ket('b') + ket('c')
    y = ket('b') + ket('a')
    r = superposition_simm(x, y)
    assert r == 0.6666666666666666


def test_print_table_1():
    context.load('sw-examples/fred-sam-friends.sw')
    x = ket('Fred') + ket('Sam')
    x.apply_sp_fn(old_pretty_print_table, context, "person,friends")
    assert True  # yup, works. And don't know a clean way to assert that.


def test_print_table_2():
    context.load('sw-examples/fred-sam-friends.sw')
    x = ket('Fred') + ket('Sam')
    # x.apply_sp_fn(pretty_print_table,context,"person,friends")            # old invoke method
    x.apply_sp_fn(pretty_print_table, context, "person", "friends")  # new invoke method
    assert True  # yup, works. And don't know a clean way to assert that.


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
    assert str(r) == '|op8: op7: op6: fish>'


def test_op_sequence_3():
    context.load('sw-examples/test-operators.sw')
    s = 'op8 (op7)'
    r = extract_compound_sequence(context, s)
    assert str(r) == ''  # Don't know what we want returned here.


def test_normalize_seq_len_1():
    x = ket('a', 2) + ket('b', 3.3)
    y = sequence('x') + ket('y') + ket('z')
    print(str(x))
    print(str(y))
    r1, r2 = normalize_seq_len(x, y)
    print(str(r1))
    print(str(r2))
    assert str(r1) == '2|a> + 3.3|b> . |> . |>'
    assert str(r2) == '|x> . |y> . |z>'


def test_predict_next_1():
    s = 'seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7>\n'
    s += 'seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>\n'
    s += 'seq |fact> => |1> . |2> . |6> . |24> . |120>'
    process_sw_file(context, s)
    #  context.print_universe()
    #  r = predict_next(context, sequence('2') + ket('3'), 'seq,3')
    # r = predict_next(sequence('2') + ket('3'), context, 'seq,3') # old invoke method
    r = predict_next(sequence('2') + ket('3'), context, 'seq', 3)  # new invoke method
    assert str(r) == '|count: 4 . 5 . 6> + |fib: 5 . 8 . 13> + 0.5|fact: 6 . 24 . 120>'


def test_predict_next_2():
    s = 'seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7>\n'
    s += 'seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>\n'
    s += 'seq |fact> => |1> . |2> . |6> . |24> . |120>'
    process_sw_file(context, s)
    #  r = predict_next(context, sequence('6') + ket('2'), 'seq,3')
    # r = predict_next(sequence('6') + ket('2'), context, 'seq,3')  # old invoke method
    r = predict_next(sequence('6') + ket('2'), context, 'seq', 3)  # new invoke method
    assert str(r) == '0.5|count: 7> + 0.5|fib: 3 . 5 . 8> + 0.5|fact: 24 . 120>'


def test_predict_next_3():
    s = 'seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7>\n'
    s += 'seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>\n'
    s += 'seq |fact> => |1> . |2> . |6> . |24> . |120>'
    process_sw_file(context, s)
    #  r = predict_next(context, sequence('2') + ket('5'), 'seq,3')
    # r = predict_next(sequence('2') + ket('5'), context, 'seq,3') # old invoke method
    r = predict_next(sequence('2') + ket('5'), context, 'seq', 3)  # new invoke method
    assert str(r) == '|count: 6 . 7> + |fib: 8 . 13> + 0.5|fact: 6 . 24 . 120>'


def test_multi_line_stored_rule_1():
    s = "tally-stored-food |*> #=> merge-value stored-food |_self>"
    r = op_grammar(s).stored_rule()
    context.print_universe()
    r = context.recall('tally-stored-food', '*')
    assert str(r) == 'merge-value stored-food |_self>'


def test_multi_line_stored_rule_2():
    s = """tally-stored-food-2 |*> #=>
    merge-value stored-food |_self>

bah |x> => |fish>
"""
    r = op_grammar(s).multi_stored_rule()  # I think we want this one to fail.
    context.print_universe()
    assert False


def test_multi_line_stored_rule_3():
    s = """
tally-stored-food-3 |*> #=>
    merge-value stored-food |_self>

bah |x> => |fish>
"""
    r = op_grammar(s).sw_file()
    context.print_universe()
    r1 = context.recall('tally-stored-food-3', '*')
    r2 = context.recall('bah', 'x')
    assert str(r1) == '\n    merge-value stored-food |_self>'
    assert str(r2) == '|fish>'


def test_multi_line_stored_rule_4():
    s = """
process-if |reached home> #=>
    drop-the |food>
    lay |scent> => |no>
    type |walk> => |op: random>
    path |home> => |home>

"""
    r = op_grammar(s).sw_file()
    context.print_universe()
    r = context.recall('process-if', 'reached home')
    assert str(
        r) == '\n    drop-the |food>\n    lay |scent> => |no>\n    type |walk> => |op: random>\n    path |home> => |home>'


def test_single_stored_rule_1():
    s = "foo |*> #=> |bah>"
    r = op_grammar(s).sw_file()
    context.print_universe()
    r = context.recall('foo', 'x')
    assert str(r) == '|bah>'


# yup, works!
# def test_multi_line_stored_rule_recall_1():
#  r = context.recall('process-if', 'reached home')
#  assert str(r) == ''


def test_multi_line_stored_rule_5():
    s = """

bah-a |*> #=>
    |fish>
    |soup>

"""
    r = op_grammar(s).sw_file()
    context.print_universe()
    r = context.recall('bah-a', 'x')
    assert str(r) == '\n    |fish>\n    |soup>'


def test_sw_file_load_1():
    context.load('sw-examples/test-multi-line.sw')
    context.print_universe()
    assert True  # yup, works. Don't know how to assert that though.


def test_process_sw_file_2():
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
    assert str(r) == '|op: return-home>'


def test_multi_value_stored_rules_1():
    s = """

foo (*,*) #=>
    the |result> => 3|__self1> + 5|__self2>

"""
    r = process_sw_file(context, s)
    context.print_universe()
    s = 'foo(|a>, |b>)'
    r1 = process_input_line(context, s, ket())
    s = 'foo(|a>.|b>, |x> + 7|y> )'
    r2 = process_input_line(context, s, ket())
    assert str(r1) == '3|a> + 5|b>'
    assert str(r2) == '3|a> . 3|b> + 5|x> + 35|y>'


def test_active_recall_1():
    context.learn('age', 'sam', '2')
    r = context.recall('age', ket('sam', 3), True)
    assert str(r) == '3|2>'


def test_new_compound_invoke_1():
    s = 'ssplit[" and "] |a and b>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a> . |b>'


def test_new_compound_invoke_2():
    context.load('sw-examples/fred-sam-friends.sw')
    s = 'common[friends] split |Fred Sam>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|Jack> + |Emma> + |Charlie>'


def test_new_compound_invoke_3():
    s = 'normalize[10] (3|a> + 2|b>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '6|a> + 4|b>'


def test_new_compound_invoke_4():
    s = 'threshold-filter[2] (3|a> + 2.2|b> - 3 |c> + |d>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '3|a> + 2.2|b> + 0|c> + 0|d>'


# let's test all our compound_ops:
def test_compound_invoke_smerge_1():
    s = 'smerge[", "] (|a> . |b> . |c> . |d>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a, b, c, d>'


def test_compound_invoke_insert_1():
    s = 'insert["Fred"] |hey {1}!>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|hey Fred!>'


def test_compound_invoke_insert_2():
    s = 'insert["Fred", "Sam"] |Hello {1} and {2}.>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|Hello Fred and Sam.>'


def test_compound_invoke_to_upper_1():
    s = 'to-upper[1] |fred>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|Fred>'


def test_compound_invoke_to_upper_2():
    s = 'to-upper[1,3,5] |abcdefg>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|AbCdEfg>'


def test_compound_invoke_remove_prefix_1():
    s = 'remove-prefix["not "] |not sitting at the beach>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|sitting at the beach>'


def test_compound_invoke_has_prefix_1():
    s = 'has-prefix["not "] |not sitting at the beach>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|yes>'


def test_compound_invoke_rel_kets_1():
    context.learn('is-hungry', 'fred', 'yes')
    context.learn('is-hungry', 'sam', 'no')
    s = 'rel-kets[is-hungry] |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|fred> + |sam>'


def test_compound_invoke_such_that_1():
    context.learn('is-hungry', 'fred', 'yes')
    context.learn('is-hungry', 'sam', 'no')
    s = 'such-that[is-hungry] rel-kets[supported-ops] |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|fred>'


def test_compound_invoke_table_1():
    context.load('sw-examples/fred-sam-friends.sw')
    s = 'table[person, friends] split |Fred Sam>'
    r = extract_compound_sequence(context, s)
    assert True  # yup, it works.


def test_compound_invoke_predict_1():
    context.load('sw-examples/integer-sequences.sw')
    s = 'predict[seq] (|2> . |5>)'
    r = extract_compound_sequence(context, s)
    # assert True                       # yup, it works.
    assert str(
        r) == '|count: 6 . 7 . 8 . 9 . 10> + |fib: 8 . 13> + |primes: 7 . 11 . 13 . 17 . 19 . 23> + 0.5|fact: 6 . 24 . 120>'


def test_compound_invoke_predict_2():
    context.load('sw-examples/integer-sequences.sw')
    s = 'predict[seq,1] (|2> . |5>)'
    r = extract_compound_sequence(context, s)
    # assert True                       # yup, it works.
    assert str(r) == '|count: 6> + |fib: 8> + |primes: 7> + 0.5|fact: 6>'


# only test this one out of the is-x family.
# I presume if one works, the rest do too.
def test_compound_invoke_is_greater_than_1():
    s = 'is-greater-than[3] |price: 3.50>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|yes>'


def test_compound_invoke_round_1():
    s = 'round[3] |3.14159265>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|3.142>'


def test_compound_invoke_times_by_1():
    s = 'times-by[5] |6.1>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|30.5>'


def test_compound_invoke_divide_by_1():
    s = 'divide-by[5] |625.5>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|125.1>'


def test_compound_invoke_int_divide_by_1():
    s = 'int-divide-by[1000] |123456>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|123>'


def test_compound_invoke_plus_1():
    s = 'plus[5] |3.14159265>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|8.14159265>'


def test_compound_invoke_minus_1():
    s = 'minus[2] |3.14159265>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|1.1415926500000002>'


def test_compound_invoke_mod_1():
    s = 'mod[1000] |1234567>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|567>'


def test_compound_invoke_is_mod_1():
    s = 'is-mod[3] |96>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|yes>'


def test_compound_invoke_learn_map_1():
    s = 'learn-map[3, 3] |>'
    r = extract_compound_sequence(context, s)
    assert True


def test_compound_invoke_learn_map_2():
    s = 'learn-map[5, 5] |>'
    r = extract_compound_sequence(context, s)
    s = 'display-map[5, 5] |>'
    r = extract_compound_sequence(context, s)
    assert True

def test_compound_invoke_sort_by_1():
    context.load('sw-examples/pretty-print-table-of-australian-cities.sw')
    s = 'sort-by[area] "" |city list>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|Darwin> + |Adelaide> + |Hobart> + |Melbourne> + |Sydney> + |Perth> + |Brisbane>'

def test_compound_invoke_active_buffer_1():
    s = """
|body part: face> => 2|eye> + |nose> + 2|ear> + 2|lip> + |hair>
"""
    r = process_sw_file(context, s)
    s = 'active-buffer[7,0] (2|eye> + |nose>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '0.375|body part: face>'

def test_compound_invoke_active_buffer_2():
    s = """
|body part: face> => 2|eye> + |nose> + 2|ear> + 2|lip> + |hair>
"""
    r = process_sw_file(context, s)
    s = 'active-buffer[7,0] (2|eye> + |nose> + 2|ear> + 2|lip> + |hair>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|body part: face>'

def test_compound_invoke_active_buffer_3():
    context.load('sw-examples/internet-acronyms.sw')
    s = 'active-buffer[7,0] read |text: fwiw I think it is all fud imho, lol. thx.>'
    r = extract_compound_sequence(context, s)
    assert str(r) == "|phrase: For What It's Worth> . |> . |> . |> . |> . |> . |phrase: Fear, Uncertainty, Doubt> . |phrase: In My Humble Opinion> . |phrase: Laughing Out Loud> . |phrase: Thanks>"

def test_compound_invoke_active_buffer_4():
    context.load('sw-examples/breakfast-menu.sw')
    s = 'active-buffer[7,0] read description |food: Homestyle Breakfast>'
    r = extract_compound_sequence(context, s)
    assert str(r) == "|number: 2> . |food: eggs> . |food: bacon> . |> . |food: sausage> . |food: toast> . |> . |> . |> . |food: hash browns> . |>"

def test_compound_invoke_active_buffer_5():
    context.load('sw-examples/active-buffer-example.sw')
    s = "active-buffer[7,0] read |text: Hey Freddie what's up?>"
    r = extract_compound_sequence(context, s)
    assert str(r) == "|greeting: Hey!> . 0.25|person: Fred Smith> . |question: what is> . |direction: up> + 0.333|phrase: up the duff>"

def test_compound_invoke_active_buffer_6():
    context.load('sw-examples/active-buffer-example.sw')
    s = "active-buffer[7,0] read |text: Hey Mazza, you with child, up the duff, in the family way, having a baby?>"
    r = extract_compound_sequence(context, s)
    assert str(r) == "|greeting: Hey!> . |person: Mary> . |> . |phrase: with child> . |> . |direction: up> + |phrase: up the duff> + 0.25|phrase: in the family way> . |> . |> . |phrase: in the family way> + 0.333|phrase: up the duff> . |> . |> . |> . |phrase: having a baby> . |> . |>"

def test_compound_invoke_active_buffer_7():
    context.load('sw-examples/active-buffer-example.sw')
    s = "active-buffer[7,0] active-buffer[7,0] read |text: Hey Mazza, you with child, up the duff, in the family way, having a baby?>"
    r = extract_compound_sequence(context, s)
    assert str(r) == "|> . |> . |> . 0.25|concept: pregnancy> . |> . 0.361|concept: pregnancy> . |> . |> . 0.5|concept: pregnancy> . |> . |> . |> . 0.25|concept: pregnancy> . |> . |>"




def test_new_sequence_fn_invoke_1():
    s = 'union(|a>, |b>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a> + |b>'


def test_new_sequence_fn_invoke_tri_union_1():
    s = 'union(|a>, |b>, |c>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a> + |b> + |c>'


# test process_single_op replacement code:
# one branch at a time
def test_multiply_1():
    s = '3^9 |x>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '19683|x>'


def test_quote_operator_1():
    context.learn('', 'foo', 'bah')
    s = '"" |foo>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|bah>'


def test_built_in_table_1():
    s = 'normalize (|a> + |b> + |c>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '0.333|a> + 0.333|b> + 0.333|c>'


def test_sigmoid_table_1():
    s = 'clean (3|a> + 0.5|b> - 2 |c>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a> + |b> + 0|c>'


def test_fn_table_1():
    s = 'extract-category |a: b: c>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a: b>'


def test_sp_fn_table_1():
    s = 'rank (|a> + |b> + |c>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a> + 2|b> + 3|c>'


def test_seq_fn_table_1():
    s = 'smerge (|F> . |r> . |e> . |d>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|Fred>'


def test_ket_context_table_1():
    s = 'int-coeffs-to-word (3|apple> + 2|pear> + |orange> + 7|lemon>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|3 apple> + |2 pear> + |1 orange> + |7 lemon>'


# don't have an example yet.
# def test_sp_context_table_1():
#  s = ''

def test_literal_op_1():
    context.learn('age', 'fred', '25')
    s = 'age |fred>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|25>'


def test_literal_op_1():
    context.learn('age', 'fred', stored_rule('|37>'))
    s = 'age |fred>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|37>'


# try to fix add-learn bug:
# fixed it! It was a very sneaky parser bug.
# indirect add-learn rules were parsing as invalid, and so treated as '=>'
# I had to add ~'+=>' to the front of the symbol_single_compound_sequence parse rule to fix
#
def test_add_learn_bug_1():
    s = """

current |cell> => |grid: 5: 5>
stored-food current |cell> +=> 5| >
stored-food current |cell> +=> 5| >
stored-food current |cell> +=> 5| >

"""
    r = process_sw_file(context, s)
    s = 'stored-food current |cell>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '15| >'


# this case has no issues:
def test_add_learn_bug_2():
    s = """

stored-food |grid: 7: 7> +=> 7| >
stored-food |grid: 7: 7> +=> 7| >
stored-food |grid: 7: 7> +=> 7| >

"""
    r = process_sw_file(context, s)
    s = 'stored-food |grid: 7: 7>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '21| >'


# solve the sequence add bug.
# I don't know what is going on!
# solved.
# it had a weird bug when the first element of a sequence was |>
# in which case __str__ reported the entire sequence as |>
def test_sequence_add_1():
    seq = sequence([])
    r = superposition('5')
    seq += r
    r = superposition('7')
    seq += r
    assert str(seq) == '|5> . |7>'


def test_sequence_add_2():
    context.learn('is-prime', '*', stored_rule('is-prime |_self>'))
    s = 'such-that[is-prime] ssplit |123456789>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|2> . |3> . |5> . |7>'

# learn seq rules:
# spell |fred> .=> |f>
# spell |fred> .=> |r>
# spell |fred> .=> |e>
# spell |fred> .=> |d>
def test_seq_learn_1():
    context.seq_learn('spell', 'fred', 'f')
    context.seq_learn('spell', 'fred', 'r')
    context.seq_learn('spell', 'fred', 'e')
    context.seq_learn('spell', 'fred', 'd')
    r = context.recall('spell', 'fred')
    assert str(r) == '|f> . |r> . |e> . |d>'

def test_seq_learn_2():
    context.seq_learn('pattern', 'a', ket('a',2) + ket('b', 0.3))
    context.seq_learn('pattern', 'a', ket('x', 5.5) + ket('y', -7) + ket('z'))
    r = context.recall('pattern', 'a')
    assert str(r) == '2|a> + 0.3|b> . 5.5|x> - 7|y> + |z>'

def test_seq_learn_3():
    s = """
pattern |b> .=> 0.4|a> + 0.9|b>
pattern |b> .=> |x>  + 2|y> - |z>
"""
    r = process_sw_file(context, s)
    r = context.recall('pattern', 'b')
    assert str(r) == '0.4|a> + 0.9|b> . |x> + 2|y> - |z>'

def test_indirect_seq_learn_1():
    s = """
indirect |foo> => |c>
pattern indirect |foo> .=> 3|a>
pattern indirect |foo> .=> 2|b> - 7|c>
pattern indirect |foo> .=> |x> + |y> + |z>
"""
    r = process_sw_file(context, s)
    r = context.recall('pattern', 'c')
    assert str(r) == '3|a> . 2|b> - 7|c> . |x> + |y> + |z>'


def test_extract_compound_sequence_empty_learn_1():
    s = '|>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|>'

def test_extract_compound_sequence_empty_learn_2():
    s = '|> . |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == 'fish'

def test_extract_compound_sequence_empty_learn_3():
    s = '|> . |> . |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == 'fish'

def test_extract_compound_sequence_empty_learn_4():
    s = '|a> . |b> . |c>'
    r = extract_compound_sequence(context, s)
    assert str(r) == 'fish'

def test_extract_compound_sequence_empty_learn_5():
    s = '|> . |> . |a> . |b> . |a> . |> . |> . |b> . |> . |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == 'fish'

def test_find_path_between_1():
    context.load('sw-examples/fred-sam-friends.sw')
    context.create_inverse_op('friends')
    # context.print_universe()
    r = find_path_between(context, ket('Fred'), ket('Sam'))
    assert str(r) == '|op: friends> . |op: inverse-friends>'

def test_find_path_between_2():
    context.load('sw-examples/fred-sam-friends.sw')
    context.create_inverse_op('friends')
    # context.print_universe()
    r = find_path_between(context, ket('Fred'), ket('Julie'))
    assert str(r) == '|op: friends> . |op: inverse-friends> . |op: friends>'

