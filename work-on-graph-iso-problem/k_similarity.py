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
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-12
# Update:
# Copyright: GPLv3
#
# Usage: ./k_similarity.py network.sw k
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("find k similarity")


try:
  filename = sys.argv[1]
  k = int(sys.argv[2])
except:
  print("\nUsage: ./k_similarity.py network.sw k\n")
  sys.exit(1)

# define our primes:
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71]

# check we have enough primes:
if 2*k +2 > len(primes):
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
  for n in range(0,2*k+2,2):
    print("n:",n)
    print("r:",r)
    v1 = int(r.count())
    v2 = int(r.count_sum())
    print("v1:",v1)
    print("v2:",v2)
    signature *= primes[n]**v1
    signature *= primes[n+1]**v2
    print("signature:",signature)  
    r = r.apply_op(context,op)
  return signature

print()
signature = 1

# walk the network:
for x in context.relevant_kets(op):
  signature *= node_to_signature(x,op,k)

print("final %s signature: %s" % (str(k),signature))

