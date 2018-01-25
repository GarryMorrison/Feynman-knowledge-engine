#!/usr/bin/env python3

#######################################################################
# code to test v0.02 the_semantic_db_code.py
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-1-23
# Update: 2018-1-25
# Copyright: GPLv3
#
# Usage: py.test -v test_code.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *


context = context_list("semantic db code")
context.load("sw-examples/fred-sam-friends.sw")    # currently fails to load.
#context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
#context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
context.print_multiverse()
#print(context.dump_multiverse())
#sys.exit(0)


def test_empty_ket():
  x = ket()
  assert str(x) == '|>'

def test_string_ket():
  x = ket('fred')
  assert str(x) == '|fred>'

def test_string_int_ket():
  x = ket('fred',3)
  assert str(x) == '3|fred>'

def test_string_float_ket():
  x = ket('fred',3.141592)
  assert str(x) == '3.142|fred>'

def test_ket_addition():
  x = ket('fred', 3.2)
  y = ket('fred', 5)
  assert str(x + y) == '8.2|fred>'

def test_ket_addition_2():
  x = ket('fred')
  y = ket('sam',2.9)
  z = ket('hank')
  assert str(x + y + z) == '|fred> + 2.9|sam> + |hank>'

def test_ket_subtraction():
  x = ket('fred')
  y = ket('sam',2.9)
  assert str(x - y) == '|fred> + -2.9|sam>'

def test_superposition_init_sp():
  x = ket('fred')
  y = ket('sam',2.9)
  z = superposition(x + y)
  assert str(z) == '|fred> + 2.9|sam>'
  
def test_superposition_empty_ket_addition():
  x = ket()
  y = ket('fred')
  z = ket('sam')
  assert str(y + x + z) == '|fred> + |sam>'

def test_superposition_empty_ket_with_value_addition():
  x = ket('',3.1415)
  y = ket('fred')
  z = ket('sam')
  assert str(y + x + z) == '|fred> + |sam>'

def test_ket_extract_value():
  x = ket('a: b: c').apply_fn(extract_value)
  assert str(x) == '|c>'
  
def test_ket_extract_category():
  x = ket('a: b: c').apply_fn(extract_category)
  assert str(x) == '|a: b>'

def test_ket_apply_value_fail():
  x = ket('price: fish').apply_fn(apply_value)
  assert str(x) == '|price: fish>'

def test_ket_apply_value_float():
  x = ket('price: 37.25').apply_fn(apply_value)
  assert str(x) == '37.25|price: 37.25>'

def test_ket_greater_than_pass():
  x = ket('price: 37.25').apply_fn(greater_than,20)
  assert str(x) == '|price: 37.25>'

def test_ket_greater_than_fail():
  x = ket('price: 37.25').apply_fn(greater_than,40)
  assert str(x) == '|>'

def test_ket_letter_ngrams():
  x = ket('fish').apply_fn(make_ngrams,"1,2","letter")
  assert str(x) == '|f> + |i> + |s> + |h> + |fi> + |is> + |sh>'

def test_sp_greater_than_pass():
  x = ket('price: 37.25') + ket('price: 19.94') + ket('price: 10.50') + ket('price: 25.00')
  y = x.apply_fn(greater_than,20)
  assert str(y) == '|price: 37.25> + |price: 25.00>'


def test_ket_ket_merge():
  x = ket('fish')
  y = ket('soup')
  z = x.merge(y)
  assert str(z) == '|fishsoup>'

def test_ket_ket_merge():
  x = ket('fish')
  y = ket('soup') + ket(' tonight')
  z = x.merge(y)
  assert str(z) == '|fishsoup>'

def test_sp_select_elt_out_of_range():
  x = ket('a') + ket('b') + ket('c') + ket('d')
  y = x.select_elt(7)
  assert str(y) == '0|>'

def test_sp_select_elt_1():
  x = ket('a') + ket('b') + ket('c') + ket('d')
  y = x.select_elt(1)
  assert str(y) == '|a>'

def test_sp_select_elt_3():
  x = ket('a') + ket('b') + ket('c') + ket('d')
  y = x.select_elt(3)
  assert str(y) == '|c>'

def test_sp_select_elt_neg_1():
  x = ket('a') + ket('b') + ket('c') + ket('d')
  y = x.select_elt(-1)
  assert str(y) == '|d>'

def test_ket_seq_merge():
  x = ket('fish')
  y = ket('soup')
  z = x.seq_add(y)
  assert str(z) == '|fish> . |soup>'

def test_ket_apply_op_friends():
  context = context_list("test apply_op")
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
  x = ket('Fred').apply_op(context, "friends")
  assert str(x) == '|Sam> + |Max> + |Harry>'


def test_ket_apply_sp_fn_common_friends():
  context = context_list("test common")
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
  x = ket('Fred')
  y = x.apply_sp_fn(common,context,"friends")
  assert str(y) == '|Sam> + |Max> + |Harry>'

def test_sp_apply_sp_fn_common_friends():
  context = context_list("test common")
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
  x = ket('Fred') + ket('Sam')
  y = x.apply_sp_fn(common,context,"friends")
  assert str(y) == '|Max> + |Harry>'

def test_ket_normalize():
  x = ket('Fred', 3.72)
  y = x.normalize(2)
  assert str(y) == '2|Fred>'

def test_sp_normalize():
  x = ket('Fred', 3.72) + ket('Sam') + ket('Harry',0.3)
  y = x.normalize(1)
  assert str(y) == '0.741|Fred> + 0.199|Sam> + 0.06|Harry>'

def test_ket_rescale():
  x = ket('Fred', 3.72)
  y = x.rescale(3)
  assert str(y) == '3|Fred>'

def test_sp_rescale():
  x = ket('Fred', 3.72) + ket('Sam') + ket('Harry',0.3)
  y = x.rescale(1)
  assert str(y) == '|Fred> + 0.269|Sam> + 0.081|Harry>'

def test_ket_multiply():
  x = ket('Fred', 3.72)
  y = x.multiply(3)
  assert str(y) == '11.16|Fred>'

def test_sp_multiply():
  x = ket('Fred', 3.72) + ket('Sam') + ket('Harry',0.3)
  y = x.multiply(3)
  assert str(y) == '11.16|Fred> + 3|Sam> + 0.9|Harry>'

def test_ket_context_recall():
  context = context_list("test recall")
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  x = context.recall('friends', 'Fred')
  assert str(x) == '|Sam> + |Max> + |Harry>'

def test_ket_apply_op():
  context = context_list("test ket apply_op")
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  x = ket('Fred').apply_op(context, 'friends')
  assert str(x) == '|Sam> + |Max> + |Harry>'
  
def test_ket_apply_sigmoid_clean_neg():
  x = ket('x',-2).apply_sigmoid(clean)
  assert str(x) == '0|x>'

def test_ket_apply_sigmoid_clean_pos():
  y = ket('y',7.3).apply_sigmoid(clean)
  assert str(y) == '|y>'

def test_sp_apply_sigmoid_clean():
  x = ket('x',-2) + ket('y',7.3) + ket('z') + ket('fish',-10)
  y = x.apply_sigmoid(clean)
  assert str(y) == '0|x> + |y> + |z> + 0|fish>'

def test_sp_apply_sigmoid_clean_drop():
  x = ket('x',-2) + ket('y',7.3) + ket('z') + ket('fish',-10)
  y = x.apply_sigmoid(clean).drop()
  assert str(y) == '|y> + |z>'

def test_ket_label():
  x = ket('fred',3.7).label
  assert str(x) == 'fred'

def test_ket_value():
  x = ket('fred',3.7).value
  assert x == 3.7
 
def test_sp_label():
  x = ket('fred',3.7) + ket('sam', 22)
  y = x.label
  assert str(y) == 'fred'

def test_sp_value():
  x = ket('fred',3.7) + ket('sam', 22)
  y = x.value
  assert y == 3.7

def test_arithmetic_function():
  x = ket('number: 3')
  plus = ket('symbol: +')
  y = ket('number: 8')
  z = arithmetic(x, plus, y)
  assert str(z) == '|number: 11>'

def test_list2sp():
  x = [3.141, 7, 'fish', 'cat', 5.6, 'horse']
  y = list2sp(x)
  assert str(y) == '|number: 3.141> + |number: 7> + |fish> + |cat> + |number: 5.6> + |horse>'

def test_ket_add():
  x = ket('fred', 3.21)
  y = x.add('sam')
  assert str(y) == '3.21|fred> + |sam>'

def test_ket_add_sp():
  x = ket('fred', 3.21)
  y = ket('sam')
  z = x.add_sp(y)
  assert str(z) == '3.21|fred> + |sam>'

def test_ket_pick_elt():
  x = ket('fred', 3.17)
  y = x.pick_elt()
  assert str(y) == '3.17|fred>'

def test_sp_pick_elt():
  x = ket('fred', 3.17) + ket('x') + ket('y',12)
  y = x.pick_elt()
  assert str(y) == ''

def test_ket_weighted_pick_elt():
  x = ket('fred', 3.17)
  y = x.weighted_pick_elt()
  assert str(y) == '3.17|fred>'

def test_sp_weighted_pick_elt():
  x = ket('fred', 3.17) + ket('x') + ket('y',12)
  y = x.weighted_pick_elt()
  assert str(y) == ''

def test_sp_apply_op():
  context = context_list("test sp apply_op")
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
  x = ket('Fred') + ket('Sam')
  y = x.apply_op(context, 'friends')
  assert str(y) == '|Sam> + 2|Max> + 2|Harry> + |Simon>'

def test_sp_count_empty():
  x = superposition().count()
  assert x == 0

def test_sp_count_1():
  x = superposition('fred').count()
  assert x == 1

def test_sp_count():
  x = ket('Fred') + ket('Sam',3.2) + ket('Harry',2) + ket('Simon')
  y = x.count()
  assert y == 4

def test_sp_count_sum():
  x = ket('Fred') + ket('Sam',3.2) + ket('Harry',2) + ket('Simon')
  y = x.count_sum()
  assert y == 7.2

def test_sp_product():
  x = ket('Fred') + ket('Sam',3.2) + ket('Harry',2) + ket('Simon')
  y = x.product()
  assert y == 6.4

def test_sp_number_count():
  x = ket('Fred') + ket('Sam',3.2) + ket('Harry',2) + ket('Simon')
  y = x.number_count()
  assert str(y) == '|number: 4>'

def test_sp_number_count_sum():
  x = ket('Fred') + ket('Sam',3.2) + ket('Harry',2) + ket('Simon')
  y = x.number_count_sum()
  assert str(y) == '|number: 7.2>'

def test_sp_number_product():
  x = ket('Fred') + ket('Sam',3.2) + ket('Harry',2) + ket('Simon')
  y = x.number_product()
  assert str(y) == '|number: 6.4>'

def test_ket_split_ket():
  x = ket('a b c d e f g h').apply_fn(split_ket)
  assert str(x) == '|a> + |b> + |c> + |d> + |e> + |f> + |g> + |h>'

def test_sp_select_range():
  x = ket('a b c d e f g h').apply_fn(split_ket)
  y = x.select_range(3,5)
  assert str(y) == '|c> + |d> + |e>'

def test_ket_rank():   
  x = ket('a b c d e f g h')
  y = x.apply_fn(split_ket).apply_sp_fn(rank)
  assert str(y) == '|a> + 2|b> + 3|c> + 4|d> + 5|e> + 6|f> + 7|g> + 8|h>'

def test_sp_top_3():
  x = ket('a b c d e f g h').apply_fn(split_ket).apply_sp_fn(rank).top(3)
  assert str(x) == '6|f> + 7|g> + 8|h>'

def test_sp_top_3_all_same():
  x = ket('a b c d e f g h').apply_fn(split_ket).top(3)
  assert str(x) == '|a> + |b> + |c> + |d> + |e> + |f> + |g> + |h>'

def test_sp_delete_elt():
  x = ket('a b c d e f g h').apply_fn(split_ket).delete_elt(4)
  assert str(x) == '|a> + |b> + |c> + |e> + |f> + |g> + |h>'

def test_sp_delete_elt_v2():
  x = ket('a b c d e f g h').apply_fn(split_ket).delete_elt_v2(4)
  assert str(x) == '|a> + |b> + |c> + 0|d> + |e> + |f> + |g> + |h>'

def test_sp_delete_elt_v3():
  x = ket('a b c d e f g h').apply_fn(split_ket).delete_elt_v3(4)
  assert str(x) == '|a> + |b> + |c> + |e> + |f> + |g> + |h>'

def test_sp_find_index_empty():
  x = ket('a b c d e f g h').apply_fn(split_ket).find_index('fred')
  assert x == 0

def test_sp_find_index():
  x = ket('a b c d e f g h').apply_fn(split_ket).find_index('e')
  assert x == 5

def test_sp_find_value_empty():
  x = ket('a b c d e f g h').apply_fn(split_ket).find_value('fred')
  assert x == 0

def test_sp_find_value_1():
  x = ket('a b c d e f g h').apply_fn(split_ket).find_value('e')
  assert x == 1

def test_sp_find_value():
  x = ket('a b c d e f g h').apply_fn(split_ket).apply_sp_fn(rank).find_value('e')
  assert x == 5

def test_sp_delete_ket():
  x = ket('a b c d e f g h').apply_fn(split_ket).delete_ket('b')
  assert str(x) == '|a> + |c> + |d> + |e> + |f> + |g> + |h>'

def test_sp_softmax():
  x = ket('Fred') + ket('Sam',3.2) + ket('Harry',2) + ket('Simon')
  y = x.softmax()
  assert str(y) == '0.073|Fred> + 0.657|Sam> + 0.198|Harry> + 0.073|Simon>'

def test_sp_absolute_noise():
  x = ket('a b c d e f g h').apply_fn(split_ket).absolute_noise(5)
  assert str(x) == ''

def test_sp_relative_noise():
  x = ket('a b c d e f g h').apply_fn(split_ket).relative_noise(5)
  assert str(x) == ''
  
def test_sp_reverse():
  x = ket('a b c d e f g h').apply_fn(split_ket).reverse()
  assert str(x) == '|h> + |g> + |f> + |e> + |d> + |c> + |b> + |a>'

def test_sp_shuffle():
  x = ket('a b c d e f g h').apply_fn(split_ket).shuffle()
  assert str(x) == ''

def test_sp_coeff_sort():
  x = ket('a b c d e f g h').apply_fn(split_ket).apply_sp_fn(rank).shuffle().coeff_sort()
  assert str(x) == '8|h> + 7|g> + 6|f> + 5|e> + 4|d> + 3|c> + 2|b> + |a>'

def test_sp_ket_sort():
  x = ket('a b c d e f g h').apply_fn(split_ket).apply_sp_fn(rank).shuffle().ket_sort()
  assert str(x) == '|a> + 2|b> + 3|c> + 4|d> + 5|e> + 6|f> + 7|g> + 8|h>'

def test_sp_find_max():
  x = ket('a',3) + ket('b',2) + ket('c', 11) + ket('d')
  y = x.find_max()
  assert str(y) == '11|c>'

def test_sp_find_min():
  x = ket('a',3) + ket('b',2) + ket('c', 11) + ket('d') + ket('e') + ket('f',9)
  y = x.find_min()
  assert str(y) == '|d> + |e>'


def test_parse_rule_line():
  context = new_context('test parse rule line')
  s = 'friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick>'
  parse_rule_line(context, s)
  context.print_multiverse()
  assert True

def test_context_load():
  context.load("sw-examples/fred-sam-friends.sw")
  context.print_multiverse()
  assert True

def test_new_context():
  context = new_context('testing')
  context.print_universe()
  assert True

def test_new_context_learn():
  context = new_context('testing')
  context.learn('', 'b', 'empty')
  context.learn('a', 'b', ket('fish') + ket('soup'))
  context.learn('x', 'y', 'z')
  context.print_universe(True)
  assert True

def test_new_context_add_learn():
  context = new_context('testing add learn')
  context.add_learn('a', 'b', 'x')
  context.add_learn('a', 'b', ket('x',3.21) + ket('z'))
  context.add_learn('a', 'b', 'y')
  context.add_learn('a', 'b', 'z')
  context.print_universe(True)
  assert True

def test_new_context_learn_stored_rule():
  context = new_context('testing stored rule')
  context.learn('x', 'y', stored_rule('|fish> + 2.3|soup>'))
  context.print_universe(True)
  assert True

def test_new_context_add_learn_stored_rule():
  context = new_context('testing stored rule')
  context.add_learn('x', 'y', stored_rule('|fish> + 2.3|soup>'))
  context.print_universe(True)
  assert False

def test_new_context_learn_adding_stored_rules():
  context = new_context('testing stored rule')
  context.learn('x', 'y', stored_rule('|fish> + 2.3|soup>'))
  context.add_learn('x', 'y', stored_rule('2|cats> + |dog>'))
  context.add_learn('x', 'y', ket('onions',3))
  context.print_universe(True)
  assert True

def test_ket_is_not_empty__empty():
  x = ket('', 3)
  y = x.is_not_empty()
  assert str(y) == '|no>'

def test_ket_is_not_empty__not_empty():
  x = ket('fred')
  y = x.is_not_empty()
  assert str(y) == '|yes>'

def test_sp_is_not_empty__empty():
  x = ket('', 3) + ket() + ket('',7.2)
  y = x.is_not_empty()
  assert str(y) == '|no>'

def test_sp_is_not_empty__not_empty():
  x = ket() + ket('',2) + ket('fred')
  y = x.is_not_empty()
  assert str(y) == '|yes>'



# test the new_context class:

def test_new_context_set():
  context = new_context('starting context')
  context.set('next context')
  context.print_universe()
  assert True

def test_new_context_learn():
  context = new_context('starting context')
  context.learn('op', 'object', ket('a') + ket('b',2) + ket('c', -3))
  context.learn('op2', 'object', 'foo')
  context.print_universe(True)
  assert True

def test_new_context_add_learn():
  context = new_context('starting context')
  context.add_learn('op', 'object', ket('a') + ket('b',2) + ket('c', -3))
  context.add_learn('op2', 'object', 'foo')
  context.add_learn('op', 'object', 'b')
  context.add_learn('op2', 'object', ket('fish') + ket('soup'))
  context.print_universe(True)
  assert True

def test_new_context_recall():
  context = new_context('starting context')
  context.learn('op', 'object', ket('a') + ket('b',2) + ket('c', -3))
  x = context.recall('op', 'object')
  assert str(x) == '|a> + 2|b> + -3|c>'

def test_new_context_stored_rule_recall():
  context = new_context('starting context')
  context.learn('op', 'object', stored_rule('|a> + 2|b> - 3 |c>'))
  x = context.recall('op', 'object')
  assert str(x) == '|a> + 2|b> - 3 |c>'

def test_new_context_stored_rule_recall():
  context = new_context('starting context')
  context.learn('op', 'object', stored_rule('|a> + 2|b> - 3 |c>'))
  x = context.recall('op', 'object', active=True)
  assert str(x) == '|a> + 2|b>'      # ignore the -3|c> for now.

def test_new_context_stored_rule_apply_op():
  context = new_context('starting context')
  context.learn('op', 'object', stored_rule('|a> + 2|b> - 3 |c>'))
  x = ket('object').apply_op(context, 'op')
  assert str(x) == '|a> + 2|b>'

def test_new_context_dump_rule():
  context = new_context('starting context')
  context.learn('op', 'object', ket('a') + ket('b',2) + ket('c', -3))
  s = context.dump_rule('op', 'object')
  assert s == 'op |object> => |a> + 2|b> + -3|c>'

def test_new_context_stored_rule_dump_rule():
  context = new_context('starting context')
  context.learn('op', 'object', stored_rule('|a> + 2|b> - 3 |c>'))
  s = context.dump_rule('op', 'object')
  assert s == 'op |object> #=> |a> + 2|b> - 3 |c>'

def test_new_context_create_inverse():
  context = new_context('the context')
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
  context.create_universe_inverse()
  context.print_universe()
  assert True

def test_new_context_relevant_kets():
  context = new_context('the context')
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
  x = context.relevant_kets('friends')
  assert str(x) == '|Fred> + |Sam>'

def test_new_context_relevant_kets():
  context = new_context('the context')
  context.learn('op1', 'x', 'y')
  context.learn('op2', 'a', 'b')
  context.learn('friends', 'Fred', ket('Sam') + ket('Max') + ket('Harry'))
  context.learn('friends', 'Sam', ket('Harry') + ket('Max') + ket('Simon'))
  x = context.supported_operators()
  assert str(x) == '|op: op1> + |op: op2> + |op: friends>'


# test sequence class:
def test_sequence_ket_add():
  x = ket('x')
  y = ket('y')
  z = x.seq_add(y)
  assert str(z) == '|x> . |y>'

def test_sequence_sp_add():
  x = ket('x') + ket('z')
  y = ket('y') + ket('fish')
  z = x.seq_add(y)
  assert str(z) == '|x> + |z> . |y> + |fish>'

def test_sequence_ket_addition():
  x = ket('x')
  y = sequence() + x + x + x
  assert str(y) == '|x> . |x> . |x>'

def test_sequence_sp_addition():
  x = ket('x') + ket('y',2.7) + ket('z',93)
  y = sequence() + x + x + x
  assert str(y) == '|x> + 2.7|y> + 93|z> . |x> + 2.7|y> + 93|z> . |x> + 2.7|y> + 93|z>'


# needs more test cases!
def test_superposition_merge():
  x = ket('a') + ket('b',2.1) + ket('c',3)
  y = ket('d',7.9) + ket('e') + ket('f')
  z = x.merge(y)
  assert str(z) == '|a> + 2.1|b> + |cd> + |e> + |f>'

