#!/usr/bin/env python

#######################################################################
# the semantic-db class implementation file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 9/8/2015
# Copyright: GPLv3
#
# Usage: 
#
#######################################################################

import sys
import random
import copy
import re

from operator import mul

# put this here for now:
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

# 4/3/2015: I hate when integers are displayed as floats. Sorry, pet peeve. 
# convert float to int if possible:
def float_to_int(x,t=3):
  if float(x).is_integer():
    return str(int(x))
#  return str("%.3f" % x)
  return str(round(x,t))
  

# NB: I have not yet normalized kets vs superpositions in terms of supported functions.
# The basics are covered, but there are still gaps I'm too lazy to fill, ATM.
class ket(object):
  def __init__(self,label='?',value=1):
    self.label = label
    self.value = float(value)  # perhaps look into decimal type.
                               # http://docs.python.org/2/library/decimal.html
                               # nah. float seems appropriate.

  def __str__(self):
    return self.display()
    
  def __len__(self):
#    return 1                   # maybe if self.label == "", return 0?
    if self.label == '':
      return 0
    return 1

  # 6/1/2014: finally implement iterator. 
  def __iter__(self):
    yield ket(self.label,self.value)

  def type(self):
    return "ket"

  def old_display(self):
    if self.value == 1:
      return '|' + self.label + '>'
    else:
      return str(self.value) + '|' + self.label + '>'

# probably slower. Need to do a speed test, and see if significant.
# tweaked for exact display, so dump to file and load again don't accidentally zero coeffs.
  def display(self,exact=False):
    if self.value == 1:
      return "|{0}>".format(self.label)
    elif exact:
      return str(self.value) + '|' + self.label + '>'
    else:
#      return "{0:.3f}|{1}>".format(self.value,self.label)
      return float_to_int(self.value,3) + '|' + self.label + '>'

  def long_display(self):
#    return self.display()
    if self.value == 1:
      return self.label
    else:
      return str("%.3f" % self.value) + '    ' + self.label
    
  def readable_display(self):
    if self.label == '':
      return ""
    if self.value == 1:
      return self.label
    else:
      if self.value.is_integer():
        return "{0:.0f} {1}".format(self.value,self.label)
      return "{0:.2f} {1}".format(self.value,self.label)      
        

  def transpose(self):
    return bra(self.label,self.value)

  def __add__(self,x):
    return superposition() + self + x
    
# 14/1/2015:
# I think this is right ...  
  def clean_add(self,x):
    return (superposition() + self).clean_add(x)

  def apply_bra(self,a_bra):
    return apply_bra_to_ket(a_bra,self)

  # maybe an apply_projection too?

  def probably_buggy_apply_fn(self,fn,t1=None,t2=None):  # Bug? What happens if the result is |> or contains |>?
    if t1 == None:                        # Bug? What happens if fn() is a superposition?
      return fn(self)
    elif t2 == None:
      return fn(self,t1)
    else:
      return fn(self,t1,t2)

  def apply_fn(self,fn,t1=None,t2=None):  # Bug? What happens if the result is |> or contains |>?
    #print("boop")
    result = fast_superposition()
    if t1 == None:                        # Bug? What happens if fn() is a superposition?
      r = fn(self)
    elif t2 == None:
      r = fn(self,t1)
    else:
      r = fn(self,t1,t2)
    return (result + r).superposition()


  def apply_fn_collapse(self,fn,t=None):
    if t == None:
      return fn(self)
    return fn(self,t)

  def apply_sp_fn(self,fn,t1=None,t2=None,t3=None,t4=None):
    if t1 == None:
      return fn(self)
    elif t2 == None:
      return fn(self,t1)
    elif t3 == None:
      return fn(self,t1,t2)
    elif t4 == None:
      return fn(self,t1,t2,t3)
    else:
      return fn(self,t1,t2,t3,t4)

# need to check this works.     # seems to.
  def apply_naked_fn(self,fn,t1=None,t2=None,t3=None):
    if t1 == None:
      return fn()
    elif t2 == None:
      return fn(t1)
    elif t3 == None:
      return fn(t1,t2)
    else:
      return fn(t1,t2,t3)


  def apply_op(self,context,op):
    return context.recall(op,self,True)  # see much later in the code for definition of recall.

# apply the same op more than once.
# especially useful for networks.
  def apply_op_multi(self,context,op,n):
    result = copy.deepcopy(self)
    for k in range(n):
      result = result.apply_op(context,op)
    return result

  def select_elt(self,k):
    if k != 1 and k != -1:
      return ket("",0)
    else:
      return ket(self.label,self.value)
      
# 5/2/2015: eg: without this: select[1,5] "" |bah> bugs out if "" |bah> is not defined.
# seems to work!
  def select_range(self,a,b):      
    if a <= 1 <= b:
      return ket(self.label,self.value)
    return ket("",0)
    
# 6/8/2015:
  def index_split(self,k):                      # OK. Now need to test it. Maybe improve for k other than {1,-1}.
    if k == 1:
      return ket(self.label,self.value), ket("")
    if k == -1:
      return ket(""), ket(self.label,self.value) 
  
  def pick_elt(self):
    return ket(self.label,self.value)

  def weighted_pick_elt(self):
    return ket(self.label,self.value)      

  def find_index(self,one):
    label = one.label if type(one) == ket else one
    if self.label == label:
      return 1
    return 0

  def find_value(self,one):
    label = one.label if type(one) == ket else one
    if self.label == label:
      return self.value
    return 0

  def find_max_coeff(self):
    return self.value

  def find_min_coeff(self):
    return self.value

  def normalize(self,t=1):
    result = copy.deepcopy(self)
    if result.value > 0:
      result.value = t
    return result

  def rescale(self,t=1):
    result = copy.deepcopy(self)
    if result.value > 0:
      result.value = t
    return result

  def multiply(self,t):
    return ket(self.label,self.value*t)

# 6/1/2015: hrmm... maybe abs, absolute_noise, and relative_noise should be sigmoids!
# newly added 2/4/2014:
# yeah. moved to sigmoid (4/5/2015) Hope we don't break anything!
#  def abs(self):
#    return ket(self.label,abs(self.value))
    
# newly added 7/4/2014:
# add noise to the ket/sp in range [0,t]
  def absolute_noise(self,t):
    return ket(self.label,self.value + random.uniform(0,t))  # hrmm.. so noise is additive only?
  
# newly added 7/4/2014:
# add noise to ket/sp in range [0,t*max_coeff]
  def relative_noise(self,t):
    max_coeff = self.value
    return ket(self.label,self.value + random.uniform(0,t*max_coeff))            
    
  def coeff_sort(self):
    return ket(self.label,self.value)

  def ket_sort(self):
    return ket(self.label,self.value)

  def find_max_coeff(self):
    return self.value

  def find_min_coeff(self):
    return self.value

  def number_find_max_coeff(self):
    return ket("number: " + str(self.value))

  def number_find_min_coeff(self):
    return ket("number: " + str(self.value))
    
  def discrimination(self):
    return ket(" ",self.value)

# 24/2/2015:
# implements discrim-drop[t] SP
# ie: if discrim is > t return |>, else return value.
# don't know how I want this to work! 
  def discrimination_drop(self,t):
    return ket(self.label,self.value)    
    


# sigmoids apply to the values of kets, and leave ket labels alone.
  def apply_sigmoid(self,sigmoid,t1=None,t2=None):
    result = copy.deepcopy(self)
    if t1 == None:
      result.value = sigmoid(result.value)
    elif t2 == None:
      result.value = sigmoid(result.value,t1)
    else:
      result.value = sigmoid(result.value,t1,t2)
    return result

# do we need a superposition version of this? Probably...
# implements: similar[op] |x>
  def old_similar(self,context,op):              # should I use .apply_op(context,op,True)? 
    f = self.apply_op(context,op)            # use apply_op or context.recall() directly?
    print("f:",f.display())                  # in light of active=True thing, apply_op() seems the right answer.
#    return context.pattern_recognition(f,op) # yeah, but what about in pat_rec?
    return context.pattern_recognition(f,op).delete_ket(self)    # we delete self, ie |x>, from the result, since it is always a 100% match anyway.

# 23/2/2015:
# implements: similar[op1,op2] |x>
  def similar(self,context,ops):              
    try:
      op1,op2 = ops.split(',')
    except:
      op1 = ops
      op2 = ops 
    f = self.apply_op(context,op1)            
    return context.pattern_recognition(f,op2).delete_ket(self)    # we delete self, ie |x>, from the result, since it is always a 100% match anyway.
    
# 23/2/2015: 
# implements: self-similar[op1,op2] |x>
# ie don't delete |x>
  def self_similar(self,context,ops):
    try:
      op1,op2 = ops.split(',')
    except:
      op1 = ops
      op2 = ops 
    f = self.apply_op(context,op1)            
    return context.pattern_recognition(f,op2) 
    

# implements: find-topic[op] |x> 
  def find_topic(self,context,op):           
    return context.map_to_topic(self,op)

# 2/4/2015: intn-find-topic[op] |a b c>
# this goes some way to a search engine.
# currently we don't have a superposition version of this. Not sure it is needed.
#
  def intn_find_topic(self,context,op):
    words = self.label.lower().split()
    print("words:",words)
    if len(words) == 0:
      return ket("",0)
    results = [context.map_to_topic(ket(x),op) for x in words]
    print("len results:",len(results))
    if len(results) == 0:                    # this should never be true!
      return ket("",0)
    r = results[0]
    for sp in results:
      print("sp:",sp)
      r = intersection(r,sp)
    return r.normalize(100).coeff_sort()
         

# implement op3 op2 op1 |x>                  # this is actaully also "matrix multiplication", of sorts.
  def merged_apply_op(self,context,ops):
    result = copy.deepcopy(self)
    for op in ops.split()[::-1]:
#      print("op:",op)
      result = result.apply_op(context,op)
    return result

  def count(self):
#    return 1
# 4/1/2015 tweak:
    if self.label == "":
      return 0
    return 1

  def count_sum(self):
    return self.value

  def number_count(self):
#    return ket("number: 1")
# 4/1/2015 tweak:
    if self.label == "":
      return ket("number: 0")
    return ket("number: 1")

  def number_count_sum(self):           
    return ket("number: " + float_to_int(self.value))

  def drop(self):
    if self.value > 0:
      return ket(self.label,self.value)
    else:
      return ket("",0)

  def drop_below(self,t):
    if self.value >= t:
      return ket(self.label,self.value)
    else:
      return ket("",0)
  
  def drop_above(self,t):
    if self.value <= t:
      return ket(self.label,self.value)
    else:
      return ket("",0)


# I'm using this in show_range, arithemetic etc, so can feed in sp or ket.
# deprecated. Now use x.the_label()
# usage: X.ket()
# the other half is in superposition.
  def ket(self):
    return ket(self.label,self.value)

  def the_label(self):
    return self.label
  
  def the_value(self):
    return self.value

  def activate(self,context=None,op=None,self_label=None):
    return ket(self.label,self.value)            # not sure if we need this:
    #return self                                 # or if this will suffice.

# 4/1/2015:
  def is_not_empty(self):
    print("ket is-not-empty:",self)
    if self.label == "":
      return ket("no")
    return ket("yes")

class bra(object):
  def __init__(self,label='?',value=1):
    self.label = label
    self.value = float(value)

  def __str__(self):
    return self.display()

  def type(self):
    return "bra"


  def old_display(self):
    if self.value == 1:
      return '<' + self.label + '|'
    else:
      return '<' + self.label + '|' + str(self.value)

  def display(self,exact=False):                    # do we need an "exact" option here? May as well. Not sure where we use it though.
    if self.value == 1:                             # hrmm... how display bra's: 3<foo| or <foo|3 ??
      return "<{0}|".format(self.label)
    elif exact:
      return '<' + self.label + '|' + str(self.value)
    else:
#      return "<{0}|{1:.3f}".format(self.label,self.value)
      return  '<' + self.label + '|' + float_to_int(self.value,3) 

  def transpose(self):
    return ket(self.label,self.value)


# also at some stage I suppose a transpose of a superposition.
# so I guess we would need to distinguish between a bra-superposition and a ket-superposition.
def transpose(x):
  return x.transpose()


# need to think on how we want |> and <| to behave.
# eg, currently <*||> returns 1. May want 0.
def labels_match(label_1,label_2):
  print("label_1:",label_1)
  print("label_2:",label_2)

  truth_var = True

  one = label_1.lower()  # make label compare case insensitive
  two = label_2.lower()  # hrrmm... may not want this ....
  if one[0] == '!':   # for now only consider bra's with <!x| rather than kets |!x>
    one = one[1:]     # though it is not much work to extend it.
    truth_var = False

  print("one:",one)
  print("two:",two)
  if one == two:
    return truth_var
  a_cat = one.split(': ')
  b_cat = two.split(': ')
  if a_cat[-1] == '*':
    new_a_cat = a_cat[:-1]
    new_b_cat = b_cat[:len(new_a_cat)]
    if new_a_cat == new_b_cat:
      return truth_var
    else:
      return not truth_var
  if b_cat[-1] == '*':
    new_b_cat = b_cat[:-1]
    new_a_cat = a_cat[:len(new_b_cat)]
    if new_b_cat == new_a_cat:
      return truth_var
    else:
      return not truth_var
  return not truth_var

# 25/3/2014 added label_descent()
# Pretty sure it is correct.
def label_descent(x):
  print("x:",x)
  result = [x]
  if x == "*":
    return result
  if x.endswith(": *"):
    x = x[:-3]
  while True:
    try:
      x,null = x.rsplit(": ",1)
      result.append(x + ": *")
    except:
      result.append("*")
      return result

# 18/1/2015: could probably tidy this!
# and I think, in a lot of use cases we don't even need it!
# also, should it be here, or in the functions file? 
def extract_category_value(label):
  one = label.split(': ')
  value = one[-1]
  category = ": ".join(one[:-1])
  return category, value



def apply_bra_to_ket(a_bra,a_ket):
  if type(a_bra) == str:     # this is so we don't need bra("person: Fred") everywhere.
    a_bra = bra(a_bra)       # we can use "person: Fred" directly.
  # maybe the same conversion from string for a_ket??
  elif type(a_bra) == ket:   # this so we can fudge and pass in a ket that acts like a bra.
    a_bra = bra(a_bra.label,a_bra.value)

  star = "*"
  if a_bra.value == 1 or a_ket.value == 1:
    star = ""
  print(a_bra.display() + star + a_ket.display())

  if labels_match(a_bra.label,a_ket.label):
    return a_bra.value * a_ket.value
  else:
    return 0



class superposition(object):
  def __init__(self):
    self.data = []

  def __str__(self):
    return self.display()

  def __len__(self):
    if len(self.data) == 1:           # if sp is |> then return lenght= 0
      if self.data[0].label == "":    # given how the rest of the project handles |> probably never gets touched, but anyway, good just in case.
        return 0
    return len(self.data)

  def type(self):                                              # seems to be broken in console.
    return "(" + " + ".join(x.type() for x in self.data) + ")" # just returns |>
  

  def add_ket(self,a_ket):
    if a_ket.label == '':      # treat |> as the identity ket
      return
    match = None
    for x in self.data:
      if x.label == a_ket.label:
        match = True
        x.value += a_ket.value
        break
    if match == None:
      new_ket = ket(a_ket.label,a_ket.value)
      self.data.append(new_ket)

  def __add__(self,elt):
    result = copy.deepcopy(self)
    if type(elt) == ket:
      result.add_ket(elt)
    if type(elt) == superposition:
      for x in elt.data:
        result.add_ket(x)
    return result
  
  # 6/1/2015:  
  def __iter__(self):       # finally wrote an iterator for superpositions!
    for x in self.data:
      yield x

# a version of add that does not add kets with the same label
  def clean_add_ket(self,a_ket):
    if a_ket.label == '':
      return
#    if len([x.label for x in self.data if x.label == a_ket.label]) == 0:
    if sum(1 for x in self.data if x.label == a_ket.label) == 0:
      self.data.append(ket(a_ket.label,a_ket.value))

# same as above, but also works for superpositions:
  def clean_add(self,one):
    if type(one) == ket:
      self.clean_add_ket(one)
    if type(one) == superposition:
      for x in one.data:
        self.clean_add_ket(x)


  def display(self,exact=False):
    if len(self.data) == 0:
      return '|>'
    return " + ".join(x.display(exact) for x in self.data)

# LOL. Currently is never invoked, the ket version gets called instead!
# Maybe need to tweak which table to use in the processor.
  def long_display(self):
    if len(self.data) == 0:
      return '|>'
#    return "\n".join(str("%.3f" % x.value) + '    |' + x.label + '>' for x in self.data)
# let's do a tidier one, we don't need ket label wrappers here!
# tmp change to number of sig figures:
#    return "\n".join(str("%.3f" % x.value) + '    ' + x.label for x in self.data)                                                                                         
    return "\n".join(str("%.1f" % x.value) + '    ' + x.label for x in self.data)
    
# Hrmm.. meant to be more readable, but not so much!
  def readable_display(self):
    if len(self.data) == 0:
      return ""
    return ", ".join(x.readable_display() for x in self.data)
    

  def apply_bra(self,a_bra):
    return sum(apply_bra_to_ket(a_bra,x) for x in self.data)

# maybe a version where the projection is of more than one element?
  def apply_projection(self,a_bra):
    if len(self.data) == 0:
      return 0                     # should this be ket("")? Or ket("",0)
    result = copy.deepcopy(self)
    for x in result.data:
      x.value = apply_bra_to_ket(a_bra,x)
    return result

# we don't need the next two.
# use apply_fn(extract_value), and apply_fn(extract_category), and apply_fn(apply_value) instead.
#  def apply_extract_value(self):
#    result = copy.deepcopy(self)
##    result.data = [x.apply_extract_value() for x in result.data ]
#    result.data = [extract_value(x) for x in result.data ]
#    return result

#  def apply_extract_category(self):
#    result = copy.deepcopy(self)
##    result.data = [x.apply_extract_category() for x in result.data ]
#    result.data = [extract_category(x) for x in result.data ]
#    return result

# for the family of functions that apply to kets.
# mapping ket -> ket.
# this is buggy if fn(x) actually returns a superposition!
# it sort of works, but creates wierd bugs down the line.
# Now, if we had a mixed type that can handle lists of not just
# kets, but superpositions, sequences, and everything else, then it would be fine.
  def buggy_apply_fn(self,fn):
    result = superposition()
    result.data = [fn(x) for x in self.data ]  # this behaviour is more inline of what you would 
    return result                              # expect from the sequence type (not yet implemented!)

# let's try and write a non-buggy version, but without needing to collapse the kets.
  def also_buggy_apply_fn(self,fn,t1=None,t2=None):                       # maybe an apply_ket_fn, and apply_sp_fn?
    result = superposition()
    for x in self.data:
      if t1 == None:
        r = fn(x)
      elif t2 == None:
        r = fn(x,t1)
      else:
        r = fn(x,t1,t2)
      if type(r) == ket:                       # this code is ugly, and I suspect buggy! 
        result.data.append(r)                  # with fast_sp, should be able to fix this mess!
      if type(r) == superposition:
        result.data += r.data                  # this line looks buggy!!!
    return result

  def still_buggy_apply_fn(self,fn,t1=None,t2=None): 
    result = superposition()
    for x in self:
      if t1 == None:
        r = fn(x)
      elif t2 == None:
        r = fn(x,t1)
      else:
        r = fn(x,t1,t2)
      for elt in r:
#        result.data.append(elt)          # BUGGY! Because we side-stepped "result += elt" we also
                                          # side-stepped checking for |>. This bug probably elsewhere too!
# option a:                               # swapping in fast_sp should help, since then we can use "result += elt"
#        result += elt                    
# option b:
        if elt.label != '':
          result.data.append(elt)         # pretty sure this is broken! that's why "push-float pop-float (|number: 3> + 2|number: 5> + 7|number: 6>)" doesn't work as expected.                                         
    return result

  def apply_fn(self,fn,t1=None,t2=None):
    #print("beep") 
    result = fast_superposition()
    for x in self:
      if t1 == None:
        r = fn(x)
      elif t2 == None:
        r = fn(x,t1)
      else:
        r = fn(x,t1,t2)
      for elt in r:
        result += elt                    
    return result.superposition()


# define a function that maps sp -> sp, instead of ket -> ket/sp.
# now we need to 1) add it to ket class, and 2) wire it into the processor.
# 5/2/2015: starting to wonder if there is a tidier way to do this!!
  def apply_sp_fn(self,fn,t1=None,t2=None,t3=None,t4=None):
    if t1 == None:
      return fn(self)
    elif t2 == None:
      return fn(self,t1)
    elif t3 == None:
      return fn(self,t1,t2)
    elif t4 == None:
      return fn(self,t1,t2,t3)
    else:
      return fn(self,t1,t2,t3,t4)

# need to check this works!
# 27/6/2014: hrmm... so let me get this right, a sp_fn applies to the applied superposition.
# and naked_fn ignores any passed in superpositions.
  def apply_naked_fn(self,fn,t1=None,t2=None,t3=None):
    if t1 == None:
      return fn()
    elif t2 == None:
      return fn(t1)
    elif t3 == None:
      return fn(t1,t2)
    else:
      return fn(t1,t2,t3)
    

# keep this variant distinct from apply_fn(fn) for now.
# also, now fn can map ket -> ket, and also ket -> superposition.
  def apply_fn_collapse(self,fn,t=None):
    result = superposition()
    if t == None:
      for x in self.data:
        result += fn(x)
    else:
      for x in self.data:
        result += fn(x,t)
    return result

# if there are repeated elements in the superposition, add them up.
# This is buggy, some of the time! Look into it!
# I think it might just be the apply_fn() with fn() returning a superposition, is the bug.
# Yup. The bug was in apply_fn(). Fixed now.
# eg, ((ket) + (ket + ket + ket + ket) + (ket + ket))
# would cause collapse() to fail.
  def collapse(self):
    return superposition() + self

  def apply_op(self,context,op):
    result = superposition()
    for x in self.data:
      result += context.recall(op,x,True) # should this be apply_op() instead?
    return result

# apply the same op more than once.
# especially useful for networks.
  def apply_op_multi(self,context,op,n):
    result = copy.deepcopy(self)
    for k in range(n):
      result = result.apply_op(context,op)
    return result



  def count(self):
#    if len(self.data) == 1 and ... # do we need code to implement "count |> == |number: 0>" here? For now nope, see if it bugs eventually!            
    return len(self.data)           # Indeed, |> as identity element may mean (not certain) that it never comes up.

  def count_sum(self):
    return sum(x.value for x in self.data)

  def number_count(self):
    result = len(self.data)
    return ket("number: " + str(result))

  def number_count_sum(self):  
    result = sum(x.value for x in self.data)  # does this bug out if len(self.data) == 0?
    return ket("number: " + float_to_int(result))

  def product(self):                          # need to put these in ket now.
    r = 1
    for x in self.data:
      r *= x.value
    return r

  def number_product(self):
    r = 1
    for x in self.data:
      r *= x.value
    return ket("number: " + str(r))
    

  def drop(self):
    result = copy.deepcopy(self)
    result.data = [x for x in result.data if x.value > 0 ]
    return result

  def drop_below(self,t):
    result = copy.deepcopy(self)
    result.data = [x for x in result.data if x.value >= t ]
    return result

  def drop_above(self,t):
    result = copy.deepcopy(self)
    result.data = [x for x in result.data if x.value <= t ]
    return result

# NB: we use: 1 <= k <= len, not 0 <= k < len to access ket objects.
# NB: though we still use -1 for the last element, -2 for the second last element, etc.
# 3/11/2014: hrmm... is this wired into the processor yet?
  def select_elt(self,k):
#    result = copy.deepcopy(self)
#    if k >= 1 and k <= len(result.data):
#      result.data = [result.data[k - 1]]
#    else:
#      result.data = []    
#    return result
    if k >= 1 and k <= len(self.data):
      return copy.deepcopy(self.data[k - 1])
    elif k < 0:
      return copy.deepcopy(self.data[k])
    else:
      return ket("",0)

# now with the change to select_elt(k), if you want to select a single elt, but still return a superposition,
# you need to do select_range(k,k).
# what if we want to index from the end of the list? cf, tail -3 or something?
  def select_range(self,a,b):
    a = max(1,a) - 1
    b = min(b,len(self.data))
    result = superposition()
    result.data = copy.deepcopy(self.data[a:b])
    return result

  def delete_elt(self,k):
    result = copy.deepcopy(self)
    result.data = [x for i,x in enumerate(result.data) if i != (k-1) ]
    return result

# 6/8/2015:
  def index_split(self,k):                      # OK. Now need to test it.
    result = copy.deepcopy(self)                # Yup. Seems to work.
    r1 = superposition()                        # Now need a ket version.
    r1.data = result.data[:k]
    r2 = superposition()
    r2.data = result.data[k:]
    return r1,r2

# maybe a version of this that takes into account the coeffs, and makes a weighted random choice.
# Yeah. For a start, see: http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
# Yup. This looks good: (BTW, what happens if coeffs are < 0?)
# def weighted_choice(choices):
#   total = sum(w for c, w in choices)
#   r = random.uniform(0, total)
#   upto = 0
#   for c, w in choices:
#      if upto + w > r:
#         return c
#      upto += w
#   assert False, "Shouldn't get here"
#
#
# 14/6/2015: broken! If self.data is the empy list it triggers an exception.
# also, we really don't need to copy the entire superposition, and then return only one of them.
# fixed version just below
  def broken_pick_elt(self):                      # has some similarity with wave-fn collapse in QM.
    result = copy.deepcopy(self)
    return random.choice(result.data)

  def pick_elt(self):
    if len(self) == 0:
      return ket("",0)
    return copy.deepcopy(random.choice(self.data))    

# 5/8/2015
  def weighted_pick_elt(self):                    # quick test in the console, looks to be roughly right.
    if len(self) == 0:
      return ket("",0)
    total = sum(x.value for x in self)
    r = random.uniform(0,total)
    upto = 0
    for x in self:
      w = x.value
      if upto + w > r:
        return x
      upto += w
    assert False, "Shouldn't get here"    

# NB: this is case sensitive, since |x> != |X>
# NB: in some cases find_index() gives very different answers than set_mbr(), in terms of yes or no of membership.
# It basically boils down to:
# labels_match(x.label,label) vs x.label == label (first is used, indirectly, in set_mbr(), second in find_index() )
#
# Also recall:
## test for set membership of |x> in |X>
#def set_mbr(x,X,t=1):
#  return X.apply_bra(x) >= t
#
  def find_index(self,one):
    label = one.label if type(one) == ket else one
    for k,x in enumerate(self.data):
      if x.label == label:
        return k + 1
    return 0             # yeah, 0 for not in the superposition.

  def find_value(self,one):
    label = one.label if type(one) == ket else one # maybe a version for when one is a superposition?
    for x in self.data:
      if x.label == label:
        return x.value
    return 0          

  def delete_ket(self,one):        # do we need a delete_sp() too?
    result = copy.deepcopy(self)
    result.data = [x for x in result.data if x.label != one.label ]
    return result

  def normalize(self,t=1):
    result = copy.deepcopy(self)
    the_sum = sum(x.value for x in result.data)
    if the_sum > 0:
      for x in result.data:
        x.value = t*x.value/the_sum  
    return result

  def rescale(self,t=1):
    if len(self.data) == 0:
      return ket("")
    result = copy.deepcopy(self)
    the_max = max(x.value for x in result.data)
    if the_max > 0:
      for x in result.data:
        x.value = t*x.value/the_max
    return result
  
  def multiply(self,t):
    result = copy.deepcopy(self)
    for x in result.data:
      x.value = x.value*t
    return result

# 6/1/2015: again, abs, absolute_noise and relative_noise should be sigmoids. Pretty sure!
# OK. Abs and absolute_noise we can certainly migrate to sigmoids.
# But relative-noise needs to know max_coeff, which is impossible with sigmoids.
# So just abs in sigmoids I guess.  
# newly added 2/4/2014:    
  def abs(self):                                     # probably rare use given coeffs are meant to be >= 0
    result = copy.deepcopy(self)
    for x in result.data:
      x.value = abs(x.value)
    return result

# newly added 7/4/2014:
# add noise to the ket/sp in range [0,t]
  def absolute_noise(self,t):
    result = copy.deepcopy(self)
    for x in result.data:
      x.value = x.value + random.uniform(0,t)
    return result 
        
# newly added 7/4/2014:
# add noise to ket/sp in range [0,t*max_coeff]
  def relative_noise(self,t):
    max_coeff = self.find_max_coeff()
    result = copy.deepcopy(self)
    for x in result.data:
      x.value = x.value + random.uniform(0,t*max_coeff)
    return result            
    

  def reverse(self):
    result = copy.deepcopy(self)
    result.data.reverse()
    return result

  def shuffle(self):
    result = copy.deepcopy(self)
    random.shuffle(result.data)
    return result

# with thanks to this page: https://wiki.python.org/moin/HowTo/Sorting
# maybe we want the reverse, biggest first, not last?
  def coeff_sort(self):
    result = superposition()
#    result.data = sorted(self.data, key=lambda x: x.value)
    result.data = sorted(self.data, key=lambda x: x.value,reverse=True)
    return result

  def ket_sort(self):
    result = superposition()
#    result.data = sorted(self.data, key=lambda x: x.label.lower())
#    result.data = sorted(self.data, key=lambda x: x.label.lower(),reverse=False)
# 22/5/2014: let's try for a natural sort: Woot! It works!
    result.data = natural_sorted(self.data, key=lambda x: x.label.lower())
    return result

  def find_max_elt(self):
    if len(self.data) == 0:
      return ket("",0)
    the_max = max(x.value for x in self.data)
    for x in self.data:
      if x.value == the_max:
        return ket(x.label,x.value)
    print("I shouldn't be here in find_max_elt.")


  def find_min_elt(self):
    if len(self.data) == 0:
      return ket("",0)
    the_min = min(x.value for x in self.data)
    for x in self.data:
      if x.value == the_min:
        return ket(x.label,x.value)
    print("I shouldn't be here in find_min_elt.")

  def find_max(self):
    if len(self.data) == 0:
      return superposition()
    the_max = max(x.value for x in self.data)
    result = copy.deepcopy(self)
    result.data = [x for x in result.data if x.value == the_max]
    return result

  def find_min(self):
    if len(self.data) == 0:
      return superposition()
    the_min = min(x.value for x in self.data)
    result = copy.deepcopy(self)
    result.data = [x for x in result.data if x.value == the_min]
    return result

# 6/1/2015: maybe a version for find_max_coeff, find_min_coeff and discrimination
# that returns in |number: x> format? Done!
  def find_max_coeff(self):
    if len(self.data) == 0:
      return 0                     # maybe it should return None?
    return max(x.value for x in self.data)

  def find_min_coeff(self):
    if len(self.data) == 0:
      return 0
    return min(x.value for x in self.data)

  def number_find_max_coeff(self):
    if len(self.data) == 0:
      value = 0
    else:
      value = max(x.value for x in self.data)
    return ket("number: " + str(value))

  def number_find_min_coeff(self):
    if len(self.data) == 0:
      value = 0
    else:
      value = min(x.value for x in self.data)
    return ket("number: " + str(value))
  
  def discrimination(self):
    result = 0
    if len(self.data) == 0:
      result = 0
    elif len(self.data) == 1:
      result = self.data[0].value
    else:
      tmp = self.coeff_sort()
      result = tmp.data[0].value - tmp.data[1].value  # if something is "distinctive", this result will be large.
    return ket(" ",result)                            # really the definition of distinctive, if you think about it!
    
# 24/2/2015:
# implements discrim-drop[t] SP
# ie: if discrim is > t return |>, else return value.
# NOPE! I don't know how I want this to work!    
#  def discrimination_drop(self,t):
#    if len(self.data) == 0:
#      return ket("",0)
#    elif len(self.data) == 1:
#      return copy.deepcopy(self.data[0])              # maybe tweak this. eg, ket(self.data[0].label,self.data[0].value) ??
#    else:
#      tmp = self.coeff_sort()
#      result = tmp.data[0].value - tmp.data[1].value
#      ...
    
  
  
    

# 17/6/2014 update: Let's wire in a superposition version of find-topic.
# implements: find-topic[op] (|x> + |y> + |z>)
# motivated by this: http://semantic-db.org/next-gen/multi_map_to_topic.py 
  def find_topic(self,context,op):           
    result = superposition()
    for x in self.data:
      result += context.map_to_topic(x,op)         # .drop_below(min) here too?
    r = result.normalize(100).coeff_sort()
    print(r.long_display())
    return r
    

# sigmoids apply to the values of kets, and leave ket labels alone.
  def apply_sigmoid(self,sigmoid,t1=None,t2=None):
    result = copy.deepcopy(self)
    if t1 == None:
      for x in result.data:
        x.value = sigmoid(x.value)
    elif t2 == None:
      for x in result.data:
        x.value = sigmoid(x.value,t1)
    else:
      for x in result.data:
        x.value = sigmoid(x.value,t1,t2)
    return result

# deprecated. This use case is now: X.the_label()
# usage: X.ket()
  def ket(self):
    if len(self.data) == 0:
      return ket("",0)
    tmp = self.data[0]
    return ket(tmp.label,tmp.value)

  def the_label(self):
    if len(self.data) == 0:
      return ""
    return self.data[0].label
  
  def the_value(self):
    if len(self.data) == 0:
      return 0
    return self.data[0].value

  def activate(self,context=None,op=None,self_label=None):
    #return copy.deepcopy(self)          # not sure if we need this:
    return self

# 4/1/2015:
  def is_not_empty(self):
    print("sp is-not-empty:",self)
    if len(self.data) == 0:
      return ket("no")
    return self.data[0].is_not_empty()
    

def display(x):
  return x.display()



# some sigmoids:
def clean(x):
  if x <= 0:
    return 0
  else:
    return 1

# this one is so common that it is implemented in superposition as .drop_below(t)
def threshold_filter(x,t):
  if x < t:
    return 0
  else:
    return x

def not_threshold_filter(x,t):
  if x <= t:
    return x
  else:
    return 0

def binary_filter(x):
  if x <= 0.96:
    return 0
  else:
    return 1

def not_binary_filter(x):
  if x <= 0.96:
    return 1
  else:
    return 0

def pos(x):           # what about an "abs" sigmoid?
  if x <= 0:
    return 0
  else:
    return x

# 4/5/2015:
def sigmoid_abs(x):           
  return abs(x)

# 4/5/2015:
def max_filter(x,t):
  if x <= t:
    return x
  else:
    return t

def NOT(x):
  if x <= 0.04:
    return 1
  else:
    return 0

# otherwise known as the Goldilock's function.
# not too hot, not too cold.
def xor_filter(x):
  if 0.96 <= x and x <= 1.04:
    return 1
  else:
    return 0

# so common this has been added to superposition as x.multiply(t)
def mult(x,t):
  return x*t

# this is another type of "Goldilock function"
# the in-range sigmoid:
def sigmoid_in_range(x,a,b):
  if a <= x and x <= b:
    return x
  else:
    return 0

# 14/4/2014: newly added:
def invert(x):
  if x == 0:
    return 0
  else:
    return 1/x
    
# 21/5/2014: newly added:
# set all coeffs to t, even the 0'd ones.
def set_to(x,t):
  return t

# 4/1/2015:
def subtraction_invert(x,t):
  return t - x
    

# we need this since pattern_recognition() requires simm().
# bug's out if I put this at the top of the page.
from the_semantic_db_functions import *

# we need this for stored_rule().
#from the_semantic_db_processor import *


# code for the yet to be added stored function rules:
# We have a stored learn rule:
# op |x> #=> foo |y> + bah |z> + some-action
# This stores the rule: "foo |y> + bah |z> + some-action"
# without processing it at learn time.
# Then it activates later when we do: op |x>  (where |x> is self_object)
# However, we don't want it to activate when we do a dump rule (at least I think so)
# Going to take some work to implement, but let's start with a class:
# Baring any bugs, I think it is working!
class stored_rule(object):        
  def __init__(self,rule):           # rule should be a string.
    self.rule = rule
    print("in stored_rule class: just stored:",rule)
  
  def type(self):                    # not 100% we need this, but no harm in putting it in anyway.
    return "stored rule"

  def display(self,exact=False):     # we don't need exact, but we do need to handle display with 1 parameter.
    return self.rule
    
  def readable_display(self):
    return "# " + self.rule
  
  def __str__(self):
    return self.display()
    
  def __len__(self):                # not sure what to return. so 1 sounds good for now.
    return 1    

  # where currently self_object is a string. Breaks even with ket, let alone sp.
  # eventually I want support for all three cases.    
  def activate(self,context,op,self_label=None):                         
    try:
      return extract_compound_superposition(context,self.rule,self_label)[0] # how does return work in try/except?
    except:                                                                   # works fine.
      print("FYI: except in stored_rule")
      return superposition()  
  
  def multiply(self,value):
    return self                                    # will probably do a better job of multiplication later.

# 13/2/2015:
# essentially a copy of stored_rule
# idea is:
# op |x> !=> some-rule
# on activation, we store: op |x> => some-rule
# eg, fib |*> !=> arithmetic( fib n-1 |_self>, |+>, fib n-2 |_self>)
# so no need to manually do:
# fib |10> => fib |10>
# fib |11> => fib |11> 
# and so on. It is done for us!
# At least that is the idea, not sure if I can get it to work.
# yup! works great. eg fib |100> is fast now! 
#     
class memoizing_rule(object):        
  def __init__(self,rule):           # rule should be a string.
    self.rule = rule
    print("in memoizing_rule class: just stored:",rule)
  
  def type(self):                    # not 100% we need this, but no harm in putting it in anyway.
    return "memoizing stored rule"

  def display(self,exact=False):     # we don't need exact, but we do need to handle display with 1 parameter.
    return self.rule
    
  def readable_display(self):
    return "! " + self.rule
  
  def __str__(self):
    return self.display()
    
  def __len__(self):                # not sure what to return. so 1 sounds good for now.
    return 1    

  # where currently self_object is a string. Breaks even with ket, let alone sp.
  # eventually I want support for all three cases.    
  def activate(self,context,op,self_label):                         
    try:
      resulting_rule = extract_compound_superposition(context,self.rule,self_label)[0] # how does return work in try/except?
      context.learn(op,self_label,resulting_rule)
      return resulting_rule
    except:                                                                   # works fine.
      print("FYI: except in stored_rule")
      return superposition()  
  
  def multiply(self,value):
    return self                                    # will probably do a better job of multiplication later.


# 10/1/2015:
# let's try and write a fast_superposition() version of this using ordered dictionaries.
# Later, the plan is for them to replace standard superposition everywhere!
# useful guide: http://www.voidspace.org.uk/python/odict.html
# Idea: define an iterator for fast_superposition that returns kets. Done!
from collections import OrderedDict

class fast_superposition(object):
  def __init__(self):
    self.odict = OrderedDict()

  def __iter__(self):
    for label in self.odict:
      value = self.odict[label]
      yield ket(label,value)

  def __add__(self,one):
    result = copy.deepcopy(self)
    if type(one) in [ket, superposition, fast_superposition]:
      for x in one:
        if x.label != "":                  # treat |> as the identity element
          if x.label in result.odict:
            result.odict[x.label] += x.value
          else:
            result.odict[x.label] = x.value
    return result

  # a version of sp add that does not add (ie, ignores) kets already in the superposition.
  def clean_add(self,one):
    if type(one) in [ket, superposition, fast_superposition]:
      for x in one:
        if x.label != "":
          if x.label not in self.odict:
            self.odict[x.label] = x.value

  # cast from fast_superposition() back to standard superposition().
  def superposition(self):
    r = superposition()
    for x in self:                          # I think this is right.
      r.data.append(x)
    return r

  # given a string label (corresponding to a ket label)
  # return its value, 0 if not in superposition:
  # tempted to put this into the standard superposition class too, but no point, it's going away!
  def get_value(self,label):               # what about a set_value(self,label,value)?
    if label in self.odict:
      return self.odict[label]
    return 0

  def count(self):
    return len(self.odict)

  def count_sum(self):
    r = 0
    for label in self.odict:
      r += self.odict[label]
    return r

  def ket(self):
    if len(self.odict) == 0:
      return ket("",0)
    for label in self.odict:
      value = self.odict[label]
      return ket(label,value)

  def normalize(self):
    sum = 0
    for label in self.odict:
      sum += self.odict[label]
    result = copy.deepcopy(self)
    if sum > 0:
      for label in result.odict:
        result.odict[label] /= sum
    return result


# we need this for stored_rule class.
# seems to work even this side of the class. Cool.
from the_semantic_db_processor import *

# we need this to speed up context.learn():
from collections import OrderedDict

# let's dive into it!
class new_context(object):
  def __init__(self,name):
    self.name = name
    self.ket_rules_dict = OrderedDict()

# op is a string
# label is a string or a ket
# rule can be anything
# add_learn is either True or False
#
  def learn(self,op,label,rule,add_learn=False):
    # some prelims:
    if op == "supported-ops":                    # never learn "supported-ops", it is auto-generated and managed
      return
    if type(label) == ket:                       # label is string. if ket, convert back to string
      label = label.label
    if type(rule) == str:                        # rule is assumed to be ket, superposition, or stored rule (maybe fast sp too).
      rule = ket(rule)                           # if string, cast to ket
    if len(rule) == 0:                           # do not learn rules that are |>
      return

    if label not in self.ket_rules_dict:
      self.ket_rules_dict[label] = OrderedDict()
      self.ket_rules_dict[label]["supported-ops"] = superposition()
    self.ket_rules_dict[label]["supported-ops"].clean_add(ket("op: " + op))  # this is probably a speed bump now.
                                                                             # but if we merge over to fast_sp, that should fix itself.
    if not add_learn:
      self.ket_rules_dict[label][op] = rule
    else:
      if op not in self.ket_rules_dict[label]:
        self.ket_rules_dict[label][op] = superposition()
      self.ket_rules_dict[label][op].clean_add(rule)

  def add_learn(self,op,label,rule):
    return self.learn(op,label,rule,True)       # corresponds to "op |x> +=> |y>"

# op is a string, or a ket in form |op: some-operator>
# label is a string or a ket
#
  def recall(self,op,label,active=False):
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]                         # map |op: age> to "age"
    if type(label) == ket:
      coeff = label.value
      ket_label = label.label
    else:
      coeff = 1
      ket_label = label
#    coeff = 1                                  # use this to switch off the multiply(coeff) feature

    match = False
    for trial_label in label_descent(ket_label):
      if trial_label in self.ket_rules_dict:
        if op in self.ket_rules_dict[trial_label]:
          rule = self.ket_rules_dict[trial_label][op]
          match = True
          break
    if not match:
      print("recall not found")
      rule = ket("",0)

    if active:
      rule = rule.activate(self,op,ket_label)
    return rule.multiply(coeff)

# op is a string, or a ket in form |op: some-operator>
# label is a string or a ket
#
  def dump_rule(self,op,label,exact=False):
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]
    ket_name = label if type(label) == ket else ket(label) # maybe tidy this.

    rule = self.recall(op,label)
    rule_string = " => "
    if type(rule) == stored_rule:
      rule_string = " #=> "
    if type(rule) == memoizing_rule:
      rule_string = " !=> "
      

    return op + " " + ket_name.display() + rule_string + rule.display(exact)

# previously called dump_all_rules()
  def dump_ket_rules(self,label,exact=False):
    # some prelims:
    if type(label) == ket:
      ket_label = label.label
    else:
      ket_label = label

    if ket_label not in self.ket_rules_dict:
      return ""

    return "\n".join(self.dump_rule(op,label,exact) for op in self.ket_rules_dict[ket_label] if exact or (op != "supported-ops") )


  # instead of dumping all the rules for a known ket, dump all the rules for all kets in the superposition:
  # sp should be a ket, or superposition
  #
  def dump_sp_rules(self,sp,exact=False):
    if type(sp) == str:
      sp = ket(sp)
    return "\n\n".join(self.dump_ket_rules(x,exact) for x in sp )

  # dump everything we know about the current context:
  def dump_universe(self,exact=False):
    context_string = "|context> => |context: " + self.name + ">"
    sep = "\n----------------------------------------\n"
    return sep + context_string + "\n\n" + "\n\n".join(self.dump_ket_rules(x,exact) for x in self.ket_rules_dict ) + sep


  # create inverse for a single learn rule:
  # not sure we want this factored out. But leave as is for now.
  def create_single_learn_rule_inverse(self,op,label):
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]
    if op.startswith("inverse-"):              # don't take the inverse of an inverse.
      return
    if type(label) == ket:
      label = label.label

    if label not in self.ket_rules_dict:
      return
    if op not in self.ket_rules_dict[label]:
      return

    rule = self.ket_rules_dict[label][op]
    if type(rule) in [ket, superposition, fast_superposition]:      # don't learn inverse for stored_rules.
      for x in rule:
        if x.label != "":
          self.add_learn("inverse-" + op,x,label)                   # do we want ket(label)?
                                                                    # also, NB: the add_learn. ie, slow with current superposition class.
                                                                    # will be faster with fast_superposition class (which I will swap in eventually!)

  # create inverse for a single known ket:
  def create_ket_rules_inverse(self,label):
    if type(label) == ket:
      label = label.label
    if label not in self.ket_rules_dict:
      return

    for op in self.ket_rules_dict[label]:
      self.create_single_learn_rule_inverse(op,label)


  # it would be nice for this to be idempotent, but I don't think it is.
  # also, slightly concerned we may create infinite loops, though no example of that seen so far.
  #
  # create inverse for all known kets:
  def create_universe_inverse(self):
    for label in self.ket_rules_dict:
      self.create_ket_rules_inverse(label)

# let's merge in the pieces, into one function:
# doh! so much for that! Pretty sure infinite loop.
  def infinite_loop____create_universe_inverse(self):
    for label in self.ket_rules_dict:
      for op in self.ket_rules_dict[label]:
        rule = self.ket_rules_dict[label][op]
        if type(rule) in [ket, superposition, fast_superposition]:      # don't learn inverse for stored_rules.
          for x in rule:
            if x.label != "":
              self.add_learn("inverse-" + op,x,label)

  def create_inverse_op(self,op):
    if type(op) == ket:
      op = op.label[4:] 
    for label in self.ket_rules_dict:
      if op in self.ket_rules_dict[label]:
        rule = self.ket_rules_dict[label][op]
        if type(rule) in [ket, superposition, fast_superposition]:      # don't learn inverse for stored_rules.
          for x in rule:
            if x.label != "":
              self.add_learn("inverse-" + op,x,label)


# do we need unlearn stuff?
# unlearn rule, unlearn everything to do with a ket, and so on??
# might not be that hard ...

  # what I'm calling pattern recognition.
  # just simm applied to relevant kets
  def pattern_recognition(self,pattern,op,t=0):
    if type(op) == ket:
      op = op.label[4:]
    result = superposition()                                            # later swap out superposition to fast_superposition
    for label in self.ket_rules_dict:                                   # though when I do so I will probably rename fast_sp to plain superposition.
      if op in self.ket_rules_dict[label]:
#        candidate_pattern = self.recall(op,label,True)                       # do we need active=True here? probably. OK. On a trial basis :)
        candidate_pattern = self.ket_rules_dict[label][op]
        value = silent_simm(pattern,candidate_pattern)
        if value > t:                                                   # "value >= t" instead?
          result.data.append(ket(label,value))                          # "result += ket(label,value)" when swap in fast_superposition
    return result.coeff_sort()


# essentially identical in structure to pattern_recognition.
# I wonder if they should be merged into one more generic function?? Not for now, at least.
  def map_to_topic(self,e,op,t=0):
    if type(op) == ket:
      op = op.label[4:]
    result = superposition()                                            # later swap out superposition to fast_superposition
    for label in self.ket_rules_dict:
      if op in self.ket_rules_dict[label]:
        frequency_list = self.recall(op,label,True)                       # do we need active=True here? probably. OK. On a trial basis :)
        value = normed_frequency_class(e,frequency_list)
        if value > t:                                                   # "value >= t" instead?
          result.data.append(ket(label,value))                          # "result += ket(label,value)" when swap in fast_superposition
    return result.normalize(100).coeff_sort()


  # given an operator, return superposition of kets that support that operator:
  # slightly weird we have this here, and then a wrapper around it in the functions code, and this latter is what the processor uses.
  #
  # 22/2/2015 tweak: relevant_kets(self,"*") returns all known kets.
  def relevant_kets(self,op):
    result = superposition()
    if op == "*":
      for label in self.ket_rules_dict:
        result.data.append(ket(label))
    else:
      for label in self.ket_rules_dict:
        if op in self.ket_rules_dict[label]:
          result.data.append(ket(label))                                  # "result += ket(label)" when swap in fast_sp
    return result

# 14/4/2015:
# given a ket, return matching lists of kets.
# eg: list-kets |movie: *>, should return all movies.
# list-kets |*> should return all KET's that have: OP KET => SP 
# Now, just need to test it!
# decided to rename and tweak, and call it starts-with.
# eg: starts-with |animal: > to list all animals.
# e is a ket.
  def starts_with(self,e):
    label = e.the_label()
#    if len(label) == 0:
#      return ket("",0)
#    if label[-1] != "*":
#      return e
#    label = label.rstrip("*").rstrip(": ")
    result = superposition()
    for trial_label in self.ket_rules_dict:
      if trial_label.startswith(label):
        result.data.append(ket(trial_label))  
    return result
      

# try and pretty print the sp data, instead of the BKO scheme.
# First, display the data for a single ket:
# Fred
# friends: Sam, George, Harry
#     age: age: 32
# parents: Mary, Richard
#
#
# NB: we renamed display_ket() to pretty_print_ket(). May want to swap that back.
  def pretty_print_ket(self,one):     # one is a ket
    label = one.label if type(one) == ket else one
    head = "  " + label + "\n"
    frame = ""
    op_list = list(self.ket_rules_dict[label])
    if len(op_list) != 0:
      max_len = max(len(op) for op in op_list)
      sep = ": "
      frame = "\n".join("  " + op.rjust(max_len) + sep + self.recall(op,label).readable_display() for op in op_list) + "\n"
    return head + frame

  def display_sp(self,sp):     # sp is a ket or sp
    return "\n".join(self.pretty_print_ket(x) for x in sp)

  def display_all(self):
    head = "  context: " + self.name + "\n\n"
    return head + "\n".join(self.pretty_print_ket(label) for label in self.ket_rules_dict)

# there are other possible "pretty print" too. Maybe write code for this eventually...
# eg: (this one is common for end of movie credits)
# Fred
# friends: Sam
#          George
#          Harry
#     age: age: 32
# parents: Mary
#          Richard


# I don't recall how this works!
# anyway, meant to convert context into frequency list.
  def to_freq_list(self):
    result = superposition()
    for label in self.ket_rules_dict:
      count_label = - 1                                # we subtract 1 because we don't want to count the supported-ops term.
      for op in self.ket_rules_dict[label]:
        count_label += 1
        rule = self.recall(op,label)                   # do we need "active=True" here? Probably not.
        if type(rule) in [ket, superposition, fast_superposition]:
          result += rule.apply_sigmoid(clean)          # this will auto-speed up once we swap in fast_superpositions.
      result += ket(label,count_label)
    return result.coeff_sort()

                        
                                                                      
class context_list(object):
  def __init__(self,name):
    self.name = name
    c = new_context(name)
    self.data = [c]
    self.index = 0

  def set(self,name):                              # maybe write a set_index, where you specify index number, instead of context name
    match = False
    for k,context in enumerate(self.data):
      if context.name == name:
        self.index = k
        match = True
        break
    if not match:
      c = new_context(name)
      self.data.append(c)
      self.index = len(self.data) - 1

  def show_context_list(self):                      # maybe include a count of the number of kets known to that context
    text = "context list:\n"
    for k,context in enumerate(self.data):
      pre = "* " if k == self.index else "  "
      text += pre + context.name + " (" + str(len(context.ket_rules_dict)) + ")\n"
    return text

# new 12/2/2015:
# assumes k is an integer:
  def set_index(self,k):
    if k < 0 or k >= len(self.data):
      return False
    self.index = k
    return True
    
  def show_context_list_index(self):
    text = "context list:\n"
    for k,context in enumerate(self.data):
      pre = "* " if k == self.index else "  "
      text += " " + str(k) + ") " + pre + context.name + " (" + str(len(context.ket_rules_dict)) + ")\n"
    return text  

  def context_name(self):
    return self.data[self.index].name

  def learn(self,op,label,rule,add_learn=False):
    self.data[self.index].learn(op,label,rule,add_learn)

  def add_learn(self,op,label,rule):
    self.data[self.index].add_learn(op,label,rule)

  def recall(self,op,label,active=False):
    return self.data[self.index].recall(op,label,active)

  def dump_ket_rules(self,label,exact=False):
    return self.data[self.index].dump_ket_rules(label,exact)

  def dump_sp_rules(self,label,exact=False):                  # is this really a label here, or a sp?
    return self.data[self.index].dump_sp_rules(label,exact)

  def display_sp(self,sp):
    return self.data[self.index].display_sp(sp)

  def display_all(self):
    return self.data[self.index].display_all()


  def to_freq_list(self):
    return self.data[self.index].to_freq_list()    # later rewrite so it returns results from all context's.      

# make the all context-to-freq it's own function.
  def multiverse_to_freq_list(self):
    result = superposition()
    for context in self.data:
      result += context.to_freq_list()
    return result
    

  def dump_universe(self,exact=False):
    return self.data[self.index].dump_universe(exact)

  def create_universe_inverse(self):
    self.data[self.index].create_universe_inverse()
    
  def create_multiverse_inverse(self):
    for context in self.data:
      context.create_universe_inverse()

  def create_inverse_op(self,op):
    self.data[self.index].create_inverse_op(op)
      
  def pattern_recognition(self,pattern,op,t=0):
    return self.data[self.index].pattern_recognition(pattern,op,t)

# currently unimplemented. It was dropped from the recent new_context() class work. Maybe re-instate it?
#  def verbose_pattern_recognition(self,pattern,op="pattern"):
#    return self.data[self.index].verbose_pattern_recognition(pattern,op)
  
  def map_to_topic(self,e,op,t=0):
    return self.data[self.index].map_to_topic(e,op,t)   
 
  def relevant_kets(self,op):
    return self.data[self.index].relevant_kets(op)
    
#  def list_kets(self,e):
#    return self.data[self.index].list_kets(e)    
# renames to starts-with
  def starts_with(self,e):
    return self.data[self.index].starts_with(e)    
         
  
  def global_recall(self,op,label):              # where do we even use this?
    result = superposition()                     # does it need active=True too?
    for context in self.data:
      result += context.recall(op,label)
    return result

  def dump_multiverse(self,exact=False):
    result = ""
    for context in self.data:
      result += context.dump_universe(exact)
    return result



    
