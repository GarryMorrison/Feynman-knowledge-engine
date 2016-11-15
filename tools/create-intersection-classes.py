#!/usr/bin/env python3

#######################################################################
# let's find intersection classes, a nice step towards grammar
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-11-13
# Update: 2016-11-15
# Copyright: GPLv3
#
# Usage: ./create-intersection-classes.py [filename.txt]
#
# Seems to work. Now need to think how to optimize it.
# In testing only a bit faster than the console version!
# That is bad, given the lack of optimization in the console version.
#
#######################################################################


import sys
import re
from collections import OrderedDict

number_of_results = 20000
class_width = 12
#tidy = False
tidy = True
strict = True

#filename = "text/Mary-sentence.txt"
#filename = "text/ebook-Sherlock-Holmes.txt"
#filename = "text/ebook-Tom_Sawyer_74.txt"
#filename = "text/tidy-rusty.txt"
#filename = "text/complete-k5-posts.txt"
#filename = "text/tdillo.txt"
#filename = "text/trane.txt"
#filename = "text/tidy-procrasti.txt"
#filename = "text/Cable4096.txt"
#filename = "text/ebook-moby-shakespeare.txt"
#filename = "text/ebook-Asimov_Isaac_-_I_Robot.txt"
#filename = "text/ebook-Alices_Adventures_in_Wonderland_11.txt"
#filename = "text/WP-Australia.txt"
#filename = "text/high-order-sequence-paper.txt"
filename = "text/code.txt"

if len(sys.argv) == 2:
  filename = sys.argv[1]


def create_word_n_grams(s,N):
  return [s[i:i+N] for i in range(len(s)-N+1)]

def generate_word_n_grams(s,N):
  for i in range(len(s)-N+1):
    yield s[i:i+N]

# define our bare-bones superposition class:
class superposition(object):
  def __init__(self):
#    self.dict = {}
    self.dict = OrderedDict()

  def __str__(self):
    list_of_kets = []
    for key,value in self.dict.items():
      if value == 1:
        s = "|%s>" % key
      else:
        s = "%s|%s>" % (value,key)
      list_of_kets.append(s)
    return " + ".join(list_of_kets)

  def __iter__(self):
    for key,value in self.dict.items():
      yield key, value

  def __len__(self):
    return len(self.dict)

  def add(self,str,value=1):
    if str in self.dict:
      self.dict[str] += value
    else:
      self.dict[str] = value

  def pair(self):                               # if the dict is longer than 1 elt, this returns a random pair
    for key,value in self.dict.items():         # presuming not using an OrderedDict
      return key, value

  def get_value(self,str):
    if str in self.dict:
      return self.dict[str]
    else:
      return 0

  def rescale(self,t=1):
    if len(self.dict) == 0:
      return superposition()
    the_max = max(value for key,value in self.dict.items())
    result = superposition()
    if the_max > 0:
      for key,value in self:
        result.dict[key] = t*self.dict[key]/the_max
    return result

  def normalize(self,t=1):
    if len(self.dict) == 0:
      return superposition()
    the_sum = sum(value for key,value in self.dict.items())
    result = superposition()
    if the_sum > 0:
      for key,value in self:
        result.dict[key] = t*self.dict[key]/the_sum
    return result

  def coeff_sort(self):
    r = superposition()
    for key,value in sorted(self.dict.items(), key=lambda x: x[1], reverse=True):
      r.add(key,value)
    return r

  def select_top(self,k):
    r = superposition()
    for i,(key,value) in enumerate(self.dict.items()):
      r.add(key,value)
      if i + 1 >= k:
        break
    return r


def print_sw_dict(dict,op):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op,label,sp))

def print_sorted_sw_dict(dict,op):
  for label,sp in dict.items():
#    if len(sp) > 20:
    print("%s |%s> => %s" % (op,label,sp.coeff_sort()))

# probably can optimize this more yet. 
#
def fast_simm(A,B):
  if len(A) == 0 or len(B) == 0:
    return 0
  if len(A) == 1 and len(B) == 1:
    a_label, a_value = A.pair()
    b_label, b_value = B.pair()
    
    if a_label != b_label:                    # put a.label == '' test in here too?
      return 0
    a = max(a_value,0)                        # just making sure they are >= 0.
    b = max(b_value,0)
    if a == 0 and b == 0:                     # prevent div by zero.
      return 0
    return min(a,b)/max(a,b)
#  return intersection(A.normalize(),B.normalize()).count_sum()     # very slow version!

  # now calculate the superposition version of simm, while trying to be as fast as possible:
  try:
    merged = {}
    one_sum = 0
    one = {}
    for label,value in A:
      one[label] = value
      one_sum += value                     # assume all values in A are >= 0
      merged[label] = True                 # potentially we could use abs(elt.value)

    two_sum = 0
    two = {}
    for label,value in B:
      two[label] = value
      two_sum += value                     # assume all values in B are >= 0
      merged[label] = True

    # prevent div by zero:
    if one_sum == 0 or two_sum == 0:
      return 0

    merged_sum = 0
    for key in merged:
      if key in one and key in two:
        v1 = one[key]/one_sum
        v2 = two[key]/two_sum
        merged_sum += min(v1,v2)
    return merged_sum
  except Exception as e:
    print("fast_simm exception reason: %s" % e)

# I don't think we use this anywhere.
# pretty print a float:
def float_to_int(x,t=2):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

# return list version:
def pattern_recognition_list(dict,pattern,t=0):
  result = []
  for label,sp in dict.items():
    value = fast_simm(pattern,sp)       # if a clean superposition, then swap in faster_simm()
    if value > t:
      result.append((label,value))
  return result

# return superposition version:
def pattern_recognition_sp(dict,pattern,k):
  r = superposition()
  for label,sp in dict.items():
    value = fast_simm(pattern,sp)       # if a clean superposition, then swap in faster_simm()
    if value > 0:
      r.add(label,value)
  return r.coeff_sort().select_top(k)    # putting the select_top() statement here rather than later, doesn't seem to improve speed.


# this is the data we need to create the intersection classes:
def create_word_classes(filename):
  with open(filename,'r') as f:
    text = f.read()
    words = [w for w in re.split('[^a-z0-9_\']',text.lower().replace('\\n',' ')) if w]
  
    class_1_1 = superposition()
    for w in words:
      class_1_1.add(w)
#    print("class-1-1 |X> => %s\n" % class_1_1.coeff_sort())  

    class_2_1 = {}
    class_2_2 = {}
    for one, two in generate_word_n_grams(words,2):
      head_2_1 = "X %s" % two
      head_2_2 = "%s X" % one
      if head_2_1 not in class_2_1:
        class_2_1[head_2_1] = superposition()
      if head_2_2 not in class_2_2:
        class_2_2[head_2_2] = superposition()
      class_2_1[head_2_1].add(one)
      class_2_2[head_2_2].add(two)
#    print_sorted_sw_dict(class_2_1, "class-2-1")
#    print_sorted_sw_dict(class_2_2, "class-2-2")
  return class_1_1.coeff_sort(), class_2_1, class_2_2


class_1_1, class_2_1, class_2_2 = create_word_classes(filename)
#print("class_1_1:", class_1_1.select_top(5))
#sys.exit(0)

def pre_class_op(class_2_1, word, class_width):
  try:
    head = "X %s" % word
    pattern = class_2_1[head]
    result = pattern_recognition_sp(class_2_1, pattern, class_width)
    return [ word.replace("X ","") for word,value in result ]
  except:
    return []

def post_class_op(class_2_2, word, class_width):
  try:
    head = "%s X" % word
    pattern = class_2_2[head]                                           # had a key error. How??? Ahh... end of document.
    result = pattern_recognition_sp(class_2_2, pattern, class_width)
    return [ word.replace(" X","") for word,value in result ]
  except:
    return []

def list_intersection(one,two):
  return [ x for x in one if x in two]

# now the main event.
# later make into a function?
for word,value in class_1_1.select_top(number_of_results):
  r1 = pre_class_op(class_2_1,  word, class_width)
  r2 = post_class_op(class_2_2, word, class_width)
  r3 = list_intersection(r1, r2)
  if tidy:
    if strict:
      if len(r3) > 1:
        print(", ".join(r3))
    else:
      print(", ".join(r3))
  else:
#    print("word:",word)
    print("pre-class:         ", ", ".join(r1))
    print("post-class:        ", ", ".join(r2))
    print("intersection-class:", ", ".join(r3))
    print()  



sys.exit(0)
# superposition version follows.
def pre_class_op(class_2_1,word,number_of_results):
  head = "X %s" % word
  pattern = class_2_1[head]
  result = pattern_recognition_sp(class_2_1,pattern).select_top(number_of_results)
  r = superposition()
  for word,value in result:
    r.add(word.replace("X ",""))
  return r

def post_class_op(class_2_2,word,number_of_results):
  head = "%s X" % word
  pattern = class_2_2[head]
  result = pattern_recognition_sp(class_2_2,pattern).select_top(number_of_results)
  r = superposition()
  for word,value in result:
    r.add(word.replace(" X",""))
  return r

def sp_intersection(one,two):
  r = superposition()
  for x in one.dict:
    if x in two.dict:
      r.add(x)
  return r  

# now the main event.
# later make into a function
for word,value in class_1_1.select_top(k):
  print("word:",word)
  r1 = pre_class_op(class_2_1,word,10)
  r2 = post_class_op(class_2_2,word,10)
  r3 = sp_intersection(r1, r2)
  print("pre-class:",r1)
  print("post-class:",r2)
  print("intersection-class:",r3)


sys.exit(0)
# set version follows. I think we want to preseve order, so need superposition version.
def pre_class_op(class_2_1,word,number_of_results):
  head = "X %s" % word
  pattern = class_2_1[head]
  result = pattern_recognition_sp(class_2_1,pattern).select_top(number_of_results)
  r = set()
  for word,value in result:
    r.update({word.replace("X ","")})
  return r

def post_class_op(class_2_2,word,number_of_results):
  head = "%s X" % word
  pattern = class_2_2[head]
  result = pattern_recognition_sp(class_2_2,pattern).select_top(number_of_results)
  r = set()
  for word,value in result:
    r.update({word.replace(" X","")})
  return r

# now the main event. 
# later make into a function
for word,value in class_1_1.select_top(k):
  print("word:",word)
  r1 = pre_class_op(class_2_1,word,10)
  r2 = post_class_op(class_2_2,word,10)
  r3 = r1 & r2
  print("pre-class:",r1)
  print("post-class:",r2)
  print("intersection-class:",r3)
