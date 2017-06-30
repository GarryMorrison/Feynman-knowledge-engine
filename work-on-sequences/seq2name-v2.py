#!c:/Python34/python.exe

#######################################################################
# given an input sequence, guess its name
# sequence class version.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-06-25
# Update: 2017-6-30
# Copyright: GPLv3
#
# Usage: ./seq2name-v2.py [a b c d e ... ]
#
# eg: detect Fibonacci, despite a couple of typo's:
# ./seq2name-v2.py 1 1 2 3 5 7 13 21 36
#
# eg: detect the alphabet, despite a gap:
# ./seq2name-v2.py a b c g h i j k l m
#
# eg: detect a curve:
# ./seq2name-v2.py 0 0 2 2 2 2
# 
# set max_number_of_predictions_to_return to 7 then:
# ./seq2name-v2.py 0 0 2 2 1.5 1.5 1.6 1.7 1.4 1.5 1.1 1.1 1.1
# ./seq2name-v2.py 0 0 2 2 1.5 1.5 1.6 1.7 1.4 1.5 1.1 1.1 1.1 1.3 1.2 1.9 1.7 1.7 1.6 1.5 1.8
#
# eg: detect a pathway:
# ./seq2name-v2.py '(1,1)' '(1,2)' '(1,3)' '(1,4)'
# ./seq2name-v2.py '(4,3)' '(5,3)' '(5,4)'
# ./seq2name-v2.py '(4,3)' '(4,4.5)' '(4,5.5)'
# ./seq2name-v2.py '(3.6,3.5)' '(4,4.5)' '(4,5.5)' '(5,5.7)' '(6.3,5.2)'
#
# TODO: ngram version of float-sequence, similar to full_seq2name 
#######################################################################


import sys
import numpy as np
import math
from collections import OrderedDict
import random
import copy
from ast import literal_eval
import matplotlib.pyplot as plt


# either print all matches, or best match only (much easier to read)
print_best_match_only = False

# only print name when it changes from one step to the next:
print_delta_only = False

# max length of sequence prediction. eg 5 or 10 is good.
max_output_len = 20

# max length of input sequence (ie, how far back does our sequence memory go). eg 5 or 6 is good.
max_input_len = 5
#max_input_len = 10

# number of smooth iterations, 0 for off:
# the smaller max_input_len is, the smaller smooth_count_frag should be.
# Likewise, the larger max_input_len is, the larger smooth_count_frag should be.
# NB: breaks integer sequence detection. eg, Pi: 1 4 1 5 9. In which case set it to 0.
# NB: if a sequence contains a string element, smooth_count is swithced off.

# smooth count for full input sequence:
#smooth_count_full = 5
smooth_count_full = 0

# smooth count for ngram fragment of input sequence:
smooth_count_frag = 0

# smooth count for final sequence:
smooth_count_final = 0

# smooth count for individual sequences in data[]
smooth_count_data = 0

# switch on/off strict similarity:
# ie, new_coeff = min(coeff, similarity)
# vs: new_coeff = (coeff + similarity)/2
strict_similarity = False


# ignore answers below this noise threshold, in percent:
noise_threshold = 0.1
#noise_threshold = 0

# max number of predictions to return, and hence graph, from float_sequence:
max_number_of_predictions_to_return = 7

# max plot length:
max_plot_len = 30



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
  if type(x) in [superposition]:                  # don't encode something that is already encoded. May delete this line later.
    return x
  if type(x) in [int, float, np.float64]:
    r = gaussian_scalar_encoder(x)
  elif type(x) in [tuple]:
    r = gaussian_tuple_encoder(x)
  elif type(x) in [str]:
    r = ngram_str_encoder(x)                       # this is a string similarity encoder. A semantic similarity encoder would be more fun!
  else:
    r = random_encoder(10)                         # random encoder desgined to not have similarity with anything else.
  encode_dict[x] = r
  return r


# define our plot functions:
# tidy later!
def plot_2tuple_sequences(sequences):         
  colours = 'bgrcmyk'                               # colours to cycle through
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
      seq.data = new_arr[:-1]
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

  def get_value(self,str):
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


def print_sw_dict(dict, op=''):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op, label, sp))         # add coeff_sort() if sp is superposition?


def test_code():
  seq = sequence('test sequence ngrams', [1,2,3,4,5,6,7])
  seq.add('a')
  seq.add('b')
  seq.add('c')
  seq.add('d')
  seq.display()
  print('--------')
  for x in seq.ngrams(3):
    x.display()
    print()

  Pi = sequence('Pi', [3, '.', 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9])
  Pi.display()
  print(Pi[4])

  encode_dict = {}
  new_Pi = Pi.encode(encode_dict)
  new_Pi.display()

  new_seq = seq.encode(encode_dict)
  print("-----------")
  new_seq.display()
  print("+++++++++++")
  seq.display()

  seq.noise(0.2).encode(encode_dict).display()

  float_seq = sequence('float seq', [1,2,3,4,5,6,7,8,9,10])
  float_seq.display()
  float_seq.smooth(1).display()
  
  a = superposition()
  a.add('a')
  print(a)

  b = a/4
  print(b)

  c = a + b
  print(c)

  x = superposition()
  x.add('x',3)
  y = superposition()
  y.add('y', 5)
  z = superposition()
  z.add('z', 0.333)
  r = x + y + z
  print(r)

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
  sp_seq.smooth(1).display()

  Pi_digits = sequence('Pi', [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9])

  new_seq = sequence('new seq') + Pi + seq + [13,13,13,17,19,23] + sp_seq
  new_seq.display()
#  new_seq.smooth(1).display()          # can't smooth sequence that mixes types. Maybe fix definition of smooth()?
  
  a_seq = sequence('a seq') + Pi_digits + [13,13,13,17,19,23,2]
  a_seq.smooth(1).noise(0.1).display()

  Pi.display()
  print(Pi[3:])
  print([3, '.', 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9][3:])

  print(Pi[0])
  print([3, '.', 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9][0])

  print(Pi[1:])
  print([3, '.', 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9][1:])

  Pi.display()
  Pi.encode(encode_dict).encode(encode_dict).display()

  tuple_seq = sequence('tuple seq', [(3,5), (2,7), (3,5,7)])
  tuple_seq.display()
  tuple_seq.encode(encode_dict).display()

  str_seq = sequence('string seq', ['fish', 'a', 'ab', 'xyz', 'basket'])
  str_seq.encode(encode_dict).display()


  sp_seq = sequence('sp seq', [a,b,c,d,e])
  sp_seq.display()
  sp_seq.delta().display()

 
#test_code()
#sys.exit(0)


# pretty print a table:
# table print tweaked from here: http://stackoverflow.com/questions/25403249/print-a-list-of-tuples-as-table
def print_table(table):
  if len(table) == 0:           # don't print an empty table
    return

  max_length_column = []
  tuple_len = len(table[0])     # assume entire table has the same shape as the first row
  for i in range(tuple_len):
    max_length_column.append(max(len(e[i])+2 for e in table))
  for e in table:
    for i in range(tuple_len):
      print(e[i].ljust(max_length_column[i]), end='')
    print()


# I think this code is correct .... kind of hard to tell :(
def float_sequence(input_seq, data, max_output_len):
  def generate_working_table(data, encoded_sequences, input_pattern):
    working_table = []
    for k, seq in enumerate(encoded_sequences):
      #seq.display()                              # print out our sequences of superpositions
      name = seq.name
      similar_index = seq.similar_index(input_pattern)
      #print(name, similar_index)
      for idx, coeff in similar_index:
        #print("idx: %s, coeff: %s" % (idx, coeff))
        seq_list = data[k][int(idx):]
        working_table.append([name, coeff, seq_list])
    return working_table

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
        if strict_similarity:
          new_coeff = min(coeff, similarity)                 # perhaps an alternative more tolerant version would be: new_coeff = (coeff + similarity)/2
        else:
          new_coeff = (coeff + similarity)/2
        if new_coeff >= noise_threshold/100:                 # convert noise_threshold back from percent
          new_table.append([name, new_coeff, seq_list])
      except:
        continue
    return new_table

  def format_output_table(working_table, max_output_len):
    # first, sort the table:
    sorted_working_table = sorted(working_table, key = lambda x: x[1], reverse = True)

    # now format it:
    sequences = []

    table = [['name', 'similarity', 'prediction']]
    table.append(['----', '----------', '----------'])
    for name, coeff, seq in sorted_working_table:
      coeff_str = float_to_int(100 * coeff)                       # NB: converted to percent
      seq_str = " ".join(str(x) for x in seq[:max_output_len])    # tweak later. For long input sequences, and short max_output_len, predictions are not visible.
      table.append([name, coeff_str, seq_str])

      predicted_seq = sequence(coeff_str + " " + name, seq)
      sequences.append(predicted_seq)
    return sequences, table

  # print input sequence:
  print("input sequence: %s" % input_seq[:] )      # hack to convert sequence type to list.

  # generate encoded_sequences:
  encode_dict = {}
  encoded_sequences = [x.encode(encode_dict) for x in data]

  # generate working table:
  input_pattern = full_encoder(encode_dict, input_seq[0])
  working_table = generate_working_table(data, encoded_sequences, input_pattern)

  # filter working_table using the rest of our input sequence:
  for k, element in enumerate(input_seq[1:]):
    working_table = filter_working_table(encode_dict, working_table, element, k + 1)

  # format and print output table:
  predicted_sequences, table = format_output_table(working_table, max_output_len)
  print_table(table)

  # print out the encode_dict:
  #print_sw_dict(encode_dict, 'encode')

  return predicted_sequences[:max_number_of_predictions_to_return]


def single_seq2name(input_seq, encoded_sequences):
  def generate_working_table(encoded_sequences, input_pattern):
    working_table = []
    for seq in encoded_sequences:
      #seq.display()                              # print out our sequences of superpositions
      name = seq.name
      similar_index = seq.similar_index(input_pattern)
      #print(name, similar_index)
      for idx, coeff in similar_index:
        #print("idx: %s, coeff: %s" % (idx, coeff))
        seq_list = seq[int(idx):]
        working_table.append([name, coeff, seq_list])
    return working_table

  def filter_working_table(table, element_pattern, position):
    new_table = []
    for name, coeff, seq_list in table:
      try:
        seq_element_pattern = seq_list[position]
        similarity = simm(element_pattern, seq_element_pattern)
        #print("simm:",similarity)
        if strict_similarity:
          new_coeff = min(coeff, similarity)                 # perhaps an alternative more tolerant version would be: new_coeff = (coeff + similarity)/2
        else:
          new_coeff = (coeff + similarity)/2
        if new_coeff >= noise_threshold/100:                 # convert noise_threshold back from percent
          new_table.append([name, new_coeff, seq_list])
      except Exception as e:
        #print("filter_working_table exception reason: %s" % e)
        continue
    return new_table

  def format_output_table(working_table, max_len):
    # first, sort the table:
    sorted_working_table = sorted(working_table, key = lambda x: x[1], reverse = True)

    # now format it:
    table = []
    for name, coeff, seq in sorted_working_table:
      coeff_str = float_to_int(coeff)
      #seq_str = " ".join(str(x) for x in seq[:max_len])      # seq is an encoded sequence, so can't display it cleanly.
      #table.append([name, coeff_str, seq_str])
      table.append([name, coeff_str])
    return table

  def find_scores(working_table):
    if len(working_table) == 0:
      r = superposition()
      r.add("ANOMALY")
      return r

    # find a score for each sequence. Improve later! 
    r = superposition()
    for name, coeff, seq in working_table:
      r.max_add(name, 100 * coeff)                                  # maybe there are better options than this simple thing? Also, converted to percent.
    return r.coeff_sort()


  # print input sequence:
  #input_seq.display()

  # generate working table:
  input_pattern = input_seq[0]
  working_table = generate_working_table(encoded_sequences, input_pattern)

  # filter working_table using the rest of our input sequence:
  for k, element_pattern in enumerate(input_seq[1:]):
    working_table = filter_working_table(working_table, element_pattern, k + 1)

  # format and print output table:
  #print_table(format_output_table(working_table, max_input_len))

  return find_scores(working_table)


def full_seq2name(input_seq, data, max_input_len, smooth_count_full, smooth_count_frag):
  # store a copy of the final sequence:
  seq = sequence('seq2name sequence')

  # encode sequences:
  encode_dict = {}
  #encoded_sequences = [x.encode(encode_dict) for x in data]                    # add a smooth option?
  encoded_sequences = [x.smooth(smooth_count_data).encode(encode_dict) for x in data]
  encoded_input_seq = input_seq.smooth(smooth_count_full).encode(encode_dict)

  previous_str_value = ''
  for seq_fragment in encoded_input_seq.ngrams(max_input_len):
    smooth_seq_fragment = seq_fragment.smooth(smooth_count_frag)
    value = single_seq2name(smooth_seq_fragment, encoded_sequences)
    seq.add(value)
    if print_best_match_only:
      str_value = value.select_top(1).display()
    else:
      str_value = value.display()    
      #str_value = str(value)                   # in superposition notation
    if previous_str_value != str_value or not print_delta_only:
      print(str_value)
      previous_str_value = str_value

  return seq


# generate some curves:
def generate_sine_curve(start, finish, dx):
  curve = []
  for a in np.arange(start, finish, dx):
    value = math.sin(a)
    curve.append(value)
  curve = [ round(x, 3) for x in curve]
  for x in curve:
    print(x)

def generate_triangle_curve(w, h, dx):
  def foo1(x):
    return 2*h*x/w
  def foo2(x):
    return -2*h*x/w + 2*h
  curve = []
  for a in np.arange(0, w/2 + dx, dx):
    value = foo1(a)
    curve.append(value)
  for a in np.arange(w/2 + dx, w, dx):
    value = foo2(a)
    curve.append(value)
  curve = [ round(x, 3) for x in curve ]
  for x in curve:
    print(x)


# auto-generate our data:                      # ./seq2name-v2.py | sed 's/$/,/g' | tr -d '\n'
#generate_triangle_curve(25, 1, 1)
#generate_sine_curve(0,2*math.pi, 0.1)
#sys.exit(0)


# learn and name some sequences:
# floats, ints, and strings are all acceptable.
# other types would be too, if you define an appropriate encoder. See: full_encoder()
# start with some integer sequences:
Pi = sequence('Pi', [3, '.', 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4, 6, 2, 6, 4, 3, 3, 8, 3, 2, 7, 9, 5])
e = sequence('e', [2, '.', 7, 1, 8, 2, 8, 1, 8, 2, 8, 4])
Fib = sequence('Fibonacci', [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]) # Fib, and factorial tend to ruin our plots!
factorial = sequence('factorial', [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800])  # so maybe comment them out.
counting_numbers = sequence('counting', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])


# now some string sequences:
boys = sequence('boy sentence', ['boys', 'eat', 'many', 'cakes'])
girls = sequence('girl sentence', ['girls', 'eat', 'many', 'pies'])
alphabet = sequence('alphabet', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

# now some float sequences:
zero = sequence('zero', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#square = sequence('square', [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0])
square = sequence('square', [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0])
triangle = sequence('triangle', [0.0,0.08,0.16,0.24,0.32,0.4,0.48,0.56,0.64,0.72,0.8,0.88,0.96,1.04,0.92,0.84,0.76,0.68,0.6,0.52,0.44,0.36,0.28,0.2,0.12,0.04])
sin = sequence('sin', [0.0,0.1,0.199,0.296,0.389,0.479,0.565,0.644,0.717,0.783,0.841,0.891,0.932,0.964,0.985,0.997,1.0,
0.992,0.974,0.946,0.909,0.863,0.808,0.746,0.675,0.598,0.516,0.427,0.335,0.239,0.141,0.042,-0.058,-0.158,-0.256,
-0.351,-0.443,-0.53,-0.612,-0.688,-0.757,-0.818,-0.872,-0.916,-0.952,-0.978,-0.994,-1.0,-0.996,-0.982,-0.959,
-0.926,-0.883,-0.832,-0.773,-0.706,-0.631,-0.551,-0.465,-0.374,-0.279,-0.182,-0.083])

# now some tuple sequences:
# NB: having tuple sequences in your list of known sequences slows things down.
# so if you don't need them, please omit them! Though tweaks to 2d-gaussian could speed them up.
path_a = sequence('path a', [(1,1), (1,2), (1,3), (2,4), (3,4), (3,5), (3,6), (4,6), (5,6), (6,6), (7,6)])
path_b = sequence('path b', [(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (6,2), (5,3), (5,4), (5,5), (6,5), (7,6)])
path_c = sequence('path c', [(1,1), (1,-1), (0,-0.7), (-2.5,3.2), (-4,2.1), (-5,5), (-7,3), (-8,0)])


# learn our known sequences:
#data = [Pi, e, boys, girls, alphabet, zero, square, triangle, sin, path_a, path_b, path_c]
#data = [Pi, e, Fib, factorial, counting_numbers, boys, girls, alphabet, zero, square, sin, path_a, path_b, path_c]   # dropped triangle, since triangle looks like first half of sin.
#data = [Pi, e, Fib, factorial, counting_numbers, boys, girls, alphabet, zero, square, sin]                           # dropped paths
data = [Pi, e, Fib, factorial, counting_numbers]                       # sequences only
#data = [zero, square, triangle, sin]                                  # curves only
#data = [zero, square, triangle, sin, path_a, path_b, path_c]          # curves and paths only
#data = [boys, girls]                                                  # sentences only
#data = [zero.delta(), square.delta(), triangle.delta(), sin.delta()]   # delta curves only

# quick plot of our curves:
#plot_sequences([zero, square, triangle, sin], 200)

# quick plot of our delta curves:
#plot_sequences([zero.delta()], 200)
#plot_sequences([square.delta()], 200)
#plot_sequences([triangle.delta()], 200)
#plot_sequences([sin.delta(0.1)], 200)        # this is the only interesting one, in my opinion

# quick plot of our paths:
#plot_sequences([path_a, path_b, path_c])
#sys.exit(0)


# if possible, convert a string to a float:
def str_to_float(s):
  try:
    x = float(s)
  except:
    x = s
  return x

# if possible, convert a string to a float, or a tuple:
def str_to_float_tuple(s):
  try:
    x = literal_eval(s)
  except:
    x = s
  return x


# invoke it!
if __name__ == '__main__':

  # define our input-sequence:
  if len(sys.argv) > 1:
    input_seq = sequence('input seq', [str_to_float_tuple(x) for x in sys.argv[1:] ])
  else:
    #input_seq = sequence('input seq', [0.1, 0.2, 0.3])
    input_seq = sequence('input seq') + zero + square + triangle + sin + [7,7,7,7,7,7,7,7,7] + triangle + square + zero
    #input_seq = Pi
    #input_seq = triangle
    #input_seq = square
    #input_seq = sin
    #input_seq = input_seq.noise(0.1)               # add noise to our input sequence
    #input_seq = input_seq.noise(0.2)
    #input_seq = input_seq.delta()                  # convert seq to delta sequence


  # plot input sequence
  #plot_sequences([input_seq], 1000)
  #plot_sequences([input_seq.smooth(5)], 1000)
  #plot_sequences([input_seq.smooth(10)], 1000)
  #plot_sequences([input_seq.delta(0.1)], 1000)
  #sys.exit(0)

  # invoke it!
  print("float_sequence:")
  predicted_sequences = float_sequence(input_seq, data, max_output_len)
  if len(predicted_sequences) > 0:
    plot_sequences([input_seq] + predicted_sequences, max_plot_len)

  print("-----------------------\nseq2name:")
  second_seq = full_seq2name(input_seq, data, max_input_len, smooth_count_full, smooth_count_frag)

  # print superposition version of the full results:
  print("----------------------\nseq2name in superposition notation:")
  #second_seq.display_minimalist()
  second_seq.smooth(smooth_count_final).display_minimalist()

  # 2nd order sequence naming: (this is potentially interesting!)
  data.append(second_seq)                  # learn a new sequence, in this case second_seq
  #print("-----------------------\n2nd order seq2name:")
  #seq2 = full_seq2name(second_seq, data, max_input_len, smooth_count_full, smooth_count_frag)
  #second_seq.display()

