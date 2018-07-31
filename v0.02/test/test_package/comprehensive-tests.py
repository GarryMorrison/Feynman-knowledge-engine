#######################################################################
# let's do a comprehensive test of version 2
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 27/7/2018
# Update: 31/7/2018
# Copyright: GPLv3
#
# Usage: py.test -v comprehensive-tests.py
#
#######################################################################

from semantic_db import *
context.load('sw-examples/fred-sam-friends.sw')
context.load('sw-examples/test-operators.sw')


# test the parser section:
def test_literal_sequence_1():
    x = op_grammar(' |a> - 2.1|b> + 3|c> _ 7.9|d> . 29.9|e> + |f> . |fish> __ |soup> + 13.2|pasta> ').literal_sequence()
    assert str(x) == '|a> - 2.1|b> + 23.7|cd> . 29.9|e> + |f> . |fish soup> + 13.2|pasta>'

# parse error due to the ( ). This is not a bug!
# literal-sequence was not designed to handle brackets
# def test_literal_sequence_2():
#     x = op_grammar(' |1> __ (|a> + |b> + |c>) + |2> __ (|d> + |e> + |f>) ').literal_sequence()
#     assert str(x) == ''


def test_single_compound_sequence_1():
    x = op_grammar(' 3|x>').single_compound_sequence()
    assert x == [[3], 'x']

def test_single_compound_sequence_2():
    x = op_grammar(' op3  op2 op1 |x>').single_compound_sequence()
    assert x == [['op3', 'op2', 'op1'], 'x']

def test_single_compound_sequence_3():
    x = op_grammar(' select[1,2]^3  op2 op1 3.14|pi>').single_compound_sequence()
    assert x == [[(['c_op', 'select', 1, 2], 3), 'op2', 'op1', 3.14], 'pi']


def test_full_compound_sequence_1():
    x = op_grammar(' select[1,2]^3  op2 op1 3.14|pi>').full_compound_sequence()
    assert x == [('+', [[(['c_op', 'select', 1, 2], 3), 'op2', 'op1', 3.14], 'pi'])]

def test_full_compound_sequence_2():
    x = op_grammar(' |a> - 2.1|b> + 3|c> _ 7.9|d> . 29.9|e> + |f> . |fish> __ |soup> + 13.2|pasta> ').full_compound_sequence()
    print(x)
    assert x == [('+', [[], 'a']), ('-', [[2.1], 'b']), ('+', [[3], 'c']), ('_', [[7.9], 'd']), ('.', [[29.9], 'e']), ('+', [[], 'f']), ('.', [[], 'fish']), ('__', [[], 'soup']), ('+', [[13.2], 'pasta'])]

def test_full_compound_sequence_3():
    x = op_grammar(' |1> __ (|a> + |b>) + |2> __ (|d> + |e> + |f>) ').full_compound_sequence()
    assert x == [('+', [[], '1']), ('__', [[], [('+', [[], 'a']), ('+', [[], 'b'])]]), ('+', [[], '2']), ('__', [[], [('+', [[], 'd']), ('+', [[], 'e']), ('+', [[], 'f'])]])]



def test_general_op_1():
    x = op_grammar('select[1,3]').general_op()
    assert x == ['c_op', 'select', 1, 3]

def test_general_op_2():
    x = op_grammar('such-that( |a>, |b> + 2|c>, 3|d> . 1.7|e>)').general_op()
    assert x == ['f_op', 'such-that', [('+', [[], 'a'])], [('+', [[], 'b']), ('+', [[2], 'c'])], [('+', [[3], 'd']), ('.', [[1.7], 'e'])]]


def test_bracket_ops_1():
    x = op_grammar('(op3 op2 + op1 _ op)').bracket_ops()
    assert x == [('+', ['op3', 'op2']), ('+', ['op1']), ('_', ['op'])]


def test_op_sequence_1():
    x = op_grammar('op4 select[1,3]^2 such-that(|a>, |b>) op1').op_sequence()
    assert x == ['op4', (['c_op', 'select', 1, 3], 2), ['f_op', 'such-that', [('+', [[], 'a'])], [('+', [[], 'b'])]], 'op1']

def test_op_sequence_2():
    x = op_grammar(' (op3 op2 + op1 _ op) ').op_sequence()
    assert x == [[('+', ['op3', 'op2']), ('+', ['op1']), ('_', ['op'])]]

def test_op_sequence_3():
    x = op_grammar(' op8 op7^3 (op6 . op5)^2 op4 (op3 + op2 _ op1) ').op_sequence()
    # print(x)
    assert x == ['op8', ('op7', 3), ([('+', ['op6']), ('.', ['op5'])], 2), 'op4', [('+', ['op3']), ('+', ['op2']), ('_', ['op1'])]]

def test_op_sequence_4():
    x = op_grammar('(op3 + op2 _ op1) select[1,3] ').op_sequence()
    # print(x)
    assert x == [[('+', ['op3']), ('+', ['op2']), ('_', ['op1'])], ['c_op', 'select', 1, 3]]

def test_op_sequence_5():
    x = op_grammar(' op8 op7^3 (op6 . op5)^2 op4 (op3 + op2 _ op1) select[1,3] such-that(|_seq>) ').op_sequence()
    # print(x)
    assert x == ['op8', ('op7', 3), ([('+', ['op6']), ('.', ['op5'])], 2), 'op4', [('+', ['op3']), ('+', ['op2']), ('_', ['op1'])], ['c_op', 'select', 1, 3], ['f_op', 'such-that', [('+', [[], '_seq'])]]]



def test_full_compound_sequence_naked_union_1():
    x = op_grammar(' union(|a>, |b>)').full_compound_sequence()
    print(x)
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


# these next two are currently incompletely implemented in the compiler:
# fixed!
def test_full_compound_sequence_union_input_seq_1():
    x = op_grammar('union(|a>, |b>) (|x> . |y>) ').full_compound_sequence()
    assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]]], [('+', [[], 'x']), ('.', [[], 'y'])]])]

def test_full_compound_sequence_union_input_op_seq_2():
    x = op_grammar('union(|a>, |b>) op1 op2 (|x> . |y>) ').full_compound_sequence()
    assert x == [('+', [[['f_op', 'union', [('+', [[], 'a'])], [('+', [[], 'b'])]], 'op1', 'op2'], [('+', [[], 'x']), ('.', [[], 'y'])]])]



# test the compiler section:
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
    assert str(x) == '|a> - 2.1|b> + 23.7|cd> . 29.9|e> + |f> . |fish soup> + 13.2|pasta>'

# current code ignores the seq to the right of the sequence function
# Maybe one day change that, and convert the back-end: union(one, two) to union(input-seq, one, two)
# that would be quite a bit of work though!!
# not sure how we would handle foo (*,*,*) rules though. Would they need input-seq fed to them too?
# Heh, we could call the input-seq |_self0>, and that would result in less breakage.
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

# strange that this one fails. How long has that been the case??
# it works in the test_parser directory!
# $ py.test -v test_parser_v2.py | grep 'test_compiler_simple_op_bracket_1'
# test_parser_v2.py::test_compiler_simple_op_bracket_1 PASSED
#
# some more data points:
# foo |*> #=> |foo:> __ |_self>
# op (*) #=> |op:> __ |_self>
#
# now test them:
# sa: foo(|x> + |y>)
# |>
#
# sa: foo (|x> + |y>)
# |foo: x> + |foo: y>
#
# sa: op(|x> + |y>)
# |op: x> + |op: y>
#
# sa: op (|x> + |y>)
# |op: x> + |op: y>
#
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



def test_single_ket():
    x = op_grammar(' |Fred> + |Sam> ').compiled_compound_sequence()
    assert str(x) == '|Fred> + |Sam>'

def test_single_sequence():
    x = op_grammar(' (|Fred> + |Sam>) ').compiled_compound_sequence()
    assert str(x) == '|Fred> + |Sam>'

def test_common_friends():
    x = op_grammar(' common[friends] (|Fred> + |Sam>) ').compiled_compound_sequence()
    assert str(x) == '|Jack> + |Emma> + |Charlie>'



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
    assert str(x) == '|x> + 0.5|y> + 2.7|z> + |fish> - |cats> - |dogs> + |mice> + |rats>'


# this is broken, and I don't exactly know why, or where to fix it.
# hiding somewhere in the compiler I presume
# but I'm not eager to go tinkering with the compiler!
def test_buggy_merge():
    x = op_grammar(' |1> __ (|a> + |b> + |c>) + |2> __ (|d> + |e> + |f>) ').compiled_compound_sequence()
    assert str(x) == '|1 a> + |1 b> + |1 c> + |2 d> + |2 e> + |2 f>'


def test_op_sentence_sum():
    x = op_grammar(' 3^2 common[friends] split |Fred Sam> + |mice> + (|cats> + |dogs>) + split |horse pony mare> ').compiled_compound_sequence()
    print(x)
    assert str(x) == '9|Jack> + 9|Emma> + 9|Charlie> + |mice> + |cats> + |dogs> + |horse> + |pony> + |mare>'

def test_op_sentence_sum_v2():
    x = op_grammar(" 3^2 common[friends] split |Fred Sam> _ |mice> - (|cats> + |dogs>) . split |horse pony mare> ").compiled_compound_sequence()
    print(x)
    assert str(x) == '9|Jack> + 9|Emma> + 9|Charliemice> - |cats> - |dogs> . |horse> + |pony> + |mare>'

# has the same issue as: test_compiler_simple_op_bracket_1
def test_tuple_op_4_bracket_op():
    x = op_grammar(' op5((- op4 + op3 __ op2 . op1)) |x>   ' ).compiled_compound_sequence()
    assert str(x) == ''

def test_tuple_op_4_bracket_op_2():
    x = op_grammar(' op5 ((- op4 + op3 __ op2 . op1)) |x>   ' ).compiled_compound_sequence()
    assert str(x) == ' - |op5: op4: x> + |op5: op3: x op2: x> . |op5: op1: x>'



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
    assert str(x) == '|fish> - |cats> - |dogs>'


def test_distributed_minus_2():
    x = op_grammar(' |fish> - (((|cats> + |dogs>))) ').compiled_compound_sequence()
    assert str(x) == '|fish> - |cats> - |dogs>'


def test_distributed_minus_3():
    x = op_grammar(' |fish> - split |cats dogs> ').compiled_compound_sequence()
    assert str(x) == '|fish> - |cats> - |dogs>'


def test_distributed_minus_4():
    x = op_grammar(' |fish> - union( |cats> ,  |dogs> ) ').compiled_compound_sequence()
    assert str(x) == '|fish> - |cats> - |dogs>'


def test_distributed_minus_5():
    x = op_grammar(' |fish> - |cats> + |dogs> ').compiled_compound_sequence()
    assert str(x) == '|fish> - |cats> + |dogs>'


# it is not entirely clear how '(op3 __ op2) seq' should be handled:
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
    assert str(x) == '|op3: x> - |op2: x>'


def test_bracket_ops_minus_2():
    x = op_grammar(' (op3 - op2) (|x> + |y>) ').compiled_compound_sequence()
    assert str(x) == '|op3: x> + |op3: y> - |op2: x> - |op2: y>'


def test_bracket_ops_dot_1():
    x = op_grammar(' (op3 . op2) |x> ').compiled_compound_sequence()
    assert str(x) == '|op3: x> . |op2: x>'


def test_bracket_ops_dot_2():
    x = op_grammar(' (op3 . op2) (|x> + |y>) ').compiled_compound_sequence()
    assert str(x) == '|op3: x> + |op3: y> . |op2: x> + |op2: y>'


def test_bracket_ops_dot_3():
    x = op_grammar(' (op3 . op2) split |x y> ').compiled_compound_sequence()
    assert str(x) == '|op3: x> + |op3: y> . |op2: x> + |op2: y>'


def test_tuple_op_1():
    x = op_grammar(' op1^3 |x> ').compiled_compound_sequence()
    assert str(x) == '|op1: op1: op1: x>'


def test_tuple_op_2():
    x = op_grammar('  (  ( op1 ))^3 |x> ').compiled_compound_sequence()
    assert str(x) == '|op1: op1: op1: x>'



# the learn rule section:
def test_learn_standard_rule_1():
    x = op_grammar(' age |Fred> => |37> ').learn_rule()
    r = context.recall('age', 'Fred')
    assert str(r) == '|37>'


def test_learn_standard_rule_2():
    x = op_grammar(' spell |Fred> => |F> . |r> . |e> . |d> ').learn_rule()
    r = context.recall('spell', 'Fred')
    assert str(r) == '|F> . |r> . |e> . |d>'


def test_learn_stored_rule_1():
    x = op_grammar(' |ket> #=> |foo> ').stored_rule()
    r = context.recall('', 'ket')
    assert str(r) == '|foo> '


def test_learn_stored_rule_2():
    x = op_grammar('op |ket> #=> |bah> ').stored_rule()
    r = context.recall('op', 'ket')
    assert str(r) == '|bah> '


def test_learn_memoizing_rule_1():
    x = op_grammar(' measure |system> !=> some |state> ').stored_rule()
    r = context.recall('measure', 'system')
    assert str(r) == 'some |state> '


def test_learn_star_ket_1():
    x = op_grammar(' star |*> #=> supported-ops |_self> ').stored_rule()
    context.print_universe()
    y = context.recall('star', 'Fred')
    assert str(y) == 'supported-ops |_self> '


def test_learn_star_rule_1():
    x = op_grammar(' star1 (*) #=> supported-ops |_self> ').stored_rule()
    context.print_universe()
    y = context.seq_fn_recall('star1', ['', 'Sam'])
    assert str(y) == 'supported-ops |_self> '


def test_learn_star_rule_2():
    x = op_grammar(' star2 (*,*) #=> supported-ops |_self1> + age |_self2> ').stored_rule()
    context.print_universe()
    y = context.seq_fn_recall('star2', ['', 'Sam', 'Fred'])
    assert str(y) == 'supported-ops |_self1> + age |_self2> '


def test_learn_star_rule_active_1():
    x = op_grammar(' star1 (*) #=> supported-ops |_self> ').stored_rule()
    context.print_universe()
    y = context.seq_fn_recall('star1', ['', 'Sam'], active=True)
    assert str(y) == '|op: friends>'


def test_learn_star_rule_active_2():
    x = op_grammar(' star2 (*,*) #=> supported-ops |_self1> + age |_self2> ').stored_rule()
    context.print_universe()
    y = context.seq_fn_recall('star2', ['', 'Sam', 'Fred'], active=True)
    assert str(y) == '|op: friends> + |37>'



# test some smaller components:
def test_line_parse_1():
    x = op_grammar(' some random string ').line()
    assert x == ' some random string '


# this is meant to fail:
# def test_line_parse_2():
#     x = op_grammar(' some random string \n ').line()
#     assert x == ''

def test_filtered_parameter_string_empty_1():
    x = op_grammar('""').filtered_parameter_string()
    assert x == ''


def test_filtered_parameter_string_2():
    x = op_grammar('" fish "').filtered_parameter_string()
    assert x == ' fish '


# meant to fail:
# the goal was to try to eliminate SQL injection type attacks
# def test_filtered_parameter_string_3():
#    x = op_grammar('" fish ] ["').filtered_parameter_string()
#    assert x == ''


def test_object_1():
    x = op_grammar('|Fred>').object()
    assert x == 'Fred'


def test_object_2():
    x = op_grammar('|*>').object()
    assert x == '*'


def test_object_3():
    x = op_grammar('(*,*)').object()
    assert x == '(*,*)'


def test_object_4():
    x = op_grammar('the |list>').object()
    assert x == [('+', [['the'], 'list'])]


def test_sw_file_1():
    x = op_grammar('age |Julie> => |32> \n spell-out |Julie> => |J> . |u> . |l> . |i> . |e> \n\n\n\n friends |Julie> #=> |Fred> + |Sam> + |Robert> ').sw_file()
    context.print_universe()
    y = op_grammar('spell-out|Julie>').recall_rule()
    assert str(y) == '|J> . |u> . |l> . |i> . |e>'

def test_sequence_sigmoids_1():
    x = op_grammar(' foo |bah> => 3|a> + 2.2 |b> . 3.14|pi> . 2.7|e> - 3(|cats> + |dogs>)').sw_file()
    #context.print_universe()
    y = op_grammar(' clean foo |bah>').compiled_compound_sequence()
    assert str(y) == '|a> + |b> . |pi> . |e> + 0|cats> + 0|dogs>'



# test |_self> ket insertions:
def test_self_object_1():
    x = op_grammar(' age |Fred> => 33|_self> ').learn_rule()
    context.print_universe()
    r = context.recall('age', 'Fred')
    assert str(r) == '33|Fred>'


def test_self_object_2():
    x = op_grammar(' 33 |_self> ').full_compound_sequence()
    r = compile_compound_sequence(context, x, 'rabbit')
    assert str(r) == '33|rabbit>'


def test_self_object_3():
    x = op_grammar(' 13 (|x> + |y> . |_self> + |z>) ').full_compound_sequence()
    r = compile_compound_sequence(context, x, 'rabbit')
    assert str(r) == '13|x> + 13|y> . 13|rabbit> + 13|z>'


def test_self_object_4():
    x = op_grammar(' 13 (|x> + |y> . |_self> + |z>) ').full_compound_sequence()
    r = compile_compound_sequence(context, x, ket('rabbit', 2))
    assert str(r) == '13|x> + 13|y> . 26|rabbit> + 13|z>'


def test_self_object_5():
    x = op_grammar(' 13 (|x> + |y> . |_self> + |z>) ').full_compound_sequence()
    r = compile_compound_sequence(context, x, ket('rabbit', 2) + ket('soup', 7))
    assert str(r) == '13|x> + 13|y> . 26|rabbit> + 91|soup> + 13|z>'


def test_self_object_6():
    x = op_grammar(' 13 (|x> + |y> . |_self> + |z>) ').full_compound_sequence()
    a = sequence('a') + sequence('b') + sequence('c')
    r = compile_compound_sequence(context, x, a)
    assert str(r) == '13|x> + 13|y> . 13|a> . 13|b> . 13|c> + 13|z>'


def test_self_object_7():
    x = op_grammar(' 13 (|x> + |y> . |_self> + |z>) ').full_compound_sequence()
    a = sequence('a') + ket('b', 2) + ket('c', 3)
    r = compile_compound_sequence(context, x, a)
    assert str(r) == '13|x> + 13|y> . 13|a> . 26|b> . 39|c> + 13|z>'



# test extract_compound_sequence |_self> insertions:
def test_extract_compound_sequence_1():
    s = '5|_self>'
    seq = extract_compound_sequence(context, s, 'fish')
    assert str(seq) == '5|fish>'


def test_extract_compound_sequence_1():
    s = '5|_self1> + 7|_self2>'
    seq = extract_compound_sequence(context, s, ['', 'fish', 'soup'])
    assert str(seq) == '5|fish> + 7|soup>'


def test_star_learn_1():
    s = 'foo (*) => |bah>'
    process_sw_file(context, s)
    context.print_multiverse()
    s = 'foo (|a> + 2|b> . |c>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|bah>'


def test_star_learn_2():
    s = 'foo-2 (*,*) => |bah 2>'
    process_sw_file(context, s)
    context.print_multiverse(True)
    s = 'foo-2(|a> + 2|b> . |c>, |x> . 3|y> )'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|bah 2>'


# test learn indirectly:
def test_learn_indirectly_1():
    x = op_grammar('|list> => split |Eric Rob Matt>\n age "" |list> => 23 |_self> ').sw_file()
    context.print_universe()
    y = context.recall('age', 'Rob')
    assert str(y) == '23|Rob>'

def test_learn_indirectly_2():
    x = op_grammar(' age-self friends split |Fred Sam> => 20 clean |_self>').sw_file()
    context.print_universe()
    y = context.recall('age-self', 'Patrick')
    assert str(y) == '20|Patrick>'



# test seq_fn_learn and seq_fn_recall:
def test_context_seq_fn_learn_1():
    context.seq_fn_learn('op-a', '*', 'value a')
    context.print_universe()
    r = context.seq_fn_recall('op-a', ['', 'fish'])
    assert str(r) == '|value a>'


def test_context_seq_fn_learn_2():
    context.seq_fn_learn('op-b', '*,*', 'value b')
    context.print_universe(True)
    r = context.seq_fn_recall('op-b', ['', 'fish', 'soup'])
    assert str(r) == '|value b>'


def test_context_seq_fn_learn_3():
    context.seq_fn_learn('op-c', '*,*', stored_rule('|_self1>'))
    context.print_universe(True)
    r = context.seq_fn_recall('op-c', ['', 'fish', 'soup'], active=True)
    assert str(r) == '|fish>'


def test_context_seq_fn_learn_4():
    context.seq_fn_learn('op-d', '*,*', stored_rule('|_self>'))
    context.print_universe(True)
    r = context.seq_fn_recall('op-d', ['', 'more', 'soup'], active=True)
    assert str(r) == '|more>'


def test_context_seq_fn_learn_5():
    context.seq_fn_learn('op-e', '*', stored_rule('|_self>'))
    context.print_universe(True)
    r = context.seq_fn_recall('op-e', ['', 'soup'], active=True)
    assert str(r) == '|soup>'


def test_context_seq_fn_learn_6():
    context.seq_fn_learn('op-f', '*,*', stored_rule('3|_self1> + 5|_self2>'))
    context.print_universe(True)
    r = context.seq_fn_recall('op-f', ['', 'fish', 'soup'], active=True)
    assert str(r) == '3|fish> + 5|soup>'


# test seq_learn:

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



# test extract_compound_sequence and |>:
# for some reason it chomps the leading |>
# not a super urgent bug, but would be nice to fix!
def test_extract_compound_sequence_empty_learn_1():
    s = '|>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|>'

def test_extract_compound_sequence_empty_learn_2():
    s = '|> . |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|> . |>'

def test_extract_compound_sequence_empty_learn_3():
    s = '|> . |> . |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|> . |> . |>'

def test_extract_compound_sequence_empty_learn_4():
    s = '|a> . |b> . |c>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|a> . |b> . |c>'

def test_extract_compound_sequence_empty_learn_5():
    s = '|> . |a> . |b> . |a> . |> . |> . |b> . |> . |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|> . |a> . |b> . |a> . |> . |> . |b> . |> . |>'


def test_extract_compound_sequence_empty_learn_6():
    s = '|> . |> . |a> . |b> . |a> . |> . |> . |b> . |> . |>'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|> . |> . |a> . |b> . |a> . |> . |> . |b> . |> . |>'


def test_extract_compound_sequence_input_seq():
    s = 'test-input-seq(|a>, |b>) (|x> . |y>)'
    r = extract_compound_sequence(context, s)
    assert str(r) == '|x> . |y>'


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
    assert str(r2) == '3|a> . 3|b> + 5|x> + 35|y>'  # yeah, addition of sp to seq is kind of weird.


def test_multi_line_stored_rule_1():
    s = """

multi |*> #=>
    multi-op1 |a> => |b>
    multi-op2 |b> => |c>
    multi-op3 |c> => |d>    

"""
    r = process_sw_file(context, s)
    r = context.recall('multi', 'x', active=True)
    context.print_universe()
    r1 = context.recall('multi-op1', 'a')
    r2 = context.recall('multi-op2', 'b')
    r3 = context.recall('multi-op3', 'c')
    assert str(r1) == '|b>'
    assert str(r2) == '|c>'
    assert str(r3) == '|d>'


def test_seq_fn_input_seq_1():
    s = """
foo-input-seq (*,*) #=> 2|_self0> + 3|_self1> + 5|_self2>
"""
    r = process_sw_file(context, s)
    context.print_universe()
    s = 'foo-input-seq(|a>, |b>) (|x> . |y>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '2|x> . 2|y> + 3|a> + 5|b>'

def test_seq_fn_input_seq_2():
    s = """

bah-input-seq (*,*) #=>
    the |result> => 2|__self0> + 3|__self1> + 5|__self2>
    

"""
    r = process_sw_file(context, s)
    s = 'bah-input-seq(|a>, |b>) (|x> . |y>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '2|x> . 2|y> + 3|a> + 5|b>'



# a bunch of test self insert cases:
def test_self_insert_1():
    s = """
foo1 |*> #=> 13|_self>

"""
    r = process_sw_file(context, s)
    s = 'foo1 (|x> + |y> + |z>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '13|x> + 13|y> + 13|z>'

# |*> rules do not process |_selfk> rules:
# so the result is not a bug
def test_self_insert_2():
    s = """
foo2 |*> #=> 13|_self0> + 17|_self1>

"""
    r = process_sw_file(context, s)
    s = 'foo2 (|x> + |y> + |z>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '39|_self0> + 51|_self1>'

def test_self_insert_3():
    s = """
foo3 (*) #=> 19|_self>

"""
    r = process_sw_file(context, s)
    s = 'foo3 (|x> + |y> + |z>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '19|x> + 19|y> + 19|z>'

def test_self_insert_4():
    s = """
foo4 (*) #=> 23|_self1>

"""
    r = process_sw_file(context, s)
    s = 'foo4 (|x> + |y> + |z>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '23|x> + 23|y> + 23|z>'

def test_self_insert_5():
    s = """
foo5 (*) #=> 29|_self0>

"""
    r = process_sw_file(context, s)
    s = 'foo5 (|x> + |y> + |z>)'
    r = process_input_line(context, s, ket())
    assert str(r) == ''

def test_self_insert_6():
    s = """
foo6 (*) #=> 29|_self0> + 31|_self1>

"""
    r = process_sw_file(context, s)
    s = 'foo6 (|x> + |y> + |z>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '31|x> + 31|y> + 31|z>'

def test_self_insert_7():
    s = """
foo7 (*) #=> 37|_self0> + 41|_self1>

"""
    r = process_sw_file(context, s)
    s = 'foo7(|x> + |y> + |z>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '41|x> + 41|y> + 41|z>'

def test_self_insert_8():
    s = """
foo8 (*) #=> 43|_self0> + 47|_self1>

"""
    r = process_sw_file(context, s)
    s = 'foo8(|x> + |y> + |z>) (|a> + |b>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '43|a> + 43|b> + 47|x> + 47|y> + 47|z>'

def test_self_insert_9():
    s = """
foo9 (*,*) #=> 53|_self0> + 59|_self1> + 61|_self2>

"""
    r = process_sw_file(context, s)
    s = 'foo9(|x>, |y>) (|a> + |b>)'
    r = process_input_line(context, s, ket())
    assert str(r) == '53|a> + 53|b> + 59|x> + 61|y>'
