#!c:/Python34/python.exe

#######################################################################
# Given a sw file that represents an undirected network, all with the same operator, generate a signature integer
# if it works as hoped, then non-isomorphic networks should have a k where the integer differs
# if two networks have the same signature, then they may or may not be graph isomorphic.
# either: 
# 1) they are isomorphic 
# 2a) they are not isomorphic, but k is not large enough 
# 2b) they are not isomorphic but our algo has a coincidence
# potentially our algo doesn't work and is always of type (2b) except for very obvious cases!
# ok. Seems to work! Though the signature integers are very large. But the code is fast, at least for the 8 node networks I have been testing it with.
# NB: what is the big-O for this code? Doesn't look too bad!
# Details here:
# http://write-up.semantic-db.org/194-introducing-network-k-similarity.html
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-12
# Update:
# Copyright: GPLv3
#
# Usage: ./k_similarity_v2.py network.sw k
#
#######################################################################


import sys
import math
import hashlib

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("find k similarity")


try:
  filename = sys.argv[1]
  k = int(sys.argv[2])
except:
  print("\nUsage: ./k_similarity_v2.py network.sw k\n")
  sys.exit(1)

# define our primes:
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]

# check we have enough primes:
if 2*k + 2 > len(primes):
  print("We need",2*k+2,"primes. We only have",len(primes))
  sys.exit(1)

# hardwire in the operator label:
op = "op"

# load the network.sw file:
context.load(filename)

# define our node to signature function:
# node is a ket, op is a string, k is a positive integer
#
def node_to_signature(node,op,k):
  signature = 1
  r = node
  v_list = []
  for n in range(0,k+1):
    v1 = int(r.count())
    v2 = int(r.count_sum())
    v_list.append(v1)
    v_list.append(v2)

    print("n:",n)
    print("r:",r)
    print("v1:",v1)
    print("v2:",v2)
    r = r.apply_op(context,op)

  print("v_list:",v_list)
#  v_list.sort(reverse=True)        # we reverse sort the list, so largest v's are applied to smallest primes. This is quite a big saving.
  v_list.reverse()                  # just reverse the list. Yeah, slightly bigger integers than reverse-sort, but reduces the chance of an accidental collision.
  print("v_list:",v_list)
  for i,v in enumerate(v_list):
    signature *= primes[i]**v
  print("signature:",signature)
  return signature

print()
signature = 1

# walk the network:
# NB: multiplication is Abelian, so the order we examine nodes does not matter.
for x in context.relevant_kets(op):
  signature *= node_to_signature(x,op,k)

print("final %s signature: %s" % (str(k),signature))
print("signature log 10:",math.log10(signature))
print("final %s hash signature: %s" % (str(k),hashlib.sha1(str(signature).encode('utf-8')).hexdigest()))

