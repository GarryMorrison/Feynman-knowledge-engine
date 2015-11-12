#!/usr/bin/env python3

#######################################################################
# split webpages into fragments, then hash the fragments
# ie, webpage => superposition
#
# Author: Garry Morrison
# Date: 2015-02-23
# Copyright: GPLv3
#
# Usage:
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

import hashlib


C = context_list("fragment webpages")

# NB: webpages by default often have chars that python complains about. 
# So I strip pages down to clean ascii. 
# Yes! I need to learn how to use unicode!
# This is the script:
#
# $ cat clean-webpages.sh
# #!/bin/sh
# 
# for f in $(ls -1 *.html); do
# echo "f: $f"
# tr -cd '[:print:]\t\n' < "$f" > "clean-$f"
# done

# I think we need a better name!
def fragment_string(s,fragment_strings):
  r = [s]
  for frag in fragment_strings:
    list = r
    r = []
    for s in list:
      r += s.split(frag)
  return [s.strip() for s in r if len(s.strip()) > 0 ]

file_directory = "webpages-v2/"

fragment_strings = ["<",">"]

def create_fragment_hashes(filename,fragment_strings,size):
  result = fast_superposition()
  with open(filename,'r') as f:
    text = f.read()
    for fragment in fragment_string(text,fragment_strings):
      hash = hashlib.sha1(fragment.encode('utf-8')).hexdigest()[-size:]
      result += ket(hash)
  return result.superposition().coeff_sort()

def list_create_fragment_hashes(filename,fragment_strings,size):
  array = [0] * (16**size)
  with open(filename,'r') as f:
    text = f.read()
    for fragment in fragment_string(text,fragment_strings):
      hash = hashlib.sha1(fragment.encode('utf-8')).hexdigest()[-size:]
      x = int(hash,16)
      array[x] += 1      
  return array


# do some testing:
#file = "webpages-v2/clean-abc-1.html"
#print(create_fragment_hashes(file,fragment_strings,8))
#print(list_create_fragment_hashes(file,fragment_strings,4))


size_table = {
  4 : "64k",
  5 : "1M",
  8 : "4B",
}

size_list = [[4,"64k"],[5,"1M"],[8,"4B"]]

def learn_webpage_hashes(C,webpage,n):
  for k in range(n):
    web_file = "webpages-v2/clean-" + webpage + "-" + str(k+1) + ".html"
    print("web_file:",web_file)
    for pair in size_list:
      size, string_size = pair
      print("size:",size)
      print("string size:",string_size)
#      ket_name = webpage + "-" + str(k+1) + "-" + string_size
      ket_name = webpage + " " + str(k+1)
      print("ket_name:",ket_name)
      hash_name = "hash-" + string_size

# now lets learn the superpositions:
      r = create_fragment_hashes(web_file,fragment_strings,size)
      C.learn(hash_name,ket_name,r)

# learn the drop-n hashes:
# an experiment really, trying to work out what is best.
# Probably r by itself, but we need to check.
      C.learn("drop-2-" + hash_name,ket_name,r.drop_below(2))
      C.learn("drop-3-" + hash_name,ket_name,r.drop_below(3))
      C.learn("drop-4-" + hash_name,ket_name,r.drop_below(4))
      C.learn("drop-5-" + hash_name,ket_name,r.drop_below(5))
      C.learn("drop-6-" + hash_name,ket_name,r.drop_below(6))
      C.learn("drop-7-" + hash_name,ket_name,r.drop_below(7))
      C.learn("drop-8-" + hash_name,ket_name,r.drop_below(8))
      C.learn("drop-9-" + hash_name,ket_name,r.drop_below(9))
      C.learn("drop-10-" + hash_name,ket_name,r.drop_below(10))

# learn how many of each:
      C.learn("count-1-" + hash_name,ket_name,r.number_count())
      C.learn("count-2-" + hash_name,ket_name,r.drop_below(2).number_count())
      C.learn("count-3-" + hash_name,ket_name,r.drop_below(3).number_count())
      C.learn("count-4-" + hash_name,ket_name,r.drop_below(4).number_count())
      C.learn("count-5-" + hash_name,ket_name,r.drop_below(5).number_count())
      C.learn("count-6-" + hash_name,ket_name,r.drop_below(6).number_count())
      C.learn("count-7-" + hash_name,ket_name,r.drop_below(7).number_count())
      C.learn("count-8-" + hash_name,ket_name,r.drop_below(8).number_count())
      C.learn("count-9-" + hash_name,ket_name,r.drop_below(9).number_count())
      C.learn("count-10-" + hash_name,ket_name,r.drop_below(10).number_count())


# test it works.
# yup!
#learn_webpage_hashes(C,"slashdot",3)
#print(C.dump_universe())  

# learn them all!
sites = ["abc","adelaidenow","slashdot","smh","wikipedia","youtube"]
number = 11

for site in sites:
  learn_webpage_hashes(C,site,number)


#sys.exit(0)
name = "sw-examples/improved-fragment-webpages.sw"
save_sw(C,name)
