#######################################################################
# the semantic-db sigmoids
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018
# Update: 17/2/2018
# Copyright: GPLv3
#
# Usage: 
#
#######################################################################

import math

# some sigmoids:
def clean(x):
  if x <= 0:
    return 0
  else:
    return 1

# this one is so common that it is implemented in superposition as .drop_below(t)
def threshold_filter(x,t):
  if x < t:
    return 0
  else:
    return x

def not_threshold_filter(x,t):
  if x <= t:
    return x
  else:
    return 0

def binary_filter(x):
  if x <= 0.96:
    return 0
  else:
    return 1

def not_binary_filter(x):
  if x <= 0.96:
    return 1
  else:
    return 0

def pos(x):           # what about an "abs" sigmoid?
  if x <= 0:
    return 0
  else:
    return x

# 4/5/2015:
def sigmoid_abs(x):           
  return abs(x)

# 4/5/2015:
def max_filter(x,t):
  if x <= t:
    return x
  else:
    return t

def NOT(x):
  if x <= 0.04:
    return 1
  else:
    return 0

# otherwise known as the Goldilock's function.
# not too hot, not too cold.
def xor_filter(x):
  if 0.96 <= x and x <= 1.04:
    return 1
  else:
    return 0

# so common this has been added to superposition as x.multiply(t)
def mult(x,t):
  return x*t

# this is another type of "Goldilock function"
# the in-range sigmoid:
def sigmoid_in_range(x,a,b):
  if a <= x and x <= b:
    return x
  else:
    return 0

# 14/4/2014: newly added:
def invert(x):
  if x == 0:
    return 0
  else:
    return 1/x
    
# 21/5/2014: newly added:
# set all coeffs to t, even the 0'd ones.
def set_to(x,t):
  return t

# 4/1/2015:
def subtraction_invert(x,t):
  return t - x

# 15/12/2015:
def log(x,t=None):
  if x <= 0:
    return 0
  if t is None:
    return math.log(x)       # default is base e, ie natural logarithm
  return math.log(x,t)       # choose another base

# 17/5/2016:                 # log(1 + x)
def log_1(x,t=None):
  if x <= 0:                 # maybe tweak this, given that it is log(1 + x), not log(x)
    return 0
  if t is None:
    return math.log(1+x)       # default is base e, ie natural logarithm
  return math.log(1+x,t)       # choose another base

  
# 14/1/2016:
def square(x):
  return x*x
  
def sqrt(x):
  return math.sqrt(x)
  
# 12/9/2016:
def floor(x):
  return math.floor(x)
  
def ceiling(x):
  return math.ceil(x)      

def not_zero(x):
  if x <= 0:
    return 1
  return x