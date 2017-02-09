#!/usr/bin/env python3

#######################################################################
# simple create word context example
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-02-04
# Update:
# Copyright: GPLv3
#
# Usage: ./create-word-context.py
#
#######################################################################


import sys
import re
from collections import OrderedDict

#filename = "text/Mary-sentence.txt"
#filename = "text/ebook-Sherlock-Holmes.txt"
#filename = "text/ebook-Tom_Sawyer_74.txt"
filename = "text/tidy-rusty.txt"
#filename = "text/complete-k5-posts.txt"
#filename = "text/tdillo.txt"
#filename = "text/trane.txt"
#filename = "text/tidy-procrasti.txt"

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

  word_context = {}
  for one, two, three in generate_word_n_grams(words,3):
    a_context = "%s X %s" % (one,three)
    if two not in word_context:
      word_context[two] = superposition()
    word_context[two].add(a_context)
  print_sw_dict(word_context, "context")




