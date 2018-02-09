#!/usr/bin/env python

#######################################################################
# the semantic-db function-operator file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 2018-2-8
# Copyright: GPLv3
#
# Usage: 
#
#######################################################################

# a collection of functions that apply to kets and superpositions (and later sequences and so on).
# the idea is that you add more of these with time.
# I guess, with no upper bound on how many.
# and of course to use them you need to enter them in the appropriate table in the processor.

import sys
import random
import copy
import string
import re

from the_semantic_db_code import *
#from the_semantic_db_processor import *

# the value function
# eg: value |price: _x> => _x |_self>
# provided _x is convertable to float, else return |_self>
def apply_value(one):
  cat, value = one.label.rsplit(': ', 1)
  try:
    x = float(value)
  except ValueError:
    return one
  return ket(one.label,x * one.value)

# the extract category function
# eg: extract-category |animal: fish> => |animal>
def extract_category(one):
  cat, value = one.label.rsplit(': ', 1)  
  return ket(cat,one.value)

# the extract value function
# eg: extract-value |animal: fish> => |fish>
def extract_value(one):
  cat, value = one.label.rsplit(': ', 1)
  return ket(value,one.value)

# 28/8/2015:
# remove-leading-category |a: b: c: d> == |b: c: d>
# I think this will be useful in the table[] code.
# one is a ket
def remove_leading_category(one):
  text = one.label.split(': ',1)[-1]
  return ket(text,one.value)

# find-leading-category |a: b: c: d> == |a>
# one is a ket
def find_leading_category(one):
  text = one.label.split(': ',1)[0]
  return ket(text,one.value)
   

# 1/5/2014:
# to-value and to-category (maybe come up with better names!)
# to-value |> => |>
# to-value |19> => 19| >  -- NB the space, cf to-number
# to-value |age: 23> => 23|age>
# to-value |age: 23.5> => 23.5|age>
# to-value |string> => |string> or 0| >        -- currently the first one.
# to-value |cat: val> => |cat: val> or 0|cat>
# to-value |cat1: cat2: 13> => 13|cat1: cat2>
#
# to-category 57| > => |57>
# to-category |age> => |age: 1>
# to-category 23|age> => |age: 23>
def to_value(one):                          # tested. Seems to work as desired!
  # do we need one = one.ket() here?
  cat, value = extract_category_value(one.label)
  logger.debug("cat: " + cat)
  logger.debug("value: " + value)
  
  if len(cat) == 0:
    label = " "
  else:
    label = cat

  try:
    x = float(value)
    return ket(label,x)
  except:
    return one 

def to_category(one):
  # do we need one = one.ket() here?
  label = one.label
  if label in [""," "]:                      # maybe label.strip() == ""?
    label = ""                               # Also, stop using -- for comments in python!
  else:
    label += ": "
  return ket(label + "%.3f" % one.value)
            

# the range function
# eg: show_range(|year: 1982>, |year: 1985>)
# should spit out: |year: 1982> + |year: 1983> + |year: 1984> + |year: 1985>
# maybe later a sequence version too/instead.
# not sure what to do if the passed in kets have values other than 1.
# later I might need a date range too.
# eg: 2/11/2009 .. 7/12/2009
# probably give it it's own function though.
# if we want -1 steps, use superposition.reverse()

# bug if start or finish are superpositions!
# fix it.
# introduced X.ket(). Breaks if X is a string!
# Nope. Now using X.the_label()
#
def old_show_range(start,finish,step="n: 1"):
# tweak so full kets are optional, and labels are sufficient:
  start_label = start if type(start) == str else start.the_label()
  finish_label = finish if type(finish) == str else finish.the_label()
  step_label = step if type(step) == str else step.the_label()

#  print("step_label:",step_label)

  cat1, v1 = extract_category_value(start_label)
  cat2, v2 = extract_category_value(finish_label)
  cat3, v3 = extract_category_value(step_label)
#  print("v3:",v3)

  if cat1 != cat2 or not v1.isdigit() or not v2.isdigit() or not v3.isdigit():  # maybe check v1, v2 for float instead of int?
    return ket("")
  label = ""
  if len(cat1) > 0:
    label = cat1 + ": "         # perhaps extract_category_value should append the ": " bit??
  result = superposition()      # probably not.
  for k in range(int(v1),int(v2) + 1,int(v3)):
    result += ket(label + str(k))
  return result


# 23/4/2014: need float range:
# from: http://stackoverflow.com/questions/4189766/python-range-with-step-of-type-float
def float_range(start, stop, step):
  while start <= stop + 0.0000001:           # hack so hopefully the float rounding doesn't give the wrong result.
    yield start                              # may need to tweak the 0.0000001 value.
    start += step                            # also, I like my ranges to reach their upper-bound!

# 23/4/2014: decided to change range from integer steps to float steps.
#
def show_range(start,finish,step="n: 1"):
# tweak so full kets are optional, and labels are sufficient:
  start_label = start if type(start) == str else start.the_label()
  finish_label = finish if type(finish) == str else finish.the_label()
  step_label = step if type(step) == str else step.the_label()

#  print("step_label:",step_label)

  cat1, v1 = extract_category_value(start_label)
  cat2, v2 = extract_category_value(finish_label)
  cat3, v3 = extract_category_value(step_label)
#  print("v3:",v3)

  if cat1 != cat2:
    return ket("",0)

  label = ""
  if len(cat1) > 0:
    label = cat1 + ": "         
  result = superposition()      

  try:
    start = int(v1)
    stop = int(v2) + 1           # maybe bug. also in float version!
    step = int(v3)
    for k in range(start,stop,step):
      #result += ket(label + str(k))            # fast_superposition will speed this line up.
      result.data.append(ket(label + str(k)))   # temp hack/fix. Remove when swap in fast_superposition. Made a vast improvement for range(|2>,|50000>)
  except:     
    try:
      start = float(v1)
      stop = float(v2)
      step = float(v3)
      for k in float_range(start,stop,step):
        result += ket(label + "%.2f" % k)      # here too. Though hasn't been an issue yet.
    except:
      return ket("",0)
  return result



# the arithmetic function
# eg: arithmetic(|number: 3>,|symbol: +>,|number: 8>)
# heh. note the "amplification factor"
# of z = x*y directly in python vs what this function does!
# you do get some power in return though.
# and it is still much cheaper than a fully neural model equivalent presumably is.
#
# What I meant by "amplification factor" is the amount of computing power needed to calculate say z = x*y 
# in python, vs the amount if you use this arithmetic function.
#
# x, y superposition bug here too!
# fixed, I hope.
#
def arithmetic(x,operator,y):
  x_label = x if type(x) == str else x.label
  op_label = operator if type(operator) == str else operator.label
  y_label = y if type(y) == str else y.label

  cat1, v1 = x_label.rsplit(': ', 1)
  name, op = op_label.rsplit(': ', 1)
  cat2, v2 = y_label.rsplit(': ', 1)
  if cat1 != cat2 or op not in ['+','-','*','/','%','^']:
    return ket()
  try:
    x = int(v1)
    y = int(v2)
  except ValueError:
    try:
      x = float(v1)
      y = float(v2)
    except ValueError:
      return ket()
  label = ""
  if len(cat1) > 0:
    label = cat1 + ": "      
  if op == '+':
    return ket(label + str(x + y))
  elif op == '-':
    return ket(label + str(x - y))
  elif op == '*':
    return ket(label + str(x * y))
  elif op == '/':
    if y == 0:         # prevent div by zero
      return ket()
    return ket(label + str(x / y))
  elif op == '%':
    return ket(label + str(x % y))
  elif op == '^':
    return ket(label + str(x ** y))
  else:
    return ket()                       # presumably this should never be reached.




# the intersection function.
# if you set foo = min, then it is a generalization of Boolean set intersection.
# if you set foo = max, then it is a generalization of Boolean set union.
# if you set foo = sum, then it is a literal sum.
# if you set foo = mult, then it is a multiplication of the list elements. 
# possibly other useful values of foo too.
# maybe we can do a complement function? if value1 == 0 and value2 != 0, then return value2
# maybe make the label compare case insensitive. Probably not though.
#
# 9/5/2014: I think this could do with some optimization!
# I think ordered-dict and standard dict could probably improve the big-O here by quite a bit!
#
def first_intersection_fn(foo,one,two):
# so that also works with kets:
#  if type(one) == ket:
#    one = superposition() + one
#  if type(two) == ket:
#    two = superposition() + two

# fix bug, where simm(X,X) != 1 if X contains duplicates.
# eg, if X was defined using spell_word() is one example.
# the superposition() + one, should neatly fix this bug! Provided we have auto-collapse on addition.
  one = superposition() + one
  two = superposition() + two

  result = superposition()
  labels = []
  for x in one.data:
    if x.label not in labels:
      labels.append(x.label)
  for x in two.data:
    if x.label not in labels:
      labels.append(x.label)
#  print(labels)
  for label in labels:
    v1 = 0
    for x in one.data:
      if x.label == label:         # instead of direct equality testing,
        v1 = x.value               # maybe use: labels_match(x.label,label) ??
        break                      # probably not.
    v2 = 0
    for x in two.data:
      if x.label == label:
        v2 = x.value
        break
    value = foo(v1,v2)
    result += ket(label,value)
  return result

from collections import OrderedDict
# 4/6/2014 update: Let's try and optimize this puppy!
# BTW, the long term plan is to convert the back-end of the superposition class to ordered dictionaries.
# The problem is I have broken the "hide details in the class" abstraction everywhere, so would take a lot of work to change!
# The other part is we would need a general way to iterate over a superposition.
# Good link: http://www.voidspace.org.uk/python/odict.html
# Heh. Not sure if this is faster or slower!
# But it hints at how the improved superposition class should be written.
def second_intersection_fn(foo,one,two):

  result = superposition()
  
  one_dict = OrderedDict()                     # fast_sp_fix: tweak this once fast_sp is switched in.
  for elt in one:                              # we should be able to really tidy this beast up.
    one_dict[elt.label] = elt.value
    
  two_dict = OrderedDict()
  for elt in two:
    two_dict[elt.label] = elt.value

  merged = OrderedDict()
  merged.update(one_dict)
  merged.update(two_dict)
#  print(merged)
  
  for key in merged:
    v1 = 0
    if key in one_dict:
      v1 = one_dict[key]
    v2 = 0
    if key in two_dict:
      v2 = two_dict[key]

    value = foo(v1,v2)
#    result += ket(label,value)
#    result.data.append(ket(key,value))
    result.add(key, value)
  return result

# 24/1/2015: let's write the intersection_fn version that uses the fast_sp as a backend.
# one and two must be fast_superpositions!
# need to test this .....
# anyway, looks good. Should be much faster.
def fast_sp_intersection_fn(foo,one,two):
  r = fast_superposition()
  merged = OrderedDict()
  merged.update(one.odict)            # yeah, breaking class abstractions again!
  merged.update(two.odict)            # maybe I should just do: one + two
  
  for key in merged:
    v1 = one.get_value(key)
    v2 = two.get_value(key)
    value = foo(v1,v2) 
    r += ket(key,value)
  return r

def superposition_intersection_fn(foo, one, two):
  if type(one) not in [ket, superposition] and type(two) not in [ket, superposition]:
    return superposition()
  r = superposition()
#  merged = OrderedDict()
#  merged.update(one.dict)
#  merged.update(two.dict)
  merged = one + two
  
  for key,value in merged.items():
    v1 = one.get_value(key)
    v2 = two.get_value(key)
    new_value = foo(v1, v2)
    r.add(key, new_value)
  return r

# version to handle sequences too.
def intersection_fn(foo, one, two):   
  if type(one) in [ket, superposition] or type(two) in [ket, superposition]:
    return superposition_intersection_fn(foo, one, two)
  max_len = max(len(one), len(two)) 
  seq = sequence([])
  for k in range(max_len):
    try:                                                 # ugly! But will do for now.
      sp1 = one.data[k]
    except:
      sp1 = ket()
    try:
      sp2 = two.data[k]
    except:
      sp2 = ket()
    r = superposition_intersection_fn(foo, sp1, sp2)
    seq.data.append(r)
#    print('sp1: %s' % sp1)
#    print('sp2: %s' % sp2)    
#    print('r: %s' % r)
  print('seq: %s' % seq)
  return seq


# now the actual intersection:
# NB: intersection is actually one key component of learning.
# Say a child trying to learn the meaning of "apple". 
# They take an intersection of what they were currently thinking everytime their parents say "apple".
# The bit in common (ie, the intersection) most likely is the meaning of "apple".
# Something similar for a dog learning a trick and hearing "good dog".
#
# Let's expand a bit.
# Let's say the superpositions of each time their parents said "apple" are r1, r2, r3, ...,rn
# Then, if not over-specified (ie we get the empty set), meaning-apple might simply be: intersection(r1,r2,...,rn)
#
# 1/5/2014: Alternatively, we can learn using thresholds and sums:
# TF[t5](TF[t1] pattern-1 |dog> + TF[t2] pattern-2 |dog> + TF[t3] pattern-3 |dog> + TF[t4] pattern-4 |dog>) 
#
# I suspect intersection can also be used in language translation (more thought needed!).
# Say you have a good set of sentence pairs in language A and B.
# Then intersection may help in finding the word pairs. Word in A vs same meaning in B.
#
# a union also plays a role in learning, when quite distinct things refer to the same object.
# say if we want |word: frog> and |image: frog> to both trigger the |concept: frog>
def intersection(one,two):
  return intersection_fn(min,one,two).drop()

# now the union:
def union(one,two):
  return intersection_fn(max,one,two)

# potentially we could write a wrapper that maps associative pair functions into triple, quad etc fns.
# eg: assoc_wrapper(fn,pieces)
# where pieces is the list of parametrs to feed to "fn"
#
# the triple intersection:
def tri_intersection(one,two,three):
  return intersection(intersection(one,two),three)

# the triple union:
def tri_union(one,two,three):
  return union(union(one,two),three)


# the complement variable function:
def comp_fn(x,y):
  if x == 0 and y != 0:
    return y
  elif x != 0 and y == 0:
    return x
  else:
    return 0

# now for complement:
def complement(one,two):
  return intersection_fn(comp_fn,one,two)

# test for set membership of |x> in |X>
# this is simple enough, that we probably don't even need this function. Just do it inline.
# Probably a little clearer to do it inline anyway, instead of the one step of indirection.
# 24/1/2015: what about using X.get_value(x.label)?
def set_mbr(x,X,t=1):
  return X.apply_bra(x) >= t

# the delete function:
def del_fn(x,y):    # a possible variant is "return y - x"
  if x != 0:
    return 0
  else:
    return y

def delete(one,two):
  return intersection_fn(del_fn,one,two).drop()  # NB: the .drop()

# OK. Let's write the "return y - x" variant:
def del_fn2(x,y):
  if x <= y:
    return y - x
  else:
    return 0

def delete2(one,two):
  return intersection_fn(del_fn2,one,two).drop()

def mult_fn(x,y):
  return x*y
  
def multiply(one,two):
  return intersection_fn(mult_fn,one,two)
  
def sum_fn(x,y):
  return x + y
  
def addition(one,two):
  return intersection_fn(sum_fn,one,two)
  

def del_fn3(x,y):   # NB: creates negative coeffs.
  return x - y
  
def delete3(one,two):
  return intersection_fn(del_fn3,one,two)
  
def squared_difference(x,y):
  return (x - y)**2

import math
def Euclidean_distance(one,two):
  return ket("number: " + str(math.sqrt(intersection_fn(squared_difference,one,two).count_sum())))

# 11/8/2015: the exclude function:
# exclude(|a> + |c>,|a> + |b> + |c> + |d>) == |b> + |d>
# in quick testing, seems to work.
#
def exclude_fn(x,y):
  if x > 0:
    return 0
  return y
       
def exclude(one,two):
  return intersection_fn(exclude_fn,one,two).drop()

# a superposition version of simm.
# not yet sure how to write the sequence version of simm.
# BTW, simm stands for "similarity metric".
# ie, 1 for exact match
# 0 for exact mismatch
# values in between otherwise.
# in practice it is more of a concept than a single equation.
# but it is the foundation equation for pattern recognition
#
# One interesting use of simm is the Landscape function:
# L(f,x) = simm(f,g(x))
# with a different pattern g(x) at each point x.
# cf. DNA micro-array
# http://en.wikipedia.org/wiki/DNA_microarray
# the landscape fn converts an incoming pattern f into a mathematical surface (in general not a smooth surface though)
#
# A well supported similarity is one that has a high simm score, 
# and A and B have a large number of terms.
# A weakly supported similarity is where A and B have a small number of terms.
# Though on further thought it is not that simple.
# If the kets are "low order", ie close to the input, then you need more of them.
# If the kets are "higher order", ie more abstract, and hence rarer in frequency,
# then each ket carries more meaning.
# 
# Maybe we need a version of simm for kets. Currently simm(a|x>,b|x>) returns 100% 
# independent of the coeffs a and b. 
# Recall we were meant to only use s1*wf == s2*wg if f and g are longer than one element.
# Provided they are not negative, simm for single elts should be: min(a,b)/max(a,b)
#
def simm(A,B):
  print(display(A))
  print(display(B))

  A = superposition() + A
  B = superposition() + B

  one = A.normalize()
  two = B.normalize()

  print(display(one))
  print(display(two))

  result = intersection(one,two)
  print(display(result))
  return result.count_sum()


# a quiet version of simm:
# maybe we should use |A intn B|/|A union B| instead?? 
# Though would need to check it gives the same answer as the current method. 
def silent_simm(A,B):
# handle single kets, where we don't want rescaling to s1*wf == s2*wg
# seems to be working just fine.
  if A.count() <= 1 and B.count() <= 1:
    a = A.ket()
    b = B.ket()
    if a.label != b.label:                    # put a.label == '' test in here too?
      return 0
    a = max(a.value,0)                        # just making sure they are >= 0.
    b = max(b.value,0)
    if a == 0 and b == 0:                     # prevent div by zero.
      return 0
    return min(a,b)/max(a,b)
  return intersection(A.normalize(),B.normalize()).count_sum()

# unscaled simm.
def unscaled_simm(A,B):
  wf = A.count_sum()
  wg = B.count_sum()
  if wf == 0 and wg == 0:
    return 0
  return intersection(A,B).count_sum()/max(wf,wg)
  

# quick test found this is not in [0,1]
#  return intersection(A,B).count_sum()
#
# potentially need a version that is intersection(A,B).count_sum()
# cf: |A intn B|, where intn is the intersection operator, and usually applies to A,B with Boolean values, not float.
# We can emulate the Boolean bit with: intersection(A,B).drop().count()
# though the closest to original simm corresponds to the .normalize() version.

# closer to the original simm[w,f,g], we are going to introduce a weighted simm:
#
# a couple of common use cases are:
# weighted_simm(A,A,B) and weighted_simm(B,A,B)
# or something close to that.
#
def weighted_simm(w,A,B):
  A = multiply(w,A)
  B = multiply(w,B)
  return intersection(A.normalize(),B.normalize()).count_sum()


# a version of simmm that returns: result|simm>
def ket_simm(A,B):
#  result = intersection(A.normalize(),B.normalize()).count_sum()
  result = silent_simm(A,B)
  return ket("simm",result)

def ket_weighted_simm(w,A,B):
  result = weighted_simm(w,A,B)
  return ket("simm",result)
    

# 18/6/2016:
# implement a faster simm.
# simm is often a time sink, so we need to find ways to speed it up.
# note eventually we might be able to implement a parallel version.
# if not simm, then pattern_recognition function in new_context().
#
# OK. In testing in the console it seems to work.
# Not sure if we can make it faster, but I think we are O(n) now. 
def fast_simm(A,B):
#  logger.debug("inside fast_simm")
  if A.count() <= 1 and B.count() <= 1:
    a = A.ket()
    b = B.ket()
    if a.label != b.label:                    # put a.label == '' test in here too?
      return 0
    a = max(a.value,0)                        # just making sure they are >= 0.
    b = max(b.value,0)
    if a == 0 and b == 0:                     # prevent div by zero.
      return 0
    return min(a,b)/max(a,b)
#  return intersection(A.normalize(),B.normalize()).count_sum()

  # now calculate the superposition version of simm, while trying to be as fast as possible:
#  logger.debug("made it here in fast_simm")
  try:
    merged = {}
    one_sum = 0
    one = {}
    for elt in A:
      one[elt.label] = elt.value               # what about empty kets? How does this code handle them?
      one_sum += elt.value                     # assume all values in A are >= 0
      merged[elt.label] = True                 # potentially we could use abs(elt.value)

    two_sum = 0
    two = {}
    for elt in B:
      two[elt.label] = elt.value
      two_sum += elt.value                     # assume all values in B are >= 0
      merged[elt.label] = True

    # prevent div by zero:
    if one_sum == 0 or two_sum == 0:
      return 0

    merged_sum = 0
#    for key in merged:
#      v1 = 0
#      if key in one:
#        v1 = one[key]/one_sum
#      v2 = 0
#      if key in two:
#        v2 = two[key]/two_sum
#      merged_sum += min(v1,v2)
    for key in merged:
      if key in one and key in two:
        v1 = one[key]/one_sum
        v2 = two[key]/two_sum
        merged_sum += min(v1,v2)
    return merged_sum
  except Exception as e:
    logger.debug("fast_simm exception reason: %s" % e)


# 27/3/2014: time to implement the landscape function.
# Hrm... how do I plan on testing it?
#
# Recall the math definition:
# L(f,x) = simm(f,g(x))
#
def landscape(context,pattern,f,x):
  f = f.apply_op(context,pattern)
  g = x.apply_op(context,pattern)
  return silent_simm(f,g)             # or should this be ket_simm()?

# list simm. This is not a ket/sp function at all, but I think it belongs here anyway.
# eg, maybe as background to explain the ket/sp simm() I do have here.
#
# First definition of simm:
# simm(w,f,g) = w*[f - g] + R abs(w*f - w*g)/[w*f + w*g + R abs(w*f - w*g)]
# where one version of a*b is:
# a*b = \Sum_k abs(a_k * b_k)
# And for best results set R = 1.
# This version has the property:
# 0 <= simm(w,f,g) <= 1. 1 for f,g completely disjoint, 0 for f,g exactly identical.
# BTW, this follows from:
# w*[f - g] = w*f + w*g if f,g are completely disjoint (taking into account the effect of w)
# w*[f - g] = 0 if f,g are identical (taking into account the effect of w)
#
# The second version of simm is: 1 - simm(w,f,g)
# w*f + w*g - w*[f - g]/[w*f + w*g + R abs(w*f - w*g)]
# This version has the property:
# 0 <= simm(w,f,g) <= 1. 0 for f,g completely disjoint, 1 for f,g exactly identical.
#
# Both versions have some symmetries (indeed, I tweaked the function to create symmetries, cf physics). I'll type them up later.
# NB: I swap back and forth between these two variations, and call them the same name,
# depending on what I am trying to do.
#
# NB: if a,b >= 0 then:                    # what about if a and or b are < 0?
# a + b + abs(a - b) = 2*max(a,b)
# a + b - abs(a - b) = 2*min(a,b)
#
# w,f,g are lists of ints or floats. They have nothing to do with kets or superpositions!
def list_simm(w,f,g):
  the_len = min(len(f),len(g))
  print("the_len:",the_len)
  print("w:",w)
  print("f:",f)
  print("g:",g)
  print()
# w += [0] * (the_len - len(w))            # from here: http://stackoverflow.com/questions/3438756/some-built-in-to-pad-a-list-in-python
  w += [1] * (the_len - len(w))   
  f = f[:the_len]
  g = g[:the_len]
  print("w:",w)
  print("f:",f)
  print("g:",g)

  wf = sum(abs(w[k]*f[k]) for k in range(the_len))
  wg = sum(abs(w[k]*g[k]) for k in range(the_len))
  wfg = sum(abs(w[k]*f[k] - w[k]*g[k]) for k in range(the_len))
  
  print("wf:",wf)
  print("wg:",wg)
  print("wfg:",wfg)

  
  if wf == 0 and wg == 0:
#    return 0
    result = 0
  else:
    #return (wf + wg - wfg)/(2*max(wf,wg))
    result = (wf + wg - wfg)/(2*max(wf,wg))
  print("result:",result)
  return result

# 17/2/2015: a rescaled version of list simm
# need to test it now!
#
def rescaled_list_simm(w,f,g):
  the_len = min(len(f),len(g))
#  print("the_len:",the_len)
#  print("w:",w)
#  print("f:",f)
#  print("g:",g)
#  print()
# normalize lengths of our lists:
#  w += [0] * (the_len - len(w))            # from here: http://stackoverflow.com/questions/3438756/some-built-in-to-pad-a-list-in-python
  w += [1] * (the_len - len(w))          
  f = f[:the_len]
  g = g[:the_len]
#  print("w:",w)
#  print("f:",f)
#  print("g:",g)

# rescale step, first find size:
  s1 = sum(abs(w[k]*f[k]) for k in range(the_len))
  s2 = sum(abs(w[k]*g[k]) for k in range(the_len))

# if s1 == 0, or s2 == 0, we can't rescale:
  if s1 == 0 or s2 == 0:
    return 0
  
# now rescale:
  f = [f[k]/s1 for k in range(the_len)]  
  g = [g[k]/s2 for k in range(the_len)]  
  
# proceed with algo:
# if rescaled correctly, wf and wg should == 1.
#  wf = sum(abs(w[k]*f[k]) for k in range(the_len))
#  wg = sum(abs(w[k]*g[k]) for k in range(the_len))
  wfg = sum(abs(w[k]*f[k] - w[k]*g[k]) for k in range(the_len))
  
#  print("wf:",wf)
#  print("wg:",wg)
#  print("wfg:",wfg)

# we should never have wf or wg == 0 in the rescaled case:  
#  if wf == 0 and wg == 0:
#    return 0
#    result = 0
#  else:
    #return (wf + wg - wfg)/(2*max(wf,wg))
#    result = (wf + wg - wfg)/(2*max(wf,wg))
  return (2 - wfg)/2
#  print("result:",result)
#  return result


# still can't use this in the console, since the context needs to be passed in too.
# the train-of-though function, or perhaps a better name is "stream of conciousness"
def train_of_thought(context,x,n):
  if type(n) != int:
    try:
      cat,v = extract_category_value(n.the_label())
      n = int(v)
    except:
      return superposition()                # return an empty superposition.

  print("context:",context.name)
  print("x:",x.display())
  print("n:",n)
  X = x.pick_elt()
  print("|X>:",X.display())
  print()
  result = superposition()

  for k in range(n):
    op = X.apply_op(context,"supported-ops").pick_elt()  #   |op> => pick-elt supported-ops |X>
#    print("op:",op.display())
    X = X.apply_op(context,op).pick_elt()                #   |X> => pick-elt apply(|op>,|X>)
#    result += X                            # this version adds repeated elements
    result.data.append(X)                   # this version preserves order
#    print("|X>:",a_ket.display())
    print(X.display())
  return result                             # return a record of the train-of-thought

# 28/7/2014: 
# Let's finally implement console train of thought.
# train-of-thought[n] some-superposition
# eg: train-of-thought[20] |colour: red>
# First up, I want to try it on this data set: http://semantic-db.org/next-gen/train_of_thought.py
# OK. In early testing seems to work just fine.
#
# where n is an int.
def console_train_of_thought(one,context,n):
  try:
    n = int(n)
  except:
    return ket("",0)

  print("context:",context.name)
  print("one:",one)
  print("n:",n)
  X = one.pick_elt()
  print("|X>:",X)
  print()
  result = superposition()

  for k in range(n):
    op = X.apply_op(context,"supported-ops").pick_elt()  #   |op> => pick-elt supported-ops |X>
    X = X.apply_op(context,op).pick_elt()                #   |X> => pick-elt apply(|op>,|X>)
    result.data.append(X)                   
    print(X.display())
  return result                             # return a record of the train-of-thought



# first attempt at the read() function:
# Yeah. For a "naked" read, it is fine.
# I'm going to try for a more active read down lower.
# NB: one should be string or ket.
def read_text(one):
  label = one.label if type(one) == ket else one

  cat, text = extract_category_value(label)
  if cat != "text":
    return ket("")
# for now, comment this out.
#  print("text:",text)

#  text = text.lower().split()  # need more processing. Leading and trailing ", plus handle punctuation, etc.
# see here: http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
#  text = text.lower().translate(string.maketrans("",""), string.punctuation).split()
# fix here: http://www.gossamer-threads.com/lists/python/python/1053035
#  text = text.lower().translate(str.maketrans("","",string.punctuation)).split()
#  print("text:",text)
# 17/6/2014 update:
# keep case version:
#  text = "".join(c for c in text if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\'- ').split()
# convert to lower case version:
  text = "".join(c for c in text.lower() if c in 'abcdefghijklmnopqrstuvwxyz\'- ').split()

  result = superposition()
# this version sums up repeated words. Sometimes useful, sometimes not.
#  for w in text:
#    result += ket("word: " + w)
#
# alternatively, this variant. This one does not add up the words, while the += version does.
# Hence, this is closer to how the sequence version would work.
# Heh, that is if I ever write the sequence version :)
  result.data = [ket("word: " + w) for w in text]                                # isn't this fundamentally broken!!!
  return result

# note the almost identical structure to read_text().
# This is not a coincidence, and hints that this structure is very common
# and operates at various levels in the brain.
def spell_word(one):
  label = one.label if type(one) == ket else one

  cat, word = extract_category_value(label)
  if cat != "word":
    return ket("")

  result = superposition()          # later when we finally implement sequence, use sequence() here.
  result.data = [ket("letter: " + c) for c in word]
  return result


# 29/1/14, let's put in a collapse_read_text() here, eg, for the frequency of words thing.
def collapse_read_text(one):
  label = one.label if type(one) == ket else one

  cat, text = extract_category_value(label)
  if cat != "text":
    return ket("",0)
#  print("text:",text)
# don't keep case version:
  text = text.lower().translate(str.maketrans("","",string.punctuation)).split()
# keep case for now:
#  text = text.translate(str.maketrans("","",string.punctuation)).split()

  result = superposition()
  for w in text:
    result += ket("word: " + w)
  return result
  


# code from here:
# http://stackoverflow.com/questions/16996217/prime-factorization-list  
# pretty sure this is wrong! Yup! Broken!!
# x = number: 98712948751984751983471953871983475198347519475
# returns: |number: 5> + 34.000|number: 8> + |number: 19> + |number: 653> + |number: 313817949986>
# since when is 8 a prime?
# ditto: 313817949986
def broken_primes(n):
  factors = []
  d = 2
  while d*d <= n:
    while (n % d) == 0:
      factors.append(d)  # supposing you want multiple factors repeated
      n /= d
    d += 1
  if n > 1:
    factors.append(n)
  return factors

def another_broken_primes(n):
  print("n:",n)
  f, fs = 3, []
  while n % 2 == 0:
    fs.append(2)
    n /= 2
  while f * f <= n:
    while n % f == 0:
      fs.append(f)
      n /= f
    f += 2
  if n > 1: fs.append(n)
  print("factors:",fs)
  return fs
  
def primes(n):
  print("n:",n)
  f, fs = 3, []
  while n % 2 == 0:
    fs.append(2)
    n //= 2                 # this is the fix.
  while f * f <= n:
    while n % f == 0:
      fs.append(f)
      n //= f               # and this too.
    f += 2
  if n > 1: fs.append(n)
  print("factors:",fs)
  return fs  

# returns |yes> if |x> is a prime, else |no>
def is_prime(x):
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket("",0)
  try:
    n = int(v)
  except:
    return ket("",0)
  if n <= 1:
    return ket("",0)
  
  if n == primes(n)[0]:
    return ket("yes")
  else:
    return ket("no")
  

# the factor number function
# eg: factor |number: 30>  returns |number: 2> + |number: 3> + |number: 5>
# interestingly, you could use this to find in a completely different space,
# a set of objects that have the identical factor structure as positive integers.
# a weird kind of duality between primes and that other space.
# or I guess, an isomorphism.
#                                                                                              
# Though I guess that is a general idea.
# An example is say the network structure of your friends network
# can be identical to say the network structure of a certain set of websites.
# The only differentiator is the ket labels of the components.
# This also has the implication that reconstructing meaning
# just from a (local) network of neurons is essentially impossible.
# Without broader knowledge, the network could represent pretty much anything!
# x must be a ket! Or it bugs out in wierd ways.
def factor_number(x):
  value = x.value if type(x) == ket else 1
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket("",0)
  try:
    n = int(v)
  except:
    return ket("",0)
  if n <= 1:
    return ket("",0)

  result = superposition()
  for p in primes(n):
    result += ket("number: " + str(p),value)
  return result


# this one handles superpositions too!
# bug, it chomps coefficients. Look into it later. Fixed in factor_number(x). See value = x.value ...
# 24/1/2015: I have no idea why I wrote this function.
# Seems completely pointless.
# chomped it out of the fn_table2 table, and put in factor_number(x), NB no s at the end.  
def factor_numbers(x):  # NB: the plural, the 's.
  if type(x) == ket:
    return factor_number(x)
  if type(x) == superposition:
    result = superposition()
    for v in x.data:
      result += factor_number(v)
    return result

# 24/1/2015: I have no idea the point for these next two functions!
# I guess I wrote them when I was a newb.    
# this is a general idea (have ket code mapped to handle superpositions too).
# So:
def old_ket_superposition(fn,x):
  if type(x) == ket:
    return fn(x)
  if type(x) == superposition:
    result = superposition()
    for v in x.data:
      result += fn(v)
    return result

# try again:
def ket_superposition(fn,x):
  result = superposition()
  if type(x) == ket:
    result += fn(x)
  if type(x) == superposition:
    for v in x.data:
      result += fn(v)
  return result


# 24/1/2015: this this is weird and boring!
# Now, some weird maths thing. 
# A kind of "number is near", based on digits.
# Yeah, hard-wired to base 10 for now.
# eg: 70 is near: 80,60 and 71,79
def near_number(x):
  value = x.value if type(x) == ket else 1
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket(x_label,value)
  try:
    n = int(v)                 # test for valid int. Don't actually use n.
  except:
    return ket(x_label,value)

  digits = [int(c) for c in v ]
  result = superposition()
  for k,d in enumerate(digits):
    d1 = (d + 1) % 10
    d2 = (d - 1) % 10

    tmp = copy.copy(digits)
    tmp[k] = d1
    s = ''.join(str(n) for n in tmp)
    result += ket("number: " + s,value)

    tmp = copy.copy(digits)
    tmp[k] = d2
    s = ''.join(str(n) for n in tmp)
    result += ket("number: " + s,value)
  return result

# the handle superpositions version:
def near_numbers(x):
  return ket_superposition(near_number,x)


# update: google found this: http://mathworld.wolfram.com/SumofPrimeFactors.html
# This is a thing I call a strange int.
# Say r has prime factorisation:
# r = p1^n1 * p2^n2 * p3^n3 * p4^n4 * ...
# Then strange_int(r) = p1*n1 + p2*n2 + p3*n3 + p4*n4 + ...
# This is just one of a range of results from doing the simple mapping:
# a^b to a*b
# c*b to c + b
#
# A couple of things to mention:
# 1) strange_int(p) == p, when p is prime, or p == 4.
# 2) If p is neither prime or 4, then strange_int(p) < p
# 3) Hence, there exists a finite positive integer k such that
# strange-int^k |x> == |p>, where p is a prime (or 4).
# and by (1), strange-int^(k+1) |x> == |p> 
def strange_int(x):
  value = x.value if type(x) == ket else 1
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket(x_label,value)
  try:
    n = int(v)   
  except:
    return ket(x_label,value)
  if n <= 1:
    return ket(x_label,value)
  
  return ket("number: " + str(sum(primes(n))))


# find the strange-int-prime.
# ie, |p> such that strange-int^k |x> == |p>
def strange_int_prime(x):
  value = x.value if type(x) == ket else 1
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket(x_label,value)
  try:
    n = int(v)
  except:
    return ket(x_label,value)
  if n <= 1:
    return ket(x_label,value)

  next = sum(primes(n))
  while n != next:
    n = next
    next = sum(primes(n))

  return ket("number: " + str(n))


# find the strange-int-depth.
# ie, smallest k such that strange-int^k |x> == |p>
def strange_int_depth(x):
  value = x.value if type(x) == ket else 1
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket(x_label,value)
  try:
    n = int(v)
  except:
    return ket(x_label,value)
  if n <= 1:
    return ket(x_label,value)

  k = 0
  next = sum(primes(n))
  while n != next:
    n = next
    next = sum(primes(n))
    k += 1

  return ket("number: " + str(k))


# find the strange-int-delta
# ie, |x> - strange-int |x>
def strange_int_delta(x):
  value = x.value if type(x) == ket else 1
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket(x_label,value)
  try:
    n = int(v)
  except:
    return ket(x_label,value)
  if n <= 1:
    return ket(x_label,value)

  r = n - sum(primes(n))
  return ket("number: " + str(r))


# find the strange-int-list
# ie, |x> + strange-int |x> + strange-int^2 |x> + ...
def strange_int_list(x):
  value = x.value if type(x) == ket else 1
  x_label = x.label if type(x) == ket else x

  cat, v = extract_category_value(x_label)
  if cat != "number":
    return ket(x_label,value)
  try:
    n = int(v)
  except:
    return ket(x_label,value)
  if n <= 1:
    return ket(x_label,value)

  result = superposition()
  result += ket("number: " + str(n))
#  result += ket(str(n))
  next = sum(primes(n))
  while n != next:
    n = next
    next = sum(primes(n))
    result += ket("number: " + str(n))
#    result += ket(str(n))

  return result



import math
# the frequency class equation:
# see: http://en.wikipedia.org/wiki/Frequency_list
def frequency_class(e,X):

  X = X.drop()              # filter out elements <= 0
  smallest = X.find_min_coeff()
  largest = X.find_max_coeff()
  f = X.find_value(e)

  print("e:",e)
  print("largest:",largest)
  print("value:",f)

# need a check in here that f > 0.
# Indeed, largest > 0 too.

  if largest <= 0:
    return 1

  if f <= 0:      # what happens if smallest == 0?? X.drop() means largest == 0 too, hence already returned 1.
    return math.floor(0.5 - math.log(smallest/largest,2)) + 1

  return math.floor(0.5 - math.log(f/largest,2))


# the normalized frequency class equation.
# result is in [0,1]
# 1 for exact match, 0 for not in set.
#
# works great! Indeed, it is a bit like a fuzzy set membership function.
# eg, if all coeffs in X are equal, it gives Boolean 1 for membership, and 0 for non-membership.
# and if the coeffs are not all equal, then it has fuzzier properties.
#
# 25/7/2014 note: Hrmm... I wonder if we can tweak this.
# Currently you only get 20 odd different classes using the frequency class equation.
# Is there a version that gives more graduations?
# Though in practice this is usually not an issue.
# It will almost certainly be of form foo(current/largest)
#
# e is a ket, X is a superposition
# for best effect X should be a frequency list
def normed_frequency_class(e,X):
  e = e.ket()                                  # make sure e is a ket, not a superposition, else X.find_value(e) bugs out.
  X = X.drop()                                 # drop elements with coeff <= 0
  smallest = X.find_min_coeff()                # return the min coeff in X as float
  largest = X.find_max_coeff()                 # return the max coeff in X as float
  f = X.find_value(e)                          # return the value of ket e in superposition X as float

  if largest <= 0 or f <= 0:                   # otherwise the math.log() blows up!
    return 0

  fc_max = math.floor(0.5 - math.log(smallest/largest,2)) + 1  # NB: the + 1 is important, else the smallest element in X gets reported as not in set.
#  print("fc_max: ",fc_max)
#  print("max log:",math.log(smallest/largest,2))
#  print("max val:",0.5 - math.log(smallest/largest,2))
#  print("ret log:",math.log(f/largest,2))
#  print("ret val:",0.5 - math.log(f/largest,2))
  return 1 - math.floor(0.5 - math.log(f/largest,2))/fc_max


# OK. I think this is the time sink with my MtT.
# If we assume X[1] is the largest, and X[-1] is smallest,
# then we don't need find_min and find_max.
# I didn't time it, but it felt no faster....
def faster_normed_frequency_class(e,X):
  X = X.drop()
#  smallest = X.find_min_coeff()
#  largest = X.find_max_coeff()
  smallest = X.select_elt(-1).value   # bug if X is empty??
  largest = X.select_elt(1).value
 
  f = X.find_value(e)

  if largest <= 0 or f <= 0:
    return 0

  fc_max = math.floor(0.5 - math.log(smallest/largest,2)) + 1
  return 1 - math.floor(0.5 - math.log(f/largest,2))/fc_max


# 19/3/2015:
# e is a ket, X is a superposition
# for best effect X should be a frequency list
def ket_normed_frequency_class(e,X):
  result = normed_frequency_class(e,X)
  return ket("nfc",result)


# describe this later ...
# Heh. Structure wise, this is remarkably similar to pattern_recognition().
# BTW, perhaps S should be a superposition instead of a list?
#
# I think this should be tidied up and most probably put in new_context next to pattern-recognition.
# Also fix the hardwiring of "list".
#
# This is now deprecated, but leaving it here because a couple of my scripts.
# See new_context.map_to_topic(e,"list") for the improved version.
def map_to_topic(context,e,S):
  result = superposition()
  for X in S:
#    print("X:",X)
    data = context.recall("list",X)
    value = normed_frequency_class(e,data)
#    value = faster_normed_frequency_class(e,data)  # doesn't seem any faster.
#    result += ket(X.label,value)
    result.data.append(ket(X.label,value))         

#  return result.normalize(100)
# NB: .normalize(100) is a key component of this function.
# Half the magic is in nfc(), the other half in normalize(100).
  return result.drop().normalize(100).coeff_sort()



# let's see if we can do some simple algebra in BKO.
# a|x> + b|y> => a|x> + b|y>
def algebra_add(one,two):
  return one + two

# 10/4/2014 new:
def algebra_subtract(one,two):
  return delete3(one,two) 

def old_algebra_mult(one,two,Abelian=True):
  one = superposition() + one  # hack so one and two are definitely sp, not ket
  two = superposition() + two

  result = superposition()
  for x in one.data:
    for y in two.data:
      print("x*y",x,"*",y)
      labels = x.label.split('*') + y.label.split('*')
      if Abelian:  
        labels.sort()
      label = "*".join(labels)
      result += ket(label,x.value * y.value)
  return result

# maps ket -> ket
# to-number 3|x> == 3|x>
# to-number |number: 7.2> == 7.2| >  # NB: the space in the ket label.
# to-number 2|number: 3> == 6| >     # We can't use just |> because it is dropped all over the place!
# to-number 8|number: text> == 0| >  # so the maths eqn: 3a + 7
# to-number |3.7> == 3.7| >          # in my notation is 3|a> + 7| >
# to-number 3|5> == 15| >
def old_category_number_to_number(one):         # find better name!
  one = one.ket()
  cat, value = extract_category_value(one.label)
  if cat != 'number':
    return one
  try:
    n = float(value)
  except:
    return ket(" ",0)
  return ket(" ",one.value * n)

# 26/3/2016:
# so that algebra() can handle rationals too.
# copied from here: 
# http://stackoverflow.com/questions/575925/how-to-convert-rational-and-decimal-number-strings-to-floats-in-python
#
def parse_float_string(x):
    parts = x.split('/', 1)
    if len(parts) == 1:
        return float(x)
    elif len(parts) == 2:
        return float(parts[0])/float(parts[1])
    else:
        raise ValueError

def category_number_to_number(one):         # find better name!
  one = one.ket()
  cat, value = extract_category_value(one.label)
  try:
#    n = float(value)
    n = parse_float_string(value)    
  except:
    if cat == 'number':                     # not 100% want to keep these two lines
      return ket(" ",0)
    return one
  return ket(" ",one.value * n)


# a|x> * b|y> => a*b |x*y>
#
def algebra_mult(one,two,Abelian=True):
  one = superposition() + one  # hack so one and two are definitely sp, not ket
  two = superposition() + two

  result = superposition()
  for x in one.data:
    x = category_number_to_number(x)  
    for y in two.data:
      y = category_number_to_number(y)
      print("x*y",x,"*",y)
      labels = [ L for L in x.label.split('*') + y.label.split('*') if L.strip() != '' ]
      if Abelian:  
        labels.sort()
      label = "*".join(labels)
      if label == '':         # we can't have ket("",value), since it will be dropped.
        label = " "
      result += ket(label,x.value * y.value)
  return result

# (a|x> + b|y>)^|n>
# eg: (|a> + |b> + |c>)^|2> = |a*a> + 2.000|a*b> + 2.000|a*c> + |b*b> + 2.000|b*c> + |c*c>
def old_algebra_power(one,two):
  one = superposition() + one
  two_label = two.ket().label
  null, power = extract_category_value(two_label)
  try:
    n = int(power)
  except:
    return ket("",0)

  if n <= 0:
    return ket("1")

  result = one                         
  for k in range(n - 1):
    result = algebra_mult(result,one)
  return result

def algebra_power(one,two,Abelian=True):
  one = superposition() + one
  two = category_number_to_number(two)
  try:
    n = int(two.value)
  except:
    return ket(" ",0)

  if n <= 0:
    return ket(" ",1)

  result = one
  for k in range(n - 1):
    result = algebra_mult(result,one,Abelian)
  return result

# implement basic algebra:
def algebra(one,operator,two,Abelian=True):
  op_label = operator if type(operator) == str else operator.the_label()
  null, op = extract_category_value(op_label)

  if op not in ['+','-','*','^']:
    return ket(" ",0)

  if op == '+':                                        # drop_zero() added so that terms with coeff 0 are dropped.
    return algebra_add(one,two).drop_zero()            # Abelian option here too?
  elif op == '-':
    return algebra_subtract(one,two).drop_zero()       # ditto.
  elif op == '*':
    return algebra_mult(one,two,Abelian).drop_zero()
  elif op == '^':
    return algebra_power(one,two,Abelian).drop_zero()
  else:
    return ket(" ",0)

# 2/2/2015: finally wire in non Abelian algebra:
def non_Abelian_algebra(one,operator,two):
  return algebra(one,operator,two,False)  

# simple complex number mult:
def complex_algebra_mult(one,two):
  one = superposition() + one  # hack so one and two are definitely sp, not ket
  two = superposition() + two

  result = superposition()
  for x in one.data:
    for y in two.data:
      if x.label == 'real' and y.label == 'real':
        result += ket("real",x.value * y.value)

      if x.label == 'real' and y.label == 'imag':
        result += ket("imag",x.value * y.value)

      if x.label == 'imag' and y.label == 'real':
        result += ket("imag",x.value * y.value)

      if x.label == 'imag' and y.label == 'imag':
        result += ket("real",-1 * x.value * y.value)
  return result


# convert decimal number to base b.
# eg, b = 2, we have:
# |10> => |2> + |8>
# |7> => |1> + |2> + |4>
#
# number, base need to be kets. category_number_to_number() should take care of that.
def decimal_to_base(number,base):
  r = int(category_number_to_number(number).value)
  b = int(category_number_to_number(base).value)
#  print("r:",r)
#  print("b:",b)
  current_base = 1
  result = superposition()
  while r > 0:
    rem = r%b
    r //= b
    result += ket(str(current_base),rem)
    current_base *= b
  return result  


# here is a fun one. 
# just a test function really for stored_rules().
def shout(one):
  string = (one if type(one) == str else one.the_label()).upper()
  print(string)
  return ket(string)
  #return ket("",0) 
    

# the discrimination function.
# returns the difference between largest coeff, and second largest coeff.
# discrim (90|x> + 55|y>)
# should return 35| >
#
# I now think this should be moved to ket/sp classes.
# Done. This is now deprecated.
# Alternatively, remove from ket/sp and put in "sp_fn_table" -- see the processor.
def discrimination(one):
  result = 0
  if type(one) == ket:
    result = one.value
  elif len(one.data) == 0:
    result = 0
  elif len(one.data) == 1:
    result = one.data[0].value
  else:
    one = one.coeff_sort()
    result = one.data[0].value - one.data[1].value
  return ket(" ",result)



# lets do some temp conversion, as seen here:
# http://semantic-db.org/temperature-conversion.sw
# NB: inline code as seen on that page is a long way off!
# Hrmm... wondering if we want full names too. Celsius, Kelvin, Fahrenheit, or just the single letters?
# Should be easy enough. Just temperature_type[0] == 'C' and so on. Done.
# Is there any way to compact the logic down a bit?
def to_temperature_type(one,convert_to_type='C'):      # I'm Aussie, so default is C.
  print("one:",one)
  p = one.the_label().split(": ")                    
  if len(p) < 2:                                       # check for p[-2] out of index
    return ket("",0)
  try:
    t = float(p[-1])
  except:
    return ket("",0)
  label = ": ".join(p[:-2] + [convert_to_type])
  label += ": "
  temperature_type = p[-2]
  if convert_to_type[0] == 'F':
    if temperature_type[0] == 'F':
      pass
    elif temperature_type[0] == 'C':
      t = t*9/5 + 32
    elif temperature_type[0] == 'K':
      t = t*9/5 - 459.67
    else:
      return ket("",0)
  
  elif convert_to_type[0] == 'C':
    if temperature_type[0] == 'F':
      t = (t - 32)*5/9
    elif temperature_type[0] == 'C':
      pass
    elif temperature_type[0] == 'K':
      t = t - 273.15
    else:
      return ket("",0)
  
  elif convert_to_type[0] == 'K':
    if temperature_type[0] == 'F':
      t = (t + 459.67)*5/9
    elif temperature_type[0] == 'C':
      t = t + 273.15
    elif temperature_type[0] == 'K':
      pass
    else:
      return ket("",0)
  else:
    return ket("",0)
  return ket(label + "%.2f" % t)

  
def to_Fahrenheit(one):
#  return to_temperature_type(one,'Fahrenheit')
  return to_temperature_type(one,'F')

def to_Celsius(one):
  return to_temperature_type(one,'C')  
  
def to_Kelvin(one):
  return to_temperature_type(one,'K')
  

# for now just km, m, and mi, but potential for a whole mess. mm, inches, cm, etc.
# Also, is there a neater way to do this?
def to_distance_type(one,convert_to_type='km'):      # I'm Aussie, so default is km
  print("one:",one)
  p = one.the_label().split(": ")               
  if len(p) < 2:                                       # check for p[-2] out of index
    return ket("",0)
  try:
    x = float(p[-1])
  except:
    return ket("",0)
  label = ": ".join(p[:-2] + [convert_to_type])
  label += ": "
  distance_type = p[-2]
  if convert_to_type == 'km':
    if distance_type == 'km':
      pass
    elif distance_type == 'm':
      x = x/1000
    elif distance_type == 'miles':
      x = x*1.609344                  # yeah, over precission!
    else:                             # from here: http://en.wikipedia.org/wiki/Mile#Comparison_table
      return ket("",0)
  
  elif convert_to_type == 'm':
    if distance_type == 'km':
      x = x*1000
    elif distance_type == 'm':
      pass
    elif distance_type == 'miles':
      x = x*1609.344
    else:
      return ket("",0)
  
  elif convert_to_type == 'miles':
    if distance_type == 'km':
      x = x/1.609344
    elif distance_type == 'm':
      x = x/1609.344
    elif distance_type == 'miles':
      pass
    else:
      return ket("",0)
  else:
    return ket("",0)
  return ket(label + "%.3f" % x)
  
def to_km(one):
  return to_distance_type(one,'km')
  
def to_meter(one):                       # yeah, went for US spelling here.
  return to_distance_type(one,'m')

def to_mile(one):
  return to_distance_type(one,'miles')


# smooth[dx] a|x: 3> => a/4 |x: 3 - dx> + a/2 |x: 3> + a/4 |x: 3 + dx>
# (where dx is an int or float)
# Heh. It works. But let's just say it is sloooow....
# Probably too slow for production use, as is.
# Really need a version that applies to lists of floats, 
# with none of the this back and forth with kets, and str() and junk.
# HRmm... in further testing, the speed seems fine. Just a glitch in the matrix I suppose.
#
# What about this tweak: smooth[dx,k] |x: 100>
# instead of the current: smooth[dx]^k |x: 100>
# Yup. Good idea. Problem is, not currently obvious to me how to do it!
#
# Note, BTW. This thing converges on a Guassian smooth if you apply it enough times.
# Even smooth[d]^10 |x> should be well on the way to a Gaussian/bell curve.
def smooth(one,dx):
  one = one.ket()
  coeff = one.value
  label, value = extract_category_value(one.label)
  if len(label) > 0:
    label += ": "
  try:
    dx = float(dx)
    x = float(value)
  except:
#    return ket(one.label,one.value)    # possible alternative
    return ket("",0)
#  return ket(label + str(x - dx),coeff/4) + ket(label + str(x),coeff/2) + ket(label + str(x + dx),coeff/4) 
  # hrmm... in float world, not guaranteed to work as expected ....
  return ket(label + float_to_int(x - dx),coeff/4) + ket(label + float_to_int(x),coeff/2) + ket(label + float_to_int(x + dx),coeff/4)  


# we need this for read_letters, and read_words, maybe other things in the future too.
def extract_letters(x):
  if x.startswith("letter: "):
    return x[8:]
  if x.startswith("word: "):
    return x[6:]
  return ""
  
# maybe this should be shifted closer to spell and read, but here will do for now.
# I'm looking at the inverse of spell really.
# so read-letters spell |word: frog> => |word: frog>
#
# Currently "one" must be a superposition.
# We need to fix this at some stage! Fixed.
def read_letters(one):
  w = "".join(extract_letters(x.label) for x in one)
  if len(w) == 0:
    return ket("",0)
  return ket("word: " + w)

# a full implementation of this would do capitilization and i to I, and a bunch of other stuff!
# maybe I should put extract_letters() outside of these two functions?
#
# some examples from the console:
# sa: read-words (|word: fish> + |word: dog>)
# |text: fish dog>
#
# sa: read-words (|letter: I> + |word: don't> + |word: give> + |letter: a> + |word: fish>)
# |text: I don't give a fish>
#
# sa: read-words (read |text: I don't give a fish>)
# |text: i dont give a fish>
#
# Fixed, so read-words doesn't have to be in the table of functions with 1 parameter.
# It is now in apply_sp_fn table.
# so now can do:
# sa: read-words read |text: I don't give a fish>
# |text: i dont give a fish>
# ie, we don't need to wrap the read |text: ... in brackets.
def read_words(one):
  w = " ".join(extract_letters(x.label) for x in one)
  if len(w) == 0:
    return ket("",0)
  return ket("text: " + w)

# merge labels
# merge-labels (|fish> + |soup>) returns |fishsoup>
def merge_labels(one):
  w = "".join(x.label for x in one)
  return ket(w)
  
     

# a thing called active read.
# returns results from read_text, and word.apply_op(context,"")
def first_active_read_text(context,one):
  result = superposition()
  for x in read_text(one).data:
 #   result += x
    result += x.apply_op(context,"")
  return result

#  def pattern_recognition(self,pattern,op="pattern",t=0)
    
def second_active_read_text(context,one):
  result = superposition()
  data = read_text(one).data
  for k in range(len(data) - 1):
    y1 = data[k]
    print("y1:",y1)
    tmp1 = context.pattern_recognition(y1,"")
    print("tmp1:",tmp1)
    result += tmp1.drop_below(1)                       # ie, looking for exact match.
    
    y2 = data[k] + data[k + 1]
    print("y2:",y2)
    tmp2 = context.pattern_recognition(y2,"")
    print("tmp2:",tmp2)
    result += tmp2.drop_below(1)                       # again, drop_below(1) is for an exact match.
  y1 = data[-1]
  print("y1:",y1)
  tmp1 = context.pattern_recognition(y1,"")
  print("tmp1:",tmp1)
  result += tmp1.drop_below(1)

  return result
  
def active_read_text(context,one):
  result = superposition()
  data = read_text(one).data
  for k in range(len(data)):
    y1 = data[k]
    print("y1:",y1)
    tmp1 = context.pattern_recognition(y1,"")
    print("tmp1:",tmp1)
    result += tmp1.drop_below(1)                       # ie, looking for exact match.
    
    if k < len(data) - 1:
      y2 = data[k] + data[k + 1]
      print("y2:",y2)
      tmp2 = context.pattern_recognition(y2,"")
      print("tmp2:",tmp2)
      result += tmp2.drop_below(1)                       # again, drop_below(1) is for an exact match.

  return result

# hrmmm is one ket or sp?
# It is whatever type that read_text() can handle.
# quick look there says: ket or string. 
def silent_active_read_text(context,one,pattern=""):
  result = superposition()
  data = read_text(one).data
  for k in range(len(data)):
    y1 = data[k]
    result += context.pattern_recognition(y1,pattern).drop_below(0)  # hrmm.. maybe we don't need drop_below(1)?
                                                                # instead of deleting the drop_below, I just 
    if k < len(data) - 1:                                       # inactivated it by setting to 0.
      y2 = data[k] + data[k + 1]                         # this line corresponds to my "buffer" idea. Explain later!
      result += context.pattern_recognition(y2,pattern).drop_below(0)

  return result

# try and implement my active buffer idea:
# the idea is that as you input data you try and pattern match it against what you know.
# it is a generalisation of the active_read() idea.
# And I imagine it will be very useful indeed. But that is for later.
#
# fn needs to return a superposition, else code breaks.
# N is the number of elements in the buffer. 
# Usually <= 7, I'm guessing (based on short term memory with 7 +-2 items), though that depends on how low or high level we are working at. Lower generally implies larger N.
# pattern is the pattern label we are looking for.
# t is the drop-below threshold.
#
# We need to test this beast!
def active_buffer(context,fn,one,N,pattern="",t=0):
  result = superposition()
  data = fn(one).data
  for k in range(len(data)):
    for n in range(N):
      if k < len(data) - n:
        y = superposition()
        y.data = data[k:k+n+1]                              
        result += context.pattern_recognition(y,pattern).drop_below(t)
  return result        

# added 27/6/2014:
# active-buffer[N,t] some-superposition             -- uses "" as the default pattern.
# active-buffer[N,t,pattern] some-superposition     -- uses your chosen pattern (we can't use "" as the pattern, due to broken parser!)
# eg: active-buffer[3,0] read |text: I want french waffles>
# where: 
# N is an int                                       -- the size of the active buffer  
# t is a float                                      -- the drop below threshold
# pattern is a string                               -- the pattern we are using
#
# Maybe a version that preserves currency?
# Just using currency = one.count_sum(), then return result.normalize(currency)
def console_active_buffer(one,context,parameters):  # one is the passed in superposition
  try:
    N,t,pattern = parameters.split(',')
    N = int(N)
    t = float(t)
  except:
    try:
      N,t = parameters.split(',')
      N = int(N)
      t = float(t)
      pattern = ""
    except:
      return ket("",0)
  
  one = superposition() + one                      # make sure one is a superposition, not a ket.    
  result = superposition()                         # Need cleaner way to handle the ket/sp problem, really.
  data = one.data                                  # Maybe a unified iterator in the background?
  for k in range(len(data)):                       # so x in one: instead of x in one.data:
    for n in range(N):                             # though here we do need the list, not just an iterator.
      if k < len(data) - n:
        y = superposition()
        y.data = data[k:k+n+1]                      # this is the bit you could call the buffer.        
        result += context.pattern_recognition(y,pattern).drop_below(t)
  return result        



#
# the idea:
# |x> => "x"
# |x> + |y> => "x and y"
# |x> + |y> + |z> => "x, y and z"
# |x> + |y> + |z> + |p> => "x, y, z and p"
#
# Here is one common usage:
# sa: friends |person: Eric>
# |person: Fred> + |person: Sam> + |person: Harry> + |person: Mary> + |person: liz>
#
# sa: list-to-words extract-value friends |person: Eric>
# |text: Fred, Sam, Harry, Mary and liz>
#
# sa: extract-value list-to-words extract-value friends |person: Eric>
# |Fred, Sam, Harry, Mary and liz>
#
# Update: for now I have dropped the "text: " prefix.  
# 9/8/2015: update: maybe have an: "or" variant. So |x> + |y> + |z> => "x, y or z"
#
def sp_to_words(one):
  labels = [x.label for x in one]
  if len(labels) == 0:
    return ket("",0)               # maybe something else instead of this?
  if len(labels) == 1:
    result = labels[0]
  else:
    head = ", ".join(labels[:-1])
    tail = labels[-1]
    result = head + " and " + tail
#  return ket("text: " + result)
  return ket(result)

# 12/9/2016
# let's implement the inverse of list-to-words
# sa: words-to-list |a, b, c, d and e> 
# |a> + |b> + |c> + |d> + |e> 
# this will be the first very, very early step towards parsing incoming English into back-end BKO
# That would need a LOT of thinking time though. 
#
# one is a ket
def words_to_sp(one):
  try:
    head, tail = one.label.split(' and ')
    front = head.split(', ')
    r = superposition()
    for x in front + [tail]:
      #r.data.append(ket(x))                        # yeah, breaking the class abstraction again. Later swap in: r += ket(x)
      r += ket(x)
    return r
  except Exception as e:
    logger.debug("words-to-list exception reason: " + str(e))
    return one   


# Hrmm.. sp_to_words() is an implementation of list-to-words.
# Now I need its brother, number-to-words.
# eg: 
# number-to-words |number: 7> => |text: seven>
# number-to-words |number: 35> => |text: thirty five>
# number-to-words |number: 137> => |text: one hundred and thirty seven>
# number-to-words |number: 8,921> => |text: eight thousand, nine hundred and twenty one>
# number-to-words |number: 54,329> => |text: fifty four thousand, three hundred and twenty nine>
# number-to-words |number: 673,421> => |text: six hundred and seventy three thousand, four hundred and twenty one>
# number-to-words |number: 3,896,520> => |text: three million, eight hundred and ninety six thousand, five hundred and twenty>  
#
# I think something here should do the job:
# http://stackoverflow.com/questions/8982163/how-do-i-tell-python-to-convert-integers-into-words
def number_to_words(one):
  result = superposition()
  # details ...
  


# 13/4/2014:
# Let's add an if/else statement to BKO.
# Motivated by recursion works without even trying (though vastly inefficient at the moment).
# So seems sensible to add if/else too.
#
# bko_if(|True>,|a>,|b>)  -- returns |a>
# bko_if(|False>,|c>,|d>) -- returns |d>
def bko_if(condition,one,two):
  if condition.the_label().lower() in ["true","yes"]:
    return one
  else:
    return two

# 14/12/2014:
# Let's add a weighted if to BKO.
# eg: wif(0.7|True>,|a>,|b>)
# returns: 0.7|a> + 0.3|b>
# and
# wif(0.8|False>,|a>,|b>)
# returns: 0.2|a> + 0.8|b> 
# assumes the coeff of True/False is in [0,1] otherwise we get negative coeffs.
# though we can filter those using drop().
# 
def weighted_bko_if(condition,one,two):
  condition_ket = condition.ket()
  label = condition_ket.label 
  value = condition_ket.value 
  if label.lower() in ["true","yes"]:
    return one.multiply(value) + two.multiply(1 - value)
  else:
    return one.multiply(1 - value) + two.multiply(value)     

  
# 8/5/2014:
# common[op] (|x> + |y> + |z>)
# eg: common[friends] (|Fred> + |Sam>)
# eg: common[actors] (|movie-1> + |movie-2>)
# or indirectly
# |list> => |Fred> + |Sam> + |Charles> 
# common[friends] "" |list>
def common(one,context,op):
  if len(one) == 0:
    return ket("",0)
  for sp in one:
    r = sp.apply_op(context,op)
    break
  for sp in one:
    tmp = sp.apply_op(context,op)
    r = intersection(r,tmp)
  return r                 


# 24/9/2015:
# union[op] (|x> + |y> + |z>)  -- maybe needs a better name. I'm not sure the English counterpart.
#
def operator_union(one,context,op):
  if len(one) == 0:
    return ket("",0)
  for sp in one:
    r = sp.apply_op(context,op)
    break
  for sp in one:
    tmp = sp.apply_op(context,op)
    r = union(r,tmp)                              # we could probably make this a general function, and then pass in intersection(), union() etc.
  return r                                        # ie, cast pair-fn(sp1,sp2) into fn(sp1,sp2,...,spn)
    


def absolute_difference_fn(x,y):
  return abs(x - y)  
  
# general to specific.
# The idea is you take an average of some object.
# Let's say the slashdot-to-sp I've recently been playing with.
# So: hashes |ave-slashdot> => hashes |slashdot-1> + hashes |slashdot-2> + hashes |slashdot-3> + hashes |slashdot-4>
# Then, given |ave-slashdot>, find the bits that are unique to |slashdot-n>
# Maybe something like:
# hashes |slashdot: 5> => general-to-specific(hashes |ave-slashdot>, hashes |slashdot-5>)
# NB: in the process we made a sub-category. And hashes|slashdot: 5> will look vastly different from hashes|slashdot-5>
#
# Update: probably works better if we have threshold filters in there before learning the average:
# roughly: hashes |ave-slashdot> => TF[t1] hashes |slashdot-1> + TF[t2] hashes |slashdot-2> + TF[t3] hashes |slashdot-3> + TF[t4] hashes |slashdot-4>
# Indeed, it is probably actually this:
# hashes |ave-slashdot> => TF[t5] (TF[t1] hashes |slashdot-1> + TF[t2] hashes |slashdot-2> + TF[t3] hashes |slashdot-3> + TF[t4] hashes |slashdot-4> )
# Not currently sure how to choose the values for tk
#
# 10/5/2015: work on images shows that abs() is not he best choice. pos(x) is much better!
#  
def general_to_specific(average,specific):
  return intersection_fn(absolute_difference_fn,average.normalize(),specific.normalize())  # NB: .normalize() is vital for this to work!
  #return intersection_fn(absolute_difference_fn,average,specific)  


# 12/5/2014:
# exp[child,n] |x>
# maps to: (1 + child + child^2 + ... + child^n ) |x>
# cf: exp(A) |Psi> in QM.
# if n <= 0, return |x>
# 
def exp(one,context,parameters):
  try:
    op, n = parameters.split(",")              # slightly hackish. Don't know a better way to do it ....
    print("exp op " + op)
    print("exp n  " + n)
    n = int(n)
  except:
    return one

  r = one
  tmp = one
  for k in range(n):
    tmp = tmp.apply_op(context,op)            # this is broken for some operators, depends on details of that operator though!
    r += tmp
  return r

# 4/8/2014:
# exp-max[op] |x>
# maps to (1 + op + op^2 + ... op^n) |x>
# such that exp[op,n] |x> == exp[op,n+1] |x>
# Warning: we have no idea before hand how many resources this will end up using. We don't know n, or how big the sp is going to be!
#
# Need to check it works. Cool. Seems to give the right result. eg, using binary-tree.sw
# Done.
#
# Now, let's implement: exp-max[op,t] |x>
# Now need to check this one works.
#
# Something I have wanted to do for a very long time is to split an academic field of study into categories.
# Roughly: exp-max[references,t] |some seed physics paper>
# where the "references" operator applied to a paper on arxiv.org returns the list of papers it references.
# We may (though maybe not) need t > 0, else it might drag in all of arxiv.org
# But won't know this for sure until we try. 
def exp_max(one,context,parameters):
  try:
    op, t = parameters.split(",")
    t = int(t)
  except:
    op = parameters
    t = 0

  r = one
  tmp = one
  previous_size = len(r)                    # yup. I finally implemented len() for superpositions/kets.
  n = 0
  while True:
    tmp = tmp.apply_op(context,op)
    r += tmp
#    if len(r) == previous_size:            # a variant is: len(r) - previous_size <= t
    if len(r) - previous_size <= t:         # since kets add in sp, this difference is the number of newly discovered kets.
      break                                 # so, if this is 0, then we have reached the end of the network.
    previous_size = len(r)                  # if this is say 1, then in this round we only found 1 new ket.
    n += 1                                  # which in some cases is enough to say, this will suffice as the end of the network.
  print("n:",n)
  return r


from math import factorial
# 17/4/2015:
# full-exp[child,n] |x>
# maps to: (1 + child/1 + child^2/2 + ... + child^n/n! ) |x>
# cf: exp(A) |Psi> in QM.
# if n <= 0, return |x>
# 
def full_exp(one,context,parameters):
  try:
    op, n = parameters.split(",")              # slightly hackish. Don't know a better way to do it ....
    print("exp op " + op)
    print("exp n  " + n)
    n = int(n)
  except:
    return one

  r = one
  tmp = one
  for k in range(n):
    tmp = tmp.apply_op(context,op)
    r += tmp.multiply(1/factorial(k+1))
  return r
  
                                                                 
# 19/5/2014:
# relevant-kets[op]
# eg: relevant-kets[friends]
# returns |Fred> + |Sam>
#
# 13/2/2015: idea for a tweak:
# relevant-kets[op] |> works as normal (ie, incoming superposition is the empty superposition)
# but, a tweak:
# relevant-kets[op2] relevant-kets[op1] |>
# returns intersection(relevant-kets[op2],relevant-kets[op1])
# also: relevant-kets[op] SP
# returns intersection(relevant_kets[op],SP)
# Cool! Seems to work!
#
# 17/2/2015: Nah. I was really mixing two ideas into the one function.
# what happens if your restrict down to |> relevant-kets, then you apply one more layer, and bam all of those kets are valid? Not what we want.
# So now a distinction: relevant-kets[op], and intn-relevant-kets[op]  
#
# 22/2/2015: tweak: relevant-kets[op1,op2,...] SP
# no need to do: relevant-kets[op1] relevant-kets[op2] SP
#
def intersection_relevant_kets(one,context,ops):
  r = one
  for op in ops.split(','):
    kets_list = context.relevant_kets(op)
    r = intersection(r,kets_list)  
  return r 

# 22/2/2015 tweaked: now if op == "*" it returns a sp of all known kets.
def relevant_kets(one,context,op):
  return context.relevant_kets(op)

  
# convert the labels in a superposition to a pretty-print vector
def old_sp_to_vect(one):
  max_len = 0
  for x in one.data:
    max_len = max(max_len,len(x.label))
  for x in one.data:
    print("[ " + x.label.ljust(max_len) + " ]")

def sp_to_vect(one):
  if one.count() <= 1:
    vect = one.the_label()
  else:                                        
    vect = "\n".join(x.label for x in one.data)
  return paste_columns([vect],'[ ','',' ]')

def sp_to_list(one):                                        # what happens if one is a ket? Fixed, I think.
  if one.count() <= 1:
    return one.the_label()
  return "\n".join(x.label for x in one.data)

# make 0.000 coeffs prettier!
def old_coeff_to_str(x):
  if x == 0:
    return "0"
  else:
    return str("%.2f" % x)                                         # this means if we want to change precission, we only need to change it here.
    #return str("%.0f" % x)                                         # this means if we want to change precission, we only need to change it here.
    #return str("%.2f" % (100 - x))                                 # we use this version when graphing heat-maps of simm matrices, since 0 is black, 100 is white.    

def coeff_to_str(x):                                              # yeah, ugly code. Too scared of my code that depends on this, to do it the tidy way.
  return float_to_int(x,2)
    
def sp_coeffs_to_list(one):                                        # what happens if one is a ket? Fixed, I think.
  if one.count() <= 1:
    return coeff_to_str(one.the_value())
  return "\n".join(coeff_to_str(x.value) for x in one.data)


# these two functions help to pretty-print tables, and matrices in particular:
def normalize_column_return_list(s,n):
  lines = (s.split('\n') + ['']*n)[:n]
  max_len = max(len(x) for x in lines)
  return [x.ljust(max_len) for x in lines]

def paste_columns(data,pre='',sep=' ',post=''):
  if len(data) == 0:
    return ""
  columns = len(data)
  rows = max(s.count('\n') + 1 for s in data)
  r = [normalize_column_return_list(s,rows) for s in data]
  return "\n".join(pre + sep.join(r[j][k] for j in range(columns)) + post for k in range(rows))
    

# first version of code to spit out a pretty printed matrix given BKO rules:
def first_matrix(context,op):
  one = context.relevant_kets(op).ket_sort()       # one is the list of kets that will be on the right hand side.
                                                   # usefully, relevant_kets() always returns a superposition.
  if one.count() == 0:                             # if one is empty, return the identity ket.
    return ket("",0)
                                                  
  two = superposition()                            # two is the list of kets that will be on the left hand side.
  for elt in one.data:
    sp = elt.apply_op(context,op)
    two = union(two,sp)
  two = two.ket_sort()

  empty = two.multiply(0)                           # empty is the two list, with all coeffs set to 0
  
  matrix_columns = []                                   # convert to list-comprehension?
  for elt in one.data:
    sp = (elt.apply_op(context,op) + empty).ket_sort()  # we add "empty" so the column has all the elements.
    matrix_columns.append(sp_coeffs_to_list(sp))

  x = sp_to_vect(one)
  y = sp_to_vect(two)
  M = paste_columns(matrix_columns,'[  ','  ','  ]')
  matrix = paste_columns([y,'=',M,x])    
  print(matrix)
  #print("\n" + paste_columns(matrix_columns,'',' ',''))
  return ket("matrix")                              # Just here so it retuns a ket of some sort. Has no meaning, really.

              
# code to return a single matrix, and the left-hand superposition:
# one must be a superposition
# op is a literal op
# NB: the difference between this one, and the one below is it uses: x.apply_op(context,op)
# the "new" one uses x.merged_apply_op(context,ops)
def first_single_matrix(one,context,op):
  one = one.apply_sigmoid(set_to,1)
  two = superposition()                                 # two is the list of kets that will be on the left hand side.
  for elt in one.data:                                  # heh. using one.data kind of breaks the superposition abstract interface idea.
    sp = elt.apply_op(context,op)
    two = union(two,sp)
  two = two.ket_sort().multiply(0)                      # merged two, and empty into the same thing.
  matrix_columns = [sp_coeffs_to_list((elt.apply_op(context,op) + two).ket_sort()) for elt in one.data ]
  M = paste_columns(matrix_columns,'[  ','  ','  ]')    # M is the matrix
  return two, M
  
# second version of code to spit out a matrix:
# seems to be correct.
def matrix(context,op):
  one = context.relevant_kets(op).ket_sort()       # one is the list of kets that will be on the right hand side.
                                                   # usefully, relevant_kets() always returns a superposition.
  if one.count() == 0:                             # if one is empty, return the identity ket.
    return ket("",0)

  two, M = single_matrix(one,context,op)                                                  

  x = sp_to_vect(one)
  y = sp_to_vect(two)
  matrix = paste_columns([y,'=',M,x])    
  print(matrix)
  return ket("matrix")                              # Just here so it retuns a ket of some sort. Has no meaning, really.
  
# third version. 
# this one I want to handle multiple ops at once, and then chain the matrices.
# eg: matrix[M2,M1]
# or: matrix[friends,friends]  -- ie, matrix of second-order friends
def multi_matrix(context,ops):
  ops = ops.split(',')[::-1]
  print("ops:",ops)
  
  one = context.relevant_kets(ops[0]).ket_sort()   # one is the list of kets that will be on the right hand side.
                                                   # usefully, relevant_kets() always returns a superposition.
  if one.count() == 0:                             # if one is empty, return the identity ket.
    return ket("",0)

  two, M = single_matrix(one,context,ops[0])
  matrices = [M]
  for op in ops[1:]:
    two, M = single_matrix(two,context,op)
    matrices.append(M)
  x = sp_to_vect(one)
  y = sp_to_vect(two)
  line = [y,'='] + matrices[::-1] + [x]
  matrix = paste_columns(line)
  print(matrix)  

# code to save the matrix (useful for big ones, too hard to cut and paste from the console)
  print("saving to: saved-matrix.txt")
  file = open("saved-matrix.txt",'w')
  file.write("sa: matrix[" + ",".join(ops[::-1]) + "]\n")
  file.write(matrix)
  file.close()  

  return ket("matrix")  



# uses x.merged_apply_op(context,ops) instead of x.apply_op(context,op)
def single_matrix(one,context,op):
  one = one.apply_sigmoid(set_to,1)
  two = superposition()                                 # two is the list of kets that will be on the left hand side.
  for elt in one.data:                                  # heh. using one.data kind of breaks the superposition abstract interface idea.
    sp = elt.merged_apply_op(context,op)
    two = union(two,sp)
  two = two.ket_sort().multiply(0)                      # merged two, and empty into the same thing.
  matrix_columns = [sp_coeffs_to_list((elt.merged_apply_op(context,op) + two).ket_sort()) for elt in one.data ]
  M = paste_columns(matrix_columns,'[  ','  ','  ]')    # M is the matrix
  return two, M
  

# see if we can tidy this up later!  
# Heh. Doesn't need tidying up. This deprecates matrix(context,ops)
def merged_multi_matrix(context,ops):
  ops = ops.replace(',',' ')                       # we have to do this, as the current parser can't handle: matrix[op3 op2 op1], 
                                                   # but can handle matrix[op3,op2,op1]. It would be nice to eventually fix this!
                                                   # Indeed, even op-sequence: matrix[op2 op1^k] kind of thing.
  one = context.relevant_kets(ops.split()[-1]).ket_sort()       # one is the list of kets that will be on the right hand side.
                                                   # usefully, relevant_kets() always returns a superposition.
  if one.count() == 0:                             # if one is empty, return the identity ket.
    return ket("",0)

  two, M = single_matrix(one,context,ops)                                                  

  x = sp_to_vect(one)
  y = sp_to_vect(two)
  matrix = paste_columns([y,'=',M,x])    
  print(matrix)
  return ket("matrix")                              # Just here so it retuns a ket of some sort. Has no meaning, really.
  
def merged_naked_matrix(context,ops):
  ops = ops.replace(',',' ')
  one = context.relevant_kets(ops.split()[-1]).ket_sort()       # one is the list of kets that will be on the right hand side.
                                                   # usefully, relevant_kets() always returns a superposition.
  if one.count() == 0:                             # if one is empty, return the identity ket.
    return ket("",0)

  two, M = single_matrix(one,context,ops)
  print(M)
  return ket("matrix")
  
# 5/6/2014 update: Let's write vector[op] (|x> + |y>)
# Same as merged-matrix, just you pass in the superpositions of interest, instead of using relevant_kets.
# May need a better name.
def first_vector(one,context,ops):
  one = superposition() + one   # just make sure one is a sp.
  if one.count() == 0:
    return ket("",0)
  ops = ops.replace(',',' ')
  two, M = single_matrix(one,context,ops)                                                  
  x = sp_to_vect(one)
  y = sp_to_vect(two)
  matrix = paste_columns([y,'=',M,x])    
  print(matrix)
  return ket("matrix")             
  
def vector(one,context,ops):
  ops = ops.replace(',',' ')
  one = superposition() + one   # just make sure one is a sp.
  if one.count() == 0:          # this happens a) if the default ket is |>, or the passed in ket is |>
                                # sa: id
                                # 0.000|>
                                # sa: vector[op]
                                # or:
                                # sa: vector[op] |>
    one = context.relevant_kets(ops.split()[-1]).ket_sort() 
    if one.count() == 0:
      return ket("",0)

  two, M = single_matrix(one,context,ops)                                                  
  x = sp_to_vect(one)
  y = sp_to_vect(two)
  matrix = paste_columns([y,'=',M,x])    
  print(matrix)
  return ket("matrix")             

 
# 23/5/2014:
# let's implement a map function (since we can't have multi-line for loops, this will have to do!)
# eg: map[op] (|x> + |y>)
# runs:
# op |x> => op |_self>
# op |y> => op |_self>
# ie, it converts function operators (op on the right hand side), in to literal operators (on the left hand side)
# eg: map[fib] (|10> + |11>)
# eg: map[child] (|x> + |0> + |1> + |00> + |01> + |10> + |11>)
# or indirectly:
# map[op] "" |list>
# one is a ket/sp
# op is a string
# 
# tweak, now we can also do: map[fn,result] "" |list>  -- ie, we can now specify the destination, in this case "result"
def map(one,context,op):
  try:
    fn, op = op.split(',')
  except:
    fn = op
  print("fn:", fn)
  print("op:", op)

  for x in one:             # what if x has x.value != 1? x.apply_op handles that.
    context.learn(op,x,x.apply_op(context,fn))  # currently fn must be of form: fn |*> #=> bah.
  return ket("map")                             # Would sometimes be useful to be able to use a full function here.
                                                # Something we probably need to take up with .apply_op()
                                                # As then (presumably) it could work for similar[op] |ket> too.
                                                # Code change for this is probably hard, since would need pieces from the processor file.

# 4/5/2015: 
# a new version of map. This one puts results in a temporary store while doing the calculatoin, then copies the result back after.
# Basically to stop the code eating its own tail. eg, mapping a grid to a grid, you need a temporary grid.
def copy_map(one,context,op):
  try:
    fn, op = op.split(',')
  except:
    fn = op
  print("fn:", fn)
  print("op:", op)
  op_tmp = op + "-pDBUKObhYk"       # thanks: https://www.random.org/strings/
  print("op-tmp:",op_tmp)

  for x in one:   
    context.learn(op-tmp,x,x.apply_op(context,fn))    # store results on temporary grid
#  for x in one:
#    context.learn(op,x,x.apply_op(context,op-tmp))    
#  context.copy_op(op_tmp,op)        # maybe ... still need some thinking time. What about context.mv_op(op_tmp,op)? 
#  context.delete_op(op-tmp)         # need to implement this function.
  context.move_op(op_tmp,op)  
  return ket("copy-map")                             


# 28/5/2014:
# working towards a BKO version of the categorize code.
# first, the equivalent of metric_mbr, using simm.
#
# one is a superposition
# op is a string
# x is a ket
# thresh is a float
def simm_mbr(context,op,x,thresh,one):
  f = x.apply_op(context,op)
  for elt in one:
    g = elt.apply_op(context,op)
    if silent_simm(f,g) >= thresh:
      return True
  return False
   
# categorize[op,thresh,destination]
def categorize(context,parameters):
  try:
    op,thresh,destination = parameters.split(',')
    thresh = float(thresh)
    destination = ket(destination)
  except:
    return ket("",0)
  
  one = context.relevant_kets(op)                 # one is a superposition
  print("one:",one)  
  out_list = []                                   # out_list will be a list of superpositions.
  for x in one:                                   # x is of course a ket
    n = 0
    del_list = []                                 # del_list will be a list of integers.
    for i in range(len(out_list)):
      if simm_mbr(context,op,x,thresh,out_list[i]):
        if n == 0:
          out_list[i] += x
          idx = i
          n = 1
        else:
          out_list[idx] += out_list[i]
          del_list.append(i)
    if n == 0:
      out_list.append(superposition() + x)        # we use "superposition() + x" instead of just "x" so out_list is always a list of superpositions, not kets.
    else:
      out_list = [x for index,x in enumerate(out_list) if index not in del_list]

  for k, sp in enumerate(out_list):
    print("sp:",sp)
    context.learn("category-" + str(k),destination,sp)  
  return ket("categorize")


import datetime
# day of the week function:
# day-of-the-week |date: 2014/06/3> => |day: Tuesday>
# Code from here: http://stackoverflow.com/questions/9847213/which-day-of-week-given-a-date-python
# Heh. Python makes this super easy!
def day_of_the_week(one):
  cat, value = extract_category_value(one.the_label())
  if cat.split(': ')[-1] != "date":
    return ket("",0)
  
# 5/2/2015: tidy it up:
  try:
    year,month,day = (int(x) for x in value.split('/'))
  except:
    try:
      year,month,day = (int(x) for x in value.split('-'))    
    except:
      return ket("",0) 
  day_list  = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
  the_day = day_list[datetime.date(year,month,day).weekday()]
  return ket("day: " + the_day)


# maybe do a version using pretty print columns code.
def print_pixels(one,context,op="pixels"):      # heh. Can't currently think of a way to do this without needing op fed in.
  data = one.apply_op(context,op)               # Since only compound table handles fn's needing context.
                                                # But this is a weird case where we don't really want anything other than "pixels"
  I = int(apply_value(one.apply_op(context,"dim-1")).value)
  J = int(apply_value(one.apply_op(context,"dim-2")).value)

  print("I:",I)
  print("J:",J)  

  for j in range(1,J+1):
    for i in range(1,I+1):
      elt = ket("pixel: " + str(j) + ": " + str(i))     # not sure what happens if we want other than pixel: 
      c = int(data.find_value(elt))
      #c = '#'
      if c == 0:
        c = ' '
      print(c,end='')
    print()
  return ket("pixels")
  
  
# long sp. Prints out the long_display form of a sp.
def long_display(one):
  print(one.long_display())
  return one
  
# split |word1 word2 word3 word4> => |word1> + |word2> + |word3> + |word4>
# saves typing in some cases. eg, find-topic[words] split |word1 word2 word3>
# assumes one is a ket
def old_split_ket(one):
  result = superposition()
  result.data = [ket(w,one.the_value()) for w in one.the_label().split() ]        # Buggy? eg, anything with duplicates. eg: split |a a b a b a a c a>
  return result                                                   # superficially it seems to work, because elsewhere tidies up our mess (probably the extract_compound_superposition code)

def split_ket(one):
  r = superposition()
  for key,value in one.items():
    for label in key.split():
      r.add(label, value)
  return r

# 29/8/2015:
# clean-split |word1 word2 word3> => |word1> + |word2> + |word3>
# essentially the same as split_ket, except it sends punctuation to ' '
#
# one is a ket
def clean_split_ket(one):
  result = superposition()
  text = re.sub('[.,!?$\"-]',' ',one.label)
  text = text.replace('\\n',' ').replace('\\r',' ')      # should this line be before the re.sub() line?
  for word in text.split():
    result += ket(word,one.value)
  return result

# quick play here: http://semantic-db.org/the-semantic-agent/play_with_list_to_sp.py
def list_to_sp(s,list):
  result = superposition()
  result.data = [ket(s + str(k),v) for k,v in enumerate(list)]
  return result

def sp_to_list(sp):
  return [x.value for x in sp.ket_sort().data]                     # NB: the ket_sort(). Even if we shuffle the sp, we get the same list back.

# currently broken, since it gets fed a list of kets, rather than one superposition.
# I don't currently know where/how to fix that!
# I presume I need a new table in the processor.
# 7/8/2014: heh. I don't understand what I was trying to do here!
def sp_as_list(sp):                                                # I think natural sort is buggy when you have negative values, eg |x: -10>. 
  sp = superposition() + sp                                        # cast any kets to superposition
  print([x.value for x in sp.ket_sort().data])                     # NB: the ket_sort(). Even if we shuffle the sp, we get the same list back.
  return sp                              
  


# 7/8/2014, let's write a sp-propagate function.
# Takes an initial superposition, then takes an operator, and applies it repeatedly.
# Then display this all as a matrix, maybe something we can plot in gnuplot.
# First need this:
def sp_coeffs_to_column(one): 
  one = superposition() + one   # cast kets to sp.
  def to_str(n):
    if n == 0:
      return "0"
      #return " "
    else:
      return str("%.2f" % n)
      #return "1"
  return "\n".join(to_str(x.value) for x in one.data)

# usage: sp-propagate[op,k] "" |list>
# op is an operator, k is the number of iterations.  
def sp_propagate(one,context,parameters):
  try:
    op,k = parameters.split(",")
    k = int(k)
  except:
    return ket("",0)

  matrix = []
  r = one
  empty = r.apply_sigmoid(set_to,0)
  for idx in range(k):
    matrix.append(sp_coeffs_to_column((r + empty).ket_sort()))  # making use of adding an sp of all 0's does not change the meaning
    r = r.apply_op(context,op)
  print(paste_columns(matrix,'',' ',''))
  return ket("matrix")
 

# 10/11/2014:
# apply()
# eg:
# apply(|op: age> + |op: friends>,|Fred>)
# maps to:
# age |Fred> + friends |Fred>
# a more common usage:
# star |*> #=> apply(supported-ops|_self>,|_self>)
def apply_sp(context,one,two):
  print("one:",one)
  print("two:",two)
  r = superposition()
  for x in one:                    # yeah, about time we defined iterators or something for superpositions! Done!
    print("x.label:",x.label)
    print("x.value:",x.value)
    if x.label.startswith("op: "):
      op = x.label[4:] 
      r += two.apply_op(context,op).multiply(x.value)
  return r

# 17/1/2015:
# clone(|x>,|y>)
# copies rules from |x> and applies them to |y>
# eg: age |x> => |31>
# mother |x> => |Jane>
# After clone(|x>,|y>) we have:
# age |y> = |31>
# mother |x> = |Jane>
# not super sure the use of this yet though :)
# quick test, and it works! 
def clone_ket(context,one,two):
  one = one.ket()                   # one needs to be a ket. two can be ket or sp.
  operators = context.recall("supported-ops",one)
  for op_ket in operators:
    op = op_ket.label[4:]
    rule = context.recall(op,one)    # we can't use one.apply_op(C,op) as that activates any stored rules.        
    for x in two:
      context.learn(op,x,rule)
  return ket("clone")  

# 10/11/2014:
# expand-hierarchy (not that I can spell that word!)
# expand-hierarchy |a: b: c: d>
# maps to:
# |a> + |a: b> + |a: b: c> + |a: b: c: d>
#
# example usage:
# intersection(expand-hierarchy |a: b: c: d: e: f>, expand-hierarchy |a: b: c: x: y>)
#
# assumes "one" is a ket.
def expand_hierarchy(one):
  r = superposition()
  L = []
  for x in one.label.split(": "):
    L.append(x)
    r += ket(": ".join(L))
  return r.multiply(one.value)
  
# 10/11/2014:
# chars |some text>
# maps to:
# | > + 2|e> + |m> + |o> + |s> + 2|t> + |x>
#
# example usage:
# chars-fn |*> #=> chars |_self>
# map[chars-fn,chars] "" |list>
# similar[chars] |George>                      # NB: similar[op] bugs out if "op |*> #=> ... " is defined.
#                                              # something to do with the stored-rule vs similar[]. 
# assumes "one" is a ket.                      # related: maybe make similar work with ops other than literal ops?
# Probably we can tidy it up a bit ... Nah. Looks about right. # probably a lot of work though!
def chars(one):
  char_list = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:-*"
  L = [0]*len(char_list)
  for c in one.label:
    k = char_list.find(c)
    if k >= 0:
      L[k] += 1
  r = superposition()
  for k, count in enumerate(L):
    r += ket(char_list[k],count)
  return r.drop().multiply(one.value)
  

# 4/1/2015:
# equal(one,two), returns:                  # name clash with "equal[70] |number: 37>"
# 1|True> if one == two
# 0|True> if one and two are completely disjoint
# values in between otherwise (makes use of unscaled_simm)
# name change from test_equal() to equality_test() due to pytest.
def equality_test(one,two):
  value = unscaled_simm(one,two)            # NB: equal(0|x>,0|x>) returns 0|True>. Not currently sure if we want this, or need to tweak.
  return ket("True",value)
  

# LOL. Seems we already have the equiv of push-float and pop-float at the start of this file!
# Anyway, I think these are better versions. 
# push-float
# examples:
# push-float 3| > == |3>
# push-float 3|x> == |x: 3>
# push-float 3.2|x: y > == |x: y: 3.2> (not sure the number of decimal places to keep, initially all of them)
#
# 5/2/2015: hrmm... maybe push-float n|> == |> for any n?
#
def push_float(one):
  if one.label == "":
    return ket("",0)
  value = one.value
  label = one.label.rstrip()
  if float(value).is_integer():
    value = str(int(value))
  else:
    value = str(value)
  if label == "":
    return ket(value)
  return ket(label + ": " + value)
  
# pop-float
# examples:
# pop-float |3.2> == 3.2| >
# pop-float 5|7> == 35| >
# pop-float |x: 2> == 2|x>
# pop-float 5.1|x: y: 2> == 10.2|x: y>
# pop-float |x: y> == |x: y>
def pop_float(one):
  coeff = one.value
  label = one.label
  try:
    value = float(label)
    label = " "
  except:
    try:
      label, value = label.rsplit(": ",1)
      value = float(value)
    except:
      return one
  return ket(label,coeff * value)

# cat-depth
# return the depth of the categories:
# cat-depth |> == |number: 0>
# cat-depth |x> == |number: 1>
# cat-depth |x: y> == |number: 2>
def category_depth(one):
#  return ket("number: " + str(len(one.label.split(": "))))
  if one.label == "":
    return ket("number: 0")
  return ket("number: " + str(one.label.count(": ") + 1))


#from PIL import Image
# 12/1/2015:
# load-image[lenna.png] |my image>
#
# Notes: I'm reading here: http://pillow.readthedocs.org/en/latest/handbook/tutorial.html
# I'm not sure there is a win from working with images in BKO, compared to straight python!!
# 
def load_image(one,context,filename):
  try:
    im = Image.open(filename)
    width = im.size[0]
    height = im.size[1]
    for x in one:                                         # why do we do this? Why do the same thing for all the elements in a superposition?
      context.learn("filename",x,"file: " + filename)
      context.learn("width",x,str(width))
      context.learn("height",x,str(height))
      pixel_list = superposition()
      for h in range(height):
        for w in range(width):
          pixel = ket(x.label + ": pixel: " + str(h) + ": " + str(w))
          if w > 0:
            context.learn("left",pixel,ket(x.label + ": pixel: " + str(h) + ": " + str(w-1)))
          if w < (width-1):
            context.learn("right",pixel,ket(x.label + ": pixel: " + str(h) + ": " + str(w+1)))
          if h > 0:
            context.learn("up",pixel,ket(x.label + ": pixel: " + str(h-1) + ": " + str(w)))
          if h < (height-1):
            context.learn("down",pixel,ket(x.label + ": pixel: " + str(h+1) + ": " + str(w)))
          
# way too slow! Unusably so.
#          context.add_learn("pixel-list",x,pixel)                    # NB: this line is seriously slow!
          pixel_list.data.append(pixel)
          r, g, b = im.getpixel((w,h))[:3]                           # assumes image is RGB or RGBA
#          context.learn("r-pixel-value-self",pixel,pixel.multiply(r))# and promptly ignores the A if RGBA
#          context.learn("g-pixel-value-self",pixel,pixel.multiply(g))
#          context.learn("b-pixel-value-self",pixel,pixel.multiply(b))
          context.learn("R",pixel,pixel.multiply(r))# and promptly ignores the A if RGBA
          context.learn("G",pixel,pixel.multiply(g))
          context.learn("B",pixel,pixel.multiply(b))
      context.learn("pixel-list",x,pixel_list)
# show the image. later will comment this out.
    im.show()  
    return ket("load-image")
  except:
    return ket("failed to load image")   # not yet sure which of these two I want to return. 
    #return ket("")

# 20/4/2015: finally returned to try and finish this beasty!
# save-image[lenna-diff.png] |my image>
#
# one is a ket! Not sure why load_image() needed superpositions!
def save_image(one,context,filename):
  try:
    x = one.ket()
    width = int(context.recall("width",x).the_label())
    height = int(context.recall("height",x).the_label())
    size = (width,height)
    im = Image.new('RGB',size)
    image_pixels = im.load()
    for h in range(height):
      for w in range(width):
        pixel = ket(x.label + ": pixel: " + str(h) + ": " + str(w))
        r = int(context.recall("R",pixel).the_value())
        g = int(context.recall("G",pixel).the_value())
        b = int(context.recall("B",pixel).the_value())
        print("R:",r,"G:",g,"B:",b)
        image_pixels[w,h] = (r,g,b)
    im.save(filename)
    return ket("save-image")
  except:
    return ket("failed to save image")

# 4/5/2015: 
# show-image |my image>
#
# one is a ket! Not sure why load_image() needed superpositions!
def show_image(one,context):
  try:
    x = one.ket()
    width = int(context.recall("width",x).the_label())
    height = int(context.recall("height",x).the_label())
    size = (width,height)
    im = Image.new('RGB',size)
    image_pixels = im.load()
    for h in range(height):
      for w in range(width):
        pixel = ket(x.label + ": pixel: " + str(h) + ": " + str(w))
        r = int(context.recall("R",pixel).the_value())
        g = int(context.recall("G",pixel).the_value())
        b = int(context.recall("B",pixel).the_value())
        print("R:",r,"G:",g,"B:",b)
        image_pixels[w,h] = (r,g,b)
    im.show()
    return ket("show-image")
  except:
    return ket("failed to show image")
  
# 10/5/2015:
# OK. Let's write a new version of image-load.
# this time, so all the data is in one single superposition. This makes a few things easier, and a bunch of things neater.
# eg, currently: "load-image[lenna.png] |Lenna>" modifies |Lenna>, kind of breaks the non-mutablility thing really.
# Plan this time is: |Lenna> => image-load[lenna.png] |>
# for this to work we have to drop things like: 
# filename |Lenna> => |file: 220px-Lenna.png>
# width |Lenna> => |220>                  # plan is for these to be auto-calculated. Also means we can create an n*m image using just: 0|image: pixel: R: n: m>
# height |Lenna> => |220>
# And:
# left |Lenna: pixel: 219: 215> => |Lenna: pixel: 219: 214>
# right |Lenna: pixel: 219: 215> => |Lenna: pixel: 219: 216>
# up |Lenna: pixel: 219: 215> => |Lenna: pixel: 218: 215>
# 
def working_image_load(filename):
  # not sure what speed impact separating this out has:
  def pixel_ket(type,h,w,r):
    if type == '':
      return ket("pixel: " + str(h) + ": " + str(w),r)
    else:
      return ket("pixel: " + type + ": " + str(h) + ": " + str(w),r)
  
  try:
    im = Image.open(filename)
    width = im.size[0]
    height = im.size[1]
    pixel_list = superposition()
    for h in range(height):
      tmp_list = []
      for w in range(width):
        r, g, b = im.getpixel((w,h))[:3]                           # assumes image is RGB or RGBA

#        pixel_r = ket("pixel: R: " + str(h) + ": " + str(w),r)
#        pixel_g = ket("pixel: G: " + str(h) + ": " + str(w),g)
#        pixel_b = ket("pixel: B: " + str(h) + ": " + str(w),b)

#        print("R:",pixel_r)
#        print("G:",pixel_g)
#        print("B:",pixel_b)

        # tmp_list version:
#        tmp_list.append(pixel_r)
#        tmp_list.append(pixel_g)
#        tmp_list.append(pixel_b)
        tmp_list.append(pixel_ket("R",h,w,r))
        tmp_list.append(pixel_ket("G",h,w,g))
        tmp_list.append(pixel_ket("B",h,w,b))

      pixel_list.data += tmp_list
                  
# show the image:
    im.show()
    return pixel_list
  except:
    return ket("failed to load image")   

# still slow at 20 min to load up 220px-lenna.png
# not sure what else to try
# I wonder if fast_sp would be faster.
# though we have the "fast_sp doesn't work here" bug!
#
def improved_image_load(filename):
  def pixel_ket(type,h,w,r):
    if type == '':
      return ket("pixel: " + str(h) + ": " + str(w),r)
    else:
      return ket("pixel: " + type + ": " + str(h) + ": " + str(w),r)
                                                             
  try:
    im = Image.open(filename)
    width = im.size[0]
    height = im.size[1]
    pixel_list = superposition()
#    for h in range(height):
#      tmp_list_r = [pixel_ket("R",h,w,im.getpixel((w,h))[0]) for w in range(width)]
#      tmp_list_g = [pixel_ket("G",h,w,im.getpixel((w,h))[1]) for w in range(width)]
#      tmp_list_b = [pixel_ket("B",h,w,im.getpixel((w,h))[2]) for w in range(width)]
#      pixel_list.data += tmp_list_r + tmp_list_g + tmp_list_b
#    tmp_list_r = [ pixel_ket("R",h,w,im.getpixel((w,h))[0]) for w in range(width) for h in range(height) ]
#    tmp_list_g = [ pixel_ket("G",h,w,im.getpixel((w,h))[1]) for w in range(width) for h in range(height) ]
#    tmp_list_b = [ pixel_ket("B",h,w,im.getpixel((w,h))[2]) for w in range(width) for h in range(height) ]
# im.load() version:
    pixels = im.load()
    tmp_list_r = [ pixel_ket("R",h,w,pixels[w,h][0]) for w in range(width) for h in range(height) ]  
    tmp_list_g = [ pixel_ket("G",h,w,pixels[w,h][1]) for w in range(width) for h in range(height) ]
    tmp_list_b = [ pixel_ket("B",h,w,pixels[w,h][2]) for w in range(width) for h in range(height) ]

    pixel_list.data += tmp_list_r + tmp_list_g + tmp_list_b
                  
# show the image:
    im.show()
    return pixel_list
  except:
    return ket("failed to load image")    

# 11/5/2015:
# image-save[lenna.png] "" |lenna>
# image-show "" |lenna>
#
# one is a superposition
#
def improved_image_save_show(one,filename=""):
  def extract_ket_details(one):       # one is a ket
    try:
      value = one.value
      pixel_type, x, y = one.label.split(': ')[1:]
      return pixel_type, x, y, int(value)
    except:
      return                      # not sure what to do here!
  def extract_pixel_value(pixel_dict,pixel_type,h,w):
    try:
      value = pixel_dict[pixel_type + ":" + str(h) + ":" + str(w)]
    except:
      value = 0
    return value
        
  try:
    pixel_dict = {}
    max_x = 0
    max_y = 0
    for x in one:
      print("x:",x)
      pixel_type, x, y, value = extract_ket_details(x)
      if int(x) > max_x:
        max_x = int(x)
      if int(y) > max_y:
        max_y = int(y)
      pixel_dict[pixel_type + ":" + x + ":" + y] = value
    print("finished for loop")
    max_x += 1
    max_y += 1
    print("max x:",max_x)
    print("max y:",max_y)
    size = (max_y,max_x)          # should it be: (max_y,max_x)?      
    im = Image.new('RGB',size)
    print("size worked")
    pixels = im.load()
    print("load worked")
    for h in range(max_x):
      for w in range(max_y):
        r = extract_pixel_value(pixel_dict,"R",h,w)
        g = extract_pixel_value(pixel_dict,"G",h,w)
        b = extract_pixel_value(pixel_dict,"B",h,w)
        pixels[w,h] = (r,g,b)
    if filename != "":
      im.save(filename)
    im.show()
    return ket("image show/save")
  except:
    return ket("failed to show/save image")

# image-smooth[20] "" |lenna>
#
# 
def image_smooth(one,k):
  try:
    k = int(k)
  except:
    return ket("",0)

  def extract_ket_details(one):       # one is a ket
    try:
      value = one.value
      pixel_type, x, y = one.label.split(': ')[1:]
      return pixel_type, x, y, int(value)
    except:
      return            
      
  def extract_pixel_value(pixel_dict,pixel_type,h,w):
    try:
      value = pixel_dict[pixel_type + ":" + str(h) + ":" + str(w)]
    except:
      value = 0
    return value

  def smooth_pixel_value(pixel_dict,pixel_type,h,w): # can we do this neater!?  
    value = extract_pixel_value(pixel_dict,pixel_type,h-1,w-1)/16 + extract_pixel_value(pixel_dict,pixel_type,h,w-1)/16 + extract_pixel_value(pixel_dict,pixel_type,h+1,w-1)/16
    value += extract_pixel_value(pixel_dict,pixel_type,h-1,w)/16 + extract_pixel_value(pixel_dict,pixel_type,h,w)/2 + extract_pixel_value(pixel_dict,pixel_type,h+1,w)/16
    value += extract_pixel_value(pixel_dict,pixel_type,h-1,w+1)/16 + extract_pixel_value(pixel_dict,pixel_type,h,w+1)/16 + extract_pixel_value(pixel_dict,pixel_type,h+1,w+1)/16
    return value  

  try:
    pixel_dict = {}
    max_x = 0
    max_y = 0
    for x in one:
      print("x:",x)
      pixel_type, x, y, value = extract_ket_details(x)
      if int(x) > max_x:
        max_x = int(x)
      if int(y) > max_y:
        max_y = int(y)
      pixel_dict[pixel_type + ":" + x + ":" + y] = value
    print("finished for loop")
    max_x += 1
    max_y += 1
    print("max x:",max_x)
    print("max y:",max_y)
    #for i in range(k):
      
    pixel_list = superposition()
  except:
    return ket("failed to smooth image")            

# 2/3/2016:
# time to revisit image load. I have some new ideas how I want to handle it now:
# load-image[image.png] |>
# returns: |image: 200 200: AF36782BA...>
# ie, we are creating an image data-type. Much more efficient than the superposition idea.
# After that, save-image, edge-enhance[20], and image-ngrams[5] (where an image-ngram is partitioning an image into size k*k smaller images)
#
#from PIL import Image
def new_image_load(filename):
  logger.debug("image name: " + filename)
  def int_to_hex(x):
    return "%0.2X" % x
  
  try:
    im = Image.open(filename)
    logger.debug("imaged open")
    width = im.size[0]
    height = im.size[1]
    ket_image_string = "image: %s %s: " % (width,height)
    for h in range(height):
      for w in range(width):
        r, g, b = im.getpixel((w,h))[:3]                           # assumes image is RGB or RGBA, maybe fix later.
        ket_image_string += int_to_hex(r)
        ket_image_string += int_to_hex(g)
        ket_image_string += int_to_hex(b)
                  
# show the image:
#    im.show()
    return ket(ket_image_string)
  except:
    return ket("",0)
#    return ket("failed to load image")     

# 3/3/2016:
# image.histogram() looks interesting. With quick testing on the Lenna image, seems it would make a very nice first order image -> superposition mapping.
# image-histogram[image.png] |>
# Then test with a couple of examples.
#
def image_histogram(filename):
  try:
    im = Image.open(filename)
    result = superposition()
    for k,x in enumerate(im.histogram()):
      result.data.append(ket(str(k),x))                            # later swap in result += ket(str(k),x)
    return result      
  except:
    logger.debug("failed to load image")
    return ket("",0)

# 4/3/2016:
# time to revisit image save
# image-save[bah.png] image-load[foo.png] |>
# where image-save[some.png] takes input in the new image data type format: |image: 15 17: AB376C...>
# cool, seems to work!
#
def new_image_save(one,filename):
  try:
    datatype, size, data = one.label.split(": ")
    if datatype != "image":
      logger.debug("not image datatype")
      return one
    width,height = size.split(" ")
    width = int(width)
    height = int(height)
    expected_length = 6*width*height                             # It is hexadecimal, so 2+2+2 for RGB, times width*height
    if len(data) != expected_length:
      logger.debug("wrong image data length")
      return ket("")
  except:
    return ket("")                                                # on error do we want to return |> or 0|> ?? Or, in this case maybe we want to return one, the input superposition?

  size = (width,height)
  im = Image.new('RGB',size)
  image_data = []
  for triple in [data[i:i+6] for i in range(0, len(data), 6)]:
    print("triple: " + triple)  
    r = int(triple[0:2],16)
    g = int(triple[2:4],16)
    b = int(triple[4:6],16)
    print("R:",r)
    print("G:",g)
    print("B:",b)
    image_data.append((r,g,b))
  im.putdata(image_data)    
  im.show()
#  im.save(filename)
  return ket("making progress!")
    
# convert float to int if possible:
def float_to_int(x,t=3):
  if float(x).is_integer():
    return str(int(x))
#  return str("%.3f" % x)
  return str(round(x,t))


# 29/1/2015:
# table[C,F,K] range(|c: 0>,|C: 100,|10>)         readable_display
# ie, create a pretty printed table:
# table[C,F,K] range(|C: 0>,|C: 50>,|10>)
# +-------+-----------+-----------+
# | C     | F         | K         |
# +-------+-----------+-----------+
# | C: 0  | F: 32.00  | K: 273.15 |
# | C: 10 | F: 50.00  | K: 283.15 |
# | C: 20 | F: 68.00  | K: 293.15 |
# | C: 30 | F: 86.00  | K: 303.15 |
# | C: 40 | F: 104.00 | K: 313.15 |
# | C: 50 | F: 122.00 | K: 323.15 |
# +-------+-----------+-----------+
#
# 10/2/2015: now with "extract-value" operator applied automatically, we now have:
#  F |*> #=> F |_self>
#  K |*> #=> K |_self>
#  table[C,F,K] range(|C: 0>,|C: 50>,|10>)
# +----+--------+--------+
# | C  | F      | K      |
# +----+--------+--------+
# | 0  | 32.00  | 273.15 |
# | 10 | 50.00  | 283.15 |
# | 20 | 68.00  | 293.15 |
# | 30 | 86.00  | 303.15 |
# | 40 | 104.00 | 313.15 |
# | 50 | 122.00 | 323.15 |
# +----+--------+--------+
#
# Finally! Took way, way longer than expected, but it works!!!!
#
# maybe table should apply clean? Decided on set-to[1]
#
# Now we have 4 permutations: table[], strict-table[], rank-table[], strict-rank-table[]
# hrmm... strict-rank-table has a bug!
#
# also, now with table code, should not be much work to convert sw => csv.
#
def pretty_print_table(one,context,params,strict=False,rank=False):
  #logger.debug("one: " + str(one))
  ops = params.split(',')         
  if "coeff" in ops:                                  # yup. seems to work.
    coeff_col = [ float_to_int(x.value) for x in one] # see float_to_int() for number of decimal places. Currently 3.
  if len(ops) == 2 and ops[1] == "*":                # display all supported ops, instead of having to specify them manually.
    ops = [ops[0]] + [x.label[4:] for x in one.apply_op(context,"supported-ops")] 
  #logger.debug("ops: " + str(ops))
# set all coeffs to 1. A table where the incoming superposition has coeffs is ugly, and I can't think of a use case.
# easy enough to comment this line out, if we want:    # we need a way to occasionally show the coeffs of the incoming superposition. Don't yet know how!
  one = one.apply_sigmoid(set_to,1)   
  columns = []
  max_col_widths = []
  if rank:                                           # display rank option is on.
    col = [str(k + 1) for k in range(len(one))]      # start at 1, not 0.
    max_width = 4                                    # len("rank") == 4
    if len(col) > 0:
      max_width = max(4,len(col[-1]))                # longest element in col will be the last one.
    columns.append(col)
    max_col_widths.append(max_width)
  for k,op in enumerate(ops):
    if k == 0:                                       # don't process the incoming superposition
#      col = [x.readable_display() for x in one]      # first op is treated as a label
#      col = [x.apply_fn(extract_value).readable_display() for x in one]          # swapped in "extract-value".
      col = [x.apply_fn(remove_leading_category).readable_display() for x in one]          # swapped in "remove_leading_category".
    elif op == "coeff":
      col = coeff_col
    else:                                                                        # I currenlty think it is the right approach 
#      col = [x.apply_op(context,op).readable_display() for x in one]            # and don't want yet another table variant (extract-value vs not)
#      col = [x.apply_op(context,op).apply_fn(extract_value).readable_display() for x in one]  # "where-live" in foaf-example-in-sw.sw looks like needs categories!
      col = [x.apply_op(context,op).apply_fn(remove_leading_category).readable_display() for x in one]  # hopefully remove_leading_category will help with the foaf-example-in-sw.sw case.
    max_width = 0
    if len(col) > 0:
      max_width = max(len(y) for y in col)   # max() bugs out if applied to an empty list             
    max_width = max(max_width,len(op))
    columns.append(col)
    max_col_widths.append(max_width)
  #logger.debug("max_col_widths: " + str(max_col_widths))
  #logger.debug("columns: " + str(columns))
#  return ket("bug!")
  hpre = "+-"
  hmid = "-+-"
  hpost = "-+\n"
  hfill = "-"
  header = hpre + hmid.join(hfill*w for w in max_col_widths) + hpost
# logger.debug("header: " + str(header))        
  pre = "| "
  mid = " | "
  post = " |\n"
  if rank:
    ops = ["rank"] + ops
  label_header = pre + mid.join(op.ljust(max_col_widths[k]) for k,op in enumerate(ops)) + post
# logger.debug("label_header: " + str(label_header))
  s = header + label_header + header
#  return ket("bug!")
  for k in range(len(one)):
    row = [columns[col_idx][k] for col_idx in range(len(columns))]
    if strict and '' in row:
      continue
    srow = pre + mid.join(row[col_idx].ljust(max_col_widths[col_idx]) for col_idx in range(len(columns))) + post
    s += srow
  s += header
  print(s)
  
# code to save the table (useful for big ones, too hard to cut and paste from the console)
  logger.info("saving to: saved-table.txt")
  file = open("saved-table.txt",'w')
  file.write("sa: table[" + params + "]\n")
  file.write(s)
  file.close()  
  
  return ket("table")
  

# 3/2/2015: decided to natural sort for sort-by[], so need this: 
# http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
# 6/8/2014: Doh! There is a bug in sorting things like 0 vs 00 vs 000.
def natural_sorted(list, key=lambda s:s):
    """
    Sort the list into natural alphanumeric order.
    """
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
    sort_key = get_alphanum_key_func(key)
#    list.sort(key=sort_key)
    return sorted(list,key=sort_key)

#
# 1/2/2015: sort-by[op] some-superposition
# 
# what happens if some of the op |x> have differnet types from op |y> say?
#
# may tweak the method of sorting later. Not 100% happy yet, but close.   
# 3/2/2015: yup. Swapped in natural sort. Seems to work correctly.
def sort_by(one,context,op):
  def extract_ket_details(x):
    return x.apply_op(context,op).the_label().lower() 

  try:                                                             # maybe a sort by ket label?? Or is that just ket-sort?
    working_sp = [[k,extract_ket_details(x)] for k,x in enumerate(one) ]
    sorted_sp = natural_sorted(working_sp, key=lambda x: x[1])
    print("working sp:",working_sp)
    print("sorted sp:",sorted_sp)
    result = superposition()
    result.data = [one.data[k] for k,null in sorted_sp]            # yup, broke sp abstraction twice in one line! 
    return result                                                  # fix when we finally merge in fast_sp.
  except:
    return ket("",0)

# 22/2/2015:
# such-that[op] SP
# returns |x> if op is true/yes, |> otherwise.
# assumes one is a ket
#
# tweak: such-that[op1,op2,...] SP
# returns |x> if true/yes for all operators, |> otherwise.
#
# what happens if we have 0.3|yes>? ie, if coeff < 0.5 I think we want that ket ignored.  
#
def ket_such_that(one,context,ops):     # what happens if coeff != 1, eg 0?
  for op in ops.split(','):
#    label = one.apply_op(context,op).the_label().lower()
    e = one.apply_op(context,op).ket()
    label = e.label
    value = e.value
    if label not in ["true","yes"]:
      return ket("",0)
    if value < 0.5:                # need to test this bit.
      return ket("",0)
  return one

# 28/4/2016:
# tweak such-that[op] so it is a sp -> sp function, instead of a ket -> ket function. Should be an optimization, with a better big-O.  
def sp_such_that(one,context,ops):
  def valid_ket(one,context,ops):
    for op in ops.split(','):
      e = one.apply_op(context,op).ket()
      if e.label not in ["true","yes"]:
        return False
      if e.value < 0.5:                # need to test this bit.
        return False
    return True       
  result = superposition()
  result.data = [ x for x in one if valid_ket(x,context,ops) ]
  return result
      
# 2/2/2015:
# int-coeffs-to-sentence (3|apple> + 2|pear> + |orange> + 7|lemon>)
# |3 apples, 2 pears, 1 orange and 7 lemons>
#def int_coeffs_to_sentence(one,context):

#2/2/2015:
# int-ceoffs-to-word (3|apple> + 2|pear> + |orange> + 7|lemon>)
# |3 apples> + |2 pears> + |1 orange> + |7 lemons>
#
# Here is one common usage, combine it with list-to-words:
# sa: list-to-words int-coeffs-to-word (|apple> + 3|mouse> + 2|tooth> + 9|cat>)
# |1 apple, 3 mice, 2 teeth and 9 cats>
#
# assumes one is a ket
def int_coeffs_to_word(one,context):                      # at some point maybe we want float_coeffs_to_word??
  label = one.label
  value = int(one.value)
  if value == 0:
    value = "no"
  if value != 1:
    label = one.apply_op(context,"plural").the_label() # .the_label() to make sure it is a ket.    
    if label == '':
      label = one.label                                  # maybe return |> if plural not known? or the fed in ket? The fed in ket, is the correct way to do this.
  return ket(str(value) + " " + label)


from time import sleep
# 3/2/2015:
# sleep for 5 seconds: sleep[5]
def bko_sleep(one,time):
  sleep(float(time))
  return one

# 4/2/2015:
# map: 3752 -> 3,752
# map: 29872 -> 29,872
# and so on.
# I don't understand how "{:,}".format(value) works, but copied from here: 
# http://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators
#  
# desired exmples:
# to-comma-number |8825 => |8,825>
# to-comma-number |population: 230000 => |population: 2,300,00>
# to-comma-number |3759.27 => |3,759.27>
# to-comma-number |km: 22956.53 => |km: 22,9356.53>
# Tested, and it works!
#
# assumes one is a ket.
def number_to_comma_number(one):
  cat, value = extract_category_value(one.label)
  try:
    if float(value).is_integer():
      value = int(value)
    else:
      value = float(value)
  except:
    return one
  if len(cat) > 0:
    cat += ": "
  return ket(cat + "{:,}".format(value),one.value)

# current date, and current time:
import datetime
def current_date(one):
  return ket("date: " + str(datetime.date.today()))

# buggy! Not my local time. Not sure how to fix yet!
from time import gmtime, strftime  
def current_time(one):
#  return ket("time: " + str(datetime.datetime.now().time()))
#  return ket("time: " + str(datetime.datetime.now().strftime('%H:%M:%S')))
  return ket("time: " + strftime('%H:%M:%S', gmtime()))



# 9/2/2015: working towards a BKO rambler
# extract-3-tail |a b c d e f g h> == |f g h>
# example usage:
# ramble |*> #=> merge-labels(|_self> + | > + pick-elt next-2 extract-3-tail |_self>)
#
# assumes one is a ket
def extract_3_tail(one):
  split_str = one.label.rsplit(' ',3)
  if len(split_str) < 4:
    return one
  return ket(" ".join(split_str[1:]))

# 19/7/2015: working towards a BKO letter rambler
# extract-3-tail-chars |abcdefgh> == |fgh>
# example usage:
# letter-ramble |*> #=> merge-labels(|_self> + pick-elt next-2-letters extract-3-tail-chars |_self>)
#
# assumes one is a ket
def extract_3_tail_chars(one):
  chars = one.label[-3:]
  return ket(chars)

  
  
# TODO:
# greater-than[51] SP
# greater-equal-than[30] SP
# less-than[3] SP
# equal[37] SP
# in-range[300,700]
# we already have in-range sigmoid.
# maybe they should all be sigmoids??
# yeah, but then all the push-float, pop-float, and drop is needed.
#
# eg:
# is-greater-than[3] |5> == |5>
# is-greater-than[7] |6> == |>
# is-greater-than[13] |age: 14> == |age: 14>
# assumes one is a ket
def greater_than(one,t):
  try:    
    value = float(one.label.rsplit(": ",1)[-1]) # NB: if one is not a ket, one.label fails, and the exception is tripped. Neat!
  except:
    return ket("",0)
  if value > t:
    return one
  return ket("",0)

def greater_equal_than(one,t):
  try:    
    value = float(one.label.rsplit(": ",1)[-1])
  except:
    return ket("",0)
  if value >= t:
    return one
  return ket("",0)

def less_than(one,t):
  try:    
    value = float(one.label.rsplit(": ",1)[-1])
  except:
    return ket("",0)
  if value < t:
    return one
  return ket("",0)

def less_equal_than(one,t):
  try:    
    value = float(one.label.rsplit(": ",1)[-1])
  except:
    return ket("",0)
  if value <= t:
    return one
  return ket("",0)

def equal(one,t):          # name clash with equal(SP1,SP2)??
  epsilon = 0.0001         # Need code since equal and float don't work well together.
  try:    
    value = float(one.label.rsplit(": ",1)[-1])
  except:
    return ket("",0)
  if (t - epsilon) <= value <= (t + epsilon):
    return one
  return ket("",0)

def in_range(one,t1,t2):
  try:    
    value = float(one.label.rsplit(": ",1)[-1])
  except:
    return ket("",0)
  if t1 <= value <= t2:
    return one
  return ket("",0)

# 21/2/2015: round[3] |number: 3.1415> == |number: 3.142>
# assumes one is a ket, t is an integer
#
def old_round_numbers(one,t):
  cat, value = extract_category_value(one.label)
  try:
    value = float(value)
  except:
    return one
  if len(cat) > 0:
    cat += ": "
  rounded_value = round(value,t)
  if rounded_value.is_integer():
    rounded_value = int(rounded_value)
  return ket(cat + str(rounded_value))

# 14/1/2016:
# Instead of just round_numbers(), let's implement a more general numbers_fn().
# Eventually we want: round[3], times-by[2], divide-by[7], plus[5.2], minus[9], and maybe others.
#
# foo() is a 2 param fn, one is a ket, t is number
def numbers_fn(foo,one,t):
  try:
    cat, value = one.label.rsplit(': ', 1)
    value = float(value)
  except:
    try:
      cat = ''
      value = float(one.label)
    except:
      return one                            # not sure best thing to return for this case.
  if len(cat) > 0:
    cat += ": "
  result_value = foo(value,t)
  if result_value.is_integer():
    result_value = int(result_value)
  return ket(cat + str(result_value),one.value)

def round_numbers(one,t):               # cool, this one seems to work. Now need to do the rest.
  return numbers_fn(round,one,t)
  
def times_numbers(one,t):               # cool, times_numbers, and plus_numbers both seem to work!
  def multiply(a,b):
    return a*b
  return numbers_fn(multiply,one,t)
  
def plus_numbers(one,t):
  def add(a,b):
    return a+b
  return numbers_fn(add,one,t)

def mod_numbers(one,t):
  def mod(a,b):
    return a % b
  return numbers_fn(mod,one,t)        

def is_mod_numbers(one,t):
  def mod(a,b):
    return a % b
  return equal(numbers_fn(mod,one,t),0).is_not_empty()        


# to-coeff 12|> == |>
# to-ceoff 26|a: b> == 26| >
#
# assumes one is a ket
def to_coeff(one):
  if one.label == "":
    return ket("",0)
  return ket(" ",one.value)
  
  
  
# one off use:
# extract year from movie name:
# eg:
# extract-year |movie: Nykytaiteen museo (1986)> == |year: 1986>
# 
# one is a ket
def extract_year(one):
  year = one.label[-5:-1]
  return ket("year: " + year)

# ket-length
# eg: ket-length |abcde> == |number: 5>
#
def ket_length(one):
  return ket("number: " + str(len(one.label)))
  
  
# function to pretty print seconds
# from here: http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
# eg: 
# >>> display_time(33)
# '33 seconds'
# >>> display_time(3600)
# '1 hour'
# >>> display_time(3640)
# '1 hour, 40 seconds'
# >>> display_time(10987341908)
# '18166 weeks, 6 days, 7 hours, 25 minutes, 8 seconds'
#
old_intervals = (
  ('weeks', 604800),  # 60 * 60 * 24 * 7
  ('days', 86400),    # 60 * 60 * 24
  ('hours', 3600),    # 60 * 60
  ('minutes', 60),
  ('seconds', 1),
  )

def old_display_time(float_seconds):
# cast to int:
  seconds = int(float_seconds)           # it wasn't handling decimal places correctly anyway, so may as well cast to int.
  result = []

  for name, count in intervals:
    value = seconds // count
    if value:
      seconds -= value * count
      if value == 1:
        name = name.rstrip('s')
      result.append("{} {}".format(value, name))
  if len(result) == 0:
    return str("%.4f" % float_seconds) + " seconds"
  return ', '.join(result)

# 11/3/2015: I tweaked so can handle ms too.
intervals = (
  ('weeks', 604800000),  # 1000 * 60 * 60 * 24 * 7
  ('days', 86400000),    # 1000 * 60 * 60 * 24
  ('hours', 3600000),    # 1000 * 60 * 60
  ('minutes', 60000),    # 1000 * 60
  ('seconds', 1000),     # 1000
  ('milliseconds',1),
  )

def display_time(seconds):
  ms = int(1000 * seconds)
  result = []

  for name, count in intervals:
    value = ms // count
    if value:
      ms -= value * count
      if value == 1:
        name = name.rstrip('s')
      result.append("{} {}".format(value, name))
  if len(result) == 0:
    return "0"
  return ', '.join(result)


# 6/3/2015:
# display-algebra:
# display-algebra (3|x*x> + 2|y> + |z> + 13| >)      
# 3*x*x + 2*y + z + 13
#
# what a mess! Surely we can write it neater than this!!!
# seems to work though.
#
# one is a superposition
def display_algebra(one):
  result = []
  for x in one:
    if x.label == '':                # should never be true, since it should be taken care of elsewhere.
      continue
    if x.value == 1:
      coeff = ""
    else:
      coeff = str(float_to_int(x.value)) + "*"
    if x.label.strip() == '':
      term = coeff.rstrip("*")
      if term == "":
        term = "1"
    else:
      term = coeff + x.label
    result.append(term)
  return ket(" + ".join(result))


# 24/3/2015: we need this for find_unique
# though if we had fast_superpostion in place, we probably wouldn't need it.
# converts superposition to ordered dictionary
#
def sp_to_dict(one):
  r = OrderedDict()
  for elt in one:
    r[elt.label] = elt.value
  return r

# 24/3/2015:
# find-unique[names]
#
# unique-names |male name>
# unique-names |female name>
# unique-names |last name>
#
# yup. seems to work! And is fast! 4 days estimated for the names.sw data, down to 2 seconds, 753 milliseconds
def find_unique(context,op):
  kets = context.relevant_kets(op)
  print("kets:",kets)
  sp_list = [[x.label,sp_to_dict(x.apply_op(context,op))] for x in kets]
  print("sp-list:",sp_list)
  
  for your_label,your_dict in sp_list:
    other_dict = {}
    for label,the_dict in sp_list:
      if label != your_label:
        other_dict.update(the_dict)
    result = superposition()        
    result.data = [ket(key,your_dict[key]) for key in your_dict if key not in other_dict]  # because we use dictionaries, presumably there will be no duplicate kets.
    print(your_label,"result:",result)
    context.learn("unique-" + op,your_label,result)   
  return ket("find-unique")
  
# 2/6/2015:
# find-inverse[op]
#
# hrmm... I wonder if it should be shifted from context class to here?
# I mean, it does seem a very close brother with find-unique[op], yet that is here and not in context class. Shouldn't they be in the same spot?
# Is it faster to have create-inverse[op] in the context class? Yeah, probably quite a bit faster than going via apply_op() and context.recall()!
# does that mean I should move find_unique to the context class?   
#
def find_inverse(context,op):
  context.create_inverse_op(op)
    
  

# 26/3/2015:
# just a simple one:
# mbr(|x>,SP)
# returns the coeff of |x> in SP, if 0 or not in set return |>
# Note, you can consider this an optimization of: intn(|x>,SP), but having tested it, I'm not sure it is much of one!
# though I haven't looked at exact timings. Maybe I should.
# Note though that when we swap in fast_sp, this will drop from O(n) to roughly O(1).   
#
def mbr(e,two):
  e = e.ket()
  value = two.find_value(e)
  if value == 0:
    return ket("",0)
  return ket(e.label,value)

# 19/1/2/2016:
# is-mbr(|x>,SP) returns |yes> if |x> is in the SP, |no> otherwise.
# eg:
# friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
# sa: is-mbr(|Ed>,friends |Fred>)
# |yes>
# sa: is-mbr(|Frank>,friends |Fred>)
# |no>
#
def is_mbr(e,two):
  return mbr(e,two).is_not_empty()
  

# 9/4/2015:
# subset(one,two)
# returns degree of subsetness of one with respect to two.
# now, need to test it! Seems to work!
#
def subset(one,two):
  if one.count_sum() == 0:           # prevent div by 0.
    return ket("",0)
  value = intersection(one,two).count_sum()/one.count_sum()
  return ket("subset",value)

# 14/4/2015:
# starts-with |a: b: > returns |a: b: c>, |a: b: c: d> and so on.
# eg, we can now do: starts-with |person: Fred > to list all people with first name Fred.
#
# e is a ket
def starts_with(e,context):
  return context.starts_with(e)

# apply-weights[5,3,2] SP
#
def apply_weights(one,weights):
  weights = weights.split(",")
  result = superposition()
  for k,x in enumerate(one):
    if k >= len(weights):
      break
    result += x.multiply(float(weights[k]))
  return result

    
# rank (|a> + |b> + |c>)
# 1|a> + 2|b> + 3|c>
#
# one is a superposition
def rank(one):
  r = superposition()
  for k, (label, value) in enumerate(one.items()):
    r.add(label, k+1)
  return r


# lower-case, upper-case, sentence-case
#
# one is a ket
def lower_case(one):
  return ket(one.label.lower(),one.value)

def upper_case(one):
  return ket(one.label.upper(),one.value)

#from the_semantic_db_code import fast_superposition
# one-gram |text: just some text>
# two-gram |text: just some more text>
#
# one is a ket
def one_gram(one):
  text = one.label
  if text.startswith('text: '):
    text = text[6:]
#  result = fast_superposition()
  result = superposition()
  for x in text.split():                        # update to use the 2-gram word-split method?
    for y in x.split('\\n'):                    # what about escaped \n?
      result += ket(y)                          # what about non-char words? eg, "This is a sentence." is returned as |this> + |is> + |a> + |sentence.>
#  return result.superposition()                # actually, maybe the "read" operator fixed this. Yup. Use that instead.
  return result

def create_word_n_grams(s,N):
  return [" ".join(s[i:i+N]) for i in range(len(s)-N+1)]

def create_letter_n_grams(s,N):
  return ["".join(s[i:i+N]) for i in range(len(s)-N+1)]


def two_gram(one):
  text = one.label if type(one) == ket else one
  if text.startswith('text: '):
    text = text[6:]

#  text = "".join(c for c in text.lower() if c in 'abcdefghijklmnopqrstuvwxyz\'- ').split() # not sure this is exactly what we want!
  words = [w for w in re.split('[^a-z0-9_\']',text.lower().replace('\\n',' ')) if w]

  result = superposition()
  for w in create_word_n_grams(words,2):
    result += ket(w)
  return result

def three_gram(one):
  text = one.label if type(one) == ket else one
  if text.startswith('text: '):
    text = text[6:]

  words = [w for w in re.split('[^a-z0-9_\']',text.lower().replace('\\n',' ')) if w]

  result = superposition()
  for w in create_word_n_grams(words,3):
    result += ket(w)
  return result

def make_ngrams(one,parameters,ngram_type):
  logger.debug("one: " + str(one))
  logger.debug("parameters: " + parameters)
  logger.debug("ngram-type: " + ngram_type)
  sizes = parameters.split(',')
  for k in sizes:                 # check our sizes are all integers. The list should be short, so the O(n) is very cheap.
    if not k.isdigit():
      return ket("",0)
  
  text = one.label if type(one) == ket else one
  if text.startswith('text: '):
    text = text[6:]

  if ngram_type == "word":
    words = [w for w in re.split('[^a-z0-9_\']',text.lower().replace('\\n',' ')) if w]       # do we want .lower() in there?
    create_ngram_fn = create_word_n_grams
  elif ngram_type == "letter":
    words = list(text)
    create_ngram_fn = create_letter_n_grams
  else:
    return ket("",0)

#  result = fast_superposition()           # seems to bug out. 
  result = superposition()
  for k in sizes:
    for w in create_ngram_fn(words,int(k)):
      result += ket(w)
#  return result.superposition()
  return result      
       
      
  
# 30/4/2015:
# plus-or-minus |x> returns |+ x> + |- x>
# plus-or-minus |+ x> returns |+ x> + |- x>
# plus-or-minus |- x> returns |- x> + |+ x>
# not sure what we want for: plus-or-minus plus-or-minus |x>
#
# one is a ket
def plus_or_minus(one):
  if one.label.startswith('+ '):
    return one + ket("- " + one.label[2:],one.value)
  if one.label.startswith('- '):
    return one + ket("+ " + one.label[2:],one.value)
  return ket("+ " + one.label,one.value) + ket("- " + one.label,one.value)
 

#
def average_categorize(context,parameters):
  try:
    op,t,phi,ave = parameters.split(',')
    t = float(t)
  except:
    return ket("",0)
    
  one = context.relevant_kets(op)
  print("one:",one)
  out_list = []
  for x in one:
    print("x:",x)
    r = x.apply_op(context,op)
    print("r:",r)
    best_k = -1
    best_simm = 0
    for k,sp in enumerate(out_list):
      similarity = silent_simm(r,sp)
      if similarity > best_simm:
        best_k = k
        best_simm = similarity
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append(r)
    else:
      k = best_k
#      out_list[k] += r
      out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
  for k,sp in enumerate(out_list):
    print("sp:",sp)
    context.learn(ave,phi + ": " + str(k+1),sp)
  return ket("average categorize")

# 25/11/2015:
# unique-categorize. If it works as hoped, a kind of principle component thingy.
# How do we test this thing?? Maybe the simple images example?
# Hrmm.. might be able to use this (a thing I recall from linear algebra): https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process
# Instead of <u,v> being standard dot-product, use simm(u,v). Might just work.
# I don't think this will be the unique_categorize I'm after, but should still be useful. And also as a starting point.
#
# Hrm... I don't think I know what I am doing here. I need to give it a lot more thought!    
#
def unique_categorize(context,parameters):
  try:
    op,t,phi,ave = parameters.split(',')
    t = float(t)
  except:
    return ket("",0)
    
  one = context.relevant_kets(op)
  print("one:",one)
  out_list = []
  for x in one:
    print("x:",x)
    r = fast_superposition() + x.apply_op(context,op)    # Yeah, a hack. But using fast_sp is the easiest way to do the "find-unique" step.
    print("r:",r)
    best_k = -1
    best_simm = 0
    for k,sp in enumerate(out_list):
      similarity = silent_simm(r,sp)
      if similarity > best_simm:
        best_k = k
        best_simm = similarity
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append(r)
    else:
      k = best_k
#      out_list[k] += r
      out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
    for k1,sp1 in enumerate(out_list):
      tmp_sp = fast_superposition()
      for k2,sp2 in enumerate(out_list):
        if k1 != k2:
          tmp_sp += sp2
# ...           
      
  for k,sp in enumerate(out_list):
    print("sp:",sp)
    context.learn(ave,phi + ": " + str(k+1),sp.superposition()) # need to convert fast_sp back to sp. Yeah, when am I going to finally swap in fast_sp full time?? 
  return ket("average categorize")


# 5/5/2016:
# New idea, a tweak to average-categorize, so now it has a suppress element to it.
# I don't know if this will work or not, but I will test soon.  
def average_categorize_suppress(context,parameters):
  try:
    op,t,phi,ave = parameters.split(',')
    t = float(t)
  except:
    return ket("",0)
    
  w = 1                                            # w = 0 should reproduce standard version. w = 1 hopefully makes final sp's more "orthogonal"
  one = context.relevant_kets(op)
  print("one:",one)
  out_list = []
  for x in one:
    print("x:",x)
    r = x.apply_op(context,op)
    print("r:",r)
    best_k = -1
    best_simm = 0
    for k,sp in enumerate(out_list):
      similarity = silent_simm(r,sp)
      if similarity > best_simm:
        best_k = k
        best_simm = similarity
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append(r)
    else:
      for k in range(len(out_list)):
        if k == best_k:
          out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
        else:
          if w != 0:
            similarity = silent_simm(r,out_list[k])
            out_list[k] += r.multiply(-w*similarity)   # suppress r from this pattern, w chooses how much. Alternatively, put a .drop() in here.
  for k,sp in enumerate(out_list):
    print("sp:",sp)
    context.learn(ave,phi + ": " + str(k+1),sp.drop())
  return ket("average categorize")

# 6/5/2016:
# a list-average-categorize-suppress(). Hopefully converting sp's to lists, the simm will be faster, and also handle negative values if needed.
#
# 7/5/2016: in testing so far, w != 0 doesn't work so great.
#
#import numpy as np                      # yeah, another dependence. 
def list_average_categorize_suppress(context,parameters):
  try:
    op,t,phi,ave = parameters.split(',')
    t = float(t)
  except:
    return ket("",0)

  def simple_sp_to_list(sp):              # need to test these two, but I think they are correct.
    r = np.array([x.value for x in sp])
    return r
  def list_to_simple_sp(data):
    r = superposition()
    r.data = [ ket(str(k),x) for k,x in enumerate(data) ]
    return r
  def rescale(arr):
    arr = arr - arr.min()
    if arr.max() == 0:
      return arr
    arr = arr*255/arr.max()                            # maybe try rescale to [0,255] later. Bug, what about max == 0?
    return arr
    
  #w = 0.01                                            # w = 0 should reproduce standard version. w = 1 hopefully makes final sp's more "orthogonal"
  w = 0                                                # switch it off for now
  one = context.relevant_kets(op)
  print("one:",one)
  out_list = []
  for x in one:
    print("x:",x)
    r0 = x.apply_op(context,op)
    r = simple_sp_to_list(r0)
    print("r:",r)
    best_k = -1
    best_simm = 0
    for k,sp in enumerate(out_list):
#      similarity = silent_simm(r,sp)
      similarity = rescaled_list_simm([1],r,sp)
      if similarity > best_simm:
        best_k = k
        best_simm = similarity
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append(r)
    else:
      for k in range(len(out_list)):
        if k == best_k:
#          out_list[k] += r*best_simm  # reweight based on result of simm.  # bug! a + b for lists is append, not add in place.
          out_list[k] = out_list[k] + r*best_simm                   # bug! a*b for a list, b scalar does not work as expected either! numpy to the rescue!
#          out_list[k] = rescale(out_list[k] + r*best_simm)           # trying another idea. Rescale each time.
        else:
          if w != 0:
            similarity = rescaled_list_simm([1],r,out_list[k])
            out_list[k] = out_list[k] - r*w*similarity              # suppress r from this pattern, w chooses how much. Alternatively, put a .drop() in here.
  for k,sp in enumerate(out_list):
    print("sp:",sp)
#    context.learn(ave,phi + ": " + str(k+1),sp.drop())             # NB: we can't use drop, as that will break our sp to image code
#    context.learn(ave,phi + ": " + str(k+1),list_to_simple_sp(sp).apply_sigmoid(pos))
    context.learn(ave,phi + ": " + str(k+1),list_to_simple_sp(rescale(sp))) # final rescale didn't seem to make much difference
    context.learn(ave,phi + ": " + str(k+1),list_to_simple_sp(sp)) 
  return ket("average categorize")


# 6/5/2016:
# average-categorize-suppress has 2 issues: 
# 1) I'm not sure it is designed to work with sp's with negative coeffs. ie, silent_simm() is the problem. So maybe a more general version?
# 2) it is slow! Maybe swap in a sp to list step, and use scaled-list-simm() in place of silent_simm()?
def bah__average_categorize_suppress(context,parameters):
  try:
    op,t,phi,ave = parameters.split(',')
    t = float(t)
  except:
    return ket("",0)
    
  w = 1                                            # w = 0 should reproduce standard version. w = 1 hopefully makes final sp's more "orthogonal"
  one = context.relevant_kets(op)
  print("one:",one)
  out_list = []
  for x in one:
    print("x:",x)
    r = x.apply_op(context,op)
    print("r:",r)
    best_k = -1
    best_simm = 0
    for k,sp in enumerate(out_list):
      similarity = silent_simm(r,sp)
      if similarity > best_simm:
        best_k = k
        best_simm = similarity
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append(r)
    else:
      for k in range(len(out_list)):
        if k == best_k:
          out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
        else:
          if w != 0:
            similarity = silent_simm(r,out_list[k])
            out_list[k] += r.multiply(-w*similarity)   # suppress r from this pattern, w chooses how much
  for k,sp in enumerate(out_list):
    print("sp:",sp)
    context.learn(ave,phi + ": " + str(k+1),sp.drop())
  return ket("average categorize")
  

# 5/8/2015:
# split-chars |abcde> == |a> + |b> + |c> + |d> + |e>
#
# one is a ket
def split_chars(one):
  try:
    chars = list(one.label)
    result = superposition()
    for c in chars:
      result += ket(c)
    return result
  except:
    return ket("",0)

# select-chars[a,b] |uvwxyz>
# eg: select-chars[3,4,7] |abcdefgh> == |cdg>
# should it be similar to select[1,5]? I think we are breaking that.
# maybe we need to distinguish between select-range and select-elts
# or, a better option, allow: select-chars[3,5,7,13-19,23,31-41] |...>
# and we would have to do the same for superposition select[] too.
# OK. I like that idea. Not sure if current parser can handle that. I need to check.  
# 
# and what about: select-chars[1,3] |abcdef> == |a> + |c> ?? 
# presumably the just written: split-chars will do that for us.
#
# what about indexing from the end of the list?
# do we have a reverse ket-label function operator?
# And I'm starting to get annoyed with adding all these little things! I know I promised we could add new ones without bounds, but still, I'm getting sick of this!   
#
# one is a ket
def select_chars(one,positions):
  try:
    positions = positions.split(",")
    chars = list(one.label)
    text = "".join(chars[int(x)-1] for x in positions if int(x) <= len(chars))
    return ket(text)
  except:
    return ket("",0)   
                                                                                                          

import hashlib
# 24/8/2015:
# ket-hash[size] |some ket>
#
# one is a ket
def ket_hash(one,size):
  logger.debug("ket-hash one: " + str(one))
  logger.debug("ket-hash size: " + size)
  try:
    size = int(size)
  except:
    return ket("",0)
  our_hash = hashlib.md5(one.label.encode('utf-8')).hexdigest()[-size:]
  return ket(our_hash,one.value)

import zlib
# 19/6/2016:
# hash-compress (|a> + |b> + |c> + |d>)
#
# sa: hash-compress split |a b c d>
# |620062> + |630063> + |640064> + |650065>
#
# one is a ket
def hash_compress(one):
  our_hash = zlib.adler32(one.label.encode('utf-8'))
  return ket("%0.2X" % our_hash,one.value) 
  
  
# 24/8/2015:
# hash-data[size] SP
#
# one is a superposition
def hash_data(one,size):
  logger.debug("hash-data one: " + str(one))
  logger.debug("hash-data size: " + size)
  try:
    size = int(size)
  except:
    return ket("",0)
  array = [0] * (16**size)
  for x in one:
    our_hash = hashlib.md5(x.label.encode('utf-8')).hexdigest()[-size:]
    k = int(our_hash,16)
    array[k] += 1 * x.value
  logger.info("hash-data writing to tmp-sp.dat")
  f = open('tmp-sp.dat','w')
  for k in array:
    f.write(str(k) + '\n')
  f.close()
  return ket("hash-data")

# eg: process-reaction(current-sp,2|H2> + |O2>,2|H2O>) == current-sp - (2|H2> + |O2>) + 2|H2O>
# Cool. Seems to work.
# 16/2/2016: maybe process-consuming-reaction() is a better name, to tie in with process-catalytic-reacion()
#
# one, two and three are superpositions
def process_reaction(one,two,three):
  def del_fn(x,y):   # NB: creates negative coeffs.
    return x - y
  if intersection(two,one).count_sum() != two.count_sum():
    return one
  else:
    return intersection_fn(del_fn,one,two).drop() + three              # can we do superposition subtraction? Maybe implement it?? Meaning: one - two + three

# 16/2/2016:
# process-catalytic-reaction(current-sp,|a> + |b>,|c> +|d>) = current-sp + |c> + |d> if |a> + |b> is in current-sp
# What if |c> + |d> is already in current-sp? Do you add it again?
# I suspect process-catalytic-reaction() can be used to encode maths proofs. One is the current state of knowledge. Two is the necessary conditions for the proof to be true. Three is the implications of that proof.
# Another example is simple physics problems. You write down what you know, and any possibly relevant equations. Then try to figure out a pathway to the desired result.  
#
def process_catalytic_reaction(one,two,three):
  if intersection(two,one).count_sum() != two.count_sum():
    return one
  else:
    return one + three

# 31/10/2016:
# rewrite(SP,|s1>,|s2>)
# replace all instances of string "s1" with "s2" in SP
# simple, but powerful. cf. productions: https://en.wikipedia.org/wiki/Production_(computer_science)
# Doh! Already implemented long ago as "rename_kets" with essentially identical code!
#
# one is a sp, s1 and s2 are kets
def rewrite(one,s1,s2):
  string1 = s1.the_label()
  string2 = s2.the_label()
  r = superposition()
  for x in one:
    y_label = x.label.replace(string1,string2)
    r += ket(y_label,x.value)
  return r     

# x,y are floats
def filter_fn(x,y):
  if x == 0:
    return 0
  return y
  
# filter-down-to(|b> + 3|c>,|a> + 5|b> + 0.7|c> + 9|d> + 3.2|e>) == 5|b> + 0.7|c>
#
# one, two are superpositions
def filter_down_to(one,two):
  return intersection_fn(filter_fn,one,two).drop()

# respond-to-pattern(current-sp,pattern,consequence)
# heh. I forgot what this even does! 
#
# one, two and three are superpositions
def respond_to_pattern(one,two,three):
  r = filter_down_to(two,one)
  similarity = silent_simm(r,two)
  return one + three.multiply(similarity)
  

# 26/11/2015:
# Let's try to implement edit-distance using operators.
# https://en.wikipedia.org/wiki/Edit_distance
#
#def edit_insert(one,parameters):
#def edit_delete():
#def edit_substitute():
#
# 17/12/2015: let's finally get to this.
# start with:
# delete[k,0]
# insert[s,0]
#
# It works:
# LCS distance: 
# sa: insert[g,6] insert[i,4] delete[e,4] insert[s,0] delete[k,0] |kitten>
# |sitting>
#
# Levenshtein distance:
# sa: insert[g,6] substitute[i,e,4] substitute[s,k,0] |kitten>
# |sitting>
#
# one is a ket
# delete[k,0]
def edit_delete(one,parameters):                # cool. Seems to work!
  try:
    char,k = parameters.split(',')
    k = int(k)
    text = one.label
    if text[k] == char:
      result = text[:k] + text[k+1:]
    return ket(result,one.value)
  except:
    return one

# insert[s,0]
def edit_insert(one,parameters):
  try:
    char,k = parameters.split(',')
    k = int(k)
    text = one.label
    result = text[:k] + char + text[k:]
    return ket(result,one.value)
  except:
    return one

# substitue[s,k,0]
def edit_substitute(one,parameters):
  try:
    char1,char2,k = parameters.split(',')
    k = int(k)
    text = one.label
    if text[k] == char2:
      text = text[:k] + char1 + text[k+1:]
    return ket(text,one.value)
  except:
    return one
    

# 9/2/2016:
# guess-ket |fred>          -- return the best matching known ket (using simm and so on)
# guess-ket[3] |Sam>        -- return the best 3 matching known kets, providing simm > 0
# guess-ket[*] |robbie>     -- return all matching known kets, providing simm > 0
#
# could do with some optimization!
#
# one is a ket
def guess_ket(one,context,t='1'):
  def process_string(s):
    one = ket(s.lower())                                            # I presume we want s.lower(). Maybe sometimes we don't? 
    return make_ngrams(one,'1,2,3','letter')
  try:
    guess = process_string(one.label)
    r = superposition()
    for x in context.relevant_kets("*"):                            # what about kets that are only on the right hand side of a learn rule? This misses them. One way is run "create inverse", but is there a better way?
#      similarity = silent_simm(guess,process_string(x.label))
      similarity = fast_simm(guess,process_string(x.label))
      if similarity > 0:
        r.data.append(x.multiply(similarity))                         # later swap in r += x.multiply(similarity)
    if t == '*':
      return r.coeff_sort()
    else:
      return r.coeff_sort().select_range(1,int(t))    
  except:
    return ket("",0)

# 9/2/2016:
# guess-operator[age]          -- return the best matching known operator (using simm and so on)
# guess-operator[friend,3]     -- return the best 3 matching known operators, providing simm > 0
# guess-operator[mother,*]     -- return all matching known operators, providing simm > 0
#
def guess_operator(context,parameters):
  try:
    op,t = parameters.split(',')
    if t != '*':
      t = int(t)
  except:
    op = parameters
    t = 1
  def process_string(s):
    one = ket(s.lower())
    return make_ngrams(one,'1,2,3','letter')
  try:
    guess = process_string(op)
    r = superposition()
    for x in context.supported_operators():  
      similarity = silent_simm(guess,process_string(x.label[4:]))   # need to convert 'op: age' to 'age'
      r.data.append(x.multiply(similarity))                         # later swap in r += x.multiply(similarity)
    if t == '*':
      return r.drop().coeff_sort()
    else:
      return r.drop().coeff_sort().select_range(1,t)    
  except:
    return ket("",0)
    
# 9/2/2016:
# rename_kets: 
# takes a superposition (one), and for each ket replaces the string in ket two with the string in ket three
#
# one is a superposition, two and three are kets.
def rename_kets(one,two,three):
  try:
    s1 = two.the_label()
    s2 = three.the_label()
    result = superposition()
    for x in one:
      y = ket(x.label.replace(s1,s2),x.value)
#      result.data.append(y)                                         # later swap in result += y. data.append is buggy in case the string replace creates duplicate kets
      result += y
    return result
  except:
    return ket("",0) 


# 20/3/2016:
#
# path-op[op] sp
# eg:
# op |A> => |B: 1> + |C: 2> + |G: 3>
# op |B> => |A: 4> + |D: 5> + |H: 6>
#
# then:
# path-op[op] |B: 1>
# == |A: 1: 4> + |D: 1: 5> + |H: 1: 6>
#
# one is a ket (so linear in kets), op is a string
def path_op(one,context,op):
  try:
    split_ket_string = one.label.split(': ',1)
    element = split_ket_string[0]
    rule = context.recall(op,element)
    if len(split_ket_string) == 1:
      return rule
    path_history = split_ket_string[1]
    print("element:",element)
    print("path_history:",path_history)
    print("rule:",rule)
    r = superposition()
    for x in rule:
      x_element, x_path_history = x.label.split(': ',1)
      r += ket('%s: %s: %s' % (x_element,path_history,x_path_history))
    return r      
  except Exception as e:
    print("reason:",e)  
    return ket("",0)
    
# 10/5/2016:
# implement my idea for simm-add[op,p]
# where:
# R0 = r0
# R_k = R_k-1 + r_k * [simm(R_k-1,r_k)]^p
#
# how on Earth do we test this thing??
# Hrmm... result seems essentially identical, to say 1% or less, with just adding them! At least for p = 1,2. I tried p = 100, and still not much difference. 
#
def simm_add(one,context,parameters):
  try:
    op,p = parameters.split(',')
    p = int(p)                     # maybe try float(p) later
  except:
    return ket("",0)

  head, *tail = one
  Rk = head.apply_op(context,op)
  for x in tail:
    rk = x.apply_op(context,op)
    similarity = silent_simm(Rk,rk)**p
    Rk = Rk + rk.multiply(similarity)
  return Rk

# now, in our digit recognition task, it is clear that some features are far more common than others. eg white space
# so the question is, how best to normalize this a bit. 
# Currently I'm using log(1 + x) which maps the test case of 1000 test images from 70.9% to 72.1%
# Recall best algo's give 98%, so I have a lot of work to do yet!!
# Next idea is ket normalization. ie, reweight kets so that on average, each ket "fires" at the same rate
# Hopefully it will encode the idea that frequently firing kets are less interesting than rarely firing ones.
# In BKO, this:
# -- these are our starting superpositions:
#    the |sp1> => a1|A> + b1|B> + c1|C>
#    the |sp2> => a2|A> + b2|B> + c2|C>
#    the |sp3> => a3|A> + b3|B> + c3|C>
#    the |sp4> => a4|A> + b4|B> + c4|C>
#
# -- the sum of our superpositions:
#    the-sum |sp> => the (|sp1> + |sp2> + |sp3> + |sp4)
#
# -- these are what we want our code to learn:
#    norm-ket |A> => 1/(a1 + a2 + a3 + a4) |A>
#    norm-ket |B> => 1/(b1 + b2 + b3 + b4) |B>
#    norm-ket |C> => 1/(c1 + c2 + c3 + c4) |C>
#
# -- this is intended usage once we have them (probably implemented with map)
#    the-normed |sp1> => norm-ket the |sp1>
#    the-normed |sp2> => norm-ket the |sp2>
#    the-normed |sp3> => norm-ket the |sp3>
#    the-normed |sp4> => norm-ket the |sp4>
#
# -- test our code works:
#    norm-ket the-sum |sp> == |A> + |B> + |C>
# 
# 
def learn_ket_normalizations(context,parameters):
  try:
    op1,op2,t = parameters.split(',')
    t = float(t)
  except:
    return ket("",0)

  the_kets = context.relevant_kets(op1)
  the_sum = superposition()
  for x in the_kets:
    the_sum += x.apply_op(context,op1)
  for x in the_sum:
    if x.value <= 0:
      continue
    y = ket(x.label)
    context.learn(op2,y,y.multiply(t/x.value))
  return ket("ket-norms")
      

# append-column[n] SP
# for use in Hierarchical Temporal Memory sequence learning
# append-column[5] |X> == |X: 0> + |X: 1> + |X: 2> + |X: 3> + |X: 4>
# Cool! In testing it works just fine.
# and has the property:
# extract-category append-column[10] |X> == 10 |X>
#
# one is a ket, N is a positive integer
def append_column(one,N):
  try:
    N = int(N) 
  except:
    return ket("",0)

  r = superposition()
  for k in range(N):
    r += ket("%s: %s" % (one.label,k),one.value)
  return r

import random
# random-column[n] SP
# for use in Hierarchical Temporal Memory sequence learning
# random-column[5] |X> == pick-elt( |X: 0> + |X: 1> + |X: 2> + |X: 3> + |X: 4>)
# and has the property:
# extract-category random-column[10] |X> == |X>
#
# one is a ket, N is a positive integer
def random_column(one,N):
  try:
    N = int(N) 
  except:
    return ket("",0)

  random_integer = random.randint(0,N-1)
  return ket("%s: %s" % (one.label,random_integer),one.value)

# 28/7/16:
# usage:
# have-in-common (|Fred> + |Sam> + |Jack>)
# 0.7 |op: friends> + |op: age> + 0.5|op: parents>
#
def have_in_common(one,context):
  logger.debug("have-in-common one: %s" % str(one))
  
  if len(one) == 0:
    return ket("",0)
  for sp in one:
    supported_ops = sp.apply_op(context,"supported-ops")
    break
  for sp in one:
    tmp = sp.apply_op(context,"supported-ops")
    supported_ops = intersection(supported_ops,tmp)
  if len(supported_ops) == 0:
    return ket("",0)                 
# ... finish


def bar_chart(one,width,sorted=False):
  if len(one) == 0:
    return ket("bar chart")
  try:
    width = int(width)
  except:
    return ket("bar chart")
  max_len = max(len(x.label) for x in one)
#  print("max_len:",max_len)
#  two = one.coeff_sort().rescale(width).apply_sigmoid(floor)
  if sorted:
    two = one.coeff_sort().rescale(width)
  else:
    two = one.rescale(width)
  mid = ' : '
  print("----------")
  for x in two:
    print(x.label.ljust(max_len) + mid + '|'*int(x.value))
  print("----------")
  return ket("bar chart")      


# 15/9/2016:
# recall a learned high-order sequence, and print it out.
# see:
# Using the proposed swc language: 
# (which I'm never going to be able to write a compiler for! and is almost certainly going to be a tar-pit)
#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# current |node> => start-node |input ket>
# while name current |node> /= |end of sequence>:
#   print name current |node>
#   current |node> => next current |node>
# print |end of sequence>
#
# one is a ket
def recall_sequence(one,context):
  if len(one.apply_op(context,"start-node")) == 0:                  # we don't know the start-node, so return the input ket
    return one
  print("recall sequence:",one)
  context.learn("current","node",one.apply_op(context,"start-node"))
  name = context.recall("current","node").apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  while name.the_label() != "end of sequence":
    print(name)
    context.learn("current","node",ket("node").apply_op(context,"current").similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then"))
    name = context.recall("current","node").apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
#  print(name)
  return name

# recall a chunked high order sequence, and print it out.
#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# not |yes> => |no>
# not |no> => |yes>
#
# if not do-you-know start-node |input ket>:
#   return |input ket>
# current |node L2> => start-node |input ket>
# while name current |node L2> /= |end of sequence>:
#   current |node L1> => start-node name current |node L2>
#   while name current |node L1> /= |end of sequence>:
#     print name current |node L1>
#     current |node L1> => next current |node L1>
#   current |node L2> => next current |node L2>
# print |end of sequence>
#
# one is a ket
def recall_chunked_sequence(one,context):
  if len(one.apply_op(context,"start-node")) == 0:                  # we don't know the start-node, so return the input ket
    return one
  print("recall chunked sequence:",one)
  context.learn("current","node L2",one.apply_op(context,"start-node"))
  name2 = context.recall("current","node L2").apply_fn(extract_category).similar_input(context,"encode").select_range(1,1)
  while name2.the_label() != "end of sequence":

    context.learn("current","node L1",name2.apply_op(context,"start-node"))
    name1 = context.recall("current","node L1").apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
    while name1.the_label() != "end of sequence":
      print(name1)
      context.learn("current","node L1",ket("node L1").apply_op(context,"current").similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then"))
      name1 = context.recall("current","node L1").apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)

    context.learn("current","node L2",ket("node L2").apply_op(context,"current").similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then"))
    name2 = context.recall("current","node L2").apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  return name2


# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# not |yes> => |no>
# not |no> => |yes>
#
# spell (*) #=>
#   if not do-you-know first-letter |_self>:
#     return |_self>
#   current |node> => first-letter |_self>
#   while name current |node> /= |end of sequence>:
#     print name current |node>
#     current |node> => next current |node>
#   return |end of sequence>
#
# code to spell words
#
# one is a ket
def spell(one,context):
  start = one.apply_op(context,"first-letter")
  if len(start) == 0:                  # we don't know the first letter, so return the input ket
    return one
  print("spell word:",one)
  context.learn("current","node",start)
  name = context.recall("current","node",True).apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  while name.the_label() != "end of sequence":
    print(name)
#    bar_chart(name,'80')
    context.learn("current","node",ket("node").apply_op(context,"current").similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then"))
    name = context.recall("current","node",True).apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
#  print(name)
  return name
  

# 25/9/2016:
# recall a learned chunked high-order sequence, of arbitrary depth, and print it out.
#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# NB: this pseudo-code is out of date! Update it!!
# if not do-you-know start-node |input ket>:
#   return |input ket>
# current |node> => start-node |input ket>
# while name current |node> /= |end of sequence>:
#   print name current |node>
#   current |node> => next current |node>
# print |end of sequence>
#
# Let's try to update the pseudo-code:
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# print-sequence (*,*) #=>
#   if not do-you-know start-node |_self1>:
#     return |_self1>
#   if name start-node |_self1> == |_self1>:                  -- prevent infinite loop
#     print |_self1>
#     return |>
#   |node> => |_self2>
#   current "" |node> => start-node |_self1>
#   while name current "" |node> != |end of sequence>:
#     if not do-you-know start-node name current "" |node>:
#       print name current "" |node>
#     else:
#       print-sequence(name current "" |node>, plus[1] "" |node>)
#     current "" |node> => next current "" |node>
#   return |end of sequence>
#
# Invoke using:
# print-sequence(|alphabet>, |seq node: 1>)              -- need a version that doesn't need to pass in the sequence node! Need a GUID generator! How implement that??
#
# one is a ket
def print_sequence(one,context,start_node=None,node_id=1):
  if start_node is None:                                          # so we can change the operator name that links to the first element in the sequence.
    start_node = "start-node"
  if len(one.apply_op(context,start_node)) == 0:                  # we don't know the start-node, so return the input ket
    return one
  print("print sequence:",one)
  if one.apply_op(context,start_node).apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean).the_label() == one.the_label():  # need to implement 'sp1 == sp2' at some stage. 
    print(one)                                                   # infinte loop when object is its own sequence.
    return ket("")  
  node = "seq node: " + str(node_id)
  context.learn("current",node,one.apply_op(context,start_node))
  name = context.recall("current",node).apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  while name.the_label() != "end of sequence": 
    has_start_node = name.apply_op(context,start_node)
    if len(has_start_node) == 0:
      print(name)      
    else:
      print_sequence(name,context,start_node,node_id + 1)
    context.learn("current",node,ket(node).apply_op(context,"current").similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then"))
    name = context.recall("current",node).apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  return name

#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# print-sequence |*> #=>                                      -- I don't see the advantage of this function over the python! Why should my language exist?? 
#   if not do-you-know start-node |_self>:
#     return |_self>
#   if name start-node |_self> == |_self>:                    -- prevent infinite loop
#     print |_self>
#     return |>
#   |node> => new-GUID |>                                     -- feels like a hack! 
#   current "" |node> => start-node |_self>
#   while name current "" |node> != |end of sequence>:
#     if not do-you-know start-node name current "" |node>:
#       print name current "" |node>
#     else:
#       print-sequence name current "" |node>
#     current "" |node> => next current "" |node>
#   return |end of sequence>
#
# Invoke using:
# print-sequence |alphabet>                 
#
def new_print_sequence(one,context,start_node=None):
  if start_node is None:                                          # so we can change the operator name that links to the first element in the sequence.
    start_node = "start-node"
  if len(one.apply_op(context,start_node)) == 0:                  # if we don't know the start-node, return the input ket
    return one
  print("print sequence:",one)

  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
    
  if name(one.apply_op(context,start_node)).the_label() == one.the_label():  # need to implement 'sp1 == sp2' at some stage so we don't need .the_label() 
    print(one)                                                               # prevent infinte loop when object is its own sequence. Maybe should have handled at learn stage, not recall?
    return ket("")  
  current_node = one.apply_op(context,start_node)  
  while name(current_node).the_label() != "end of sequence":
    if len(name(current_node).apply_op(context,start_node)) == 0:
      print(name(current_node))      
    else:
      new_print_sequence(name(current_node),context,start_node)
    current_node = next(current_node)
  return ket("end of sequence")


# 29/9/2016:
# discrimination. The difference in coeff between the highest and the next highest
# Bah! Seems I have already implemented it over in the ket and sp classes. 
#
def discrimination(one):
  if len(one) == 0:
    return ket("discrimination",0)
  if len(one) == 1:
    return ket("discrimination")
  r = one.coeff_sort().normalize()
  first = r.data[0].value                                 # yeah, breaks the superposition class abstraction. Fix later!
  second = r.data[1].value
  return ket("discrimination",first-second)
  
  
# 5/10/2016
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# follow-sequence (*) #=>
#   current |node> => |_self>
#   while name current |node> /= |end of sequence>:
#     print name current |node>
#     current |node> => next current |node>
#   return |end of sequence>
#
# code to follow a sequence
#
# one is a sp
def old_follow_sequence(one,context):
  if len(one) == 0:
    return one
  context.learn("current","node",one)
  name = context.recall("current","node",True).apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  while name.the_label() != "end of sequence":
    print(name)
    context.learn("current","node",ket("node").apply_op(context,"current").similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then"))
    name = context.recall("current","node",True).apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  return name
  
# 17/11/2016
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# follow-sequence[op] (*) #=>
#   current |node> => |_self>
#   while name current |node> /= |end of sequence>:
#     op name current |node>                              -- NB: "op" instead of "print"
#     current |node> => next current |node>
#   return |end of sequence>
#
# code to follow a sequence
#
# one is a sp
def follow_sequence(one,context,op=None):
  if len(one) == 0:
    return one
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)    
    
  current_node = one  
  while name(current_node).the_label() != "end of sequence":
    if op == None:
      print(name(current_node))      
    else:
      name(current_node).apply_op(context,op)
    current_node = next(current_node)
  return ket("end of sequence")
  
# 25/11/2016:
# code to display a sequence in dot format. eg: |the> . |dog> . |sat>
#
# one is a sp
def display_sequence(one,context,op=None):
  if len(one) == 0:
    return one
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)    
    
  current_node = one  
  node_names = []
  while name(current_node).the_label() != "end of sequence":
    if op == None:
#      node_names.append(str(name(current_node)))
      node_names.append(name(current_node).the_label())          
    else:
      name(current_node).apply_op(context,op)
    current_node = next(current_node)
#  print(" . ".join(node_names))
  print("|%s>" % " . ".join(node_names))
  return ket("end of sequence")


# 20/11/2016:
# code to recall a sentence
# hrm... seems to work. Needs tidying though.
#
# Usage:
# load sentence-sequence--multi-layer.sw 
# print-sentence |*> #=> recall-sentence pattern |_self>
# print-sentence |node 200: 1>
#
#
# one is a sp
def recall_sentence(one,context):
  if len(one) == 0:
    return one
  current_node = one
#  current_node = one.apply_op(context,"pattern")
#  if len(current_node) == 0:
#    return one
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def old_has_start_node(one):                                            # check if one is a class
    two = ket(one.the_label() + ": 1")                                # this breaks if you use: |A: 0> or |A: 1> for your first node. What is a tidy fix?
    return len(two.apply_op(context,"start-node")) > 0

  def has_start_node(one):                                            # check if one is a class
    two = ket(one.the_label() + ": ")                                 # see if this fixes the |A: 0> vs |A: 1> as first node bug.
    return len(two.apply_fn(starts_with,context).select_range(1,1).apply_op(context,"start-node")) > 0

# python: x.apply_op(context,"append-colon").apply_fn(starts_with,context).pick_elt().apply_op(context,"start-node").apply_sp_fn(follow_sequence,context)
  def get_start_node(one):
    two = ket(one.the_label() + ": ")
    return two.apply_fn(starts_with,context).pick_elt().apply_op(context,"start-node")        
   
  while name(current_node).the_label() != "end of sequence":
    if not has_start_node(name(current_node)):
      print(name(current_node))
    else:
#      print("%s has start node" % name(current_node))
      start_node = get_start_node(name(current_node))
      recall_sentence(start_node, context)       
    current_node = next(current_node)
  return ket("end of sequence")
    

# 23/11/2016:
# hopefully improved version of recall-sentence:
# usage: recall-sentence-v2 sentence |R>
#
# one is a sp
def recall_sentence_v2(one,context):
  if len(one) == 0:
    return one
#  current_node = one
  current_node = one.apply_op(context,"pattern")
  if len(current_node) == 0:
    return one
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
#  def has_start_node(one):                                            # check if one is a class
#    return len(one.apply_op(context,"start-nodes")) > 0
  def get_start_node(one):
    return one.apply_op(context,"start-nodes").weighted_pick_elt()             # need clean?        
 
  while name(current_node).the_label() != "end of sequence":
    start_node = get_start_node(name(current_node))
    if len(start_node) == 0:                                           # check if one is a class
      print(name(current_node))
    else:
      recall_sentence_v2(start_node, context)       
    current_node = next(current_node)
  return ket("end of sequence")

# 10/10/2016
# whats_next(sp)
# whats_next(sp,sp)
# whats_next(sp,sp,sp)
# ...
# ie, given learned high order sequences of SDR's, predict what the next SDR is going to be.
#
# then drop-below[t] similar-input[pattern] sp1
# then intersection(drop-below[t] similar-input[pattern] then drop-below[t] similar-input[pattern] sp1, drop-below[t] similar-input[pattern] sp2)
# then intersection(drop-below[0.09] similar-input[pattern] then drop-below[0.09] similar-input[pattern] input-encode |f>, drop-below[0.09] similar-input[pattern] input-encode |f>)
# or ...
# find-pattern (*) #=> drop-below[t] similar-input[pattern] |_self>
# then find-pattern sp1
# then intersection(find-pattern then find-pattern sp1, find-pattern sp2)
# then intersection(find-pattern then find-pattern then find-pattern sp1, find-pattern then find-pattern sp2, find-pattern sp3) 
#
# one is a sp
def whats_next_one(context,one):
  pattern = "pattern"
  then = "then"
  t = 0.09
  return one.similar_input(context,pattern).drop_below(t).apply_op(context,then)

# bah! I can't get it to work.... Not sure where the bug is.
# Hrmm... I think it is from "then similar-input[pattern]" applied to more than one pattern at a time.
# Maybe not. Since this works:
# next-step-op |*> #=> ket-sort similar-input[encode] extract-category then drop-below[0.09] similar-input[pattern] input-encode |_self>
#  
# one, two are sp's
def first_attempt_whats_next_two(context,one,two):
  pattern = "pattern"
  then = "then"
  t1 = 0.09
  t2 = 0.8
  nodes_one = one.similar_input(context,pattern).drop_below(t1).apply_op(context,then).similar_input(context,pattern).rescale() 
  nodes_two = two.similar_input(context,pattern).drop_below(t1)
#  return intersection(nodes_one,nodes_two).apply_op(context,then)
  print("nodes_one:",nodes_one)
  print("nodes_two:",nodes_two)
  return intersection(nodes_two,nodes_one)                             # I should look into optimizing intersection! 
  
# one, two and three are sp's
def whats_next_three(context,one,two,three):
  pattern = "pattern"
  then = "then"
  t = 0.09
  nodes_one = one.similar_input(context,pattern).drop_below(t).apply_op(context,then).similar_input(context,pattern).drop_below(t).apply_op(context,then).similar_input(context,pattern).drop_below(t) 
  nodes_two = two.similar_input(context,pattern).drop_below(t).apply_op(context,then).similar_input(context,pattern).drop_below(t) 
  nodes_three = three.similar_input(context,pattern).drop_below(t)
  return intersection(intersection(nodes_one,nodes_two),nodes_three).apply_op(context,then)       

# bah! Try another approach!
# I don't even know if it is correct!....
# 
# one, two are sp's
def whats_next_two(context,one,two):
  pattern = "pattern"
  then = "then"
  t1 = 0.09
  t2 = 0.8
  nodes_one = one.similar_input(context,pattern).drop_below(t1) 
  nodes_two = two.similar_input(context,pattern).drop_below(t1)
  r = superposition()
  for x in nodes_one:
#    y = x.apply_sigmoid(clean).apply_op(context,then).similar_input(context,pattern).drop_below(t1)               # maybe select[1,1] instead of drop-below
    y = ket(x.label).apply_op(context,then).similar_input(context,pattern).select_range(1,1).apply_sigmoid(clean)
#    z = intersection(y,nodes_two)                                          # value = two.find_value(e)
#    z = ket(nodes_two.find_value(y))
    z = mbr(y,nodes_two)
    r += z
  return r 
#  return intersection(nodes_one,nodes_two).apply_op(context,then)
#  print("nodes_one:",nodes_one)
#  print("nodes_two:",nodes_two)
#  return intersection(nodes_two,nodes_one)                             # I should look into optimizing intersection! 

# 24/11/2016:
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "a cat sat on the mat"
# Given a word, predict what word follows.
# eg: predict-whats-next(|a>) == |cat>
# eg: predict-whats-next(|the>) == 2|dog> + |ball> + |mat>
#
# Cool, seems to work. Next up, the 2 word version.
#
# later, implement a sequence version
#
# one is a sp
def predict_whats_next_one(context,one):
  if len(one) == 0:                                                      # if it is the empty sp, we can't do anything.
    return one
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def get_node(one):
    return one.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").drop_below(0.09)
  def then(one):
    return one.apply_op(context,"then")
  def follow_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(follow_sequence,context)

  nodes_one = get_node(one)
  print("nodes:", nodes_one)
  if len(nodes_one) == 1:
    return follow_node_sequence(nodes_one)
  
  r = superposition()
  for x in nodes_one:
    print(name(then(x)))
    r += name(then(x))
  return r

# 24/11/2016  
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "a cat sat on the mat"
# Given two words, predict what word follows.
# eg: predict-whats-next(|a>, |cat>) == |sat>
# eg: predict-whats-next(|the>, |dog>) == |wants> + |chased>
#
# Cool, seems to work. Next up, the three word version.
#
# later, implement a sequence version. I guess by passing in the relevant node of a sequence. 
#
# one and two are sp's
def predict_whats_next_two(context,one,two):
  if len(one) == 0:                                                      # if it is the empty sp, we can't do anything.
    return one
  if len(two) == 0:                                                      # if two == |> then feed it to the one word version of predict-whats-next() 
    return predict_whats_next_one(context,one)
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def get_node(one):
    return one.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").drop_below(0.09)
  def then(one):
    return one.apply_op(context,"then")
  def get_next_node(one):
    return one.similar_input(context,"pattern").select_range(1,1)            # .apply_sigmoid(clean).apply_op(context,"then")
  def follow_node_sequence(one):
#    return one.apply_op(context,"pattern").apply_sp_fn(follow_sequence,context)
    return one.apply_op(context,"then").apply_sp_fn(follow_sequence,context)
  
  nodes_one = get_node(one)
  print("nodes 1:", nodes_one)
  nodes_two = get_node(two)
  print("nodes 2:", nodes_two)
  next_nodes = superposition()
  for x in nodes_one:
    next_nodes += get_next_node(then(x))    
  intersected_nodes = intersection(next_nodes, nodes_two)
  print("intersected nodes:", intersected_nodes)
  if len(intersected_nodes) == 1:
    return follow_node_sequence(intersected_nodes)
  else:
    r = superposition()
    for x in intersected_nodes:
      print(name(then(x)))
      r += name(then(x))
    return r
        
# 25/11/2016
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "a cat sat on the mat"
# Given three words, predict what word follows.
# eg: predict-whats-next(|a>, |cat>, |sat>) == |on>
# eg: predict-whats-next(|the>, |dog>, |wants>) == |food>
#
# Cool, seems to work. Next up, the sequence version. Probably by passing in the start node of a sequence.
#
# one, two and three are sp's
def predict_whats_next_three(context,one,two,three):
  if len(one) == 0:                                                      # if it is the empty sp, we can't do anything.
    return one
  if len(two) == 0:                                                      # if two == |> then feed it to the one word version of predict-whats-next() 
    return predict_whats_next_one(context,one)
  if len(three) == 0:
    return predict_whats_next_two(context,one,two)
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def get_node(one):
    return one.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").drop_below(0.09)
  def then(one):
    return one.apply_op(context,"then")
  def get_next_node(one):
    return one.similar_input(context,"pattern").select_range(1,1)            # .apply_sigmoid(clean).apply_op(context,"then")
  def follow_node_sequence(one):
#    return one.apply_op(context,"pattern").apply_sp_fn(follow_sequence,context)
    return one.apply_op(context,"then").apply_sp_fn(follow_sequence,context)
  
  nodes_one = get_node(one)
  print("nodes 1:", nodes_one)
  nodes_two = get_node(two)
  print("nodes 2:", nodes_two)
  nodes_three = get_node(three)
  print("nodes 3:", nodes_three)

  next_nodes = superposition()
  for x in nodes_one:
    next_nodes += get_next_node(then(x))    
  intersected_nodes = intersection(next_nodes, nodes_two)
  print("intersected nodes:  ", intersected_nodes)
  if len(intersected_nodes) == 1:
    return follow_node_sequence(intersected_nodes)
  
  next_nodes2 = superposition()
  for x in intersected_nodes:
    next_nodes2 += get_next_node(then(x))    
  intersected_nodes2 = intersection(next_nodes2, nodes_three)
  print("intersected nodes 2:", intersected_nodes2)
  if len(intersected_nodes2) == 1:
    return follow_node_sequence(intersected_nodes2)
          
  r = superposition()
  for x in intersected_nodes2:
    print(name(then(x)))
    r += name(then(x))
  return r

# 25/11/2016:
# skip version. 
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "the very hungry dog wants some food"
# predict-whats-next-skip(|the>, |dog>) == 2|wants> + |chased>
# NB: the 2nd |wants> from the third sentence, where we skip "very hungry"
#
# seems to work.
#
# one and two are sp's
def predict_whats_next_skip_two(context,one,two):
  if len(one) == 0:                                                      # if it is the empty sp, we can't do anything.
    return one
  if len(two) == 0:                                                      # if two == |> then feed it to the one word version of predict-whats-next() 
    return predict_whats_next_one(context,one)
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def get_node(one):
    return one.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").drop_below(0.09)
  def then(one):
    return one.apply_op(context,"then")
  def get_next_node(one):
    return one.similar_input(context,"pattern").select_range(1,1)            # .apply_sigmoid(clean).apply_op(context,"then")
  def follow_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(follow_sequence,context)
  def display_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(display_sequence,context)    
  def get_next_nodes(one):
    r = superposition()
    for x in one:
      r += get_next_node(then(x))
    return r
  def name_next_nodes(one):
    r = superposition()
    for x in one:
      r += name(then(x))
    return r
  
  nodes_one = get_node(one)
  print("nodes 1:", nodes_one)
  nodes_two = get_node(two)
  print("nodes 2:", nodes_two)
  next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(get_next_nodes(get_next_nodes(nodes_one)))  # improve later.
  intersected_nodes = intersection(next_nodes, nodes_two)
  print("intersected nodes:", intersected_nodes)
#  if len(intersected_nodes) == 1:
#    return follow_node_sequence(intersected_nodes)
  for x in intersected_nodes:
    display_node_sequence(x)    
  return name_next_nodes(intersected_nodes)
 

# 25/11/2016:
# skip version. 
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "the very hungry dog wants some food"
# predict-whats-next-skip(|the>, |dog>) == 2|wants> + |chased>
# NB: the 2nd |wants> from the third sentence, where we skip "very hungry"
#
# seems to work.
#
# one, two and three are sp's
def predict_whats_next_skip_three(context,one,two,three):
  if len(one) == 0:                                                      # if it is the empty sp, we can't do anything.
    return one
  if len(two) == 0:                                                      # if two == |> then feed it to the one word version of predict-whats-next() 
    return predict_whats_next_one(context,one)
  if len(three) == 0:
    return predict_whats_next_skip_two(context,one,two)
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def get_node(one):
    return one.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").drop_below(0.09)
  def then(one):
    return one.apply_op(context,"then")
  def get_next_node(one):
    return one.similar_input(context,"pattern").select_range(1,1)            # .apply_sigmoid(clean).apply_op(context,"then")
  def follow_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(follow_sequence,context)
  def display_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(display_sequence,context)
  def get_next_nodes(one):
    r = superposition()
    for x in one:
      r += get_next_node(then(x))
    return r
  def name_next_nodes(one):
    r = superposition()
    for x in one:
      r += name(then(x))
    return r
  
  nodes_one = get_node(one)
  print("nodes 1:", nodes_one)
  nodes_two = get_node(two)
  print("nodes 2:", nodes_two)
  nodes_three = get_node(three)
  print("nodes 3:", nodes_three)
  
  next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(get_next_nodes(get_next_nodes(nodes_one)))  # improve later.
  intersected_nodes = intersection(next_nodes, nodes_two)
  print("intersected nodes  :", intersected_nodes)
#  if len(intersected_nodes) == 1:                           # slight "stutter". Not sure how to best fix. If at all.
#    return follow_node_sequence(intersected_nodes)          # eg: predict-whats-next-skip(|the>,|hungry>,|dog>) == |dog>.|wants>.|some>.|food>
                                                             # also: predict-whats-next-skip(|the>,|hungry>,|fish>) == |dog>.|wants>.|some>.|food>
  next_nodes2 = get_next_nodes(intersected_nodes) + get_next_nodes(get_next_nodes(intersected_nodes)) + get_next_nodes(get_next_nodes(get_next_nodes(intersected_nodes)))  # improve later. Also has slight tolerance for order changes.
  intersected_nodes2 = intersection(next_nodes2, nodes_three)                                                                                                              # bug or feature?
  print("intersected nodes 2:", intersected_nodes2)
#  if len(intersected_nodes2) == 1:                           # if len > 1, use pick-elt??
#    return follow_node_sequence(intersected_nodes2)
  for x in intersected_nodes2:
    display_node_sequence(x)
  return name_next_nodes(intersected_nodes2)
     
# one, two, three and four are sp's
def predict_whats_next_skip_four(context,one,two,three,four):
  if len(one) == 0:                                                      # if it is the empty sp, we can't do anything.
    return one
  if len(two) == 0:                                                      # if two == |> then feed it to the one word version of predict-whats-next() 
    return predict_whats_next_one(context,one)
  if len(three) == 0:
    return predict_whats_next_skip_two(context,one,two)
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def get_node(one):
    return one.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").drop_below(0.09)
  def then(one):
    return one.apply_op(context,"then")
  def get_next_node(one):
    return one.similar_input(context,"pattern").select_range(1,1)            # .apply_sigmoid(clean).apply_op(context,"then")
  def follow_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(follow_sequence,context)
  def display_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(display_sequence,context)
  def get_next_nodes(one):
    r = superposition()
    for x in one:
      r += get_next_node(then(x))
    return r
  def name_next_nodes(one):
    r = superposition()
    for x in one:
      r += name(then(x))
    return r
  
  nodes_one = get_node(one)
  print("nodes 1:", nodes_one)
  nodes_two = get_node(two)
  print("nodes 2:", nodes_two)
  nodes_three = get_node(three)
  print("nodes 3:", nodes_three)
  nodes_four = get_node(four)
  print("nodes 4:", nodes_four)
  
  next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(get_next_nodes(get_next_nodes(nodes_one)))  # improve later.
  intersected_nodes = intersection(next_nodes, nodes_two)
  print("intersected nodes  :", intersected_nodes)
  next_nodes2 = get_next_nodes(intersected_nodes) + get_next_nodes(get_next_nodes(intersected_nodes)) + get_next_nodes(get_next_nodes(get_next_nodes(intersected_nodes)))  # improve later. Also has slight tolerance for order changes.
  intersected_nodes2 = intersection(next_nodes2, nodes_three)                                                                                                              # bug or feature?
  print("intersected nodes 2:", intersected_nodes2)

  next_nodes3 = get_next_nodes(intersected_nodes2) + get_next_nodes(get_next_nodes(intersected_nodes2)) + get_next_nodes(get_next_nodes(get_next_nodes(intersected_nodes2)))  # improve later. Also has slight tolerance for order changes.
  intersected_nodes3 = intersection(next_nodes3, nodes_four)                                                                                                                  # bug or feature?
  print("intersected nodes 3:", intersected_nodes3)

  for x in intersected_nodes3:
    display_node_sequence(x)
  return name_next_nodes(intersected_nodes3)

# 29/11/2016:
# sequence version of  whats-next.
# eg: next |the . dog . chased> == |the . ball>
#
# one is a sequence ket, eg |the . dog . chased>, or |the . mother . of . george . is>
# sort of a hack until we make sequences first class objects, if we ever do.
#
#def sequence_predict_whats_next_skip(context,one):
def sequence_predict_whats_next_skip(one,context,parameters=None):
  if len(one) == 0:                                                      # if it is the empty sp, we can't do anything.
    return one
  try:
    k = int(parameters)
  except:
    k = 3
  incoming_sequence = [x.strip() for x in one.the_label().split('.')]
  print("incoming_sequence:",incoming_sequence)
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)
  def get_node(one):
    return one.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").drop_below(0.09)
  def then(one):
    return one.apply_op(context,"then")
  def get_next_node(one):
    return one.similar_input(context,"pattern").select_range(1,1)            # .apply_sigmoid(clean).apply_op(context,"then")
  def follow_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(follow_sequence,context)
  def display_node_sequence(one):
    return one.apply_op(context,"then").apply_sp_fn(display_sequence,context)
  def get_next_nodes(one):
    r = superposition()
    for x in one:
      r += get_next_node(then(x))
    return r
  def name_next_nodes(one):
    r = superposition()
    for x in one:
      r += name(then(x))
    return r
  
  nodes_one = get_node(ket(incoming_sequence[0]))
  
  for x in incoming_sequence[1:]:
    print("nodes 1:", nodes_one)
    nodes_two = get_node(ket(x))
#    next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(get_next_nodes(get_next_nodes(nodes_one))) + get_next_nodes(get_next_nodes(get_next_nodes(get_next_nodes(nodes_one))))
    next_nodes = get_next_nodes(nodes_one)
    r = next_nodes
    for _ in range(k):
      r = get_next_nodes(r)
      next_nodes += r
    intersected_nodes = intersection(next_nodes, nodes_two)
    print("intersected nodes:", intersected_nodes)
    nodes_one = intersected_nodes
  for x in nodes_one:
    display_node_sequence(x)
  return name_next_nodes(nodes_one)
    
  
  
      
# 5/11/2016:
# vsa-mult(sp1,sp2)
# eg:
# vsa-mult(|name>,|usa>) == |name: usa>
#
# one, two are superpositions
def vsa_mult(one,two):
  r = superposition()
  for x in one:
    for y in two:
      x_pieces = x.label.split(": ")
      y_pieces = y.label.split(": ")
      pieces = x_pieces + y_pieces
      print("pieces:",pieces)
      new_pieces = []
      for p in pieces:
        if p in x_pieces and p in y_pieces:                 # not pefect, but works for now.
          continue
        new_pieces.append(p)        
#      new_pieces.sort()
      r += ket(": ".join(new_pieces))
  return r

import random
from itertools import product
# 9/12/2016:
# random-frame[w,h,on-bits]
# display-frame[w,h] frame |3>
#
def random_frame(parameters):
  try:
    w,h,bits = [int(x) for x in parameters.split(',')]
    pixels = [x for x in product(range(w), range(h))]
    on_pixels = random.sample(pixels, bits)
    r = superposition()
    for pair in on_pixels:
      r += ket("%s: %s" % (pair[0], pair[1]))
    return r
  except Exception as e:
    print("random_frame exception reason:",e)
    return ket("")

def display_frame(one,parameters):
  try:
    w,h = [int(x) for x in parameters.split(',')]
    on_pixels = [x.label.split(": ") for x in one]
    on_pixels = [(int(x),int(y)) for x,y in on_pixels]                         # tidy later?
#    print("on-pixels: %s" % on_pixels)
    for y in range(h):
      for x in range(w):
        if (x,y) in on_pixels:
          print("#",end='')
        else:
          print(".",end='')
      print()
    print()  
    return ket("display-frame")
  except Exception as e:
    print("display_frame exception reason:",e)
    return ket("")
    
# display-frame-sequence[10,10] start-node |seq 1>
#
# one is a sp
def display_frame_sequence(one, context, parameters):
  if len(one) == 0:
    return one

  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"frame").select_range(1,1).apply_sigmoid(clean)
  def display_our_frame(one, parameters):
    display_frame(one.apply_fn(extract_category), parameters)      
    
  try:
    current_node = one.apply_op(context,"pattern")  
    while name(current_node).the_label() != "end of sequence":
  #    print(name(current_node))
  #    display_frame(name(current_node).apply_op(context,"frame"), parameters)
      display_our_frame(current_node, parameters)
      current_node = next(current_node)
    return ket("end of sequence")
    
  except Exception as e:
    print("display_frame_sequence exception reason:",e)
    return ket("")

   
    
  
# 6/6/2017:
# Given we have learnt this sequence: 
# |3> . |1> . |4> . |1> . |5>
# we want this output:
# sa: float-sequence |3.2>
# 0.992 |3> . |1> . |4> . |1> . |5>
# 0.191 |4> . |1> . |5>
#
# sa: float-sequence |1.3>
# 0.928 |1> . |4> . |1> . |5>
# 0.928 |1> . |5>
# 0.0   |3> . |1> . |4> . |1> . |5>
#
# Improved, so now handles sequence-names, and input sequences longer than 1:
# sa: load pi-e-sequences.sw
# sa: float-sequence |3.3 . 1 . 4.2>
# Pi  0.664  |3> . |1> . |4> . |1> . |5> . |9> . |2> . |6> . |5> . |3> . |5>
# Pi  0.078  |4> . |1> . |5> . |9> . |2> . |6> . |5> . |3> . |5>
# Pi  0.0    |5> . |3> . |5>
#
# sa: float-sequence |2 . 8 . 2>
# e  0.071  |1> . |8> . |2> . |8> . |1> . |8> . |2> . |8> . |4>
# e  0.071  |1> . |8> . |2> . |8> . |4>
# e  0.027  |2> . |8> . |1> . |8> . |2> . |8> . |4>
# e  0.027  |2> . |7> . |1> . |8> . |2> . |8> . |1> . |8> . |2> . |8> . |4>
# e  0.0    |2> . |8> . |4>
#
# NB: important for float_sequence to work that we have an appropriate "encode" operator defined.
# eg: encode |*> #=> rescale smooth[0.1]^10 |_self> 
#
# Now, the approximate mathematics this is doing:
# Given input sequence |v1> . |v2> . |v3>
# find x such that f(x) approx-eq v1 and f(x + delta) approx-eq  v2 and f(x + 2*delta) approx-eq v3
# where the exact meaning of "a approx-eq b" is a consequence of how you define your encode operator
#
def float_sequence(one, context, parameters=None):
  def similar_pattern(x, context):
    return x.apply_op(context,"encode").apply_fn(append_column,"10").similar_input(context,"pattern").multiply(10)
  
  def filter_working_table(table, element, position):
    #print("%s: %s" % (position, element))
    element_pattern = ket(element).apply_op(context, "encode")
    new_table = []
    for name, coeff, seq in table:
      try:
        seq_element = seq[position]
        seq_element_pattern = seq_element.apply_op(context, "encode")
        #print("seq_element:",seq_element)
        #print("seq_element_pattern:",seq_element_pattern)
        similarity = fast_simm(element_pattern, seq_element_pattern)
        #print("simm:",similarity)
        new_coeff = min(coeff, similarity)
        if new_coeff > 0:
          new_table.append([name, new_coeff, seq])
      except:
        continue
    return new_table

  def format_output_table(working_table):
    # first, sort the table:
    sorted_working_table = sorted(working_table, key = lambda x: x[1], reverse = True)

    # now format it:
    table = []
    for name, coeff, seq in sorted_working_table:
      coeff_str = float_to_int(coeff)
      seq_str = " . ".join(str(x) for x in seq)
      table.append([name, coeff_str, seq_str])
    return table
  
  # handle: float-sequence |3.2 . 1.3 . 4>:
  input_sequence = one.the_label().split(' . ')
  logger.info("input sequence: " + str(input_sequence))
  one = ket(input_sequence[0])
  
  # generate working_table:
  r = similar_pattern(one, context)
  working_table = []
  for x in r:
    name = x.apply_op(context, "sequence-name").the_label()
    coeff = x.value
    seq = sequence_to_list(x, context)
    working_table.append([name, coeff, seq])
    
  # filter working_table using the rest of our input sequence:
  for k, element in enumerate(input_sequence[1:]):
    working_table = filter_working_table(working_table, element, k + 1)       

  # don't format and print an empty table:
  if len(working_table) == 0:
    return ket("")
    
  # format and print output table:
  print_table(format_output_table(working_table))
  return ket("float-sequence")

def sequence_to_list(one, context, length = None):
  if len(one) == 0:
    return one
    
  def next(one):
    return one.similar_input(context,"pattern").select_range(1,1).apply_sigmoid(clean).apply_op(context,"then")
  def name(one):
    return one.apply_fn(extract_category).similar_input(context,"encode").select_range(1,1).apply_sigmoid(clean)    
    
  current_pattern = one.apply_op(context, "pattern")  
  node_names = []
#  print("one:",one)
#  print("current_pattern:", current_pattern)
#  print("name current_pattern:", name(current_pattern))
  while name(current_pattern).the_label() != "end of sequence":
#    node_names.append(str(name(current_pattern)))
    node_names.append(name(current_pattern))
    current_pattern = next(current_pattern)
  return node_names

# pretty print a table:
# table print tweaked from here: http://stackoverflow.com/questions/25403249/print-a-list-of-tuples-as-table
def print_table(table):
  max_length_column = []
  tuple_len = len(table[0])     # assume entire table has the same shape as the first row
  for i in range(tuple_len):
    max_length_column.append(max(len(e[i])+2 for e in table))
  for e in table:
    for i in range(tuple_len):
      print(e[i].ljust(max_length_column[i]), end='')
    print()

# spell-out |fish> => |f> . |i> . |s> . |h>
# AKA: ssplit |fish> => |f> . |i> . |s> . |h>
def spell_out(one):
  seq = sequence([])
  if type(one) in [ket, superposition]:
    for x in one:
      for c in list(x.label):
        seq += ket(c, x.value)
  return seq
  
def ssplit(one, split_char = ''):
  if split_char == '':
    def split_with(x):
      return list(x)
  else:
    def split_with(x):
      return x.split(split_char)
  seq = sequence([])
  if type(one) in [ket, superposition]:
    for x in one:
      for c in split_with(x.label):
        seq += ket(c, x.value)
  return seq
                                                                                                  
