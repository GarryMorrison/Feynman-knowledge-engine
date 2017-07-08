#!c:/Python34/python.exe

#######################################################################
# given a sequence with repeating subsequences, learn those subsequences
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-07-08
# Update:
# Copyright: GPLv3
#
# Usage: ./subseqlearn.py
#
#######################################################################


import sys
import random
import copy
import math
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt



# pretty print a float:
def float_to_int(x,t=3):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

# define our encoders:
# the plan is to add more as needed.
def gaussian_scalar_encoder(x):
  def guassian(x, a, sigma):
    return math.exp(-(x - a)**2 / 2 * sigma**2)
  w = 1                                     # hard wire in our Gaussian parameters. Feel free to tweak. Especially sigma.
  dx = 0.1
  sigma = 3.5
  r = superposition()
  for a in np.arange(x - w, x + w + dx, dx):
    value = guassian(x, a, sigma)
    #print(a, value)                         # this line is helpful when tuning our Gaussian paramters: w,dx,sigma.
    r.add(float_to_int(a,1), value)          # may need to tweak the float_to_int() size to 2 say. Nah. Would make superpositions too large.
  return r

def gaussian_2d_encoder(x,y):
  def guassian(x, y, a, b, sigma):
    return math.exp(-(x - a)**2 / 2 * sigma**2  -(y - b)**2 / 2 * sigma**2)
  w = 1                                     # hard wire in our Gaussian parameters. Feel free to tweak. Especially sigma.
  dx = 0.1
  sigma = 3.5
  r = superposition()
  for a in np.arange(x - w, x + w + dx, dx):
    for b in np.arange(y - w, y + w + dx, dx):
      value = guassian(x, y, a, b, sigma)
      r.add(float_to_int(a,1) + ": " + float_to_int(b,1), value)          # may need to tweak the float_to_int() size to 2 say.
  return r

def gaussian_3d_encoder(x,y,z):             # this thing spits out quite large superpositions, so will potentially be slow in seq2name.
  def guassian(x, y, z, a, b, c, sigma):
    return math.exp(-(x - a)**2 / 2 * sigma**2  -(y - b)**2 / 2 * sigma**2  -(z - c)**2 / 2 * sigma**2)
  w = 1                                     # hard wire in our Gaussian parameters. Feel free to tweak. Especially sigma.
  dx = 0.1
  sigma = 3.5
  r = superposition()
  for a in np.arange(x - w, x + w + dx, dx):
    for b in np.arange(y - w, y + w + dx, dx):
      for c in np.arange(z - w, z + w + dx, dx):
        value = guassian(x, y, z, a, b, c, sigma)
        r.add(float_to_int(a,1) + ": " + float_to_int(b,1) + ": " + float_to_int(c,1), value)  # may need to tweak the float_to_int() size to 2 say.
  return r

def gaussian_tuple_encoder(t):                   # hrmm.... need to handle if tuple elements are not int or float.
  if len(t) == 2:
    return gaussian_2d_encoder(t[0],t[1])
  if len(t) == 3:
    return gaussian_3d_encoder(t[0],t[1],t[2])
  else:
    return random_encoder(10)

def ngram_str_encoder(s):                         # simple string similarity encoder. 
  r = superposition()
  seq = sequence('ngram encoder', list(s))
  for x in seq.pure_ngrams(1):
    ngram = x[0]
    r.add(ngram)                                   # maybe give different ngram sizes different weights?
  for x in seq.pure_ngrams(2):
    ngram = "".join(x)
    r.add(ngram)
  for x in seq.pure_ngrams(3):
    ngram = "".join(x)
    r.add(ngram)
  return r

def random_encoder(n):
  r = superposition()
  for key in random.sample(range(65536), n):      # even at 65,536 there are still occasional "collisions".
    r.add(str(key + 1))
  return r

def full_encoder(encode_dict, x):                 # this is where the magic happens!
  if x in encode_dict:                            # converts input into encoded input.
    return encode_dict[x]                         # if you implement more interesting encoders, this is where you would use them.
  if type(x) in [superposition]:                  # don't encode something that is already encoded.
    return x
  if type(x) in [int, float, np.float64]:
    r = gaussian_scalar_encoder(x)
  elif type(x) in [tuple]:
    r = gaussian_tuple_encoder(x)
  elif type(x) in [str]:
    r = ngram_str_encoder(x)                       # this is a string similarity encoder. A semantic similarity encoder would be cooler!
  else:
    r = random_encoder(10)                         # random encoder desgined to not have similarity with anything else.
  encode_dict[x] = r
  return r


# define our plot functions:
# tidy later!
def plot_2tuple_sequences(sequences):              # assumes 2tupples are (x1,y1) pairs, not (t1, x1) pairs. Might not be an issue.
  colours = 'bgrcmyk'                              # colours to cycle through
  colour_index = 0
  for seq in sequences:
    my_label = seq.name
    my_linewidth = 1.0
    if my_label == 'input seq':
      my_linewidth = 5.0
    for pair in seq.pure_ngrams(2):
      #pair.display()
      #print()
      x0,y0 = pair[0]
      x1,y1 = pair[1]
      plt.plot([x0,x1], [y0,y1], c=colours[colour_index], label=my_label, linewidth=my_linewidth)
      my_label = '__nolegend__'
    colour_index = (colour_index + 1) % 7
  #plt.legend(loc='upper right')
  plt.legend(loc='best')
  plt.show()

def force_str_to_float(s):
  try:
    x = float(s)
  except:
    x = 0
  return x

def all_sequences_of_same_type(sequences, my_type):
  for seq in sequences:
    if not all(type(x) == my_type for x in seq):
      return False
  return True

def plot_float_sequences(sequences, max_plot_len):
  for seq in sequences:
    my_label = seq.name
    my_linewidth = 1.0
    if my_label == 'input seq':
      my_linewidth = 5.0
    data = [force_str_to_float(x) for x in seq[:max_plot_len] ]
    plt.plot(data, label=my_label, linewidth=my_linewidth)
  #plt.legend(loc='upper right')
  plt.legend(loc='best')
  plt.show()


def plot_sequences(sequences, max_plot_len = 30):
  first_elt = sequences[0][0]
  if type(first_elt) in [tuple] and len(first_elt) == 2:  # assume if the first element in the first sequence is a 2-tuple, so are the rest.
    plot_2tuple_sequences(sequences)
  elif all_sequences_of_same_type(sequences, str):        # do we really need to walk all our sequences? Does it matter?
    pass
  else:
    plot_float_sequences(sequences, max_plot_len)


class sequence(object):
  def __init__(self, name='', data = []):
    self.name = name
    self.data = data

  def __len__(self):
    return len(self.data)

  def __getitem__(self, key):
    return self.data[key]

  def __add__(self, seq):              # tidy later!
    if type(seq) in [sequence]:
      r = copy.deepcopy(self)
      r.data += seq.data
      return r
    if type(seq) in [list]:
      r = copy.deepcopy(self)
      r.data += seq
      return r
    else:
      return NotImplemented

  def display(self):                   # print out a sequence class
    for k,x in enumerate(self.data):
      if type(x) in [superposition]:
        print("seq |%s: %s> => %s" % (self.name, str(k), x.coeff_sort())) # not super happy with this.
      else:
        print("seq |%s: %s> => %s" % (self.name, str(k), x))

  def display_minimalist(self):
    for x in self.data:
      if type(x) in [superposition]:
        print(x.coeff_sort())                                              # not super happy with this.
      else:
        print(x)

  def add(self, seq):
    self.data.append(seq)

  def similar_index(self, sp):
    r = superposition()
    for k, elt in enumerate(self.data):
      similarity = simm(elt, sp)
      if similarity > 0:
        r.add(str(k), similarity)
    return r.coeff_sort()

  def ngrams(self, p):
    seq = sequence(self.name)
    for i in range(min(len(self.data)+1,p) - 1):
      seq.data = self.data[0:i+1]
      yield seq
    for i in range(len(self.data) - p + 1):
      seq.data = self.data[i:i+p]
      yield seq

  def pure_ngrams(self, p):
    seq = sequence(self.name)
    for i in range(len(self.data) - p + 1):
      seq.data = self.data[i:i+p]
      yield seq

  def encode(self, encode_dict):
    seq = sequence(self.name, [])
    for x in self.data:
      sp = full_encoder(encode_dict, x)
      seq.add(sp)
    return seq

  def noise(self, t):
    seq = sequence(self.name, [])
    for x in self.data:
      try:
        value = x + np.random.normal(0, t)               # enable adding noise to superpositions??
      except:
        value = x
      seq.add(value)
    return seq

  def smooth(self, k):                                    # hrmm... maybe if type superposition, apply coeff_sort()?
    try:
      arr = [self.data[0]] + self.data + [self.data[-1]]
      for _ in range(k):
        new_arr = arr[:]
        for i in range(len(self.data)):
          new_arr[i+1] = arr[i]/4 + arr[i+1]/2 + arr[i+2]/4
        arr = new_arr
      seq = sequence(self.name, [])
      seq.data = arr[1:-1]
      return seq
    except:
      return self

  def delta(self, dx = 1):                           # how do we handle sequences of 2tuples?
    try:
      arr = self.data + [self.data[-1]]              # how do we want to handle boundaries?
      new_arr = arr                                  # do we need [:]?
      #for i in range(len(self.data)):
      for i in range(len(self.data) - 1):            # how do we want to handle boudaries?
        new_arr[i] = (arr[i+1] - arr[i])/dx
      seq = sequence(self.name, [])
      #seq.data = new_arr[:-1]
      seq.data = new_arr[:-2]
      return seq
    except Exception as e:
      #print("delta exception:", e)
      return self
    
  def seq2sp(self):                                      # needs more thinking. Also, only works for sequences of superpositions.
    r = superposition()                                  # don't even know if useful yet.
    for x in self.data:
      r += x
    return r

# a superposition is a collection of float,string pairs, displayed using ket notation.
class superposition(object):
  def __init__(self):
#    self.dict = {}                     # faster and cheaper than OrderedDict() if you don't need to preserve order
    self.dict = OrderedDict()

  def __str__(self):
    list_of_kets = []
    for key,value in self.dict.items():
      if value == 1.0:
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

  def __truediv__(self, divisor):
    if type(divisor) in [int, float]:
      r = superposition()
      for key,value in self.dict.items():
        r.dict[key] = value/divisor
      return r
    else:
      return NotImplemented

  def __add__(self, sp):
    if type(sp) in [superposition]:
      r = copy.deepcopy(self)
      for key,value in sp.dict.items():
        r.add(key, value)
      return r
    else:
      return NotImplemented

  def __sub__(self, sp):
    if type(sp) in [superposition]:
      r = copy.deepcopy(self)
      for key,value in sp.dict.items():
        r.add(key, - value)
      return r
    else:
      return NotImplemented

  def add(self,str,value=1):
    if str in self.dict:
      self.dict[str] += float(value)
    else:
      self.dict[str] = float(value)

  def max_add(self, str, value = 1):
    if str in self.dict:
      self.dict[str] = max(self.dict[str], float(value))
    else:
      self.dict[str] = float(value)

  def display(self):
    list_of_pairs = []
    for key,value in self.dict.items():
      if value == 1.0:
        s = "%s" % key
      else:
        s = "%s %s" % (float_to_int(value), key)
      list_of_pairs.append(s)
    return ",\t".join(list_of_pairs)

  def pair(self):                               # if the dict is longer than 1 elt, this returns a random pair
    for key,value in self.dict.items():         # presuming not using an OrderedDict
      return key, value

  def pick(self, n):                            # randomly pick and return n elements from the superposition
    r = superposition()
    for key in random.sample(list(self.dict), n):
      value = self.dict[key]
      r.add(key,value)
    return r

  def get_value(self,str):                      # maybe convert to  __getitem__
    if str in self.dict:
      return self.dict[str]
    else:
      return 0                                 # maybe return None?

  def the_value(self):                         # if the dict is longer than 1 elt, this returns a random value
    for key,value in self.dict.items():
      return value
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


# simm(A,B) returns the similarity in [0,1] of two superpositions:
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


# sequence similarity measure
# returns in range [0,1], 
# 1 for exact match, 0 for no match, values in between otherwise.
#
def seq_simm(A, B, strict=True):
  if len(A) != len(B):
    return 0
  similarity = 1
  for k in range(len(A)):
    value_simm = simm(A[k], B[k])                    # using simm on elements in the sequences, so it must be a sequence of superpositions
    if strict:
      similarity = min(similarity, value_simm)
    else:
      similarity = (similarity + value_simm)/2
  return similarity



def print_sw_dict(dict, op=''):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op, label, sp))         # add coeff_sort() if sp is superposition?


# testing our code, delete later
def test_code():
  a = superposition()
  a.add('a')
  b = superposition()
  b.add('b')
  c = superposition()
  c.add('c')
  d = superposition()
  d.add('d')
  e = superposition()
  e.add('e')


  sp_seq = sequence('sp seq', [a,b,c,d,e])
  sp_seq.display()

  sp_seq2 = sequence('sp seq1', [a,c,b,d,e])
  sp_seq2.display()

  strict_similarity = seq_simm(sp_seq, sp_seq2)
  similarity = seq_simm(sp_seq, sp_seq2, False)
  print("strict similarity:", strict_similarity)
  print("similarity:", similarity)

test_code()
