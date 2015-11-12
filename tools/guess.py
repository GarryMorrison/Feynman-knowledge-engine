#!/usr/bin/env python3

#######################################################################
# given a string, find the closest matching filenames in the given directory
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015-05-30
# Update:
# Copyright: GPLv3
#
# Usage: ./guess.py string [directory]
#
#######################################################################


import sys
import glob
import os

if len(sys.argv) < 2:
  print("\nUsage: ./guess.py string [directory]\n")
  sys.exit(0)

# string to compare with filenames:
string = sys.argv[1]

# directory to search for filenames:
dir = "."
if len(sys.argv) >= 3:
  dir = sys.argv[2].rstrip('/')   # hrmm... windows vs linux file separator issue?

# number of results to return:
# for now, show all results. Maybe instead we can have a simm threshold? 
number = 20000

print("\nstring to match:     ",string)
print("directory to search: ",dir)
#print("number of results to return:",number)
print("====================================\n")


# convert a string to an array we can feed to simm:
def string_to_2_array(s):
  # make case insensitive:
  s = s.lower()
  result = [0] * 65536
  a = 0
  for char in s:
    b = ord(char)
    c = a + b*256
    a = b
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


string_array = string_to_2_array(string)

# place to store our simm results:
result = []

# now find the similarities:
for file in glob.glob(dir + "/*"):
  base = os.path.basename(file)
  file_array = string_to_2_array(base)
  simm = list_simm(string_array,file_array)
#  simm = rescaled_list_simm(string_array,file_array) # 50% slower, and very little difference in result.
  result.append([simm,base])


# sort the results:
#sorted_result = sorted(result, key = lambda x: x[0], reverse = True)[:number]
sorted_result = sorted(result, key = lambda x: x[0], reverse = True)

# print the result:
for simm,base in sorted_result:
  if simm > 0:
    print((float_to_int(100*simm) + " %").ljust(8),base)

