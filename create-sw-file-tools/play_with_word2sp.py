#!/usr/bin/env python3

#######################################################################
# 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-11-19
# Update:
# Copyright: GPLv3
#
# Usage: ./play_with_word2sp.py text-source.txt
#
# Motivated by: 
#  https://code.google.com/p/word2vec/
#
#  though they have vectors with negative values, we need positive.
#  it will be interesting to see if my idea works ....
#
# example: "This is a sentence about Mary and her pet dog" 
#
# next-1 |this> => |is> 
# next-2 |this> => |a> 
# next-3 |this> => |sentence>
# next-2gram |this> => |is a>
# next-3gram |this> => |is a sentence>
#
# pre-1 |is> => |this> 
# next-1 |is> => |a> 
# next-2 |is> => |sentence> 
# next-3 |is> => |about> 
# next-2gram |is> => |a sentence>
# next-3gram |is> => |a sentence about>
# 
# pre-2 |a> => |this>
# pre-1 |a> => |is>
# pre-2gram |a> => |this is>
# next-1 |a> => |sentence>
# next-2 |a> => |about>
# next-3 |a> => |mary>
# next-2gram |a> => |sentence about>
# next-3gram |a> => |sentence about mary>
#
# pre-3 |sentence> => |this>
# pre-2 |sentence> => |is>
# pre-3 |sentence> => |a>
# pre-3gram |sentence> => |this is a>
# pre-2gram |sentence> => |is a>
# next-1 |sentence> => |about>
# next-2 |sentence> => |mary>
# next-3 |sentence> => |and>
# next-2gram |sentence> => |about mary>
# next-3gram |sentence> => |about mary and>
# ...
# 
# sa: word2sp-op |*> #=> apply(|op: pre-3> + |op: pre-2> + |op: pre-3gram> + |op: pre-2gram> + |op: next-1> + |op: next-2> + |op: next-3> + |op: next-2gram> + |op: next-3gram>,|_self>)
# sa: map[word2sp-op,word2sp] list-of |words>
# sa: table[word,coeff] select[1,50] 100 self-similar[word2sp] |some-word>
#
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("word2sp")

# source file:
#filename = "text/WP-Adelaide.txt"
#filename = "text/ebook-Tom_Sawyer_74.txt"
#filename = "text/all.txt"  # used too much RAM. Not sure how much in total it would need. test later.
#filename = "text/ebook-moby-shakespeare.txt"
#filename = "text/ebook-Gone-with-the-wind--0200161.txt"
filename = "text/ebook-Sherlock-Holmes.txt"


def create_word_n_grams(s,N):
  return [" ".join(s[i:i+N]) for i in range(len(s)-N+1)]


def two_gram(one):
  text = one.label if type(one) == ket else one
  if text.startswith('text: '):
    text = text[6:]

  words = [w for w in re.split('[^a-z0-9_\']',text.lower().replace('\\n',' ')) if w]

  result = superposition()
  for w in create_word_n_grams(words,2):
    result += ket(w)
  return result

with open(filename,'r') as f:
  text = f.read()
  words = [w for w in re.split('[^a-z0-9_\']',text.lower().replace('\\n',' ')) if w]


dest = "sw-examples/testing-word2sp.sw"
C.save(dest)

