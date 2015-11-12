#!/usr/bin/env python3

#######################################################################
# convert wikipedia pages to frequency lists.
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015-03-30
# Update:
# Copyright: GPLv3
#
# Usage: ./play_with_wp_to_freq.py
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("wikipedia word frequencies")

file_table = {
  "Adelaide"         : "text/WP-Adelaide.txt",
  "Australia"        : "text/WP-Australia.txt",
  "rivers"           : "text/WP-rivers-by-length.txt",
  "US presidents"    : "text/WP-US-presidents.txt",
  "physics"          : "text/WP-physics.txt",
  "particle physics" : "text/WP-particle-physics.txt",
  "country list"     : "text/WP-country-list.txt",
}

def create_word_n_grams(s,N):
  return [" ".join(s[i:i+N]) for i in range(len(s)-N+1)]

def create_freq_list(filename,N):
  result = fast_superposition()
  with open(filename,'r') as f:
    text = f.read()
    words = [w for w in re.split('[^a-z0-9_\']',text.lower()) if w]
    for gram in create_word_n_grams(words,N):
      result += ket(gram)
  return result.superposition().coeff_sort()


for topic in file_table:
  print("WP:",topic)
  x = ket("WP: " + topic)
  file = file_table[topic]
  C.learn("name",x,topic)
  C.learn("file",x,"file: " + file)
  C.learn("words-1",x,create_freq_list(file,1))
  C.learn("words-2",x,create_freq_list(file,2))
  C.learn("words-3",x,create_freq_list(file,3))
#  break

#print(C.dump_universe())

#sys.exit(0)
name = "sw-examples/improved-WP-word-frequencies.sw"
save_sw(C,name)


