#!/usr/bin/env python3

#######################################################################
# Implement my new idea of simm over p patterns, instead of just 2.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-07-28
# Update:
# Copyright: GPLv3
#
# Usage: ./multi-simm.py
#
#######################################################################


import sys
import math
import cmath
import itertools

# define p'th roots of unity:
def jpk(p,k):
  return cmath.exp(1j*2*math.pi*k/p)

print("j31:",jpk(3,0))
print("j32:",jpk(3,1))
print("j33:",jpk(3,2))

def test_identity(vect):
  p = len(vect)
  r1 = sum(x for x in vect)
  r2 = abs(sum(jpk(p,k)*x for k,x in enumerate(vect)))
  r3 = p*max(x for x in vect)
  print("%s : %s : %s" % (r1 + r2, r3, r1 + r2 <= r3))

# r2 = 0
# for k in range(len(vect)):
#   r2 += jpk(p,k)*vect[k]
# return abs(r2)


vect = [6,6,6,6,6]
test_identity(vect)

test_identity([2,3,4,5,6])
test_identity([6,2,3,4,5])
test_identity([6,5,4,3,2])
test_identity([2,4,3,5,6])
test_identity([2,4,5,3,6])

print("-------------------")
vect = [2,3,4,5]
for permutation in itertools.permutations(vect):
  test_identity(permutation)
print("-------------------")

# define wf_k:
def wf(vect):
  return sum(abs(x) for x in vect)

# define wf^p:
def wfp(vects):
  p = len(vects)
  i_max = len(vects[0])          # assume all vects are the same size as the first one.
  r1 = 0
  for i in range(i_max):
    r2 = 0
    for k in range(p):
      r2 += jpk(p,k)*vects[k][i]
    r1 += abs(r2)
  return r1


def multi_simm(vects):
  p = len(vects)
  i_max = len(vects[0])          # assume all vects are the same size as the first one.

  # sum over wf_k term:
  r1 = 0
  max_wf = 0
  for k in range(p):
    wf_k = wf(vects[k])
    max_wf = max(max_wf,wf_k)
    r1 += wf_k
  
  # wf^p term:
  r2 = wfp(vects)

  # p.max term:
  r3 = p*max_wf

  # prevent divide by 0:
  if r3 == 0:
    return 0

  # return result:
  return (r1 - r2)/r3



def rescaled_multi_simm(vects):
  p = len(vects)
  i_max = len(vects[0])          # assume all vects are the same size as the first one.

  # find normalization terms:
  norms = []
  for k in range(p):
    wf_k = wf(vects[k])
    if wf_k == 0:                # prevent divide by zero
      return 0
    norms.append(wf_k)

  # find normalized wf^p:
  r1 = 0
  for i in range(i_max):
    r2 = 0
    for k in range(p):
      r2 += jpk(p,k)*vects[k][i]/norms[k]
    r1 += abs(r2)

  # return result:
  return 1 - r1/p


# our test patterns:
list_of_vects = [[2,3,4,5,6], [6,5,4,3,2], [2,4,3,5,6], [2,4,5,3,6]]
#list_of_vects = [[2,3,4,5,6], [2,3,4,5,6], [2,3,4,5,6]]
#list_of_vects = [[2,3,4,5,6], [4,6,8,10,12], [6,9,12,15,18]]
#list_of_vects = [[5,0,0,0], [0,-5,0,0], [0,0,-5,0], [0,0,0,5]]

print("wfp: %s" % wfp(list_of_vects))
print("multi-simm: %s" % multi_simm(list_of_vects))
print("rescaled-multi-simm: %s" % rescaled_multi_simm(list_of_vects))
