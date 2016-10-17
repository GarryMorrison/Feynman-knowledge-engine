#!/usr/bin/env python3

#######################################################################
# wikipedia based find-topic
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-10-17
# Update: 
# Copyright: GPLv3
#
# Usage: ./find-topic.py word [number-of-results-to-show]
#
# data source: http://semantic-db.org/sw-examples/30k--wikipedia-frequency-list.sw
#
#######################################################################


import sys
import math

if len(sys.argv) < 2:
  print("\nUsage: ./find-topic.py word [number-of-results-to-show]\n")
  sys.exit(1)

if len(sys.argv) >= 2:
  word = sys.argv[1]

number_of_results = 50
if len(sys.argv) == 3:
  number_of_results = int(sys.argv[2])

op = "words-1"
source = "sw-examples/30k--wikipedia-frequency-list.sw"
interactive = True
#interactive = False


# define our bare-bones superposition class:
class superposition(object):
  def __init__(self):
    self.dict = {}

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


# load a simple sw file into a dictionary:
# (copied from phi-superpositions-v3.py)
# with a tweak to store the max_coeff,
# which we need to speed up find-topic[op]
def load_simple_sw_into_dict(filename,op):
  op_head = op + " |"
  sw_dict = {}
  with open(filename,'r') as f:
    for line in f:
      line = line.strip()
      if line.startswith(op_head):
        try:
          max_coeff = 0
          head,tail = line.split('> => ',1)
          label = head.split(' |',1)[1]
          sw_dict[label] = superposition()
          for piece in tail[:-1].split('> + '):
#            print("piece:",piece)
            float_piece, string_piece = piece.split('|')
            try:            
              float_piece = float(float_piece)
#              float_piece = int(float_piece)              # Nope. float() is faster than int()
            except:
              float_piece = 1
            sw_dict[label].add(string_piece,float_piece)
            if float_piece > max_coeff:
              max_coeff = float_piece
          sw_dict[label].add("__max",max_coeff)            # is this the best way to store the max_coeff??
        except Exception as e:
          print("Exception reason: %s" % e)
          continue
  return sw_dict

def print_sw_dict(dict):
  for label,sp in dict.items():
    print("|%s> => %s" % (label,sp))

#sw_dict = load_simple_sw_into_dict(source,"words-1")
#print_sw_dict(sw_dict)
#sys.exit(0)

# the normalized frequency class equation.
# result is in [0,1]
# 1 for exact match, 0 for not in set.
#
# works great! Indeed, it is a bit like a fuzzy set membership function.
# eg, if all coeffs in X are equal, it gives Boolean 1 for membership, and 0 for non-membership.
# and if the coeffs are not all equal, then it has fuzzier properties.
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


# an optimized version of the normed_frequence_class function:
# e is a string
# X is a frequency list (stored as a superposition)
# with a special member the |__max> ket, that carries the max coeff of the given sp.
# All coefs in X must be > 0
#
def fast_normed_frequency_class(e,X):
  smallest = 1                                  # assume the smallest coeff is 1
  largest = X.get_value("__max")
  f = X.get_value(e)

  if largest <= 0 or f <= 0:                    # otherwise the math.log() blows up!
    return 0

  fc_max = math.floor(0.5 - math.log(smallest/largest,2)) + 1  # NB: the + 1 is important, else the smallest element in X gets reported as not in set.
  return 1 - math.floor(0.5 - math.log(f/largest,2))/fc_max
  
def map_to_topic(dict,e,t=0):
  result = []
  for label,sp in dict.items():
    value = fast_normed_frequency_class(e,sp)
    if value > t:
      result.append((label,value))
#  return result                                  # non-normalization version
# normalization version:
  if len(result) == 0:
    return []
  the_sum = sum(value for label,value in result)
  r2 = []
  if the_sum > 0:
    for label,value in result:
      r2.append((label, 100*value/the_sum))
  return r2

# bah. Seems easier to use superpositions than lists of (label,value) pairs.
# I wonder which is faster/slower?
def map_to_topic_sp(dict,e,t=0):
  result = superposition()
  for label,sp in dict.items():
    value = fast_normed_frequency_class(e,sp)
    if value > t:
      result.add(label,value)
  return result.normalize(100)


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

# pretty print a float:
def float_to_int(x,t=2):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

def print_find_topic(sw_dict,word,number_of_results):
  # find matching topics:
  result = map_to_topic_sp(sw_dict,word)

  # check we have a result:
  if len(result) == 0:
    print()
    return

  # sort the results:
  sorted_result = sorted(result.dict.items(), key = lambda x: x[1], reverse = True)[:number_of_results]

  # format the results a little:
  # NB: the [4:] is to remove the "WP: " prefix. May later change our frequency list to not have this prefix.
  r = [(str(k+1), label.replace('&colon;',':')[4:], float_to_int(value)) for k,(label,value) in enumerate(sorted_result) ]

  # print the result:
  print_table(r)
  print()

sw_dict = load_simple_sw_into_dict(source,op)
print_find_topic(sw_dict,word,number_of_results)

# interactive wiki similarity:
if interactive:
  while True:
    line = input("Enter word: ")
    word = line.strip().lower()
    if len(word) == 0:
      continue

  # exit the agent:
    if word in ['q']:
      break

    print_find_topic(sw_dict,word,number_of_results)

