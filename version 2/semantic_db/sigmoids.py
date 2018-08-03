#######################################################################
# the semantic-db sigmoids
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018
# Update: 14/3/2018
# Copyright: GPLv3
#
# a collection of 'sigmoids'
# they only change the coefficients of kets, not the labels
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
def threshold_filter(x, t):
    if x < t:
        return 0
    else:
        return x


def not_threshold_filter(x, t):
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


def pos(x):  # what about an "abs" sigmoid?
    if x <= 0:
        return 0
    else:
        return x


def sigmoid_abs(x):
    return abs(x)


def max_filter(x, t):
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
def mult(x, t):
    return x * t


# this is another type of "Goldilock function"
# the in-range sigmoid:
def sigmoid_in_range(x, a, b):
    if a <= x and x <= b:
        return x
    else:
        return 0


def invert(x):
    if x == 0:
        return 0
    else:
        return 1 / x


def set_to(x, t):
    return t


def subtraction_invert(x, t):
    return t - x


def log(x, t=None):
    if x <= 0:
        return 0
    if t is None:
        return math.log(x)  # default is base e, ie natural logarithm
    return math.log(x, t)  # choose another base


def log_1(x, t=None):
    if x <= 0:  # maybe tweak this, given that it is log(1 + x), not log(x)
        return 0
    if t is None:
        return math.log(1 + x)  # default is base e, ie natural logarithm
    return math.log(1 + x, t)  # choose another base


def square(x):
    return x * x


def sqrt(x):
    return math.sqrt(x)


def floor(x):
    return math.floor(x)


def ceiling(x):
    return math.ceil(x)


def increment(x):
    return x + 1


def decrement(x):
    return x - 1
