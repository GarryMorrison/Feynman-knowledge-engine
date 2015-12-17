#!/usr/bin/env python3

#######################################################################
# given two files, find their byte, 2-byte and fragment similarity
# for html good split strings are '<' and '>'
# for code ' ' is probably sufficient
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015-05-06
# Update:
# Copyright: GPLv3
#
# Usage: ./simm.py file1 file2 [split-string-1 split-string-2 ...]
#
# examples: http://semantic-db.blogspot.com.au/2015/05/announcing-command-line-file-similarity.html
#
# for details on simm, see here:
# http://write-up.semantic-db.org/70-a-similarity-metric.html
# http://write-up.semantic-db.org/71-a-list-implementation-of-the-simm.html
# 
#
#######################################################################


import sys
import hashlib

if len(sys.argv) < 3:
  print("\nUsage: ./simm.py file1 file2 [split-string-1 split-string-2 ...]\n")
  sys.exit(0)

# some prelims:
file_1 = sys.argv[1]
file_2 = sys.argv[2]
print("file 1:               ",file_1)
print("file 2:               ",file_2,"\n")

fragment_simm = False
if len(sys.argv) > 3:
  split_strings = sys.argv[3:]
  print("split strings:        "," ".join("'" + x + "'" for x in split_strings),"\n")
  fragment_simm = True
  
# our functions:
def file_to_array(filename):
  result = [0] * 256
  with open(filename,'rb') as f:
    for line in f:
      for c in line:
        result[c] += 1
  return result

def file_to_2_array(filename):
  result = [0] * 65536
  a = 0
  with open(filename,'rb') as f:
    for line in f:
      for b in line:
        c = a + b*256
        a = b
        result[c] += 1
  return result

def fragment_string(s,split_strings):
  r = [s]
  for x in split_strings:
    list = r
    r = []
    for s in list:
      r += s.split(x)
  return [s.strip() for s in r if len(s.strip()) > 0 ]

def create_fragment_array(filename,split_strings):
  size = 6
  result = [0] * 16777216
  with open(filename,'r') as f:
    text = f.read()
    for fragment in fragment_string(text,split_strings):
      hash = hashlib.md5(fragment.encode('utf-8')).hexdigest()[-size:]  # can we speed this up?
      c = int(hash,16)
      result[c] += 1
  return result

# for details on simm, see here:
# http://write-up.semantic-db.org/70-a-similarity-metric.html
# http://write-up.semantic-db.org/71-a-list-implementation-of-the-simm.html
#
# unscaled simm:
def list_simm(f,g):
  length = min(len(f),len(g))

  wf = sum(abs(f[k]) for k in range(length))
  wg = sum(abs(g[k]) for k in range(length))
  wfg = sum(abs(f[k] - g[k]) for k in range(length))
  
  if wf == 0 and wg == 0:
    return 0
  else:
    return (wf + wg - wfg)/(2*max(wf,wg))


# scaled simm:
def rescaled_list_simm(f,g):
  the_len = min(len(f),len(g))

# rescale step, first find size:
  s1 = sum(abs(f[k]) for k in range(the_len))
  s2 = sum(abs(g[k]) for k in range(the_len))

# if s1 == 0, or s2 == 0, we can't rescale:
  if s1 == 0 or s2 == 0:
    return 0

# now rescale:
# we just need w*f == w*g, the exact value doesn't matter, so we choose 1.
  f = [f[k]/s1 for k in range(the_len)]
  g = [g[k]/s2 for k in range(the_len)]

# proceed with algo:
# if we did the rescale step correctly we will have:
# wf == wg == 1
#  wf = sum(abs(f[k]) for k in range(the_len))
#  wg = sum(abs(g[k]) for k in range(the_len))
  wfg = sum(abs(f[k] - g[k]) for k in range(the_len))

# we should never have wf or wg == 0 in the rescaled case:
#  if wf == 0 and wg == 0:
#    return 0
#  else:
#    return (wf + wg - wfg)/(2*max(wf,wg))
  return (2 - wfg)/2


# pretty print the result:
def float_to_int(x,t=2):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

# find the results:
r1 = file_to_array(file_1)
r2 = file_to_array(file_2)

r3 = file_to_2_array(file_1)
r4 = file_to_2_array(file_2)

if fragment_simm:
  r5 = create_fragment_array(file_1,split_strings)
  r6 = create_fragment_array(file_2,split_strings)

# print the results:
print("unscaled:")
print("  byte similarity:    ",float_to_int(100*list_simm(r1,r2)),"%")
print("  2 byte similarity:  ",float_to_int(100*list_simm(r3,r4)),"%")
if fragment_simm:
  print("  fragment similarity:",float_to_int(100*list_simm(r5,r6)),"%")

print()
print("scaled:")
print("  byte similarity:    ",float_to_int(100*rescaled_list_simm(r1,r2)),"%")
print("  2 byte similarity:  ",float_to_int(100*rescaled_list_simm(r3,r4)),"%")
if fragment_simm:
  print("  fragment similarity:",float_to_int(100*rescaled_list_simm(r5,r6)),"%")

