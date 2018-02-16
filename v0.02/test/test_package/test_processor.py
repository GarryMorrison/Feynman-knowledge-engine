#!/usr/bin/env python3

#######################################################################
# let's test our new processor
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-2-9
# Update: 2018-2-16
# Copyright: GPLv3
#
# Usage: py.test -v test_processor.py
#
#######################################################################


import sys
from pprint import pprint
from semantic_db import *

#pprint(globals())
#pprint(locals())

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

