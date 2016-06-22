#!/usr/bin/env python3

#######################################################################
# show wikivec similarity
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-06-22
# Update:
# Copyright: GPLv3
#
# Usage: ./wikivec-similarity.py wikipage-title [number-of-results-to-show]
#
# data source:
#
#######################################################################


import sys
import hashlib
import zlib

if len(sys.argv) < 2:
  print("\nUsage: ./wikivec-similarity.py wikipage-title [number-of-results-to-show]\n")
  sys.exit(1)

if len(sys.argv) >= 2:
  wikipage = "WP: " + sys.argv[1]              # maybe wikivec should leave out the "WP: " prefix? Done.
  wikipage = sys.argv[1]

number_of_results = 30
if len(sys.argv) == 3:
  number_of_results = int(sys.argv[2])


# maybe op and destination should be passed in at the command line?
#op = "friends"
#op = "inverse-hash-links-to"
#destination = "sw-examples/fred-sam-friends-inverse-hash.sw"
#source = "sw-examples/30k--wikipedia-links--inverse-hash.sw"

op = "wikivec"
source = "sw-examples/30k--wikivec.sw"


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


# load a simple sw file, ie they are all literal superpositions, into a dictionary.
# the parsing is a hack though, hence the need for well formed literal superpositions!
# 
def load_simple_sw_into_dict(filename,op):
  op_head = op + " |"
  sw_dict = {}
  with open(filename,'r') as f:
    for line in f:
      line = line.strip()
      if line.startswith(op_head):
#        print("line:",line)
        try:
          head,tail = line.split('> => ',1)
          label = head.split(' |',1)[1]
          sw_dict[label] = superposition()
#          print("head:",head)
#          print("tail:",tail)
#          print("label:",label)
          for piece in tail[:-1].split('> + '):
            tidy_piece = piece.split('|')[1]
#            if tidy_piece == "WP: =":                    # hack to fix a bug in the wikipedia links sw file: a term: |WP: =>
#              continue
            sw_dict[label].add(tidy_piece)
#          print("sp:",sw_dict[label])
        except Exception as e:
          print("Exception reason: %s" % e)
          continue
  return sw_dict        

sw_dict = load_simple_sw_into_dict(source,op)
print("----------------")

def print_sw_dict(dict):
  for label,sp in dict.items():
    print("|%s> => %s" % (label,sp))

def save_sw_dict(dict,filename,op):
  with open(filename,'w') as f:
    for label,sp in dict.items():
      f.write("%s |%s> => %s\n" % (op,label,sp))

#print_sw_dict(sw_dict)

# probably can optimize this more yet.
def fast_simm(A,B):
#  logger.debug("inside fast_simm")
  if len(A) <= 1 and len(B) <= 1:
    a = A.ket()                               # x.ket() broken for now.
    b = B.ket()
    if a.label != b.label:                    # put a.label == '' test in here too?
      return 0
    a = max(a.value,0)                        # just making sure they are >= 0.
    b = max(b.value,0)
    if a == 0 and b == 0:                     # prevent div by zero.
      return 0
    return min(a,b)/max(a,b)
#  return intersection(A.normalize(),B.normalize()).count_sum()

  # now calculate the superposition version of simm, while trying to be as fast as possible:
#  logger.debug("made it here in fast_simm")
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

# probably can optimize this more yet.
def faster_simm(A,B):
#  logger.debug("inside fast_simm")
  if len(A) <= 1 and len(B) <= 1:
    a = A.ket()                               # x.ket() broken for now.
    b = B.ket()
    if a.label != b.label:                    # put a.label == '' test in here too?
      return 0
    a = max(a.value,0)                        # just making sure they are >= 0.
    b = max(b.value,0)
    if a == 0 and b == 0:                     # prevent div by zero.
      return 0
    return min(a,b)/max(a,b)
#  return intersection(A.normalize(),B.normalize()).count_sum()

  # now calculate the superposition version of simm, while trying to be as fast as possible:
#  logger.debug("made it here in fast_simm")
  try:
    one_sum = len(A)                       # we can only do this since we are working with clean superpositions
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


def pattern_recognition(dict,pattern,t=0):
  result = []
  for label,sp in dict.items():
    value = fast_simm(pattern,sp)
    if value > t:
      result.append((label,value))
  return result

# pretty print the result:
def float_to_int(x,t=2):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

def massaged_pattern_recognition(dict,pattern,t=0):
  result = []
  for label,sp in dict.items():
    value = faster_simm(pattern,sp)
    if value > t:
      result.append((label,float_to_int(100*value)))     # float to int returns a string, which messes with sorting, so be aware!!
  return result


pattern = sw_dict[wikipage]
print("wikipage:",wikipage)
print("pattern:",pattern)
#result = pattern_recognition(sw_dict,pattern)
result = massaged_pattern_recognition(sw_dict,pattern)
#print("result:",result)

# sort the results:
sorted_result = sorted(result, key = lambda x: float(x[1]), reverse = True)[:number_of_results]
#sorted_result = sorted(result, key = lambda x: x[1], reverse = True)

# print the results:
#for label,value in sorted_result:
#  print("%s\t\t\t\t%s" % (label,value))


# table print, from here: http://stackoverflow.com/questions/25403249/print-a-list-of-tuples-as-table
max_length_column = []
tuple_len = 2

print("len results:",len(sorted_result))
#sys.exit(0)
for i in range(tuple_len):
    max_length_column.append(max(len(e[i])+2 for e in sorted_result))    

#sys.exit(0)
for e in sorted_result:
    for i in range(tuple_len):
        print(e[i].ljust(max_length_column[i]), end='')
    print()

sys.exit(0)

def find_inverse_of_sw_dict(dict):
  inverse_dict = {}
  for label,sp in dict.items():
    for key,value in sp:
      if key not in inverse_dict:
        inverse_dict[key] = superposition()  
      inverse_dict[key].add(label)
  return inverse_dict

print("----")
#inverse_dict = find_inverse_of_sw_dict(sw_dict)
#print_sw_dict(inverse_dict)

def our_hash(s):
  size = 6                                                     # length of the final hash
  return hashlib.md5(s.encode('utf-8')).hexdigest()[-size:]    # seems no speed difference between md5 and adler32. 
#  return "%0.2X" % zlib.adler32(s.encode('utf-8'))

def find_inverse_hash_of_sw_dict(dict):
  inverse_dict = {}
  for label,sp in dict.items():
    for key,value in sp:
      if key not in inverse_dict:
        inverse_dict[key] = superposition()
      inverse_dict[key].add(our_hash(label))
  return inverse_dict

inverse_dict = find_inverse_hash_of_sw_dict(sw_dict)
print_sw_dict(inverse_dict)
#save_sw_dict(inverse_dict,destination,"inverse-hash-" + op)
save_sw_dict(inverse_dict,destination,"wikivec")
