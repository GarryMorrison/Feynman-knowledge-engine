#!/usr/bin/env python3

#######################################################################
# improved k-classifier.
# This time extract out the bare minimum of the project, so this code is independent of the rest of the Feynman Knowledge Engine.
# Full Feynman Knowledge Engine is here:
# https://github.com/GarryMorrison/Feynman-knowledge-engine
#
# My k-similarity idea is explained here:
# http://write-up.semantic-db.org/194-introducing-network-k-similarity.html
#
# Hrmm... I wonder if standard dictionaries are faster than OrderedDict's? Since unlike the full project, we don't need superposition ordering information.
# Yup. Cut run time in half for Ramsey-graph-1.sw and Ramsey-graph-2.sw for k = 44
# from "real 0m3.743s" to "real 0m1.553s"
# BTW, full project version:
# $ time ./fast_k_classifier.py 44 sw-examples/Ramsey-graph-*.sw
# took "real 0m12.010s"
#
# I now have two versions of node_to_signature().
# I'm not sure which is faster, or if they are roughly the same.
# and with v_list.reverse() switched off, they give the same signature.
#
# Bah! My algo is broken!!!
# See here:
# http://www.dharwadker.org/tevet/isomorphism/
# the k = 6 network classes:
# ----------------------------
# 28aaf886be21944c0d7218a318347e2348c2683a: network-1-a, network-1-b
# e242ed2c2806c046642ed188fe1522b2bdef1fdd: network-2-a, network-2-b
# a9ffd7aec14150e874edcfef9c148a257b9ce5a0: network-3-a, network-3-b
# c3cdb555ffde8b6ef1503a1e4cfaa3ddbada92d5: network-4-a, network-4-b
# 44204cf40f670496e8604dcf01b5dd7d84aadf6a: network-5-a, network-5-b
# abf9113fea4efd003fcf32b7dae9139a860e896b: network-6-a
# 951749d0e6112d63b97cc19a97a597e426b547ce: network-6-b
# 7843931b988a3a60cf812e8270919ceca8df5c18: network-7-a, network-7-b
# e887570d4ddee153d1eefc01945eb68971f8e81a: network-8-a, network-8-b
# 25797af66d9142a2f8bebe626b3fef4f56e49772: network-9-a, network-9-b
# ----------------------------
# 6,7,8,9 should all be non-iso, yet only 6 reports non-iso.
# Is this fixable?? I suspect not!
#
# OK. With some thought. It still works quite frequently.
# Provided there is a k where adj^k is different then it will work.
# adj being the adjacency matrix for the graph.
#
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-17
# Update: 2016-03-18
# Copyright: GPLv3
#
# Usage: ./improved_k_classifier.py k network-1.sw [network-2.sw network-3.sw ...]
#
#######################################################################


import os
import sys
import copy
import hashlib
from collections import OrderedDict

try:
  k = int(sys.argv[1])
  list_of_files = sys.argv[2:]
except:
  print("\nUsage: ./improved_k_classifier.py k network-1.sw [network-2.sw network-3.sw ...]\n")
  sys.exit(1)


# define our primes:
# from here: https://primes.utm.edu/lists/small/10000.txt
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
primes += [127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229]
primes += [233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349]
primes += [353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463]
primes += [467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601]
primes += [607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733]
primes += [739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863]
primes += [877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013]
primes += [1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151]
primes += [1153,1163,1171,1181,1187,1193,1201,1213,1217,1223,1229,1231,1237,1249,1259,1277,1279,1283,1289,1291]
primes += [1297,1301,1303,1307,1319,1321,1327,1361,1367,1373,1381,1399,1409,1423,1427,1429,1433,1439,1447,1451]
primes += [1453,1459,1471,1481,1483,1487,1489,1493,1499,1511,1523,1531,1543,1549,1553,1559,1567,1571,1579,1583]


# check we have enough primes:
if 2*k + 2 > len(primes):
  print("We need",2*k+2,"primes. We only have",len(primes))
  sys.exit(1)

# define our modulus (a prime):
#m = 32416190071
m = 4257452468389
#m = 4257452468389*32416190071


class superposition(object):
  def __init__(self,in_list=[]):
    self.odict = OrderedDict()
#    self.odict = {}
    for x in in_list:
      if x != '':
        if x in self.odict:
          self.odict[x] += 1
        else:
          self.odict[x] = 1

  def __add__(self,one):
    result = copy.deepcopy(self)
    if type(one) == superposition:
      for label,value in one.odict.items():
        if label != "":                  # treat |> as the identity element
          if label in result.odict:
            result.odict[label] += value
          else:
            result.odict[label] = value
    return result

  def __str__(self):
    sp_list = []
    for label,value in self.odict.items():
      if value == 1:
        element = '|%s>' % label
      else:
        element = '%s|%s>' % (value,label)
      sp_list.append(element)
    if len(sp_list) == 0:
      return '|>'
    return ' + '.join(sp_list)

  def display_as_set(self):
    return '{' + ','.join(label for label in self.odict) + '}'
      
  def count(self):
    return len(self.odict)

  def count_sum(self):
    if len(self.odict) == 0:
      return 0
    sp_sum = sum(value for label,value in self.odict.items() )
    return sp_sum

  def multiply(self,t):
    result = copy.deepcopy(self)
    for label in result.odict:
      result.odict[label] *= t
    return result

  def delete_node(self,node):
    if node in self.odict:            # hack! We shouldn't need to rely on this!
      del self.odict[node]


class new_context(object):
  def __init__(self):
    self.rules = OrderedDict()
#    self.rules = {}

  # we want to learn simple rules like these:
  # op |1> => |2> + |3> + |5> + |9> + |10> + |14> + |16> + |17>
  # op |2> => |1> + |3> + |4> + |6> + |10> + |11> + |15> + |17>
  # op |3> => |1> + |2>
  #
  def load(self,filename):
    with open(filename,'r') as f:
      for line in f:
        if line.startswith('op'):              # hardwire in either: "op |node> => ...", or "|node> => ..."
          line = line[2:]                      # maybe swap in ability to handle other length operators later, if useful.
        line = line.strip()
        if line.startswith('|'):
          try:
            head,tail = line.split(' => ')
            head_node = head[1:-1]
            if head_node == 'context':
              continue
            tail_list = tail[1:-1].split('> + |')
            self.rules[head_node] = superposition(tail_list)
          except Exception as e:
            print("exception reason:",e)
            continue

  def print(self):
    for node,tail in self.rules.items():
      print('op |%s> => %s' % (node,str(tail)))

  # node is a string, value is an integer
  def recall_node(self,node,value=1):
    if node in self.rules:
      if value == 1:
        return self.rules[node]                      # no point doing multiplication if we don't need it.
      else:
        return self.rules[node].multiply(value)
    return superposition()

  # returns a list of known nodes:
  def nodes(self):
    return [node for node in self.rules]

  # removes an edge from the graph:
  def delete_edge(self,node1,node2):
    self.rules[node1].delete_node(node2)
    self.rules[node2].delete_node(node1)


#context = new_context()
#context.load(list_of_files[0])
#k = 0
#max_k = 5
#for node in context.nodes():
#  print("{%s}, " % node,end='')
#  rule = context.recall_node(node)
#  print(rule.display_as_set(),end='')
#  for node in rule.odict:
#...    
    
#sys.exit(0)
# print data as sets:
#context = new_context()
#context.load(list_of_files[0])
#context.print()
#for node in context.nodes():
#  rule = context.recall_node(node)
#  print("%s: %s: %s" % (node,rule.count(),rule.display_as_set()))
#sys.exit(0)

# test our edge remove code works:
# context = new_context()
# context.load("sw-examples/network-1.sw")
# context.print()
# context.delete_edge("A","B")
# context.delete_edge("A","C")
# context.delete_edge("A","G")
# print()
# context.print()
# sys.exit(0)

# define our node to signature function:
# context is a context, node is a string, k is a positive integer, m is the modulus
#
def node_to_signature_v1(context,node,k,m):
  signature = 1
  r = superposition([node])
  for n in range(0,2*k+2,2):
    v1 = r.count()                      # these are the simplest mapping of superposition to an integer.
    v2 = r.count_sum()                  # there are probably other better ones. Perhaps, coeff-sort, then 2^c1 * 3^c2 * 5^c3 * 7^c4 ...
    signature = ((signature % m) * pow(primes[n],v1,m) ) % m
    signature = ((signature % m) * pow(primes[n+1],v2,m) ) % m
#    print("n:",n)
#    print("r:",r)
#    print("v1:",v1)
#    print("v2:",v2)
#    print("signature:",signature)
    r1 = superposition()
    for node,value in r.odict.items():
      r1 += context.recall_node(node,value)
    r = r1
  return signature


# define our node to signature function:
# context is a context, node is a string, k is a positive integer, m is the modulus
#
def node_to_signature_v2(context,node,k,m):
  signature = 1
  r = superposition([node])
  v_list = []
  for n in range(0,k+1):
    v1 = r.count()
    v2 = r.count_sum()
    v_list.append(v1)
    v_list.append(v2)

#    print("n:",n)
#    print("r:",r)
#    print("v1:",v1)
#    print("v2:",v2)
    r1 = superposition()
    for node,value in r.odict.items():
      r1 += context.recall_node(node,value)
    r = r1

#  print("v_list:",v_list)
#  v_list.sort(reverse=True)        # we reverse sort the list, so largest v's are applied to smallest primes. This is quite a big saving.
#  v_list.reverse()                  # just reverse the list. Yeah, slightly bigger integers than reverse-sort, but reduces the chance of an accidental collision.
#  print("v_list:",v_list)           # since we are now using modulus arithmetic, v_list.reverse() doesn't gain us anything.
  for i,v in enumerate(v_list):      # it is now better to leave it out, so method 1 and 2 give the same signature.
    signature = ((signature % m) * pow(primes[i],v,m) ) % m
#  print("signature:",signature)
  return signature


# define our node to signature function:
# context is a context, node is a string, k is a positive integer, m is the modulus
#
def node_to_signature_v3(context,node,k,m):
  signature = 1
  i = 0
  r = superposition([node])
  for n in range(0,2*k+2,2):
    v1 = r.count()
    signature = ((signature % m) * pow(primes[i],v1,m) ) % m
    i += 1
    for c in sorted(r.odict.values()):
      signature = ((signature % m) * pow(primes[i],c,m) ) % m
      i += 1
#    print("n:",n)
#    print("r:",r)
#    print("v1:",v1)
#    print("v2:",v2)
#    print("signature:",signature)
    r1 = superposition()
    for node,value in r.odict.items():
      r1 += context.recall_node(node,value)
    r = r1
  return signature


# define our node to signature function:
# context is a context, node is a string, k is a positive integer, m is the modulus
#
def node_to_signature_v4(context,node,k,m):
  signature = 1
  r = superposition([node])
  for n in range(0,2*k+2,2):
    v1 = r.count()
    signature = ((signature % m) * pow(primes[n],v1,m) ) % m
    i = 0
    v2 = 1
    for c in sorted(r.odict.values()):
      v2 = ((v2 % m) * pow(primes[i],c,m) ) % m
      i += 1
    signature = ((signature % m) * pow(primes[n+1],v2,m) ) % m
#    print("n:",n)
#    print("r:",r)
#    print("v1:",v1)
#    print("v2:",v2)
#    print("signature:",signature)
    r1 = superposition()
    for node,value in r.odict.items():
      r1 += context.recall_node(node,value)
    r = r1
  return signature


# define our node to signature function:
# context is a context, node is a string, k is a positive integer, m is the modulus
#
# Nope! This doesn't solve our hard examples either!
# this code proves it:
#  load network-7-a--as-result-sw.sw
#  clean-op-0 |*> #=> push-float coeff-sort op-0 |_self>
#  clean-op-1 |*> #=> push-float coeff-sort op-1 |_self>
#  clean-op-2 |*> #=> push-float coeff-sort op-2 |_self>
#  clean-op-3 |*> #=> push-float coeff-sort op-3 |_self>
#  table[node,clean-op-0,clean-op-1,clean-op-2,clean-op-3] rel-kets[op-0]
#
#
def node_to_signature_v5(context,node,k,m):
  self_context = copy.deepcopy(context)                       # maybe optimize this later
  signature = 1
  i = 0
  r = superposition([node])
  for n in range(0,2*k+2,2):
#    v1 = r.count()      
#    v2 = r.count_sum()
#    signature = ((signature % m) * pow(primes[n],v1,m) ) % m
#    signature = ((signature % m) * pow(primes[n+1],v2,m) ) % m

    v1 = r.count()
    signature = ((signature % m) * pow(primes[i],v1,m) ) % m
    i += 1
    for c in sorted(r.odict.values()):
      signature = ((signature % m) * pow(primes[i],c,m) ) % m
      i += 1

    print("n:",n)
    print("r:",r)
    print("op-%s |%s> => %s" % (str(int(n/2)),node,str(r)))
#    print("v1:",v1)
#    print("v2:",v2)
#    print("signature:",signature)
    r1 = superposition()
    for node1,value in r.odict.items():
      r1 += self_context.recall_node(node1,value)
    for node1 in r.odict:
      for node2 in r1.odict:
        print("delete edge: %s %s" % (node1,node2))
        self_context.delete_edge(node1,node2)
    r = r1
#  if len(r) == 0:
#     return signature
  return signature



# filename is a string, k is a positive integer
#
def file_to_hash(filename,k,m):
  context = new_context()
  context.load(filename)

  signature = 1

  # walk the network:
  # NB: multiplication is Abelian, so the order we examine nodes does not matter.
  for node in context.nodes():
#  for node in context.rules:       # don't know if this is faster or not.
    signature = ((signature % m) * node_to_signature_v4(context,node,k,m) ) % m
#  print("sig:",signature)
  return hashlib.sha1(str(signature).encode('utf-8')).hexdigest()


network_classes = OrderedDict()
for name in list_of_files:
  base = os.path.basename(name)
  base, ext = base.rsplit('.',1)
  file_hash = file_to_hash(name,k,m)
  if file_hash in network_classes:
    network_classes[file_hash].append(base)
  else:
    network_classes[file_hash] = [base]

print("\nthe k = %s network classes:\n----------------------------" % str(k))
for hash in network_classes:
  the_class = network_classes[hash]
#  print(", ".join(the_class))
  print(hash + ": " + ", ".join(the_class))
print("----------------------------\n")

#sys.exit(0)
print("2nd-order-k%s-network:" % str(k))
for i,hash in enumerate(network_classes):
  the_class = network_classes[hash]
  the_class_sp = '|' + '> + |'.join(the_class) + '>'
  print('class |%s> => ' % str(i+1) + the_class_sp)

print()
for i,hash in enumerate(network_classes):
  print('hash |%s> => |%s>' % (str(i+1),hash))

