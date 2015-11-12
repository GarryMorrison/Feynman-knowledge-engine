#!/usr/bin/env python3

import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *


c = new_context("Moby Thesaurus")

# test data, no point running on full data if you don't know if your code works.
#source = "data/test-moby-syns.txt"

# full data:
source = "data/moby-syns.txt"

with open(source,'r') as f:
  for line in f:
    try:
      words = line.strip().split(',')
      word = ket("word: " + words[0])
      synonyms = [ket("word: " + w) for w in words[1:]]
      r = superposition()
      r.data = synonyms                   # assumes superposition class has a list of kets, ie not the fast-superposition version.
      c.learn("synonym",word,r)
    except:
      continue

#print(c.dump_universe())
sw_dest_file = "sw-examples/improved-moby-thesaurus.sw"
save_sw(c,sw_dest_file)
 
