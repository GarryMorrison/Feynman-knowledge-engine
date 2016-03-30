#!c:/Python34/python.exe

#######################################################################
# use sympy for my ds^5,3 problem 
# this time aiming for R = exp(P5 t1) * exp(P3 t2)
# Bah! Can't get it to work. Either bug in my ugly code, or it is not possible.
# I suspect it is possible though ....
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-30
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


R1_str = """
a c b 0 0
b a c 0 0
c b a 0 0
0 0 0 u 0
0 0 0 0 u
"""

R2_str = """
a e d c b
b a e d c
c b a e d
d c b a e
e d c b a
"""

R1 = zeros(5,5)
R2 = zeros(5,5)
R = zeros(5,5)             # R = R2 * R1
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

# in the R1 case we need hand learning, we can't use learn_matrix:
i = 0
j = 0
for line in R1_str.split('\n'):
  line = line.strip()
  if len(line) == 0:
    continue
  for elt in line.split(' '):
    if elt == '0':
      R1[i,j] = 0
    elif elt == 'u':
      R1[i,j] = R1[0,0] + R1[0,1] + R1[0,2]
    else:
      R1[i,j] = Symbol(elt)
    j += 1
  i += 1
  j = 0

# we can use learn_matrix for R2:
learn_matrix(R2,R2_str)

# finally, our R matrix, that encodes exp(P5 t1) * exp(P3 t2):
R = R2 * R1

# see what we have:
pprint(R1)
pprint(R2)
pprint(R)
#sys.exit(0)

# check the determinant:
print(R.det())
#sys.exit(0)


# bah this is ugly!!!
R_det = R.det()
det_table = {}
count = 0
sign = 1
for term in R_det.args:
  str_term = str(term)
  if str_term[0] == '-':
    sign = -1
    str_term = str_term[1:]
  if str_term[0].isalpha():
    det_table[str_term] = sign
  else:
    coeff,rest = str_term.split('*',1)
    det_table[rest] = sign*int(coeff)
  sign = 1
  count += 1
print("count:",count)

det_integers = set()
for key,value in det_table.items():
  print("%s: %s" % (key,value))
  det_integers.add(abs(value))

# LCM of our integers:
det_table_LCM = lcmm(*det_integers)

print("det_integers:",det_integers)
print("det_table_LCM:",det_table_LCM)
#sys.exit(0)


# construct the equation over Qijklm so we can compare to det(R):
count = 1
eqn = 0
for i,j,k,l,m in product(range(5), repeat=5):
  indices = (i,j,k,l,m)

# Nope! Doesn't work in this case! Hrmm.... didn't expect that.
# Means longer calculations when we hit larger d, though.
#  if ((i + j + k + l + m) % 3 != 0) and ((i + j + k + l + m) % 5 != 0):   # if a term has the wrong signature it has coeff 0
#    continue

#  if len(set(indices)) == 1:                      # ie, a diagonal element. I don't think they apply in this case.
#    Q = 1
#  else:
#    Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
#    Q = symbols(Qijklm)

  Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
  Q = symbols(Qijklm)

  eqn += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0]

# expand the equation:
eqn = expand(eqn)
print(eqn)
#sys.exit(0)


# maybe need to warn if Q_table values are going to be non-integer, though hopefully all the LCM stuff will prevent it!
#
Q_table = {}
count = 0
for term in eqn.args:
  str_term = str(term)
  if str_term[0] == 'Q':
    coeff = '1'
    Q,rest = str_term.split('*',1)
  else:
    coeff,Q,rest = str_term.split('*',2)
  print("coeff:%s\tQ:%s\trest:%s" % (coeff,Q,rest))
  if not coeff.isalpha():                          # does this break sometimes?? Should we check coeff is a float/int instead?
#    Q_table[Q] = int(coeff) // det_table[rest]     # preserve integerness, so don't map to imprecise floats
#    Q_table[Q] = int(coeff) / det_table[rest]       # nope! In this case not integer. How handle then?? LCM of det-table?
    if rest not in det_table:                        # since we want "eqn - det = 0", if term is not in det, then it must be 0.
      Q_table[Q] = 0
    else:                                                           # what about multiple rest's per Q? Is this a problem? It might mean it is not solvable. ie Q doesn't exist.
      Q_table[Q] = det_table_LCM * int(coeff) // det_table[rest]    # LCM of det-table worked, after some thinking!
  count += 1
print("count:",count)
#sys.exit(0)

Q_integers = set()
for key,value in Q_table.items():
  print("%s: %s" % (key,value))
  if value != 0:
    Q_integers.add(abs(value))

# LCM of our integers:
Q_table_LCM = lcmm(*Q_integers)

print("Q_integers:",Q_integers)
print("Q_table_LCM:",Q_table_LCM)
#sys.exit(0)


# Now, let's test we have the right values in Q_table:
# eqn - R_det should be zero.
#
eqn = 0
for i,j,k,l,m, in product(range(5), repeat=5):
#  if (i + j + k + l + m + n + o) % 7 != 0:       # if a term has the wrong signature it has coeff 0
#    continue

#  indices = (i,j,k,l,m)

#  if len(set(indices)) == 1:                      # ie, a diagonal element
#    Q = Q_table_LCM // det_table_LCM
#  else:
#    Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
#    if Qijklm not in Q_table:
#      continue
#    else:
#      Q = Q_table_LCM // Q_table[Qijklm]

  Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
  if Qijklm not in Q_table:
    continue
  else:
    Q = Q_table_LCM // Q_table[Qijklm]

  eqn += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0]

eqn = expand(eqn)
pprint(eqn)
print("----------------------------------------\ntest if zero:")
pprint(eqn - (Q_table_LCM // det_table_LCM) * R_det)
sys.exit(0)

print("=======================================================")

# now, let's find our full polynomial ...
# first, we need to know the r matrix:
r_str = """
r11 r12 r13 r14 r15
r21 r22 r23 r24 r25
r31 r32 r33 r34 r35
r41 r42 r43 r44 r45
r51 r52 r53 r54 r55
"""

r = zeros(5,5)
#pprint(r)

# learn the r matrix:
learn_matrix(r,r_str)
pprint(r)
#sys.exit(0)

# now the polynomial:
eqn = 0
for i,j,k,l,m in product(range(5), repeat=5):
#  if (i + j + k + l + m + n + o) % 7 != 0:       # if a term has the wrong signature it has coeff 0
#    continue

  indices = (i,j,k,l,m)

  if len(set(indices)) == 1:                      # ie, a diagonal element
    Q = Q_table_LCM // det_table_LCM
  else:
    Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
    if Qijklm not in Q_table:
      continue
    else:
      Q = Q_table_LCM // Q_table[Qijklm]

  eqn += Q * r[0,i] * r[1,j] * r[2,k] * r[3,l] * r[4,m]


# now, put it in a form we can use in python:
# how many terms per line:
n = 5

ds = "def ds5_3(values):\n  "
for i,j in product(range(1,6), repeat=2):
  rij = "r%s%s" % (i,j)
  ds += rij + ","
ds = ds[:-1]                       # chomp off trailing ","
ds += " = values\n  return ("      # what if the resulting line is too long??

equation = [str(x) for x in eqn.args ]
for k in range(0,len(equation),n):
  short_row = equation[k:k+n]
  ds += " + ".join(short_row) + '\n  + '
ds += "0 )\n"

print("ds5_3:")
print(ds)

# now save to disk:
with open('ds5_3.py','w') as f:
  f.write(ds)

