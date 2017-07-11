#!c:/Python34/python.exe

#######################################################################
# given a sequence with repeating subsequences, learn those subsequences
# not even sure this idea will work neatly ....
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-07-08
# Update: 2017-7-9
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

np.set_printoptions(linewidth=180)


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
    my_label = '__nolegend__'
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

  def shift_left(self, w=1):
    seq = copy.deepcopy(self)
    seq.data = seq.data[w:]
    return seq

  def similar_index(self, sp):
    r = superposition()
    for k, elt in enumerate(self.data):
      similarity = simm(elt, sp)
      if similarity > 0:
        r.add(str(k), similarity)
    return r.coeff_sort()

  def similar_sequence_offset(self, seq):
    p = len(seq)
    r = superposition()
    for k, elt in enumerate(self.pure_ngrams(p)):
      similarity = seq_simm(elt, seq)                 # list_simm instead??
      if similarity > 0:
        r.add(str(k), similarity)
    return r.coeff_sort()


  def ngrams(self, p):
    seq = sequence(self.name)
    for i in range(min(len(self.data)+1,p) - 1):
      seq.data = self.data[0:i+1]
      yield copy.deepcopy(seq)
    for i in range(len(self.data) - p + 1):
      seq.data = self.data[i:i+p]
      yield copy.deepcopy(seq)

  def pure_ngrams(self, p):
    seq = sequence(self.name)
    for i in range(len(self.data) - p + 1):
      seq.data = self.data[i:i+p]
      yield copy.deepcopy(seq)                         # yeah, need this for list(seq.pure_ngrams(k)) to work.

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
  if len(A) == 0:
    return 0
  similarity = 1
  for k in range(len(A)):
    value_simm = simm(A[k], B[k])                    # using simm on elements in the sequences, so it must be a sequence of superpositions
    if strict:
      similarity = min(similarity, value_simm)
    else:
      similarity = (similarity + value_simm)/2
  return similarity


def rescaled_list_simm(f,g):
  if len(f) != len(g):
    return 0
  the_len = len(f)

# rescale step, first find size:
  s1 = sum(abs(f[k]) for k in range(the_len))
  s2 = sum(abs(g[k]) for k in range(the_len))

# if s1 == 0, or s2 == 0, we can't rescale:
  if s1 == 0 or s2 == 0:
    return 0

  wfg = sum(abs(f[k]/s1 - g[k]/s2) for k in range(the_len))

  return 1 - wfg/2


# input is a list of sequences,
# currently output is a list of lists. Tweak later.
#
def average_categorize_seq_fragments(data,t):
  out_list = []
  for r0 in data:
    r = np.array(r0[:])                                # convert a sequence to a numpy array
    if r.max() == 0:
      continue
    print("r:",r)
    best_k = -1
    best_simm = 0
    for k,sp in enumerate(out_list):
      similarity = rescaled_list_simm(r,sp[1])
      if similarity > best_simm:
        best_k = k
        best_simm = similarity
    print("max k:", len(out_list))
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append([1,r])
    else:
      out_list[best_k][0] += 1
      out_list[best_k][1] = out_list[best_k][1] + r*best_simm       # this line is why we cast r to np array.
  sequences = []                                              # convert to list comprehension later.
  for k,r in enumerate(out_list):
    seq = sequence('ave seq: ' + str(k), r[1])
    sequences.append(seq) 
    r_sum = np.sum(r[1])
    r_count = r[0]
    print("count: %s\tsum: %s\tr: %s " % (r_count, r_sum, r[1]))
  return sequences


def print_sw_dict(dict, op=''):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op, label, sp))         # add coeff_sort() if sp is superposition?

# assumes input_seq is a sequence of ints or floats, for now
#
def average_categorize_sequence(input_seq, ngram_size, threshold):
  seq_ngrams = list(input_seq.pure_ngrams(ngram_size))
  ave_seq_ngrams = average_categorize_seq_fragments(seq_ngrams, threshold)
  return ave_seq_ngrams

def learn_subsequences_v1(full_seq):                                            # ugly mess, fix later!!!
  full_seq.display()

  start = 0
  n = len(full_seq)
  subsequences = []
  previous_x = sequence('empty seq')
  working_seq = full_seq
  while len(working_seq) > 0:
    len_previous_r = 0
    for x in working_seq.ngrams(n):
      x.display()
      r = full_seq.similar_sequence_offset(x)
      print("r: %s\n" % r)
      if len(x) == 1 and len(r) == 1:
        break
      #if len(r) < len_previous_r:
      if len(r) != len_previous_r and len(x) > 1:
      #if len(r) == 1 and len(r) < len_previous_r:
        subsequences.append(previous_x)
        print("subsequence:")
        previous_x.display()
        print("-----------")
        break
      previous_x = x
      len_previous_r = len(r)
    working_seq = working_seq.shift_left(len(previous_x))
  print("=================")
  for seq in subsequences:
    print("\nsubsequence:")
    seq.display()

def similar_sequence_offset(full_seq, seq_frag):
  p = len(seq_frag)
  r = superposition()
  for k, elt in enumerate(self.pure_ngrams(p)):
    similarity = seq_simm(elt, seq_frag)                 # list_simm instead??
    if similarity > 0:
      r.add(str(k), similarity)
  return r.coeff_sort()


def learn_subsequences_v2(full_seq):
  end_marker = superposition()
  end_marker.add("end of seq")
  full_seq += [end_marker]
  full_seq.display()
  working_seq = full_seq[:]
  start = 0
  n = len(full_seq)
  subsequences = []
  partition_points = []
  while start < n:
    previous_seq = []
    previous_r = superposition()
    for i in range(0, n - 1):
      #if i == 0:
      #  start += 1
      #  break
      print("i: %s, start: %s" % (i, start))
      seq = working_seq[start:start + i + 1]
      print("seq:", ", ".join(str(x) for x in seq))
      #if seq in subsequences:
      #  start += len(seq)
      #  break
      r = full_seq.similar_sequence_offset(seq)
      print("r: %s\n" % r)
      if i == 1 and len(r) == 1:
        #start += 1
        break
#      if simm(seq[-1], seq[-2]) > 0.8:                # hack!
#        break
      #if len(r) < len(previous_r):
      #  print("len(previous_seq): %s" % len(previous_seq))
      if len(r) < len(previous_r) and i > 1:
      #if len(r) == 1:
        #if previous_seq not in subsequences:
        subsequences.append(previous_seq)
        print("***** sub seq:", ", ".join(str(x) for x in previous_seq))
        partition_points.append((start, start + i - 1))
        print("***** partition points: %s %s" % (start, start + i -1))
        break
      previous_seq = seq
      previous_r = r
    #start += len(previous_seq)
    start += i
  for seq in subsequences:
    print("seq:", ", ".join(str(x) for x in seq))  
  print("partition points:", partition_points)
  full_seq.display()

def learn_subsequences(full_seq):
  def filter(r):
    r2 = [r[0]]
    for k in range(1,len(r)):
      if int(r[k]) == int(r[k-1]) + 1:
        continue
      r2.append(r[k])
    return r2

  end_marker = superposition()
  end_marker.add("end of seq")
  full_seq += [end_marker]

  working_seq = full_seq[:]
  n = len(full_seq)
  partition_points = []
  subsequences = []
  start = 0
  while start < n:
    previous_r3 = []
    for i in range(n):
      print("\ni: %s, start: %s" % (i, start))
      seq = working_seq[start:start + i + 1]
      print("seq:", ", ".join(str(x) for x in seq))
      r = full_seq.similar_sequence_offset(seq)                     # really shouldn't be using this every iteration!
      print("r: %s" % r)
      r2 = list(r.dict)
      print("r2: %s" % r2)
      r3 = filter(r2)
      print("r3: %s" % r3)
      if i == 1 and len(r3) == 1:
        break
      if len(r3) < len(previous_r3) and i > 1:
        partition_points.append((start, start + i - 1))
        sub_seq = full_seq[start:start + i]
        subsequences.append(sub_seq)
        print("***** sub seq:", ", ".join(str(x) for x in sub_seq))
        print("***** partition points: %s %s" % (start, start + i -1))
        break
      previous_r3 = r3
    start += i
  for seq in subsequences:
    print("seq:", ", ".join(str(x) for x in seq))
  print("partition points:", partition_points)
  full_seq.display()


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
  f = superposition()
  f.add('f')
  g = superposition()
  g.add('g')
  h = superposition()
  h.add('h')
  i = superposition()
  i.add('i')
  x = superposition()
  x.add('x')
  y = superposition()
  y.add('y')
  z = superposition()
  z.add('z')



  sp_seq = sequence('sp seq', [a,b,c,d,e,f,g,h,i])
  sp_seq.display()

  sp_seq2 = sequence('sp seq1', [a,c,b,d,e])
  sp_seq2.display()

  strict_similarity = seq_simm(sp_seq, sp_seq2)
  similarity = seq_simm(sp_seq, sp_seq2, False)
  print("strict similarity:", strict_similarity)
  print("similarity:", similarity)

  seq_frag = sequence('seq frag', [c,d,e,f])
  r = sp_seq.similar_sequence_offset(seq_frag)
  print("r:",r)

  seq_frag = sequence('seq frag', [f,g,h])
  r = sp_seq.similar_sequence_offset(seq_frag)
  print("r:",r)


  full_seq = sequence('full seq', [a,b,c,d,e,f,g,h,i, b,c,d, h,i,b, a,b,c,d])
  learn_subsequences(full_seq)

  full_seq2 = sequence('full seq 2', [a,b,c,d,e,f,g,h,i, a,b,c,d, h,i,b, a,b,c,d])
  learn_subsequences(full_seq)

  full_seq3 = sequence('full seq 3', [a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f,h, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
  learn_subsequences(full_seq3)

  #full_seq4 = sequence('full seq 4', [e,h,h,e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f,h, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
  full_seq4 = sequence('full seq 4', [e,h,h,e,e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,h,d, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
  learn_subsequences(full_seq4)

  full_seq5 = sequence('full seq 5', [x,x,x,x,x, e,h,h,e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f,h, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
  learn_subsequences(full_seq5)

  full_seq6 = sequence('full seq 6', [x,x,x,x,x, e,h,h,e,e,e, x,x,x,x, a,b,c,d])
  learn_subsequences(full_seq6)

  return

  triangle = sequence('triangle', [0.0,0.08,0.16,0.24,0.32,0.4,0.48,0.56,0.64,0.72,0.8,0.88,0.96,1.04,0.92,0.84,0.76,0.68,0.6,0.52,0.44,0.36,0.28,0.2,0.12,0.04])
  the_len = len(triangle)
  input_seq = sequence('input seq') + triangle + triangle + triangle + triangle + triangle + triangle + triangle
  plot_sequences([input_seq], 5*the_len) 
  working_sequences = average_categorize_sequence(input_seq, the_len, 0.4)     # 0.98
  plot_sequences(working_sequences, 6*the_len)

  square = sequence('square', [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0])
  the_len = len(square)
  input_seq = sequence('input seq') + square + square + square + square + square
  working_sequences = average_categorize_sequence(input_seq, the_len, 0.7)    # 0.98
  plot_sequences(working_sequences, 6*the_len)
  

test_code()

# learn some float sequences:
zero = sequence('zero', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#square = sequence('square', [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0])
square = sequence('square', [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0])
triangle = sequence('triangle', [0.0,0.08,0.16,0.24,0.32,0.4,0.48,0.56,0.64,0.72,0.8,0.88,0.96,1.04,0.92,0.84,0.76,0.68,0.6,0.52,0.44,0.36,0.28,0.2,0.12,0.04])
sin = sequence('sin', [0.0,0.1,0.199,0.296,0.389,0.479,0.565,0.644,0.717,0.783,0.841,0.891,0.932,0.964,0.985,0.997,1.0,
0.992,0.974,0.946,0.909,0.863,0.808,0.746,0.675,0.598,0.516,0.427,0.335,0.239,0.141,0.042,-0.058,-0.158,-0.256,
-0.351,-0.443,-0.53,-0.612,-0.688,-0.757,-0.818,-0.872,-0.916,-0.952,-0.978,-0.994,-1.0,-0.996,-0.982,-0.959,
-0.926,-0.883,-0.832,-0.773,-0.706,-0.631,-0.551,-0.465,-0.374,-0.279,-0.182,-0.083])


