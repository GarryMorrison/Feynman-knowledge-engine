#!/usr/bin/env python3

#######################################################################
# try to implement very simple sequence interesection
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-11-24
# Update: 2016-11-27
# Copyright: GPLv3
#
# Usage: ./sequence-intersection.py
#
#######################################################################


import sys
from collections import OrderedDict
from itertools import combinations

sentence1 = "the dog wants the ball".split()
sentence2 = "the dog chased the ball".split()
sentence7 = "the dog wants food".split()
sentence8 = "the hungry dog wants food".split()

sentence3 = "the old man also used a telescope".split()
sentence4 = "the {} man {} used a telescope".split()
sentence5 = "the {} {} man used a telescope".split()
sentence6 = "the other man on the hill used a telescope".split()
sentence9 = "the man used a telescope".split()

def simple_sentence_simm(s1,s2):
  if len(s1) != len(s2):                         # for now, if different lengths, then simple-sequence-simm == 0
    return 0
  if len(s1) == 0:                               # prevent div by 0
    return 0  
  the_sum = sum(1 for k in range(len(s1)) if s1[k] == s2[k] )
  return 100*the_sum/len(s1)
  
print(simple_sentence_simm(sentence1, sentence2))
print(simple_sentence_simm(sentence3, sentence4))
print(simple_sentence_simm(sentence3, sentence5))
#sys.exit(0)

# if s1 and s2 are different lengths, need to align them
def align_sentences(s1, s2):
  print("s1:",s1)
  print("s2:",s2)
  if len(s1) == len(s2):                         # if same length, then for now, do nothing. 
    return s1, s2                                # though there exist sequences that need alignment even if the same length. Bah!
  if len(s2) > len(s1):
    s1, s2 = s2, s1
  len_difference = len(s1) - len(s2)
  max_score = 0
  max_sentence = []
  for indecies in combinations(range(len(s1)), len_difference):
    s = s2[:]
    for x in indecies:
      s.insert(x, '{}')
    score = simple_sentence_simm(s1,s)
    print("s:",s)
    print("score:", score)
    if score > max_score:
      max_score = score
      max_sentence = s

  return s1, max_sentence


def first_process_sentence_pair(s1,s2):
  class_dict = OrderedDict()
  prefix = "a"
  sentence_name = "B"
  if len(s1) != len(s2):
    s1,s2 = align_sentences(s1,s2)
  classes = []
  for k in range(len(s1)):
    x = set()
    x.add(s1[k])
    x.add(s2[k])
    class_value = ", ".join(sorted(x))
    if class_value not in class_dict:
      class_name = "%s%s" % (prefix, k)
      class_dict[class_value] = class_name
      print("%s = {%s}" % (class_name, class_value))
    else:
      class_name = class_dict[class_value]
    classes.append(class_name)
  print("%s = %s" % (sentence_name, ".".join(classes)))

def process_sentence_pair(s1,s2):
  class_dict = OrderedDict()
  prefix = "a"
  sentence_name = "B"
  if len(s1) != len(s2):
    s1,s2 = align_sentences(s1,s2)
  classes = []
#  for k in range(len(s1)):
  k = 0
  while k < len(s1):
    if s1[k] == s2[k]:
      class_value = s1[k]
    elif s1[k] == '{}' or s2[k] == '{}':
      buffer1 = []
      buffer2 = []
#      i = k
      while s1[k] == '{}' or s2[k] == '{}':
        buffer1.append(s1[k])
        buffer2.append(s2[k])
        k += 1
      k -= 1
      x = [".".join(buffer1), ".".join(buffer2)]
      class_value = ", ".join(sorted(x))
    elif s1[k] != s2[k]:
      x = [s1[k], s2[k]]
      class_value = ", ".join(sorted(x))
    if class_value not in class_dict:
      class_name = "%s%s" % (prefix, k)
      class_dict[class_value] = class_name
      print("%s = {%s}" % (class_name, class_value))
    else:
      class_name = class_dict[class_value]
    classes.append(class_name)
    k += 1
  print("%s = %s" % (sentence_name, ".".join(classes)))


process_sentence_pair(sentence1, sentence2)
process_sentence_pair(sentence3, sentence4)
#sys.exit(0)
#align_sentences(sentence1, sentence7)
process_sentence_pair(sentence1, sentence7)
process_sentence_pair(sentence7, sentence8)
process_sentence_pair(sentence3, sentence9)
process_sentence_pair(sentence6, sentence9)
