#!c:/Python34/python.exe

#######################################################################
# learning how to use sympy for my ds^7 problem 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-28
# Update:
# Copyright: GPLv3
#
# Usage: ./play_with_sympy.py
#
#######################################################################


import sys
import functools                                    # so reduce() works in python 3.

from sympy import *
init_printing()

from itertools import product

#from the_semantic_db_code import *
#from the_semantic_db_functions import *
#from the_semantic_db_processor import *

#context = context_list("learn sympy basics")

# code to find LCM, from here:
# http://stackoverflow.com/questions/147515/least-common-multiple-for-3-or-more-numbers
#
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(*args):
    """Return lcm of args."""   
    return functools.reduce(lcm, args)               # maybe remove need for reduce() later, since discouraged in python3.

# test LCM:
#integers = {36, -90, -20, 15, -48, 120, -6}
#print("LCM:",lcmm(*integers))
#sys.exit(0)


R_str = """
a g f e d c b
b a g f e d c
c b a g f e d
d c b a g f e
e d c b a g f
f e d c b a g
g f e d c b a
"""

R = zeros(7,7)
#pprint(R)

# learn a matrix:
def learn_matrix(R,R_str):
  i = 0
  j = 0
  for line in R_str.split('\n'):
    line = line.strip()
    if len(line) == 0:
      continue
    for elt in line.split(' '):
      R[i,j] = Symbol(elt)
      j += 1
    i += 1
    j = 0

# learn the R matrix:
learn_matrix(R,R_str)
pprint(R)
#sys.exit(0)
# cool, det(R) works, and gives J7():
#pprint(R.det())

R_det = R.det()
det_table = {}
count = 0
for term in R_det.args:
  coeff,rest = str(term).split('*',1)
  print("coeff:%s rest:%s" % (coeff,rest))
  if not coeff.isalpha():
    det_table[rest] = int(coeff)
  else:
    det_table[str(term)] = 1
  count += 1
print("count:",count)
#print("table:",det_table)
for key,value in det_table.items():
  print("%s: %s" % (key,value))
#sys.exit(0)

# clean the mapping of Q from Qijklmno to Qcount
# I don't think we need this. Yup. Pretty sure we don't!
#Q_table = {}
#count = 1
#for i,j,k,l,m,n,o in product(range(7), range(7), range(7), range(7), range(7), range(7), range(7)):
#  indices = [i,j,k,l,m,n,o]
#  if indices == sorted(indices):
#    Qijklmno = "Q{0}{1}{2}{3}{4}{5}{6}".format(*sorted(indices))
#    Q_table[Qijklmno] = symbols(Qijklmno)
#    count += 1

#print(clean_Q_mapping)
#sys.exit(0)


# yup. This works. Takes about 30 minutes.
count = 1
eqn = 0
#for i,j,k,l,m,n,o in product(range(7), range(7), range(7), range(7), range(7), range(7), range(7)):
for i,j,k,l,m,n,o in product(range(7), repeat=7):
  indices = (i,j,k,l,m,n,o)

  if (i + j + k + l + m + n + o) % 7 != 0:      # if a term has the wrong signature it has coeff 0
    continue

  if len(set(indices)) == 1:                      # ie, a diagonal element
    Q = 1
#  elif (i + j + k + l + m + n + o) % 7 != 0:      # if a term has the wrong signature it has coeff 0
#    Q = 0
  else:
    Qijklmno = "Q{0}{1}{2}{3}{4}{5}{6}".format(*sorted(indices))
    Q = symbols(Qijklmno)

  eqn += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0] * R[n,0] * R[o,0]
#  count += 1
#  if count == 100:
#    break

#sys.exit(0)

#pprint(eqn - R_det)
#print(eqn)

Q_table = {}
count = 0
for term in eqn.args:
  coeff,Q,rest = str(term).split('*',2)
  print("coeff:%s\tQ:%s\trest:%s" % (coeff,Q,rest))
  if not coeff.isalpha():
#    Q_table[Q] = det_table[rest]/int(coeff)
    Q_table[Q] = int(coeff) // det_table[rest]     # preserve integerness, so don't map to imprecise floats
#    Q_table[Q] = int(coeff) / det_table[rest]
  count += 1
print("count:",count)
#sys.exit(0)

integers = set()
for key,value in Q_table.items():
  print("%s: %s" % (key,value))
  integers.add(value)

# LCM of our integers:
LCM = lcmm(*integers)


# Now, let's test we have the right values in Q_table:
# eqn - R_det should be zero.
#
eqn = 0
#for i,j,k,l,m,n,o in product(range(7), range(7), range(7), range(7), range(7), range(7), range(7)):
for i,j,k,l,m,n,o in product(range(7), repeat=7):
  if (i + j + k + l + m + n + o) % 7 != 0:       # if a term has the wrong signature it has coeff 0
    continue

  indices = (i,j,k,l,m,n,o)

  if len(set(indices)) == 1:                      # ie, a diagonal element
    Q = LCM 
  else:
    Qijklmno = "Q{0}{1}{2}{3}{4}{5}{6}".format(*sorted(indices))
    Q = LCM // Q_table[Qijklmno]

  eqn += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0] * R[n,0] * R[o,0]

pprint(eqn)
print("----------------------------------------")
pprint(eqn - LCM*R_det)
print("----------------------------------------")
print("integers:",integers)
sys.exit(0)

print("=======================================================")

# now, let's find our full polynomial ...
# first, we need to know the r matrix:
r_str = """
r11 r12 r13 r14 r15 r16 r17
r21 r22 r23 r24 r25 r26 r27
r31 r32 r33 r34 r35 r36 r37
r41 r42 r43 r44 r45 r46 r47
r51 r52 r53 r54 r55 r56 r57
r61 r62 r63 r64 r65 r66 r67
r71 r72 r73 r74 r75 r76 r77
"""

r = zeros(7,7)
#pprint(r)

# learn the r matrix:
learn_matrix(r,r_str)

# now the polynomial:
eqn = 0
for i,j,k,l,m,n,o in product(range(7), repeat=7):
  if (i + j + k + l + m + n + o) % 7 != 0:       # if a term has the wrong signature it has coeff 0
    continue

  indices = (i,j,k,l,m,n,o)

  if len(set(indices)) == 1:                      # ie, a diagonal element
    Q = LCM
  else:
    Qijklmno = "Q{0}{1}{2}{3}{4}{5}{6}".format(*sorted(indices))
    Q = LCM // Q_table[Qijklmno]

  eqn += Q * r[0,i] * r[1,j] * r[2,k] * r[3,l] * r[4,m] * r[5,n] * r[6,o]      # not 100% this line is correct!


# now, put it in a form we can use in python:
# how many terms per line:
n = 5

ds7 = "def ds7(values):\n  "
for i,j in product(range(1,6), repeat=2):      # should this be range(1,8)?
  rij = "r%s%s" % (i,j)
  ds7 += rij + ","
ds7 = ds7[:-1]                      # chomp off trailing ","
ds7 += " = values\n  return ("      # what if the resulting line is too long??

equation = [str(x) for x in eqn.args ]
for k in range(0,len(equation),n):
  short_row = equation[k:k+n]
  ds7 += " + ".join(short_row) + '\n  + '
ds7 += "0 )\n"

print("ds7:")
print(ds7)

