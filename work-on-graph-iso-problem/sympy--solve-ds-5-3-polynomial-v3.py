#!c:/Python34/python.exe

#######################################################################
# use sympy for the solved ds^3 problem
# this time, try and use the fact there are integers solutions {a,b,c,d} to J3(a,b,c) = d^3
# and in general Jp(a1,...,ap) = r^p
# OK. It worked. Now, try Jp(a/d^3,b/d^3,c/d^3) version.
# Had a float problem, but solved it, and my equations are over rationals now, and it works!
# Now copy this code and try for d = 5.
#
# OK. d = 5, here we come!
# Let's start with R1
# Bah! Fails. I know there is a solution for R1 since my other methods have found and tested it.
# Fails with this method though. I don't know why ....
# Maybe J3() is the wrong equation to find integer solutions to. Maybe det(R) is the right one.
# Yup. det(R) is the right one.
# Next, it doesn't find a unique solution. It doesn't find the empty set, but it doesn't completely solve it.
# Maybe we need more than just the first equation from: Qabcde = Qijklm Ria Rjb Rkc Rld Rme
# Though other methods solve it just using the first equation.
# Maybe we need more integers that give det(R) == 1?
# Maybe there is some other bug?
# Woot! I needed 2 equations. a,b,c,d,e = 0,0,0,0,0 and a,b,c,d,e = 1,1,1,1,1
# And is fast! 13 seconds. 
# sympy--solve-ds-5-53-polynomial-v2.py
# took 5 minutes for the same problem.
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
#from itertools import product
import itertools
#from itertools import combinations
import string

from sympy import *
from sympy.solvers.solveset import linsolve
init_printing()
rational = True


# learn a matrix:
def learn_matrix(R,R_str):
  i = 0
  j = 0
  for line in R_str.split('\n'):
    line = line.strip()
    if len(line) == 0:
      continue
    for elt in line.split(' '):
      if not elt.isalpha():
        R[i,j] = int(elt)
      else:
        R[i,j] = Symbol(elt)
      j += 1
    i += 1
    j = 0


# try a new method for defining R, that will easily allow symbol substitution:
# P3^3 = I
P3_str = """
0 0 1 0 0
1 0 0 0 0
0 1 0 0 0
0 0 0 1 0
0 0 0 0 1
"""
# P5^5 = I
P5_str = """
0 0 0 0 1
1 0 0 0 0
0 1 0 0 0
0 0 1 0 0
0 0 0 1 0
"""

# now learn our permutation matrices P5 and P3:
P3 = zeros(5,5)
learn_matrix(P3,P3_str)

P5 = zeros(5,5)
learn_matrix(P5,P5_str)

# define our symbols:
a,b,c,d,e,f,g,h,q,s = symbols('a b c d e f g h q s')

# define our R1 = exp(P3 t):
R1 = a*eye(5)/q + b*P3/q + c*P3**2/q

# define our R2 = exp(P5 t):
R2 = d*eye(5)/s + e*P5/s + f*P5**2/s + g*P5**3/s + h*P5**4/s

#R = R2 * R1
R = R1
#R = R2
# see if it is correct: Yup. Is good.
pprint(R1)
pprint(R2)
pprint(R)

# check the determinant:
R_det = R.det()
print("------------")
print(R_det)
#sys.exit(0)

# hand define J3:                 # we can write code to define a python Jp() later.
def J3(a,b,c):
  return a**3 + b**3 + c**3 - 3*a*b*c

#print(simplify(R2.det()*s**5))    # use this to hand define J5

# hand define J5_3:
def J5_3(a,b,c):
  return ( a**5 + 2*a**4*b + 2*a**4*c + a**3*b**2 - a**3*b*c 
  + a**3*c**2 + a**2*b**3 - 6*a**2*b**2*c - 6*a**2*b*c**2 + a**2*c**3 
  + 2*a*b**4 - a*b**3*c - 6*a*b**2*c**2 - a*b*c**3 + 2*a*c**4 
  + b**5 + 2*b**4*c + b**3*c**2 + b**2*c**3 + 2*b*c**4 + c**5 )

print("zero:",J5_3(7,7,7))   # Jp(a,a,a,...,a) = 0. Good.
#sys.exit(0)


# hand define J5:
def J5(d,e,f,g,h):
  return ( d**5 -5*d**3*e*h -5*d**3*f*g + 5*d**2*e**2*g + 5*d**2*e*f**2 + 5*d**2*f*h**2 
  + 5*d**2*g**2*h -5*d*e**3*f + 5*d*e**2*h**2 -5*d*e*f*g*h -5*d*e*g**3 -5*d*f**3*h + 5*d*f**2*g**2 
  + -5*d*g*h**3 + e**5 -5*e**3*g*h + 5*e**2*f**2*h + 5*e**2*f*g**2 -5*e*f**3*g -5*e*f*h**3 
  + 5*e*g**2*h**2 + f**5 + 5*f**2*g*h**2 -5*f*g**3*h + g**5 + h**5 )

#print("zero:",J5(7,7,7,7,7))   # Jp(a,a,a,...,a) = 0. Good. This check helped spot a bug.
#sys.exit(0)

#our_integer_J3_solutions = []
# find integer solutions to: J3(a,b,c) = det(r) = d^3
# then find rational solutions to J3(a,b,c) = 1
#for x,y,z,r in itertools.product(range(2,50), repeat=4):
##  J3 = R_det.subs([(a,x), (b,y), (c,z)])
#  indices = [x,y,z]
#  if len(set(indices)) == 1:               # trivial solution: J3(a,a,a) = 0
#    continue
#  if indices == sorted(indices):
##for r in range(2,100):
##  for x,y,z in combinations(range(2,100), 3):
#    if J3(x,y,z) == r**3:
#      print("%s %s %s: %s" % (x,y,z,r))
#      our_integer_J3_solutions.append([x,y,z,r])

#our_integer_J5_3_solutions = []
# find integer solutions to: J3(a,b,c) = det(r) = d^3
# then find rational solutions to J3(a,b,c) = 1
#for x,y,z,r in itertools.product(range(2,50), repeat=4):
##  J3 = R_det.subs([(a,x), (b,y), (c,z)])
#  indices = [x,y,z]
#  if len(set(indices)) == 1:               # trivial solution: J3(a,a,a) = 0
#    continue
#  if indices == sorted(indices):
#for r in range(2,500):                     # swap this version in later
#  for x,y,z in itertools.combinations(range(2,500), 3):
#    if J5_3(x,y,z) == r**5:
#      print("%s %s %s: %s" % (x,y,z,r))
#      our_integer_J5_3_solutions.append([x,y,z,r])

# load them from disk, since they take so long to make in python:
# in practice a massive speed up. In the background I have c code to make them fast!
our_integer_J5_3_solutions = []
filename = "J5_3_integers_200.txt"
with open(filename,'r') as f:
  for line in f:
    line = line.strip()
    print("line:",line)
    x,y,z,r = line.split(' ')
    our_integer_J5_3_solutions.append([int(x),int(y),int(z),int(r)])
print("-----------")
#sys.exit(0)

#our_integer_J5_solutions = []
# find integer solutions to: J5(a,b,c,d,e) = det(R2) = s^5
#for u,v,x,y,z,r in product(range(2,50), repeat=6):
#  indices = [u,v,x,y,z]
#  if len(set(indices)) == 1:               # trivial solution: J3(a,a,a) = 0
#    continue
#  if indices == sorted(indices):           # only consider one of each, no point learning duplicates
#    if J5(u,v,x,y,z) == r**5:
#      print("%s %s %s %s %s: %s" % (u,v,x,y,z,r))
#      our_integer_J5_solutions.append([x,y,z,r])

#sys.exit(0)

# construct the equation over Qijklm:
eqn1 = 0
eqn2 = 0
for i,j,k,l,m in itertools.product(range(5), repeat=5):
  indices = (i,j,k,l,m)

  Qijklm = "Q{0}{1}{2}{3}{4}".format(*sorted(indices))
  Q = symbols(Qijklm)

  eqn1 += Q * R[i,0] * R[j,0] * R[k,0] * R[l,0] * R[m,0]
  eqn2 += Q * R[i,1] * R[j,1] * R[k,1] * R[l,1] * R[m,1]

# expand the equations:
eqn1 = expand(eqn1)
eqn2 = expand(eqn2)
print(eqn1)
print(eqn1)
print("-----------------------")
print(R_det)
print("-------------------------------------")
#sys.exit(0)

# check our J5_3 integer solutions against det(R):
for x,y,z,r in our_integer_J5_3_solutions:
  print("%s %s %s: %s" % (x,y,z,r))
#  value = J3(x,y,z)/r**3
#  print("value:%s r:%s" %(value,r))
  r0 = R_det.subs([(a,x), (b,y), (c,z), (q,r)])              # woot! Code works. These all give det(R) = 1 at these integer values.
  print("r0:",r0)
#sys.exit(0)

# find a system of equations:
# use actual values to create a system of equations over Q. Try and solve that way.
# this time using a,b,c such that J3(a,b,c) = 1. This way we can completely ignore det(R).
system_of_eqns = []
max = 10
count = 0
for x,y,z,r in our_integer_J5_3_solutions:
  
#  r0 = eqn.subs([(a,x), (b,y), (c,z)])                # this version works.
#  print("r0:",r0)
#  this_eqn = simplify(r0 - r**3)

#  r_3 = r**3                                           # this version does not. Cursed by floats. Not sure how to fix. I'm thinking LCM again, over our set of r's.
#  r1 = r**3 * eqn.subs([(a,x/r), (b,y/r), (c,z/r)])            # because for the "R = R2 * R1" case we can't expect r0 == r**3.
#  print("r1:",r1)                                      # but we can expect J3()/r**3 == 1 and J5()/s**5 == 1
#  this_eqn = simplify(r1 - 1)
#  this_eqn = r1 - r**3

  r2 = eqn1.subs([(a,x), (b,y), (c,z), (q,r)])           # solved my float problem. Woot!!! It works!!
  r3 = eqn2.subs([(a,x), (b,y), (c,z), (q,r)])
#  print("r2:",r2)
  this_eqn1 = r2 - 1
  this_eqn2 = r3 - 1

#  this_eqn1 = r2 - symbols('Q00000')                     # this version gives a messier output, but looks to work.
#  this_eqn2 = r3 - symbols('Q11111')

  system_of_eqns.append(this_eqn1)
  system_of_eqns.append(this_eqn2)
#  count += 1
#  if count >= max:
#    break

# print out our system of equations:
for an_eqn in system_of_eqns:
  print("eqn:",an_eqn)

our_Qs = OrderedDict()
for term in eqn1.args:
  str_term = str(term)
  print("term:",str_term)
  if str_term[0] == 'Q':
    coeff = '1'
    Q,rest = str_term.split('*',1)
  else:
    coeff,Q,rest = str_term.split('*',2)
  if Q not in our_Qs:
    our_Qs[Q] = [coeff + "*" + rest]
  else:
    our_Qs[Q].append(coeff + "*" + rest)

for key,value in our_Qs.items():
  print("%s: %s" % (key,value))

variables = symbols(" ".join(list(our_Qs)))                # assumes our_Qs is an ordered dictionary, not a standard one.
print(variables)

result = linsolve(system_of_eqns,variables)
print("result:",result)

Q_values = OrderedDict()
for k,Q in enumerate(our_Qs):
  value = list(result)[0][k]
  print("%s: %s" % (Q,value))
  Q_values[Q] = value

sys.exit(0)


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
print("-----------------------")
print(R_det)
print("-------------------------------------")
#eqn.subs(R_det,1)              # nope. Doesn't work, but I had to try.
#print(eqn)

# use actual values to create a system of equations over Q. Try and solve that way.
system_of_eqns = []
a1,b1,c1,d1,e1,f1,g1,h1 = symbols('a b c d e f g h')
#str_eqn = str(eqn)
#det_eqn = str(R_det)
max = 10
count = 0
#for a,b,c,d,e,f,g,h in product(range(4), repeat=8):
#for a,b,c,d,e,f,g,h in product((0,1,11), repeat=8):
for a,b,c,d,e in product(range(4), repeat=5):
#  r0 = str_eqn.replace('a',str(a))
#  r1 = r0.repace('b',str(b))
#  r2 = r1.replace('c',str(c))
#  r3 = r2.replace('d',str(d))
#  r4 = r3.replace('e',str(e))

#  r5 = r4.replace('f',str(f))
#  r6 = r5.replace('g',str(g))
#  r7 = r6.replace('h',str(h))

#  print("r7:",r7)

  p0 = det_eqn.replace('a',str(a))
  p1 = p0.replace('b',str(b))
  p2 = p1.replace('c',str(c))
  p3 = p2.replace('d',str(d))
  p4 = p3.replace('e',str(e))

  p5 = p4.replace('f',str(f))
  p6 = p5.replace('g',str(g))
  p7 = p6.replace('h',str(h))

#  print("r7:",r7)

  this_eqn = simplify(sympify(r7) - sympify(p7))
  system_of_eqns.append(this_eqn)
  count += 1
  if count >= max:
    break

for an_eqn in system_of_eqns:
  print("eqn:",an_eqn)


our_Qs = OrderedDict()
for term in eqn.args:
  str_term = str(term)
  print("term:",str_term)
  if str_term[0] == 'Q':
    coeff = '1'
    Q,rest = str_term.split('*',1)
  else:
    coeff,Q,rest = str_term.split('*',2)
  if Q not in our_Qs:
    our_Qs[Q] = [coeff + "*" + rest]
  else:
    our_Qs[Q].append(coeff + "*" + rest)

for key,value in our_Qs.items():
  print("%s: %s" % (key,value))


variables = symbols(" ".join(list(our_Qs)))                # assumes our_Qs is an ordered dictionary, not a standard one.
print(variables)

#sys.exit(0)
result = linsolve(system_of_eqns,variables)
print("result:",result)

Q_values = OrderedDict()
for k,Q in enumerate(our_Qs):
  value = list(result)[0][k]
  print("%s: %s" % (Q,value))
  Q_values[Q] = value

sys.exit(0)


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

