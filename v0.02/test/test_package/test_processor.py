#!/usr/bin/env python3

#######################################################################
# let's test our new processor
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-2-9
# Update: 2018-2-10
# Copyright: GPLv3
#
# Usage: py.test -v test_processor.py
#
#######################################################################


import sys
from parsley import makeGrammar

from semantic_db import *
#import semantic_db as sdb


context = ContextList('in test the processor')

logger.setLevel(logging.DEBUG)


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
  assert True
