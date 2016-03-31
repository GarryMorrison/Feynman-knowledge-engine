#!c:/Python34/python.exe

#######################################################################
# use sympy for my ds^5,3 problem 
# this time aiming for R = exp(P5 t1) * exp(P3 t2)
# Bah! Can't get it to work. Either bug in my ugly code, or it is not possible.
# I suspect it is possible though ....
# ahh... I tracked down the bug. 
# a**6*b**4: ['10*Q00022', '80*Q01111', '120*Q00112']
# for my current code to work, we need only 1 element on the right hand side of this.
# I'm sure it's solvable, just not yet how :)
# So, in a way, this is good news. It makes it more likely for this idea to work.
# Ahh.... going to have to make M Q = V, then Q = M^-1 V, assuming we can make M invertable, which might not be possible.
# but how make sure final elts in Q are integers and not floats? Oh well, for later.
# BTW, previous method implicitly assumed M was diagonal, which of course is particularly easy to invert.
# Woot! Finally have solve linear equations version. Took some work!
# Works for P5 and P3, but I don't think it does for P5,P3.
# Nope. For exp(P5 t1) * exp(P3 t2) I get: result: EmptySet()
# So either it has no solution, or there is a bug in this code.
# Pity, because it would have been really useful!
# I need a proof that it is or is not possible!
# ahh... I think I found the bug! mixing a,b,c in R1 with those in R2.
# they should be completely distinct!! Fixing this doesn't guarantee solution though ....
#
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-30
# Update: 2016-3-31
# Copyright: GPLv3
#
# Usage: ./play_with_sympy.py
#
#######################################################################


import sys
import functools                                    # so reduce() works in python 3.
from collections import OrderedDict

from sympy import *
from sympy.solvers.solveset import linsolve
init_printing()

from itertools import product


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
f h g 0 0
g f h 0 0
h g f 0 0
0 0 0 u 0
0 0 0 0 u
"""

R1_test_str = """
a c b 0 0
b a c 0 0
c b a 0 0
0 0 0 1 0
0 0 0 0 1
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
    if not elt.isalpha():
      R1[i,j] = int(elt)
    elif elt == 'u':                               # try with this switched off
      R1[i,j] = R1[0,0] + R1[0,1] + R1[0,2]
    else:
      R1[i,j] = Symbol(elt)
    j += 1
  i += 1
  j = 0

# we can use learn_matrix for R2:
learn_matrix(R2,R2_str)

# finally, our R matrix, that encodes exp(P5 t1) * exp(P3 t2):
#R = R2 * R1                 # doesn't work, result is the empty set
#R = R1                     # works
R = R2                     # works

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
#det_table = {}
det_table = OrderedDict()
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
print("det_table count:",count)

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

  Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))                 # maybe Q is not symmetric?? Nope. It is symmetric.
  Q = symbols(Qijklm)

  eqn += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0]

# expand the equation:
eqn = expand(eqn)
print(eqn)
#sys.exit(0)



# maybe need to warn if Q_table values are going to be non-integer, though hopefully all the LCM stuff will prevent it!
#
#Q_table = {}
Q_table = OrderedDict()
rest_table = OrderedDict()
our_Qs = OrderedDict()
count = 0
for term in eqn.args:
  str_term = str(term)
  print("term:",str_term)
  if str_term[0] == 'Q':
    coeff = '1'
    Q,rest = str_term.split('*',1)
  else:
    coeff,Q,rest = str_term.split('*',2)

  if rest not in rest_table:
    rest_table[rest] = [coeff + "*" + Q]
  else:
    rest_table[rest].append(coeff + "*" + Q)

  if Q not in our_Qs:
    our_Qs[Q] = [coeff + "*" + rest]
  else:
    our_Qs[Q].append(coeff + "*" + rest)

  if Q in Q_table:                                               # only need to learn it once
    continue
  if rest not in det_table:
#    continue
    det_table[rest] = 0                                          # though messes with "foo //det_table[rest]"
  print("coeff:%s\tQ:%s\trest:%s\tdet_table:%s" % (coeff,Q,rest,det_table[rest]))
  if int(coeff) == 0:
    print("WARNING: unexpected 0")
    continue
  if not coeff.isalpha():                                         # does this break sometimes?? Should we check coeff is a float/int instead?
#    Q_table[Q] = det_table_LCM * int(coeff) // det_table[rest]    # LCM of det-table worked, after some thinking!
    Q_table[Q] = det_table[rest] / int(coeff)
  count += 1
print("count:",count)
#sys.exit(0)

#Q_integers = set()
#for key,value in Q_table.items():
#  print("%s: %s" % (key,value))
#  if value != 0:
#    Q_integers.add(abs(value))

# LCM of our integers:
#Q_table_LCM = lcmm(*Q_integers)

#print("Q_integers:",Q_integers)
#print("Q_table_LCM:",Q_table_LCM)

eqn_dict = OrderedDict()
for key,value in rest_table.items():
  if key not in det_table:
    det_value = 0
  else:
    det_value = det_table[key]
  print("%s: %s: %s" % (key,det_value,value))
  the_eqn = " + ".join(value) + " - " + str(det_value)
  eqn_dict[key] = sympify(the_eqn)

system_of_eqns = []
for key,value in eqn_dict.items():
  print("%s: %s" % (key,value))
  system_of_eqns.append(value)

print(system_of_eqns)

variables = symbols(" ".join(list(our_Qs)))                # assumes our_Qs is an ordered dictionary, not a standard one.
print(variables)

result = linsolve(system_of_eqns,variables)
print("result:",result)

Q_values = OrderedDict()
for k,Q in enumerate(our_Qs):
  value = list(result)[0][k]
  print("%s: %s" % (Q,value))
  Q_values[Q] = value



# Now, let's test we have the right values in Q_table:
# eqn - R_det should be zero.
#
eqn = 0
for i,j,k,l,m, in product(range(5), repeat=5):
#  if (i + j + k + l + m + n + o) % 7 != 0:       # if a term has the wrong signature it has coeff 0
#    continue

  indices = (i,j,k,l,m)

#  if len(set(indices)) == 1:                      # ie, a diagonal element. Doesn't work if using exp(P5 t1) * exp(P3 t2)
#    Q = Q_table_LCM // det_table_LCM
#  else:
#    Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
#    if Qijklm not in Q_table:
#      continue
#    else:
#      Q = Q_table_LCM // Q_table[Qijklm]

  Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))        # maybe not symmetric. Testing it ....
  if Qijklm not in Q_values:
    continue
  Q = Q_values[Qijklm]

  eqn += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0]

eqn = expand(eqn)
print(eqn)
print("---------------------------------")
print(R_det)
print("test zero:")
print(eqn - R_det)                                             # Yup. Works for R1 and R2
sys.exit(0)


# now, let's find our full polynomial ...
# first, we need to know the r matrix:
r_str = """
r11 r12 r13 r14 r15
r21 r22 r23 r24 r25
r31 r32 r33 r34 r35
r41 r42 r43 r44 r45
r51 r52 r53 r54 r55
"""

# learn the r matrix:
r = zeros(5,5)
learn_matrix(r,r_str)
pprint(r)

# now learn the poly:
eqn = 0
for i,j,k,l,m, in product(range(5), repeat=5):
  indices = (i,j,k,l,m)

  Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
  if Qijklm not in Q_table:
    continue
  Q = Q_values[Qijklm]
  eqn += Q * r[0,i] * r[1,j] * r[2,k] * r[3,l] * r[4,m]

# convert from fractions to integers:
eqn = eqn*24                            # need to automate this step later!

# now, put it in a form we can use in python:
# how many terms per line:
n = 5

ds = "def ds5_3_test(values):\n  "
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

print("ds5_3_test:")
print(ds)

# now save to disk:
filename = "ds5_3_test.py"
print("saving ds to:",filename)
with open(filename,'w') as f:
  f.write(ds)

sys.exit(0)




print("len det_table:",len(det_table))
print("len Q-table:",len(Q_table))
print("len rest-table:",len(rest_table))
count = 0
for key,value in rest_table.items():
  if key in det_table:
    count += 1
print("non-zero rest-table eqns:",count)

print("*****************************")
count = 0
for key,value in det_table.items():
#  if key not in rest_table:
#    print("key: %s value: %s" % (key,value))
#  else:
#     count += 1
  print("%s: %s: %s" % (key,value,rest_table[key]))

count = 0
for key,value in our_Qs.items():
  print("%s: %s" % (key,value))
  count += 1
print("count:",count)

system_of_eqns = []
for key,value in eqn_dict.items():
  print("%s: %s" % (key,value))
  system_of_eqns.append(value)

print(system_of_eqns)

variables = symbols(" ".join(list(our_Qs)))
print(variables)
result = linsolve(system_of_eqns,variables)
print("result:",result)
sys.exit(0)


# Now, let's test we have the right values in Q_table:
# eqn - R_det should be zero.
#
eqn = 0
for i,j,k,l,m, in product(range(5), repeat=5):
#  if (i + j + k + l + m + n + o) % 7 != 0:       # if a term has the wrong signature it has coeff 0
#    continue

#  indices = (i,j,k,l,m)

#  if len(set(indices)) == 1:                      # ie, a diagonal element. Doesn't work if using exp(P5 t1) * exp(P3 t2)
#    Q = Q_table_LCM // det_table_LCM
#  else:
#    Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
#    if Qijklm not in Q_table:
#      continue
#    else:
#      Q = Q_table_LCM // Q_table[Qijklm]

  Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))        # maybe not symmetric. Testing it ....
#  Qijklm = "Q{0}{1}{2}{3}{4}".format(*indices) 
  if Qijklm not in Q_table:
    continue
#  Q = Q_table_LCM // Q_table[Qijklm]
  Q = Q_table[Qijklm]

  eqn += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0]

eqn = expand(eqn)
print(eqn)
print("---------------------------------")
print(R_det)
sys.exit(0)
pprint(eqn2)
print("----------------------------------------\ntest if zero:")
pprint(eqn2 - (Q_table_LCM // det_table_LCM) * R_det)
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

