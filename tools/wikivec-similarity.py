#!/usr/bin/env python3

#######################################################################
# show wikivec similarity
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-06-22
# Update: 2016-6-23
# Copyright: GPLv3
#
# Usage: ./wikivec-similarity.py wikipage-title [number-of-results-to-show]
#
# data source: http://semantic-db.org/sw-examples/30k--wikivec.sw
#
# Note: command line is old tech. An interactive html version would be a little more fun.
# Though it would need to be at least 30 times faster, so finishes in 1 sec, instead of 30+ sec.
# Worst case speed I have seen is with "France" at about 5 minutes.
#
# TODO: I wonder if I could implement a fast version of guess-ket?
# Done. Though takes maybe 1 1/2 minutes to run. I haven't timed it exactly.
# Standard edit-distance spell-check algo would be faster, but this code is all about superposition similarity.
# We have string similarity with the guess-ket code, 
# and semantic similarity with the wikivec similarity.
#
#######################################################################


import sys
import hashlib
import zlib

if len(sys.argv) < 2:
  print("\nUsage: ./wikivec-similarity.py wikipage-title [number-of-results-to-show]\n")
  sys.exit(1)

if len(sys.argv) >= 2:
#  wikipage = "WP: " + sys.argv[1]              # maybe wikivec should leave out the "WP: " prefix? Done.
  wikipage = sys.argv[1]

number_of_results = 30
if len(sys.argv) == 3:
  number_of_results = int(sys.argv[2])

#op = "wikivec"
#op = "context"
op = "position"

#source = "sw-examples/30k--wikivec.sw"
#source = "sw-examples/300k--wikivec.sw"
#source = "sw-examples/word-context--procrasti.sw"
#source = "sw-examples/word-context--rusty.sw"
#source = "sw-examples/word-positions--sherlock.sw"
source = "sw-examples/word-positions--rusty.sw"


interactive = True
#interactive = False
#use_guess_ket = True
use_guess_ket = False

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
    for key,value in self.dict.items():
      return key, value


# load a clean sw file, ie they are all clean literal superpositions, into a dictionary.
# the parsing is a hack though, hence the need for well formed clean literal superpositions!
# where 'clean' means all coeffs are 1.
# 
def load_clean_sw_into_dict(filename,op):
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
            tidy_piece = piece.split('|')[1]
            sw_dict[label].add(tidy_piece)
        except Exception as e:
          print("Exception reason: %s" % e)
          continue
  return sw_dict        

# load literal superpositions into a dictionary
# Unlike the above, this one is slightly more general, and handles coeffs other than 1
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


def process_string(s):
  def create_letter_n_grams(s,N):
    for i in range(len(s)-N+1):
      yield s[i:i+N]
  r = superposition()
  for k in [1,2,3]:               # hard-wire in the letter ngram sizes
    for w in create_letter_n_grams(s.lower(),k):      # inline the create_letter_ngrams fn?
      r.add(w)
  return r

def load_sw_dict_into_guess_dict(sw_dict):
  dict = {}
  for key in sw_dict:
    dict[key] = process_string(key)
  return dict      

def print_sw_dict(dict):
  for label,sp in dict.items():
    print("|%s> => %s" % (label,sp))

def save_sw_dict(dict,filename,op):
  with open(filename,'w') as f:
    for label,sp in dict.items():
      f.write("%s |%s> => %s\n" % (op,label,sp))

# probably can optimize this more yet. 
# Yup! See faster_simm(). Though it assumes clean superpositions.
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

# seems maybe 50% faster if I recall.
# maybe I should test that number?
def faster_simm(A,B):
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
#  return intersection(A.normalize(),B.normalize()).count_sum()   # very slow version!

  # now calculate the superposition version of simm, while trying to be as fast as possible:
  try:
    one_sum = len(A)                       # we can only do this since we are working with clean superpositions, otherwise need to use fast_simm()
    two_sum = len(B)                       # ie, all coeffs = 1, hence A.count_sum() == A.count() == len(A)
    merged_sum = 0                         # makes the normalization step much cheaper.

    # prevent div by zero:
    if one_sum == 0 or two_sum == 0:
      return 0

    for label,v1 in A:
      if label in B.dict:                   # yeah, breaking the class abstraction again!
        v2 = B.dict[label]
        merged_sum += min(v1/one_sum,v2/two_sum)
    return merged_sum
  except Exception as e:
    print("faster_simm exception reason: %s" % e)

# pretty print a float:
def float_to_int(x,t=2):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

# standard superposition version:
def pattern_recognition(dict,pattern,t=0):
  result = []
  for label,sp in dict.items():
    value = fast_simm(pattern,sp)       # if a clean superposition, then swap in faster_simm()
    if value > t:
      result.append((label,value))
  return result

# clean superposition version:
def faster_pattern_recognition(dict,pattern,t=0):
  result = []
  for label,sp in dict.items():
    value = faster_simm(pattern,sp)
    if value > t:
      result.append((label,value))
  return result

# find the key in the dictionary that is closest to s:
# would standard spell-check edit-distance be faster? Probably!
def guess_ket(guess_dict,s):
  pattern = process_string(s)
  result = ''
  best_simm = 0
  for label,sp in guess_dict.items():
    similarity = fast_simm(pattern,sp)       # can't use faster_simm, since some coeffs are not equal 1
    if similarity > best_simm:
      result = label
      best_simm = similarity
  return result

def find_wikivec_similarity(sw_dict,guess_dict,wikipage,number_of_results):
  # test wikipage is in sw_dict:
  if wikipage not in sw_dict:
    if use_guess_ket:                       # we need to be able to switch it off, since it is slow!
      wikipage = guess_ket(guess_dict,wikipage)
    else:
      print("%s not in dictionary" % wikipage)
      return [()]

  # convert wikipage to wikivec pattern:
  print("----------------")
  pattern = sw_dict[wikipage]            # currently bugs out if wikipage is not in the dictionary.
  print("wikipage:",wikipage)
  print("pattern:",pattern)
  print("pattern length:",len(pattern))
  print("----------------")

  # find matching patterns:
#  result = faster_pattern_recognition(sw_dict,pattern)     # maybe add switch to swap between faster and slower versions?
  result = pattern_recognition(sw_dict,pattern)

  # sort the results:
  sorted_result = sorted(result, key = lambda x: float(x[1]), reverse = True)[:number_of_results]

  # format the results a little:
  return [(str(k+1),label.replace('&colon;',':'),float_to_int(100*value)) for k,(label,value) in enumerate(sorted_result) ]

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

# invoke it:
sw_dict = load_simple_sw_into_dict(source,op)
guess_dict = {}
if use_guess_ket:                    # this is slow, so only want to use it when we want to.
  guess_dict = load_sw_dict_into_guess_dict(sw_dict)

# test the guess_dict:
#print_sw_dict(guess_dict)
#print(guess_ket(guess_dict,"adelaide university"))
#sys.exit(0)

result = find_wikivec_similarity(sw_dict,guess_dict,wikipage,number_of_results)
print_table(result)
print()

# interactive wiki similarity:
if interactive:
  while True:
    line = input("Enter table row number, or wikipage: ")
    line = line.strip()
    if len(line) == 0:
      continue

  # exit the agent:
    if line in ['q','quit','exit']:
      break

    try:
      line = int(line)
      wikipage = result[line-1][1]
    except:
      wikipage = line

    result = find_wikivec_similarity(sw_dict,guess_dict,wikipage,number_of_results)
    print_table(result)
    print()
  
