#!/usr/bin/env python3

#######################################################################
# convert wikivec to json format
# just a quick script.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-07-10
# Update:
# Copyright: GPLv3
#
# Usage: ./wikivec-to-json.py sw-examples/30k--wikivec.sw
#
#######################################################################


import sys
import os
import json

source = sys.argv[1]
base = os.path.basename(source)
destination = base.rsplit('.')[0] + ".json"
print("dest:",destination)
#sys.exit(0)

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

  def to_int_list(self):
    r = []
    for key in self.dict:
      try:
        value = int(key,16) % 65536              # I think 16^6 is too large, so shrink it to 16^4.
        r.append(value)
      except:
        continue
    return r


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

def print_sw_dict(dict):
  for label,sp in dict.items():
    print("%s: %s" % (label,sp.to_int_list()))

wikivec_dict = load_simple_sw_into_dict(source,"wikivec")
#print_sw_dict(wikivec_dict)

json_dict = {}
for label,sp in wikivec_dict.items():
  json_dict[label] = sp.to_int_list()

with open(destination,'w') as f:
  json.dump(json_dict, f, sort_keys=True, indent=4)


