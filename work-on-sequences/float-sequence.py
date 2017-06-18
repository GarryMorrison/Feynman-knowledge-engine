#!/usr/bin/env python3

#######################################################################
# implement a python version of the float-sequence idea
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-06-18
# Update:
# Copyright: GPLv3
#
# Usage: ./float-sequence.py [float1 float2 ... ]
#
#######################################################################


import sys
import math
import numpy as np
from collections import OrderedDict
import random


# define our named-lists:
Pi = ['Pi', 3, '.', 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9]
e = ['e', 2, '.', 7, 1, 8, 2, 8, 1, 8, 2, 8, 4]
boys = ['boy sentence', 'boys', 'eat', 'many', 'cakes']
girls = ['girl sentence', 'girls', 'eat', 'many', 'pies']

# define our collection of named-lists:
#data = [Pi]
#data = [Pi, e]
data = [Pi, e, boys, girls]


def str_to_float(s):
  try:
    x = float(s)
  except:
    x = s
  return x


# define our input-sequence:
if len(sys.argv) > 1:
  input_seq = [str_to_float(x) for x in sys.argv[1:] ]
else:
  input_seq = [3.2, 1]


# pretty print a float:
def float_to_int(x,t=4):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))


class sequence(object):
  def __init__(self, name=''):
    self.name = name
    self.data = []

  def __len__(self):
    return len(self.data)

#  def __str__(self):                   # is there a clean way to display a sequence of superpositions?
   
  def add(self, sp):
    self.data.append(sp)

  def similar_index(self, sp):
    r = superposition()
    for k, elt in enumerate(self.data):
      similarity = simm(elt, sp)  
      if similarity > 0:
        r.add(str(k), similarity)
    return r.coeff_sort()


class superposition(object):
  def __init__(self):
#    self.dict = {}                     # faster and cheaper than OrderedDict() if you don't need to preserve order
    self.dict = OrderedDict()

  def __str__(self):
    list_of_kets = []
    for key,value in self.dict.items():
      if value == 1:
        s = "|%s>" % key
      else:
        s = "%s|%s>" % (float_to_int(value), key)
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

  def pick(self, n):
    r = superposition()
    for key in random.sample(list(self.dict), n):
      value = self.dict[key]
      r.add(key,value)
    return r

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

  def coeff_sort(self):                                    # implement ket_sort() too?
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


# can we tidy and optimize this ugly thing??
def simm(A,B):
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


def print_sw_dict(dict, op=''):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op, label, sp))


def gaussian_scalar_encoder(n):
  def guassian(x, a, sigma):
    return math.exp(-(x - a)**2 / 2 * sigma**2)
  w = 1                                     # hard wire in our Gaussian parameters. Feel free to tweak. Especially sigma.
  dx = 0.1
  sigma = 3.5
  r = superposition()
  for a in np.arange(n - w, n + w + dx, dx):
    value = guassian(n, a, sigma)
    #print(a, value)
    r.add(str(a), value)
  return r

def first_random_encoder(n):
  full_range = superposition()
  for a in range(65536):
    full_range.add(str(a + 1))
  return full_range.pick(n)

def random_encoder(n):
  r = superposition()
  for key in random.sample(range(65536), n):
    r.add(str(key + 1))
  return r

def first_full_encoder(x):
  if type(x) in [int, float]:
    r = gaussian_scalar_encoder(x)
  else:
    r = random_encoder(10)
  return r

def full_encoder(encode_dict, x):                 # this is where the magic happens.
  if x in encode_dict:                            # converts input into encoded input.
    return encode_dict[x]
  if type(x) in [int, float]:
    r = gaussian_scalar_encoder(x)
  else:
    r = random_encoder(10)
  encode_dict[x] = r
  return r

def map_named_list_to_encoded_sequence(input_list):
  seq = sequence(input_list[0])                     # learn the name of the sequence
  for x in input_list[1:]:
    sp = gaussian_scalar_encoder(x)
    seq.add(sp)
  return seq

def map_named_list_to_encoded_sequence_v2(encode_dict, input_list):
  seq = sequence(input_list[0])                     # learn the name of the sequence
  for x in input_list[1:]:
    if x not in encode_dict:                        # only encode an object once, then store in encode_dict
      sp = full_encoder(x)                          # this is needed when the random_encoder() kicks in.
      encode_dict[x] = sp
    else:
      sp = encode_dict[x]
    seq.add(sp)
  return encode_dict, seq

def map_named_list_to_encoded_sequence_v3(encode_dict, input_list):
  seq = sequence(input_list[0])                     # learn the name of the sequence
  for x in input_list[1:]:
    sp = full_encoder(encode_dict, x)
    seq.add(sp)
  return seq
  

# just some testing code. Remove later!
def test_code():
  r = gaussian_scalar_encoder(10)
  print("r:",r)
  r2 = r.pick(3)
  print("r2:",r2)

  r3 = random_encoder(10)
  print("r3:",r3)


  # populate encode_dict:
  encode_dict = {}
  encode_dict['boys'] = random_encoder(10)
  encode_dict['eat'] = random_encoder(10)
  encode_dict['many'] = random_encoder(10)
  encode_dict['cakes'] = random_encoder(10)
  encode_dict['girls'] = random_encoder(10)
  encode_dict['pies'] = random_encoder(10)

  print_sw_dict(encode_dict, 'encode')

  seq = map_named_list_to_encoded_sequence(Pi)
  three = gaussian_scalar_encoder(3)
  r4 = seq.similar_index(three)
  print("r4:",r4)

#test_code()


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


def float_sequence(input_seq, data):
  def filter_working_table(encode_dict, table, element, position):
    #print("%s: %s" % (position, element))
    element_pattern = full_encoder(encode_dict, element)
    new_table = []
    for name, coeff, seq_list in table:
      try:
        seq_element = seq_list[position]
        seq_element_pattern = full_encoder(encode_dict, seq_element)
        #print("seq_element:",seq_element)
        #print("seq_element_pattern:",seq_element_pattern)
        similarity = simm(element_pattern, seq_element_pattern)
        #print("simm:",similarity)
        new_coeff = min(coeff, similarity)                 # perhaps an alternative more tolerant version would be: new_coeff = (coeff + similarity)/2
        if new_coeff > 0:
          new_table.append([name, new_coeff, seq_list])
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
#      seq_str = " . ".join(str(x) for x in seq)
      seq_str = " ".join(str(x) for x in seq)
      table.append([name, coeff_str, seq_str])
    return table

  print("input sequence:", input_seq)
  one = input_seq[0]
  encode_dict = {}
  input_pattern = full_encoder(encode_dict, one)

  # generate encoded_seq:
#  encoded_seq = [ map_named_list_to_encoded_sequence(x) for x in data]
  encoded_seq = [ map_named_list_to_encoded_sequence_v3(encode_dict, x) for x in data]


  # generate working_table:                    # maybe make into own function.
  working_table = []
  for k, seq in enumerate(encoded_seq):
    name = seq.name
    similar_index = seq.similar_index(input_pattern)
    #print(name, similar_index)
    for idx, coeff in similar_index:
      #print("idx: %s, coeff: %s" % (idx, coeff))
      seq_list = data[k][int(idx) + 1:]
      working_table.append([name, coeff, seq_list])

  # filter working_table using the rest of our input sequence:
  for k, element in enumerate(input_seq[1:]):
    working_table = filter_working_table(encode_dict, working_table, element, k + 1)       

  # don't format and print an empty table:
  if len(working_table) == 0:
    return

  # format and print output table:
  print_table(format_output_table(working_table))

  # print out the encode_dict:
  #print_sw_dict(encode_dict, 'encode')

float_sequence(input_seq, data)

