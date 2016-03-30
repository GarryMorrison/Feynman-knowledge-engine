#!/usr/bin/env python3

#######################################################################
# implement my ds^5 signature polynomial
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-28
# Update:
# Copyright: GPLv3
#
# Usage: ./calculate_ds5.py file.mat
#
#######################################################################


import sys
from fractions import Fraction

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("calculate ds5")

filename = sys.argv[1]

def first_ds5(values):
  r11,r12,r13,r14,r15,r21,r22,r23,r24,r25,r31,r32,r33,r34,r35,r41,r42,r43,r44,r45,r51,r52,r53,r54,r55 = values
  return (r11*r21*r31*r41*r51 + -1/4*r11*r21*r31*r42*r55 + -1/4*r11*r21*r31*r43*r54 + -1/4*r11*r21*r31*r44*r53 + -1/4*r11*r21*r31*r45*r52
  + -1/4*r11*r21*r32*r41*r55 + 1/6*r11*r21*r32*r42*r54 + 1/6*r11*r21*r32*r43*r53 + 1/6*r11*r21*r32*r44*r52 + -1/4*r11*r21*r32*r45*r51
  + -1/4*r11*r21*r33*r41*r54 + 1/6*r11*r21*r33*r42*r53 + 1/6*r11*r21*r33*r43*r52 + -1/4*r11*r21*r33*r44*r51 + 1/6*r11*r21*r33*r45*r55
  + -1/4*r11*r21*r34*r41*r53 + 1/6*r11*r21*r34*r42*r52 + -1/4*r11*r21*r34*r43*r51 + 1/6*r11*r21*r34*r44*r55 + 1/6*r11*r21*r34*r45*r54
  + -1/4*r11*r21*r35*r41*r52 + -1/4*r11*r21*r35*r42*r51 + 1/6*r11*r21*r35*r43*r55 + 1/6*r11*r21*r35*r44*r54 + 1/6*r11*r21*r35*r45*r53
  + -1/4*r11*r22*r31*r41*r55 + 1/6*r11*r22*r31*r42*r54 + 1/6*r11*r22*r31*r43*r53 + 1/6*r11*r22*r31*r44*r52 + -1/4*r11*r22*r31*r45*r51
  + 1/6*r11*r22*r32*r41*r54 + -1/4*r11*r22*r32*r42*r53 + -1/4*r11*r22*r32*r43*r52 + 1/6*r11*r22*r32*r44*r51 + 1/6*r11*r22*r32*r45*r55
  + 1/6*r11*r22*r33*r41*r53 + -1/4*r11*r22*r33*r42*r52 + 1/6*r11*r22*r33*r43*r51 + -1/24*r11*r22*r33*r44*r55 + -1/24*r11*r22*r33*r45*r54
  + 1/6*r11*r22*r34*r41*r52 + 1/6*r11*r22*r34*r42*r51 + -1/24*r11*r22*r34*r43*r55 + -1/4*r11*r22*r34*r44*r54 + -1/24*r11*r22*r34*r45*r53
  + -1/4*r11*r22*r35*r41*r51 + 1/6*r11*r22*r35*r42*r55 + -1/24*r11*r22*r35*r43*r54 + -1/24*r11*r22*r35*r44*r53 + 1/6*r11*r22*r35*r45*r52
  + -1/4*r11*r23*r31*r41*r54 + 1/6*r11*r23*r31*r42*r53 + 1/6*r11*r23*r31*r43*r52 + -1/4*r11*r23*r31*r44*r51 + 1/6*r11*r23*r31*r45*r55
  + 1/6*r11*r23*r32*r41*r53 + -1/4*r11*r23*r32*r42*r52 + 1/6*r11*r23*r32*r43*r51 + -1/24*r11*r23*r32*r44*r55 + -1/24*r11*r23*r32*r45*r54
  + 1/6*r11*r23*r33*r41*r52 + 1/6*r11*r23*r33*r42*r51 + -1/4*r11*r23*r33*r43*r55 + 1/6*r11*r23*r33*r44*r54 + -1/4*r11*r23*r33*r45*r53
  + -1/4*r11*r23*r34*r41*r51 + -1/24*r11*r23*r34*r42*r55 + 1/6*r11*r23*r34*r43*r54 + 1/6*r11*r23*r34*r44*r53 + -1/24*r11*r23*r34*r45*r52
  + 1/6*r11*r23*r35*r41*r55 + -1/24*r11*r23*r35*r42*r54 + -1/4*r11*r23*r35*r43*r53 + -1/24*r11*r23*r35*r44*r52 + 1/6*r11*r23*r35*r45*r51
  + -1/4*r11*r24*r31*r41*r53 + 1/6*r11*r24*r31*r42*r52 + -1/4*r11*r24*r31*r43*r51 + 1/6*r11*r24*r31*r44*r55 + 1/6*r11*r24*r31*r45*r54
  + 1/6*r11*r24*r32*r41*r52 + 1/6*r11*r24*r32*r42*r51 + -1/24*r11*r24*r32*r43*r55 + -1/4*r11*r24*r32*r44*r54 + -1/24*r11*r24*r32*r45*r53
  + -1/4*r11*r24*r33*r41*r51 + -1/24*r11*r24*r33*r42*r55 + 1/6*r11*r24*r33*r43*r54 + 1/6*r11*r24*r33*r44*r53 + -1/24*r11*r24*r33*r45*r52
  + 1/6*r11*r24*r34*r41*r55 + -1/4*r11*r24*r34*r42*r54 + 1/6*r11*r24*r34*r43*r53 + -1/4*r11*r24*r34*r44*r52 + 1/6*r11*r24*r34*r45*r51
  + 1/6*r11*r24*r35*r41*r54 + -1/24*r11*r24*r35*r42*r53 + -1/24*r11*r24*r35*r43*r52 + 1/6*r11*r24*r35*r44*r51 + -1/4*r11*r24*r35*r45*r55
  + -1/4*r11*r25*r31*r41*r52 + -1/4*r11*r25*r31*r42*r51 + 1/6*r11*r25*r31*r43*r55 + 1/6*r11*r25*r31*r44*r54 + 1/6*r11*r25*r31*r45*r53
  + -1/4*r11*r25*r32*r41*r51 + 1/6*r11*r25*r32*r42*r55 + -1/24*r11*r25*r32*r43*r54 + -1/24*r11*r25*r32*r44*r53 + 1/6*r11*r25*r32*r45*r52
  + 1/6*r11*r25*r33*r41*r55 + -1/24*r11*r25*r33*r42*r54 + -1/4*r11*r25*r33*r43*r53 + -1/24*r11*r25*r33*r44*r52 + 1/6*r11*r25*r33*r45*r51
  + 1/6*r11*r25*r34*r41*r54 + -1/24*r11*r25*r34*r42*r53 + -1/24*r11*r25*r34*r43*r52 + 1/6*r11*r25*r34*r44*r51 + -1/4*r11*r25*r34*r45*r55
  + 1/6*r11*r25*r35*r41*r53 + 1/6*r11*r25*r35*r42*r52 + 1/6*r11*r25*r35*r43*r51 + -1/4*r11*r25*r35*r44*r55 + -1/4*r11*r25*r35*r45*r54
  + -1/4*r12*r21*r31*r41*r55 + 1/6*r12*r21*r31*r42*r54 + 1/6*r12*r21*r31*r43*r53 + 1/6*r12*r21*r31*r44*r52 + -1/4*r12*r21*r31*r45*r51
  + 1/6*r12*r21*r32*r41*r54 + -1/4*r12*r21*r32*r42*r53 + -1/4*r12*r21*r32*r43*r52 + 1/6*r12*r21*r32*r44*r51 + 1/6*r12*r21*r32*r45*r55
  + 1/6*r12*r21*r33*r41*r53 + -1/4*r12*r21*r33*r42*r52 + 1/6*r12*r21*r33*r43*r51 + -1/24*r12*r21*r33*r44*r55 + -1/24*r12*r21*r33*r45*r54
  + 1/6*r12*r21*r34*r41*r52 + 1/6*r12*r21*r34*r42*r51 + -1/24*r12*r21*r34*r43*r55 + -1/4*r12*r21*r34*r44*r54 + -1/24*r12*r21*r34*r45*r53
  + -1/4*r12*r21*r35*r41*r51 + 1/6*r12*r21*r35*r42*r55 + -1/24*r12*r21*r35*r43*r54 + -1/24*r12*r21*r35*r44*r53 + 1/6*r12*r21*r35*r45*r52
  + 1/6*r12*r22*r31*r41*r54 + -1/4*r12*r22*r31*r42*r53 + -1/4*r12*r22*r31*r43*r52 + 1/6*r12*r22*r31*r44*r51 + 1/6*r12*r22*r31*r45*r55
  + -1/4*r12*r22*r32*r41*r53 + r12*r22*r32*r42*r52 + -1/4*r12*r22*r32*r43*r51 + -1/4*r12*r22*r32*r44*r55 + -1/4*r12*r22*r32*r45*r54
  + -1/4*r12*r22*r33*r41*r52 + -1/4*r12*r22*r33*r42*r51 + 1/6*r12*r22*r33*r43*r55 + 1/6*r12*r22*r33*r44*r54 + 1/6*r12*r22*r33*r45*r53
  + 1/6*r12*r22*r34*r41*r51 + -1/4*r12*r22*r34*r42*r55 + 1/6*r12*r22*r34*r43*r54 + 1/6*r12*r22*r34*r44*r53 + -1/4*r12*r22*r34*r45*r52
  + 1/6*r12*r22*r35*r41*r55 + -1/4*r12*r22*r35*r42*r54 + 1/6*r12*r22*r35*r43*r53 + -1/4*r12*r22*r35*r44*r52 + 1/6*r12*r22*r35*r45*r51
  + 1/6*r12*r23*r31*r41*r53 + -1/4*r12*r23*r31*r42*r52 + 1/6*r12*r23*r31*r43*r51 + -1/24*r12*r23*r31*r44*r55 + -1/24*r12*r23*r31*r45*r54
  + -1/4*r12*r23*r32*r41*r52 + -1/4*r12*r23*r32*r42*r51 + 1/6*r12*r23*r32*r43*r55 + 1/6*r12*r23*r32*r44*r54 + 1/6*r12*r23*r32*r45*r53
  + 1/6*r12*r23*r33*r41*r51 + 1/6*r12*r23*r33*r42*r55 + -1/4*r12*r23*r33*r43*r54 + -1/4*r12*r23*r33*r44*r53 + 1/6*r12*r23*r33*r45*r52
  + -1/24*r12*r23*r34*r41*r55 + 1/6*r12*r23*r34*r42*r54 + -1/4*r12*r23*r34*r43*r53 + 1/6*r12*r23*r34*r44*r52 + -1/24*r12*r23*r34*r45*r51
  + -1/24*r12*r23*r35*r41*r54 + 1/6*r12*r23*r35*r42*r53 + 1/6*r12*r23*r35*r43*r52 + -1/24*r12*r23*r35*r44*r51 + -1/4*r12*r23*r35*r45*r55
  + 1/6*r12*r24*r31*r41*r52 + 1/6*r12*r24*r31*r42*r51 + -1/24*r12*r24*r31*r43*r55 + -1/4*r12*r24*r31*r44*r54 + -1/24*r12*r24*r31*r45*r53
  + 1/6*r12*r24*r32*r41*r51 + -1/4*r12*r24*r32*r42*r55 + 1/6*r12*r24*r32*r43*r54 + 1/6*r12*r24*r32*r44*r53 + -1/4*r12*r24*r32*r45*r52
  + -1/24*r12*r24*r33*r41*r55 + 1/6*r12*r24*r33*r42*r54 + -1/4*r12*r24*r33*r43*r53 + 1/6*r12*r24*r33*r44*r52 + -1/24*r12*r24*r33*r45*r51
  + -1/4*r12*r24*r34*r41*r54 + 1/6*r12*r24*r34*r42*r53 + 1/6*r12*r24*r34*r43*r52 + -1/4*r12*r24*r34*r44*r51 + 1/6*r12*r24*r34*r45*r55
  + -1/24*r12*r24*r35*r41*r53 + -1/4*r12*r24*r35*r42*r52 + -1/24*r12*r24*r35*r43*r51 + 1/6*r12*r24*r35*r44*r55 + 1/6*r12*r24*r35*r45*r54
  + -1/4*r12*r25*r31*r41*r51 + 1/6*r12*r25*r31*r42*r55 + -1/24*r12*r25*r31*r43*r54 + -1/24*r12*r25*r31*r44*r53 + 1/6*r12*r25*r31*r45*r52
  + 1/6*r12*r25*r32*r41*r55 + -1/4*r12*r25*r32*r42*r54 + 1/6*r12*r25*r32*r43*r53 + -1/4*r12*r25*r32*r44*r52 + 1/6*r12*r25*r32*r45*r51
  + -1/24*r12*r25*r33*r41*r54 + 1/6*r12*r25*r33*r42*r53 + 1/6*r12*r25*r33*r43*r52 + -1/24*r12*r25*r33*r44*r51 + -1/4*r12*r25*r33*r45*r55
  + -1/24*r12*r25*r34*r41*r53 + -1/4*r12*r25*r34*r42*r52 + -1/24*r12*r25*r34*r43*r51 + 1/6*r12*r25*r34*r44*r55 + 1/6*r12*r25*r34*r45*r54
  + 1/6*r12*r25*r35*r41*r52 + 1/6*r12*r25*r35*r42*r51 + -1/4*r12*r25*r35*r43*r55 + 1/6*r12*r25*r35*r44*r54 + -1/4*r12*r25*r35*r45*r53
  + -1/4*r13*r21*r31*r41*r54 + 1/6*r13*r21*r31*r42*r53 + 1/6*r13*r21*r31*r43*r52 + -1/4*r13*r21*r31*r44*r51 + 1/6*r13*r21*r31*r45*r55
  + 1/6*r13*r21*r32*r41*r53 + -1/4*r13*r21*r32*r42*r52 + 1/6*r13*r21*r32*r43*r51 + -1/24*r13*r21*r32*r44*r55 + -1/24*r13*r21*r32*r45*r54
  + 1/6*r13*r21*r33*r41*r52 + 1/6*r13*r21*r33*r42*r51 + -1/4*r13*r21*r33*r43*r55 + 1/6*r13*r21*r33*r44*r54 + -1/4*r13*r21*r33*r45*r53
  + -1/4*r13*r21*r34*r41*r51 + -1/24*r13*r21*r34*r42*r55 + 1/6*r13*r21*r34*r43*r54 + 1/6*r13*r21*r34*r44*r53 + -1/24*r13*r21*r34*r45*r52
  + 1/6*r13*r21*r35*r41*r55 + -1/24*r13*r21*r35*r42*r54 + -1/4*r13*r21*r35*r43*r53 + -1/24*r13*r21*r35*r44*r52 + 1/6*r13*r21*r35*r45*r51
  + 1/6*r13*r22*r31*r41*r53 + -1/4*r13*r22*r31*r42*r52 + 1/6*r13*r22*r31*r43*r51 + -1/24*r13*r22*r31*r44*r55 + -1/24*r13*r22*r31*r45*r54
  + -1/4*r13*r22*r32*r41*r52 + -1/4*r13*r22*r32*r42*r51 + 1/6*r13*r22*r32*r43*r55 + 1/6*r13*r22*r32*r44*r54 + 1/6*r13*r22*r32*r45*r53
  + 1/6*r13*r22*r33*r41*r51 + 1/6*r13*r22*r33*r42*r55 + -1/4*r13*r22*r33*r43*r54 + -1/4*r13*r22*r33*r44*r53 + 1/6*r13*r22*r33*r45*r52
  + -1/24*r13*r22*r34*r41*r55 + 1/6*r13*r22*r34*r42*r54 + -1/4*r13*r22*r34*r43*r53 + 1/6*r13*r22*r34*r44*r52 + -1/24*r13*r22*r34*r45*r51
  + -1/24*r13*r22*r35*r41*r54 + 1/6*r13*r22*r35*r42*r53 + 1/6*r13*r22*r35*r43*r52 + -1/24*r13*r22*r35*r44*r51 + -1/4*r13*r22*r35*r45*r55
  + 1/6*r13*r23*r31*r41*r52 + 1/6*r13*r23*r31*r42*r51 + -1/4*r13*r23*r31*r43*r55 + 1/6*r13*r23*r31*r44*r54 + -1/4*r13*r23*r31*r45*r53
  + 1/6*r13*r23*r32*r41*r51 + 1/6*r13*r23*r32*r42*r55 + -1/4*r13*r23*r32*r43*r54 + -1/4*r13*r23*r32*r44*r53 + 1/6*r13*r23*r32*r45*r52
  + -1/4*r13*r23*r33*r41*r55 + -1/4*r13*r23*r33*r42*r54 + r13*r23*r33*r43*r53 + -1/4*r13*r23*r33*r44*r52 + -1/4*r13*r23*r33*r45*r51
  + 1/6*r13*r23*r34*r41*r54 + -1/4*r13*r23*r34*r42*r53 + -1/4*r13*r23*r34*r43*r52 + 1/6*r13*r23*r34*r44*r51 + 1/6*r13*r23*r34*r45*r55
  + -1/4*r13*r23*r35*r41*r53 + 1/6*r13*r23*r35*r42*r52 + -1/4*r13*r23*r35*r43*r51 + 1/6*r13*r23*r35*r44*r55 + 1/6*r13*r23*r35*r45*r54
  + -1/4*r13*r24*r31*r41*r51 + -1/24*r13*r24*r31*r42*r55 + 1/6*r13*r24*r31*r43*r54 + 1/6*r13*r24*r31*r44*r53 + -1/24*r13*r24*r31*r45*r52
  + -1/24*r13*r24*r32*r41*r55 + 1/6*r13*r24*r32*r42*r54 + -1/4*r13*r24*r32*r43*r53 + 1/6*r13*r24*r32*r44*r52 + -1/24*r13*r24*r32*r45*r51
  + 1/6*r13*r24*r33*r41*r54 + -1/4*r13*r24*r33*r42*r53 + -1/4*r13*r24*r33*r43*r52 + 1/6*r13*r24*r33*r44*r51 + 1/6*r13*r24*r33*r45*r55
  + 1/6*r13*r24*r34*r41*r53 + 1/6*r13*r24*r34*r42*r52 + 1/6*r13*r24*r34*r43*r51 + -1/4*r13*r24*r34*r44*r55 + -1/4*r13*r24*r34*r45*r54
  + -1/24*r13*r24*r35*r41*r52 + -1/24*r13*r24*r35*r42*r51 + 1/6*r13*r24*r35*r43*r55 + -1/4*r13*r24*r35*r44*r54 + 1/6*r13*r24*r35*r45*r53
  + 1/6*r13*r25*r31*r41*r55 + -1/24*r13*r25*r31*r42*r54 + -1/4*r13*r25*r31*r43*r53 + -1/24*r13*r25*r31*r44*r52 + 1/6*r13*r25*r31*r45*r51
  + -1/24*r13*r25*r32*r41*r54 + 1/6*r13*r25*r32*r42*r53 + 1/6*r13*r25*r32*r43*r52 + -1/24*r13*r25*r32*r44*r51 + -1/4*r13*r25*r32*r45*r55
  + -1/4*r13*r25*r33*r41*r53 + 1/6*r13*r25*r33*r42*r52 + -1/4*r13*r25*r33*r43*r51 + 1/6*r13*r25*r33*r44*r55 + 1/6*r13*r25*r33*r45*r54
  + -1/24*r13*r25*r34*r41*r52 + -1/24*r13*r25*r34*r42*r51 + 1/6*r13*r25*r34*r43*r55 + -1/4*r13*r25*r34*r44*r54 + 1/6*r13*r25*r34*r45*r53
  + 1/6*r13*r25*r35*r41*r51 + -1/4*r13*r25*r35*r42*r55 + 1/6*r13*r25*r35*r43*r54 + 1/6*r13*r25*r35*r44*r53 + -1/4*r13*r25*r35*r45*r52
  + -1/4*r14*r21*r31*r41*r53 + 1/6*r14*r21*r31*r42*r52 + -1/4*r14*r21*r31*r43*r51 + 1/6*r14*r21*r31*r44*r55 + 1/6*r14*r21*r31*r45*r54
  + 1/6*r14*r21*r32*r41*r52 + 1/6*r14*r21*r32*r42*r51 + -1/24*r14*r21*r32*r43*r55 + -1/4*r14*r21*r32*r44*r54 + -1/24*r14*r21*r32*r45*r53
  + -1/4*r14*r21*r33*r41*r51 + -1/24*r14*r21*r33*r42*r55 + 1/6*r14*r21*r33*r43*r54 + 1/6*r14*r21*r33*r44*r53 + -1/24*r14*r21*r33*r45*r52
  + 1/6*r14*r21*r34*r41*r55 + -1/4*r14*r21*r34*r42*r54 + 1/6*r14*r21*r34*r43*r53 + -1/4*r14*r21*r34*r44*r52 + 1/6*r14*r21*r34*r45*r51
  + 1/6*r14*r21*r35*r41*r54 + -1/24*r14*r21*r35*r42*r53 + -1/24*r14*r21*r35*r43*r52 + 1/6*r14*r21*r35*r44*r51 + -1/4*r14*r21*r35*r45*r55
  + 1/6*r14*r22*r31*r41*r52 + 1/6*r14*r22*r31*r42*r51 + -1/24*r14*r22*r31*r43*r55 + -1/4*r14*r22*r31*r44*r54 + -1/24*r14*r22*r31*r45*r53
  + 1/6*r14*r22*r32*r41*r51 + -1/4*r14*r22*r32*r42*r55 + 1/6*r14*r22*r32*r43*r54 + 1/6*r14*r22*r32*r44*r53 + -1/4*r14*r22*r32*r45*r52
  + -1/24*r14*r22*r33*r41*r55 + 1/6*r14*r22*r33*r42*r54 + -1/4*r14*r22*r33*r43*r53 + 1/6*r14*r22*r33*r44*r52 + -1/24*r14*r22*r33*r45*r51
  + -1/4*r14*r22*r34*r41*r54 + 1/6*r14*r22*r34*r42*r53 + 1/6*r14*r22*r34*r43*r52 + -1/4*r14*r22*r34*r44*r51 + 1/6*r14*r22*r34*r45*r55
  + -1/24*r14*r22*r35*r41*r53 + -1/4*r14*r22*r35*r42*r52 + -1/24*r14*r22*r35*r43*r51 + 1/6*r14*r22*r35*r44*r55 + 1/6*r14*r22*r35*r45*r54
  + -1/4*r14*r23*r31*r41*r51 + -1/24*r14*r23*r31*r42*r55 + 1/6*r14*r23*r31*r43*r54 + 1/6*r14*r23*r31*r44*r53 + -1/24*r14*r23*r31*r45*r52
  + -1/24*r14*r23*r32*r41*r55 + 1/6*r14*r23*r32*r42*r54 + -1/4*r14*r23*r32*r43*r53 + 1/6*r14*r23*r32*r44*r52 + -1/24*r14*r23*r32*r45*r51
  + 1/6*r14*r23*r33*r41*r54 + -1/4*r14*r23*r33*r42*r53 + -1/4*r14*r23*r33*r43*r52 + 1/6*r14*r23*r33*r44*r51 + 1/6*r14*r23*r33*r45*r55
  + 1/6*r14*r23*r34*r41*r53 + 1/6*r14*r23*r34*r42*r52 + 1/6*r14*r23*r34*r43*r51 + -1/4*r14*r23*r34*r44*r55 + -1/4*r14*r23*r34*r45*r54
  + -1/24*r14*r23*r35*r41*r52 + -1/24*r14*r23*r35*r42*r51 + 1/6*r14*r23*r35*r43*r55 + -1/4*r14*r23*r35*r44*r54 + 1/6*r14*r23*r35*r45*r53
  + 1/6*r14*r24*r31*r41*r55 + -1/4*r14*r24*r31*r42*r54 + 1/6*r14*r24*r31*r43*r53 + -1/4*r14*r24*r31*r44*r52 + 1/6*r14*r24*r31*r45*r51
  + -1/4*r14*r24*r32*r41*r54 + 1/6*r14*r24*r32*r42*r53 + 1/6*r14*r24*r32*r43*r52 + -1/4*r14*r24*r32*r44*r51 + 1/6*r14*r24*r32*r45*r55
  + 1/6*r14*r24*r33*r41*r53 + 1/6*r14*r24*r33*r42*r52 + 1/6*r14*r24*r33*r43*r51 + -1/4*r14*r24*r33*r44*r55 + -1/4*r14*r24*r33*r45*r54
  + -1/4*r14*r24*r34*r41*r52 + -1/4*r14*r24*r34*r42*r51 + -1/4*r14*r24*r34*r43*r55 + r14*r24*r34*r44*r54 + -1/4*r14*r24*r34*r45*r53
  + 1/6*r14*r24*r35*r41*r51 + 1/6*r14*r24*r35*r42*r55 + -1/4*r14*r24*r35*r43*r54 + -1/4*r14*r24*r35*r44*r53 + 1/6*r14*r24*r35*r45*r52
  + 1/6*r14*r25*r31*r41*r54 + -1/24*r14*r25*r31*r42*r53 + -1/24*r14*r25*r31*r43*r52 + 1/6*r14*r25*r31*r44*r51 + -1/4*r14*r25*r31*r45*r55
  + -1/24*r14*r25*r32*r41*r53 + -1/4*r14*r25*r32*r42*r52 + -1/24*r14*r25*r32*r43*r51 + 1/6*r14*r25*r32*r44*r55 + 1/6*r14*r25*r32*r45*r54
  + -1/24*r14*r25*r33*r41*r52 + -1/24*r14*r25*r33*r42*r51 + 1/6*r14*r25*r33*r43*r55 + -1/4*r14*r25*r33*r44*r54 + 1/6*r14*r25*r33*r45*r53
  + 1/6*r14*r25*r34*r41*r51 + 1/6*r14*r25*r34*r42*r55 + -1/4*r14*r25*r34*r43*r54 + -1/4*r14*r25*r34*r44*r53 + 1/6*r14*r25*r34*r45*r52
  + -1/4*r14*r25*r35*r41*r55 + 1/6*r14*r25*r35*r42*r54 + 1/6*r14*r25*r35*r43*r53 + 1/6*r14*r25*r35*r44*r52 + -1/4*r14*r25*r35*r45*r51
  + -1/4*r15*r21*r31*r41*r52 + -1/4*r15*r21*r31*r42*r51 + 1/6*r15*r21*r31*r43*r55 + 1/6*r15*r21*r31*r44*r54 + 1/6*r15*r21*r31*r45*r53
  + -1/4*r15*r21*r32*r41*r51 + 1/6*r15*r21*r32*r42*r55 + -1/24*r15*r21*r32*r43*r54 + -1/24*r15*r21*r32*r44*r53 + 1/6*r15*r21*r32*r45*r52
  + 1/6*r15*r21*r33*r41*r55 + -1/24*r15*r21*r33*r42*r54 + -1/4*r15*r21*r33*r43*r53 + -1/24*r15*r21*r33*r44*r52 + 1/6*r15*r21*r33*r45*r51
  + 1/6*r15*r21*r34*r41*r54 + -1/24*r15*r21*r34*r42*r53 + -1/24*r15*r21*r34*r43*r52 + 1/6*r15*r21*r34*r44*r51 + -1/4*r15*r21*r34*r45*r55
  + 1/6*r15*r21*r35*r41*r53 + 1/6*r15*r21*r35*r42*r52 + 1/6*r15*r21*r35*r43*r51 + -1/4*r15*r21*r35*r44*r55 + -1/4*r15*r21*r35*r45*r54
  + -1/4*r15*r22*r31*r41*r51 + 1/6*r15*r22*r31*r42*r55 + -1/24*r15*r22*r31*r43*r54 + -1/24*r15*r22*r31*r44*r53 + 1/6*r15*r22*r31*r45*r52
  + 1/6*r15*r22*r32*r41*r55 + -1/4*r15*r22*r32*r42*r54 + 1/6*r15*r22*r32*r43*r53 + -1/4*r15*r22*r32*r44*r52 + 1/6*r15*r22*r32*r45*r51
  + -1/24*r15*r22*r33*r41*r54 + 1/6*r15*r22*r33*r42*r53 + 1/6*r15*r22*r33*r43*r52 + -1/24*r15*r22*r33*r44*r51 + -1/4*r15*r22*r33*r45*r55
  + -1/24*r15*r22*r34*r41*r53 + -1/4*r15*r22*r34*r42*r52 + -1/24*r15*r22*r34*r43*r51 + 1/6*r15*r22*r34*r44*r55 + 1/6*r15*r22*r34*r45*r54
  + 1/6*r15*r22*r35*r41*r52 + 1/6*r15*r22*r35*r42*r51 + -1/4*r15*r22*r35*r43*r55 + 1/6*r15*r22*r35*r44*r54 + -1/4*r15*r22*r35*r45*r53
  + 1/6*r15*r23*r31*r41*r55 + -1/24*r15*r23*r31*r42*r54 + -1/4*r15*r23*r31*r43*r53 + -1/24*r15*r23*r31*r44*r52 + 1/6*r15*r23*r31*r45*r51
  + -1/24*r15*r23*r32*r41*r54 + 1/6*r15*r23*r32*r42*r53 + 1/6*r15*r23*r32*r43*r52 + -1/24*r15*r23*r32*r44*r51 + -1/4*r15*r23*r32*r45*r55
  + -1/4*r15*r23*r33*r41*r53 + 1/6*r15*r23*r33*r42*r52 + -1/4*r15*r23*r33*r43*r51 + 1/6*r15*r23*r33*r44*r55 + 1/6*r15*r23*r33*r45*r54
  + -1/24*r15*r23*r34*r41*r52 + -1/24*r15*r23*r34*r42*r51 + 1/6*r15*r23*r34*r43*r55 + -1/4*r15*r23*r34*r44*r54 + 1/6*r15*r23*r34*r45*r53
  + 1/6*r15*r23*r35*r41*r51 + -1/4*r15*r23*r35*r42*r55 + 1/6*r15*r23*r35*r43*r54 + 1/6*r15*r23*r35*r44*r53 + -1/4*r15*r23*r35*r45*r52
  + 1/6*r15*r24*r31*r41*r54 + -1/24*r15*r24*r31*r42*r53 + -1/24*r15*r24*r31*r43*r52 + 1/6*r15*r24*r31*r44*r51 + -1/4*r15*r24*r31*r45*r55
  + -1/24*r15*r24*r32*r41*r53 + -1/4*r15*r24*r32*r42*r52 + -1/24*r15*r24*r32*r43*r51 + 1/6*r15*r24*r32*r44*r55 + 1/6*r15*r24*r32*r45*r54
  + -1/24*r15*r24*r33*r41*r52 + -1/24*r15*r24*r33*r42*r51 + 1/6*r15*r24*r33*r43*r55 + -1/4*r15*r24*r33*r44*r54 + 1/6*r15*r24*r33*r45*r53
  + 1/6*r15*r24*r34*r41*r51 + 1/6*r15*r24*r34*r42*r55 + -1/4*r15*r24*r34*r43*r54 + -1/4*r15*r24*r34*r44*r53 + 1/6*r15*r24*r34*r45*r52
  + -1/4*r15*r24*r35*r41*r55 + 1/6*r15*r24*r35*r42*r54 + 1/6*r15*r24*r35*r43*r53 + 1/6*r15*r24*r35*r44*r52 + -1/4*r15*r24*r35*r45*r51
  + 1/6*r15*r25*r31*r41*r53 + 1/6*r15*r25*r31*r42*r52 + 1/6*r15*r25*r31*r43*r51 + -1/4*r15*r25*r31*r44*r55 + -1/4*r15*r25*r31*r45*r54
  + 1/6*r15*r25*r32*r41*r52 + 1/6*r15*r25*r32*r42*r51 + -1/4*r15*r25*r32*r43*r55 + 1/6*r15*r25*r32*r44*r54 + -1/4*r15*r25*r32*r45*r53
  + 1/6*r15*r25*r33*r41*r51 + -1/4*r15*r25*r33*r42*r55 + 1/6*r15*r25*r33*r43*r54 + 1/6*r15*r25*r33*r44*r53 + -1/4*r15*r25*r33*r45*r52
  + -1/4*r15*r25*r34*r41*r55 + 1/6*r15*r25*r34*r42*r54 + 1/6*r15*r25*r34*r43*r53 + 1/6*r15*r25*r34*r44*r52 + -1/4*r15*r25*r34*r45*r51
  + -1/4*r15*r25*r35*r41*r54 + -1/4*r15*r25*r35*r42*r53 + -1/4*r15*r25*r35*r43*r52 + -1/4*r15*r25*r35*r44*r51 + r15*r25*r35*r45*r55
  + 0 )


def ds5(values):
  r11,r12,r13,r14,r15,r21,r22,r23,r24,r25,r31,r32,r33,r34,r35,r41,r42,r43,r44,r45,r51,r52,r53,r54,r55 = values
  return (r11*r21*r31*r41*r51 + -Fraction(1,4)*r11*r21*r31*r42*r55 + -Fraction(1,4)*r11*r21*r31*r43*r54 + -Fraction(1,4)*r11*r21*r31*r44*r53 + -Fraction(1,4)*r11*r21*r31*r45*r52
  + -Fraction(1,4)*r11*r21*r32*r41*r55 + Fraction(1,6)*r11*r21*r32*r42*r54 + Fraction(1,6)*r11*r21*r32*r43*r53 + Fraction(1,6)*r11*r21*r32*r44*r52 + -Fraction(1,4)*r11*r21*r32*r45*r51
  + -Fraction(1,4)*r11*r21*r33*r41*r54 + Fraction(1,6)*r11*r21*r33*r42*r53 + Fraction(1,6)*r11*r21*r33*r43*r52 + -Fraction(1,4)*r11*r21*r33*r44*r51 + Fraction(1,6)*r11*r21*r33*r45*r55
  + -Fraction(1,4)*r11*r21*r34*r41*r53 + Fraction(1,6)*r11*r21*r34*r42*r52 + -Fraction(1,4)*r11*r21*r34*r43*r51 + Fraction(1,6)*r11*r21*r34*r44*r55 + Fraction(1,6)*r11*r21*r34*r45*r54
  + -Fraction(1,4)*r11*r21*r35*r41*r52 + -Fraction(1,4)*r11*r21*r35*r42*r51 + Fraction(1,6)*r11*r21*r35*r43*r55 + Fraction(1,6)*r11*r21*r35*r44*r54 + Fraction(1,6)*r11*r21*r35*r45*r53
  + -Fraction(1,4)*r11*r22*r31*r41*r55 + Fraction(1,6)*r11*r22*r31*r42*r54 + Fraction(1,6)*r11*r22*r31*r43*r53 + Fraction(1,6)*r11*r22*r31*r44*r52 + -Fraction(1,4)*r11*r22*r31*r45*r51
  + Fraction(1,6)*r11*r22*r32*r41*r54 + -Fraction(1,4)*r11*r22*r32*r42*r53 + -Fraction(1,4)*r11*r22*r32*r43*r52 + Fraction(1,6)*r11*r22*r32*r44*r51 + Fraction(1,6)*r11*r22*r32*r45*r55
  + Fraction(1,6)*r11*r22*r33*r41*r53 + -Fraction(1,4)*r11*r22*r33*r42*r52 + Fraction(1,6)*r11*r22*r33*r43*r51 + -Fraction(1,24)*r11*r22*r33*r44*r55 + -Fraction(1,24)*r11*r22*r33*r45*r54
  + Fraction(1,6)*r11*r22*r34*r41*r52 + Fraction(1,6)*r11*r22*r34*r42*r51 + -Fraction(1,24)*r11*r22*r34*r43*r55 + -Fraction(1,4)*r11*r22*r34*r44*r54 + -Fraction(1,24)*r11*r22*r34*r45*r53
  + -Fraction(1,4)*r11*r22*r35*r41*r51 + Fraction(1,6)*r11*r22*r35*r42*r55 + -Fraction(1,24)*r11*r22*r35*r43*r54 + -Fraction(1,24)*r11*r22*r35*r44*r53 + Fraction(1,6)*r11*r22*r35*r45*r52
  + -Fraction(1,4)*r11*r23*r31*r41*r54 + Fraction(1,6)*r11*r23*r31*r42*r53 + Fraction(1,6)*r11*r23*r31*r43*r52 + -Fraction(1,4)*r11*r23*r31*r44*r51 + Fraction(1,6)*r11*r23*r31*r45*r55
  + Fraction(1,6)*r11*r23*r32*r41*r53 + -Fraction(1,4)*r11*r23*r32*r42*r52 + Fraction(1,6)*r11*r23*r32*r43*r51 + -Fraction(1,24)*r11*r23*r32*r44*r55 + -Fraction(1,24)*r11*r23*r32*r45*r54
  + Fraction(1,6)*r11*r23*r33*r41*r52 + Fraction(1,6)*r11*r23*r33*r42*r51 + -Fraction(1,4)*r11*r23*r33*r43*r55 + Fraction(1,6)*r11*r23*r33*r44*r54 + -Fraction(1,4)*r11*r23*r33*r45*r53
  + -Fraction(1,4)*r11*r23*r34*r41*r51 + -Fraction(1,24)*r11*r23*r34*r42*r55 + Fraction(1,6)*r11*r23*r34*r43*r54 + Fraction(1,6)*r11*r23*r34*r44*r53 + -Fraction(1,24)*r11*r23*r34*r45*r52
  + Fraction(1,6)*r11*r23*r35*r41*r55 + -Fraction(1,24)*r11*r23*r35*r42*r54 + -Fraction(1,4)*r11*r23*r35*r43*r53 + -Fraction(1,24)*r11*r23*r35*r44*r52 + Fraction(1,6)*r11*r23*r35*r45*r51
  + -Fraction(1,4)*r11*r24*r31*r41*r53 + Fraction(1,6)*r11*r24*r31*r42*r52 + -Fraction(1,4)*r11*r24*r31*r43*r51 + Fraction(1,6)*r11*r24*r31*r44*r55 + Fraction(1,6)*r11*r24*r31*r45*r54
  + Fraction(1,6)*r11*r24*r32*r41*r52 + Fraction(1,6)*r11*r24*r32*r42*r51 + -Fraction(1,24)*r11*r24*r32*r43*r55 + -Fraction(1,4)*r11*r24*r32*r44*r54 + -Fraction(1,24)*r11*r24*r32*r45*r53
  + -Fraction(1,4)*r11*r24*r33*r41*r51 + -Fraction(1,24)*r11*r24*r33*r42*r55 + Fraction(1,6)*r11*r24*r33*r43*r54 + Fraction(1,6)*r11*r24*r33*r44*r53 + -Fraction(1,24)*r11*r24*r33*r45*r52
  + Fraction(1,6)*r11*r24*r34*r41*r55 + -Fraction(1,4)*r11*r24*r34*r42*r54 + Fraction(1,6)*r11*r24*r34*r43*r53 + -Fraction(1,4)*r11*r24*r34*r44*r52 + Fraction(1,6)*r11*r24*r34*r45*r51
  + Fraction(1,6)*r11*r24*r35*r41*r54 + -Fraction(1,24)*r11*r24*r35*r42*r53 + -Fraction(1,24)*r11*r24*r35*r43*r52 + Fraction(1,6)*r11*r24*r35*r44*r51 + -Fraction(1,4)*r11*r24*r35*r45*r55
  + -Fraction(1,4)*r11*r25*r31*r41*r52 + -Fraction(1,4)*r11*r25*r31*r42*r51 + Fraction(1,6)*r11*r25*r31*r43*r55 + Fraction(1,6)*r11*r25*r31*r44*r54 + Fraction(1,6)*r11*r25*r31*r45*r53
  + -Fraction(1,4)*r11*r25*r32*r41*r51 + Fraction(1,6)*r11*r25*r32*r42*r55 + -Fraction(1,24)*r11*r25*r32*r43*r54 + -Fraction(1,24)*r11*r25*r32*r44*r53 + Fraction(1,6)*r11*r25*r32*r45*r52
  + Fraction(1,6)*r11*r25*r33*r41*r55 + -Fraction(1,24)*r11*r25*r33*r42*r54 + -Fraction(1,4)*r11*r25*r33*r43*r53 + -Fraction(1,24)*r11*r25*r33*r44*r52 + Fraction(1,6)*r11*r25*r33*r45*r51
  + Fraction(1,6)*r11*r25*r34*r41*r54 + -Fraction(1,24)*r11*r25*r34*r42*r53 + -Fraction(1,24)*r11*r25*r34*r43*r52 + Fraction(1,6)*r11*r25*r34*r44*r51 + -Fraction(1,4)*r11*r25*r34*r45*r55
  + Fraction(1,6)*r11*r25*r35*r41*r53 + Fraction(1,6)*r11*r25*r35*r42*r52 + Fraction(1,6)*r11*r25*r35*r43*r51 + -Fraction(1,4)*r11*r25*r35*r44*r55 + -Fraction(1,4)*r11*r25*r35*r45*r54
  + -Fraction(1,4)*r12*r21*r31*r41*r55 + Fraction(1,6)*r12*r21*r31*r42*r54 + Fraction(1,6)*r12*r21*r31*r43*r53 + Fraction(1,6)*r12*r21*r31*r44*r52 + -Fraction(1,4)*r12*r21*r31*r45*r51
  + Fraction(1,6)*r12*r21*r32*r41*r54 + -Fraction(1,4)*r12*r21*r32*r42*r53 + -Fraction(1,4)*r12*r21*r32*r43*r52 + Fraction(1,6)*r12*r21*r32*r44*r51 + Fraction(1,6)*r12*r21*r32*r45*r55
  + Fraction(1,6)*r12*r21*r33*r41*r53 + -Fraction(1,4)*r12*r21*r33*r42*r52 + Fraction(1,6)*r12*r21*r33*r43*r51 + -Fraction(1,24)*r12*r21*r33*r44*r55 + -Fraction(1,24)*r12*r21*r33*r45*r54
  + Fraction(1,6)*r12*r21*r34*r41*r52 + Fraction(1,6)*r12*r21*r34*r42*r51 + -Fraction(1,24)*r12*r21*r34*r43*r55 + -Fraction(1,4)*r12*r21*r34*r44*r54 + -Fraction(1,24)*r12*r21*r34*r45*r53
  + -Fraction(1,4)*r12*r21*r35*r41*r51 + Fraction(1,6)*r12*r21*r35*r42*r55 + -Fraction(1,24)*r12*r21*r35*r43*r54 + -Fraction(1,24)*r12*r21*r35*r44*r53 + Fraction(1,6)*r12*r21*r35*r45*r52
  + Fraction(1,6)*r12*r22*r31*r41*r54 + -Fraction(1,4)*r12*r22*r31*r42*r53 + -Fraction(1,4)*r12*r22*r31*r43*r52 + Fraction(1,6)*r12*r22*r31*r44*r51 + Fraction(1,6)*r12*r22*r31*r45*r55
  + -Fraction(1,4)*r12*r22*r32*r41*r53 + r12*r22*r32*r42*r52 + -Fraction(1,4)*r12*r22*r32*r43*r51 + -Fraction(1,4)*r12*r22*r32*r44*r55 + -Fraction(1,4)*r12*r22*r32*r45*r54
  + -Fraction(1,4)*r12*r22*r33*r41*r52 + -Fraction(1,4)*r12*r22*r33*r42*r51 + Fraction(1,6)*r12*r22*r33*r43*r55 + Fraction(1,6)*r12*r22*r33*r44*r54 + Fraction(1,6)*r12*r22*r33*r45*r53
  + Fraction(1,6)*r12*r22*r34*r41*r51 + -Fraction(1,4)*r12*r22*r34*r42*r55 + Fraction(1,6)*r12*r22*r34*r43*r54 + Fraction(1,6)*r12*r22*r34*r44*r53 + -Fraction(1,4)*r12*r22*r34*r45*r52
  + Fraction(1,6)*r12*r22*r35*r41*r55 + -Fraction(1,4)*r12*r22*r35*r42*r54 + Fraction(1,6)*r12*r22*r35*r43*r53 + -Fraction(1,4)*r12*r22*r35*r44*r52 + Fraction(1,6)*r12*r22*r35*r45*r51
  + Fraction(1,6)*r12*r23*r31*r41*r53 + -Fraction(1,4)*r12*r23*r31*r42*r52 + Fraction(1,6)*r12*r23*r31*r43*r51 + -Fraction(1,24)*r12*r23*r31*r44*r55 + -Fraction(1,24)*r12*r23*r31*r45*r54
  + -Fraction(1,4)*r12*r23*r32*r41*r52 + -Fraction(1,4)*r12*r23*r32*r42*r51 + Fraction(1,6)*r12*r23*r32*r43*r55 + Fraction(1,6)*r12*r23*r32*r44*r54 + Fraction(1,6)*r12*r23*r32*r45*r53
  + Fraction(1,6)*r12*r23*r33*r41*r51 + Fraction(1,6)*r12*r23*r33*r42*r55 + -Fraction(1,4)*r12*r23*r33*r43*r54 + -Fraction(1,4)*r12*r23*r33*r44*r53 + Fraction(1,6)*r12*r23*r33*r45*r52
  + -Fraction(1,24)*r12*r23*r34*r41*r55 + Fraction(1,6)*r12*r23*r34*r42*r54 + -Fraction(1,4)*r12*r23*r34*r43*r53 + Fraction(1,6)*r12*r23*r34*r44*r52 + -Fraction(1,24)*r12*r23*r34*r45*r51
  + -Fraction(1,24)*r12*r23*r35*r41*r54 + Fraction(1,6)*r12*r23*r35*r42*r53 + Fraction(1,6)*r12*r23*r35*r43*r52 + -Fraction(1,24)*r12*r23*r35*r44*r51 + -Fraction(1,4)*r12*r23*r35*r45*r55
  + Fraction(1,6)*r12*r24*r31*r41*r52 + Fraction(1,6)*r12*r24*r31*r42*r51 + -Fraction(1,24)*r12*r24*r31*r43*r55 + -Fraction(1,4)*r12*r24*r31*r44*r54 + -Fraction(1,24)*r12*r24*r31*r45*r53
  + Fraction(1,6)*r12*r24*r32*r41*r51 + -Fraction(1,4)*r12*r24*r32*r42*r55 + Fraction(1,6)*r12*r24*r32*r43*r54 + Fraction(1,6)*r12*r24*r32*r44*r53 + -Fraction(1,4)*r12*r24*r32*r45*r52
  + -Fraction(1,24)*r12*r24*r33*r41*r55 + Fraction(1,6)*r12*r24*r33*r42*r54 + -Fraction(1,4)*r12*r24*r33*r43*r53 + Fraction(1,6)*r12*r24*r33*r44*r52 + -Fraction(1,24)*r12*r24*r33*r45*r51
  + -Fraction(1,4)*r12*r24*r34*r41*r54 + Fraction(1,6)*r12*r24*r34*r42*r53 + Fraction(1,6)*r12*r24*r34*r43*r52 + -Fraction(1,4)*r12*r24*r34*r44*r51 + Fraction(1,6)*r12*r24*r34*r45*r55
  + -Fraction(1,24)*r12*r24*r35*r41*r53 + -Fraction(1,4)*r12*r24*r35*r42*r52 + -Fraction(1,24)*r12*r24*r35*r43*r51 + Fraction(1,6)*r12*r24*r35*r44*r55 + Fraction(1,6)*r12*r24*r35*r45*r54
  + -Fraction(1,4)*r12*r25*r31*r41*r51 + Fraction(1,6)*r12*r25*r31*r42*r55 + -Fraction(1,24)*r12*r25*r31*r43*r54 + -Fraction(1,24)*r12*r25*r31*r44*r53 + Fraction(1,6)*r12*r25*r31*r45*r52
  + Fraction(1,6)*r12*r25*r32*r41*r55 + -Fraction(1,4)*r12*r25*r32*r42*r54 + Fraction(1,6)*r12*r25*r32*r43*r53 + -Fraction(1,4)*r12*r25*r32*r44*r52 + Fraction(1,6)*r12*r25*r32*r45*r51
  + -Fraction(1,24)*r12*r25*r33*r41*r54 + Fraction(1,6)*r12*r25*r33*r42*r53 + Fraction(1,6)*r12*r25*r33*r43*r52 + -Fraction(1,24)*r12*r25*r33*r44*r51 + -Fraction(1,4)*r12*r25*r33*r45*r55
  + -Fraction(1,24)*r12*r25*r34*r41*r53 + -Fraction(1,4)*r12*r25*r34*r42*r52 + -Fraction(1,24)*r12*r25*r34*r43*r51 + Fraction(1,6)*r12*r25*r34*r44*r55 + Fraction(1,6)*r12*r25*r34*r45*r54
  + Fraction(1,6)*r12*r25*r35*r41*r52 + Fraction(1,6)*r12*r25*r35*r42*r51 + -Fraction(1,4)*r12*r25*r35*r43*r55 + Fraction(1,6)*r12*r25*r35*r44*r54 + -Fraction(1,4)*r12*r25*r35*r45*r53
  + -Fraction(1,4)*r13*r21*r31*r41*r54 + Fraction(1,6)*r13*r21*r31*r42*r53 + Fraction(1,6)*r13*r21*r31*r43*r52 + -Fraction(1,4)*r13*r21*r31*r44*r51 + Fraction(1,6)*r13*r21*r31*r45*r55
  + Fraction(1,6)*r13*r21*r32*r41*r53 + -Fraction(1,4)*r13*r21*r32*r42*r52 + Fraction(1,6)*r13*r21*r32*r43*r51 + -Fraction(1,24)*r13*r21*r32*r44*r55 + -Fraction(1,24)*r13*r21*r32*r45*r54
  + Fraction(1,6)*r13*r21*r33*r41*r52 + Fraction(1,6)*r13*r21*r33*r42*r51 + -Fraction(1,4)*r13*r21*r33*r43*r55 + Fraction(1,6)*r13*r21*r33*r44*r54 + -Fraction(1,4)*r13*r21*r33*r45*r53
  + -Fraction(1,4)*r13*r21*r34*r41*r51 + -Fraction(1,24)*r13*r21*r34*r42*r55 + Fraction(1,6)*r13*r21*r34*r43*r54 + Fraction(1,6)*r13*r21*r34*r44*r53 + -Fraction(1,24)*r13*r21*r34*r45*r52
  + Fraction(1,6)*r13*r21*r35*r41*r55 + -Fraction(1,24)*r13*r21*r35*r42*r54 + -Fraction(1,4)*r13*r21*r35*r43*r53 + -Fraction(1,24)*r13*r21*r35*r44*r52 + Fraction(1,6)*r13*r21*r35*r45*r51
  + Fraction(1,6)*r13*r22*r31*r41*r53 + -Fraction(1,4)*r13*r22*r31*r42*r52 + Fraction(1,6)*r13*r22*r31*r43*r51 + -Fraction(1,24)*r13*r22*r31*r44*r55 + -Fraction(1,24)*r13*r22*r31*r45*r54
  + -Fraction(1,4)*r13*r22*r32*r41*r52 + -Fraction(1,4)*r13*r22*r32*r42*r51 + Fraction(1,6)*r13*r22*r32*r43*r55 + Fraction(1,6)*r13*r22*r32*r44*r54 + Fraction(1,6)*r13*r22*r32*r45*r53
  + Fraction(1,6)*r13*r22*r33*r41*r51 + Fraction(1,6)*r13*r22*r33*r42*r55 + -Fraction(1,4)*r13*r22*r33*r43*r54 + -Fraction(1,4)*r13*r22*r33*r44*r53 + Fraction(1,6)*r13*r22*r33*r45*r52
  + -Fraction(1,24)*r13*r22*r34*r41*r55 + Fraction(1,6)*r13*r22*r34*r42*r54 + -Fraction(1,4)*r13*r22*r34*r43*r53 + Fraction(1,6)*r13*r22*r34*r44*r52 + -Fraction(1,24)*r13*r22*r34*r45*r51
  + -Fraction(1,24)*r13*r22*r35*r41*r54 + Fraction(1,6)*r13*r22*r35*r42*r53 + Fraction(1,6)*r13*r22*r35*r43*r52 + -Fraction(1,24)*r13*r22*r35*r44*r51 + -Fraction(1,4)*r13*r22*r35*r45*r55
  + Fraction(1,6)*r13*r23*r31*r41*r52 + Fraction(1,6)*r13*r23*r31*r42*r51 + -Fraction(1,4)*r13*r23*r31*r43*r55 + Fraction(1,6)*r13*r23*r31*r44*r54 + -Fraction(1,4)*r13*r23*r31*r45*r53
  + Fraction(1,6)*r13*r23*r32*r41*r51 + Fraction(1,6)*r13*r23*r32*r42*r55 + -Fraction(1,4)*r13*r23*r32*r43*r54 + -Fraction(1,4)*r13*r23*r32*r44*r53 + Fraction(1,6)*r13*r23*r32*r45*r52
  + -Fraction(1,4)*r13*r23*r33*r41*r55 + -Fraction(1,4)*r13*r23*r33*r42*r54 + r13*r23*r33*r43*r53 + -Fraction(1,4)*r13*r23*r33*r44*r52 + -Fraction(1,4)*r13*r23*r33*r45*r51
  + Fraction(1,6)*r13*r23*r34*r41*r54 + -Fraction(1,4)*r13*r23*r34*r42*r53 + -Fraction(1,4)*r13*r23*r34*r43*r52 + Fraction(1,6)*r13*r23*r34*r44*r51 + Fraction(1,6)*r13*r23*r34*r45*r55
  + -Fraction(1,4)*r13*r23*r35*r41*r53 + Fraction(1,6)*r13*r23*r35*r42*r52 + -Fraction(1,4)*r13*r23*r35*r43*r51 + Fraction(1,6)*r13*r23*r35*r44*r55 + Fraction(1,6)*r13*r23*r35*r45*r54
  + -Fraction(1,4)*r13*r24*r31*r41*r51 + -Fraction(1,24)*r13*r24*r31*r42*r55 + Fraction(1,6)*r13*r24*r31*r43*r54 + Fraction(1,6)*r13*r24*r31*r44*r53 + -Fraction(1,24)*r13*r24*r31*r45*r52
  + -Fraction(1,24)*r13*r24*r32*r41*r55 + Fraction(1,6)*r13*r24*r32*r42*r54 + -Fraction(1,4)*r13*r24*r32*r43*r53 + Fraction(1,6)*r13*r24*r32*r44*r52 + -Fraction(1,24)*r13*r24*r32*r45*r51
  + Fraction(1,6)*r13*r24*r33*r41*r54 + -Fraction(1,4)*r13*r24*r33*r42*r53 + -Fraction(1,4)*r13*r24*r33*r43*r52 + Fraction(1,6)*r13*r24*r33*r44*r51 + Fraction(1,6)*r13*r24*r33*r45*r55
  + Fraction(1,6)*r13*r24*r34*r41*r53 + Fraction(1,6)*r13*r24*r34*r42*r52 + Fraction(1,6)*r13*r24*r34*r43*r51 + -Fraction(1,4)*r13*r24*r34*r44*r55 + -Fraction(1,4)*r13*r24*r34*r45*r54
  + -Fraction(1,24)*r13*r24*r35*r41*r52 + -Fraction(1,24)*r13*r24*r35*r42*r51 + Fraction(1,6)*r13*r24*r35*r43*r55 + -Fraction(1,4)*r13*r24*r35*r44*r54 + Fraction(1,6)*r13*r24*r35*r45*r53
  + Fraction(1,6)*r13*r25*r31*r41*r55 + -Fraction(1,24)*r13*r25*r31*r42*r54 + -Fraction(1,4)*r13*r25*r31*r43*r53 + -Fraction(1,24)*r13*r25*r31*r44*r52 + Fraction(1,6)*r13*r25*r31*r45*r51
  + -Fraction(1,24)*r13*r25*r32*r41*r54 + Fraction(1,6)*r13*r25*r32*r42*r53 + Fraction(1,6)*r13*r25*r32*r43*r52 + -Fraction(1,24)*r13*r25*r32*r44*r51 + -Fraction(1,4)*r13*r25*r32*r45*r55
  + -Fraction(1,4)*r13*r25*r33*r41*r53 + Fraction(1,6)*r13*r25*r33*r42*r52 + -Fraction(1,4)*r13*r25*r33*r43*r51 + Fraction(1,6)*r13*r25*r33*r44*r55 + Fraction(1,6)*r13*r25*r33*r45*r54
  + -Fraction(1,24)*r13*r25*r34*r41*r52 + -Fraction(1,24)*r13*r25*r34*r42*r51 + Fraction(1,6)*r13*r25*r34*r43*r55 + -Fraction(1,4)*r13*r25*r34*r44*r54 + Fraction(1,6)*r13*r25*r34*r45*r53
  + Fraction(1,6)*r13*r25*r35*r41*r51 + -Fraction(1,4)*r13*r25*r35*r42*r55 + Fraction(1,6)*r13*r25*r35*r43*r54 + Fraction(1,6)*r13*r25*r35*r44*r53 + -Fraction(1,4)*r13*r25*r35*r45*r52
  + -Fraction(1,4)*r14*r21*r31*r41*r53 + Fraction(1,6)*r14*r21*r31*r42*r52 + -Fraction(1,4)*r14*r21*r31*r43*r51 + Fraction(1,6)*r14*r21*r31*r44*r55 + Fraction(1,6)*r14*r21*r31*r45*r54
  + Fraction(1,6)*r14*r21*r32*r41*r52 + Fraction(1,6)*r14*r21*r32*r42*r51 + -Fraction(1,24)*r14*r21*r32*r43*r55 + -Fraction(1,4)*r14*r21*r32*r44*r54 + -Fraction(1,24)*r14*r21*r32*r45*r53
  + -Fraction(1,4)*r14*r21*r33*r41*r51 + -Fraction(1,24)*r14*r21*r33*r42*r55 + Fraction(1,6)*r14*r21*r33*r43*r54 + Fraction(1,6)*r14*r21*r33*r44*r53 + -Fraction(1,24)*r14*r21*r33*r45*r52
  + Fraction(1,6)*r14*r21*r34*r41*r55 + -Fraction(1,4)*r14*r21*r34*r42*r54 + Fraction(1,6)*r14*r21*r34*r43*r53 + -Fraction(1,4)*r14*r21*r34*r44*r52 + Fraction(1,6)*r14*r21*r34*r45*r51
  + Fraction(1,6)*r14*r21*r35*r41*r54 + -Fraction(1,24)*r14*r21*r35*r42*r53 + -Fraction(1,24)*r14*r21*r35*r43*r52 + Fraction(1,6)*r14*r21*r35*r44*r51 + -Fraction(1,4)*r14*r21*r35*r45*r55
  + Fraction(1,6)*r14*r22*r31*r41*r52 + Fraction(1,6)*r14*r22*r31*r42*r51 + -Fraction(1,24)*r14*r22*r31*r43*r55 + -Fraction(1,4)*r14*r22*r31*r44*r54 + -Fraction(1,24)*r14*r22*r31*r45*r53
  + Fraction(1,6)*r14*r22*r32*r41*r51 + -Fraction(1,4)*r14*r22*r32*r42*r55 + Fraction(1,6)*r14*r22*r32*r43*r54 + Fraction(1,6)*r14*r22*r32*r44*r53 + -Fraction(1,4)*r14*r22*r32*r45*r52
  + -Fraction(1,24)*r14*r22*r33*r41*r55 + Fraction(1,6)*r14*r22*r33*r42*r54 + -Fraction(1,4)*r14*r22*r33*r43*r53 + Fraction(1,6)*r14*r22*r33*r44*r52 + -Fraction(1,24)*r14*r22*r33*r45*r51
  + -Fraction(1,4)*r14*r22*r34*r41*r54 + Fraction(1,6)*r14*r22*r34*r42*r53 + Fraction(1,6)*r14*r22*r34*r43*r52 + -Fraction(1,4)*r14*r22*r34*r44*r51 + Fraction(1,6)*r14*r22*r34*r45*r55
  + -Fraction(1,24)*r14*r22*r35*r41*r53 + -Fraction(1,4)*r14*r22*r35*r42*r52 + -Fraction(1,24)*r14*r22*r35*r43*r51 + Fraction(1,6)*r14*r22*r35*r44*r55 + Fraction(1,6)*r14*r22*r35*r45*r54
  + -Fraction(1,4)*r14*r23*r31*r41*r51 + -Fraction(1,24)*r14*r23*r31*r42*r55 + Fraction(1,6)*r14*r23*r31*r43*r54 + Fraction(1,6)*r14*r23*r31*r44*r53 + -Fraction(1,24)*r14*r23*r31*r45*r52
  + -Fraction(1,24)*r14*r23*r32*r41*r55 + Fraction(1,6)*r14*r23*r32*r42*r54 + -Fraction(1,4)*r14*r23*r32*r43*r53 + Fraction(1,6)*r14*r23*r32*r44*r52 + -Fraction(1,24)*r14*r23*r32*r45*r51
  + Fraction(1,6)*r14*r23*r33*r41*r54 + -Fraction(1,4)*r14*r23*r33*r42*r53 + -Fraction(1,4)*r14*r23*r33*r43*r52 + Fraction(1,6)*r14*r23*r33*r44*r51 + Fraction(1,6)*r14*r23*r33*r45*r55
  + Fraction(1,6)*r14*r23*r34*r41*r53 + Fraction(1,6)*r14*r23*r34*r42*r52 + Fraction(1,6)*r14*r23*r34*r43*r51 + -Fraction(1,4)*r14*r23*r34*r44*r55 + -Fraction(1,4)*r14*r23*r34*r45*r54
  + -Fraction(1,24)*r14*r23*r35*r41*r52 + -Fraction(1,24)*r14*r23*r35*r42*r51 + Fraction(1,6)*r14*r23*r35*r43*r55 + -Fraction(1,4)*r14*r23*r35*r44*r54 + Fraction(1,6)*r14*r23*r35*r45*r53
  + Fraction(1,6)*r14*r24*r31*r41*r55 + -Fraction(1,4)*r14*r24*r31*r42*r54 + Fraction(1,6)*r14*r24*r31*r43*r53 + -Fraction(1,4)*r14*r24*r31*r44*r52 + Fraction(1,6)*r14*r24*r31*r45*r51
  + -Fraction(1,4)*r14*r24*r32*r41*r54 + Fraction(1,6)*r14*r24*r32*r42*r53 + Fraction(1,6)*r14*r24*r32*r43*r52 + -Fraction(1,4)*r14*r24*r32*r44*r51 + Fraction(1,6)*r14*r24*r32*r45*r55
  + Fraction(1,6)*r14*r24*r33*r41*r53 + Fraction(1,6)*r14*r24*r33*r42*r52 + Fraction(1,6)*r14*r24*r33*r43*r51 + -Fraction(1,4)*r14*r24*r33*r44*r55 + -Fraction(1,4)*r14*r24*r33*r45*r54
  + -Fraction(1,4)*r14*r24*r34*r41*r52 + -Fraction(1,4)*r14*r24*r34*r42*r51 + -Fraction(1,4)*r14*r24*r34*r43*r55 + r14*r24*r34*r44*r54 + -Fraction(1,4)*r14*r24*r34*r45*r53
  + Fraction(1,6)*r14*r24*r35*r41*r51 + Fraction(1,6)*r14*r24*r35*r42*r55 + -Fraction(1,4)*r14*r24*r35*r43*r54 + -Fraction(1,4)*r14*r24*r35*r44*r53 + Fraction(1,6)*r14*r24*r35*r45*r52
  + Fraction(1,6)*r14*r25*r31*r41*r54 + -Fraction(1,24)*r14*r25*r31*r42*r53 + -Fraction(1,24)*r14*r25*r31*r43*r52 + Fraction(1,6)*r14*r25*r31*r44*r51 + -Fraction(1,4)*r14*r25*r31*r45*r55
  + -Fraction(1,24)*r14*r25*r32*r41*r53 + -Fraction(1,4)*r14*r25*r32*r42*r52 + -Fraction(1,24)*r14*r25*r32*r43*r51 + Fraction(1,6)*r14*r25*r32*r44*r55 + Fraction(1,6)*r14*r25*r32*r45*r54
  + -Fraction(1,24)*r14*r25*r33*r41*r52 + -Fraction(1,24)*r14*r25*r33*r42*r51 + Fraction(1,6)*r14*r25*r33*r43*r55 + -Fraction(1,4)*r14*r25*r33*r44*r54 + Fraction(1,6)*r14*r25*r33*r45*r53
  + Fraction(1,6)*r14*r25*r34*r41*r51 + Fraction(1,6)*r14*r25*r34*r42*r55 + -Fraction(1,4)*r14*r25*r34*r43*r54 + -Fraction(1,4)*r14*r25*r34*r44*r53 + Fraction(1,6)*r14*r25*r34*r45*r52
  + -Fraction(1,4)*r14*r25*r35*r41*r55 + Fraction(1,6)*r14*r25*r35*r42*r54 + Fraction(1,6)*r14*r25*r35*r43*r53 + Fraction(1,6)*r14*r25*r35*r44*r52 + -Fraction(1,4)*r14*r25*r35*r45*r51
  + -Fraction(1,4)*r15*r21*r31*r41*r52 + -Fraction(1,4)*r15*r21*r31*r42*r51 + Fraction(1,6)*r15*r21*r31*r43*r55 + Fraction(1,6)*r15*r21*r31*r44*r54 + Fraction(1,6)*r15*r21*r31*r45*r53
  + -Fraction(1,4)*r15*r21*r32*r41*r51 + Fraction(1,6)*r15*r21*r32*r42*r55 + -Fraction(1,24)*r15*r21*r32*r43*r54 + -Fraction(1,24)*r15*r21*r32*r44*r53 + Fraction(1,6)*r15*r21*r32*r45*r52
  + Fraction(1,6)*r15*r21*r33*r41*r55 + -Fraction(1,24)*r15*r21*r33*r42*r54 + -Fraction(1,4)*r15*r21*r33*r43*r53 + -Fraction(1,24)*r15*r21*r33*r44*r52 + Fraction(1,6)*r15*r21*r33*r45*r51
  + Fraction(1,6)*r15*r21*r34*r41*r54 + -Fraction(1,24)*r15*r21*r34*r42*r53 + -Fraction(1,24)*r15*r21*r34*r43*r52 + Fraction(1,6)*r15*r21*r34*r44*r51 + -Fraction(1,4)*r15*r21*r34*r45*r55
  + Fraction(1,6)*r15*r21*r35*r41*r53 + Fraction(1,6)*r15*r21*r35*r42*r52 + Fraction(1,6)*r15*r21*r35*r43*r51 + -Fraction(1,4)*r15*r21*r35*r44*r55 + -Fraction(1,4)*r15*r21*r35*r45*r54
  + -Fraction(1,4)*r15*r22*r31*r41*r51 + Fraction(1,6)*r15*r22*r31*r42*r55 + -Fraction(1,24)*r15*r22*r31*r43*r54 + -Fraction(1,24)*r15*r22*r31*r44*r53 + Fraction(1,6)*r15*r22*r31*r45*r52
  + Fraction(1,6)*r15*r22*r32*r41*r55 + -Fraction(1,4)*r15*r22*r32*r42*r54 + Fraction(1,6)*r15*r22*r32*r43*r53 + -Fraction(1,4)*r15*r22*r32*r44*r52 + Fraction(1,6)*r15*r22*r32*r45*r51
  + -Fraction(1,24)*r15*r22*r33*r41*r54 + Fraction(1,6)*r15*r22*r33*r42*r53 + Fraction(1,6)*r15*r22*r33*r43*r52 + -Fraction(1,24)*r15*r22*r33*r44*r51 + -Fraction(1,4)*r15*r22*r33*r45*r55
  + -Fraction(1,24)*r15*r22*r34*r41*r53 + -Fraction(1,4)*r15*r22*r34*r42*r52 + -Fraction(1,24)*r15*r22*r34*r43*r51 + Fraction(1,6)*r15*r22*r34*r44*r55 + Fraction(1,6)*r15*r22*r34*r45*r54
  + Fraction(1,6)*r15*r22*r35*r41*r52 + Fraction(1,6)*r15*r22*r35*r42*r51 + -Fraction(1,4)*r15*r22*r35*r43*r55 + Fraction(1,6)*r15*r22*r35*r44*r54 + -Fraction(1,4)*r15*r22*r35*r45*r53
  + Fraction(1,6)*r15*r23*r31*r41*r55 + -Fraction(1,24)*r15*r23*r31*r42*r54 + -Fraction(1,4)*r15*r23*r31*r43*r53 + -Fraction(1,24)*r15*r23*r31*r44*r52 + Fraction(1,6)*r15*r23*r31*r45*r51
  + -Fraction(1,24)*r15*r23*r32*r41*r54 + Fraction(1,6)*r15*r23*r32*r42*r53 + Fraction(1,6)*r15*r23*r32*r43*r52 + -Fraction(1,24)*r15*r23*r32*r44*r51 + -Fraction(1,4)*r15*r23*r32*r45*r55
  + -Fraction(1,4)*r15*r23*r33*r41*r53 + Fraction(1,6)*r15*r23*r33*r42*r52 + -Fraction(1,4)*r15*r23*r33*r43*r51 + Fraction(1,6)*r15*r23*r33*r44*r55 + Fraction(1,6)*r15*r23*r33*r45*r54
  + -Fraction(1,24)*r15*r23*r34*r41*r52 + -Fraction(1,24)*r15*r23*r34*r42*r51 + Fraction(1,6)*r15*r23*r34*r43*r55 + -Fraction(1,4)*r15*r23*r34*r44*r54 + Fraction(1,6)*r15*r23*r34*r45*r53
  + Fraction(1,6)*r15*r23*r35*r41*r51 + -Fraction(1,4)*r15*r23*r35*r42*r55 + Fraction(1,6)*r15*r23*r35*r43*r54 + Fraction(1,6)*r15*r23*r35*r44*r53 + -Fraction(1,4)*r15*r23*r35*r45*r52
  + Fraction(1,6)*r15*r24*r31*r41*r54 + -Fraction(1,24)*r15*r24*r31*r42*r53 + -Fraction(1,24)*r15*r24*r31*r43*r52 + Fraction(1,6)*r15*r24*r31*r44*r51 + -Fraction(1,4)*r15*r24*r31*r45*r55
  + -Fraction(1,24)*r15*r24*r32*r41*r53 + -Fraction(1,4)*r15*r24*r32*r42*r52 + -Fraction(1,24)*r15*r24*r32*r43*r51 + Fraction(1,6)*r15*r24*r32*r44*r55 + Fraction(1,6)*r15*r24*r32*r45*r54
  + -Fraction(1,24)*r15*r24*r33*r41*r52 + -Fraction(1,24)*r15*r24*r33*r42*r51 + Fraction(1,6)*r15*r24*r33*r43*r55 + -Fraction(1,4)*r15*r24*r33*r44*r54 + Fraction(1,6)*r15*r24*r33*r45*r53
  + Fraction(1,6)*r15*r24*r34*r41*r51 + Fraction(1,6)*r15*r24*r34*r42*r55 + -Fraction(1,4)*r15*r24*r34*r43*r54 + -Fraction(1,4)*r15*r24*r34*r44*r53 + Fraction(1,6)*r15*r24*r34*r45*r52
  + -Fraction(1,4)*r15*r24*r35*r41*r55 + Fraction(1,6)*r15*r24*r35*r42*r54 + Fraction(1,6)*r15*r24*r35*r43*r53 + Fraction(1,6)*r15*r24*r35*r44*r52 + -Fraction(1,4)*r15*r24*r35*r45*r51
  + Fraction(1,6)*r15*r25*r31*r41*r53 + Fraction(1,6)*r15*r25*r31*r42*r52 + Fraction(1,6)*r15*r25*r31*r43*r51 + -Fraction(1,4)*r15*r25*r31*r44*r55 + -Fraction(1,4)*r15*r25*r31*r45*r54
  + Fraction(1,6)*r15*r25*r32*r41*r52 + Fraction(1,6)*r15*r25*r32*r42*r51 + -Fraction(1,4)*r15*r25*r32*r43*r55 + Fraction(1,6)*r15*r25*r32*r44*r54 + -Fraction(1,4)*r15*r25*r32*r45*r53
  + Fraction(1,6)*r15*r25*r33*r41*r51 + -Fraction(1,4)*r15*r25*r33*r42*r55 + Fraction(1,6)*r15*r25*r33*r43*r54 + Fraction(1,6)*r15*r25*r33*r44*r53 + -Fraction(1,4)*r15*r25*r33*r45*r52
  + -Fraction(1,4)*r15*r25*r34*r41*r55 + Fraction(1,6)*r15*r25*r34*r42*r54 + Fraction(1,6)*r15*r25*r34*r43*r53 + Fraction(1,6)*r15*r25*r34*r44*r52 + -Fraction(1,4)*r15*r25*r34*r45*r51
  + -Fraction(1,4)*r15*r25*r35*r41*r54 + -Fraction(1,4)*r15*r25*r35*r42*r53 + -Fraction(1,4)*r15*r25*r35*r43*r52 + -Fraction(1,4)*r15*r25*r35*r44*r51 + r15*r25*r35*r45*r55
  + 0 )


def ds5_3(values):
  r11,r12,r13,r14,r15,r21,r22,r23,r24,r25,r31,r32,r33,r34,r35,r41,r42,r43,r44,r45,r51,r52,r53,r54,r55 = values
  return (-r11*r21*r31*r42*r53 + -r11*r21*r31*r43*r52 + -r11*r21*r32*r41*r53 + -r11*r21*r32*r43*r51 + -r11*r21*r33*r41*r52
  + -r11*r21*r33*r42*r51 + -r11*r22*r31*r41*r53 + -r11*r22*r31*r43*r51 + -r11*r22*r32*r42*r53 + -r11*r22*r32*r43*r52
  + -r11*r22*r33*r41*r51 + -r11*r22*r33*r42*r52 + -r11*r22*r33*r43*r53 + -r11*r23*r31*r41*r52 + -r11*r23*r31*r42*r51
  + -r11*r23*r32*r41*r51 + -r11*r23*r32*r42*r52 + -r11*r23*r32*r43*r53 + -r11*r23*r33*r42*r53 + -r11*r23*r33*r43*r52
  + -r12*r21*r31*r41*r53 + -r12*r21*r31*r43*r51 + -r12*r21*r32*r42*r53 + -r12*r21*r32*r43*r52 + -r12*r21*r33*r41*r51
  + -r12*r21*r33*r42*r52 + -r12*r21*r33*r43*r53 + -r12*r22*r31*r42*r53 + -r12*r22*r31*r43*r52 + -r12*r22*r32*r41*r53
  + -r12*r22*r32*r43*r51 + -r12*r22*r33*r41*r52 + -r12*r22*r33*r42*r51 + -r12*r23*r31*r41*r51 + -r12*r23*r31*r42*r52
  + -r12*r23*r31*r43*r53 + -r12*r23*r32*r41*r52 + -r12*r23*r32*r42*r51 + -r12*r23*r33*r41*r53 + -r12*r23*r33*r43*r51
  + -r13*r21*r31*r41*r52 + -r13*r21*r31*r42*r51 + -r13*r21*r32*r41*r51 + -r13*r21*r32*r42*r52 + -r13*r21*r32*r43*r53
  + -r13*r21*r33*r42*r53 + -r13*r21*r33*r43*r52 + -r13*r22*r31*r41*r51 + -r13*r22*r31*r42*r52 + -r13*r22*r31*r43*r53
  + -r13*r22*r32*r41*r52 + -r13*r22*r32*r42*r51 + -r13*r22*r33*r41*r53 + -r13*r22*r33*r43*r51 + -r13*r23*r31*r42*r53
  + -r13*r23*r31*r43*r52 + -r13*r23*r32*r41*r53 + -r13*r23*r32*r43*r51 + -r13*r23*r33*r41*r52 + -r13*r23*r33*r42*r51
  + -4*r11*r21*r32*r42*r53 + -4*r11*r21*r32*r43*r52 + -4*r11*r21*r32*r43*r53 + -4*r11*r21*r33*r42*r52 + -4*r11*r21*r33*r42*r53
  + -4*r11*r21*r33*r43*r52 + -4*r11*r22*r31*r42*r53 + -4*r11*r22*r31*r43*r52 + -4*r11*r22*r31*r43*r53 + -4*r11*r22*r32*r41*r53
  + -4*r11*r22*r32*r43*r51 + -4*r11*r22*r32*r43*r53 + -4*r11*r22*r33*r41*r52 + -4*r11*r22*r33*r41*r53 + -4*r11*r22*r33*r42*r51
  + -4*r11*r22*r33*r42*r53 + -4*r11*r22*r33*r43*r51 + -4*r11*r22*r33*r43*r52 + -4*r11*r23*r31*r42*r52 + -4*r11*r23*r31*r42*r53
  + -4*r11*r23*r31*r43*r52 + -4*r11*r23*r32*r41*r52 + -4*r11*r23*r32*r41*r53 + -4*r11*r23*r32*r42*r51 + -4*r11*r23*r32*r42*r53
  + -4*r11*r23*r32*r43*r51 + -4*r11*r23*r32*r43*r52 + -4*r11*r23*r33*r41*r52 + -4*r11*r23*r33*r42*r51 + -4*r11*r23*r33*r42*r52
  + -4*r12*r21*r31*r42*r53 + -4*r12*r21*r31*r43*r52 + -4*r12*r21*r31*r43*r53 + -4*r12*r21*r32*r41*r53 + -4*r12*r21*r32*r43*r51
  + -4*r12*r21*r32*r43*r53 + -4*r12*r21*r33*r41*r52 + -4*r12*r21*r33*r41*r53 + -4*r12*r21*r33*r42*r51 + -4*r12*r21*r33*r42*r53
  + -4*r12*r21*r33*r43*r51 + -4*r12*r21*r33*r43*r52 + -4*r12*r22*r31*r41*r53 + -4*r12*r22*r31*r43*r51 + -4*r12*r22*r31*r43*r53
  + -4*r12*r22*r33*r41*r51 + -4*r12*r22*r33*r41*r53 + -4*r12*r22*r33*r43*r51 + -4*r12*r23*r31*r41*r52 + -4*r12*r23*r31*r41*r53
  + -4*r12*r23*r31*r42*r51 + -4*r12*r23*r31*r42*r53 + -4*r12*r23*r31*r43*r51 + -4*r12*r23*r31*r43*r52 + -4*r12*r23*r32*r41*r51
  + -4*r12*r23*r32*r41*r53 + -4*r12*r23*r32*r43*r51 + -4*r12*r23*r33*r41*r51 + -4*r12*r23*r33*r41*r52 + -4*r12*r23*r33*r42*r51
  + -4*r13*r21*r31*r42*r52 + -4*r13*r21*r31*r42*r53 + -4*r13*r21*r31*r43*r52 + -4*r13*r21*r32*r41*r52 + -4*r13*r21*r32*r41*r53
  + -4*r13*r21*r32*r42*r51 + -4*r13*r21*r32*r42*r53 + -4*r13*r21*r32*r43*r51 + -4*r13*r21*r32*r43*r52 + -4*r13*r21*r33*r41*r52
  + -4*r13*r21*r33*r42*r51 + -4*r13*r21*r33*r42*r52 + -4*r13*r22*r31*r41*r52 + -4*r13*r22*r31*r41*r53 + -4*r13*r22*r31*r42*r51
  + -4*r13*r22*r31*r42*r53 + -4*r13*r22*r31*r43*r51 + -4*r13*r22*r31*r43*r52 + -4*r13*r22*r32*r41*r51 + -4*r13*r22*r32*r41*r53
  + -4*r13*r22*r32*r43*r51 + -4*r13*r22*r33*r41*r51 + -4*r13*r22*r33*r41*r52 + -4*r13*r22*r33*r42*r51 + -4*r13*r23*r31*r41*r52
  + -4*r13*r23*r31*r42*r51 + -4*r13*r23*r31*r42*r52 + -4*r13*r23*r32*r41*r51 + -4*r13*r23*r32*r41*r52 + -4*r13*r23*r32*r42*r51
  + 2*r11*r21*r31*r42*r52 + 2*r11*r21*r31*r43*r53 + 2*r11*r21*r32*r41*r52 + 2*r11*r21*r32*r42*r51 + 2*r11*r21*r32*r42*r52
  + 2*r11*r21*r33*r41*r53 + 2*r11*r21*r33*r43*r51 + 2*r11*r21*r33*r43*r53 + 2*r11*r22*r31*r41*r52 + 2*r11*r22*r31*r42*r51
  + 2*r11*r22*r31*r42*r52 + 2*r11*r22*r32*r41*r51 + 2*r11*r22*r32*r41*r52 + 2*r11*r22*r32*r42*r51 + 2*r11*r23*r31*r41*r53
  + 2*r11*r23*r31*r43*r51 + 2*r11*r23*r31*r43*r53 + 2*r11*r23*r33*r41*r51 + 2*r11*r23*r33*r41*r53 + 2*r11*r23*r33*r43*r51
  + 2*r12*r21*r31*r41*r52 + 2*r12*r21*r31*r42*r51 + 2*r12*r21*r31*r42*r52 + 2*r12*r21*r32*r41*r51 + 2*r12*r21*r32*r41*r52
  + 2*r12*r21*r32*r42*r51 + 2*r12*r22*r31*r41*r51 + 2*r12*r22*r31*r41*r52 + 2*r12*r22*r31*r42*r51 + 2*r12*r22*r32*r41*r51
  + 2*r12*r22*r32*r43*r53 + 2*r12*r22*r33*r42*r53 + 2*r12*r22*r33*r43*r52 + 2*r12*r22*r33*r43*r53 + 2*r12*r23*r32*r42*r53
  + 2*r12*r23*r32*r43*r52 + 2*r12*r23*r32*r43*r53 + 2*r12*r23*r33*r42*r52 + 2*r12*r23*r33*r42*r53 + 2*r12*r23*r33*r43*r52
  + 2*r13*r21*r31*r41*r53 + 2*r13*r21*r31*r43*r51 + 2*r13*r21*r31*r43*r53 + 2*r13*r21*r33*r41*r51 + 2*r13*r21*r33*r41*r53
  + 2*r13*r21*r33*r43*r51 + 2*r13*r22*r32*r42*r53 + 2*r13*r22*r32*r43*r52 + 2*r13*r22*r32*r43*r53 + 2*r13*r22*r33*r42*r52
  + 2*r13*r22*r33*r42*r53 + 2*r13*r22*r33*r43*r52 + 2*r13*r23*r31*r41*r51 + 2*r13*r23*r31*r41*r53 + 2*r13*r23*r31*r43*r51
  + 2*r13*r23*r32*r42*r52 + 2*r13*r23*r32*r42*r53 + 2*r13*r23*r32*r43*r52 + 2*r13*r23*r33*r41*r51 + 2*r13*r23*r33*r42*r52
  + 8*r11*r21*r31*r41*r52 + 8*r11*r21*r31*r41*r53 + 8*r11*r21*r31*r42*r51 + 8*r11*r21*r31*r43*r51 + 8*r11*r21*r32*r41*r51
  + 8*r11*r21*r33*r41*r51 + 8*r11*r22*r31*r41*r51 + 8*r11*r22*r32*r42*r52 + 8*r11*r23*r31*r41*r51 + 8*r11*r23*r33*r43*r53
  + 8*r12*r21*r31*r41*r51 + 8*r12*r21*r32*r42*r52 + 8*r12*r22*r31*r42*r52 + 8*r12*r22*r32*r41*r52 + 8*r12*r22*r32*r42*r51
  + 8*r12*r22*r32*r42*r53 + 8*r12*r22*r32*r43*r52 + 8*r12*r22*r33*r42*r52 + 8*r12*r23*r32*r42*r52 + 8*r12*r23*r33*r43*r53
  + 8*r13*r21*r31*r41*r51 + 8*r13*r21*r33*r43*r53 + 8*r13*r22*r32*r42*r52 + 8*r13*r22*r33*r43*r53 + 8*r13*r23*r31*r43*r53
  + 8*r13*r23*r32*r43*r53 + 8*r13*r23*r33*r41*r53 + 8*r13*r23*r33*r42*r53 + 8*r13*r23*r33*r43*r51 + 8*r13*r23*r33*r43*r52
  + 20*r11*r21*r31*r41*r51 + 20*r12*r22*r32*r42*r52 + 20*r13*r23*r33*r43*r53 + 20*r14*r24*r34*r44*r54 + 20*r15*r25*r35*r45*r55
  + 0 )


# print header:
print("graph\td\tedges\tboost:\t0\t1\t2\t3\t||\t0\t1\t2\t3\n----------------------------------------------------------------")

boost = 1
#boost = 10
#boost = 100

values = []  
count = 1
results = []
with open(filename,'r') as f:
  for line in f:
    line = line.strip()
    if len(line) == 0:
#      values = [int(i) for i in values]
#      values = [float(i) for i in values]
      values = [ Fraction(int(i),1) for i in values]
#      print("values:",values)
      d = len(row)                          # breaks if matrix is not square. Shouldn't be a problem for us.
      edges = sum(values)
      boost_values_1 = [i + 1 for i in values ]
      boost_values_2 = [i + 2 for i in values ]
      boost_values_3 = [i + 3 for i in values ]
      ds55_0 = ds5(values)*24                # P^5 test
      ds55_1 = ds5(boost_values_1)*24
      ds55_2 = ds5(boost_values_2)*24
      ds55_3 = ds5(boost_values_3)*24

      ds53_0 = ds5_3(values)               # P^3 test
      ds53_1 = ds5_3(boost_values_1)
      ds53_2 = ds5_3(boost_values_2)
      ds53_3 = ds5_3(boost_values_3)

#      print("%s: d: %s edges: %s ds5: %s" % (count,d,edges,the_ds5))
#      print("%s\t%s\t%s\t\t%s\t%s\t%s\t%s" % (count,d,edges,ds5_0,ds5_1,ds5_2,ds5_3))
      print("%s\t%s\t%s\t\t%s\t%s\t%s\t%s\t\t%s\t%s\t%s\t%s" % (count,d,edges,ds55_0,ds55_1,ds55_2,ds55_3,ds53_0,ds53_1,ds53_2,ds53_3))
#      print("ds5:",the_ds5)
      count += 1
#      sys.exit(0)
      values = []  
      results.append(int(ds55_1))
      continue
    row = line.split(' ')
    values += row

print("\n\nresults:",sorted(results))

