#!/usr/bin/env python3

#######################################################################
# convert wikipedia-links sw file to wikivec sw file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-06-21
# Update: 2016-6-22
# Copyright: GPLv3
#
# Usage: ./create-wikivec.py 300k--wikipedia-links.sw
#
# data source: http://semantic-db.org/sw-examples/300k--wikipedia-links.sw
#
#######################################################################


import sys
import hashlib
import zlib

# maybe op and destination should be passed in at the command line?
#op = "friends"
op = "links-to"
#destination = "sw-examples/fred-sam-friends-inverse-hash.sw"
#destination = "sw-examples/30k--wikipedia-links--inverse-hash.sw"
destination = "sw-examples/30k--wikivec.sw"


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

  def add(self,str):
    if str in self.dict:
      self.dict[str] += 1
    else:
      self.dict[str] = 1


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
        print("line:",line)
        try:
          head,tail = line.split('> => ',1)
          label = head.split(' |',1)[1]
          sw_dict[label] = superposition()
          print("head:",head)
          print("tail:",tail)
          print("label:",label)
          for piece in tail[:-1].split('> + '):
            tidy_piece = piece.split('|')[1]
            if tidy_piece == "WP: =":                    # hack to fix a bug in the wikipedia links sw file: a term: |WP: =>
              continue
            sw_dict[label].add(tidy_piece)
          print("sp:",sw_dict[label])
        except Exception as e:
          print("Exception reason: %s" % e)
          continue
  return sw_dict        

sw_dict = load_simple_sw_into_dict(sys.argv[1],op)
print("----------------")

def print_sw_dict(dict):
  for label,sp in dict.items():
    print("|%s> => %s" % (label,sp))

def save_sw_dict(dict,filename,op):
  with open(filename,'w') as f:
    for label,sp in dict.items():
      f.write("%s |%s> => %s\n" % (op,label,sp))

print_sw_dict(sw_dict)

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
      key = key[4:]                                            # let's strip the "WP: " prefix here.
      if key not in inverse_dict:
        inverse_dict[key] = superposition()
      inverse_dict[key].add(our_hash(label))
  return inverse_dict

inverse_dict = find_inverse_hash_of_sw_dict(sw_dict)
print_sw_dict(inverse_dict)
#save_sw_dict(inverse_dict,destination,"inverse-hash-" + op)
save_sw_dict(inverse_dict,destination,"wikivec")
