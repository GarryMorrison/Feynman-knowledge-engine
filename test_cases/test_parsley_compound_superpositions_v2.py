#!/usr/bin/env python3

#######################################################################
# Just testing changes to my parser. 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-8-11
# Update:
# Copyright: GPLv3
#
# Usage: py.test -v test_parsley_compound_superpositions_v2.py
#
#######################################################################


import sys
from parsley import makeGrammar

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("parse compound superposition")

# operator parse:
our_operator_grammar = """
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
S0 = ' '*
S1 = ' '+

digit = :x ?(x in '0123456789') -> x
positive_int = <digit+>:n -> int(n)

# what about handle more than one dot char??
# fix eventually, but not super important for now
# what about minus sign?
#simple_float = ('-' | -> ''):sign <(digit | '.')+>:n -> float_int(sign + n)
# handle 9.3/5.2
simple_float = ('-' | -> ''):sign <(digit | '.')+>:numerator ('/' <(digit | '.')+> | -> '1'):denominator -> float_int(sign + numerator,denominator)


op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
# allow dot as an op char??
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.') -> x
#simple_op = op_start_char:first <op_char*>:rest -> first + rest
valid_op_string = op_start_char:first <op_char*>:rest -> first + rest
# breaks "common[op]" since we also have: "common(sp1,sp2)":
#simple_op = valid_op_string:s ?(not parameter_function(s)) -> s
# for now:
simple_op = valid_op_string:s -> s
parameter_function_name = valid_op_string:s ?(parameter_function(s)) -> s
parameters = (simple_float | simple_op | '\"\"' | '*'):p -> str(p)

# more elegant, process at the end version:
compound_op = simple_op:the_op '[' parameters:first (',' parameters)*:rest ']' -> [the_op] + [first] + rest
#general_op = (compound_op | simple_op | simple_float | '\"\"' | '-'):the_op -> the_op
general_op = (compound_op | simple_op | simple_float | '\"\"' ):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op,power)

# process as you go version:
# I eventually decided this version was too ugly! 
#compound_op = simple_op:the_op '[' parameters:first (',' parameters)*:rest ']' -> process_compound_op(the_op,[first] + rest)
#general_op = (compound_op | simple_op | simple_float | '\"\"' | '-'):the_op -> process_single_op(the_op)
#powered_op = general_op:the_op '^' positive_int:power -> process_power_op(the_op,power)

op = (powered_op | general_op):the_op -> the_op
op_sequence = (S0 op:first (S1 op)*:rest S0 -> [first] + rest)
              | S0 -> []

add_sequence = S0 '+' S0 op_sequence:k -> ('+',k)
sub_sequence = S0 '-' S0 op_sequence:k -> ('-',k)
sequence_ops = (add_sequence | sub_sequence)
bracket_ops = S0 '(' op_sequence:first S0 (sequence_ops+:rest S0 ')' S0 -> [('+',first)] + rest
                                          | ')' S0 -> [('+',first)] )
# normalize op_sequence so it has same "shape" as bracket_ops:
normed_op_sequence = op_sequence:ops -> [('+', ops)]                                           

valid_ket_chars = anything:x ?(x not in '<|>') -> x
naked_ket = '|' <valid_ket_chars*>:x '>' -> x
coeff_ket = (number | -> 1):value S0 naked_ket:label -> ket(label,value)

add_ket = S0 '+' S0 coeff_ket:k -> ('+', k)
sub_ket = S0 '-' S0 coeff_ket:k -> ('-', k)
merge_ket = S0 '_' S0 coeff_ket:k -> ('_', k)
#sequence_ket = S0 '.' S0 coeff_ket:k -> ('.', k)

#ket_ops = (add_ket | sub_ket | merge_ket | sequence_ket)
ket_ops = (add_ket | sub_ket | merge_ket )
#literal_superposition = S0 coeff_ket:left S0 (ket_ops+:right S0 -> ket_calculate(left,right)
#                                          | -> left)
# simplified literal_superposition:
literal_superposition = S0 coeff_ket:left S0 ket_ops*:right S0 -> ket_calculate(left,right)                                          

bracket_literal_superposition = S0 '(' literal_superposition:sp ')' S0 -> sp
bracket1_literal_superposition = S0 '(' literal_superposition:sp1 ')' S0 -> [str(sp1)]
bracket2_literal_superposition = S0 '(' literal_superposition:sp1 ',' literal_superposition:sp2 ')' S0 -> [sp1,sp2]
bracket3_literal_superposition = S0 '(' literal_superposition:sp1 ',' literal_superposition:sp2 ',' literal_superposition:sp3 ')' S0 -> [sp1,sp2,sp3]
bracket4_literal_superposition =  S0 '(' literal_superposition:sp1 ',' literal_superposition:sp2 ',' literal_superposition:sp3 ',' literal_superposition:sp4 ')' S0 -> [sp1,sp2,sp3,sp4]

#param1_fn = op_sequence:head bracket1_literal_superposition:tail -> [head,tail]
#param2_fn = op_sequence:head bracket2_literal_superposition:tail -> [head,tail]
#param3_fn = op_sequence:head bracket3_literal_superposition:tail -> [head,tail]
#param4_fn = op_sequence:head bracket4_literal_superposition:tail -> [head,tail]

#bracket_literal_superposition_sum = S0 '(' literal_superposition:sp1 ')' S0 '+' S0 '(' literal_superposition:sp2 ')' S0 -> sp1 + sp2
#bracket_literal_superposition_sum = bracket_literal_superposition:sp1 '+' bracket_literal_superposition:sp2 -> sp1 + sp2

add_bracket_sp = S0 '+' S0 bracket_literal_superposition:sp -> ('+', sp)
sub_bracket_sp = S0 '-' S0 bracket_literal_superposition:sp -> ('-', sp)
bracket_sp_ops = (add_bracket_sp | sub_bracket_sp )
#bracket_superposition_sum = S0 bracket_literal_superposition:left S0 (bracket_sp_ops+:right S0 -> sp_calculate(left,right)
#                                                                  | -> left )
bracket_superposition_sum = S0 bracket_literal_superposition:left S0 bracket_sp_ops*:right S0 -> sp_calculate(left,right)

ket_like_sp = S0 ( coeff_ket:sp | '(' literal_superposition:sp ')' ) S0 -> sp
op_sequence_sp = op_sequence:op_seq ket_like_sp:sp -> process_op_sequence_sp(op_seq,sp)
bracket_ops_sp = bracket_ops:bracket_op ket_like_sp:sp -> process_bracket_ops_sp(bracket_op,sp)

op_sequence_fn2 = op_sequence:op_seq bracket2_literal_superposition:sp_list -> process_op_sequence_fn2(op_seq,sp_list)
op_sequence_fn3 = op_sequence:op_seq bracket3_literal_superposition:sp_list -> process_op_sequence_fn3(op_seq,sp_list)
op_sequence_fn4 = op_sequence:op_seq bracket4_literal_superposition:sp_list -> process_op_sequence_fn4(op_seq,sp_list)

bracket_ops_fn1 = bracket_ops:bracket_op simple_op:fn1 bracket1_superposition:sp_list -> process_bracket_ops_fn1(bracket_op,fn1,sp_list) 
bracket_ops_fn2 = bracket_ops:bracket_op simple_op:fn2 bracket2_literal_superposition:sp_list -> process_bracket_ops_fn2(bracket_op,fn2,sp_list)
bracket_ops_fn3 = bracket_ops:bracket_op simple_op:fn3 bracket3_literal_superposition:sp_list -> process_bracket_ops_fn3(bracket_op,fn3,sp_list)
bracket_ops_fn4 = bracket_ops:bracket_op simple_op:fn4 bracket4_literal_superposition:sp_list -> process_bracket_ops_fn4(bracket_op,fn4,sp_list)

processed_op_sequence = op_sequence:op_seq -> process_op_sequence(op_seq)

bracket1_superposition = S0 '(' literal_superposition:sp1 ')' S0 -> [sp1]
bracket2_superposition = S0 '(' literal_superposition:sp1 ',' literal_superposition:sp2 ')' S0 -> [sp1,sp2]
bracket3_superposition = S0 '(' literal_superposition:sp1 ',' literal_superposition:sp2 ',' literal_superposition:sp3 ')' S0 -> [sp1,sp2,sp3]
bracket4_superposition =  S0 '(' literal_superposition:sp1 ',' literal_superposition:sp2 ',' literal_superposition:sp3 ',' literal_superposition:sp4 ')' S0 -> [sp1,sp2,sp3,sp4]

param1_fn = S0 parameter_function_name:name bracket1_superposition:sp -> process_param1_fn(name,sp) 
param2_fn = S0 parameter_function_name:name bracket2_superposition:sp -> process_param2_fn(name,sp) 
param3_fn = S0 parameter_function_name:name bracket3_superposition:sp -> process_param3_fn(name,sp) 
param4_fn = S0 parameter_function_name:name bracket4_superposition:sp -> process_param4_fn(name,sp) 

op_like = (bracket_ops | normed_op_sequence )

objects = S0 ( literal_superposition:sp -> sp
             | '(' literal_superposition:sp ')' S0 -> sp
             | op_sequence:op_seq ket_like_sp:sp -> process_op_sequence_sp(op_seq,sp)
             | bracket_ops:bracket_op ket_like_sp:sp -> process_bracket_ops_sp(bracket_op,sp)
             | op_sequence:op_seq bracket2_superposition:sp_list -> process_op_sequence_fn2(op_seq,sp_list)
             | op_sequence:op_seq bracket3_superposition:sp_list -> process_op_sequence_fn3(op_seq,sp_list)
             | op_sequence:op_seq bracket4_superposition:sp_list -> process_op_sequence_fn4(op_seq,sp_list)
             | bracket_ops:bracket_op simple_op:fn1 bracket1_superposition:sp_list -> process_bracket_ops_fn1(bracket_op,fn1,sp_list)                                                                                                                                     
             | bracket_ops:bracket_op simple_op:fn2 bracket2_superposition:sp_list -> process_bracket_ops_fn2(bracket_op,fn2,sp_list)
             | bracket_ops:bracket_op simple_op:fn3 bracket3_superposition:sp_list -> process_bracket_ops_fn3(bracket_op,fn3,sp_list)
             | bracket_ops:bracket_op simple_op:fn4 bracket4_superposition:sp_list -> process_bracket_ops_fn4(bracket_op,fn4,sp_list) )
    


#value = ws (string | number | object | array
#           | 'true'  -> True
#           | 'false' -> False
#           | 'null'  -> None) 
"""

# what happens if we have eg: "3.73.222751" (ie, more than one dot?)
def float_int(n,d):
  x = float(n)/float(d)
  if x.is_integer():
    return int(x)                                      
  return x              

# not sure this is the best way to handle this.
# the idea is to help distinguish between "op-sequence (ECS)" and "op-sequence foo-1 (ECS)"
# Bah! Breaks "common[friends]" since we also have: "common(sp1,sp2)"
def parameter_function(s):       # returns True if s is the name of a function in 1-param-fn, 2-param-fn, 3-param-fn or 4-param-fn tables. 
  #return False                   # for now just hardwire no.
  if s in whitelist_table_1 or s in whitelist_table_2 or s in whitelist_table_3 or s in  whitelist_table_4:
    return True
  return False

def ket_calculate(start,pairs,self_ket_label=None):
  result = start
  for op, value in pairs:
    if self_ket_label != None and value.label == "_self":
      value = ket(self_ket_label)
    if op == '+':
      result += value
    elif op == '-':
      result += value.multiply(-1)
    elif op == '_':                                 # maybe handle the merge-labels bit in a cleaner way??
      head,tail = result.index_split(-1)            # how handle coeffs of merged pieces?
      result = head + ket(tail.the_label() + value.label)  # currently set to 1
  return result

def sp_calculate(start,pairs):                      # I don't think we want merge_labels of superpositions? 
  result = start
  for op, value in pairs:
    if op == '+':
      result += value
    elif op == '-':
      result += value.multiply(-1)
  return result

def process_op_sequence_sp(op_seq,sp):              # needs to handle the 1-param function case too: "op-sequence foo-1 (ECS)"
#  print("op_seq:",str(op_seq))
#  print("sp:",str(sp))
  return [op_seq,str(sp)]

def process_bracket_ops_sp(bracket_op,sp):
#  print("bracket_op:",str(bracket_op))
#  print("sp:",str(sp))
  return [bracket_op,str(sp)]

def process_op_sequence_fn2(op_seq,sp_list):             # need to test for S0 operator sequence
  return [[('+',op_seq[:-1])], op_seq[-1],[str(sp_list[0]),str(sp_list[1])]]
  
def process_op_sequence_fn3(op_seq,sp_list):
  return [[('+', op_seq[:-1])], op_seq[-1],[str(sp_list[0]),str(sp_list[1]),str(sp_list[2])]]

def process_op_sequence_fn4(op_seq,sp_list):
  return [[('+', op_seq[:-1])], op_seq[-1],[str(sp_list[0]),str(sp_list[1]),str(sp_list[2]),str(sp_list[3])]]


def process_bracket_ops_fn1(bracket_op,fn1,sp_list):
  return [bracket_op,fn1,[str(sp_list[0])]]

def process_bracket_ops_fn2(bracket_op,fn2,sp_list):
  return [bracket_op,fn2,[str(sp_list[0]),str(sp_list[1])]]
  
def process_bracket_ops_fn3(bracket_op,fn3,sp_list):
  return [bracket_op,fn3,[str(sp_list[0]),str(sp_list[1]),str(sp_list[2])]]

def process_bracket_ops_fn4(bracket_op,fn4,sp_list):
  return [bracket_op,fn4,[str(sp_list[0]),str(sp_list[1]),str(sp_list[2]),str(sp_list[3])]]


def process_op_sequence(op_seq):
#  processed_operators = [ process_single_op(op) for op in op_seq ]
#  return "".join(reversed(processed_operators))
  return "".join(process_single_op(op) for op in reversed(op_seq))

def process_param1_fn(fn_name,sp):
  if fn_name in whitelist_table_1:
    return "%s(%s)" % (whitelist_table_1[fn_name],sp[0])
  return None 

def process_param2_fn(fn_name,sp):
  if fn_name in whitelist_table_2:
    return "%s(%s, %s)" % (whitelist_table_2[fn_name],sp[0],sp[1])
  return None 

def process_param3_fn(fn_name,sp):
  if fn_name in whitelist_table_3:
    return "%s(%s, %s, %s)" % (whitelist_table_3[fn_name],sp[0],sp[1],sp[2])
  return None 

def process_param4_fn(fn_name,sp):
  if fn_name in whitelist_table_4:
    return "%s(%s, %s, %s, %s)" % (whitelist_table_4[fn_name],sp[0],sp[1],sp[2],sp[3])
  return None 


parse_dictionary = {
  "float_int"               : float_int,
  "parameter_function"      : parameter_function, 
  "ket"                     : ket,
  "ket_calculate"           : ket_calculate,
  "sp_calculate"            : sp_calculate,
  "process_op_sequence_sp"  : process_op_sequence_sp,
  "process_bracket_ops_sp"  : process_bracket_ops_sp,
  "process_op_sequence_fn2" : process_op_sequence_fn2,
  "process_op_sequence_fn3" : process_op_sequence_fn3,
  "process_op_sequence_fn4" : process_op_sequence_fn4,
  "process_bracket_ops_fn2" : process_bracket_ops_fn2,
  "process_bracket_ops_fn3" : process_bracket_ops_fn3,
  "process_bracket_ops_fn4" : process_bracket_ops_fn4,
  "process_op_sequence"     : process_op_sequence,
  
  "process_param1_fn"       : process_param1_fn,  
  "process_param2_fn"       : process_param2_fn,  
  "process_param3_fn"       : process_param3_fn,  
  "process_param4_fn"       : process_param4_fn,  

}
  
op_grammar = makeGrammar(our_operator_grammar,parse_dictionary)


# ('some-frog', 37)
def test_op_powered_op():
  x = op_grammar("some-frog^37").powered_op()
  assert str(x) == "('some-frog', 37)"

# ['foo', '""']
def test_op_compound_op_quotes():
  x = op_grammar("foo[\"\"]").compound_op()
  assert str(x) == '[\'foo\', \'""\']'

# ['foo', 'bah']
def test_op_compound_op_string():
  x = op_grammar("foo[bah]").compound_op()
  assert str(x) == "['foo', 'bah']"

# ['foo', '373', 'bah']
def test_op_compound_op_int_string():
  x = op_grammar("foo[373,bah]").compound_op()
  assert str(x) == "['foo', '373', 'bah']"


# 'foo'
def test_op_general_op():
  x = op_grammar("foo").general_op()
  assert str(x) == 'foo'

# ['foo', '3.1416']
def test_op_general_op_float():
  x = op_grammar("foo[3.1416]").general_op()
  assert str(x) == "['foo', '3.1416']"


# (['foo', '37', 'fish'], 13)
def test_op_powered_op_compound():
  x = op_grammar("foo[37,fish]^13").powered_op()
  assert str(x) == "(['foo', '37', 'fish'], 13)"


# (['foo', 'bah', '13.2'], 7)
def test_op_op():
  x = op_grammar("foo[bah,13.2]^7").op()
  assert str(x) == "(['foo', 'bah', '13.2'], 7)"

# ('foo', 2)
def test_op_op_foo_square():
  x = op_grammar("foo^2").op()
  assert str(x) == "('foo', 2)"


# []
def test_op_op_sequence_empty():
  x = op_grammar("").op_sequence()
  assert str(x) == "[]"

# []
def test_op_op_sequence_space():
  x = op_grammar("  ").op_sequence()
  assert str(x) == "[]"

# ['foo', 'bah', ['fish', 'x', 'y', '13.2'], (['select', '1', '3'], 2)]
def test_op_op_sequence_one():
  x = op_grammar("  foo bah fish[x,y,13.2] select[1,3]^2   ").op_sequence()
  assert str(x) == "['foo', 'bah', ['fish', 'x', 'y', '13.2'], (['select', '1', '3'], 2)]"

# [33.2, '""', ['fish', 'foo'], (3.14, 3), 'some-op', -13.572]
def test_op_op_sequence_two():
  x = op_grammar(" 33.2  \"\" fish[foo] 3.14^3 some-op -13.572 ").op_sequence()
  assert str(x) == "[33.2, '\"\"', ['fish', 'foo'], (3.14, 3), 'some-op', -13.572]"



# hrmm... need tests with extra spaces in various positions.
# [('+', ['op'])]
def test_op_bracket_ops_one_op():
  x = op_grammar("(op)").bracket_ops()
  assert str(x) == "[('+', ['op'])]"

# [('+', ['op3', ('op', 3), ['bah', 'fish'], 37])]
def test_op_bracket_ops_one_op_sequence():
  x = op_grammar("(op3 op^3 bah[fish] 37)").bracket_ops()
  assert str(x) == "[('+', ['op3', ('op', 3), ['bah', 'fish'], 37])]"

# [('+', ['op3', ('op', 3), ['bah', 'fish'], 37])]
def test_op_normed_op_sequence():
  x1 = op_grammar(" op3 op^3 bah[fish] 37").normed_op_sequence()
  assert str(x1) == "[('+', ['op3', ('op', 3), ['bah', 'fish'], 37])]"
  
def test_op_normed_op_sequence__bracket_ops():
  x1 = op_grammar(" op3 op^3 bah[fish] 37").normed_op_sequence()
  x2 = op_grammar(" (op3 op^3 bah[fish] 37)  ").bracket_ops()
  assert str(x1) == str(x2)
  

# [('+', ['op']), ('+', ['op2'])]
def test_op_bracket_ops_two_op():
  x = op_grammar(" (op + op2)").bracket_ops()
  assert str(x) == "[('+', ['op']), ('+', ['op2'])]"

# [('+', ['op']), ('+', ['op2']), ('-', ['op3']), ('+', ['op4']), ('-', ['op5'])]
def test_op_bracket_ops_five_negative():
  x = op_grammar(" (op + op2 - op3 + op4 - op5)").bracket_ops()
  assert str(x) == "[('+', ['op']), ('+', ['op2']), ('-', ['op3']), ('+', ['op4']), ('-', ['op5'])]"

# [('+', ['op']), ('+', ['op2', 'op3', 'op4']), ('-', [('op5', 2), ['op4', 'fish'], 'op6']), ('-', ['op5'])]
def test_op_bracket_ops_big_negative_sequences():
  x = op_grammar("  (  op + op2 op3 op4 - op5^2 op4[fish] op6 - op5 )  ").bracket_ops()
  assert str(x) == "[('+', ['op']), ('+', ['op2', 'op3', 'op4']), ('-', [('op5', 2), ['op4', 'fish'], 'op6']), ('-', ['op5'])]"

# [('+', ['op1', 'op2']), ('+', ['op3', 'op4', -3, 'op5']), ('+', ['op6', 'op7'])] 
def test_op_bracket_ops_negative_element():
  x = op_grammar("  ( op1 op2 + op3 op4 -3 op5 + op6 op7 )").bracket_ops()
  assert str(x) == "[('+', ['op1', 'op2']), ('+', ['op3', 'op4', -3, 'op5']), ('+', ['op6', 'op7'])]"


# 3.2|a> + |b> + 3.142|pi> + -1|d> + |z> + -3|omega>
def test_op_literal_superposition():
  x = op_grammar(" 3.2|a> + |b> + 3.1415|pi> -|d> + |z> -3 |omega> ").literal_superposition()
  assert str(x) == "3.2|a> + |b> + 3.142|pi> + -1|d> + |z> + -3|omega>"

# 3.2|a> + |b> + 3.142|pi> + -1|d> + |z> + -3|omega> 
def test_op_literal_superposition_verify_idempotent():
  x = op_grammar("3.2|a> + |b> + 3.142|pi> + -1|d> + |z> + -3|omega>").literal_superposition()
  assert str(x) == "3.2|a> + |b> + 3.142|pi> + -1|d> + |z> + -3|omega>"

# |xyz>
def test_op_literal_superposition_merge_labels():
  x = op_grammar(" 3|x> _ 5|y> _ |z> ").literal_superposition()
  assert str(x) == "|xyz>"

# |a> + 0.7|b> + |xyz> + 9|fish>
def test_op_literal_superposition_merge_labels_plus_sps():
  x = op_grammar(" |a> + 0.7|b> + 3|x> _ 5|y> _ |z> + 9|fish> ").literal_superposition()
  assert str(x) == "|a> + 0.7|b> + |xyz> + 9|fish>"


# 3.2|a> + |b> + 3.142|pi> + -1|d> + |z>
def test_op_bracket_literal_superposition():
  x = op_grammar(" ( 3.2|a> + |b> + 3.1415|pi> -|d> + |z>  ) ").bracket_literal_superposition()
  assert str(x) == "3.2|a> + |b> + 3.142|pi> + -1|d> + |z>"

# ['3.2|a> + |b> + 3.142|pi> + -1|d> + |z>']
# NB: the current rule applies str() to the sp.
def test_op_bracket1_literal_superposition():
  x = op_grammar(" ( 3.2|a> + |b> + 3.1415|pi> -|d> + |z>  ) ").bracket1_literal_superposition()
  assert str(x) == "['3.2|a> + |b> + 3.142|pi> + -1|d> + |z>']"

# 3.2|a> + 8|b> + 0.5|c> + |d>
def test_op_literal_superposition_plus_literal_superposition():
  x = op_grammar(" (3|a> + 7 |b> + 0.5|c> ) + (|b> + 0.2|a> + |d>)  ").bracket_superposition_sum()
  assert str(x) == "3.2|a> + 8|b> + 0.5|c> + |d>"

# 3.2|a> + 8|b> + 0.5|c> + |d> + 6|x> + 1.7|y> + |fish>
def test_op_literal_superposition_plus_literal_superposition_plus_more():
  x = op_grammar(" (3|a> + 7 |b> + 0.5|c> ) + (|b> + 0.2|a> + |d>) + (|x> + 2|y>) - (0.3|y> - 5|x>) + (|fish>)").bracket_superposition_sum()
  assert str(x) == "3.2|a> + 8|b> + 0.5|c> + |d> + 6|x> + 1.7|y> + |fish>"


# 3.7|fish>
def test_op_ket_like_sp_single_ket():
  x = op_grammar(" 3.7|fish> ").ket_like_sp()
  assert str(x) == "3.7|fish>"

# 2|x> + |y>   
def test_op_ket_like_sp_literal_sp():
  x = op_grammar(" (2|x> + |y>) ").ket_like_sp()
  assert str(x) == "2|x> + |y>"

# [['op3', 'op2', 'op1', 3.7], '|fish>']
# NB: the 3.7 is considered an operator. Not sure if we want this. Don't know how to change if we don't.
def test_op_op_sequence_sp_single_ket():
  x = op_grammar(" op3 op2 op1 3.7|fish> ").op_sequence_sp()
  assert str(x) == "[['op3', 'op2', 'op1', 3.7], '|fish>']"

# [['op3', 'op2', 'op1'], '2|x> + |y>']   
def test_op_op_sequence_sp_literal_sp():
  x = op_grammar(" op3 op2 op1 (2|x> + |y>) ").op_sequence_sp()
  assert str(x) == "[['op3', 'op2', 'op1'], '2|x> + |y>']"


# [[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '3.7|fish>']  
def test_op_bracket_ops_sp_single_ket():
  x = op_grammar(" (1 + op - op^2 + op3^5) 3.7|fish> ").bracket_ops_sp()
  assert str(x) == "[[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '3.7|fish>']"

# for later!
#def test_op_bracket_ops_sp_kets():
#  x = op_grammar(" (1 + op - op^2 + op3^5) 3.7|fish> + 3|pie> + 0.5 |cats> ").bracket_ops_sp()
#  assert str(x) == ""

# [[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '2|x> + |y>']   
def test_op_bracket_ops_sp_literal_sp():
  x = op_grammar(" (1 + op - op^2 + op3^5) (2|x> + |y>) ").bracket_ops_sp()
  assert str(x) == "[[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '2|x> + |y>']"

## [['op3', 'op2', 'op1', 'fn-1'], ['2|x> + |y>', '|a> + |b> + 0.3|z>']]
# [[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]
def test_op_op_sequence_fn2_literal_sps():
  x = op_grammar(" op3 op2 op1 fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").op_sequence_fn2()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]"
  
## [['op3', 'op2', 'op1', 'fn-1'], ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]
# [[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]
def test_op_op_sequence_fn3_literal_sps():
  x = op_grammar(" op3 op2 op1 fn-3 (2|x> + |y>, |a> + |b> + 0.3|z>,|fish> ) ").op_sequence_fn3()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]"

## [['op3', 'op2', 'op1', 'fn-1'], ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]
# [[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]
def test_op_op_sequence_fn4_literal_sps():
  x = op_grammar(" op3 op2 op1 fn-4 (2|x> + |y>, |a> + |b> + 0.3|z>,|pi>,|e> + |log> ) ").op_sequence_fn4()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]"


# [[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]
def test_op_bracket_ops_fn2_literal_sps():
  x = op_grammar(" (op3 op2 op1) fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").bracket_ops_fn2()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]"

# [[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]
def test_op_bracket_ops_fn3_literal_sps():
  x = op_grammar(" ( op3 op2 op1) fn-3 (2|x> + |y>, |a> + |b> + 0.3|z>,|fish> ) ").bracket_ops_fn3()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]"

# [[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']] 
def test_op_bracket_ops_fn4_literal_sps():
  x = op_grammar(" (op3 op2 op1) fn-4 (2|x> + |y>, |a> + |b> + 0.3|z>,|pi>,|e> + |log> ) ").bracket_ops_fn4()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]"


# test bracket_ops_fn2 == op_sequence_fn2. This is to help make some things easier:
def test_op_bracket_ops_fn2__op_sequence_fn2_literal_sps():
  x1 = op_grammar(" op3 op2 op1 fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").op_sequence_fn2()
  x2 = op_grammar(" (op3 op2 op1) fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").bracket_ops_fn2()
  assert str(x1) == str(x2)



# .apply_fn(split_ket).apply_sp_fn(common,context,"friends").multiply(3).multiply(3)
def test_op_processed_op_sequence():
  x = op_grammar("3^2 common[friends] split").processed_op_sequence() 
  assert str(x) == '.apply_fn(split_ket).apply_sp_fn(common,context,"friends").multiply(3).multiply(3)'
  

# sp_len_1(|x> + 3.2|y> + -1|z>)
def test_op_param1_fn():
  x = op_grammar("sp (|x> + 3.2|y> -|z>)").param1_fn() 
  assert str(x) == "sp_len_1(|x> + 3.2|y> + -1|z>)"

# intersection(|x> + 3.2|y> + -1|z>, |y>)
def test_op_param2_fn():
  x = op_grammar("intn (|x> + 3.2|y> -|z>,|y>)").param2_fn() 
  assert str(x) == "intersection(|x> + 3.2|y> + -1|z>, |y>)"

# algebra(|a>, |+>, |b>)
def test_op_param3_fn():
  x = op_grammar("algebra (|a>,|+>,|b>)").param3_fn() 
  assert str(x) == "algebra(|a>, |+>, |b>)"

#def test_op_param4_fn():
#  x = op_grammar("intn (|x> + 3.2|y> -|z>,|y>)").param4_fn() 
#  assert str(x) == ""
  
#
#def test_op_param2_fn():
#  x = op_grammar("foo (3|x> + 7.3|y> + |z>,|a> + 0.2|b>)").param2_fn()
#  assert str(x) == ""


#
#def test_op_param2_fn_example_2():
#  x = op_grammar("op3^2 op2 op1 foo (3|x> + 7.3|y> + |z>,|a> + 0.2|b>)").param2_fn()
#  assert str(x) == ""


# [('+', ['op3', 'op2', 'op1'])]
def test_op_op_like_v1():
  x = op_grammar(" op3 op2 op1 ").op_like()
  assert str(x) == "[('+', ['op3', 'op2', 'op1'])]"
  
# [('+', ['op3', 'op2', 'op1'])]
def test_op_op_like_v2():
  x = op_grammar(" (op3 op2 op1) ").op_like()
  assert str(x) == "[('+', ['op3', 'op2', 'op1'])]"

# [('+', [])]
def test_op_op_like_empty():
  x = op_grammar(" ").op_like()
  assert str(x) == "[('+', [])]"


# test the objects rule section:
# 2|x> + |y> + 3.27|z>
def test_op_objects_literal_sp():
  x = op_grammar("2|x> + |y> +3.27|z>").objects()
  assert str(x) == "2|x> + |y> + 3.27|z>"
  
# 2|x> + |y> + 3.27|z>
def test_op_objects_literal_sp_bracket():
  x = op_grammar(" ( 2|x> + |y> +3.27|z>)").objects()
  assert str(x) == "2|x> + |y> + 3.27|z>"

# [['op3', 'op2', 'op1'], '2|x> + |y> + 3.27|z>'] 
def test_op_objects_ops_literal_sp_bracket():
  x = op_grammar(" op3 op2 op1( 2|x> + |y> +3.27|z>)").objects()
  assert str(x) == "[['op3', 'op2', 'op1'], '2|x> + |y> + 3.27|z>']"

# [[('+', ['op3', 'op2', 'op1'])], '2|x> + |y> + 3.27|z>']
def test_op_objects_bracket_ops_literal_sp_bracket():
  x = op_grammar(" (op3 op2 op1)( 2|x> + |y> +3.27|z>)").objects()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], '2|x> + |y> + 3.27|z>']"

# [[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['|a>', '|b>']]
def test_op_objects_ops_fn_2():
  x = op_grammar(" op3 op2 op1 fn-2(|a>,|b> )").objects()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['|a>', '|b>']]"
  
#
def test_op_objects_ops_fn_3():
  x = op_grammar(" op3 op2 op1 fn-3(|a>,|b> ,|c> )").objects()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['|a>', '|b>', '|c>']]"

#
def test_op_objects_ops_fn_4():
  x = op_grammar(" op3 op2 op1 fn-4(|a>,|b> ,|c>,|d> )").objects()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['|a>', '|b>', '|c>', '|d>']]"

def test_op_objects_bracket_ops_fn_2():
  x = op_grammar("( op3 op2 op1) fn-2(|a>,|b> )").objects()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['|a>', '|b>']]"
  
#
def test_op_objects_bracket_ops_fn_3():
  x = op_grammar(" (op3 op2 op1 )fn-3(|a>,|b> ,|c> )").objects()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['|a>', '|b>', '|c>']]"

#
def test_op_objects_bracket_ops_fn_4():
  x = op_grammar(" (op3 op2 op1) fn-4(|a>,|b> ,|c>,|d> )").objects()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['|a>', '|b>', '|c>', '|d>']]"

      