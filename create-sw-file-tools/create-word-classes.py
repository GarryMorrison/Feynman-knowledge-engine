#!/usr/bin/env python3

#######################################################################
# let's try to find "word classes"
# hopefully a step towards word2sp. Nope! Doesn't look like it.
# But maybe a small step towards grammar.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-11-07
# Update:
# Copyright: GPLv3
#
# Usage: ./create-word-classes.py
#
#######################################################################


import sys
import re
from collections import OrderedDict

#filename = "text/Mary-sentence.txt"
filename = "text/ebook-Sherlock-Holmes.txt"
#filename = "text/ebook-Tom_Sawyer_74.txt"


def create_word_n_grams(s,N):
  return [s[i:i+N] for i in range(len(s)-N+1)]

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

def print_sw_dict(dict,op):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op,label,sp))

def print_sorted_sw_dict(dict,op):
  for label,sp in dict.items():
#    if len(sp) > 20:
    print("%s |%s> => %s" % (op,label,sp.coeff_sort()))


with open(filename,'r') as f:
  text = f.read()
  words = [w for w in re.split('[^a-z0-9_\']',text.lower().replace('\\n',' ')) if w]
  
  r = superposition()
  for w in words:
    r.add(w)
  print("class-1-1 |X> => %s\n" % r.coeff_sort())  

  class_2_1 = {}
  class_2_2 = {}
  for one, two in create_word_n_grams(words,2):
    head_2_1 = "X %s" % two
    head_2_2 = "%s X" % one
    if head_2_1 not in class_2_1:
      class_2_1[head_2_1] = superposition()
    if head_2_2 not in class_2_2:
      class_2_2[head_2_2] = superposition()
    class_2_1[head_2_1].add(one)
    class_2_2[head_2_2].add(two)
  print_sorted_sw_dict(class_2_1, "class-2-1")
  print_sorted_sw_dict(class_2_2, "class-2-2")

  class_3_1 = {}
  class_3_2 = {}
  class_3_3 = {}
  for one, two, three in create_word_n_grams(words,3):
    head_3_1 = "X %s %s" % (two,three)
    head_3_2 = "%s X %s" % (one,three)
    head_3_3 = "%s %s X" % (one,two)
    if head_3_1 not in class_3_1:
      class_3_1[head_3_1] = superposition()
    if head_3_2 not in class_3_2:
      class_3_2[head_3_2] = superposition()
    if head_3_3 not in class_3_3:
      class_3_3[head_3_3] = superposition()
    class_3_1[head_3_1].add(one)
    class_3_2[head_3_2].add(two)
    class_3_3[head_3_3].add(three)
  print_sorted_sw_dict(class_3_1, "class-3-1")
  print_sorted_sw_dict(class_3_2, "class-3-2")
  print_sorted_sw_dict(class_3_3, "class-3-3")

  class_4_1 = {}
  class_4_2 = {}
  class_4_3 = {}
  class_4_4 = {}
  for one, two, three, four in create_word_n_grams(words,4):
    head_4_1 = "X %s %s %s" % (two,three,four)
    head_4_2 = "%s X %s %s" % (one,three,four)
    head_4_3 = "%s %s X %s" % (one,two,four)
    head_4_4 = "%s %s %s X" % (one,two,three)
    if head_4_1 not in class_4_1:
      class_4_1[head_4_1] = superposition()
    if head_4_2 not in class_4_2:
      class_4_2[head_4_2] = superposition()
    if head_4_3 not in class_4_3:
      class_4_3[head_4_3] = superposition()
    if head_4_4 not in class_4_4:
      class_4_4[head_4_4] = superposition()
    class_4_1[head_4_1].add(one)
    class_4_2[head_4_2].add(two)
    class_4_3[head_4_3].add(three)
    class_4_4[head_4_4].add(four)
  print_sorted_sw_dict(class_4_1, "class-4-1")
  print_sorted_sw_dict(class_4_2, "class-4-2")
  print_sorted_sw_dict(class_4_3, "class-4-3")
  print_sorted_sw_dict(class_4_4, "class-4-4")

  class_5_1 = {}
  class_5_2 = {}
  class_5_3 = {}
  class_5_4 = {}
  class_5_5 = {}
  for one, two, three, four, five in create_word_n_grams(words,5):
    head_5_1 = "X %s %s %s %s" % (two,three,four,five)
    head_5_2 = "%s X %s %s %s" % (one,three,four,five)
    head_5_3 = "%s %s X %s %s" % (one,two,four,five)
    head_5_4 = "%s %s %s X %s" % (one,two,three,five)
    head_5_5 = "%s %s %s %s X" % (one,two,three,four)
    if head_5_1 not in class_5_1:
      class_5_1[head_5_1] = superposition()
    if head_5_2 not in class_5_2:
      class_5_2[head_5_2] = superposition()
    if head_5_3 not in class_5_3:
      class_5_3[head_5_3] = superposition()
    if head_5_4 not in class_5_4:
      class_5_4[head_5_4] = superposition()
    if head_5_5 not in class_5_5:
      class_5_5[head_5_5] = superposition()
    class_5_1[head_5_1].add(one)
    class_5_2[head_5_2].add(two)
    class_5_3[head_5_3].add(three)
    class_5_4[head_5_4].add(four)
    class_5_5[head_5_5].add(five)
  print_sorted_sw_dict(class_5_1, "class-5-1")
  print_sorted_sw_dict(class_5_2, "class-5-2")
  print_sorted_sw_dict(class_5_3, "class-5-3")
  print_sorted_sw_dict(class_5_4, "class-5-4")
  print_sorted_sw_dict(class_5_5, "class-5-5")
