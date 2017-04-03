#!/usr/bin/env python3

#######################################################################
# let's revist the MNIST problem, see if we can improve our results
# last result was 5.4% error
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-04-03
# Update:
# Copyright: GPLv3
#
# Usage: ./mnist-problem.py
#
#######################################################################


import sys
from collections import OrderedDict
import random


# our source sw files:
# first two are our image phi-superpositions,
# the next two are our labels:
train_data_file = "sw-examples/image-phi-superpositions--train-60k--using-edge-enhanced-features--k_5--t_0_4.sw"
test_data_file = "sw-examples/image-phi-superpositions--test-10k--using-edge-enhanced-features--k_5--t_0_4.sw"
train_labels_file = "sw-examples/mnist-train-labels--edge-enhanced.sw"
test_labels_file = "sw-examples/mnist-test-labels--edge-enhanced.sw"


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
      self.dict[str] += float(value)
    else:
      self.dict[str] = float(value)

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

  def reweight(self, weights):
    r = superposition()
    for k, (key, value) in enumerate(self.dict.items()):
      r.add(key, value * weights[k] )
    return r


# load literal superpositions into a dictionary, and handles coeffs other than 1
#
def load_simple_sw_into_dict(filename,op):
  op_head = op + " |"
  sw_dict = {}
  with open(filename,'r') as f:
    for line in f:
      line = line.strip()
      if line.startswith(op_head):
        try:
          head,tail = line.split('> => ',1)
          label = head.split(' |',1)[1]
          sw_dict[label] = superposition()
          for piece in tail[:-1].split('> + '):
#            print("piece:",piece)
            float_piece, string_piece = piece.split('|')
            try:
              float_piece = float(float_piece)
            except:
              float_piece = 1
            sw_dict[label].add(string_piece,float_piece)
        except Exception as e:
          print("Exception reason: %s" % e)
          continue
  return sw_dict


# maybe we should convert these sw_dict functions to a class?
def print_sw_dict(dict,op):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op,label,sp))

def print_sorted_sw_dict(dict,op):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op,label,sp.coeff_sort()))

def reweight_dict(dict, weights):
  new_dict = {}
  for label, sp in dict.items():
    new_dict[label] = sp.reweight(weights)
  return new_dict

def sample_dict(dict, sample_size):
  new_dict = {}
  for label, sp in random.sample(dict.items(), sample_size):
    new_dict[label] = sp
  return new_dict


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

# pretty print a float:
def float_to_int(x,t=4):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

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



# load up the data from our sw files:
train_data = load_simple_sw_into_dict(train_data_file, "train-phi-sp")
test_data = load_simple_sw_into_dict(test_data_file, "log-phi-sp")
train_labels = load_simple_sw_into_dict(train_labels_file, "train-label")
test_labels = load_simple_sw_into_dict(test_labels_file, "test-label")

