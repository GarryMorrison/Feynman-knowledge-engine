#!/usr/bin/env python3

#######################################################################
# Now I understand parsing a little better, still not great, but hey.
# let's try again for extract-compound-superposition.
# let's try to compile our parse tree's from yesterday
# I think I might have it! Though doesn't handle |x> _ |y> _ |z> yet ....    
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-8-19
# Update: 20/8/2016
# Copyright: GPLv3
#
# Usage: py.test -v test_parsley_compound_superpositions_v3.py
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

# operator parse:
our_full_grammar = """
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
#parameter_function_name = valid_op_string:s ?(parameter_function(s)) -> s
parameters = (simple_float | simple_op | '\"\"' | '*'):p -> str(p)

# more elegant, process at the end version:
compound_op = simple_op:the_op '[' parameters:first (',' parameters)*:rest ']' -> [the_op] + [first] + rest
#general_op = (compound_op | simple_op | simple_float | '\"\"' | '-'):the_op -> the_op
general_op = (compound_op | simple_op | simple_float | '\"\"' ):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op,power)
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
#coeff_ket = (number | -> 1):value S0 naked_ket:label -> ket_substitute(label,value,self_object)
coeff_ket = (number | -> 1):value S0 naked_ket:label -> (label,value)
#coeff_ket = (number | -> 1):value S0 naked_ket:label -> (label,value)

add_ket = S0 '+' S0 coeff_ket:k -> ('+', k)
sub_ket = S0 '-' S0 coeff_ket:k -> ('-', k)
merge_ket = S0 '_' S0 coeff_ket:k -> ('_', k)
ket_ops = (add_ket | sub_ket | merge_ket )
literal_superposition = S0 coeff_ket:left S0 ket_ops*:right S0 -> ket_calculate(left,right)                                          

compiled_op_sequence = op_sequence:op_seq -> compile_op_sequence(op_seq)
compiled_bracket_ops = bracket_ops:bracket_op -> compile_bracket_ops(bracket_op) 


rhs_ket_like = S0 coeff_ket:k S0 -> k
op_like = bracket_ops | normed_op_sequence
op_like_cs = S0 ( bracket_ops:ops | op_sequence:ops ) S0 compound_superposition:sp -> ('op_cs',ops,sp)
#op_like_cs = S0 ( bracket_ops:ops | op_sequence:ops ) S0 compound_superposition:sp -> [ops,sp[1]]
#op_like_cs = S0 ( bracket_ops:ops | normed_op_sequence:ops ) S0 compound_superposition:sp -> compile_bracket_ops_sp(ops,sp)

add_cs = S0 '+' S0 compound_superposition:k -> ('sp +',k)
#add_cs = S0 '+' S0 compound_superposition:k -> k
sub_cs = S0 '-' S0 compound_superposition:k -> ('sp -',k)
#add_cs = S0 '+' S0 coeff_ket:k -> ('+',k)
#sub_cs = S0 '-' S0 coeff_ket:k -> ('-',k)

cs_ops = (add_cs | sub_cs)
##compound_superposition = S0 rhs_ket_like:first S0 (cs_ops+:rest S0 -> [('+',first)] + rest
##                                                  | S0 -> [('+',first)] )
##compound_superposition = S0 ( rhs_ket_like:first | '(' compound_superposition:first ')' | op_like_cs:first ) S0 cs_ops*:rest S0 -> sp_calculate(first,rest)
#compound_superposition = S0 ( coeff_ket:first | '(' compound_superposition:first ')' | op_like_cs:first ) S0 cs_ops*:rest S0 -> sp_calculate(first,rest)
#compound_superposition  :rest = S0 ( bracket_ops | normed_op_sequence ):ops S0 ( coeff_ket:first | '(' compound_superposition:first ')' | op_like_cs:first | compound_superposition:first cs_ops*:rest ) S0 -> sp_calculate(ops,first,rest)
#compound_superposition = S0 ( bracket_ops | normed_op_sequence ):ops S0 ( coeff_ket:first | '(' compound_superposition:first ')' | op_like_cs:first )  S0 cs_ops*:rest S0 -> sp_calculate(ops,first,rest)
#compound_superposition = S0 ( bracket_ops | op_sequence ):ops S0 ( naked_ket:first | '(' compound_superposition:first ')' | op_like_cs:first )  S0 (cs_ops+:rest S0 -> [ops,(first)] + rest
#                                                                                                                                                     | S0 -> [ops,(first)] )
compound_superposition = S0 ( bracket_ops | op_sequence ):ops S0 ( naked_ket:first | bracketk_cs:first | op_like_cs:first )  S0 (cs_ops+:rest S0 -> [ops,first] + rest
                                                                                                                                                     | S0 -> [ops,first] )

compiled_compound_superposition = compound_superposition:sp -> compile_compound_superposition(sp)                                                                                                                                                     

bracketk_cs = S0 '(' compound_superposition:first ( S0 ',' S0 compound_superposition)*:rest ')' S0 -> [first] + rest

#op_like_cs = S0 ( bracket_ops:ops | normed_op_sequence:ops ) S0 compound_superposition:sp -> compile_bracket_ops_sp(ops,sp)

#op_cs = S0 normed_op_sequence:ops compound_superposition:sp -> (ops,sp)
#brackets_cs = bracket_ops:ops compound_superposition:sp -> (ops,sp) 
#add_cs = S0 '+' S0 compound_superposition:k -> ('+',k)
#sub_cs = S0 '-' S0 compound_superposition:k -> ('-',k)
#cs_ops = ( add_cs | sub_cs | op_cs | brackets_cs )
#compound_superposition = S0 ( coeff_ket:first | '(' compound_superposition:first ')' ) S0 (cs_ops+:rest S0 -> [('+',first)] + rest
#                                                                                       | S0 -> [('+',first)] )
#compound_superposition = S0 ( coeff_ket:first | '(' compound_superposition:first ')' ) S0 cs_ops*:rest S0 -> sp_calculate(first,rest)                                                                                                                                                           



bracket1_object = S0 '(' object:k ')' S0 -> k
# not sure why we need the :k 's in this expression:
ket_like_object = S0 ( coeff_ket:k | bracket1_object:k | op_sequence_object:k | bracket_ops_object:k ) S0 -> k 
op_sequence_object = op_sequence:op_seq ket_like_object:sp -> compile_op_sequence_sp(op_seq,sp)
bracket_ops_object = bracket_ops:bracket_op ket_like_object:sp -> compile_bracket_ops_sp(bracket_op,sp)

op_sequence_object_fnk = op_sequence:op_seq bracketk_object:sp_list -> compile_op_sequence_fnk(op_seq,sp_list)
# I'm not sure why we even need "bracket_ops_object_fnk" rule. Surely it is already handled by "bracket-ops op-sequence bracketk"
# Is it too late to test other methods?
bracket_ops_object_fnk = bracket_ops:bracket_op simple_op:fnk bracketk_object:sp_list -> compile_bracket_ops_fnk(bracket_op,fnk,sp_list)

bracketk_object = S0 '(' object:first ( S0 ',' S0 object)*:rest ')' S0 -> [first] + rest

object = S0 ( literal_superposition 
            | bracket1_object
#            | object_sum
            | op_sequence_object
            | bracket_ops_object 
            | bracket_ops_object_fnk 
#            | op_sequence_object_fnk )
            | op_sequence_object_fnk 
            | object_sum )


add_object = S0 '+' S0 object:k -> ('+',k)
sub_object = S0 '-' S0 object:k -> ('-',k)
object_ops = (add_object | sub_object)
#object_sum = S0 object:first S0 (object_ops+:rest S0 -> [('+',first)] + rest
#                                                | S0 -> [('+',first)] )
object_sum = S0 object:first S0 object_ops*:rest S0 -> sp_calculate(first,rest)
                                          
"""

# what happens if we have eg: "3.73.222751" (ie, more than one dot?)
def float_int(n,d):
  x = float(n)/float(d)
  if x.is_integer():
    return int(x)                                      
  return x              

def old_ket_substitute(label,value,self_object=None):
#  print("label:",label)
#  print("value:",value)
#  print("self_object:",str(self_object))
#  print("type self_object:",str(type(self_object)))
  if label == "_self" and self_object is not None:
    if type(self_object) == str:
      return ket(self_object,value)
    if type(self_object) == ket:                            # check for superposition later.
      return self_object.multiply(value)
  return ket(label,value)
  

# not sure this is the best way to handle this.
# the idea is to help distinguish between "op-sequence (ECS)" and "op-sequence foo-1 (ECS)"
# Bah! Breaks "common[friends]" since we also have: "common(sp1,sp2)"
def parameter_function(s):       # returns True if s is the name of a function in 1-param-fn, 2-param-fn, 3-param-fn or 4-param-fn tables. 
  #return False                   # for now just hardwire no.
  if s in whitelist_table_1 or s in whitelist_table_2 or s in whitelist_table_3 or s in  whitelist_table_4:
    return True
  return False

def ket_calculate(start,pairs):
  result = start
  for op, value in pairs:
    if op == '+':
      result += value
    elif op == '-':
      result += value.multiply(-1)
    elif op == '_':                                 # maybe handle the merge-labels bit in a cleaner way??
      head,tail = result.index_split(-1)            # how handle coeffs of merged pieces?
      result = head + ket(tail.the_label() + value.label)  # currently set to 1
  return result

def sp_calculate(ops,start,pairs):                      # I don't think we want merge_labels of superpositions?
  print("ops:",str(ops)) 
  print("start:",str(start))
  #print("pairs:",[str(x[1]) for x in pairs])
  print("pairs:",str(pairs))
  if ops != [('+', [])]:
    start = compile_bracket_ops_sp(ops,start)
    print("start2:",str(start))
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
#  return [op_seq,str(sp)]
  fn1 = op_seq[-1]                                      
  if fn1 in whitelist_table_1:
#    return [[('+',op_seq[:-1])], op_seq[-1],[str(sp)]]          # needs to have the same shape as process_bracket_ops_fn1
    return [[('+',op_seq[:-1])], whitelist_table_1[fn1], [str(sp)]]          # needs to have the same shape as process_bracket_ops_fn1
  return [[('+', op_seq)],str(sp)]                              # needs to have the same shape as process_bracket_ops_sp     

def process_bracket_ops_sp(bracket_op,sp):
#  print("bracket_op:",str(bracket_op))
#  print("sp:",str(sp))
  return [bracket_op,str(sp)]

# nice start on generalizing to the general case, rather than specific k in {1,2,3,4}.
# of course, still need appropriate whitelist_tables though.
# need to handle that later.
def process_op_sequence_fnk(op_seq,sp_list):             # need to test for fn-1 operator sequence
  return [[('+',op_seq[:-1])], op_seq[-1],[str(x) for x in sp_list]]

def process_bracket_ops_fnk(bracket_op,fnk,sp_list):
  return [bracket_op,fnk,[str(x) for x in sp_list]]


def compile_op_sequence(op_seq):
  return "".join(process_single_op(op) for op in reversed(op_seq))

# [('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])]
def compile_bracket_ops(bracket_op):
  result = []
  for op,value in bracket_op:
    processed_op = compile_op_sequence(value)
    if op == '+':
      result.append(processed_op)
    elif op == '-':
      result.append(processed_op + ".multiply(-1)")
  return result

# compile patterns of this shape:
# [('+', ('x', 3)), ('+', ('y', 1)), ('+', ('_self', 2.7)), ('-', ('d', 1))]
#
def compile_superposition(pairs,self_object):
  print("pairs:",str(pairs))

  result = superposition()
  for op, (label,value) in pairs:
    if label == "_self" and self_object.get() is not None:
      the_ket = self_object.get().multiply(value)
    else:
      the_ket = ket(label,value)

    if op == '+':
      result += the_ket
    elif op == '-':
      result += the_ket.multiply(-1)
    elif op == '_':                                 # maybe handle the merge-labels bit in a cleaner way??
      head,tail = result.index_split(-1)            # how handle coeffs of merged pieces?
      result = head + ket(tail.the_label() + the_ket.label)  # currently set to 1
  return result


#    return [[('+',op_seq[:-1])], whitelist_table_1[fn1], [str(sp)]]
def compile_op_sequence_sp(op_seq,sp):
  if len(op_seq) == 0:
    return sp
#  fn1 = op_seq[-1]                                      
#  if fn1 in whitelist_table_1:
#    python_code = "%s(sp)" % whitelist_table_1[fn1]
#    print("python code:", python_code)
#    first_eval = eval(python_code)
#    return compile_op_sequence_sp(op_seq[:-1],first_eval)                    # what happens if the last element of op_seq[:-1] is also in whitelist_table_1?
  python_code = "sp" + compile_op_sequence(op_seq)
  print("python code:", python_code)
  return eval(python_code)

def compile_bracket_ops_sp(bracket_op,sp):
  if bracket_op == [('+', [])]:
    return sp
  print("bracket_op:",str(bracket_op))
  print("sp:",str(sp))
  python_code = " + ".join("sp" + op for op in compile_bracket_ops(bracket_op))    # not sure this is the best way to handle this!
  print("python code:", python_code)
  return eval(python_code)

# Hrmm... I don't understand why this isn't parsed as: "bracket-ops op-sequence bracket2" 
# (op2 + op1) fn-2 (|x>, |y>)
def compile_bracket_ops_fnk(bracket_op,fnk,sp_list):      # is there a way to tidy this code?? I don't like the 4 if conditions. 
#  return [bracket_op,fnk,[str(x) for x in sp_list]]
  python_code = "ket('')"
  if len(sp_list) == 1:                                   # 1-parameter function:
    if fnk in whitelist_table_1:
      python_code = "%s(sp_list[0])" % whitelist_table_1[fnk]
  elif len(sp_list) == 2:                                   # 2-parameter function:
    if fnk in whitelist_table_2:
      python_code = "%s(sp_list[0],sp_list[1])" % whitelist_table_2[fnk]
  elif len(sp_list) == 3:                                   # 3-parameter function:
    if fnk in whitelist_table_3:
      python_code = "%s(sp_list[0],sp_list[1],sp_list[2])" % whitelist_table_3[fnk]
  elif len(sp_list) == 4:                                   # 4-parameter function:
    if fnk in whitelist_table_4:
      python_code = "%s(sp_list[0],sp_list[1],sp_list[2],sp_list[3])" % whitelist_table_4[fnk]
  print("python code:", python_code)
  first_eval = eval(python_code)
  return compile_bracket_ops_sp(bracket_op,first_eval)  
      
# op2 op1 fn-2 (|x>, |y>)
def compile_op_sequence_fnk(op_seq,sp_list):
  if len(op_seq) == 0:
    return ket("")
  fnk = op_seq[-1]
  new_op_seq = op_seq[:-1]
  python_code = "ket('')"
#  if len(sp_list) == 1:                                   # 1-parameter function:
#    if fnk in whitelist_table_1:
#      python_code = "%s(sp_list[0])" % whitelist_table_1[fnk]
  if len(sp_list) == 2:                                   # 2-parameter function:
    if fnk in whitelist_table_2:
      python_code = "%s(sp_list[0],sp_list[1])" % whitelist_table_2[fnk]
  elif len(sp_list) == 3:                                   # 3-parameter function:
    if fnk in whitelist_table_3:
      python_code = "%s(sp_list[0],sp_list[1],sp_list[2])" % whitelist_table_3[fnk]
  elif len(sp_list) == 4:                                   # 4-parameter function:
    if fnk in whitelist_table_4:
      python_code = "%s(sp_list[0],sp_list[1],sp_list[2],sp_list[3])" % whitelist_table_4[fnk]
  print("python code:", python_code)
  first_eval = eval(python_code)
  return compile_op_sequence_sp(new_op_seq,first_eval)
  
  
              

class reference(object):
  def __init__(self,value=None):
    if type(value) == str:                                # cast value to ket/sp type
      self.object = ket(value)
    elif type(value) in [ket,superposition]:
      self.object = value
    else:
      self.object = None

  def get(self):
    return self.object

  def set(self,value):
    if type(value) == str:                                # cast value to ket/sp type
      self.object = ket(value)
    if type(value) in [ket,superposition]:
      self.object = value


def ket_substitute(label,value,self_object):
  if label == "_self":
    if self_object.get() is not None:
      return self_object.get().multiply(value)
  return ket(label,value)


def my_pprint(s):
  pprint(s)
  return s

def ops_type(ops):
  if len(ops) > 0:                                # tidy later!
    if type(ops[0]) == tuple:                     # bracket_ops found
      if ops[0][0] in ['+', '-']:
        return "bracket_ops"
  return "opsequence"  

# currently need this since op_sequence and bracket_ops have different "shapes" 
def compile_op_sp(ops,sp): 
  foo = compile_op_sequence_sp                        # default to op_sequence type ops, not bracket_ops
  if len(ops) > 0:                                # tidy later!
    if type(ops[0]) == tuple:                     # bracket_ops found
      if ops[0][0] in ['+', '-']:
        print("found bracket_ops")
        foo = compile_bracket_ops_sp
  return foo(ops,sp)        

# compile sp parse tree
def old_compile_compound_superposition(cs,sign=None):           # tidy this function once it is working.
  ops, object, *rest = cs
  print("cs: ",end='')
  pprint(cs)
  print("ops: ",end='')
  pprint(ops)
  print("sign:",sign)
  print("object: ",end='')
  pprint(object)
  print("rest: ",end='')
  pprint(rest)

  if sign == "sp -":
    sign = -1
  else:
   sign = 1

  if type(object) == str:                         # ket found
    the_sp = ket(object)
  elif type(object) == list:                        # I think this is where we have to handle bracketk_cs. Yup, looks like it.
    if len(object) == 1:                            # Hrmm.... currently "sp |x> == sp (|x>)". I don't think we want this. 
      the_sp = compile_compound_superposition(object[0])  # the problem is, given "fn1 (|x> + |y>)" if fn1 in whitelist_table_1 then use it, otherwise return the sp and treat fn1 as an operator.
    else:                                                 # but for all other cases, if "fnk (ECS,ECS,...,ECS)" and fnk is not in whitelist_table_k, then return the empty ket.
      print("bracketk_cs found")                  
      if ops_type(ops) != "opsequence" or len(ops) == 0:        # "bracket_ops bracketk_cs" makes no sense. eg "(op3 + op2 op1) (|x>, |y>, |z>)", so return |>
        the_sp = ket("")                                        # |> or 0|> ??
      else:
        sp_list = [compile_compound_superposition(x) for x in object]
        str_sp_list = [ str(x) for x in sp_list]
        print("str_sp_list:",str_sp_list)
        fnk = ops[-1]
        new_ops = ops[:-1]
        print("fnk:",fnk)
        print("new_ops:",new_ops)
        python_code = 'ket("")'                                 # default value if fnk(ECS,ECS,...,ECS) is not in whitelist_table. Maybe we want something else?
        if len(sp_list) == 2:                                   # 2-parameter function:
          if fnk in whitelist_table_2:
            python_code = "%s(sp_list[0],sp_list[1])" % whitelist_table_2[fnk]
        elif len(sp_list) == 3:                                   # 3-parameter function:
          if fnk in whitelist_table_3:
            python_code = "%s(sp_list[0],sp_list[1],sp_list[2])" % whitelist_table_3[fnk]
        elif len(sp_list) == 4:                                   # 4-parameter function:
          if fnk in whitelist_table_4:
            python_code = "%s(sp_list[0],sp_list[1],sp_list[2],sp_list[3])" % whitelist_table_4[fnk]
        print("python code:", python_code)
        the_sp = eval(python_code)
        ops = new_ops
              
  elif type(object) == tuple:                                   # how handle fnk objects in this branch?
    prefix, tuple_ops, tuple_rest = object                            # eg: " (op2 op1) fn3 ( |x>,|y> ,|z>  ) "
    if prefix != 'op_cs':
      print("WARNING: wrong prefix:",prefix)
    print("tuple_ops: ",end='')
    pprint(tuple_ops)
    print("tuple_rest: ",end='')
    pprint(tuple_rest)
    if tuple_rest[0] == []:
      new_tuple_object = [tuple_ops,tuple_rest[1]]             # does this break anything?? Let's call it "operator injection".
      print("new_tuple_object: ",end='')
      pprint(new_tuple_object)
      the_sp = compile_compound_superposition(new_tuple_object)
    else:    
      tuple_sp = compile_compound_superposition(tuple_rest)
      print("tuple_sp:",str(tuple_sp))
      the_sp = compile_op_sp(tuple_ops,tuple_sp)
  else:
    print("WARNING: unknown object type!")
      
  result = compile_op_sp(ops,the_sp).multiply(sign)           # how handle |x> _ |y> _ |z> ??
  print("result:",str(result))
  if len(rest) == 0:
    return result
  if type(rest) == list:
    sign,tail = rest[0]
    print("tail: ",end='')
    pprint(tail)
    result += compile_compound_superposition(tail,sign)
    print("final result:",result)
    return result
  
# compile sp parse tree
def compile_compound_superposition(cs,sign=None):           # tidy this function once it is working.
  ops, object, *rest = cs
  print("cs: ",end='')
  pprint(cs)
  print("ops: ",end='')
  pprint(ops)
  print("object: ",end='')
  pprint(object)
  print("sign:",sign)
  print("rest: ",end='')
  pprint(rest)

  if sign == "sp -":
    sign = -1
  else:
   sign = 1

  if type(object) == str:                                     # ket found. later put in the self_object code here.
    the_sp = ket(object)
  elif type(object) == list:                                  # this is where we have to handle bracketk_cs. Yup, looks like it.
    print("bracketk_cs found")                  
    if ops_type(ops) != "opsequence" or len(ops) == 0:        # "bracket_ops bracketk_cs" makes no sense. eg "(op3 + op2 op1) (|x>, |y>, |z>)", so return |>
      if len(object) == 1:                                    # Hrmm.... currently "sp |x> == sp (|x>)". I don't think we want this.
        the_sp = compile_compound_superposition(object[0])    # the problem is, given "fn1 (|x> + |y>)" if fn1 in whitelist_table_1 then use it, otherwise return the sp and treat fn1 as an operator.
      else:                                                   # but for all other cases, if "fnk (ECS,ECS,...,ECS)" and fnk is not in whitelist_table_k, then return the empty ket.
        the_sp = ket("")                                        # |> or 0|> ??    
    else:                                                 
      sp_list = [compile_compound_superposition(x) for x in object]
      str_sp_list = [ str(x) for x in sp_list]
      print("str_sp_list:",str_sp_list)
      fnk = ops[-1]
      new_ops = ops[:-1]
      print("fnk:",fnk)
      print("new_ops:",new_ops)
      
      if len(object) == 1 and fnk not in whitelist_table_1:
        the_sp = sp_list[0]
      else: 
        python_code = 'ket("")'                                 # default value if fnk(ECS,ECS,...,ECS) is not in whitelist_table. Maybe we want something else?
        if len(sp_list) == 1:                                   # 1-parameter function:
          if fnk in whitelist_table_1:
            python_code = "%s(sp_list[0])" % whitelist_table_1[fnk]
        if len(sp_list) == 2:                                   # 2-parameter function:
          if fnk in whitelist_table_2:
            python_code = "%s(sp_list[0],sp_list[1])" % whitelist_table_2[fnk]
        elif len(sp_list) == 3:                                   # 3-parameter function:
          if fnk in whitelist_table_3:
            python_code = "%s(sp_list[0],sp_list[1],sp_list[2])" % whitelist_table_3[fnk]
        elif len(sp_list) == 4:                                   # 4-parameter function:
          if fnk in whitelist_table_4:
            python_code = "%s(sp_list[0],sp_list[1],sp_list[2],sp_list[3])" % whitelist_table_4[fnk]
        print("python code:", python_code)
        the_sp = eval(python_code)
        ops = new_ops
              
  elif type(object) == tuple:                                   # how handle fnk objects in this branch?
    prefix, tuple_ops, tuple_rest = object                            # eg: " (op2 op1) fn3 ( |x>,|y> ,|z>  ) "
    if prefix != 'op_cs':
      print("WARNING: wrong prefix:",prefix)
    print("tuple_ops: ",end='')
    pprint(tuple_ops)
    print("tuple_rest: ",end='')
    pprint(tuple_rest)
    if tuple_rest[0] == []:
      new_tuple_object = [tuple_ops,tuple_rest[1]]             # does this break anything?? Let's call it "operator injection".
      print("new_tuple_object: ",end='')
      pprint(new_tuple_object)
      the_sp = compile_compound_superposition(new_tuple_object)
    else:    
      tuple_sp = compile_compound_superposition(tuple_rest)
      print("tuple_sp:",str(tuple_sp))
      the_sp = compile_op_sp(tuple_ops,tuple_sp)
  else:
    print("WARNING: unknown object type!")
      
  result = compile_op_sp(ops,the_sp).multiply(sign)           # how handle |x> _ |y> _ |z> ??
  print("result:",str(result))
  if len(rest) == 0:
    return result
  if type(rest) == list:
    sign,tail = rest[0]
    print("tail: ",end='')
    pprint(tail)
    result += compile_compound_superposition(tail,sign)
    print("final result:",result)
    return result

    
# initialize the self_object
self_object = reference()


bindings_dictionary = {
  "float_int"               : float_int,
  "ket_substitute"          : ket_substitute,
  "self_object"             : self_object,
  
  "ket_calculate"           : ket_calculate,
  "sp_calculate"            : sp_calculate,

  "process_op_sequence_sp"  : process_op_sequence_sp,
  "process_bracket_ops_sp"  : process_bracket_ops_sp,
 
  "process_op_sequence_fnk" : process_op_sequence_fnk,
  "process_bracket_ops_fnk" : process_bracket_ops_fnk,  

  "compile_op_sequence"     : compile_op_sequence,
  "compile_bracket_ops"     : compile_bracket_ops,
  
  "compile_op_sequence_sp"  : compile_op_sequence_sp,
  "compile_bracket_ops_sp"  : compile_bracket_ops_sp,
  
  "compile_bracket_ops_fnk" : compile_bracket_ops_fnk,
  "compile_op_sequence_fnk" : compile_op_sequence_fnk,
  
#  "pprint"                  : my_pprint,
  "compile_compound_superposition" : compile_compound_superposition,
}

    
# wow! slow. 755 ms per makeGrammar.
# and we haven't even finished yet. 
start_time = time.time()      
op_grammar = makeGrammar(our_full_grammar,bindings_dictionary)
end_time = time.time()
delta_time = end_time - start_time
print("\n  Time taken:",display_time(delta_time))
#sys.exit(0)

def test_grammar_rhs_ket_like():
  x = op_grammar(" 2.7|z> ").rhs_ket_like()
  assert str(x) == "2.7|z>"

def test_grammar_compound_superposition_sp_ket():
  x = op_grammar(" sp |x> ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_sp_bracket_ket():
  x = op_grammar(" sp (|x>) ").compiled_compound_superposition()
  assert str(x) == ""
  
def test_grammar_compound_superposition_sp_bracket_sp():
  x = op_grammar(" sp (|x> + |y> + |z>) ").compiled_compound_superposition()
  assert str(x) == ""  

def test_grammar_compound_superposition_naked_fn2():
  x = op_grammar(" ( |x>,|y> ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_fn3():
  x = op_grammar(" fn3 ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_ops_fn3():
  x = op_grammar(" op3 op2 fn3 ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""
  
def test_grammar_compound_superposition_union3():
  x = op_grammar(" union ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_ops_union3():
  x = op_grammar(" op3 op2 union ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""  

def test_grammar_compound_superposition_bracket_fn3():
  x = op_grammar(" (op3 op2 op1) ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_bracket_ops_fn3():
  x = op_grammar(" (op2 op1) fn3 ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_bracket_ops_union3():
  x = op_grammar(" (op2 op1) union ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_bracket_ops_fn3_big():
  x = op_grammar(" (op6) (op5) op4 (op3) op2 (op1) fn3 ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_bracket_ops_union3_big():
  x = op_grammar(" (op6) (op5) op4 (op3) op2 (op1) union ( |x>,|y> ,|z>  ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_fn1():
  x = op_grammar(" sp ( |x> ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_ops_fn1():
  x = op_grammar(" op2 op1 sp ( |x> ) ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition():
  x = op_grammar(" 2.7|z> ").compiled_compound_superposition()
  assert str(x) == "2.7|z>"

def test_grammar_compound_superposition_sp():
  x = op_grammar(" |x> - 3|y> + 2.7|z> ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_sp_big():
  x = op_grammar(" |x> - 3|y> + 2.7|z> - |fish> - |cats> + |dogs> ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_bracket():
  x = op_grammar(" ( 2.7|z> ) ").compiled_compound_superposition()
#  assert str(x) == "2.7|z>"
  assert str(x) == ""
    
def test_grammar_compound_superposition_bracket_sp():
  x = op_grammar(" ( |x> + 0.5|y> + 2.7|z> ) ").compiled_compound_superposition()
#  assert str(x) == "|x> + 0.5|y> + 2.7|z>"
  assert str(x) == ""
  
def test_grammar_compound_superposition_bracket_sp_big():
  x = op_grammar(" ( |x> + 0.5|y> + 2.7|z> ) + |fish> + (|cats> + |dogs>) + |mice> + |rats> ").compiled_compound_superposition()
#  assert str(x) == "|x> + 0.5|y> + 2.7|z> + |fish> + |cats> + |dogs> + |mice> + |rats>"
  assert str(x) == ""

def test_grammar_compound_superposition_bracket_sp_big_brackets():
  x = op_grammar(" ( |x> + 0.5|y> + 2.7|z> ) + ((|fish> + (|cats> + |dogs>)) + |mice>) + |rats> ").compiled_compound_superposition()
#  assert str(x) == "|x> + 0.5|y> + 2.7|z> + |fish> + |cats> + |dogs> + |mice> + |rats>"
  assert str(x) == ""

def test_grammar_compound_superpostion_op_seq():
  x = op_grammar(" op3 op2 op1 2.7|z>  ").compiled_compound_superposition()
#  assert str(x) == "2.7|op3: op2: op1: z>"
  assert str(x) == ""

def test_grammar_compound_superposition_bracket_ops():
  x = op_grammar(" (op3 op2 op1) |x>  ").compiled_compound_superposition()
#  assert str(x) == "|op3: op2: op1: x>"
  assert str(x) == ""

def test_grammar_compound_superposition_bracket_ops_seq():
  x = op_grammar(" (op5 op4 op3) op2 op1 |x>  ").compiled_compound_superposition()
#  assert str(x) == "|op5: op4: op3: op2: op1: x>"
  assert str(x) == ""

def test_grammar_compound_superposition_op_bracket():
  x = op_grammar(" op2 op1 (3|x> - |y> + 0.2|z>) ").compiled_compound_superposition()
#  assert str(x) == "3|op2: op1: x> + |op2: op1: y> + 0.2|op2: op1: z>"
  assert str(x) == ""

def test_grammar_compound_superposition_brackets_op_bracket():
  x = op_grammar(" (1 + op4 - op3) op2 op1 (3|x> + 0.2|z>) ").compiled_compound_superposition()
#  assert str(x) == "3|op2: op1: x> + 0.2|op2: op1: z> + 3|op4: op2: op1: x> + 0.2|op4: op2: op1: z> + -3|op3: op2: op1: x> + -0.2|op3: op2: op1: z>"
  assert str(x) == ""  

def test_grammar_compound_superposition_brackets_op_bracket_v2():
  x = op_grammar(" op5 (1 - op4 ) op2 op1 (3|x> + 0.2|z>) ").compiled_compound_superposition()
#  assert str(x) == "3|op5: op2: op1: x> + 0.2|op5: op2: op1: z> + -3|op5: op4: op2: op1: x> + -0.2|op5: op4: op2: op1: z>"
  assert str(x) == ""

def test_grammar_compound_superpostion_empty_bracket():
  x = op_grammar(" () (3|x> + |y>) ").compiled_compound_superposition()
#  assert str(x) == "3|x> + |y>"
  assert str(x) == ""

def test_grammar_compound_superposition_op_sentence():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> ").compiled_compound_superposition() 
#  assert str(x) == "9|Jack> + 9|Emma> + 9|Charlie>"
  assert str(x) == ""  

# Bah! This is being parsed as: "3^2 common[friends] ( split |Fred Sam> + |mice> + (|cats> + |dogs>)) "
def test_grammar_compound_superposition_op_sentence_sum():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> + |mice> + (|cats> + |dogs>) + split |horse pony mare> ").compiled_compound_superposition()
#  x = op_grammar(" 3^2 common[friends] split |Fred Sam> + |mice> + (|cats> + |dogs>) ").compiled_compound_superposition() 
  assert str(x) == ""  

def test_grammar_compound_superposition_op_sentence_sum_v2():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> + |mice> + (|cats> + |dogs>) + 5^3 split |horse pony mare> ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_op_sentence_sum_v3():
  x = op_grammar(" 3^2 common[friends] split |Fred Sam> + |mice> - (|cats> + |dogs>) + 5^3 split |horse pony mare> ").compiled_compound_superposition()
  assert str(x) == ""

def test_grammar_compound_superposition_op_sentence_sum_v4():
  x = op_grammar(" op8 (op7) op5 (op4 - op2) sp(split|x y> - |z>) ").compiled_compound_superposition()
  assert str(x) == ""
        
#===================================================================================================================
def test_grammar_literal_sp():
  x = op_grammar("3|x> + |y> + 2.7|z>").literal_superposition()
  assert str(x) == "3|x> + |y> + 2.7|z>"

def test_grammar_literal_sp_substitute():
  self_object.set(ket("fish-soup",3))
  x = op_grammar("3|x> + |y> + 2.7|_self>").literal_superposition()
  assert str(x) == "3|x> + |y> + 8.1|fish-soup>"

def test_grammar_literal_sp_substitute_rabbits():                   
  self_object.set("rabbits")
  x = op_grammar("3|x> + |y> + 2.7|_self>").literal_superposition()
  assert str(x) == "3|x> + |y> + 2.7|rabbits>"
  
  
def test_grammar_literal_sp_substitute_object():
  self_object.set(ket("fish-soup",3))
  x = op_grammar("3|x> + |y> + 2.7|_self>").object()
  assert str(x) == "3|x> + |y> + 8.1|fish-soup>"

def test_grammar_literal_sp_substitute_rabbits_object():                   
  self_object.set("rabbits")
  x = op_grammar("3|x> + |y> + 2.7|_self>").object()
  assert str(x) == "3|x> + |y> + 2.7|rabbits>"


def test_grammar_op_sequence_object():
  x = op_grammar(" op3 op2 op1 |x> ").op_sequence_object()
  assert str(x) == "|op3: op2: op1: x>"

def test_grammar_op_sequence_object_sp():
  x = op_grammar(" op2 op1 (3|x> + |y> + 0.2|z>) ").op_sequence_object()
  assert str(x) == "3|op2: op1: x> + |op2: op1: y> + 0.2|op2: op1: z>"
  
def test_grammar_op_sequence_object_object():
  x = op_grammar(" op3 op2 op1 |x> ").object()
  assert str(x) == "|op3: op2: op1: x>"

def test_grammar_op_sequence_object_sp_object():
  x = op_grammar(" op2 op1 (3|x> + |y> + 0.2|z>) ").object()
  assert str(x) == "3|op2: op1: x> + |op2: op1: y> + 0.2|op2: op1: z>"


def test_grammar_bracket_ops_ket():
  x = op_grammar(" (op3 + op2 op1) |x> ").bracket_ops_object()
  assert str(x) == "|op3: x> + |op2: op1: x>"

def test_grammar_bracket_ops_sp():
  x = op_grammar(" (op2 - op1) (3|x> + |y> + 0.2|z>) ").bracket_ops_object()
  assert str(x) == "3|op2: x> + |op2: y> + 0.2|op2: z> + -3|op1: x> + -1|op1: y> + -0.2|op1: z>"

def test_grammar_bracket_ops_sp_v2():
  x = op_grammar(" (op2 - 2 op1) (3|x> + |y> + 0.2|z>) ").bracket_ops_object()
  assert str(x) == "3|op2: x> + |op2: y> + 0.2|op2: z> + -6|op1: x> + -2|op1: y> + -0.4|op1: z>"

def test_grammar_bracket_ops_sp_object():
  x = op_grammar(" (op2 - 2 op1) (3|x> + |y> + 0.2|z>) ").object()
  assert str(x) == "3|op2: x> + |op2: y> + 0.2|op2: z> + -6|op1: x> + -2|op1: y> + -0.4|op1: z>"
  
def test_grammar_empty_bracket_ops_sp_object():
  x = op_grammar(" () (3|x> + |y>) ").object()
  assert str(x) == "3|x> + |y>"  

def test_grammar_fn1():
  x = op_grammar(" sp (3|x> + |y>) ").object()
  assert str(x) == "|sp> + 3|x> + |y>"
  
def test_grammar_op_seq_fn1():
  x = op_grammar(" op2 op1 sp (3|x> + |y>) ").object()
  assert str(x) == "|op2: op1: sp> + 3|op2: op1: x> + |op2: op1: y>"  

# (op2 + op1) fn-2 (|x>, |y>)
def test_grammar_bracket_ops_fnk():
  x = op_grammar(" (op2 + op1) fn-2 (|x>, |y>) ").object()
  assert str(x) == "|op2: > + |op1: >"
  
# (op2 + op1) union (|x>, |y>)
def test_grammar_bracket_ops_union():
  x = op_grammar(" (op2 + op1) union (|x>, |y>) ").object()
  assert str(x) == "|op2: x> + |op2: y> + |op1: x> + |op1: y>"  

# op2 op1 fn-2 (|x>, |y>)
def test_grammar_sequence_ops_fnk():
  x = op_grammar(" op2 op1 fn-2 (|x>, |y>) ").object()
  assert str(x) == "|op2: op1: >"
  
# op2 op1 union (|x>, |y>)
def test_grammar_sequence_ops_union():
  x = op_grammar(" op2 op1 union (|x>, |y>) ").object()
  assert str(x) == "|op2: op1: x> + |op2: op1: y>"

# op2 op1 (1 + op3 + op5^2) (op6 + op7) op8 op9 |x>
def test_op_objects_sequences_big():
  x = op_grammar(" op2 op1 (1 + op3 - op5^2) (op6 + op7) op8 op9 |x> ").object()
  assert str(x) == "|op2: op1: op6: op8: op9: x> + |op2: op1: op7: op8: op9: x> + |op2: op1: op3: op6: op8: op9: x> + |op2: op1: op3: op7: op8: op9: x> + -1|op2: op1: op5: op5: op6: op8: op9: x> + -1|op2: op1: op5: op5: op7: op8: op9: x>"  

def test_op_sentence():
  x = op_grammar("3^2 common[friends] split |Fred Sam>").object_sum() 
  assert str(x) == "9|Jack> + 9|Emma> + 9|Charlie>"

# 3.2|a> + 8|b> + 0.5|c> + |d> + 6|x> + 1.7|y> + |fish>
def test_op_simple_sp_sum():
  x = op_grammar(" (3|a> + 7 |b> + 0.5|c> ) + (|b> + 0.2|a> + |d>) + (|x> + 2|y>) - (0.3|y> - 5|x>) + (|fish>)").object_sum()
  assert str(x) == "3.2|a> + 8|b> + 0.5|c> + |d> + 6|x> + 1.7|y> + |fish>"
  
def test_op_sentence_sum():
  x = op_grammar("3^2 common[friends] split |Fred Sam> + union(|x>,|y>)").object_sum() 
  assert str(x) == "9|Jack> + 9|Emma> + 9|Charlie> + |x> + |y>"
  
def test_op_sentence_sum_brackets():
  x = op_grammar(" (3^2 common[friends] split |Fred Sam> + union(|x>,|y>)) ").object() 
  assert str(x) == ""  
  

# run-time for the two parse rules: 2 ms
# I wonder what run-time for .object()? 
#start_time = time.time()      
#test_grammar_literal_sp()
#test_grammar_literal_sp_substitute()
#end_time = time.time()
#delta_time = end_time - start_time
#print("\n  Time taken v2:",display_time(delta_time))
#sys.exit(0)

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
#def test_op_bracket_literal_superposition():
#  x = op_grammar(" ( 3.2|a> + |b> + 3.1415|pi> -|d> + |z>  ) ").bracket_literal_superposition()
#  assert str(x) == "3.2|a> + |b> + 3.142|pi> + -1|d> + |z>"

# ['3.2|a> + |b> + 3.142|pi> + -1|d> + |z>']
# NB: the current rule applies str() to the sp.
def test_op_bracket1_object():
#  x = op_grammar(" ( 3.2|a> + |b> + 3.1415|pi> -|d> + |z>  ) ").bracket1_literal_superposition()
#  assert str(x) == "['3.2|a> + |b> + 3.142|pi> + -1|d> + |z>']"
  x = op_grammar(" ( 3.2|a> + |b> + 3.1415|pi> -|d> + |z>  ) ").bracket1_object()
  assert str(x) == "3.2|a> + |b> + 3.142|pi> + -1|d> + |z>"

def test_op_bracketk_object():
  x = op_grammar(" ( 3.2|a> + |b> + 3.1415|pi> -|d> + |z>  ) ").bracketk_object()
  assert str(x[0]) == "3.2|a> + |b> + 3.142|pi> + -1|d> + |z>"


# 3.2|a> + 8|b> + 0.5|c> + |d>
def test_op_literal_superposition_plus_literal_superposition():
  x = op_grammar(" (3|a> + 7 |b> + 0.5|c> ) + (|b> + 0.2|a> + |d>)  ").object_sum()
  assert str(x) == "3.2|a> + 8|b> + 0.5|c> + |d>"

# 3.2|a> + 8|b> + 0.5|c> + |d> + 6|x> + 1.7|y> + |fish>
def test_op_literal_superposition_plus_literal_superposition_plus_more():
  x = op_grammar(" (3|a> + 7 |b> + 0.5|c> ) + (|b> + 0.2|a> + |d>) + (|x> + 2|y>) - (0.3|y> - 5|x>) + (|fish>)").object_sum()
  assert str(x) == "3.2|a> + 8|b> + 0.5|c> + |d> + 6|x> + 1.7|y> + |fish>"


# 3.7|fish>
def test_op_ket_like_object_single_ket():
  x = op_grammar(" 3.7|fish> ").ket_like_object()
  assert str(x) == "3.7|fish>"

# 2|x> + |y>   
def test_op_ket_like_object_literal_sp():
  x = op_grammar(" (2|x> + |y>) ").ket_like_object()
  assert str(x) == "2|x> + |y>"
  
def test_op_ket_like_object_brackets_literal_sp():
  x = op_grammar("(( (2|x> + |y>) ))").ket_like_object()
  assert str(x) == "2|x> + |y>"
  

## [['op3', 'op2', 'op1', 3.7], '|fish>']
# NB: the 3.7 is considered an operator. Not sure if we want this. Don't know how to change if we don't.
# [[('+', ['op3', 'op2', 'op1', 3.7])], '|fish>']
def test_op_op_sequence_object_single_ket():
  x = op_grammar(" op3 op2 op1 3.7|fish> ").op_sequence_object()
#  assert str(x) == "[['op3', 'op2', 'op1', 3.7], '|fish>']"
  assert str(x) == "[[('+', ['op3', 'op2', 'op1', 3.7])], '|fish>']"

## [['op3', 'op2', 'op1'], '2|x> + |y>']   
#
def test_op_op_sequence_object_literal_sp():
  x = op_grammar(" op3 op2 op1 (2|x> + |y>) ").op_sequence_object()
#  assert str(x) == "[['op3', 'op2', 'op1'], '2|x> + |y>']"
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], '2|x> + |y>']"

# [[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '3.7|fish>']  
def test_op_bracket_ops_object_single_ket():
  x = op_grammar(" (1 + op - op^2 + op3^5) 3.7|fish> ").bracket_ops_object()
  assert str(x) == "[[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '3.7|fish>']"

# for later!
#def test_op_bracket_ops_sp_kets():
#  x = op_grammar(" (1 + op - op^2 + op3^5) 3.7|fish> + 3|pie> + 0.5 |cats> ").bracket_ops_sp()
#  assert str(x) == ""

# [[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '2|x> + |y>']   
def test_op_bracket_ops_object_literal_sp():
  x = op_grammar(" (1 + op - op^2 + op3^5) (2|x> + |y>) ").bracket_ops_object()
  assert str(x) == "[[('+', [1]), ('+', ['op']), ('-', [('op', 2)]), ('+', [('op3', 5)])], '2|x> + |y>']"

## [['op3', 'op2', 'op1', 'fn-1'], ['2|x> + |y>', '|a> + |b> + 0.3|z>']]
# [[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]
def test_op_op_sequence_object_fnk_literal_sps_2():
  x = op_grammar(" op3 op2 op1 fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").op_sequence_object_fnk()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]"
  
  
  
## [['op3', 'op2', 'op1', 'fn-1'], ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]
# [[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]
def test_op_op_sequence_object_fnk_literal_sps_3():
  x = op_grammar(" op3 op2 op1 fn-3 (2|x> + |y>, |a> + |b> + 0.3|z>,|fish> ) ").op_sequence_object_fnk()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]"

## [['op3', 'op2', 'op1', 'fn-1'], ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]
# [[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]
def test_op_op_sequence_object_fnk_literal_sps_4():
  x = op_grammar(" op3 op2 op1 fn-4 (2|x> + |y>, |a> + |b> + 0.3|z>,|pi>,|e> + |log> ) ").op_sequence_object_fnk()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]"


# [[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]
def test_op_bracket_ops_object_fnk_literal_sps_2():
  x = op_grammar(" (op3 op2 op1) fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").bracket_ops_object_fnk()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['2|x> + |y>', '|a> + |b> + 0.3|z>']]"

# [[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]
def test_op_bracket_ops_object_fnk_literal_sps_3():
  x = op_grammar(" ( op3 op2 op1) fn-3 (2|x> + |y>, |a> + |b> + 0.3|z>,|fish> ) ").bracket_ops_object_fnk()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|fish>']]"

# [[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']] 
def test_op_bracket_ops_object_fnk_literal_sps_4():
  x = op_grammar(" (op3 op2 op1) fn-4 (2|x> + |y>, |a> + |b> + 0.3|z>,|pi>,|e> + |log> ) ").bracket_ops_object_fnk()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['2|x> + |y>', '|a> + |b> + 0.3|z>', '|pi>', '|e> + |log>']]"


# test bracket_ops_fn2 == op_sequence_fn2. This is to help make some things easier:
def test_op_bracket_ops_object_fnk__op_sequence_object_fnk_literal_sps():
  x1 = op_grammar(" op3 op2 op1 fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").op_sequence_object_fnk()
  x2 = op_grammar(" (op3 op2 op1) fn-2 (2|x> + |y>, |a> + |b> + 0.3|z> ) ").bracket_ops_object_fnk()
  assert str(x1) == str(x2)



# .apply_fn(split_ket).apply_sp_fn(common,context,"friends").multiply(3).multiply(3)
def test_op_compiled_op_sequence():
  x = op_grammar("3^2 common[friends] split").compiled_op_sequence() 
  assert str(x) == '.apply_fn(split_ket).apply_sp_fn(common,context,"friends").multiply(3).multiply(3)'


# ['.apply_fn(split_ket).apply_sp_fn(common,context,"friends").multiply(3).multiply(3)']
def test_op_compiled_bracket_ops():
  x = op_grammar(" (3^2 common[friends] split) ").compiled_bracket_ops() 
  assert str(x) == '[\'.apply_fn(split_ket).apply_sp_fn(common,context,"friends").multiply(3).multiply(3)\']'
  
# ['.multiply(1)', '.apply_op(context,"op")', '.apply_op(context,"op").apply_op(context,"op").multiply(-1)', '.apply_op(context,"op3")']
def test_op_compiled_bracket_ops():
  x = op_grammar(" (1 + op - op^2 + op3) ").compiled_bracket_ops() 
  assert str(x) == '[\'.multiply(1)\', \'.apply_op(context,"op")\', \'.apply_op(context,"op").apply_op(context,"op").multiply(-1)\', \'.apply_op(context,"op3")\']'


## sp_len_1(|x> + 3.2|y> + -1|z>)
# [[('+', [])], 'sp_len_1', ['|x> + 3.2|y> + -1|z>']]
def test_op_param1_fn():
#  x = op_grammar("sp (|x> + 3.2|y> -|z>)").param1_fn()
  x = op_grammar("sp (|x> + 3.2|y> -|z>)").op_sequence_object() 
  assert str(x) == "[[('+', [])], 'sp_len_1', ['|x> + 3.2|y> + -1|z>']]"

## intersection(|x> + 3.2|y> + -1|z>, |y>)
# [[('+', [])], 'intn', ['|x> + 3.2|y> + -1|z>', '|y>']]
def test_op_param2_fn():
#  x = op_grammar("intn (|x> + 3.2|y> -|z>,|y>)").param2_fn()
  x = op_grammar("intn (|x> + 3.2|y> -|z>,|y>)").op_sequence_object_fnk()
  assert str(x) == "[[('+', [])], 'intn', ['|x> + 3.2|y> + -1|z>', '|y>']]"

## algebra(|a>, |+>, |b>)
# [[('+', [])], 'algebra', ['|a>', '|+>', '|b>']]
def test_op_param3_fn():
  x = op_grammar("algebra (|a>,|+>,|b>)").op_sequence_object_fnk() 
  assert str(x) == "[[('+', [])], 'algebra', ['|a>', '|+>', '|b>']]"

def test_op_op_sequence_vs_bracket_param3_fn():
  x1 = op_grammar(" ( ) algebra (|a>,|+>,|b>)").bracket_ops_object_fnk()
  x2 = op_grammar("algebra (|a>,|+>,|b>)").op_sequence_object_fnk() 
  assert str(x1) == str(x2)


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


# test the object rule section:
# slowly getting closer to a full extract_compound_superposition rule.
# 2|x> + |y> + 3.27|z>
def test_op_objects_literal_sp():
  x = op_grammar("2|x> + |y> +3.27|z>").object()
  assert str(x) == "2|x> + |y> + 3.27|z>"
  
# 2|x> + |y> + 3.27|z>
def test_op_objects_literal_sp_bracket():
  x = op_grammar(" ( 2|x> + |y> +3.27|z>)").object()
  assert str(x) == "2|x> + |y> + 3.27|z>"

def test_op_objects_ops_ket():
  x = op_grammar(" op3 op2 op1 2|x>").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1', 2])], '|x>']"
  
def test_op_objects_ops_ket_bracket():
  x = op_grammar(" (op3 op2 op1 2|x>)").object()
  assert str(x) == "[[[('+', ['op3', 'op2', 'op1', 2])], '|x>']]"
  
# [[('+', ['op3', 'op2', 'op1', 2])], '|x>']
def test_op_objects_ops_ket_bracket():
  x = op_grammar(" ( (op3 op2 op1 2|x>))").object()
#  assert str(x) == "[[[[('+', ['op3', 'op2', 'op1', 2])], '|x>']]]"
  assert str(x) == "[[('+', ['op3', 'op2', 'op1', 2])], '|x>']"

# [[('+', ['op5', 'op4'])], "[[('+', ['op3', 'op2', 'op1', 2])], '|x>']"]
def test_op_objects_ops_ops_ket_bracket():
  x = op_grammar(" op5 op4 (op3 op2 op1 2|x>)").object()
  assert str(x) == "[[('+', ['op5', 'op4'])], \"[[('+', ['op3', 'op2', 'op1', 2])], '|x>']\"]"

# [[('+', ['op5', 'op4'])], "[[('+', ['op3', 'op2', 'op1', 2])], '|x>']"]
def test_op_objects_bracket_ops_ops_ket_bracket():
  x = op_grammar(" (op5 op4) (op3 op2 op1 2|x>)").object()
  assert str(x) == "[[('+', ['op5', 'op4'])], \"[[('+', ['op3', 'op2', 'op1', 2])], '|x>']\"]"

# [[('+', ['op5', 'op4'])], 'fn-2', ["[[('+', ['op2', 'op1', 2])], '|x>']", "[[('+', ['fish'])], '|soup>']"]]
def test_op_objects_ops_fn2_ops_ket_bracket():
  x = op_grammar(" op5 op4 fn-2 (op2 op1 2|x>, fish |soup>)").object()
  assert str(x) == "[[('+', ['op5', 'op4'])], 'fn-2', [\"[[('+', ['op2', 'op1', 2])], '|x>']\", \"[[('+', ['fish'])], '|soup>']\"]]"

# [[('+', ['op5', 'op4'])], 'fn-2', ["[[('+', ['op2', 'op1'])], '2|x> + |y>']", "[[('+', ['fish'])], '|soup>']"]]
def test_op_objects_ops_fn2_ops_literal_sp_bracket():
  x = op_grammar(" op5 op4 fn-2 (op2 op1 (2|x> +|y>), fish |soup>)").object()
  assert str(x) == "[[('+', ['op5', 'op4'])], 'fn-2', [\"[[('+', ['op2', 'op1'])], '2|x> + |y>']\", \"[[('+', ['fish'])], '|soup>']\"]]"
  
# [[('+', ['op8', 'op7'])], '[[(\'+\', [\'op5\', \'op4\'])], \'fn-2\', ["[[(\'+\', [\'op2\', \'op1\'])], \'2|x> + |y>\']", "[[(\'+\', [\'fish\'])], \'|soup>\']"]]']
def test_op_objects_ops_ops_fn2_ops_literal_sp_bracket():
  x = op_grammar(" op8 op7 (op5 op4 fn-2 (op2 op1 (2|x> +|y>), fish |soup>))").object()
  assert str(x) == "[[('+', ['op8', 'op7'])], '[[(\'+\', [\'op5\', \'op4\'])], \'fn-2\', [\"[[(\'+\', [\'op2\', \'op1\'])], \'2|x> + |y>\']\", \"[[(\'+\', [\'fish\'])], \'|soup>\']\"]]']"
  



## [['op3', 'op2', 'op1'], '2|x> + |y> + 3.27|z>']
# [[('+', ['op3', 'op2', 'op1'])], '2|x> + |y> + 3.27|z>'] 
def test_op_objects_ops_literal_sp_bracket():
  x = op_grammar(" op3 op2 op1( 2|x> + |y> +3.27|z>)").object()
#  assert str(x) == "[['op3', 'op2', 'op1'], '2|x> + |y> + 3.27|z>']"
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], '2|x> + |y> + 3.27|z>']"

# [[('+', ['op3', 'op2', 'op1'])], '2|x> + |y> + 3.27|z>']
def test_op_objects_bracket_ops_literal_sp_bracket():
  x = op_grammar(" (op3 op2 op1)( 2|x> + |y> +3.27|z>)").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], '2|x> + |y> + 3.27|z>']"

# [[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['|a>', '|b>']]
def test_op_objects_ops_fn_2():
  x = op_grammar(" op3 op2 op1 fn-2(|a>,|b> )").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['|a>', '|b>']]"
  
#
def test_op_objects_ops_fn_3():
  x = op_grammar(" op3 op2 op1 fn-3(|a>,|b> ,|c> )").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['|a>', '|b>', '|c>']]"

#
def test_op_objects_ops_fn_4():
  x = op_grammar(" op3 op2 op1 fn-4(|a>,|b> ,|c>,|d> )").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['|a>', '|b>', '|c>', '|d>']]"

def test_op_objects_bracket_ops_fn_2():
  x = op_grammar("( op3 op2 op1) fn-2(|a>,|b> )").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-2', ['|a>', '|b>']]"
  
#
def test_op_objects_bracket_ops_fn_3():
  x = op_grammar(" (op3 op2 op1 )fn-3(|a>,|b> ,|c> )").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-3', ['|a>', '|b>', '|c>']]"

#
def test_op_objects_bracket_ops_fn_4():
  x = op_grammar(" (op3 op2 op1) fn-4(|a>,|b> ,|c>,|d> )").object()
  assert str(x) == "[[('+', ['op3', 'op2', 'op1'])], 'fn-4', ['|a>', '|b>', '|c>', '|d>']]"

#
def test_op_objects_sequences_v1():
  x = op_grammar(" op2 op1 (op6 + op7) op8 op9 |x> ").object()
  assert str(x) == ""


# op2 op1 (1 + op3 + op5^2) (op6 + op7) op8 op9 |x>
def test_op_objects_sequences_v2():
  x = op_grammar(" op2 op1 (1 + op3 + op5^2) (op6 + op7) op8 op9 |x> ").object()
  assert str(x) == ""


# testing object_sum rule:
# [('+', '2|x> + |y> + 3.27|z>')]
#def test_op_object_sum_literal_sp():
#  x = op_grammar("2|x> + |y> +3.27|z>").object_sum()
#  assert str(x) == "[('+', '2|x> + |y> + 3.27|z>')]"

# (3|a> + 7 |b> + 0.5|c> ) - (|b> + 0.2|a> + |d>) + (|x> + 2|y>)
#def test_op_object_sum_literal_sps():
#  x = op_grammar("(3|a> + 7 |b> + 0.5|c> ) - (|b> + 0.2|a> + |d>) + (|x> + 2|y>)").object_sum()
#  assert str(x) == ""
      
