#!/usr/bin/env python

#######################################################################
# the semantic-db function-operator file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 27/5/2018
# Copyright: GPLv3
#
# A collection of functions that apply to kets, superpositions and sequences.
#
#######################################################################

import sys
import random
import copy
import string
import re

# from the_semantic_db_code import *
# from the_semantic_db_processor import *
from semantic_db.code import *
from semantic_db.sigmoids import *


# the range function
# eg: show_range(|year: 1982>, |year: 1985>)
# should spit out: |year: 1982> + |year: 1983> + |year: 1984> + |year: 1985>
# maybe later a sequence version too/instead.
# not sure what to do if the passed in kets have values other than 1.
# later I might need a date range too.
# eg: 2/11/2009 .. 7/12/2009
# probably give it it's own function though.
# if we want -1 steps, use superposition.reverse()

# bug if start or finish are superpositions!
# fix it.
# introduced X.ket(). Breaks if X is a string!
# Nope. Now using X.the_label()
#
def old_show_range(start, finish, step="n: 1"):
    # tweak so full kets are optional, and labels are sufficient:
    start_label = start if type(start) == str else start.the_label()
    finish_label = finish if type(finish) == str else finish.the_label()
    step_label = step if type(step) == str else step.the_label()

    #  print("step_label:",step_label)

    cat1, v1 = extract_category_value(start_label)
    cat2, v2 = extract_category_value(finish_label)
    cat3, v3 = extract_category_value(step_label)
    #  print("v3:",v3)

    if cat1 != cat2 or not v1.isdigit() or not v2.isdigit() or not v3.isdigit():  # maybe check v1, v2 for float instead of int?
        return ket("")
    label = ""
    if len(cat1) > 0:
        label = cat1 + ": "  # perhaps extract_category_value should append the ": " bit??
    result = superposition()  # probably not.
    for k in range(int(v1), int(v2) + 1, int(v3)):
        result += ket(label + str(k))
    return result


# 23/4/2014: need float range:


# test for set membership of |x> in |X>
# this is simple enough, that we probably don't even need this function. Just do it inline.
# Probably a little clearer to do it inline anyway, instead of the one step of indirection.
# 24/1/2015: what about using X.get_value(x.label)?
def set_mbr(x, X, t=1):
    return X.apply_bra(x) >= t


# the intersection function.
# if you set foo = min, then it is a generalization of Boolean set intersection.
# if you set foo = max, then it is a generalization of Boolean set union.
# if you set foo = sum, then it is a literal sum.
# if you set foo = mult, then it is a multiplication of the list elements.
# possibly other useful values of foo too.
# maybe we can do a complement function? if value1 == 0 and value2 != 0, then return value2
# maybe make the label compare case insensitive. Probably not though.
#
# 9/5/2014: I think this could do with some optimization!
# I think ordered-dict and standard dict could probably improve the big-O here by quite a bit!
#
def first_intersection_fn(foo, one, two):
    # so that also works with kets:
    #  if type(one) == ket:
    #    one = superposition() + one
    #  if type(two) == ket:
    #    two = superposition() + two

    # fix bug, where simm(X,X) != 1 if X contains duplicates.
    # eg, if X was defined using spell_word() is one example.
    # the superposition() + one, should neatly fix this bug! Provided we have auto-collapse on addition.
    one = superposition() + one
    two = superposition() + two

    result = superposition()
    labels = []
    for x in one.data:
        if x.label not in labels:
            labels.append(x.label)
    for x in two.data:
        if x.label not in labels:
            labels.append(x.label)
    #  print(labels)
    for label in labels:
        v1 = 0
        for x in one.data:
            if x.label == label:  # instead of direct equality testing,
                v1 = x.value  # maybe use: labels_match(x.label,label) ??
                break  # probably not.
        v2 = 0
        for x in two.data:
            if x.label == label:
                v2 = x.value
                break
        value = foo(v1, v2)
        result += ket(label, value)
    return result


from collections import OrderedDict


# 4/6/2014 update: Let's try and optimize this puppy!
# BTW, the long term plan is to convert the back-end of the superposition class to ordered dictionaries.
# The problem is I have broken the "hide details in the class" abstraction everywhere, so would take a lot of work to change!
# The other part is we would need a general way to iterate over a superposition.
# Good link: http://www.voidspace.org.uk/python/odict.html
# Heh. Not sure if this is faster or slower!
# But it hints at how the improved superposition class should be written.
def second_intersection_fn(foo, one, two):
    result = superposition()

    one_dict = OrderedDict()  # fast_sp_fix: tweak this once fast_sp is switched in.
    for elt in one:  # we should be able to really tidy this beast up.
        one_dict[elt.label] = elt.value

    two_dict = OrderedDict()
    for elt in two:
        two_dict[elt.label] = elt.value

    merged = OrderedDict()
    merged.update(one_dict)
    merged.update(two_dict)
    #  print(merged)

    for key in merged:
        v1 = 0
        if key in one_dict:
            v1 = one_dict[key]
        v2 = 0
        if key in two_dict:
            v2 = two_dict[key]

        value = foo(v1, v2)
        #    result += ket(label,value)
        #    result.data.append(ket(key,value))
        result.add(key, value)
    return result


# 24/1/2015: let's write the intersection_fn version that uses the fast_sp as a backend.
# one and two must be fast_superpositions!
# need to test this .....
# anyway, looks good. Should be much faster.
def fast_sp_intersection_fn(foo, one, two):
    r = fast_superposition()
    merged = OrderedDict()
    merged.update(one.odict)  # yeah, breaking class abstractions again!
    merged.update(two.odict)  # maybe I should just do: one + two

    for key in merged:
        v1 = one.get_value(key)
        v2 = two.get_value(key)
        value = foo(v1, v2)
        r += ket(key, value)
    return r


# still can't use this in the console, since the context needs to be passed in too.
# the train-of-though function, or perhaps a better name is "stream of conciousness"
def train_of_thought(context, x, n):
    if type(n) != int:
        try:
            cat, v = extract_category_value(n.the_label())
            n = int(v)
        except:
            return superposition()  # return an empty superposition.

    print("context:", context.name)
    print("x:", x.display())
    print("n:", n)
    X = x.pick_elt()
    print("|X>:", X.display())
    print()
    result = superposition()

    for k in range(n):
        op = X.apply_op(context, "supported-ops").pick_elt()  # |op> => pick-elt supported-ops |X>
        #    print("op:",op.display())
        X = X.apply_op(context, op).pick_elt()  # |X> => pick-elt apply(|op>,|X>)
        #    result += X                            # this version adds repeated elements
        result.data.append(X)  # this version preserves order
        #    print("|X>:",a_ket.display())
        print(X.display())
    return result  # return a record of the train-of-thought


# 28/7/2014:
# Let's finally implement console train of thought.
# train-of-thought[n] some-superposition
# eg: train-of-thought[20] |colour: red>
# First up, I want to try it on this data set: http://semantic-db.org/next-gen/train_of_thought.py
# OK. In early testing seems to work just fine.
#
# where n is an int.
def console_train_of_thought(one, context, n):
    try:
        n = int(n)
    except:
        return ket("", 0)

    print("context:", context.name)
    print("one:", one)
    print("n:", n)
    X = one.pick_elt()
    print("|X>:", X)
    print()
    result = superposition()

    for k in range(n):
        op = X.apply_op(context, "supported-ops").pick_elt()  # |op> => pick-elt supported-ops |X>
        X = X.apply_op(context, op).pick_elt()  # |X> => pick-elt apply(|op>,|X>)
        result.data.append(X)
        print(X.display())
    return result  # return a record of the train-of-thought




# note the almost identical structure to read_text().
# This is not a coincidence, and hints that this structure is very common
# and operates at various levels in the brain.
def spell_word(one):
    label = one.label if type(one) == ket else one

    cat, word = extract_category_value(label)
    if cat != "word":
        return ket("")

    result = superposition()  # later when we finally implement sequence, use sequence() here.
    result.data = [ket("letter: " + c) for c in word]
    return result


# 29/1/14, let's put in a collapse_read_text() here, eg, for the frequency of words thing.
def collapse_read_text(one):
    label = one.label if type(one) == ket else one

    cat, text = extract_category_value(label)
    if cat != "text":
        return ket("", 0)
    #  print("text:",text)
    # don't keep case version:
    text = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    # keep case for now:
    #  text = text.translate(str.maketrans("","",string.punctuation)).split()

    result = superposition()
    for w in text:
        result += ket("word: " + w)
    return result


# 24/1/2015: I have no idea the point for these next two functions!
# I guess I wrote them when I was a newb.
# this is a general idea (have ket code mapped to handle superpositions too).
# So:
def old_ket_superposition(fn, x):
    if type(x) == ket:
        return fn(x)
    if type(x) == superposition:
        result = superposition()
        for v in x.data:
            result += fn(v)
        return result


# try again:
def ket_superposition(fn, x):
    result = superposition()
    if type(x) == ket:
        result += fn(x)
    if type(x) == superposition:
        for v in x.data:
            result += fn(v)
    return result


# 24/1/2015: this this is weird and boring!
# Now, some weird maths thing.
# A kind of "number is near", based on digits.
# Yeah, hard-wired to base 10 for now.
# eg: 70 is near: 80,60 and 71,79
def near_number(x):
    value = x.value if type(x) == ket else 1
    x_label = x.label if type(x) == ket else x

    cat, v = extract_category_value(x_label)
    if cat != "number":
        return ket(x_label, value)
    try:
        n = int(v)  # test for valid int. Don't actually use n.
    except:
        return ket(x_label, value)

    digits = [int(c) for c in v]
    result = superposition()
    for k, d in enumerate(digits):
        d1 = (d + 1) % 10
        d2 = (d - 1) % 10

        tmp = copy.copy(digits)
        tmp[k] = d1
        s = ''.join(str(n) for n in tmp)
        result += ket("number: " + s, value)

        tmp = copy.copy(digits)
        tmp[k] = d2
        s = ''.join(str(n) for n in tmp)
        result += ket("number: " + s, value)
    return result


# the handle superpositions version:
def near_numbers(x):
    return ket_superposition(near_number, x)


# update: google found this: http://mathworld.wolfram.com/SumofPrimeFactors.html
# This is a thing I call a strange int.
# Say r has prime factorisation:
# r = p1^n1 * p2^n2 * p3^n3 * p4^n4 * ...
# Then strange_int(r) = p1*n1 + p2*n2 + p3*n3 + p4*n4 + ...
# This is just one of a range of results from doing the simple mapping:
# a^b to a*b
# c*b to c + b
#
# A couple of things to mention:
# 1) strange_int(p) == p, when p is prime, or p == 4.
# 2) If p is neither prime or 4, then strange_int(p) < p
# 3) Hence, there exists a finite positive integer k such that
# strange-int^k |x> == |p>, where p is a prime (or 4).
# and by (1), strange-int^(k+1) |x> == |p>
def strange_int(x):
    value = x.value if type(x) == ket else 1
    x_label = x.label if type(x) == ket else x

    cat, v = extract_category_value(x_label)
    if cat != "number":
        return ket(x_label, value)
    try:
        n = int(v)
    except:
        return ket(x_label, value)
    if n <= 1:
        return ket(x_label, value)

    return ket("number: " + str(sum(primes(n))))


# find the strange-int-prime.
# ie, |p> such that strange-int^k |x> == |p>
def strange_int_prime(x):
    value = x.value if type(x) == ket else 1
    x_label = x.label if type(x) == ket else x

    cat, v = extract_category_value(x_label)
    if cat != "number":
        return ket(x_label, value)
    try:
        n = int(v)
    except:
        return ket(x_label, value)
    if n <= 1:
        return ket(x_label, value)

    next = sum(primes(n))
    while n != next:
        n = next
        next = sum(primes(n))

    return ket("number: " + str(n))


# find the strange-int-depth.
# ie, smallest k such that strange-int^k |x> == |p>
def strange_int_depth(x):
    value = x.value if type(x) == ket else 1
    x_label = x.label if type(x) == ket else x

    cat, v = extract_category_value(x_label)
    if cat != "number":
        return ket(x_label, value)
    try:
        n = int(v)
    except:
        return ket(x_label, value)
    if n <= 1:
        return ket(x_label, value)

    k = 0
    next = sum(primes(n))
    while n != next:
        n = next
        next = sum(primes(n))
        k += 1

    return ket("number: " + str(k))


# find the strange-int-delta
# ie, |x> - strange-int |x>
def strange_int_delta(x):
    value = x.value if type(x) == ket else 1
    x_label = x.label if type(x) == ket else x

    cat, v = extract_category_value(x_label)
    if cat != "number":
        return ket(x_label, value)
    try:
        n = int(v)
    except:
        return ket(x_label, value)
    if n <= 1:
        return ket(x_label, value)

    r = n - sum(primes(n))
    return ket("number: " + str(r))


# find the strange-int-list
# ie, |x> + strange-int |x> + strange-int^2 |x> + ...
def strange_int_list(x):
    value = x.value if type(x) == ket else 1
    x_label = x.label if type(x) == ket else x

    cat, v = extract_category_value(x_label)
    if cat != "number":
        return ket(x_label, value)
    try:
        n = int(v)
    except:
        return ket(x_label, value)
    if n <= 1:
        return ket(x_label, value)

    result = superposition()
    result += ket("number: " + str(n))
    #  result += ket(str(n))
    next = sum(primes(n))
    while n != next:
        n = next
        next = sum(primes(n))
        result += ket("number: " + str(n))
    #    result += ket(str(n))

    return result


import math


# the frequency class equation:
# see: http://en.wikipedia.org/wiki/Frequency_list
def frequency_class(e, X):
    X = X.drop()  # filter out elements <= 0
    smallest = X.find_min_coeff()
    largest = X.find_max_coeff()
    f = X.find_value(e)

    print("e:", e)
    print("largest:", largest)
    print("value:", f)

    # need a check in here that f > 0.
    # Indeed, largest > 0 too.

    if largest <= 0:
        return 1

    if f <= 0:  # what happens if smallest == 0?? X.drop() means largest == 0 too, hence already returned 1.
        return math.floor(0.5 - math.log(smallest / largest, 2)) + 1

    return math.floor(0.5 - math.log(f / largest, 2))


# the normalized frequency class equation.
# result is in [0,1]
# 1 for exact match, 0 for not in set.
#
# works great! Indeed, it is a bit like a fuzzy set membership function.
# eg, if all coeffs in X are equal, it gives Boolean 1 for membership, and 0 for non-membership.
# and if the coeffs are not all equal, then it has fuzzier properties.
#
# 25/7/2014 note: Hrmm... I wonder if we can tweak this.
# Currently you only get 20 odd different classes using the frequency class equation.
# Is there a version that gives more graduations?
# Though in practice this is usually not an issue.
# It will almost certainly be of form foo(current/largest)
#
# e is a ket, X is a superposition
# for best effect X should be a frequency list
def normed_frequency_class(e, X):
    e = e.ket()  # make sure e is a ket, not a superposition, else X.find_value(e) bugs out.
    X = X.drop()  # drop elements with coeff <= 0
    smallest = X.find_min_coeff()  # return the min coeff in X as float
    largest = X.find_max_coeff()  # return the max coeff in X as float
    f = X.find_value(e)  # return the value of ket e in superposition X as float

    if largest <= 0 or f <= 0:  # otherwise the math.log() blows up!
        return 0

    fc_max = math.floor(0.5 - math.log(smallest / largest,
                                       2)) + 1  # NB: the + 1 is important, else the smallest element in X gets reported as not in set.
    #  print("fc_max: ",fc_max)
    #  print("max log:",math.log(smallest/largest,2))
    #  print("max val:",0.5 - math.log(smallest/largest,2))
    #  print("ret log:",math.log(f/largest,2))
    #  print("ret val:",0.5 - math.log(f/largest,2))
    return 1 - math.floor(0.5 - math.log(f / largest, 2)) / fc_max


# OK. I think this is the time sink with my MtT.
# If we assume X[1] is the largest, and X[-1] is smallest,
# then we don't need find_min and find_max.
# I didn't time it, but it felt no faster....
def faster_normed_frequency_class(e, X):
    X = X.drop()
    #  smallest = X.find_min_coeff()
    #  largest = X.find_max_coeff()
    smallest = X.select_elt(-1).value  # bug if X is empty??
    largest = X.select_elt(1).value

    f = X.find_value(e)

    if largest <= 0 or f <= 0:
        return 0

    fc_max = math.floor(0.5 - math.log(smallest / largest, 2)) + 1
    return 1 - math.floor(0.5 - math.log(f / largest, 2)) / fc_max


# 19/3/2015:
# e is a ket, X is a superposition
# for best effect X should be a frequency list
def ket_normed_frequency_class(e, X):
    result = normed_frequency_class(e, X)
    return ket("nfc", result)


# describe this later ...
# Heh. Structure wise, this is remarkably similar to pattern_recognition().
# BTW, perhaps S should be a superposition instead of a list?
#
# I think this should be tidied up and most probably put in new_context next to pattern-recognition.
# Also fix the hardwiring of "list".
#
# This is now deprecated, but leaving it here because a couple of my scripts.
# See new_context.map_to_topic(e,"list") for the improved version.
def map_to_topic(context, e, S):
    result = superposition()
    for X in S:
        #    print("X:",X)
        data = context.recall("list", X)
        value = normed_frequency_class(e, data)
        #    value = faster_normed_frequency_class(e,data)  # doesn't seem any faster.
        #    result += ket(X.label,value)
        result.data.append(ket(X.label, value))

    #  return result.normalize(100)
    # NB: .normalize(100) is a key component of this function.
    # Half the magic is in nfc(), the other half in normalize(100).
    return result.drop().normalize(100).coeff_sort()


# let's see if we can do some simple algebra in BKO.
# a|x> + b|y> => a|x> + b|y>
def algebra_add(one, two):
    return one + two


# 10/4/2014 new:
def algebra_subtract(one, two):
    return delete3(one, two)


def old_algebra_mult(one, two, Abelian=True):
    one = superposition() + one  # hack so one and two are definitely sp, not ket
    two = superposition() + two

    result = superposition()
    for x in one.data:
        for y in two.data:
            print("x*y", x, "*", y)
            labels = x.label.split('*') + y.label.split('*')
            if Abelian:
                labels.sort()
            label = "*".join(labels)
            result += ket(label, x.value * y.value)
    return result


# maps ket -> ket
# to-number 3|x> == 3|x>
# to-number |number: 7.2> == 7.2| >  # NB: the space in the ket label.
# to-number 2|number: 3> == 6| >     # We can't use just |> because it is dropped all over the place!
# to-number 8|number: text> == 0| >  # so the maths eqn: 3a + 7
# to-number |3.7> == 3.7| >          # in my notation is 3|a> + 7| >
# to-number 3|5> == 15| >
def old_category_number_to_number(one):  # find better name!
    one = one.ket()
    cat, value = extract_category_value(one.label)
    if cat != 'number':
        return one
    try:
        n = float(value)
    except:
        return ket(" ", 0)
    return ket(" ", one.value * n)


# 26/3/2016:
# so that algebra() can handle rationals too.
# copied from here:
# http://stackoverflow.com/questions/575925/how-to-convert-rational-and-decimal-number-strings-to-floats-in-python
#
def parse_float_string(x):
    parts = x.split('/', 1)
    if len(parts) == 1:
        return float(x)
    elif len(parts) == 2:
        return float(parts[0]) / float(parts[1])
    else:
        raise ValueError


# assume one is a sp or ket:
def category_number_to_number(one):  # find better name!
    cat, value = extract_category_value(one.label)
    try:
        #    n = float(value)
        n = parse_float_string(value)
    except:
        if cat == 'number':  # not 100% want to keep these two lines
            return ket(" ")
        return one
    return ket(" ", one.value * n)


# a|x> * b|y> => a*b |x*y>
#
def algebra_mult(one, two, Abelian=True):
    one = one.to_sp()
    two = two.to_sp()

    r = superposition()
    for x in one:
        x = category_number_to_number(x)
        for y in two:
            y = category_number_to_number(y)
            print("x*y", x, "*", y)
            labels = [L for L in x.label.split('*') + y.label.split('*') if L.strip() != '']
            if Abelian:
                labels.sort()
            label = "*".join(labels)
            if label == '':  # we can't have ket("",value), since it will be dropped.
                label = " "
            r += ket(label, x.value * y.value)
    return r


# (a|x> + b|y>)^|n>
# eg: (|a> + |b> + |c>)^|2> = |a*a> + 2.000|a*b> + 2.000|a*c> + |b*b> + 2.000|b*c> + |c*c>
def old_algebra_power(one, two):
    one = superposition() + one
    two_label = two.ket().label
    null, power = extract_category_value(two_label)
    try:
        n = int(power)
    except:
        return ket("", 0)

    if n <= 0:
        return ket("1")

    result = one
    for k in range(n - 1):
        result = algebra_mult(result, one)
    return result


def algebra_power(one, two, Abelian=True):
    one = superposition() + one
    two = category_number_to_number(two)
    try:
        n = int(two.value)
    except:
        return ket(" ", 0)

    if n <= 0:
        return ket(" ", 1)

    result = one
    for k in range(n - 1):
        result = algebra_mult(result, one, Abelian)
    return result


# implement basic algebra:
def algebra(one, operator, two, Abelian=True):
    op_label = operator if type(operator) == str else operator.to_sp().label
    null, op = extract_category_value(op_label)

    if op not in ['+', '-', '*', '^']:
        return ket()

    if op == '+':  # drop_zero() added so that terms with coeff 0 are dropped.
        return algebra_add(one, two).drop()  # Abelian option here too?
    elif op == '-':
        return algebra_subtract(one, two).drop()  # ditto.
    elif op == '*':
        return algebra_mult(one, two, Abelian).drop()
    elif op == '^':
        return algebra_power(one, two, Abelian).drop()
    else:
        return ket()


# 2/2/2015: finally wire in non Abelian algebra:
def non_Abelian_algebra(one, operator, two):
    return algebra(one, operator, two, False)


# simple complex number mult:
def complex_algebra_mult(one, two):
    one = superposition() + one  # hack so one and two are definitely sp, not ket
    two = superposition() + two

    result = superposition()
    for x in one.data:
        for y in two.data:
            if x.label == 'real' and y.label == 'real':
                result += ket("real", x.value * y.value)

            if x.label == 'real' and y.label == 'imag':
                result += ket("imag", x.value * y.value)

            if x.label == 'imag' and y.label == 'real':
                result += ket("imag", x.value * y.value)

            if x.label == 'imag' and y.label == 'imag':
                result += ket("real", -1 * x.value * y.value)
    return result


# convert decimal number to base b.
# eg, b = 2, we have:
# |10> => |2> + |8>
# |7> => |1> + |2> + |4>
#
# number, base need to be kets. category_number_to_number() should take care of that.
def decimal_to_base(number, base):
    r = int(category_number_to_number(number).value)
    b = int(category_number_to_number(base).value)
    #  print("r:",r)
    #  print("b:",b)
    current_base = 1
    result = superposition()
    while r > 0:
        rem = r % b
        r //= b
        result += ket(str(current_base), rem)
        current_base *= b
    return result


# here is a fun one.
# just a test function really for stored_rules().
def shout(one):
    string = (one if type(one) == str else one.label).upper()
    print(string)
    return ket(string)
    # return ket("",0)


# the discrimination function.
# returns the difference between largest coeff, and second largest coeff.
# discrim (90|x> + 55|y>)
# should return 35| >
#
# I now think this should be moved to ket/sp classes.
# Done. This is now deprecated.
# Alternatively, remove from ket/sp and put in "sp_fn_table" -- see the processor.
def discrimination(one):
    result = 0
    if type(one) == ket:
        result = one.value
    elif len(one.data) == 0:
        result = 0
    elif len(one.data) == 1:
        result = one.data[0].value
    else:
        one = one.coeff_sort()
        result = one.data[0].value - one.data[1].value
    return ket(" ", result)








# we need this for read_letters, and read_words, maybe other things in the future too.
def extract_letters(x):
    if x.startswith("letter: "):
        return x[8:]
    if x.startswith("word: "):
        return x[6:]
    return ""


# maybe this should be shifted closer to spell and read, but here will do for now.
# I'm looking at the inverse of spell really.
# so read-letters spell |word: frog> => |word: frog>
#
# Currently "one" must be a superposition.
# We need to fix this at some stage! Fixed.
def read_letters(one):
    w = "".join(extract_letters(x.label) for x in one)
    if len(w) == 0:
        return ket("", 0)
    return ket("word: " + w)


# a full implementation of this would do capitilization and i to I, and a bunch of other stuff!
# maybe I should put extract_letters() outside of these two functions?
#
# some examples from the console:
# sa: read-words (|word: fish> + |word: dog>)
# |text: fish dog>
#
# sa: read-words (|letter: I> + |word: don't> + |word: give> + |letter: a> + |word: fish>)
# |text: I don't give a fish>
#
# sa: read-words (read |text: I don't give a fish>)
# |text: i dont give a fish>
#
# Fixed, so read-words doesn't have to be in the table of functions with 1 parameter.
# It is now in apply_sp_fn table.
# so now can do:
# sa: read-words read |text: I don't give a fish>
# |text: i dont give a fish>
# ie, we don't need to wrap the read |text: ... in brackets.
def read_words(one):
    w = " ".join(extract_letters(x.label) for x in one)
    if len(w) == 0:
        return ket("", 0)
    return ket("text: " + w)


# merge labels
# merge-labels (|fish> + |soup>) returns |fishsoup>
def merge_labels(one):
    w = "".join(x.label for x in one)
    return ket(w)


# a thing called active read.
# returns results from read_text, and word.apply_op(context,"")
def first_active_read_text(context, one):
    result = superposition()
    for x in read_text(one).data:
        #   result += x
        result += x.apply_op(context, "")
    return result


#  def pattern_recognition(self,pattern,op="pattern",t=0)

def second_active_read_text(context, one):
    result = superposition()
    data = read_text(one).data
    for k in range(len(data) - 1):
        y1 = data[k]
        print("y1:", y1)
        tmp1 = context.pattern_recognition(y1, "")
        print("tmp1:", tmp1)
        result += tmp1.drop_below(1)  # ie, looking for exact match.

        y2 = data[k] + data[k + 1]
        print("y2:", y2)
        tmp2 = context.pattern_recognition(y2, "")
        print("tmp2:", tmp2)
        result += tmp2.drop_below(1)  # again, drop_below(1) is for an exact match.
    y1 = data[-1]
    print("y1:", y1)
    tmp1 = context.pattern_recognition(y1, "")
    print("tmp1:", tmp1)
    result += tmp1.drop_below(1)

    return result


def active_read_text(context, one):
    result = superposition()
    data = read_text(one).data
    for k in range(len(data)):
        y1 = data[k]
        print("y1:", y1)
        tmp1 = context.pattern_recognition(y1, "")
        print("tmp1:", tmp1)
        result += tmp1.drop_below(1)  # ie, looking for exact match.

        if k < len(data) - 1:
            y2 = data[k] + data[k + 1]
            print("y2:", y2)
            tmp2 = context.pattern_recognition(y2, "")
            print("tmp2:", tmp2)
            result += tmp2.drop_below(1)  # again, drop_below(1) is for an exact match.

    return result


# hrmmm is one ket or sp?
# It is whatever type that read_text() can handle.
# quick look there says: ket or string.
def silent_active_read_text(context, one, pattern=""):
    result = superposition()
    data = read_text(one).data
    for k in range(len(data)):
        y1 = data[k]
        result += context.pattern_recognition(y1, pattern).drop_below(0)  # hrmm.. maybe we don't need drop_below(1)?
        # instead of deleting the drop_below, I just
        if k < len(data) - 1:  # inactivated it by setting to 0.
            y2 = data[k] + data[k + 1]  # this line corresponds to my "buffer" idea. Explain later!
            result += context.pattern_recognition(y2, pattern).drop_below(0)

    return result


# try and implement my active buffer idea:
# the idea is that as you input data you try and pattern match it against what you know.
# it is a generalisation of the active_read() idea.
# And I imagine it will be very useful indeed. But that is for later.
#
# fn needs to return a superposition, else code breaks.
# N is the number of elements in the buffer.
# Usually <= 7, I'm guessing (based on short term memory with 7 +-2 items), though that depends on how low or high level we are working at. Lower generally implies larger N.
# pattern is the pattern label we are looking for.
# t is the drop-below threshold.
#
# We need to test this beast!
def old_active_buffer(context, fn, one, N, pattern="", t=0):
    result = superposition()
    data = fn(one).data
    for k in range(len(data)):
        for n in range(N):
            if k < len(data) - n:
                y = superposition()
                y.data = data[k:k + n + 1]
                result += context.pattern_recognition(y, pattern).drop_below(t)
    return result


# added 27/6/2014:
# active-buffer[N,t] some-superposition             -- uses "" as the default pattern.
# active-buffer[N,t,pattern] some-superposition     -- uses your chosen pattern (we can't use "" as the pattern, due to broken parser!)
# eg: active-buffer[3,0] read |text: I want french waffles>
# where:
# N is an int                                       -- the size of the active buffer
# t is a float                                      -- the drop below threshold
# pattern is a string                               -- the pattern we are using
#
# Maybe a version that preserves currency?
# Just using currency = one.count_sum(), then return result.normalize(currency)
def old_console_active_buffer(one, context, parameters):  # one is the passed in superposition
    try:
        N, t, pattern = parameters.split(',')
        N = int(N)
        t = float(t)
    except:
        try:
            N, t = parameters.split(',')
            N = int(N)
            t = float(t)
            pattern = ""
        except:
            return ket("", 0)

    one = superposition() + one  # make sure one is a superposition, not a ket.
    result = superposition()  # Need cleaner way to handle the ket/sp problem, really.
    data = one.data  # Maybe a unified iterator in the background?
    for k in range(len(data)):  # so x in one: instead of x in one.data:
        for n in range(N):  # though here we do need the list, not just an iterator.
            if k < len(data) - n:
                y = superposition()
                y.data = data[k:k + n + 1]  # this is the bit you could call the buffer.
                result += context.pattern_recognition(y, pattern).drop_below(t)
    return result





# Now I need its brother, number-to-words.
# eg:
# number-to-words |number: 7> => |text: seven>
# number-to-words |number: 35> => |text: thirty five>
# number-to-words |number: 137> => |text: one hundred and thirty seven>
# number-to-words |number: 8,921> => |text: eight thousand, nine hundred and twenty one>
# number-to-words |number: 54,329> => |text: fifty four thousand, three hundred and twenty nine>
# number-to-words |number: 673,421> => |text: six hundred and seventy three thousand, four hundred and twenty one>
# number-to-words |number: 3,896,520> => |text: three million, eight hundred and ninety six thousand, five hundred and twenty>
#
# I think something here should do the job:
# http://stackoverflow.com/questions/8982163/how-do-i-tell-python-to-convert-integers-into-words
def number_to_words(one):
    result = superposition()
    # details ...


# 24/9/2015:
# union[op] (|x> + |y> + |z>)  -- maybe needs a better name. I'm not sure the English counterpart.
#
def operator_union(one, context, op):
    if len(one) == 0:
        return ket("", 0)
    for sp in one:
        r = sp.apply_op(context, op)
        break
    for sp in one:
        tmp = sp.apply_op(context, op)
        r = union(r,
                  tmp)  # we could probably make this a general function, and then pass in intersection(), union() etc.
    return r  # ie, cast pair-fn(sp1,sp2) into fn(sp1,sp2,...,spn)


def absolute_difference_fn(x, y):
    return abs(x - y)


# general to specific.
# The idea is you take an average of some object.
# Let's say the slashdot-to-sp I've recently been playing with.
# So: hashes |ave-slashdot> => hashes |slashdot-1> + hashes |slashdot-2> + hashes |slashdot-3> + hashes |slashdot-4>
# Then, given |ave-slashdot>, find the bits that are unique to |slashdot-n>
# Maybe something like:
# hashes |slashdot: 5> => general-to-specific(hashes |ave-slashdot>, hashes |slashdot-5>)
# NB: in the process we made a sub-category. And hashes|slashdot: 5> will look vastly different from hashes|slashdot-5>
#
# Update: probably works better if we have threshold filters in there before learning the average:
# roughly: hashes |ave-slashdot> => TF[t1] hashes |slashdot-1> + TF[t2] hashes |slashdot-2> + TF[t3] hashes |slashdot-3> + TF[t4] hashes |slashdot-4>
# Indeed, it is probably actually this:
# hashes |ave-slashdot> => TF[t5] (TF[t1] hashes |slashdot-1> + TF[t2] hashes |slashdot-2> + TF[t3] hashes |slashdot-3> + TF[t4] hashes |slashdot-4> )
# Not currently sure how to choose the values for tk
#
# 10/5/2015: work on images shows that abs() is not he best choice. pos(x) is much better!
#
def general_to_specific(average, specific):
    return intersection_fn(absolute_difference_fn, average.normalize(),
                           specific.normalize())  # NB: .normalize() is vital for this to work!
    # return intersection_fn(absolute_difference_fn,average,specific)







# convert the labels in a superposition to a pretty-print vector
def old_sp_to_vect(one):
    max_len = 0
    for x in one.data:
        max_len = max(max_len, len(x.label))
    for x in one.data:
        print("[ " + x.label.ljust(max_len) + " ]")


def sp_to_vect(one):
    if one.count() <= 1:
        vect = one.the_label()
    else:
        vect = "\n".join(x.label for x in one.data)
    return paste_columns([vect], '[ ', '', ' ]')


def sp_to_list(one):  # what happens if one is a ket? Fixed, I think.
    if one.count() <= 1:
        return one.the_label()
    return "\n".join(x.label for x in one.data)


# make 0.000 coeffs prettier!
def old_coeff_to_str(x):
    if x == 0:
        return "0"
    else:
        return str("%.2f" % x)  # this means if we want to change precission, we only need to change it here.
        # return str("%.0f" % x)                                         # this means if we want to change precission, we only need to change it here.
        # return str("%.2f" % (100 - x))                                 # we use this version when graphing heat-maps of simm matrices, since 0 is black, 100 is white.


def coeff_to_str(x):  # yeah, ugly code. Too scared of my code that depends on this, to do it the tidy way.
    return float_to_int(x, 2)


def sp_coeffs_to_list(one):  # what happens if one is a ket? Fixed, I think.
    if one.count() <= 1:
        return coeff_to_str(one.the_value())
    return "\n".join(coeff_to_str(x.value) for x in one.data)


# these two functions help to pretty-print tables, and matrices in particular:
def normalize_column_return_list(s, n):
    lines = (s.split('\n') + [''] * n)[:n]
    max_len = max(len(x) for x in lines)
    return [x.ljust(max_len) for x in lines]


def paste_columns(data, pre='', sep=' ', post=''):
    if len(data) == 0:
        return ""
    columns = len(data)
    rows = max(s.count('\n') + 1 for s in data)
    r = [normalize_column_return_list(s, rows) for s in data]
    return "\n".join(pre + sep.join(r[j][k] for j in range(columns)) + post for k in range(rows))


# first version of code to spit out a pretty printed matrix given BKO rules:
def first_matrix(context, op):
    one = context.relevant_kets(op).ket_sort()  # one is the list of kets that will be on the right hand side.
    # usefully, relevant_kets() always returns a superposition.
    if one.count() == 0:  # if one is empty, return the identity ket.
        return ket("", 0)

    two = superposition()  # two is the list of kets that will be on the left hand side.
    for elt in one.data:
        sp = elt.apply_op(context, op)
        two = union(two, sp)
    two = two.ket_sort()

    empty = two.multiply(0)  # empty is the two list, with all coeffs set to 0

    matrix_columns = []  # convert to list-comprehension?
    for elt in one.data:
        sp = (elt.apply_op(context, op) + empty).ket_sort()  # we add "empty" so the column has all the elements.
        matrix_columns.append(sp_coeffs_to_list(sp))

    x = sp_to_vect(one)
    y = sp_to_vect(two)
    M = paste_columns(matrix_columns, '[  ', '  ', '  ]')
    matrix = paste_columns([y, '=', M, x])
    print(matrix)
    # print("\n" + paste_columns(matrix_columns,'',' ',''))
    return ket("matrix")  # Just here so it retuns a ket of some sort. Has no meaning, really.


# code to return a single matrix, and the left-hand superposition:
# one must be a superposition
# op is a literal op
# NB: the difference between this one, and the one below is it uses: x.apply_op(context,op)
# the "new" one uses x.merged_apply_op(context,ops)
def first_single_matrix(one, context, op):
    one = one.apply_sigmoid(set_to, 1)
    two = superposition()  # two is the list of kets that will be on the left hand side.
    for elt in one.data:  # heh. using one.data kind of breaks the superposition abstract interface idea.
        sp = elt.apply_op(context, op)
        two = union(two, sp)
    two = two.ket_sort().multiply(0)  # merged two, and empty into the same thing.
    matrix_columns = [sp_coeffs_to_list((elt.apply_op(context, op) + two).ket_sort()) for elt in one.data]
    M = paste_columns(matrix_columns, '[  ', '  ', '  ]')  # M is the matrix
    return two, M


# second version of code to spit out a matrix:
# seems to be correct.
def matrix(context, op):
    one = context.relevant_kets(op).ket_sort()  # one is the list of kets that will be on the right hand side.
    # usefully, relevant_kets() always returns a superposition.
    if one.count() == 0:  # if one is empty, return the identity ket.
        return ket("", 0)

    two, M = single_matrix(one, context, op)

    x = sp_to_vect(one)
    y = sp_to_vect(two)
    matrix = paste_columns([y, '=', M, x])
    print(matrix)
    return ket("matrix")  # Just here so it retuns a ket of some sort. Has no meaning, really.


# third version.
# this one I want to handle multiple ops at once, and then chain the matrices.
# eg: matrix[M2,M1]
# or: matrix[friends,friends]  -- ie, matrix of second-order friends
def multi_matrix(context, ops):
    ops = ops.split(',')[::-1]
    print("ops:", ops)

    one = context.relevant_kets(ops[0]).ket_sort()  # one is the list of kets that will be on the right hand side.
    # usefully, relevant_kets() always returns a superposition.
    if one.count() == 0:  # if one is empty, return the identity ket.
        return ket("", 0)

    two, M = single_matrix(one, context, ops[0])
    matrices = [M]
    for op in ops[1:]:
        two, M = single_matrix(two, context, op)
        matrices.append(M)
    x = sp_to_vect(one)
    y = sp_to_vect(two)
    line = [y, '='] + matrices[::-1] + [x]
    matrix = paste_columns(line)
    print(matrix)

    # code to save the matrix (useful for big ones, too hard to cut and paste from the console)
    print("saving to: saved-matrix.txt")
    file = open("saved-matrix.txt", 'w')
    file.write("sa: matrix[" + ",".join(ops[::-1]) + "]\n")
    file.write(matrix)
    file.close()

    return ket("matrix")


# uses x.merged_apply_op(context,ops) instead of x.apply_op(context,op)
def single_matrix(one, context, op):
    one = one.apply_sigmoid(set_to, 1)
    two = superposition()  # two is the list of kets that will be on the left hand side.
    for elt in one.data:  # heh. using one.data kind of breaks the superposition abstract interface idea.
        sp = elt.merged_apply_op(context, op)
        two = union(two, sp)
    two = two.ket_sort().multiply(0)  # merged two, and empty into the same thing.
    matrix_columns = [sp_coeffs_to_list((elt.merged_apply_op(context, op) + two).ket_sort()) for elt in one.data]
    M = paste_columns(matrix_columns, '[  ', '  ', '  ]')  # M is the matrix
    return two, M


# see if we can tidy this up later!
# Heh. Doesn't need tidying up. This deprecates matrix(context,ops)
def merged_multi_matrix(context, ops):
    ops = ops.replace(',', ' ')  # we have to do this, as the current parser can't handle: matrix[op3 op2 op1],
    # but can handle matrix[op3,op2,op1]. It would be nice to eventually fix this!
    # Indeed, even op-sequence: matrix[op2 op1^k] kind of thing.
    one = context.relevant_kets(
        ops.split()[-1]).ket_sort()  # one is the list of kets that will be on the right hand side.
    # usefully, relevant_kets() always returns a superposition.
    if one.count() == 0:  # if one is empty, return the identity ket.
        return ket("", 0)

    two, M = single_matrix(one, context, ops)

    x = sp_to_vect(one)
    y = sp_to_vect(two)
    matrix = paste_columns([y, '=', M, x])
    print(matrix)
    return ket("matrix")  # Just here so it retuns a ket of some sort. Has no meaning, really.


def merged_naked_matrix(context, ops):
    ops = ops.replace(',', ' ')
    one = context.relevant_kets(
        ops.split()[-1]).ket_sort()  # one is the list of kets that will be on the right hand side.
    # usefully, relevant_kets() always returns a superposition.
    if one.count() == 0:  # if one is empty, return the identity ket.
        return ket("", 0)

    two, M = single_matrix(one, context, ops)
    print(M)
    return ket("matrix")


# 5/6/2014 update: Let's write vector[op] (|x> + |y>)
# Same as merged-matrix, just you pass in the superpositions of interest, instead of using relevant_kets.
# May need a better name.
def first_vector(one, context, ops):
    one = superposition() + one  # just make sure one is a sp.
    if one.count() == 0:
        return ket("", 0)
    ops = ops.replace(',', ' ')
    two, M = single_matrix(one, context, ops)
    x = sp_to_vect(one)
    y = sp_to_vect(two)
    matrix = paste_columns([y, '=', M, x])
    print(matrix)
    return ket("matrix")


def vector(one, context, ops):
    ops = ops.replace(',', ' ')
    one = superposition() + one  # just make sure one is a sp.
    if one.count() == 0:  # this happens a) if the default ket is |>, or the passed in ket is |>
        # sa: id
        # 0.000|>
        # sa: vector[op]
        # or:
        # sa: vector[op] |>
        one = context.relevant_kets(ops.split()[-1]).ket_sort()
        if one.count() == 0:
            return ket("", 0)

    two, M = single_matrix(one, context, ops)
    x = sp_to_vect(one)
    y = sp_to_vect(two)
    matrix = paste_columns([y, '=', M, x])
    print(matrix)
    return ket("matrix")


# 23/5/2014:
# let's implement a map function (since we can't have multi-line for loops, this will have to do!)
# eg: map[op] (|x> + |y>)
# runs:
# op |x> => op |_self>
# op |y> => op |_self>
# ie, it converts function operators (op on the right hand side), in to literal operators (on the left hand side)
# eg: map[fib] (|10> + |11>)
# eg: map[child] (|x> + |0> + |1> + |00> + |01> + |10> + |11>)
# or indirectly:
# map[op] "" |list>
# one is a ket/sp
# op is a string
#
# tweak, now we can also do: map[fn,result] "" |list>  -- ie, we can now specify the destination, in this case "result"
def map(one, context, op):
    try:
        fn, op = op.split(',')
    except:
        fn = op
    print("fn:", fn)
    print("op:", op)

    for x in one:  # what if x has x.value != 1? x.apply_op handles that.
        context.learn(op, x, x.apply_op(context, fn))  # currently fn must be of form: fn |*> #=> bah.
    return ket("map")  # Would sometimes be useful to be able to use a full function here.
    # Something we probably need to take up with .apply_op()
    # As then (presumably) it could work for similar[op] |ket> too.
    # Code change for this is probably hard, since would need pieces from the processor file.


# 4/5/2015:
# a new version of map. This one puts results in a temporary store while doing the calculatoin, then copies the result back after.
# Basically to stop the code eating its own tail. eg, mapping a grid to a grid, you need a temporary grid.
def copy_map(one, context, op):
    try:
        fn, op = op.split(',')
    except:
        fn = op
    print("fn:", fn)
    print("op:", op)
    op_tmp = op + "-pDBUKObhYk"  # thanks: https://www.random.org/strings/
    print("op-tmp:", op_tmp)

    for x in one:
        context.learn(op - tmp, x, x.apply_op(context, fn))  # store results on temporary grid
    #  for x in one:
    #    context.learn(op,x,x.apply_op(context,op-tmp))
    #  context.copy_op(op_tmp,op)        # maybe ... still need some thinking time. What about context.mv_op(op_tmp,op)?
    #  context.delete_op(op-tmp)         # need to implement this function.
    context.move_op(op_tmp, op)
    return ket("copy-map")


# 28/5/2014:
# working towards a BKO version of the categorize code.
# first, the equivalent of metric_mbr, using simm.
#
# one is a superposition
# op is a string
# x is a ket
# thresh is a float
def simm_mbr(context, op, x, thresh, one):
    f = x.apply_op(context, op)
    for elt in one:
        g = elt.apply_op(context, op)
        if silent_simm(f, g) >= thresh:
            return True
    return False


# categorize[op,thresh,destination]
def categorize(context, parameters):
    try:
        op, thresh, destination = parameters.split(',')
        thresh = float(thresh)
        destination = ket(destination)
    except:
        return ket("", 0)

    one = context.relevant_kets(op)  # one is a superposition
    print("one:", one)
    out_list = []  # out_list will be a list of superpositions.
    for x in one:  # x is of course a ket
        n = 0
        del_list = []  # del_list will be a list of integers.
        for i in range(len(out_list)):
            if simm_mbr(context, op, x, thresh, out_list[i]):
                if n == 0:
                    out_list[i] += x
                    idx = i
                    n = 1
                else:
                    out_list[idx] += out_list[i]
                    del_list.append(i)
        if n == 0:
            out_list.append(
                superposition() + x)  # we use "superposition() + x" instead of just "x" so out_list is always a list of superpositions, not kets.
        else:
            out_list = [x for index, x in enumerate(out_list) if index not in del_list]

    for k, sp in enumerate(out_list):
        print("sp:", sp)
        context.learn("category-" + str(k), destination, sp)
    return ket("categorize")


import datetime


# day of the week function:
# day-of-the-week |date: 2014/06/3> => |day: Tuesday>
# Code from here: http://stackoverflow.com/questions/9847213/which-day-of-week-given-a-date-python
# Heh. Python makes this super easy!
def day_of_the_week(one):
    cat, value = extract_category_value(one.the_label())
    if cat.split(': ')[-1] != "date":
        return ket("", 0)

    # 5/2/2015: tidy it up:
    try:
        year, month, day = (int(x) for x in value.split('/'))
    except:
        try:
            year, month, day = (int(x) for x in value.split('-'))
        except:
            return ket("", 0)
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    the_day = day_list[datetime.date(year, month, day).weekday()]
    return ket("day: " + the_day)


# maybe do a version using pretty print columns code.
def print_pixels(one, context,
                 op="pixels"):  # heh. Can't currently think of a way to do this without needing op fed in.
    data = one.apply_op(context, op)  # Since only compound table handles fn's needing context.
    # But this is a weird case where we don't really want anything other than "pixels"
    I = int(apply_value(one.apply_op(context, "dim-1")).value)
    J = int(apply_value(one.apply_op(context, "dim-2")).value)

    print("I:", I)
    print("J:", J)

    for j in range(1, J + 1):
        for i in range(1, I + 1):
            elt = ket("pixel: " + str(j) + ": " + str(i))  # not sure what happens if we want other than pixel:
            c = int(data.find_value(elt))
            # c = '#'
            if c == 0:
                c = ' '
            print(c, end='')
        print()
    return ket("pixels")


# long sp. Prints out the long_display form of a sp.
def long_display(one):
    print(one.long_display())
    return one


# split |word1 word2 word3 word4> => |word1> + |word2> + |word3> + |word4>
# saves typing in some cases. eg, find-topic[words] split |word1 word2 word3>
# assumes one is a ket
def old_split_ket(one):
    result = superposition()
    result.data = [ket(w, one.the_value()) for w in
                   one.the_label().split()]  # Buggy? eg, anything with duplicates. eg: split |a a b a b a a c a>
    return result  # superficially it seems to work, because elsewhere tidies up our mess (probably the extract_compound_superposition code)


def split_ket(one):
    r = superposition()
    for key, value in one.items():
        for label in key.split():
            r.add(label, value)
    return r


# 29/8/2015:
# clean-split |word1 word2 word3> => |word1> + |word2> + |word3>
# essentially the same as split_ket, except it sends punctuation to ' '
#
# one is a ket
def clean_split_ket(one):
    result = superposition()
    text = re.sub('[.,!?$\"-]', ' ', one.label)
    text = text.replace('\\n', ' ').replace('\\r', ' ')  # should this line be before the re.sub() line?
    for word in text.split():
        result += ket(word, one.value)
    return result


# quick play here: http://semantic-db.org/the-semantic-agent/play_with_list_to_sp.py
def list_to_sp(s, list):
    result = superposition()
    result.data = [ket(s + str(k), v) for k, v in enumerate(list)]
    return result


def sp_to_list(sp):
    return [x.value for x in
            sp.ket_sort().data]  # NB: the ket_sort(). Even if we shuffle the sp, we get the same list back.


# currently broken, since it gets fed a list of kets, rather than one superposition.
# I don't currently know where/how to fix that!
# I presume I need a new table in the processor.
# 7/8/2014: heh. I don't understand what I was trying to do here!
def sp_as_list(sp):  # I think natural sort is buggy when you have negative values, eg |x: -10>.
    sp = superposition() + sp  # cast any kets to superposition
    print([x.value for x in
           sp.ket_sort().data])  # NB: the ket_sort(). Even if we shuffle the sp, we get the same list back.
    return sp


# 7/8/2014, let's write a sp-propagate function.
# Takes an initial superposition, then takes an operator, and applies it repeatedly.
# Then display this all as a matrix, maybe something we can plot in gnuplot.
# First need this:
def sp_coeffs_to_column(one):
    one = superposition() + one  # cast kets to sp.

    def to_str(n):
        if n == 0:
            return "0"
            # return " "
        else:
            return str("%.2f" % n)
            # return "1"

    return "\n".join(to_str(x.value) for x in one.data)


# usage: sp-propagate[op,k] "" |list>
# op is an operator, k is the number of iterations.
def sp_propagate(one, context, parameters):
    try:
        op, k = parameters.split(",")
        k = int(k)
    except:
        return ket("", 0)

    matrix = []
    r = one
    empty = r.apply_sigmoid(set_to, 0)
    for idx in range(k):
        matrix.append(sp_coeffs_to_column(
            (r + empty).ket_sort()))  # making use of adding an sp of all 0's does not change the meaning
        r = r.apply_op(context, op)
    print(paste_columns(matrix, '', ' ', ''))
    return ket("matrix")


# 10/11/2014:
# apply()
# eg:
# apply(|op: age> + |op: friends>,|Fred>)
# maps to:
# age |Fred> + friends |Fred>
# a more common usage:
# star |*> #=> apply(supported-ops|_self>,|_self>)
def old_apply_sp(context, one, two):
    print("one:", one)
    print("two:", two)
    r = superposition()
    for x in one:  # yeah, about time we defined iterators or something for superpositions! Done!
        print("x.label:", x.label)
        print("x.value:", x.value)
        if x.label.startswith("op: "):
            op = x.label[4:]
            r += two.apply_op(context, op).multiply(x.value)
    return r


# 17/1/2015:
# clone(|x>,|y>)
# copies rules from |x> and applies them to |y>
# eg: age |x> => |31>
# mother |x> => |Jane>
# After clone(|x>,|y>) we have:
# age |y> = |31>
# mother |x> = |Jane>
# not super sure the use of this yet though :)
# quick test, and it works!
def clone_ket(context, one, two):
    one = one.ket()  # one needs to be a ket. two can be ket or sp.
    operators = context.recall("supported-ops", one)
    for op_ket in operators:
        op = op_ket.label[4:]
        rule = context.recall(op, one)  # we can't use one.apply_op(C,op) as that activates any stored rules.
        for x in two:
            context.learn(op, x, rule)
    return ket("clone")


# 10/11/2014:
# expand-hierarchy (not that I can spell that word!)
# expand-hierarchy |a: b: c: d>
# maps to:
# |a> + |a: b> + |a: b: c> + |a: b: c: d>
#
# example usage:
# intersection(expand-hierarchy |a: b: c: d: e: f>, expand-hierarchy |a: b: c: x: y>)
#
# assumes "one" is a ket.
def expand_hierarchy(one):
    r = superposition()
    L = []
    for x in one.label.split(": "):
        L.append(x)
        r += ket(": ".join(L))
    return r.multiply(one.value)


# 10/11/2014:
# chars |some text>
# maps to:
# | > + 2|e> + |m> + |o> + |s> + 2|t> + |x>
#
# example usage:
# chars-fn |*> #=> chars |_self>
# map[chars-fn,chars] "" |list>
# similar[chars] |George>                      # NB: similar[op] bugs out if "op |*> #=> ... " is defined.
#                                              # something to do with the stored-rule vs similar[].
# assumes "one" is a ket.                      # related: maybe make similar work with ops other than literal ops?
# Probably we can tidy it up a bit ... Nah. Looks about right. # probably a lot of work though!
def chars(one):
    char_list = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:-*"
    L = [0] * len(char_list)
    for c in one.label:
        k = char_list.find(c)
        if k >= 0:
            L[k] += 1
    r = superposition()
    for k, count in enumerate(L):
        r += ket(char_list[k], count)
    return r.drop().multiply(one.value)





# LOL. Seems we already have the equiv of push-float and pop-float at the start of this file!
# Anyway, I think these are better versions.
# push-float
# examples:
# push-float 3| > == |3>
# push-float 3|x> == |x: 3>
# push-float 3.2|x: y > == |x: y: 3.2> (not sure the number of decimal places to keep, initially all of them)
#
# 5/2/2015: hrmm... maybe push-float n|> == |> for any n?
#
def push_float(one):
    if one.label == "":
        return ket("", 0)
    value = one.value
    label = one.label.rstrip()
    if float(value).is_integer():
        value = str(int(value))
    else:
        value = str(value)
    if label == "":
        return ket(value)
    return ket(label + ": " + value)


# pop-float
# examples:
# pop-float |3.2> == 3.2| >
# pop-float 5|7> == 35| >
# pop-float |x: 2> == 2|x>
# pop-float 5.1|x: y: 2> == 10.2|x: y>
# pop-float |x: y> == |x: y>
def pop_float(one):
    coeff = one.value
    label = one.label
    try:
        value = float(label)
        label = " "
    except:
        try:
            label, value = label.rsplit(": ", 1)
            value = float(value)
        except:
            return one
    return ket(label, coeff * value)


# cat-depth
# return the depth of the categories:
# cat-depth |> == |number: 0>
# cat-depth |x> == |number: 1>
# cat-depth |x: y> == |number: 2>
def category_depth(one):
    #  return ket("number: " + str(len(one.label.split(": "))))
    if one.label == "":
        return ket("number: 0")
    return ket("number: " + str(one.label.count(": ") + 1))


# from PIL import Image
# 12/1/2015:
# load-image[lenna.png] |my image>
#
# Notes: I'm reading here: http://pillow.readthedocs.org/en/latest/handbook/tutorial.html
# I'm not sure there is a win from working with images in BKO, compared to straight python!!
#
def load_image(one, context, filename):
    try:
        im = Image.open(filename)
        width = im.size[0]
        height = im.size[1]
        for x in one:  # why do we do this? Why do the same thing for all the elements in a superposition?
            context.learn("filename", x, "file: " + filename)
            context.learn("width", x, str(width))
            context.learn("height", x, str(height))
            pixel_list = superposition()
            for h in range(height):
                for w in range(width):
                    pixel = ket(x.label + ": pixel: " + str(h) + ": " + str(w))
                    if w > 0:
                        context.learn("left", pixel, ket(x.label + ": pixel: " + str(h) + ": " + str(w - 1)))
                    if w < (width - 1):
                        context.learn("right", pixel, ket(x.label + ": pixel: " + str(h) + ": " + str(w + 1)))
                    if h > 0:
                        context.learn("up", pixel, ket(x.label + ": pixel: " + str(h - 1) + ": " + str(w)))
                    if h < (height - 1):
                        context.learn("down", pixel, ket(x.label + ": pixel: " + str(h + 1) + ": " + str(w)))

                    # way too slow! Unusably so.
                    #          context.add_learn("pixel-list",x,pixel)                    # NB: this line is seriously slow!
                    pixel_list.data.append(pixel)
                    r, g, b = im.getpixel((w, h))[:3]  # assumes image is RGB or RGBA
                    #          context.learn("r-pixel-value-self",pixel,pixel.multiply(r))# and promptly ignores the A if RGBA
                    #          context.learn("g-pixel-value-self",pixel,pixel.multiply(g))
                    #          context.learn("b-pixel-value-self",pixel,pixel.multiply(b))
                    context.learn("R", pixel, pixel.multiply(r))  # and promptly ignores the A if RGBA
                    context.learn("G", pixel, pixel.multiply(g))
                    context.learn("B", pixel, pixel.multiply(b))
            context.learn("pixel-list", x, pixel_list)
        # show the image. later will comment this out.
        im.show()
        return ket("load-image")
    except:
        return ket("failed to load image")  # not yet sure which of these two I want to return.
        # return ket("")


# 20/4/2015: finally returned to try and finish this beasty!
# save-image[lenna-diff.png] |my image>
#
# one is a ket! Not sure why load_image() needed superpositions!
def save_image(one, context, filename):
    try:
        x = one.ket()
        width = int(context.recall("width", x).the_label())
        height = int(context.recall("height", x).the_label())
        size = (width, height)
        im = Image.new('RGB', size)
        image_pixels = im.load()
        for h in range(height):
            for w in range(width):
                pixel = ket(x.label + ": pixel: " + str(h) + ": " + str(w))
                r = int(context.recall("R", pixel).the_value())
                g = int(context.recall("G", pixel).the_value())
                b = int(context.recall("B", pixel).the_value())
                print("R:", r, "G:", g, "B:", b)
                image_pixels[w, h] = (r, g, b)
        im.save(filename)
        return ket("save-image")
    except:
        return ket("failed to save image")


# 4/5/2015:
# show-image |my image>
#
# one is a ket! Not sure why load_image() needed superpositions!
def show_image(one, context):
    try:
        x = one.ket()
        width = int(context.recall("width", x).the_label())
        height = int(context.recall("height", x).the_label())
        size = (width, height)
        im = Image.new('RGB', size)
        image_pixels = im.load()
        for h in range(height):
            for w in range(width):
                pixel = ket(x.label + ": pixel: " + str(h) + ": " + str(w))
                r = int(context.recall("R", pixel).the_value())
                g = int(context.recall("G", pixel).the_value())
                b = int(context.recall("B", pixel).the_value())
                print("R:", r, "G:", g, "B:", b)
                image_pixels[w, h] = (r, g, b)
        im.show()
        return ket("show-image")
    except:
        return ket("failed to show image")


# 10/5/2015:
# OK. Let's write a new version of image-load.
# this time, so all the data is in one single superposition. This makes a few things easier, and a bunch of things neater.
# eg, currently: "load-image[lenna.png] |Lenna>" modifies |Lenna>, kind of breaks the non-mutablility thing really.
# Plan this time is: |Lenna> => image-load[lenna.png] |>
# for this to work we have to drop things like:
# filename |Lenna> => |file: 220px-Lenna.png>
# width |Lenna> => |220>                  # plan is for these to be auto-calculated. Also means we can create an n*m image using just: 0|image: pixel: R: n: m>
# height |Lenna> => |220>
# And:
# left |Lenna: pixel: 219: 215> => |Lenna: pixel: 219: 214>
# right |Lenna: pixel: 219: 215> => |Lenna: pixel: 219: 216>
# up |Lenna: pixel: 219: 215> => |Lenna: pixel: 218: 215>
#
def working_image_load(filename):
    # not sure what speed impact separating this out has:
    def pixel_ket(type, h, w, r):
        if type == '':
            return ket("pixel: " + str(h) + ": " + str(w), r)
        else:
            return ket("pixel: " + type + ": " + str(h) + ": " + str(w), r)

    try:
        im = Image.open(filename)
        width = im.size[0]
        height = im.size[1]
        pixel_list = superposition()
        for h in range(height):
            tmp_list = []
            for w in range(width):
                r, g, b = im.getpixel((w, h))[:3]  # assumes image is RGB or RGBA

                #        pixel_r = ket("pixel: R: " + str(h) + ": " + str(w),r)
                #        pixel_g = ket("pixel: G: " + str(h) + ": " + str(w),g)
                #        pixel_b = ket("pixel: B: " + str(h) + ": " + str(w),b)

                #        print("R:",pixel_r)
                #        print("G:",pixel_g)
                #        print("B:",pixel_b)

                # tmp_list version:
                #        tmp_list.append(pixel_r)
                #        tmp_list.append(pixel_g)
                #        tmp_list.append(pixel_b)
                tmp_list.append(pixel_ket("R", h, w, r))
                tmp_list.append(pixel_ket("G", h, w, g))
                tmp_list.append(pixel_ket("B", h, w, b))

            pixel_list.data += tmp_list

        # show the image:
        im.show()
        return pixel_list
    except:
        return ket("failed to load image")

    # still slow at 20 min to load up 220px-lenna.png


# not sure what else to try
# I wonder if fast_sp would be faster.
# though we have the "fast_sp doesn't work here" bug!
#
def improved_image_load(filename):
    def pixel_ket(type, h, w, r):
        if type == '':
            return ket("pixel: " + str(h) + ": " + str(w), r)
        else:
            return ket("pixel: " + type + ": " + str(h) + ": " + str(w), r)

    try:
        im = Image.open(filename)
        width = im.size[0]
        height = im.size[1]
        pixel_list = superposition()
        #    for h in range(height):
        #      tmp_list_r = [pixel_ket("R",h,w,im.getpixel((w,h))[0]) for w in range(width)]
        #      tmp_list_g = [pixel_ket("G",h,w,im.getpixel((w,h))[1]) for w in range(width)]
        #      tmp_list_b = [pixel_ket("B",h,w,im.getpixel((w,h))[2]) for w in range(width)]
        #      pixel_list.data += tmp_list_r + tmp_list_g + tmp_list_b
        #    tmp_list_r = [ pixel_ket("R",h,w,im.getpixel((w,h))[0]) for w in range(width) for h in range(height) ]
        #    tmp_list_g = [ pixel_ket("G",h,w,im.getpixel((w,h))[1]) for w in range(width) for h in range(height) ]
        #    tmp_list_b = [ pixel_ket("B",h,w,im.getpixel((w,h))[2]) for w in range(width) for h in range(height) ]
        # im.load() version:
        pixels = im.load()
        tmp_list_r = [pixel_ket("R", h, w, pixels[w, h][0]) for w in range(width) for h in range(height)]
        tmp_list_g = [pixel_ket("G", h, w, pixels[w, h][1]) for w in range(width) for h in range(height)]
        tmp_list_b = [pixel_ket("B", h, w, pixels[w, h][2]) for w in range(width) for h in range(height)]

        pixel_list.data += tmp_list_r + tmp_list_g + tmp_list_b

        # show the image:
        im.show()
        return pixel_list
    except:
        return ket("failed to load image")

    # 11/5/2015:


# image-save[lenna.png] "" |lenna>
# image-show "" |lenna>
#
# one is a superposition
#
def improved_image_save_show(one, filename=""):
    def extract_ket_details(one):  # one is a ket
        try:
            value = one.value
            pixel_type, x, y = one.label.split(': ')[1:]
            return pixel_type, x, y, int(value)
        except:
            return  # not sure what to do here!

    def extract_pixel_value(pixel_dict, pixel_type, h, w):
        try:
            value = pixel_dict[pixel_type + ":" + str(h) + ":" + str(w)]
        except:
            value = 0
        return value

    try:
        pixel_dict = {}
        max_x = 0
        max_y = 0
        for x in one:
            print("x:", x)
            pixel_type, x, y, value = extract_ket_details(x)
            if int(x) > max_x:
                max_x = int(x)
            if int(y) > max_y:
                max_y = int(y)
            pixel_dict[pixel_type + ":" + x + ":" + y] = value
        print("finished for loop")
        max_x += 1
        max_y += 1
        print("max x:", max_x)
        print("max y:", max_y)
        size = (max_y, max_x)  # should it be: (max_y,max_x)?
        im = Image.new('RGB', size)
        print("size worked")
        pixels = im.load()
        print("load worked")
        for h in range(max_x):
            for w in range(max_y):
                r = extract_pixel_value(pixel_dict, "R", h, w)
                g = extract_pixel_value(pixel_dict, "G", h, w)
                b = extract_pixel_value(pixel_dict, "B", h, w)
                pixels[w, h] = (r, g, b)
        if filename != "":
            im.save(filename)
        im.show()
        return ket("image show/save")
    except:
        return ket("failed to show/save image")


# image-smooth[20] "" |lenna>
#
#
def image_smooth(one, k):
    try:
        k = int(k)
    except:
        return ket("", 0)

    def extract_ket_details(one):  # one is a ket
        try:
            value = one.value
            pixel_type, x, y = one.label.split(': ')[1:]
            return pixel_type, x, y, int(value)
        except:
            return

    def extract_pixel_value(pixel_dict, pixel_type, h, w):
        try:
            value = pixel_dict[pixel_type + ":" + str(h) + ":" + str(w)]
        except:
            value = 0
        return value

    def smooth_pixel_value(pixel_dict, pixel_type, h, w):  # can we do this neater!?
        value = extract_pixel_value(pixel_dict, pixel_type, h - 1, w - 1) / 16 + extract_pixel_value(pixel_dict,
                                                                                                     pixel_type, h,
                                                                                                     w - 1) / 16 + extract_pixel_value(
            pixel_dict, pixel_type, h + 1, w - 1) / 16
        value += extract_pixel_value(pixel_dict, pixel_type, h - 1, w) / 16 + extract_pixel_value(pixel_dict,
                                                                                                  pixel_type, h,
                                                                                                  w) / 2 + extract_pixel_value(
            pixel_dict, pixel_type, h + 1, w) / 16
        value += extract_pixel_value(pixel_dict, pixel_type, h - 1, w + 1) / 16 + extract_pixel_value(pixel_dict,
                                                                                                      pixel_type, h,
                                                                                                      w + 1) / 16 + extract_pixel_value(
            pixel_dict, pixel_type, h + 1, w + 1) / 16
        return value

    try:
        pixel_dict = {}
        max_x = 0
        max_y = 0
        for x in one:
            print("x:", x)
            pixel_type, x, y, value = extract_ket_details(x)
            if int(x) > max_x:
                max_x = int(x)
            if int(y) > max_y:
                max_y = int(y)
            pixel_dict[pixel_type + ":" + x + ":" + y] = value
        print("finished for loop")
        max_x += 1
        max_y += 1
        print("max x:", max_x)
        print("max y:", max_y)
        # for i in range(k):

        pixel_list = superposition()
    except:
        return ket("failed to smooth image")

    # 2/3/2016:


# time to revisit image load. I have some new ideas how I want to handle it now:
# load-image[image.png] |>
# returns: |image: 200 200: AF36782BA...>
# ie, we are creating an image data-type. Much more efficient than the superposition idea.
# After that, save-image, edge-enhance[20], and image-ngrams[5] (where an image-ngram is partitioning an image into size k*k smaller images)
#
# from PIL import Image
def new_image_load(filename):
    logger.debug("image name: " + filename)

    def int_to_hex(x):
        return "%0.2X" % x

    try:
        im = Image.open(filename)
        logger.debug("imaged open")
        width = im.size[0]
        height = im.size[1]
        ket_image_string = "image: %s %s: " % (width, height)
        for h in range(height):
            for w in range(width):
                r, g, b = im.getpixel((w, h))[:3]  # assumes image is RGB or RGBA, maybe fix later.
                ket_image_string += int_to_hex(r)
                ket_image_string += int_to_hex(g)
                ket_image_string += int_to_hex(b)

        # show the image:
        #    im.show()
        return ket(ket_image_string)
    except:
        return ket("", 0)


#    return ket("failed to load image")

# 3/3/2016:
# image.histogram() looks interesting. With quick testing on the Lenna image, seems it would make a very nice first order image -> superposition mapping.
# image-histogram[image.png] |>
# Then test with a couple of examples.
#
def image_histogram(filename):
    try:
        im = Image.open(filename)
        result = superposition()
        for k, x in enumerate(im.histogram()):
            result.data.append(ket(str(k), x))  # later swap in result += ket(str(k),x)
        return result
    except:
        logger.debug("failed to load image")
        return ket("", 0)


# 4/3/2016:
# time to revisit image save
# image-save[bah.png] image-load[foo.png] |>
# where image-save[some.png] takes input in the new image data type format: |image: 15 17: AB376C...>
# cool, seems to work!
#
def new_image_save(one, filename):
    try:
        datatype, size, data = one.label.split(": ")
        if datatype != "image":
            logger.debug("not image datatype")
            return one
        width, height = size.split(" ")
        width = int(width)
        height = int(height)
        expected_length = 6 * width * height  # It is hexadecimal, so 2+2+2 for RGB, times width*height
        if len(data) != expected_length:
            logger.debug("wrong image data length")
            return ket("")
    except:
        return ket(
            "")  # on error do we want to return |> or 0|> ?? Or, in this case maybe we want to return one, the input superposition?

    size = (width, height)
    im = Image.new('RGB', size)
    image_data = []
    for triple in [data[i:i + 6] for i in range(0, len(data), 6)]:
        print("triple: " + triple)
        r = int(triple[0:2], 16)
        g = int(triple[2:4], 16)
        b = int(triple[4:6], 16)
        print("R:", r)
        print("G:", g)
        print("B:", b)
        image_data.append((r, g, b))
    im.putdata(image_data)
    im.show()
    #  im.save(filename)
    return ket("making progress!")


# convert float to int if possible:
def float_to_int(x, t=3):
    if float(x).is_integer():
        return str(int(x))
    #  return str("%.3f" % x)
    return str(round(x, t))


# 29/1/2015:
# table[C,F,K] range(|c: 0>,|C: 100,|10>)         readable_display
# ie, create a pretty printed table:
# table[C,F,K] range(|C: 0>,|C: 50>,|10>)
# +-------+-----------+-----------+
# | C     | F         | K         |
# +-------+-----------+-----------+
# | C: 0  | F: 32.00  | K: 273.15 |
# | C: 10 | F: 50.00  | K: 283.15 |
# | C: 20 | F: 68.00  | K: 293.15 |
# | C: 30 | F: 86.00  | K: 303.15 |
# | C: 40 | F: 104.00 | K: 313.15 |
# | C: 50 | F: 122.00 | K: 323.15 |
# +-------+-----------+-----------+
#
# 10/2/2015: now with "extract-value" operator applied automatically, we now have:
#  F |*> #=> F |_self>
#  K |*> #=> K |_self>
#  table[C,F,K] range(|C: 0>,|C: 50>,|10>)
# +----+--------+--------+
# | C  | F      | K      |
# +----+--------+--------+
# | 0  | 32.00  | 273.15 |
# | 10 | 50.00  | 283.15 |
# | 20 | 68.00  | 293.15 |
# | 30 | 86.00  | 303.15 |
# | 40 | 104.00 | 313.15 |
# | 50 | 122.00 | 323.15 |
# +----+--------+--------+
#
# Finally! Took way, way longer than expected, but it works!!!!
#
# maybe table should apply clean? Decided on set-to[1]
#
# Now we have 4 permutations: table[], strict-table[], rank-table[], strict-rank-table[]
# hrmm... strict-rank-table has a bug!
#
# also, now with table code, should not be much work to convert sw => csv.
#
def old_pretty_print_table(one, context, params, strict=False, rank=False):
    # logger.debug("one: " + str(one))
    ops = params.split(',')
    if "coeff" in ops:  # yup. seems to work.
        coeff_col = [float_to_int(x.value) for x in
                     one]  # see float_to_int() for number of decimal places. Currently 3.
    if len(ops) == 2 and ops[1] == "*":  # display all supported ops, instead of having to specify them manually.
        ops = [ops[0]] + [x.label[4:] for x in one.apply_op(context, "supported-ops")]
        # logger.debug("ops: " + str(ops))
    # set all coeffs to 1. A table where the incoming superposition has coeffs is ugly, and I can't think of a use case.
    # easy enough to comment this line out, if we want:    # we need a way to occasionally show the coeffs of the incoming superposition. Don't yet know how!
    one = one.apply_sigmoid(set_to, 1)
    columns = []
    max_col_widths = []
    if rank:  # display rank option is on.
        col = [str(k + 1) for k in range(len(one))]  # start at 1, not 0.
        max_width = 4  # len("rank") == 4
        if len(col) > 0:
            max_width = max(4, len(col[-1]))  # longest element in col will be the last one.
        columns.append(col)
        max_col_widths.append(max_width)
    for k, op in enumerate(ops):
        if k == 0:  # don't process the incoming superposition
            #      col = [x.readable_display() for x in one]      # first op is treated as a label
            #      col = [x.apply_fn(extract_value).readable_display() for x in one]          # swapped in "extract-value".
            col = [x.apply_fn(remove_leading_category).readable_display() for x in
                   one]  # swapped in "remove_leading_category".
        elif op == "coeff":
            col = coeff_col
        else:  # I currenlty think it is the right approach
            #      col = [x.apply_op(context,op).readable_display() for x in one]            # and don't want yet another table variant (extract-value vs not)
            #      col = [x.apply_op(context,op).apply_fn(extract_value).readable_display() for x in one]  # "where-live" in foaf-example-in-sw.sw looks like needs categories!
            col = [x.apply_op(context, op).apply_fn(remove_leading_category).readable_display() for x in
                   one]  # hopefully remove_leading_category will help with the foaf-example-in-sw.sw case.
        max_width = 0
        if len(col) > 0:
            max_width = max(len(y) for y in col)  # max() bugs out if applied to an empty list
        max_width = max(max_width, len(op))
        columns.append(col)
        max_col_widths.append(max_width)
    # logger.debug("max_col_widths: " + str(max_col_widths))
    # logger.debug("columns: " + str(columns))
    #  return ket("bug!")
    hpre = "+-"
    hmid = "-+-"
    hpost = "-+\n"
    hfill = "-"
    header = hpre + hmid.join(hfill * w for w in max_col_widths) + hpost
    # logger.debug("header: " + str(header))
    pre = "| "
    mid = " | "
    post = " |\n"
    if rank:
        ops = ["rank"] + ops
    label_header = pre + mid.join(op.ljust(max_col_widths[k]) for k, op in enumerate(ops)) + post
    # logger.debug("label_header: " + str(label_header))
    s = header + label_header + header
    #  return ket("bug!")
    for k in range(len(one)):
        row = [columns[col_idx][k] for col_idx in range(len(columns))]
        if strict and '' in row:
            continue
        srow = pre + mid.join(row[col_idx].ljust(max_col_widths[col_idx]) for col_idx in range(len(columns))) + post
        s += srow
    s += header
    print(s)

    # code to save the table (useful for big ones, too hard to cut and paste from the console)
    logger.info("saving to: saved-table.txt")
    file = open("saved-table.txt", 'w')
    file.write("sa: table[" + params + "]\n")
    file.write(s)
    file.close()

    return ket("table")




# 22/2/2015:
# such-that[op] SP
# returns |x> if op is true/yes, |> otherwise.
# assumes one is a ket
#
# tweak: such-that[op1,op2,...] SP
# returns |x> if true/yes for all operators, |> otherwise.
#
# what happens if we have 0.3|yes>? ie, if coeff < 0.5 I think we want that ket ignored.
#
def ket_such_that(one, context, ops):  # what happens if coeff != 1, eg 0?
    for op in ops.split(','):
        #    label = one.apply_op(context,op).the_label().lower()
        e = one.apply_op(context, op).ket()
        label = e.label
        value = e.value
        if label not in ["true", "yes"]:
            return ket("", 0)
        if value < 0.5:  # need to test this bit.
            return ket("", 0)
    return one


# 28/4/2016:
# tweak such-that[op] so it is a sp -> sp function, instead of a ket -> ket function. Should be an optimization, with a better big-O.
def old_sp_such_that(one, context, ops):
    def valid_ket(one, context, ops):
        for op in ops.split(','):
            e = one.apply_op(context, op).ket()
            if e.label not in ["true", "yes"]:
                return False
            if e.value < 0.5:  # need to test this bit.
                return False
        return True

    result = superposition()
    result.data = [x for x in one if valid_ket(x, context, ops)]
    return result


from time import sleep


# 3/2/2015:
# sleep for 5 seconds: sleep[5]
def bko_sleep(one, time):
    sleep(float(time))
    return one


# 4/2/2015:
# map: 3752 -> 3,752
# map: 29872 -> 29,872
# and so on.
# I don't understand how "{:,}".format(value) works, but copied from here:
# http://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators
#
# desired exmples:
# to-comma-number |8825 => |8,825>
# to-comma-number |population: 230000 => |population: 2,300,00>
# to-comma-number |3759.27 => |3,759.27>
# to-comma-number |km: 22956.53 => |km: 22,9356.53>
# Tested, and it works!
#
# assumes one is a ket.
def number_to_comma_number(one):
    cat, value = extract_category_value(one.label)
    try:
        if float(value).is_integer():
            value = int(value)
        else:
            value = float(value)
    except:
        return one
    if len(cat) > 0:
        cat += ": "
    return ket(cat + "{:,}".format(value), one.value)


# current date, and current time:
import datetime


def current_date(one):
    return ket("date: " + str(datetime.date.today()))


# buggy! Not my local time. Not sure how to fix yet!
from time import gmtime, strftime


def current_time(one):
    #  return ket("time: " + str(datetime.datetime.now().time()))
    #  return ket("time: " + str(datetime.datetime.now().strftime('%H:%M:%S')))
    return ket("time: " + strftime('%H:%M:%S', gmtime()))


# 9/2/2015: working towards a BKO rambler
# extract-3-tail |a b c d e f g h> == |f g h>
# example usage:
# ramble |*> #=> merge-labels(|_self> + | > + pick-elt next-2 extract-3-tail |_self>)
#
# assumes one is a ket
def extract_3_tail(one):
    split_str = one.label.rsplit(' ', 3)
    if len(split_str) < 4:
        return one
    return ket(" ".join(split_str[1:]))


# 19/7/2015: working towards a BKO letter rambler
# extract-3-tail-chars |abcdefgh> == |fgh>
# example usage:
# letter-ramble |*> #=> merge-labels(|_self> + pick-elt next-2-letters extract-3-tail-chars |_self>)
#
# assumes one is a ket
def extract_3_tail_chars(one):
    chars = one.label[-3:]
    return ket(chars)


# 21/2/2015: round[3] |number: 3.1415> == |number: 3.142>
# assumes one is a ket, t is an integer
#
def old_round_numbers(one, t):
    cat, value = extract_category_value(one.label)
    try:
        value = float(value)
    except:
        return one
    if len(cat) > 0:
        cat += ": "
    rounded_value = round(value, t)
    if rounded_value.is_integer():
        rounded_value = int(rounded_value)
    return ket(cat + str(rounded_value))


# 14/1/2016:
# Instead of just round_numbers(), let's implement a more general numbers_fn().
# Eventually we want: round[3], times-by[2], divide-by[7], plus[5.2], minus[9], and maybe others.
# currently has a bug for large numbers!
# sa: int-divide-by[1000] |12345678901234567890>
# |12345678901234568>
#
# sa: mod[1000] |12345678901234567890>
# |168>
#
# foo() is a 2 param fn, one is a ket, t is number
def old_numbers_fn(foo, one, t):
    try:
        cat, value = one.label.rsplit(': ', 1)
        value = float(value)
    except:
        try:
            cat = ''
            value = float(one.label)
        except:
            return one  # not sure best thing to return for this case.
    if len(cat) > 0:
        cat += ": "
    result_value = foo(value, t)
    if result_value.is_integer():
        result_value = int(result_value)
    return ket(cat + str(result_value), one.value)


# to-coeff 12|> == |>
# to-ceoff 26|a: b> == 26| >
#
# assumes one is a ket
def to_coeff(one):
    if one.label == "":
        return ket("", 0)
    return ket(" ", one.value)


# one off use:
# extract year from movie name:
# eg:
# extract-year |movie: Nykytaiteen museo (1986)> == |year: 1986>
#
# one is a ket
def extract_year(one):
    year = one.label[-5:-1]
    return ket("year: " + year)


# ket-length
# eg: ket-length |abcde> == |number: 5>
#
def ket_length(one):
    return ket("number: " + str(len(one.label)))


# function to pretty print seconds
# from here: http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
# eg:
# >>> display_time(33)
# '33 seconds'
# >>> display_time(3600)
# '1 hour'
# >>> display_time(3640)
# '1 hour, 40 seconds'
# >>> display_time(10987341908)
# '18166 weeks, 6 days, 7 hours, 25 minutes, 8 seconds'
#
old_intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def old_display_time(float_seconds):
    # cast to int:
    seconds = int(float_seconds)  # it wasn't handling decimal places correctly anyway, so may as well cast to int.
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    if len(result) == 0:
        return str("%.4f" % float_seconds) + " seconds"
    return ', '.join(result)


# 11/3/2015: I tweaked so can handle ms too.
intervals = (
    ('weeks', 604800000),  # 1000 * 60 * 60 * 24 * 7
    ('days', 86400000),  # 1000 * 60 * 60 * 24
    ('hours', 3600000),  # 1000 * 60 * 60
    ('minutes', 60000),  # 1000 * 60
    ('seconds', 1000),  # 1000
    ('milliseconds', 1),
)


def display_time(seconds):
    ms = int(1000 * seconds)
    result = []

    for name, count in intervals:
        value = ms // count
        if value:
            ms -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    if len(result) == 0:
        return "0"
    return ', '.join(result)


# 6/3/2015:
# display-algebra:
# display-algebra (3|x*x> + 2|y> + |z> + 13| >)
# 3*x*x + 2*y + z + 13
#
# what a mess! Surely we can write it neater than this!!!
# seems to work though.
#
# one is a superposition
def display_algebra(one):
    result = []
    for x in one:
        if x.label == '':  # should never be true, since it should be taken care of elsewhere.
            continue
        if x.value == 1:
            coeff = ""
        else:
            coeff = str(float_to_int(x.value)) + "*"
        if x.label.strip() == '':
            term = coeff.rstrip("*")
            if term == "":
                term = "1"
        else:
            term = coeff + x.label
        result.append(term)
    return ket(" + ".join(result))


# 24/3/2015: we need this for find_unique
# though if we had fast_superpostion in place, we probably wouldn't need it.
# converts superposition to ordered dictionary
#
def sp_to_dict(one):
    r = OrderedDict()
    for elt in one:
        r[elt.label] = elt.value
    return r


# 24/3/2015:
# find-unique[names]
#
# unique-names |male name>
# unique-names |female name>
# unique-names |last name>
#
# yup. seems to work! And is fast! 4 days estimated for the names.sw data, down to 2 seconds, 753 milliseconds
def find_unique(context, op):
    kets = context.relevant_kets(op)
    print("kets:", kets)
    sp_list = [[x.label, sp_to_dict(x.apply_op(context, op))] for x in kets]
    print("sp-list:", sp_list)

    for your_label, your_dict in sp_list:
        other_dict = {}
        for label, the_dict in sp_list:
            if label != your_label:
                other_dict.update(the_dict)
        result = superposition()
        result.data = [ket(key, your_dict[key]) for key in your_dict if
                       key not in other_dict]  # because we use dictionaries, presumably there will be no duplicate kets.
        print(your_label, "result:", result)
        context.learn("unique-" + op, your_label, result)
    return ket("find-unique")


# 2/6/2015:
# find-inverse[op]
#
# hrmm... I wonder if it should be shifted from context class to here?
# I mean, it does seem a very close brother with find-unique[op], yet that is here and not in context class. Shouldn't they be in the same spot?
# Is it faster to have create-inverse[op] in the context class? Yeah, probably quite a bit faster than going via apply_op() and context.recall()!
# does that mean I should move find_unique to the context class?
#
def find_inverse(context, op):
    context.create_inverse_op(op)
    return ket('find-inverse')





# 14/4/2015:
# starts-with |a: b: > returns |a: b: c>, |a: b: c: d> and so on.
# eg, we can now do: starts-with |person: Fred > to list all people with first name Fred.
#
# e is a ket
def starts_with(e, context):
    return context.starts_with(e)


# apply-weights[5,3,2] SP
#
def apply_weights(one, weights):
    weights = weights.split(",")
    result = superposition()
    for k, x in enumerate(one):
        if k >= len(weights):
            break
        result += x.multiply(float(weights[k]))
    return result


# rank (|a> + |b> + |c>)
# 1|a> + 2|b> + 3|c>
#
# one is a superposition
def rank(one):
    r = superposition()
    for k, (label, value) in enumerate(one.items()):
        r.add(label, k + 1)
    return r


# lower-case, upper-case, sentence-case
#
# one is a ket
def lower_case(one):
    return ket(one.label.lower(), one.value)


def upper_case(one):
    return ket(one.label.upper(), one.value)


# from the_semantic_db_code import fast_superposition
# one-gram |text: just some text>
# two-gram |text: just some more text>
#
# one is a ket
def one_gram(one):
    text = one.label
    if text.startswith('text: '):
        text = text[6:]
    #  result = fast_superposition()
    result = superposition()
    for x in text.split():  # update to use the 2-gram word-split method?
        for y in x.split('\\n'):  # what about escaped \n?
            result += ket(
                y)  # what about non-char words? eg, "This is a sentence." is returned as |this> + |is> + |a> + |sentence.>
    #  return result.superposition()                # actually, maybe the "read" operator fixed this. Yup. Use that instead.
    return result


def create_word_n_grams(s, N):
    return [" ".join(s[i:i + N]) for i in range(len(s) - N + 1)]


def create_letter_n_grams(s, N):
    return ["".join(s[i:i + N]) for i in range(len(s) - N + 1)]


def two_gram(one):
    text = one.label if type(one) == ket else one
    if text.startswith('text: '):
        text = text[6:]

    #  text = "".join(c for c in text.lower() if c in 'abcdefghijklmnopqrstuvwxyz\'- ').split() # not sure this is exactly what we want!
    words = [w for w in re.split('[^a-z0-9_\']', text.lower().replace('\\n', ' ')) if w]

    result = superposition()
    for w in create_word_n_grams(words, 2):
        result += ket(w)
    return result


def three_gram(one):
    text = one.label if type(one) == ket else one
    if text.startswith('text: '):
        text = text[6:]

    words = [w for w in re.split('[^a-z0-9_\']', text.lower().replace('\\n', ' ')) if w]

    result = superposition()
    for w in create_word_n_grams(words, 3):
        result += ket(w)
    return result


def make_ngrams(one, parameters, ngram_type):
    logger.debug("one: " + str(one))
    logger.debug("parameters: " + parameters)
    logger.debug("ngram-type: " + ngram_type)
    sizes = parameters.split(',')
    for k in sizes:  # check our sizes are all integers. The list should be short, so the O(n) is very cheap.
        if not k.isdigit():
            return ket("", 0)

    text = one.label if type(one) == ket else one
    if text.startswith('text: '):
        text = text[6:]

    if ngram_type == "word":
        words = [w for w in re.split('[^a-z0-9_\']', text.lower().replace('\\n', ' ')) if w]  # do we want .lower() in there?
        create_ngram_fn = create_word_n_grams
    elif ngram_type == "letter":
        words = list(text)
        create_ngram_fn = create_letter_n_grams
    else:
        return ket("", 0)

    #  result = fast_superposition()           # seems to bug out.
    result = superposition()
    for k in sizes:
        for w in create_ngram_fn(words, int(k)):
            result += ket(w)
    #  return result.superposition()
    return result


# 30/4/2015:
# plus-or-minus |x> returns |+ x> + |- x>
# plus-or-minus |+ x> returns |+ x> + |- x>
# plus-or-minus |- x> returns |- x> + |+ x>
# not sure what we want for: plus-or-minus plus-or-minus |x>
#
# one is a ket
def plus_or_minus(one):
    if one.label.startswith('+ '):
        return one + ket("- " + one.label[2:], one.value)
    if one.label.startswith('- '):
        return one + ket("+ " + one.label[2:], one.value)
    return ket("+ " + one.label, one.value) + ket("- " + one.label, one.value)


#
def average_categorize(context, parameters):
    try:
        op, t, phi, ave = parameters.split(',')
        t = float(t)
    except:
        return ket("", 0)

    one = context.relevant_kets(op)
    print("one:", one)
    out_list = []
    for x in one:
        print("x:", x)
        r = x.apply_op(context, op)
        print("r:", r)
        best_k = -1
        best_simm = 0
        for k, sp in enumerate(out_list):
            similarity = silent_simm(r, sp)
            if similarity > best_simm:
                best_k = k
                best_simm = similarity
        print("best k:", best_k)
        print("best simm:", best_simm)

        if best_k == -1 or best_simm < t:
            out_list.append(r)
        else:
            k = best_k
            #      out_list[k] += r
            out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
    for k, sp in enumerate(out_list):
        print("sp:", sp)
        context.learn(ave, phi + ": " + str(k + 1), sp)
    return ket("average categorize")


# 25/11/2015:
# unique-categorize. If it works as hoped, a kind of principle component thingy.
# How do we test this thing?? Maybe the simple images example?
# Hrmm.. might be able to use this (a thing I recall from linear algebra): https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process
# Instead of <u,v> being standard dot-product, use simm(u,v). Might just work.
# I don't think this will be the unique_categorize I'm after, but should still be useful. And also as a starting point.
#
# Hrm... I don't think I know what I am doing here. I need to give it a lot more thought!
#
def unique_categorize(context, parameters):
    try:
        op, t, phi, ave = parameters.split(',')
        t = float(t)
    except:
        return ket("", 0)

    one = context.relevant_kets(op)
    print("one:", one)
    out_list = []
    for x in one:
        print("x:", x)
        r = fast_superposition() + x.apply_op(context,
                                              op)  # Yeah, a hack. But using fast_sp is the easiest way to do the "find-unique" step.
        print("r:", r)
        best_k = -1
        best_simm = 0
        for k, sp in enumerate(out_list):
            similarity = silent_simm(r, sp)
            if similarity > best_simm:
                best_k = k
                best_simm = similarity
        print("best k:", best_k)
        print("best simm:", best_simm)

        if best_k == -1 or best_simm < t:
            out_list.append(r)
        else:
            k = best_k
            #      out_list[k] += r
            out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
        for k1, sp1 in enumerate(out_list):
            tmp_sp = fast_superposition()
            for k2, sp2 in enumerate(out_list):
                if k1 != k2:
                    tmp_sp += sp2
    # ...

    for k, sp in enumerate(out_list):
        print("sp:", sp)
        context.learn(ave, phi + ": " + str(k + 1),
                      sp.superposition())  # need to convert fast_sp back to sp. Yeah, when am I going to finally swap in fast_sp full time??
    return ket("average categorize")


# 5/5/2016:
# New idea, a tweak to average-categorize, so now it has a suppress element to it.
# I don't know if this will work or not, but I will test soon.
def average_categorize_suppress(context, parameters):
    try:
        op, t, phi, ave = parameters.split(',')
        t = float(t)
    except:
        return ket("", 0)

    w = 1  # w = 0 should reproduce standard version. w = 1 hopefully makes final sp's more "orthogonal"
    one = context.relevant_kets(op)
    print("one:", one)
    out_list = []
    for x in one:
        print("x:", x)
        r = x.apply_op(context, op)
        print("r:", r)
        best_k = -1
        best_simm = 0
        for k, sp in enumerate(out_list):
            similarity = silent_simm(r, sp)
            if similarity > best_simm:
                best_k = k
                best_simm = similarity
        print("best k:", best_k)
        print("best simm:", best_simm)

        if best_k == -1 or best_simm < t:
            out_list.append(r)
        else:
            for k in range(len(out_list)):
                if k == best_k:
                    out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
                else:
                    if w != 0:
                        similarity = silent_simm(r, out_list[k])
                        out_list[k] += r.multiply(
                            -w * similarity)  # suppress r from this pattern, w chooses how much. Alternatively, put a .drop() in here.
    for k, sp in enumerate(out_list):
        print("sp:", sp)
        context.learn(ave, phi + ": " + str(k + 1), sp.drop())
    return ket("average categorize")


# 6/5/2016:
# a list-average-categorize-suppress(). Hopefully converting sp's to lists, the simm will be faster, and also handle negative values if needed.
#
# 7/5/2016: in testing so far, w != 0 doesn't work so great.
#
# import numpy as np                      # yeah, another dependence.
def list_average_categorize_suppress(context, parameters):
    try:
        op, t, phi, ave = parameters.split(',')
        t = float(t)
    except:
        return ket("", 0)

    def simple_sp_to_list(sp):  # need to test these two, but I think they are correct.
        r = np.array([x.value for x in sp])
        return r

    def list_to_simple_sp(data):
        r = superposition()
        r.data = [ket(str(k), x) for k, x in enumerate(data)]
        return r

    def rescale(arr):
        arr = arr - arr.min()
        if arr.max() == 0:
            return arr
        arr = arr * 255 / arr.max()  # maybe try rescale to [0,255] later. Bug, what about max == 0?
        return arr

    # w = 0.01                                            # w = 0 should reproduce standard version. w = 1 hopefully makes final sp's more "orthogonal"
    w = 0  # switch it off for now
    one = context.relevant_kets(op)
    print("one:", one)
    out_list = []
    for x in one:
        print("x:", x)
        r0 = x.apply_op(context, op)
        r = simple_sp_to_list(r0)
        print("r:", r)
        best_k = -1
        best_simm = 0
        for k, sp in enumerate(out_list):
            #      similarity = silent_simm(r,sp)
            similarity = rescaled_list_simm([1], r, sp)
            if similarity > best_simm:
                best_k = k
                best_simm = similarity
        print("best k:", best_k)
        print("best simm:", best_simm)

        if best_k == -1 or best_simm < t:
            out_list.append(r)
        else:
            for k in range(len(out_list)):
                if k == best_k:
                    #          out_list[k] += r*best_simm  # reweight based on result of simm.  # bug! a + b for lists is append, not add in place.
                    out_list[k] = out_list[
                                      k] + r * best_simm  # bug! a*b for a list, b scalar does not work as expected either! numpy to the rescue!
                #          out_list[k] = rescale(out_list[k] + r*best_simm)           # trying another idea. Rescale each time.
                else:
                    if w != 0:
                        similarity = rescaled_list_simm([1], r, out_list[k])
                        out_list[k] = out_list[
                                          k] - r * w * similarity  # suppress r from this pattern, w chooses how much. Alternatively, put a .drop() in here.
    for k, sp in enumerate(out_list):
        print("sp:", sp)
        #    context.learn(ave,phi + ": " + str(k+1),sp.drop())             # NB: we can't use drop, as that will break our sp to image code
        #    context.learn(ave,phi + ": " + str(k+1),list_to_simple_sp(sp).apply_sigmoid(pos))
        context.learn(ave, phi + ": " + str(k + 1),
                      list_to_simple_sp(rescale(sp)))  # final rescale didn't seem to make much difference
        context.learn(ave, phi + ": " + str(k + 1), list_to_simple_sp(sp))
    return ket("average categorize")


# 6/5/2016:
# average-categorize-suppress has 2 issues:
# 1) I'm not sure it is designed to work with sp's with negative coeffs. ie, silent_simm() is the problem. So maybe a more general version?
# 2) it is slow! Maybe swap in a sp to list step, and use scaled-list-simm() in place of silent_simm()?
def bah__average_categorize_suppress(context, parameters):
    try:
        op, t, phi, ave = parameters.split(',')
        t = float(t)
    except:
        return ket("", 0)

    w = 1  # w = 0 should reproduce standard version. w = 1 hopefully makes final sp's more "orthogonal"
    one = context.relevant_kets(op)
    print("one:", one)
    out_list = []
    for x in one:
        print("x:", x)
        r = x.apply_op(context, op)
        print("r:", r)
        best_k = -1
        best_simm = 0
        for k, sp in enumerate(out_list):
            similarity = silent_simm(r, sp)
            if similarity > best_simm:
                best_k = k
                best_simm = similarity
        print("best k:", best_k)
        print("best simm:", best_simm)

        if best_k == -1 or best_simm < t:
            out_list.append(r)
        else:
            for k in range(len(out_list)):
                if k == best_k:
                    out_list[k] += r.multiply(best_simm)  # reweight based on result of simm.
                else:
                    if w != 0:
                        similarity = silent_simm(r, out_list[k])
                        out_list[k] += r.multiply(-w * similarity)  # suppress r from this pattern, w chooses how much
    for k, sp in enumerate(out_list):
        print("sp:", sp)
        context.learn(ave, phi + ": " + str(k + 1), sp.drop())
    return ket("average categorize")


# 5/8/2015:
# split-chars |abcde> == |a> + |b> + |c> + |d> + |e>
#
# one is a ket
def split_chars(one):
    try:
        chars = list(one.label)
        result = superposition()
        for c in chars:
            result += ket(c)
        return result
    except:
        return ket("", 0)


# select-chars[a,b] |uvwxyz>
# eg: select-chars[3,4,7] |abcdefgh> == |cdg>
# should it be similar to select[1,5]? I think we are breaking that.
# maybe we need to distinguish between select-range and select-elts
# or, a better option, allow: select-chars[3,5,7,13-19,23,31-41] |...>
# and we would have to do the same for superposition select[] too.
# OK. I like that idea. Not sure if current parser can handle that. I need to check.
#
# and what about: select-chars[1,3] |abcdef> == |a> + |c> ??
# presumably the just written: split-chars will do that for us.
#
# what about indexing from the end of the list?
# do we have a reverse ket-label function operator?
# And I'm starting to get annoyed with adding all these little things! I know I promised we could add new ones without bounds, but still, I'm getting sick of this!
#
# one is a ket
def select_chars(one, positions):
    try:
        positions = positions.split(",")
        chars = list(one.label)
        text = "".join(chars[int(x) - 1] for x in positions if int(x) <= len(chars))
        return ket(text)
    except:
        return ket("", 0)


import hashlib


# 24/8/2015:
# ket-hash[size] |some ket>
#
# one is a ket
def ket_hash(one, size):
    logger.debug("ket-hash one: " + str(one))
    logger.debug("ket-hash size: " + size)
    try:
        size = int(size)
    except:
        return ket("", 0)
    our_hash = hashlib.md5(one.label.encode('utf-8')).hexdigest()[-size:]
    return ket(our_hash, one.value)


import zlib


# 19/6/2016:
# hash-compress (|a> + |b> + |c> + |d>)
#
# sa: hash-compress split |a b c d>
# |620062> + |630063> + |640064> + |650065>
#
# one is a ket
def hash_compress(one):
    our_hash = zlib.adler32(one.label.encode('utf-8'))
    return ket("%0.2X" % our_hash, one.value)


# 24/8/2015:
# hash-data[size] SP
#
# one is a superposition
def hash_data(one, size):
    logger.debug("hash-data one: " + str(one))
    logger.debug("hash-data size: " + size)
    try:
        size = int(size)
    except:
        return ket("", 0)
    array = [0] * (16 ** size)
    for x in one:
        our_hash = hashlib.md5(x.label.encode('utf-8')).hexdigest()[-size:]
        k = int(our_hash, 16)
        array[k] += 1 * x.value
    logger.info("hash-data writing to tmp-sp.dat")
    f = open('tmp-sp.dat', 'w')
    for k in array:
        f.write(str(k) + '\n')
    f.close()
    return ket("hash-data")


# eg: process-reaction(current-sp,2|H2> + |O2>,2|H2O>) == current-sp - (2|H2> + |O2>) + 2|H2O>
# Cool. Seems to work.
# 16/2/2016: maybe process-consuming-reaction() is a better name, to tie in with process-catalytic-reacion()
#
# one, two and three are superpositions
def old_process_reaction(one, two, three):
    if type(one) is sequence and type(two) is sequence and type(three) is sequence:
        one = one[0]  # hackily cast sequence to superposition for now.
        two = two[0]
        three = three[0]

    def del_fn(x, y):  # NB: creates negative coeffs.
        return x - y

    if intersection(two, one).count_sum() != two.count_sum():
        return one
    else:
        return intersection_fn(del_fn, one,
                               two).drop() + three  # can we do superposition subtraction? Maybe implement it?? Meaning: one - two + three


# 16/2/2016:
# process-catalytic-reaction(current-sp,|a> + |b>,|c> +|d>) = current-sp + |c> + |d> if |a> + |b> is in current-sp
# What if |c> + |d> is already in current-sp? Do you add it again?
# I suspect process-catalytic-reaction() can be used to encode maths proofs. One is the current state of knowledge. Two is the necessary conditions for the proof to be true. Three is the implications of that proof.
# Another example is simple physics problems. You write down what you know, and any possibly relevant equations. Then try to figure out a pathway to the desired result.
#
def old_process_catalytic_reaction(one, two, three):
    if intersection(two, one).count_sum() != two.count_sum():
        return one
    else:
        return one + three


# 31/10/2016:
# rewrite(SP,|s1>,|s2>)
# replace all instances of string "s1" with "s2" in SP
# simple, but powerful. cf. productions: https://en.wikipedia.org/wiki/Production_(computer_science)
# Doh! Already implemented long ago as "rename_kets" with essentially identical code!
#
# one is a sp, s1 and s2 are kets
def rewrite(one, s1, s2):
    string1 = s1.the_label()
    string2 = s2.the_label()
    r = superposition()
    for x in one:
        y_label = x.label.replace(string1, string2)
        r += ket(y_label, x.value)
    return r


# x,y are floats
def filter_fn(x, y):
    if x == 0:
        return 0
    return y


# filter-down-to(|b> + 3|c>,|a> + 5|b> + 0.7|c> + 9|d> + 3.2|e>) == 5|b> + 0.7|c>
#
# one, two are superpositions
def filter_down_to(one, two):
    return intersection_fn(filter_fn, one, two).drop()


# respond-to-pattern(current-sp,pattern,consequence)
# heh. I forgot what this even does!
#
# one, two and three are superpositions
def respond_to_pattern(one, two, three):
    r = filter_down_to(two, one)
    similarity = silent_simm(r, two)
    return one + three.multiply(similarity)


# 26/11/2015:
# Let's try to implement edit-distance using operators.
# https://en.wikipedia.org/wiki/Edit_distance
#
# def edit_insert(one,parameters):
# def edit_delete():
# def edit_substitute():
#
# 17/12/2015: let's finally get to this.
# start with:
# delete[k,0]
# insert[s,0]
#
# It works:
# LCS distance:
# sa: insert[g,6] insert[i,4] delete[e,4] insert[s,0] delete[k,0] |kitten>
# |sitting>
#
# Levenshtein distance:
# sa: insert[g,6] substitute[i,e,4] substitute[s,k,0] |kitten>
# |sitting>
#
# one is a ket
# delete[k,0]
def edit_delete(one, parameters):  # cool. Seems to work!
    try:
        char, k = parameters.split(',')
        k = int(k)
        text = one.label
        if text[k] == char:
            result = text[:k] + text[k + 1:]
        return ket(result, one.value)
    except:
        return one


# insert[s,0]
def edit_insert(one, parameters):
    try:
        char, k = parameters.split(',')
        k = int(k)
        text = one.label
        result = text[:k] + char + text[k:]
        return ket(result, one.value)
    except:
        return one


# substitue[s,k,0]
def edit_substitute(one, parameters):
    try:
        char1, char2, k = parameters.split(',')
        k = int(k)
        text = one.label
        if text[k] == char2:
            text = text[:k] + char1 + text[k + 1:]
        return ket(text, one.value)
    except:
        return one


# 9/2/2016:
# guess-ket |fred>          -- return the best matching known ket (using simm and so on)
# guess-ket[3] |Sam>        -- return the best 3 matching known kets, providing simm > 0
# guess-ket[*] |robbie>     -- return all matching known kets, providing simm > 0
#
# could do with some optimization!
#
# one is a ket
def guess_ket(one, context, t='1'):
    def process_string(s):
        one = ket(s.lower())  # I presume we want s.lower(). Maybe sometimes we don't?
        return make_ngrams(one, '1,2,3', 'letter')

    try:
        guess = process_string(one.label)
        r = superposition()
        for x in context.relevant_kets(
                "*"):  # what about kets that are only on the right hand side of a learn rule? This misses them. One way is run "create inverse", but is there a better way?
            #      similarity = silent_simm(guess,process_string(x.label))
            similarity = fast_simm(guess, process_string(x.label))
            if similarity > 0:
                r.data.append(x.multiply(similarity))  # later swap in r += x.multiply(similarity)
        if t == '*':
            return r.coeff_sort()
        else:
            return r.coeff_sort().select_range(1, int(t))
    except:
        return ket("", 0)


# 9/2/2016:
# guess-operator[age]          -- return the best matching known operator (using simm and so on)
# guess-operator[friend,3]     -- return the best 3 matching known operators, providing simm > 0
# guess-operator[mother,*]     -- return all matching known operators, providing simm > 0
#
def guess_operator(context, parameters):
    try:
        op, t = parameters.split(',')
        if t != '*':
            t = int(t)
    except:
        op = parameters
        t = 1

    def process_string(s):
        one = ket(s.lower())
        return make_ngrams(one, '1,2,3', 'letter')

    try:
        guess = process_string(op)
        r = superposition()
        for x in context.supported_operators():
            similarity = silent_simm(guess, process_string(x.label[4:]))  # need to convert 'op: age' to 'age'
            r.data.append(x.multiply(similarity))  # later swap in r += x.multiply(similarity)
        if t == '*':
            return r.drop().coeff_sort()
        else:
            return r.drop().coeff_sort().select_range(1, t)
    except:
        return ket("", 0)


# 9/2/2016:
# rename_kets:
# takes a superposition (one), and for each ket replaces the string in ket two with the string in ket three
#
# one is a superposition, two and three are kets.
def rename_kets(one, two, three):
    try:
        s1 = two.the_label()
        s2 = three.the_label()
        result = superposition()
        for x in one:
            y = ket(x.label.replace(s1, s2), x.value)
            #      result.data.append(y)                                         # later swap in result += y. data.append is buggy in case the string replace creates duplicate kets
            result += y
        return result
    except:
        return ket("", 0)

    # 20/3/2016:


#
# path-op[op] sp
# eg:
# op |A> => |B: 1> + |C: 2> + |G: 3>
# op |B> => |A: 4> + |D: 5> + |H: 6>
#
# then:
# path-op[op] |B: 1>
# == |A: 1: 4> + |D: 1: 5> + |H: 1: 6>
#
# one is a ket (so linear in kets), op is a string
def path_op(one, context, op):
    try:
        split_ket_string = one.label.split(': ', 1)
        element = split_ket_string[0]
        rule = context.recall(op, element)
        if len(split_ket_string) == 1:
            return rule
        path_history = split_ket_string[1]
        print("element:", element)
        print("path_history:", path_history)
        print("rule:", rule)
        r = superposition()
        for x in rule:
            x_element, x_path_history = x.label.split(': ', 1)
            r += ket('%s: %s: %s' % (x_element, path_history, x_path_history))
        return r
    except Exception as e:
        print("reason:", e)
        return ket("", 0)


# 10/5/2016:
# implement my idea for simm-add[op,p]
# where:
# R0 = r0
# R_k = R_k-1 + r_k * [simm(R_k-1,r_k)]^p
#
# how on Earth do we test this thing??
# Hrmm... result seems essentially identical, to say 1% or less, with just adding them! At least for p = 1,2. I tried p = 100, and still not much difference.
#
def simm_add(one, context, parameters):
    try:
        op, p = parameters.split(',')
        p = int(p)  # maybe try float(p) later
    except:
        return ket("", 0)

    head, *tail = one
    Rk = head.apply_op(context, op)
    for x in tail:
        rk = x.apply_op(context, op)
        similarity = silent_simm(Rk, rk) ** p
        Rk = Rk + rk.multiply(similarity)
    return Rk


# now, in our digit recognition task, it is clear that some features are far more common than others. eg white space
# so the question is, how best to normalize this a bit.
# Currently I'm using log(1 + x) which maps the test case of 1000 test images from 70.9% to 72.1%
# Recall best algo's give 98%, so I have a lot of work to do yet!!
# Next idea is ket normalization. ie, reweight kets so that on average, each ket "fires" at the same rate
# Hopefully it will encode the idea that frequently firing kets are less interesting than rarely firing ones.
# In BKO, this:
# -- these are our starting superpositions:
#    the |sp1> => a1|A> + b1|B> + c1|C>
#    the |sp2> => a2|A> + b2|B> + c2|C>
#    the |sp3> => a3|A> + b3|B> + c3|C>
#    the |sp4> => a4|A> + b4|B> + c4|C>
#
# -- the sum of our superpositions:
#    the-sum |sp> => the (|sp1> + |sp2> + |sp3> + |sp4)
#
# -- these are what we want our code to learn:
#    norm-ket |A> => 1/(a1 + a2 + a3 + a4) |A>
#    norm-ket |B> => 1/(b1 + b2 + b3 + b4) |B>
#    norm-ket |C> => 1/(c1 + c2 + c3 + c4) |C>
#
# -- this is intended usage once we have them (probably implemented with map)
#    the-normed |sp1> => norm-ket the |sp1>
#    the-normed |sp2> => norm-ket the |sp2>
#    the-normed |sp3> => norm-ket the |sp3>
#    the-normed |sp4> => norm-ket the |sp4>
#
# -- test our code works:
#    norm-ket the-sum |sp> == |A> + |B> + |C>
#
#
def learn_ket_normalizations(context, parameters):
    try:
        op1, op2, t = parameters.split(',')
        t = float(t)
    except:
        return ket("", 0)

    the_kets = context.relevant_kets(op1)
    the_sum = superposition()
    for x in the_kets:
        the_sum += x.apply_op(context, op1)
    for x in the_sum:
        if x.value <= 0:
            continue
        y = ket(x.label)
        context.learn(op2, y, y.multiply(t / x.value))
    return ket("ket-norms")


# append-column[n] SP
# for use in Hierarchical Temporal Memory sequence learning
# append-column[5] |X> == |X: 0> + |X: 1> + |X: 2> + |X: 3> + |X: 4>
# Cool! In testing it works just fine.
# and has the property:
# extract-category append-column[10] |X> == 10 |X>
#
# one is a ket, N is a positive integer
def append_column(one, N):
    try:
        N = int(N)
    except:
        return ket("", 0)

    r = superposition()
    for k in range(N):
        r += ket("%s: %s" % (one.label, k), one.value)
    return r


import random


# random-column[n] SP
# for use in Hierarchical Temporal Memory sequence learning
# random-column[5] |X> == pick-elt( |X: 0> + |X: 1> + |X: 2> + |X: 3> + |X: 4>)
# and has the property:
# extract-category random-column[10] |X> == |X>
#
# one is a ket, N is a positive integer
def random_column(one, N):
    try:
        N = int(N)
    except:
        return ket("", 0)

    random_integer = random.randint(0, N - 1)
    return ket("%s: %s" % (one.label, random_integer), one.value)


# 28/7/16:
# usage:
# have-in-common (|Fred> + |Sam> + |Jack>)
# 0.7 |op: friends> + |op: age> + 0.5|op: parents>
#
def have_in_common(one, context):
    logger.debug("have-in-common one: %s" % str(one))

    if len(one) == 0:
        return ket("", 0)
    for sp in one:
        supported_ops = sp.apply_op(context, "supported-ops")
        break
    for sp in one:
        tmp = sp.apply_op(context, "supported-ops")
        supported_ops = intersection(supported_ops, tmp)
    if len(supported_ops) == 0:
        return ket("", 0)
    # ... finish


def bar_chart(one, width, sorted=False):
    if len(one) == 0:
        return ket("bar chart")
    try:
        width = int(width)
    except:
        return ket("bar chart")
    max_len = max(len(x.label) for x in one)
    #  print("max_len:",max_len)
    #  two = one.coeff_sort().rescale(width).apply_sigmoid(floor)
    if sorted:
        two = one.coeff_sort().rescale(width)
    else:
        two = one.rescale(width)
    mid = ' : '
    print("----------")
    for x in two:
        print(x.label.ljust(max_len) + mid + '|' * int(x.value))
    print("----------")
    return ket("bar chart")


# 15/9/2016:
# recall a learned high-order sequence, and print it out.
# see:
# Using the proposed swc language:
# (which I'm never going to be able to write a compiler for! and is almost certainly going to be a tar-pit)
#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# current |node> => start-node |input ket>
# while name current |node> /= |end of sequence>:
#   print name current |node>
#   current |node> => next current |node>
# print |end of sequence>
#
# one is a ket
def recall_sequence(one, context):
    if len(one.apply_op(context, "start-node")) == 0:  # we don't know the start-node, so return the input ket
        return one
    print("recall sequence:", one)
    context.learn("current", "node", one.apply_op(context, "start-node"))
    name = context.recall("current", "node").apply_fn(extract_category).similar_input(context, "encode").select_range(1,
                                                                                                                      1).apply_sigmoid(
        clean)
    while name.the_label() != "end of sequence":
        print(name)
        context.learn("current", "node",
                      ket("node").apply_op(context, "current").similar_input(context, "pattern").select_range(1,
                                                                                                              1).apply_sigmoid(
                          clean).apply_op(context, "then"))
        name = context.recall("current", "node").apply_fn(extract_category).similar_input(context,
                                                                                          "encode").select_range(1,
                                                                                                                 1).apply_sigmoid(
            clean)
    #  print(name)
    return name


# recall a chunked high order sequence, and print it out.
#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# not |yes> => |no>
# not |no> => |yes>
#
# if not do-you-know start-node |input ket>:
#   return |input ket>
# current |node L2> => start-node |input ket>
# while name current |node L2> /= |end of sequence>:
#   current |node L1> => start-node name current |node L2>
#   while name current |node L1> /= |end of sequence>:
#     print name current |node L1>
#     current |node L1> => next current |node L1>
#   current |node L2> => next current |node L2>
# print |end of sequence>
#
# one is a ket
def recall_chunked_sequence(one, context):
    if len(one.apply_op(context, "start-node")) == 0:  # we don't know the start-node, so return the input ket
        return one
    print("recall chunked sequence:", one)
    context.learn("current", "node L2", one.apply_op(context, "start-node"))
    name2 = context.recall("current", "node L2").apply_fn(extract_category).similar_input(context,
                                                                                          "encode").select_range(1, 1)
    while name2.the_label() != "end of sequence":

        context.learn("current", "node L1", name2.apply_op(context, "start-node"))
        name1 = context.recall("current", "node L1").apply_fn(extract_category).similar_input(context,
                                                                                              "encode").select_range(1,
                                                                                                                     1).apply_sigmoid(
            clean)
        while name1.the_label() != "end of sequence":
            print(name1)
            context.learn("current", "node L1",
                          ket("node L1").apply_op(context, "current").similar_input(context, "pattern").select_range(1,
                                                                                                                     1).apply_sigmoid(
                              clean).apply_op(context, "then"))
            name1 = context.recall("current", "node L1").apply_fn(extract_category).similar_input(context,
                                                                                                  "encode").select_range(
                1, 1).apply_sigmoid(clean)

        context.learn("current", "node L2",
                      ket("node L2").apply_op(context, "current").similar_input(context, "pattern").select_range(1,
                                                                                                                 1).apply_sigmoid(
                          clean).apply_op(context, "then"))
        name2 = context.recall("current", "node L2").apply_fn(extract_category).similar_input(context,
                                                                                              "encode").select_range(1,
                                                                                                                     1).apply_sigmoid(
            clean)
    return name2


# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# not |yes> => |no>
# not |no> => |yes>
#
# spell (*) #=>
#   if not do-you-know first-letter |_self>:
#     return |_self>
#   current |node> => first-letter |_self>
#   while name current |node> /= |end of sequence>:
#     print name current |node>
#     current |node> => next current |node>
#   return |end of sequence>
#
# code to spell words
#
# one is a ket
def spell(one, context):
    start = one.apply_op(context, "first-letter")
    if len(start) == 0:  # we don't know the first letter, so return the input ket
        return one
    print("spell word:", one)
    context.learn("current", "node", start)
    name = context.recall("current", "node", True).apply_fn(extract_category).similar_input(context,
                                                                                            "encode").select_range(1,
                                                                                                                   1).apply_sigmoid(
        clean)
    while name.the_label() != "end of sequence":
        print(name)
        #    bar_chart(name,'80')
        context.learn("current", "node",
                      ket("node").apply_op(context, "current").similar_input(context, "pattern").select_range(1,
                                                                                                              1).apply_sigmoid(
                          clean).apply_op(context, "then"))
        name = context.recall("current", "node", True).apply_fn(extract_category).similar_input(context,
                                                                                                "encode").select_range(
            1, 1).apply_sigmoid(clean)
    #  print(name)
    return name


# 25/9/2016:
# recall a learned chunked high-order sequence, of arbitrary depth, and print it out.
#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# NB: this pseudo-code is out of date! Update it!!
# if not do-you-know start-node |input ket>:
#   return |input ket>
# current |node> => start-node |input ket>
# while name current |node> /= |end of sequence>:
#   print name current |node>
#   current |node> => next current |node>
# print |end of sequence>
#
# Let's try to update the pseudo-code:
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# print-sequence (*,*) #=>
#   if not do-you-know start-node |_self1>:
#     return |_self1>
#   if name start-node |_self1> == |_self1>:                  -- prevent infinite loop
#     print |_self1>
#     return |>
#   |node> => |_self2>
#   current "" |node> => start-node |_self1>
#   while name current "" |node> != |end of sequence>:
#     if not do-you-know start-node name current "" |node>:
#       print name current "" |node>
#     else:
#       print-sequence(name current "" |node>, plus[1] "" |node>)
#     current "" |node> => next current "" |node>
#   return |end of sequence>
#
# Invoke using:
# print-sequence(|alphabet>, |seq node: 1>)              -- need a version that doesn't need to pass in the sequence node! Need a GUID generator! How implement that??
#
# one is a ket
def print_sequence(one, context, start_node=None, node_id=1):
    if start_node is None:  # so we can change the operator name that links to the first element in the sequence.
        start_node = "start-node"
    if len(one.apply_op(context, start_node)) == 0:  # we don't know the start-node, so return the input ket
        return one
    print("print sequence:", one)
    if one.apply_op(context, start_node).apply_fn(extract_category).similar_input(context, "encode").select_range(1,
                                                                                                                  1).apply_sigmoid(
            clean).the_label() == one.the_label():  # need to implement 'sp1 == sp2' at some stage.
        print(one)  # infinte loop when object is its own sequence.
        return ket("")
    node = "seq node: " + str(node_id)
    context.learn("current", node, one.apply_op(context, start_node))
    name = context.recall("current", node).apply_fn(extract_category).similar_input(context, "encode").select_range(1,
                                                                                                                    1).apply_sigmoid(
        clean)
    while name.the_label() != "end of sequence":
        has_start_node = name.apply_op(context, start_node)
        if len(has_start_node) == 0:
            print(name)
        else:
            print_sequence(name, context, start_node, node_id + 1)
        context.learn("current", node,
                      ket(node).apply_op(context, "current").similar_input(context, "pattern").select_range(1,
                                                                                                            1).apply_sigmoid(
                          clean).apply_op(context, "then"))
        name = context.recall("current", node).apply_fn(extract_category).similar_input(context, "encode").select_range(
            1, 1).apply_sigmoid(clean)
    return name


#
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# print-sequence |*> #=>                                      -- I don't see the advantage of this function over the python! Why should my language exist??
#   if not do-you-know start-node |_self>:
#     return |_self>
#   if name start-node |_self> == |_self>:                    -- prevent infinite loop
#     print |_self>
#     return |>
#   |node> => new-GUID |>                                     -- feels like a hack!
#   current "" |node> => start-node |_self>
#   while name current "" |node> != |end of sequence>:
#     if not do-you-know start-node name current "" |node>:
#       print name current "" |node>
#     else:
#       print-sequence name current "" |node>
#     current "" |node> => next current "" |node>
#   return |end of sequence>
#
# Invoke using:
# print-sequence |alphabet>
#
def new_print_sequence(one, context, start_node=None):
    if start_node is None:  # so we can change the operator name that links to the first element in the sequence.
        start_node = "start-node"
    if len(one.apply_op(context, start_node)) == 0:  # if we don't know the start-node, return the input ket
        return one
    print("print sequence:", one)

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    if name(one.apply_op(context,
                         start_node)).the_label() == one.the_label():  # need to implement 'sp1 == sp2' at some stage so we don't need .the_label()
        print(
            one)  # prevent infinte loop when object is its own sequence. Maybe should have handled at learn stage, not recall?
        return ket("")
    current_node = one.apply_op(context, start_node)
    while name(current_node).the_label() != "end of sequence":
        if len(name(current_node).apply_op(context, start_node)) == 0:
            print(name(current_node))
        else:
            new_print_sequence(name(current_node), context, start_node)
        current_node = next(current_node)
    return ket("end of sequence")


# 29/9/2016:
# discrimination. The difference in coeff between the highest and the next highest
# Bah! Seems I have already implemented it over in the ket and sp classes.
#
def discrimination(one):
    if len(one) == 0:
        return ket("discrimination", 0)
    if len(one) == 1:
        return ket("discrimination")
    r = one.coeff_sort().normalize()
    first = r.data[0].value  # yeah, breaks the superposition class abstraction. Fix later!
    second = r.data[1].value
    return ket("discrimination", first - second)


# 5/10/2016
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# follow-sequence (*) #=>
#   current |node> => |_self>
#   while name current |node> /= |end of sequence>:
#     print name current |node>
#     current |node> => next current |node>
#   return |end of sequence>
#
# code to follow a sequence
#
# one is a sp
def old_follow_sequence(one, context):
    if len(one) == 0:
        return one
    context.learn("current", "node", one)
    name = context.recall("current", "node", True).apply_fn(extract_category).similar_input(context,
                                                                                            "encode").select_range(1,
                                                                                                                   1).apply_sigmoid(
        clean)
    while name.the_label() != "end of sequence":
        print(name)
        context.learn("current", "node",
                      ket("node").apply_op(context, "current").similar_input(context, "pattern").select_range(1,
                                                                                                              1).apply_sigmoid(
                          clean).apply_op(context, "then"))
        name = context.recall("current", "node", True).apply_fn(extract_category).similar_input(context,
                                                                                                "encode").select_range(
            1, 1).apply_sigmoid(clean)
    return name


# 17/11/2016
# next (*) #=> then clean select[1,1] similar-input[pattern] |_self>
# name (*) #=> clean select[1,1] similar-input[encode] extract-category |_self>
#
# follow-sequence[op] (*) #=>
#   current |node> => |_self>
#   while name current |node> /= |end of sequence>:
#     op name current |node>                              -- NB: "op" instead of "print"
#     current |node> => next current |node>
#   return |end of sequence>
#
# code to follow a sequence
#
# one is a sp
def follow_sequence(one, context, op=None):
    if len(one) == 0:
        return one

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    current_node = one
    while name(current_node).the_label() != "end of sequence":
        if op == None:
            print(name(current_node))
        else:
            name(current_node).apply_op(context, op)
        current_node = next(current_node)
    return ket("end of sequence")


# 25/11/2016:
# code to display a sequence in dot format. eg: |the> . |dog> . |sat>
#
# one is a sp
def display_sequence(one, context, op=None):
    if len(one) == 0:
        return one

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    current_node = one
    node_names = []
    while name(current_node).the_label() != "end of sequence":
        if op == None:
            #      node_names.append(str(name(current_node)))
            node_names.append(name(current_node).the_label())
        else:
            name(current_node).apply_op(context, op)
        current_node = next(current_node)
    #  print(" . ".join(node_names))
    print("|%s>" % " . ".join(node_names))
    return ket("end of sequence")


# 20/11/2016:
# code to recall a sentence
# hrm... seems to work. Needs tidying though.
#
# Usage:
# load sentence-sequence--multi-layer.sw
# print-sentence |*> #=> recall-sentence pattern |_self>
# print-sentence |node 200: 1>
#
#
# one is a sp
def recall_sentence(one, context):
    if len(one) == 0:
        return one
    current_node = one

    #  current_node = one.apply_op(context,"pattern")
    #  if len(current_node) == 0:
    #    return one

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def old_has_start_node(one):  # check if one is a class
        two = ket(
            one.the_label() + ": 1")  # this breaks if you use: |A: 0> or |A: 1> for your first node. What is a tidy fix?
        return len(two.apply_op(context, "start-node")) > 0

    def has_start_node(one):  # check if one is a class
        two = ket(one.the_label() + ": ")  # see if this fixes the |A: 0> vs |A: 1> as first node bug.
        return len(two.apply_fn(starts_with, context).select_range(1, 1).apply_op(context, "start-node")) > 0

    # python: x.apply_op(context,"append-colon").apply_fn(starts_with,context).pick_elt().apply_op(context,"start-node").apply_sp_fn(follow_sequence,context)
    def get_start_node(one):
        two = ket(one.the_label() + ": ")
        return two.apply_fn(starts_with, context).pick_elt().apply_op(context, "start-node")

    while name(current_node).the_label() != "end of sequence":
        if not has_start_node(name(current_node)):
            print(name(current_node))
        else:
            #      print("%s has start node" % name(current_node))
            start_node = get_start_node(name(current_node))
            recall_sentence(start_node, context)
        current_node = next(current_node)
    return ket("end of sequence")


# 23/11/2016:
# hopefully improved version of recall-sentence:
# usage: recall-sentence-v2 sentence |R>
#
# one is a sp
def recall_sentence_v2(one, context):
    if len(one) == 0:
        return one
    #  current_node = one
    current_node = one.apply_op(context, "pattern")
    if len(current_node) == 0:
        return one

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    #  def has_start_node(one):                                            # check if one is a class
    #    return len(one.apply_op(context,"start-nodes")) > 0
    def get_start_node(one):
        return one.apply_op(context, "start-nodes").weighted_pick_elt()  # need clean?

    while name(current_node).the_label() != "end of sequence":
        start_node = get_start_node(name(current_node))
        if len(start_node) == 0:  # check if one is a class
            print(name(current_node))
        else:
            recall_sentence_v2(start_node, context)
        current_node = next(current_node)
    return ket("end of sequence")


# 10/10/2016
# whats_next(sp)
# whats_next(sp,sp)
# whats_next(sp,sp,sp)
# ...
# ie, given learned high order sequences of SDR's, predict what the next SDR is going to be.
#
# then drop-below[t] similar-input[pattern] sp1
# then intersection(drop-below[t] similar-input[pattern] then drop-below[t] similar-input[pattern] sp1, drop-below[t] similar-input[pattern] sp2)
# then intersection(drop-below[0.09] similar-input[pattern] then drop-below[0.09] similar-input[pattern] input-encode |f>, drop-below[0.09] similar-input[pattern] input-encode |f>)
# or ...
# find-pattern (*) #=> drop-below[t] similar-input[pattern] |_self>
# then find-pattern sp1
# then intersection(find-pattern then find-pattern sp1, find-pattern sp2)
# then intersection(find-pattern then find-pattern then find-pattern sp1, find-pattern then find-pattern sp2, find-pattern sp3)
#
# one is a sp
def whats_next_one(context, one):
    pattern = "pattern"
    then = "then"
    t = 0.09
    return one.similar_input(context, pattern).drop_below(t).apply_op(context, then)


# bah! I can't get it to work.... Not sure where the bug is.
# Hrmm... I think it is from "then similar-input[pattern]" applied to more than one pattern at a time.
# Maybe not. Since this works:
# next-step-op |*> #=> ket-sort similar-input[encode] extract-category then drop-below[0.09] similar-input[pattern] input-encode |_self>
#
# one, two are sp's
def first_attempt_whats_next_two(context, one, two):
    pattern = "pattern"
    then = "then"
    t1 = 0.09
    t2 = 0.8
    nodes_one = one.similar_input(context, pattern).drop_below(t1).apply_op(context, then).similar_input(context,
                                                                                                         pattern).rescale()
    nodes_two = two.similar_input(context, pattern).drop_below(t1)
    #  return intersection(nodes_one,nodes_two).apply_op(context,then)
    print("nodes_one:", nodes_one)
    print("nodes_two:", nodes_two)
    return intersection(nodes_two, nodes_one)  # I should look into optimizing intersection!


# one, two and three are sp's
def whats_next_three(context, one, two, three):
    pattern = "pattern"
    then = "then"
    t = 0.09
    nodes_one = one.similar_input(context, pattern).drop_below(t).apply_op(context, then).similar_input(context,
                                                                                                        pattern).drop_below(
        t).apply_op(context, then).similar_input(context, pattern).drop_below(t)
    nodes_two = two.similar_input(context, pattern).drop_below(t).apply_op(context, then).similar_input(context,
                                                                                                        pattern).drop_below(
        t)
    nodes_three = three.similar_input(context, pattern).drop_below(t)
    return intersection(intersection(nodes_one, nodes_two), nodes_three).apply_op(context, then)


# bah! Try another approach!
# I don't even know if it is correct!....
#
# one, two are sp's
def whats_next_two(context, one, two):
    pattern = "pattern"
    then = "then"
    t1 = 0.09
    t2 = 0.8
    nodes_one = one.similar_input(context, pattern).drop_below(t1)
    nodes_two = two.similar_input(context, pattern).drop_below(t1)
    r = superposition()
    for x in nodes_one:
        #    y = x.apply_sigmoid(clean).apply_op(context,then).similar_input(context,pattern).drop_below(t1)               # maybe select[1,1] instead of drop-below
        y = ket(x.label).apply_op(context, then).similar_input(context, pattern).select_range(1, 1).apply_sigmoid(clean)
        #    z = intersection(y,nodes_two)                                          # value = two.find_value(e)
        #    z = ket(nodes_two.find_value(y))
        z = mbr(y, nodes_two)
        r += z
    return r


#  return intersection(nodes_one,nodes_two).apply_op(context,then)
#  print("nodes_one:",nodes_one)
#  print("nodes_two:",nodes_two)
#  return intersection(nodes_two,nodes_one)                             # I should look into optimizing intersection!

# 24/11/2016:
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "a cat sat on the mat"
# Given a word, predict what word follows.
# eg: predict-whats-next(|a>) == |cat>
# eg: predict-whats-next(|the>) == 2|dog> + |ball> + |mat>
#
# Cool, seems to work. Next up, the 2 word version.
#
# later, implement a sequence version
#
# one is a sp
def predict_whats_next_one(context, one):
    if len(one) == 0:  # if it is the empty sp, we can't do anything.
        return one

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def get_node(one):
        return one.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context,
                                                                                           "pattern").drop_below(0.09)

    def then(one):
        return one.apply_op(context, "then")

    def follow_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(follow_sequence, context)

    nodes_one = get_node(one)
    print("nodes:", nodes_one)
    if len(nodes_one) == 1:
        return follow_node_sequence(nodes_one)

    r = superposition()
    for x in nodes_one:
        print(name(then(x)))
        r += name(then(x))
    return r


# 24/11/2016
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "a cat sat on the mat"
# Given two words, predict what word follows.
# eg: predict-whats-next(|a>, |cat>) == |sat>
# eg: predict-whats-next(|the>, |dog>) == |wants> + |chased>
#
# Cool, seems to work. Next up, the three word version.
#
# later, implement a sequence version. I guess by passing in the relevant node of a sequence.
#
# one and two are sp's
def predict_whats_next_two(context, one, two):
    if len(one) == 0:  # if it is the empty sp, we can't do anything.
        return one
    if len(two) == 0:  # if two == |> then feed it to the one word version of predict-whats-next()
        return predict_whats_next_one(context, one)

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def get_node(one):
        return one.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context,
                                                                                           "pattern").drop_below(0.09)

    def then(one):
        return one.apply_op(context, "then")

    def get_next_node(one):
        return one.similar_input(context, "pattern").select_range(1,
                                                                  1)  # .apply_sigmoid(clean).apply_op(context,"then")

    def follow_node_sequence(one):
        #    return one.apply_op(context,"pattern").apply_sp_fn(follow_sequence,context)
        return one.apply_op(context, "then").apply_sp_fn(follow_sequence, context)

    nodes_one = get_node(one)
    print("nodes 1:", nodes_one)
    nodes_two = get_node(two)
    print("nodes 2:", nodes_two)
    next_nodes = superposition()
    for x in nodes_one:
        next_nodes += get_next_node(then(x))
    intersected_nodes = intersection(next_nodes, nodes_two)
    print("intersected nodes:", intersected_nodes)
    if len(intersected_nodes) == 1:
        return follow_node_sequence(intersected_nodes)
    else:
        r = superposition()
        for x in intersected_nodes:
            print(name(then(x)))
            r += name(then(x))
        return r


# 25/11/2016
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "a cat sat on the mat"
# Given three words, predict what word follows.
# eg: predict-whats-next(|a>, |cat>, |sat>) == |on>
# eg: predict-whats-next(|the>, |dog>, |wants>) == |food>
#
# Cool, seems to work. Next up, the sequence version. Probably by passing in the start node of a sequence.
#
# one, two and three are sp's
def predict_whats_next_three(context, one, two, three):
    if len(one) == 0:  # if it is the empty sp, we can't do anything.
        return one
    if len(two) == 0:  # if two == |> then feed it to the one word version of predict-whats-next()
        return predict_whats_next_one(context, one)
    if len(three) == 0:
        return predict_whats_next_two(context, one, two)

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def get_node(one):
        return one.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context,
                                                                                           "pattern").drop_below(0.09)

    def then(one):
        return one.apply_op(context, "then")

    def get_next_node(one):
        return one.similar_input(context, "pattern").select_range(1,
                                                                  1)  # .apply_sigmoid(clean).apply_op(context,"then")

    def follow_node_sequence(one):
        #    return one.apply_op(context,"pattern").apply_sp_fn(follow_sequence,context)
        return one.apply_op(context, "then").apply_sp_fn(follow_sequence, context)

    nodes_one = get_node(one)
    print("nodes 1:", nodes_one)
    nodes_two = get_node(two)
    print("nodes 2:", nodes_two)
    nodes_three = get_node(three)
    print("nodes 3:", nodes_three)

    next_nodes = superposition()
    for x in nodes_one:
        next_nodes += get_next_node(then(x))
    intersected_nodes = intersection(next_nodes, nodes_two)
    print("intersected nodes:  ", intersected_nodes)
    if len(intersected_nodes) == 1:
        return follow_node_sequence(intersected_nodes)

    next_nodes2 = superposition()
    for x in intersected_nodes:
        next_nodes2 += get_next_node(then(x))
    intersected_nodes2 = intersection(next_nodes2, nodes_three)
    print("intersected nodes 2:", intersected_nodes2)
    if len(intersected_nodes2) == 1:
        return follow_node_sequence(intersected_nodes2)

    r = superposition()
    for x in intersected_nodes2:
        print(name(then(x)))
        r += name(then(x))
    return r


# 25/11/2016:
# skip version.
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "the very hungry dog wants some food"
# predict-whats-next-skip(|the>, |dog>) == 2|wants> + |chased>
# NB: the 2nd |wants> from the third sentence, where we skip "very hungry"
#
# seems to work.
#
# one and two are sp's
def predict_whats_next_skip_two(context, one, two):
    if len(one) == 0:  # if it is the empty sp, we can't do anything.
        return one
    if len(two) == 0:  # if two == |> then feed it to the one word version of predict-whats-next()
        return predict_whats_next_one(context, one)

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def get_node(one):
        return one.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context,
                                                                                           "pattern").drop_below(0.09)

    def then(one):
        return one.apply_op(context, "then")

    def get_next_node(one):
        return one.similar_input(context, "pattern").select_range(1,
                                                                  1)  # .apply_sigmoid(clean).apply_op(context,"then")

    def follow_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(follow_sequence, context)

    def display_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(display_sequence, context)

    def get_next_nodes(one):
        r = superposition()
        for x in one:
            r += get_next_node(then(x))
        return r

    def name_next_nodes(one):
        r = superposition()
        for x in one:
            r += name(then(x))
        return r

    nodes_one = get_node(one)
    print("nodes 1:", nodes_one)
    nodes_two = get_node(two)
    print("nodes 2:", nodes_two)
    next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(
        get_next_nodes(get_next_nodes(nodes_one)))  # improve later.
    intersected_nodes = intersection(next_nodes, nodes_two)
    print("intersected nodes:", intersected_nodes)
    #  if len(intersected_nodes) == 1:
    #    return follow_node_sequence(intersected_nodes)
    for x in intersected_nodes:
        display_node_sequence(x)
    return name_next_nodes(intersected_nodes)


# 25/11/2016:
# skip version.
# Given these three simple sentences:
# "the dog wants food"
# "the dog chased the ball"
# "the very hungry dog wants some food"
# predict-whats-next-skip(|the>, |dog>) == 2|wants> + |chased>
# NB: the 2nd |wants> from the third sentence, where we skip "very hungry"
#
# seems to work.
#
# one, two and three are sp's
def predict_whats_next_skip_three(context, one, two, three):
    if len(one) == 0:  # if it is the empty sp, we can't do anything.
        return one
    if len(two) == 0:  # if two == |> then feed it to the one word version of predict-whats-next()
        return predict_whats_next_one(context, one)
    if len(three) == 0:
        return predict_whats_next_skip_two(context, one, two)

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def get_node(one):
        return one.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context,
                                                                                           "pattern").drop_below(0.09)

    def then(one):
        return one.apply_op(context, "then")

    def get_next_node(one):
        return one.similar_input(context, "pattern").select_range(1,
                                                                  1)  # .apply_sigmoid(clean).apply_op(context,"then")

    def follow_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(follow_sequence, context)

    def display_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(display_sequence, context)

    def get_next_nodes(one):
        r = superposition()
        for x in one:
            r += get_next_node(then(x))
        return r

    def name_next_nodes(one):
        r = superposition()
        for x in one:
            r += name(then(x))
        return r

    nodes_one = get_node(one)
    print("nodes 1:", nodes_one)
    nodes_two = get_node(two)
    print("nodes 2:", nodes_two)
    nodes_three = get_node(three)
    print("nodes 3:", nodes_three)

    next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(
        get_next_nodes(get_next_nodes(nodes_one)))  # improve later.
    intersected_nodes = intersection(next_nodes, nodes_two)
    print("intersected nodes  :", intersected_nodes)
    #  if len(intersected_nodes) == 1:                           # slight "stutter". Not sure how to best fix. If at all.
    #    return follow_node_sequence(intersected_nodes)          # eg: predict-whats-next-skip(|the>,|hungry>,|dog>) == |dog>.|wants>.|some>.|food>
    # also: predict-whats-next-skip(|the>,|hungry>,|fish>) == |dog>.|wants>.|some>.|food>
    next_nodes2 = get_next_nodes(intersected_nodes) + get_next_nodes(
        get_next_nodes(intersected_nodes)) + get_next_nodes(get_next_nodes(
        get_next_nodes(intersected_nodes)))  # improve later. Also has slight tolerance for order changes.
    intersected_nodes2 = intersection(next_nodes2, nodes_three)  # bug or feature?
    print("intersected nodes 2:", intersected_nodes2)
    #  if len(intersected_nodes2) == 1:                           # if len > 1, use pick-elt??
    #    return follow_node_sequence(intersected_nodes2)
    for x in intersected_nodes2:
        display_node_sequence(x)
    return name_next_nodes(intersected_nodes2)


# one, two, three and four are sp's
def predict_whats_next_skip_four(context, one, two, three, four):
    if len(one) == 0:  # if it is the empty sp, we can't do anything.
        return one
    if len(two) == 0:  # if two == |> then feed it to the one word version of predict-whats-next()
        return predict_whats_next_one(context, one)
    if len(three) == 0:
        return predict_whats_next_skip_two(context, one, two)

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def get_node(one):
        return one.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context,
                                                                                           "pattern").drop_below(0.09)

    def then(one):
        return one.apply_op(context, "then")

    def get_next_node(one):
        return one.similar_input(context, "pattern").select_range(1,
                                                                  1)  # .apply_sigmoid(clean).apply_op(context,"then")

    def follow_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(follow_sequence, context)

    def display_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(display_sequence, context)

    def get_next_nodes(one):
        r = superposition()
        for x in one:
            r += get_next_node(then(x))
        return r

    def name_next_nodes(one):
        r = superposition()
        for x in one:
            r += name(then(x))
        return r

    nodes_one = get_node(one)
    print("nodes 1:", nodes_one)
    nodes_two = get_node(two)
    print("nodes 2:", nodes_two)
    nodes_three = get_node(three)
    print("nodes 3:", nodes_three)
    nodes_four = get_node(four)
    print("nodes 4:", nodes_four)

    next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(
        get_next_nodes(get_next_nodes(nodes_one)))  # improve later.
    intersected_nodes = intersection(next_nodes, nodes_two)
    print("intersected nodes  :", intersected_nodes)
    next_nodes2 = get_next_nodes(intersected_nodes) + get_next_nodes(
        get_next_nodes(intersected_nodes)) + get_next_nodes(get_next_nodes(
        get_next_nodes(intersected_nodes)))  # improve later. Also has slight tolerance for order changes.
    intersected_nodes2 = intersection(next_nodes2, nodes_three)  # bug or feature?
    print("intersected nodes 2:", intersected_nodes2)

    next_nodes3 = get_next_nodes(intersected_nodes2) + get_next_nodes(
        get_next_nodes(intersected_nodes2)) + get_next_nodes(get_next_nodes(
        get_next_nodes(intersected_nodes2)))  # improve later. Also has slight tolerance for order changes.
    intersected_nodes3 = intersection(next_nodes3, nodes_four)  # bug or feature?
    print("intersected nodes 3:", intersected_nodes3)

    for x in intersected_nodes3:
        display_node_sequence(x)
    return name_next_nodes(intersected_nodes3)


# 29/11/2016:
# sequence version of  whats-next.
# eg: next |the . dog . chased> == |the . ball>
#
# one is a sequence ket, eg |the . dog . chased>, or |the . mother . of . george . is>
# sort of a hack until we make sequences first class objects, if we ever do.
#
# def sequence_predict_whats_next_skip(context,one):
def sequence_predict_whats_next_skip(one, context, parameters=None):
    if len(one) == 0:  # if it is the empty sp, we can't do anything.
        return one
    try:
        k = int(parameters)
    except:
        k = 3
    incoming_sequence = [x.strip() for x in one.the_label().split('.')]
    print("incoming_sequence:", incoming_sequence)

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    def get_node(one):
        return one.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context,
                                                                                           "pattern").drop_below(0.09)

    def then(one):
        return one.apply_op(context, "then")

    def get_next_node(one):
        return one.similar_input(context, "pattern").select_range(1,
                                                                  1)  # .apply_sigmoid(clean).apply_op(context,"then")

    def follow_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(follow_sequence, context)

    def display_node_sequence(one):
        return one.apply_op(context, "then").apply_sp_fn(display_sequence, context)

    def get_next_nodes(one):
        r = superposition()
        for x in one:
            r += get_next_node(then(x))
        return r

    def name_next_nodes(one):
        r = superposition()
        for x in one:
            r += name(then(x))
        return r

    nodes_one = get_node(ket(incoming_sequence[0]))

    for x in incoming_sequence[1:]:
        print("nodes 1:", nodes_one)
        nodes_two = get_node(ket(x))
        #    next_nodes = get_next_nodes(nodes_one) + get_next_nodes(get_next_nodes(nodes_one)) + get_next_nodes(get_next_nodes(get_next_nodes(nodes_one))) + get_next_nodes(get_next_nodes(get_next_nodes(get_next_nodes(nodes_one))))
        next_nodes = get_next_nodes(nodes_one)
        r = next_nodes
        for _ in range(k):
            r = get_next_nodes(r)
            next_nodes += r
        intersected_nodes = intersection(next_nodes, nodes_two)
        print("intersected nodes:", intersected_nodes)
        nodes_one = intersected_nodes
    for x in nodes_one:
        display_node_sequence(x)
    return name_next_nodes(nodes_one)


# 5/11/2016:
# vsa-mult(sp1,sp2)
# eg:
# vsa-mult(|name>,|usa>) == |name: usa>
#
# one, two are superpositions
def vsa_mult(one, two):
    r = superposition()
    for x in one:
        for y in two:
            x_pieces = x.label.split(": ")
            y_pieces = y.label.split(": ")
            pieces = x_pieces + y_pieces
            print("pieces:", pieces)
            new_pieces = []
            for p in pieces:
                if p in x_pieces and p in y_pieces:  # not pefect, but works for now.
                    continue
                new_pieces.append(p)
            #      new_pieces.sort()
            r += ket(": ".join(new_pieces))
    return r


import random
from itertools import product


# 9/12/2016:
# random-frame[w,h,on-bits]
# display-frame[w,h] frame |3>
#
def random_frame(parameters):
    try:
        w, h, bits = [int(x) for x in parameters.split(',')]
        pixels = [x for x in product(range(w), range(h))]
        on_pixels = random.sample(pixels, bits)
        r = superposition()
        for pair in on_pixels:
            r += ket("%s: %s" % (pair[0], pair[1]))
        return r
    except Exception as e:
        print("random_frame exception reason:", e)
        return ket("")


def display_frame(one, parameters):
    try:
        w, h = [int(x) for x in parameters.split(',')]
        on_pixels = [x.label.split(": ") for x in one]
        on_pixels = [(int(x), int(y)) for x, y in on_pixels]  # tidy later?
        #    print("on-pixels: %s" % on_pixels)
        for y in range(h):
            for x in range(w):
                if (x, y) in on_pixels:
                    print("#", end='')
                else:
                    print(".", end='')
            print()
        print()
        return ket("display-frame")
    except Exception as e:
        print("display_frame exception reason:", e)
        return ket("")


# display-frame-sequence[10,10] start-node |seq 1>
#
# one is a sp
def display_frame_sequence(one, context, parameters):
    if len(one) == 0:
        return one

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "frame").select_range(1, 1).apply_sigmoid(clean)

    def display_our_frame(one, parameters):
        display_frame(one.apply_fn(extract_category), parameters)

    try:
        current_node = one.apply_op(context, "pattern")
        while name(current_node).the_label() != "end of sequence":
            #    print(name(current_node))
            #    display_frame(name(current_node).apply_op(context,"frame"), parameters)
            display_our_frame(current_node, parameters)
            current_node = next(current_node)
        return ket("end of sequence")

    except Exception as e:
        print("display_frame_sequence exception reason:", e)
        return ket("")


# 6/6/2017:
# Given we have learnt this sequence:
# |3> . |1> . |4> . |1> . |5>
# we want this output:
# sa: float-sequence |3.2>
# 0.992 |3> . |1> . |4> . |1> . |5>
# 0.191 |4> . |1> . |5>
#
# sa: float-sequence |1.3>
# 0.928 |1> . |4> . |1> . |5>
# 0.928 |1> . |5>
# 0.0   |3> . |1> . |4> . |1> . |5>
#
# Improved, so now handles sequence-names, and input sequences longer than 1:
# sa: load pi-e-sequences.sw
# sa: float-sequence |3.3 . 1 . 4.2>
# Pi  0.664  |3> . |1> . |4> . |1> . |5> . |9> . |2> . |6> . |5> . |3> . |5>
# Pi  0.078  |4> . |1> . |5> . |9> . |2> . |6> . |5> . |3> . |5>
# Pi  0.0    |5> . |3> . |5>
#
# sa: float-sequence |2 . 8 . 2>
# e  0.071  |1> . |8> . |2> . |8> . |1> . |8> . |2> . |8> . |4>
# e  0.071  |1> . |8> . |2> . |8> . |4>
# e  0.027  |2> . |8> . |1> . |8> . |2> . |8> . |4>
# e  0.027  |2> . |7> . |1> . |8> . |2> . |8> . |1> . |8> . |2> . |8> . |4>
# e  0.0    |2> . |8> . |4>
#
# NB: important for float_sequence to work that we have an appropriate "encode" operator defined.
# eg: encode |*> #=> rescale smooth[0.1]^10 |_self>
#
# Now, the approximate mathematics this is doing:
# Given input sequence |v1> . |v2> . |v3>
# find x such that f(x) approx-eq v1 and f(x + delta) approx-eq  v2 and f(x + 2*delta) approx-eq v3
# where the exact meaning of "a approx-eq b" is a consequence of how you define your encode operator
#
def float_sequence(one, context, parameters=None):
    def similar_pattern(x, context):
        return x.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context, "pattern").multiply(
            10)

    def filter_working_table(table, element, position):
        # print("%s: %s" % (position, element))
        element_pattern = ket(element).apply_op(context, "encode")
        new_table = []
        for name, coeff, seq in table:
            try:
                seq_element = seq[position]
                seq_element_pattern = seq_element.apply_op(context, "encode")
                # print("seq_element:",seq_element)
                # print("seq_element_pattern:",seq_element_pattern)
                similarity = fast_simm(element_pattern, seq_element_pattern)
                # print("simm:",similarity)
                new_coeff = min(coeff, similarity)
                if new_coeff > 0:
                    new_table.append([name, new_coeff, seq])
            except:
                continue
        return new_table

    def format_output_table(working_table):
        # first, sort the table:
        sorted_working_table = sorted(working_table, key=lambda x: x[1], reverse=True)

        # now format it:
        table = []
        for name, coeff, seq in sorted_working_table:
            coeff_str = float_to_int(coeff)
            seq_str = " . ".join(str(x) for x in seq)
            table.append([name, coeff_str, seq_str])
        return table

    # handle: float-sequence |3.2 . 1.3 . 4>:
    input_sequence = one.the_label().split(' . ')
    logger.info("input sequence: " + str(input_sequence))
    one = ket(input_sequence[0])

    # generate working_table:
    r = similar_pattern(one, context)
    working_table = []
    for x in r:
        name = x.apply_op(context, "sequence-name").the_label()
        coeff = x.value
        seq = sequence_to_list(x, context)
        working_table.append([name, coeff, seq])

    # filter working_table using the rest of our input sequence:
    for k, element in enumerate(input_sequence[1:]):
        working_table = filter_working_table(working_table, element, k + 1)

        # don't format and print an empty table:
    if len(working_table) == 0:
        return ket("")

    # format and print output table:
    print_table(format_output_table(working_table))
    return ket("float-sequence")


def sequence_to_list(one, context, length=None):
    if len(one) == 0:
        return one

    def next(one):
        return one.similar_input(context, "pattern").select_range(1, 1).apply_sigmoid(clean).apply_op(context, "then")

    def name(one):
        return one.apply_fn(extract_category).similar_input(context, "encode").select_range(1, 1).apply_sigmoid(clean)

    current_pattern = one.apply_op(context, "pattern")
    node_names = []
    #  print("one:",one)
    #  print("current_pattern:", current_pattern)
    #  print("name current_pattern:", name(current_pattern))
    while name(current_pattern).the_label() != "end of sequence":
        #    node_names.append(str(name(current_pattern)))
        node_names.append(name(current_pattern))
        current_pattern = next(current_pattern)
    return node_names


# pretty print a table:
# table print tweaked from here: http://stackoverflow.com/questions/25403249/print-a-list-of-tuples-as-table
def print_table(table):
    max_length_column = []
    tuple_len = len(table[0])  # assume entire table has the same shape as the first row
    for i in range(tuple_len):
        max_length_column.append(max(len(e[i]) + 2 for e in table))
    for e in table:
        for i in range(tuple_len):
            print(e[i].ljust(max_length_column[i]), end='')
        print()


# spell-out |fish> => |f> . |i> . |s> . |h>
# AKA: ssplit |fish> => |f> . |i> . |s> . |h>
def spell_out(one):
    seq = sequence([])
    if type(one) in [ket, superposition]:
        for x in one:
            for c in list(x.label):
                seq += ket(c, x.value)
    return seq


# ---------------------------------------------------------------------------------------
# start of new functions file:
import math
from math import factorial

# define our usage dictionaries:
function_operators_usage = {}
sequence_functions_usage = {}

from pprint import pprint


def my_print(name, value=''):
    return
    if value is '':
        print(name)
    else:
        print(name + ': ', end='')
        pprint(value)


# convert float to int if possible:
def float_to_int(x, t=3):
    if float(x).is_integer():
        return str(int(x))
    #  return str("%.3f" % x)
    return str(round(x, t))


def extract_category_value(x):
    try:  # is there a cleaner way to find category/values?
        cat, val = x.rsplit(': ', 1)
    except:
        cat = ''
        val = x
    return cat, val


# set invoke method:
sp_fn_table['ssplit'] = 'ssplit'
# compound_table['ssplit'] = '.apply_sp_fn(ssplit, \"{0}\")'                  # maybe it should be an apply_fn??
# compound_table['ssplit'] = [apply_sp_fn, ssplit, '']
compound_table['ssplit'] = ['apply_sp_fn', 'ssplit', '']
# set usage info:
function_operators_usage['ssplit'] = """
    description:
      ssplit splits the superposition into a sequence
      ssplit["str"] splits the superposition into a sequence at the 'str' substring
      
    examples:
      ssplit |Fred>
        |F> . |r> . |e> . |d>
      
      ssplit (|a> + 2|bcd> + 3.1|efgh>)
        |a> . 2|b> . 2|c> . 2|d> . 3.1|e> . 3.1|f> . 3.1|g> . 3.1|h>      

      ssplit[", "] |a, b, c>
        |a> . |b> . |c>

      ssplit[" and "] |a, b, c and d>
        |a, b, c> . |d>

      ssplit[", "] ssplit[" and "] |a, b, c and d>
        |a> . |b> . |c> . |d>
"""


def ssplit(one, split_char=''):
    if split_char == '':
        def split_with(x):
            return list(x)
    else:
        def split_with(x):
            return x.split(split_char)
    seq = sequence([])
    if type(one) in [ket, superposition]:
        for x in one:
            for c in split_with(x.label):
                seq += ket(c, x.value)
    return seq


# set invoke method:
seq_fn_table['smerge'] = 'smerge'
compound_table['smerge'] = '.apply_seq_fn(smerge, \"{0}\")'
compound_table['smerge'] = ['apply_seq_fn', 'smerge', '']
# set usage info:
function_operators_usage['smerge'] = """
    description:
      smerge merges a sequence into a single ket
      smerge["str"] merges a sequence into a single ket, seperated by the str string
      
    examples:
      smerge (|F> . |r> . |e> . |d>)
        |Fred>
      
      smerge[", "] (|a> . |b> . |c> . |d>)
        |a, b, c, d>
      
      smerge[", "] (|a> + |b> + |c> . |d> + |e>)
        |a, b, c, d, e>
"""


# one is a sequence
#
def smerge(one, merge_char=''):
    if type(one) is not sequence:
        return ket()
    labels = []
    for elt in one:
        if len(elt) == 0:  # so this works: smerge["\n"] (|b> . |c> . |> . |d>)
            labels.append('')
        else:
            for x in elt:
                labels.append(x.label)
    s = merge_char.join(labels)
    return ket(s)


# set invoke method:
# compound_table['insert'] = '.apply_sp_fn(insert, \"{0}\")'
compound_table['insert'] = ['apply_sp_fn', 'insert', '']
# set usage info:
function_operators_usage['insert'] = """
    description:
      insert string into ket
         
    examples:
      insert["Fred"] |hey {1}!>
        |hey Fred!>
        
      insert["Fred", "Sam"] |Hello {1} and {2}.>
        |Hello Fred and Sam.>
"""


def insert(one, *pieces):
    seq = sequence([])
    if type(one) in [ket, superposition]:
        for key, value in one.items():
            text = key.format('', *pieces)
            seq += ket(text, value)
    return seq


# set invoke method:
# compound_table['to-upper'] = '.apply_sp_fn(to_upper, \"{0}\")'
compound_table['to-upper'] = ['apply_sp_fn', 'to_upper', '']
# set usage info:
function_operators_usage['to-upper'] = """
    description:
      change i'th characters to upper case
         
    examples:
      to-upper[1] |fred>
        |Fred>
      
      to-upper[1,3,5] |abcdefg>
        |AbCdEfg>
"""


def to_upper(one, *positions):
    try:
        positions = [int(x) - 1 for x in
                     positions]  # maybe change the invoke pattern later, so don't need to split on ',' everywhere!
    except:
        return one
    r = superposition()
    if type(one) in [ket, superposition]:
        for key, value in one.items():
            text = "".join(key[i].upper() if i in positions else key[i] for i in range(len(key)))
            r.add(text, value)
    return r


# set invoke method:
compound_table['remove-prefix'] = ['apply_fn', 'remove_prefix', '']
# set usage info:
function_operators_usage['remove-prefix'] = """
    description:
        remove given prefix from the ket
            
    examples:
        remove-prefix["not "] |not sitting at the beach>
            |sitting at the beach>
    
        remove-prefix["word: "] |word: fish>
            |fish>      
    
"""
def remove_prefix(one, prefix):
    if type(one) is ket:
        if one.label.startswith(prefix):
            return ket(one.label[len(prefix):], one.value)
    return one


# set invoke method:
compound_table['has-prefix'] = ['apply_fn', 'has_prefix', '']
# set usage info:
function_operators_usage['has-prefix'] = """
    description:
      asks if the ket has the given prefix
      
    examples:
      has-prefix["not "] |not sitting at the beach>
        |yes>
        
      has-prefix["not "] |sitting at the beach>
        |no>
"""
def has_prefix(one, prefix):
    if type(one) is ket:
        if one.label.startswith(prefix):
            return ket('yes', one.value)
        return ket('no', one.value)
    return ket()


# set invoke method:
compound_table['remove-suffix'] = ['apply_fn', 'remove_suffix', '']
# set usage info:
function_operators_usage['remove-suffix'] = """
    description:
      remove given suffix from the ket

    examples:
"""
def remove_suffix(one, suffix):
    if type(one) is ket:
        if one.label.endswith(suffix):
            return ket(one.label[:-len(suffix)], one.value)
    return one


# set invoke method:
compound_table['has-suffix'] = ['apply_fn', 'has_suffix', '']
# set usage info:
function_operators_usage['has-suffix'] = """
    description:
      asks if the ket has the given suffix

    examples:
      has-suffix["day"] |Tuesday>
        |yes>
"""
def has_suffix(one, suffix):
    if type(one) is ket:
        if one.label.endswith(suffix):
            return ket('yes', one.value)
        return ket('no', one.value)
    return ket()



# set invoke method:
context_whitelist_table_3['learn'] = 'learn_sp'
# set usage info:
sequence_functions_usage['learn'] = """
    description:
      wrapper around a learn rule, so we can use it in operators
      
    examples:
      learn(|op: age>, |Fred>, |37>)
      implements: age |Fred> => |37>
"""


def learn_sp(context, one, two, three):
    for op in one.to_sp():
        if op.label.startswith('op: '):
            str_op = op.label[4:]
            for object in two.to_sp():
                context.learn(str_op, object, three)
    return three


# set invoke method:
context_whitelist_table_3['add-learn'] = 'add_learn_sp'
# set usage info:
sequence_functions_usage['add-learn'] = """
    description:
      wrapper around an add-learn rule, so we can use it in operators
      
    examples:
      add-learn(|op: friends>, |Fred>, |Sam>)
      implements: friends |Fred> +=> |Sam>
"""


def add_learn_sp(context, one, two, three):
    for op in one.to_sp():
        if op.label.startswith('op: '):
            str_op = op.label[4:]
            for object in two.to_sp():
                context.add_learn(str_op, object.label, three)
    return three


# set invoke method:
context_whitelist_table_2['apply'] = 'apply_sp'
# set usage info:
sequence_functions_usage['apply'] = """
    description:
      wrapper around apply op, so we can use it in operators
      
    examples:
      apply(|op: age>, |Fred>)
      implements: age |Fred>

      apply(|op: age> + |op: friends>, |Fred>)
      implements: age |Fred> + friends |Fred>
      
      apply(|op: age> . |op: friends>, |Fred>)
      implements: age |Fred> . friends |Fred>
      
      age |Fred> => |35>
      nick-name |Fred> => |Freddie>
      mother |Fred> => |Jude>
      father |Fred> => |Tom>
      star |*> #=> apply(supported-ops|_self>, |_self>)
      star |Fred>
        |35> + |Freddie> + |Jude> + |Tom>

    future:
      maybe implement op-sequences too.
      eg: apply(|op: how-many common[friends] split>, |Fred Sam>)
"""


def apply_sp(context, one, two):
    seq = sequence([])
    for sp in one:
        r = superposition()
        for x in sp:
            if x.label.startswith("op: "):
                op = x.label[4:]
                value = two.apply_op(context, op).multiply(x.value)
                if len(value) > 0:
                    value = value.to_sp()
                    r += value
        seq += r
    return seq


# set invoke method:
# compound_table['such-that'] = '.apply_sp_fn(sp_such_that, context, \"{0}\")'
compound_table['such-that'] = ['apply_seq_fn', 'seq_such_that', 'context']
# set usage info:
function_operators_usage['such-that'] = """
    description:
      such-that[op] filters the given superposition to elements that return true for "op |element>"     
    
    examples:
      such-that[is-a-woman] rel-kets[supported-ops] |>
      
      is-hungry |Fred> => |yes>
      is-hungry |Sam> => |no>
      such-that[is-hungry] rel-kets[supported-ops] |>
        |Fred>
        
      is-a-day |Monday> => |yes>
      is-a-day |Tuesday> => |yes>
      is-a-day |Wednesday> => |yes>
      is-a-day |Thursday> => |yes>
      is-a-day |Friday> => |yes>
      is-a-day |Saturday> => |yes>
      is-a-day |Sunday> => |yes>
      is-a-day |blah> => |no>
      is-a-day |foo> => |no>
      such-that[is-a-day] (|Monday> + |Tuesday> + |blah> + |Wednesday> + |Thursday> + |Friday> + |Saturday> + |foo> + |Sunday>)
        |Monday> + |Tuesday> + |Wednesday> + |Thursday> + |Friday> + |Saturday> + |Sunday>
                        
"""


def seq_such_that(one, context, *ops):
    def valid_ket(one, context, *ops):
        for op in ops:
            e = one.apply_op(context, op).to_sp()
            if e.label not in ["true", "yes"]:
                return False
            if e.value < 0.5:  # need to test this bit.
                return False
        return True

    seq = sequence([])
    for sp in sequence(one):
        r = superposition()
        for x in sp:
            if valid_ket(x, context, *ops):
                r.add_sp(x)
        seq += r
    return seq.sdrop()


def print_table(table):
    max_length_column = []
    tuple_len = len(table[0])  # assume entire table has the same shape as the first row
    for i in range(tuple_len):
        max_length_column.append(max(len(e[i]) + 2 for e in table))
    for e in table:
        for i in range(tuple_len):
            print(e[i].ljust(max_length_column[i]), end='')
        print()


# set invoke method:
# compound_table['table'] = ".apply_sp_fn(pretty_print_table,context,\"{0}\")"
compound_table['table'] = ['apply_sp_fn', 'pretty_print_table', 'context']
# set usage info:
function_operators_usage['table'] = """
    description:
      display a nicely formatted table
      where: 
        the first column are elements from the inputted superposition/sequence
        the rest of the columns are the result of applying the given operator to the element in the first column

      we also have some special operators:
        '*' means use all supported-ops of the inputted superposition/sequence
        'coeff' means return the coeff of the element in the first column
        'rank' as the first operator means produce a rank table
    
    examples:
      load fred-sam-friends.sw
      age |Fred> => |47>
      age |Sam> => |45>
      table[person, age, friends] split |Fred Sam>
        +--------+-----+----------------------------------------------------+
        | person | age | friends                                            |
        +--------+-----+----------------------------------------------------+
        | Fred   | 47  | Jack, Harry, Ed, Mary, Rob, Patrick, Emma, Charlie |
        | Sam    | 45  | Charlie, George, Emma, Jack, Rober, Frank, Julie   |
        +--------+-----+----------------------------------------------------+
        
      web-load http://semantic-db.org/sw-examples/bots.sw
      Bella |*> #=> apply(|_self>, |bot: Bella>)
      Emma |*> #=> apply(|_self>, |bot: Emma>)
      Madison |*> #=> apply(|_self>, |bot: Madison>)
      table[op, Bella, Emma, Madison] supported-ops (|bot: Bella> + |bot: Emma> + |bot: Madison>)
        +------------------------+--------------+----------------+---------------------+
        | op                     | Bella        | Emma           | Madison             |
        +------------------------+--------------+----------------+---------------------+
        | name                   | Bella        | Emma           | Madison             |
        | mother                 | Mia          | Madison        | Mia                 |
        | father                 | William      | Nathan         | Ian                 |
        | birth-sign             | Cancer       | Capricorn      | Cancer              |
        | number-siblings        | 1            | 4              | 6                   |
        | wine-preference        | Merlot       | Pinot Noir     | Pinot Noir          |
        | favourite-fruit        | pineapples   | oranges        | pineapples          |
        | favourite-music        | genre: punk  | genre: hip hop | genre: blues        |
        | favourite-play         | Endgame      | No Exit        | Death of a Salesman |
        | hair-colour            | gray         | red            | red                 |
        | eye-colour             | hazel        | gray           | amber               |
        | where-live             | Sydney       | New York       | Vancouver           |
        | favourite-holiday-spot | Paris        | Taj Mahal      | Uluru               |
        | make-of-car            | Porsche      | BMW            | Bugatti             |
        | religion               | Christianity | Taoism         | Islam               |
        | personality-type       | the guardian | the visionary  | the performer       |
        | current-emotion        | fear         | kindness       | indignation         |
        | bed-time               | 8pm          | 2am            | 10:30pm             |
        | age                    | 31           | 29             | 23                  |
        | hungry                 |              |                | starving            |
        | friends                |              |                | Emma, Bella         |
        +------------------------+--------------+----------------+---------------------+
      
      load pretty-print-table-of-australian-cities.sw
      table[rank, city, population, area, annual-rainfall] reverse sort-by[population] "" |city list>
        +------+-----------+------------+------+-----------------+
        | rank | city      | population | area | annual-rainfall |
        +------+-----------+------------+------+-----------------+
        | 1    | Sydney    | 4336374    | 2058 | 1214.8          |
        | 2    | Melbourne | 3806092    | 1566 | 646.9           |
        | 3    | Brisbane  | 1857594    | 5905 | 1146.4          |
        | 4    | Perth     | 1554769    | 5386 | 869.4           |
        | 5    | Adelaide  | 1158259    | 1295 | 600.5           |
        | 6    | Hobart    | 205556     | 1357 | 619.5           |
        | 7    | Darwin    | 120900     | 112  | 1714.7          |
        +------+-----------+------------+------+-----------------+
        
    see also:
      such-that, sort-by
"""


# def pretty_print_table(one,context,params,strict=False,rank=False):
def pretty_print_table(one, context, *ops):
    # my_print('one', str(one))
    # my_print('ops', ops)
    ops = list(ops)
    rank = False
    if ops[0] == 'rank':
        rank = True
        ops = ops[1:]
    if len(ops) > 1 and ops[1] == '*':
        supported_ops = one.apply_op(context, 'supported-ops').to_sp()    # sort this, or not?
        ops = [ops[0]] + [x.label[4:] for x in supported_ops]
    header_row = ops
    rows = []
    for k, x in enumerate(one):
        label = x.apply_sigmoid(set_to, 1).apply_fn(remove_leading_category).readable_display()
        # row = [label] + [x.apply_op(context, op).apply_fn(remove_leading_category).readable_display() for op in ops[1:]]
        row = [label]
        for op in ops[1:]:
            if op == 'coeff':
                elt = float_to_int(x.value)
            else:
                elt = x.apply_sigmoid(set_to, 1).apply_op(context, op).apply_fn(remove_leading_category).readable_display()
            row.append(elt)
        if rank:
            row = [str(k + 1)] + row
        # my_print('row', row)
        rows.append(row)
    if rank:
        ops = ['rank'] + ops
    max_col_widths = []
    for i in range(len(ops)):
        col_width = len(ops[i])
        for k in range(len(one)):
            col_width = max(col_width, len(rows[k][i]))
        max_col_widths.append(col_width)
    # my_print('max_col_widths', max_col_widths)

    hpre = "+-"
    hmid = "-+-"
    hpost = "-+\n"
    hfill = "-"
    header = hpre + hmid.join(hfill * w for w in max_col_widths) + hpost
    # my_print('header', header)
    pre = "| "
    mid = " | "
    post = " |\n"
    label_header = pre + mid.join(op.ljust(max_col_widths[k]) for k, op in enumerate(ops)) + post
    # my_print('label_header', label_header)
    s = header + label_header + header
    for k in range(len(one)):
        srow = pre + mid.join(x.ljust(max_col_widths[w]) for w, x in enumerate(rows[k])) + post
        s += srow
    s += header
    print(s)

    # code to save the table (useful for big ones that are too hard to cut and paste from the console)
    logger.info("saving to: saved-table.txt")
    file = open("saved-table.txt", 'w')
    file.write("sa: table[%s]\n" % ','.join(ops))
    file.write(s)
    file.close()

    return ket('table')


import numpy as np
from matplotlib import pyplot as plt

# set invoke method:
sp_fn_table['plot'] = 'plot'
# set usage info:
function_operators_usage['plot'] = """
    description:
      plot a superposition as a bar chart using matplotlib
    
    examples:
      plot (|Fred> + 2|Sam>)
      plot rank split |a b c d e f>
      plot shuffle rank split |a b c d e f>
"""


def plot(one):
    values = []
    labels = []
    for label, value in one.items():
        labels.append(label)
        values.append(value)

    fig = plt.figure()
    width = 0.1
    ind = np.arange(len(values))
    plt.bar(ind, values, width=width)
    plt.xticks(ind + width / 2, labels)
    fig.autofmt_xdate()
    plt.show()
    return ket('plot')


# set invoke method:
whitelist_table_3['consume-reaction'] = 'process_reaction'
# set usage info:
sequence_functions_usage['consume-reaction'] = """
    description:
      process a chemical reaction that consumes the reactants
      eg: 2 H_2 + O_2 -> 2 H_2 0
      is represented by: 
        consume-reaction(input-sp, 2|H2> + |O2>, 2|H2O>)
      which is equivalent to:
        input-sp - (2|H2> + |O2>) + 2|H2O>
      
      if input-sp doesn't contain the necessary reactants, then it is returned unchanged 
      
    examples:
      current |state> => words-to-list |can opener, closed can and hungry>
      learn-state (*) #=> learn(|op: current>, |state>, |_self>)
      use |can opener> #=> learn-state consume-reaction(current |state>, |can opener> + |closed can>, |can opener> + |open can>)
      eat-from |can> #=> learn-state consume-reaction(current |state>, |open can> + |hungry>, |empty can> + |not hungry>)
      
      current |state>
        |can opener> + |closed can> + |hungry>
      
      use |can opener>
        |can opener> + |hungry> + |open can>
      
      eat-from |can>
        |can opener> + |empty can> + |not hungry>
    
    see also:
      catalytic-reaction, eat-from-can, fission-uranium
"""


#
# one, two and three are superpositions
def process_reaction(one, two, three):
    one = one.to_sp()
    two = two.to_sp()
    three = three.to_sp()

    def del_fn(x, y):  # NB: creates negative coeffs.
        return x - y

    if intersection(two, one).count_sum() != two.count_sum():
        return one
    else:
        return intersection_fn(del_fn, one,
                               two).drop() + three  # can we do superposition subtraction? Maybe implement it?? Meaning: one - two + three


# set invoke method:
whitelist_table_3['catalytic-reaction'] = 'process_catalytic_reaction'
# set usage info:
sequence_functions_usage['catalytic-reaction'] = """
    description:
      process a catalyzed reaction (that doesn't consume the reactants) 
      if the necessary reactants are not present, then the state is left unchanged.
      
      catalytic-reaction(input-sp, |a> + |b>, |c> +|d>)
      is equivalent to:
        input-sp + |c> + |d>,
      provided |a> + |b> is in input-sp
      else, return input-sp
            
    examples:
    
    see also:
      consume-reaction
"""


# 16/2/2016:
# process-catalytic-reaction(current-sp,|a> + |b>,|c> +|d>) = current-sp + |c> + |d> if |a> + |b> is in current-sp
# What if |c> + |d> is already in current-sp? Do you add it again?
# I suspect process-catalytic-reaction() can be used to encode maths proofs. One is the current state of knowledge. Two is the necessary conditions for the proof to be true. Three is the implications of that proof.
# Another example is simple physics problems. You write down what you know, and any possibly relevant equations. Then try to figure out a pathway to the desired result.
#
def process_catalytic_reaction(one, two, three):
    if intersection(two, one).count_sum() != two.count_sum():
        return one
    else:
        return one + three


# set invoke method:
fn_table['apply-value'] = 'apply_value'
# set usage info:
function_operators_usage['apply-value'] = """
    description:
      apply value to the given ket
      return the ket if the value is not convertable to float
            
    examples:
      apply-value |price: fish>
        |price: fish>
        
      apply-value |price: 37>
        37|price: 37>
"""


def apply_value(one):
    cat, value = one.label.rsplit(': ', 1)
    try:
        x = float(value)
    except ValueError:
        return one
    return ket(one.label, x * one.value)


# set invoke method:
fn_table['extract-category'] = 'extract_category'
# set usage info:
function_operators_usage['extract-category'] = """
    description:
      extract the category from the given ket
            
    examples:
      extract-category |fish>
        |fish>
        
      extract-category |animal: mammal: dog>
        |animal: mammal>
        
    see also:
      extract-value    
"""


def extract_category(one):
    try:
        cat, value = one.label.rsplit(': ', 1)
    except:
        return one
    return ket(cat, one.value)


# set invoke method:
fn_table['extract-value'] = 'extract_value'
# set usage info:
function_operators_usage['extract-value'] = """
    description:
      extract the value, ie remove the category, from the given ket
            
    examples:
      extract-value |fish>
        |fish>
        
      extract-value |animal: mammal: dog>
        |dog>
        
    see also:
      extract-category    
"""


# the extract value function
# eg: extract-value |animal: fish> => |fish>
def extract_value(one):
    try:
        cat, value = one.label.rsplit(': ', 1)
    except:
        return one
    return ket(value, one.value)


# set invoke method:
fn_table['remove-leading-category'] = 'remove_leading_category'
# set usage info:
function_operators_usage['remove-leading-category'] = """
    description:
      remove the leading category
            
    examples:
      remove-leading-category |fish>
        |fish>
        
      remove-leading-category |animal: mammal: dog>
        |mammal: dog>
        
    see also:
      find-leading-category    
"""


# one is a ket
def remove_leading_category(one):
    text = one.label.split(': ', 1)[-1]
    return ket(text, one.value)


# set invoke method:
fn_table['find-leading-category'] = 'find_leading_category'
# set usage info:
function_operators_usage['find-leading-category'] = """
    description:
      find the leading category
            
    examples:
      find-leading-category |fish>
        |fish>
        
      find-leading-category |animal: mammal: dog>
        |animal>
        
    see also:
      remove-leading-category    
"""


# one is a ket
def find_leading_category(one):
    text = one.label.split(': ', 1)[0]
    return ket(text, one.value)


# set invoke method:
fn_table['to-value'] = 'to_value'
# set usage info:
function_operators_usage['to-value'] = """
    description:
      if the value is a float, remove from the ket, and apply it to the coefficient
            
    examples:
      to-value |>
        |>
        
      to-value |19>
        19| >
        
      to-value |age: 33.5>
        33.5|age>
        
      to-value |cat: val>
        |cat: val>
        
      to-value |cat1: cat2: 13>
        13|cat1: cat2>
        
    see also:
      to-category
"""


# one is a ket
def to_value(one):
    try:
        cat, value = one.label.rsplit(': ', 1)
    except:
        cat = ''
        value = one.label

    if len(cat) == 0:
        label = " "
    else:
        label = cat

    try:
        x = float(value)
        return ket(label, x)
    except:
        return one

    # set invoke method:


fn_table['to-category'] = 'to_category'
# set usage info:
function_operators_usage['to-category'] = """
    description:
      append the coefficient of the ket, to the ket label
            
    examples:
      to-category 57| >
        |57>
      
      to-category |age>
        |age: 1>
        
      to-category 23|age>
        |age: 23>
        
    see also:
      to-value
"""


# one is a ket
def to_category(one):
    # do we need one = one.ket() here?
    label = one.label
    if label in ["", " "]:  # maybe label.strip() == ""?
        label = ""
    else:
        label += ": "
    return ket(label + float_to_int(one.value))


# set invoke method:
whitelist_table_3['arithmetic'] = 'arithmetic'
# set usage info:
sequence_functions_usage['arithmetic'] = """
    description:
      the arithmetic function
      supported operators: + - * / % ^
      if the categories are different, return |>
      
    examples:
      arithmetic(|number: 3>, |symbol: +>, |number: 8>)
        |number: 11>
        
      arithmetic(|3>, |^>, |4>)
        |81>
      
      arithmetic(|price: 37>, |->, |number: 5.20>)
        |>
        
      number-to-price |number: *> #=> |price:> __ extract-value |_self>
      arithmetic(|price: 37>, |->, number-to-price |number: 5.20>)
        |price: 31.8>
      
      fib |0> => |0>
      fib |1> => |1>
      n-1 |*> #=> arithmetic(|_self>,|->,|1>)
      n-2 |*> #=> arithmetic(|_self>,|->,|2>)
      fib |*> !=> arithmetic( fib n-1 |_self>, |+>, fib n-2 |_self>)
      fact |0> => |1>
      fact |*> !=> arithmetic(|_self>, |*>, fact n-1 |_self>)
      table[number,fib,fact] range(|1>, |10>)
        +--------+-----+---------+
        | number | fib | fact    |
        +--------+-----+---------+
        | 1      | 1   | 1       |
        | 2      | 1   | 2       |
        | 3      | 2   | 6       |
        | 4      | 3   | 24      |
        | 5      | 5   | 120     |
        | 6      | 8   | 720     |
        | 7      | 13  | 5040    |
        | 8      | 21  | 40320   |
        | 9      | 34  | 362880  |
        | 10     | 55  | 3628800 |
        +--------+-----+---------+
"""


# the arithmetic function
# eg: arithmetic(|number: 3>,|symbol: +>,|number: 8>)
# heh. note the "amplification factor"
# of z = x*y directly in python vs what this function does!
# you do get some power in return though.
# and it is still much cheaper than a fully neural model equivalent presumably is.
#
# What I meant by "amplification factor" is the amount of computing power needed to calculate say z = x*y
# in python, vs the amount if you use this arithmetic function.
#
# x, y superposition bug here too!
# fixed, I hope.
#
def arithmetic(x, operator, y):
    x = x.to_sp()
    operator = operator.to_sp()
    y = y.to_sp()

    x_label = x if type(x) == str else x.label
    op_label = operator if type(operator) == str else operator.label
    y_label = y if type(y) == str else y.label

    cat1, v1 = extract_category_value(x_label)
    name, op = extract_category_value(op_label)
    cat2, v2 = extract_category_value(y_label)

    if cat1 != cat2 or op not in ['+', '-', '*', '/', '%', '^']:
        return ket()
    try:
        x = int(v1)
        y = int(v2)
    except ValueError:
        try:
            x = float(v1)
            y = float(v2)
        except ValueError:
            return ket()
    label = ""
    if len(cat1) > 0:
        label = cat1 + ": "
    if op == '+':
        return ket(label + str(x + y))
    elif op == '-':
        return ket(label + str(x - y))
    elif op == '*':
        return ket(label + str(x * y))
    elif op == '/':
        if y == 0:  # prevent div by zero
            return ket()
        return ket(label + str(x / y))
    elif op == '%':
        return ket(label + str(x % y))
    elif op == '^':
        return ket(label + str(x ** y))
    else:
        return ket()  # presumably this should never be reached.


# from: http://stackoverflow.com/questions/4189766/python-range-with-step-of-type-float
# maybe use numpy instead?
def float_range(start, stop, step):
    while start <= stop + 0.0000001:  # hack so hopefully the float rounding doesn't give the wrong result.
        yield start  # may need to tweak the 0.0000001 value.
        start += step  # also, I like my ranges to reach their upper-bound!


# set invoke method:
whitelist_table_2['range'] = 'show_range'
whitelist_table_3['range'] = 'show_range'
# set usage info:
sequence_functions_usage['range'] = """
    description:
      the range function
            
    examples:
      range(|1>, |10>)
        |1> + |2> + |3> + |4> + |5> + |6> + |7> + |8> + |9> + |10>
      
      range(|1>, |5>, |0.5>)
        |1> + |1.5> + |2> + |2.5> + |3> + |3.5> + |4> + |4.5> + |5>
"""


def show_range(start, finish, step=ket("1")):
    start = start.to_sp()
    finish = finish.to_sp()
    step = step.to_sp()

    start_label = start if type(start) == str else start.label
    finish_label = finish if type(finish) == str else finish.label
    step_label = step if type(step) == str else step.label

    cat1, v1 = extract_category_value(start_label)
    cat2, v2 = extract_category_value(finish_label)
    cat3, v3 = extract_category_value(step_label)

    if cat1 != cat2:
        return ket()

    label = ""
    if len(cat1) > 0:
        label = cat1 + ": "
    result = superposition()

    try:
        start = int(v1)
        stop = int(v2) + 1  # maybe bug. also in float version!
        step = int(v3)
        for k in range(start, stop, step):
            result.add(label + str(k))
    except:
        try:
            start = float(v1)
            stop = float(v2)
            step = float(v3)
            for k in float_range(start, stop, step):
                result.add(label + float_to_int(k))
        except:
            return ket()
    return result


# the intersection function.
# if you set foo = min, then it is a generalization of Boolean set intersection.
# if you set foo = max, then it is a generalization of Boolean set union.
# if you set foo = sum, then it is a literal sum.
# if you set foo = mult, then it is a multiplication of the list elements.
# possibly other useful values of foo too.
# maybe we can do a complement function? if value1 == 0 and value2 != 0, then return value2
#
def superposition_intersection_fn(foo, one, two):
    if type(one) not in [ket, superposition] and type(two) not in [ket, superposition]:
        return superposition()
    r = superposition()
    merged = one + two

    for key, value in merged.items():
        v1 = one.get_value(key)
        v2 = two.get_value(key)
        new_value = foo(v1, v2)
        r.add(key, new_value)
    return r


# version to handle sequences too.
def intersection_fn(foo, one, two):
    if type(one) in [ket, superposition] and type(two) in [ket, superposition]:
        return superposition_intersection_fn(foo, one, two)
    seq = sequence([])
    one, two = normalize_seq_len(one, two)
    for k in range(len(one)):
        r = superposition_intersection_fn(foo, one[k], two[k])
        seq.data.append(r)
    return seq


def normalize_seq_len(one, two):
    if type(one) is not sequence:
        one = sequence(one)
    if type(two) is not sequence:
        two = sequence(two)
    if len(one) == len(two):
        return one, two
    empty = superposition()
    one = copy.deepcopy(one)
    two = copy.deepcopy(two)
    max_len = max(len(one.data), len(two.data))
    one.data = one.data + [empty] * (max_len - len(one.data))
    two.data = two.data + [empty] * (max_len - len(two.data))
    return one, two


# now the actual intersection:
# NB: intersection is actually one key component of learning.
# Say a child trying to learn the meaning of "apple".
# They take an intersection of what they were currently thinking everytime their parents say "apple".
# The bit in common (ie, the intersection) most likely is the meaning of "apple".
# Something similar for a dog learning a trick and hearing "good dog".
#
# Let's expand a bit.
# Let's say the superpositions of each time their parents said "apple" are r1, r2, r3, ...,rn
# Then, if not over-specified (ie we get the empty set), meaning-apple might simply be: intersection(r1,r2,...,rn)
#
# 1/5/2014: Alternatively, we can learn using thresholds and sums:
# TF[t5](TF[t1] pattern-1 |dog> + TF[t2] pattern-2 |dog> + TF[t3] pattern-3 |dog> + TF[t4] pattern-4 |dog>)
#
# I suspect intersection can also be used in language translation (more thought needed!).
# Say you have a good set of sentence pairs in language A and B.
# Then intersection may help in finding the word pairs. Word in A vs same meaning in B.
#
# a union also plays a role in learning, when quite distinct things refer to the same object.
# say if we want |word: frog> and |image: frog> to both trigger the |concept: frog>

# set invoke method:
whitelist_table_2['intersection'] = 'intersection'
whitelist_table_3['intersection'] = 'tri_intersection'
# set usage info:
sequence_functions_usage['intersection'] = """
    description:
      the intersection function
      takes element-wise min of the coefficients
            
    examples:
      intersection(|a>, |b>, |c>)
        |>
        
      intersection(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)      
        3|a> + 0.9|b>

      intersection(|a1> + |a2> . 0.3|b1> + 0.5|b2> , 3|a1> + 0.9|a2> . 0.7|b2>)
        |a1> + 0.9|a2> . 0.5|b2>
        
    see also:
      union, complement 
"""


def intersection(one, two):
    return intersection_fn(min, one, two).drop()


# now the union:
# set invoke method:
whitelist_table_2['union'] = 'union'
whitelist_table_3['union'] = 'tri_union'
# set usage info:
sequence_functions_usage['union'] = """
    description:
      the union function
      takes element-wise max of the coefficients
            
    examples:
      union(|a>, |b>, |c>)
        |a> + |b> + |c>
        
      union(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)
        3.5|a> + 1.2|b> + 5.13|c>

      union(|a1> + |a2> . 0.3|b1> + 0.5|b2> , 3|a1> + 0.9|a2> . 0.7|b2>)
        3|a1> + |a2> . 0.3|b1> + 0.7|b2>

    see also:
      intersection, complement 
"""


def union(one, two):
    return intersection_fn(max, one, two)


# potentially we could write a wrapper that maps associative pair functions into triple, quad etc fns.
# eg: assoc_wrapper(fn,pieces)
# where pieces is the list of parametrs to feed to "fn"
#
# the triple intersection:
def tri_intersection(one, two, three):
    return intersection(intersection(one, two), three)


# the triple union:
def tri_union(one, two, three):
    return union(union(one, two), three)


# the complement variable function:
def comp_fn(x, y):
    if x == 0 and y != 0:
        return y
    elif x != 0 and y == 0:
        return x
    else:
        return 0


# now for complement:
# set invoke method:
whitelist_table_2['complement'] = 'complement'
# set usage info:
sequence_functions_usage['complement'] = """
    description:
      the complement function
            
    examples:

    see also:
      intersection, union,  
"""


def complement(one, two):
    return intersection_fn(comp_fn, one, two)


# the delete function:
def del_fn(x, y):  # a possible variant is "return y - x"
    if x != 0:
        return 0
    else:
        return y


def delete(one, two):
    return intersection_fn(del_fn, one, two).drop()  # NB: the .drop()


# OK. Let's write the "return y - x" variant:
def del_fn2(x, y):
    if x <= y:
        return y - x
    else:
        return 0


def delete2(one, two):
    return intersection_fn(del_fn2, one, two).drop()


def mult_fn(x, y):
    return x * y


# set invoke method:
whitelist_table_2['multiply'] = 'multiply'
# set usage info:
sequence_functions_usage['multiply'] = """
    description:
      the multiply function
      takes element-wise multiply of the coefficients
            
    examples:
      multiply(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)
        10.5|a> + 1.08|b> + 0|c>

    see also:
      intersection, union, complement, addition   
"""


def multiply(one, two):
    return intersection_fn(mult_fn, one, two)


def sum_fn(x, y):
    return x + y


# set invoke method:
whitelist_table_2['addition'] = 'addition'
# set usage info:
sequence_functions_usage['addition'] = """
    description:
      the addition function
      takes element-wise sum of the coefficients
            
    examples:
      addition(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)
        6.5|a> + 2.1|b> + 5.13|c>

    see also:
      intersection, union, complement, multiply 
"""


def addition(one, two):
    return intersection_fn(sum_fn, one, two)


def del_fn3(x, y):  # NB: creates negative coeffs.
    return x - y


def delete3(one, two):
    return intersection_fn(del_fn3, one, two)


def squared_difference(x, y):
    return (x - y) ** 2


# set invoke method:
whitelist_table_2['distance'] = 'Euclidean_distance'
# set usage info:
sequence_functions_usage['distance'] = """
    description:
      the Euclidean distance function
            
    examples:
      distance(0|x> + 0|y>, 0|x> + 7|y>)
        |number: 7>
        
      distance(0|x> + 0|y>, 3|x> + 4|y>)
        |number: 5>        

      distance(0|x> + 0|y>, 5|x> + 12|y>)
        |number: 13>

      distance(0|x> + 0|y>, |x> + 2|y>)
        |number: 2.236>
           
    see also:
      simm 

    future:
      maybe change the number of decimal points in the result.
      currently set to 3
      maybe remove the number prefix too.
"""


def Euclidean_distance(one, two):
    one = one.to_sp()
    two = two.to_sp()

    return ket("number: " + float_to_int(math.sqrt(intersection_fn(squared_difference, one, two).count_sum())))


# 11/8/2015: the exclude function:
# exclude(|a> + |c>,|a> + |b> + |c> + |d>) == |b> + |d>
# in quick testing, seems to work.
#
def exclude_fn(x, y):
    if x > 0:
        return 0
    return y


def exclude(one, two):
    return intersection_fn(exclude_fn, one, two).drop()


# the similarity measures: Yeah, we have a bunch of variations.
# a superposition version of simm.
# not yet sure how to write the sequence version of simm.
# BTW, simm stands for "similarity measure".
# ie, 1 for exact match
# 0 for exact mismatch
# values in between otherwise.
# in practice it is more of a concept than a single equation.
# but it is the foundation equation for pattern recognition
#
# One interesting use of simm is the Landscape function:
# L(f,x) = simm(f,g(x))
# with a different pattern g(x) at each point x.
# cf. DNA micro-array
# http://en.wikipedia.org/wiki/DNA_microarray
# the landscape fn converts an incoming pattern f into a mathematical surface (in general not a smooth surface though)
#
# A well supported similarity is one that has a high simm score,
# and A and B have a large number of terms.
# A weakly supported similarity is where A and B have a small number of terms.
# Though on further thought it is not that simple.
# If the kets are "low order", ie close to the input, then you need more of them.
# If the kets are "higher order", ie more abstract, and hence rarer in frequency,
# then each ket carries more meaning.
#
# Maybe we need a version of simm for kets. Currently simm(a|x>,b|x>) returns 100%
# independent of the coeffs a and b.
# Recall we were meant to only use s1*wf == s2*wg if f and g are longer than one element.
# Provided they are not negative, simm for single elts should be: min(a,b)/max(a,b)
#
def simm(A, B):
    print(display(A))
    print(display(B))

    A = superposition() + A
    B = superposition() + B

    one = A.normalize()
    two = B.normalize()

    print(display(one))
    print(display(two))

    result = intersection(one, two)
    print(display(result))
    return result.count_sum()


# a quiet version of simm:
# maybe we should use |A intn B|/|A union B| instead??
# Though would need to check it gives the same answer as the current method.
def silent_simm(A, B):
    # handle single kets, where we don't want rescaling to s1*wf == s2*wg
    # seems to be working just fine.
    if A.count() <= 1 and B.count() <= 1:
        a = A.ket()
        b = B.ket()
        if a.label != b.label:  # put a.label == '' test in here too?
            return 0
        a = max(a.value, 0)  # just making sure they are >= 0.
        b = max(b.value, 0)
        if a == 0 and b == 0:  # prevent div by zero.
            return 0
        return min(a, b) / max(a, b)
    return intersection(A.normalize(), B.normalize()).count_sum()


# unscaled simm.
def unscaled_simm(A, B):
    wf = A.count_sum()
    wg = B.count_sum()
    if wf == 0 and wg == 0:
        return 0
    return intersection(A, B).count_sum() / max(wf, wg)


# quick test found this is not in [0,1]
#  return intersection(A,B).count_sum()
#
# potentially need a version that is intersection(A,B).count_sum()
# cf: |A intn B|, where intn is the intersection operator, and usually applies to A,B with Boolean values, not float.
# We can emulate the Boolean bit with: intersection(A,B).drop().count()
# though the closest to original simm corresponds to the .normalize() version.

# closer to the original simm[w,f,g], we are going to introduce a weighted simm:
#
# a couple of common use cases are:
# weighted_simm(A,A,B) and weighted_simm(B,A,B)
# or something close to that.
#
def weighted_simm(w, A, B):
    A = multiply(w, A)
    B = multiply(w, B)
    return intersection(A.normalize(), B.normalize()).count_sum()


# a version of simmm that returns: result|simm>
def ket_simm(A, B):
    #  result = intersection(A.normalize(),B.normalize()).count_sum()
    result = silent_simm(A, B)
    return ket("simm", result)


def ket_weighted_simm(w, A, B):
    result = weighted_simm(w, A, B)
    return ket("simm", result)


# 18/6/2016:
# implement a faster simm.
# simm is often a time sink, so we need to find ways to speed it up.
# note eventually we might be able to implement a parallel version.
# if not simm, then pattern_recognition function in new_context().
#
# OK. In testing in the console it seems to work.
# Not sure if we can make it faster, but I think we are O(n) now.
def old_fast_simm(A, B):
    #  logger.debug("inside fast_simm")
    if A.count() <= 1 and B.count() <= 1:
        a = A.ket()
        b = B.ket()
        if a.label != b.label:  # put a.label == '' test in here too?
            return 0
        a = max(a.value, 0)  # just making sure they are >= 0.
        b = max(b.value, 0)
        if a == 0 and b == 0:  # prevent div by zero.
            return 0
        return min(a, b) / max(a, b)
    #  return intersection(A.normalize(),B.normalize()).count_sum()

    # now calculate the superposition version of simm, while trying to be as fast as possible:
    #  logger.debug("made it here in fast_simm")
    try:
        merged = {}
        one_sum = 0
        one = {}
        for elt in A:
            one[elt.label] = elt.value  # what about empty kets? How does this code handle them?
            one_sum += elt.value  # assume all values in A are >= 0
            merged[elt.label] = True  # potentially we could use abs(elt.value)

        two_sum = 0
        two = {}
        for elt in B:
            two[elt.label] = elt.value
            two_sum += elt.value  # assume all values in B are >= 0
            merged[elt.label] = True

        # prevent div by zero:
        if one_sum == 0 or two_sum == 0:
            return 0

        merged_sum = 0
        #    for key in merged:
        #      v1 = 0
        #      if key in one:
        #        v1 = one[key]/one_sum
        #      v2 = 0
        #      if key in two:
        #        v2 = two[key]/two_sum
        #      merged_sum += min(v1,v2)
        for key in merged:
            if key in one and key in two:
                v1 = one[key] / one_sum
                v2 = two[key] / two_sum
                merged_sum += min(v1, v2)
        return merged_sum
    except Exception as e:
        logger.debug("fast_simm exception reason: %s" % e)


# 27/3/2014: time to implement the landscape function.
# Hrm... how do I plan on testing it?
#
# Recall the math definition:
# L(f,x) = simm(f,g(x))
#
def landscape(context, pattern, f, x):
    f = f.apply_op(context, pattern)
    g = x.apply_op(context, pattern)
    return silent_simm(f, g)  # or should this be ket_simm()?


# list simm. This is not a ket/sp function at all, but I think it belongs here anyway.
# eg, maybe as background to explain the ket/sp simm() I do have here.
#
# First definition of simm:
# simm(w,f,g) = w*[f - g] + R abs(w*f - w*g)/[w*f + w*g + R abs(w*f - w*g)]
# where one version of a*b is:
# a*b = \Sum_k abs(a_k * b_k)
# And for best results set R = 1.
# This version has the property:
# 0 <= simm(w,f,g) <= 1. 1 for f,g completely disjoint, 0 for f,g exactly identical.
# BTW, this follows from:
# w*[f - g] = w*f + w*g if f,g are completely disjoint (taking into account the effect of w)
# w*[f - g] = 0 if f,g are identical (taking into account the effect of w)
#
# The second version of simm is: 1 - simm(w,f,g)
# w*f + w*g - w*[f - g]/[w*f + w*g + R abs(w*f - w*g)]
# This version has the property:
# 0 <= simm(w,f,g) <= 1. 0 for f,g completely disjoint, 1 for f,g exactly identical.
#
# Both versions have some symmetries (indeed, I tweaked the function to create symmetries, cf physics). I'll type them up later.
# NB: I swap back and forth between these two variations, and call them the same name,
# depending on what I am trying to do.
#
# NB: if a,b >= 0 then:                    # what about if a and or b are < 0?
# a + b + abs(a - b) = 2*max(a,b)
# a + b - abs(a - b) = 2*min(a,b)
#
# w,f,g are lists of ints or floats. They have nothing to do with kets or superpositions!
def list_simm(w, f, g):
    the_len = min(len(f), len(g))
    print("the_len:", the_len)
    print("w:", w)
    print("f:", f)
    print("g:", g)
    print()
    # w += [0] * (the_len - len(w))            # from here: http://stackoverflow.com/questions/3438756/some-built-in-to-pad-a-list-in-python
    w += [1] * (the_len - len(w))
    f = f[:the_len]
    g = g[:the_len]
    print("w:", w)
    print("f:", f)
    print("g:", g)

    wf = sum(abs(w[k] * f[k]) for k in range(the_len))
    wg = sum(abs(w[k] * g[k]) for k in range(the_len))
    wfg = sum(abs(w[k] * f[k] - w[k] * g[k]) for k in range(the_len))

    print("wf:", wf)
    print("wg:", wg)
    print("wfg:", wfg)

    if wf == 0 and wg == 0:
        #    return 0
        result = 0
    else:
        # return (wf + wg - wfg)/(2*max(wf,wg))
        result = (wf + wg - wfg) / (2 * max(wf, wg))
    print("result:", result)
    return result


# 17/2/2015: a rescaled version of list simm
# need to test it now!
#
def rescaled_list_simm(w, f, g):
    the_len = min(len(f), len(g))
    #  print("the_len:",the_len)
    #  print("w:",w)
    #  print("f:",f)
    #  print("g:",g)
    #  print()
    # normalize lengths of our lists:
    #  w += [0] * (the_len - len(w))            # from here: http://stackoverflow.com/questions/3438756/some-built-in-to-pad-a-list-in-python
    w += [1] * (the_len - len(w))
    f = f[:the_len]
    g = g[:the_len]
    #  print("w:",w)
    #  print("f:",f)
    #  print("g:",g)

    # rescale step, first find size:
    s1 = sum(abs(w[k] * f[k]) for k in range(the_len))
    s2 = sum(abs(w[k] * g[k]) for k in range(the_len))

    # if s1 == 0, or s2 == 0, we can't rescale:
    if s1 == 0 or s2 == 0:
        return 0

    # now rescale:
    f = [f[k] / s1 for k in range(the_len)]
    g = [g[k] / s2 for k in range(the_len)]

    # proceed with algo:
    # if rescaled correctly, wf and wg should == 1.
    #  wf = sum(abs(w[k]*f[k]) for k in range(the_len))
    #  wg = sum(abs(w[k]*g[k]) for k in range(the_len))
    wfg = sum(abs(w[k] * f[k] - w[k] * g[k]) for k in range(the_len))

    #  print("wf:",wf)
    #  print("wg:",wg)
    #  print("wfg:",wfg)

    # we should never have wf or wg == 0 in the rescaled case:
    #  if wf == 0 and wg == 0:
    #    return 0
    #    result = 0
    #  else:
    # return (wf + wg - wfg)/(2*max(wf,wg))
    #    result = (wf + wg - wfg)/(2*max(wf,wg))
    return (2 - wfg) / 2


#  print("result:",result)
#  return result

def superposition_simm(A, B):
    if len(A) == 0 or len(B) == 0:
        return 0
    if len(A) == 1 and len(B) == 1:
        if A.label != B.label:  # put a.label == '' test in here too?
            return 0
        a = max(A.value, 0)  # just making sure they are >= 0.
        b = max(B.value, 0)
        if a == 0 and b == 0:  # prevent div by zero.
            return 0
        return min(a, b) / max(a, b)
    #  return intersection(A.normalize(),B.normalize()).count_sum()     # very slow version!

    # now calculate the superposition version of simm, while trying to be as fast as possible:
    try:
        merged = {}
        one_sum = 0
        one = {}
        for label, value in A.drop().items():  # handle superpositions with negative coeffs by dropping them, for now! Improve later!!
            one[label] = value
            one_sum += value  # assume all values in A are >= 0
            merged[label] = True  # potentially we could use abs(elt.value)

        two_sum = 0
        two = {}
        for label, value in B.drop().items():
            two[label] = value
            two_sum += value  # assume all values in B are >= 0
            merged[label] = True

        # prevent div by zero:
        if one_sum == 0 or two_sum == 0:
            return 0

        merged_sum = 0
        for key in merged:
            if key in one and key in two:
                v1 = one[key] / one_sum
                v2 = two[key] / two_sum
                merged_sum += min(v1, v2)
        return merged_sum
    except Exception as e:
        print("fast_simm exception reason: %s" % e)


#  if type(A) is sequence:                     # hack just for now, until we can implement a sequence version of simm.
#    A = A[0]
#  if type(B) is sequence:
#    B = B[0]

# set invoke method:
whitelist_table_2['aligned-simm'] = 'aligned_simm'
# set usage info:
sequence_functions_usage['aligned-simm'] = """
    description:
      the aligned sequences version of our similarity measure
      for each superposition in our sequences, calculate the similarity measure
      (ie, 0 for completely distinct, 1 for exactly the same, values in between otherwise)
      then average them
            
    examples:
      aligned-simm(|a>, |b>)
        |0>
        
      aligned-simm(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)
        |0.462>

      aligned-simm(|a1> + |a2> . 0.3|b1> + 0.5|b2> , 3|a1> + 0.9|a2> . 0.7|b2>)
        |0.678>

    see also: 
"""


def aligned_simm(one, two):
    # return ket(float_to_int(aligned_simm_value(one, two)))  # not sure which version we want.
    return ket('simm', aligned_simm_value(one, two))


def aligned_simm_value(one, two):
    one, two = normalize_seq_len(one, two)
    if len(one) == 0:
        return 0
    r = 0  # for now just average the results. Min of results is a stricter alternative
    for k in range(len(one)):
        r += superposition_simm(one[k], two[k])
    return r / len(one)


# set invoke method:
# compound_table['predict'] = ".apply_seq_fn(predict_next, context, \"{0}\")"
compound_table['predict'] = ['apply_seq_fn', 'predict_next', 'context']
# set usage info:
function_operators_usage['predict'] = """
    description:
      given an input sequence, predict what is next
      optionally specify the max sequence length you want returned
            
    examples:
      seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7> . |8> . |9> . |10>
      seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>
      seq |fact> => |1> . |2> . |6> . |24> . |120>
      seq |primes> => |2> . |3> . |5> . |7> . |11> . |13> . |17> . |19> . |23>
      predict[seq] (|2> . |5>)
        1.0     count   |6> . |7> . |8> . |9> . |10>
        1.0     fib     |8> . |13>
        1.0     primes  |7> . |11> . |13> . |17> . |19> . |23>
        0.5     fact    |6> . |24> . |120>
        |count: 6 . 7 . 8 . 9 . 10> + |fib: 8 . 13> + |primes: 7 . 11 . 13 . 17 . 19 . 23> + 0.5|fact: 6 . 24 . 120>

      predict[seq,3] (|2> . |5>)
        1.0     count   |6> . |7> . |8>
        1.0     fib     |8> . |13>
        1.0     primes  |7> . |11> . |13>
        0.5     fact    |6> . |24> . |120>
        |count: 6 . 7 . 8> + |fib: 8 . 13> + |primes: 7 . 11 . 13> + 0.5|fact: 6 . 24 . 120>
        
      extract-category predict[seq] (|2> . |5> . |7>)
        1.0     count   |8> . |9> . |10>
        1.0     primes  |11> . |13> . |17> . |19> . |23>
        0.5     fib     |8> . |13>
        0.25    fact    |6> . |24> . |120>
        |count> + |primes> + 0.5|fib> + 0.25|fact>

      extract-value predict[seq] (|2> . |5> . |7>)
        1.0     count   |8> . |9> . |10>
        1.0     primes  |11> . |13> . |17> . |19> . |23>
        0.5     fib     |8> . |13>
        0.25    fact    |6> . |24> . |120>
        |8 . 9 . 10> + |11 . 13 . 17 . 19 . 23> + 0.5|8 . 13> + 0.25|6 . 24 . 120>
        
      extract-value predict[seq,1] (|2> . |5> . |7>)
        1.0     count   |8>
        1.0     primes  |11>
        0.5     fib     |8>
        0.25    fact    |6>
        1.5|8> + |11> + 0.25|6>

    see also: 
"""


# def predict_next(context, one, parameters):                     # maybe change invoke order, so context comes first??
def predict_next(one, context, *params):  # doesn't look easy to change invoke order. Eg, go see: apply_seq_fn() in the sequence class.
    op = params[0]
    if len(params) == 1:
        count = False
    else:
        try:
            count = int(params[1])
        except:
            return ket()

    # pattern is a superposition
    # sequence is a sequence
    def find_similar_index(pattern, sequence, t=0):
        similar_index = superposition()
        for k, x in enumerate(sequence):
            value = superposition_simm(pattern, x)
            if value > t:
                similar_index.add(str(k + 1), value)
        return similar_index

    def find_next_sequences(sp, sequences):
        next_sequences = []
        for coeff, name, seq in sequences:
            for pos, value in find_similar_index(sp, seq).items():
                next_seq = sequence([]) + seq[int(pos):]
                next_sequences.append([value * coeff, name, next_seq])
        return next_sequences

    def find_next_sequences_v2(sp, sequences):
        next_sequences = []
        for coeff, name, seq in sequences:
            similar_index = find_similar_index(sp, seq)
            if len(similar_index) == 0:
                next_sequences.append([coeff / 2, name, seq])
            else:
                for pos, value in similar_index.items():
                    next_seq = sequence([]) + seq[int(pos):]
                    next_sequences.append([value * coeff, name, next_seq])
        return next_sequences

    # load up our sequences:
    sequences = []
    for elt in context.relevant_kets(op):
        seq = context.recall(op, elt, True)
        sequences.append([1, elt.label, seq])

    # filter our sequences:
    next_sequences = sequences
    for sp in one:  # assumes one is a sequence
        next_sequences = find_next_sequences_v2(sp, next_sequences)

    # print out our sequences:
    r = superposition()
    for coeff, name, seq in sorted(next_sequences, key=lambda x: x[0], reverse=True):
        if count is not False:
            seq = sequence([]) + seq[:count]
        print('%s\t%s\t%s' % (coeff, name, str(seq)))
        str_seq = smerge(seq, ' . ').label
        r.add(name + ": " + str_seq, coeff)
    return r


# set invoke method:
sp_fn_table['sp2seq'] = 'sp2seq'  # maybe it should be in seq_fn_table?
# set usage info:
function_operators_usage['sp2seq'] = """
    description:
      sp2seq converts superpositions into sequences
      
    examples:
      sp2seq range(|1>, |5>)
        |1> . |2> . |3> . |4> . |5>
"""


# one is a superposition:
def sp2seq(one):
    seq = sequence([])
    for x in one:
        seq += x
    return seq


# set invoke method:
seq_fn_table['seq2sp'] = 'seq2sp'
# set usage info:
function_operators_usage['seq2sp'] = """
    description:
      seq2sp flattens sequences into superpositions

    examples:
      seq2sp (|a> + 2.2|b> . 3|c> . 0.2|d> + |x> . 7|y> + 9|z>)
        |a> + 2.2|b> + 3|c> + 0.2|d> + |x> + 7|y> + 9|z>
"""


# one is a sequence:
def seq2sp(one):
    return one.to_sp()


# TODO:
# greater-than[51] SP
# greater-equal-than[30] SP
# less-than[3] SP
# equal[37] SP
# in-range[300,700]
# we already have in-range sigmoid.
# maybe they should all be sigmoids??
# yeah, but then all the push-float, pop-float, and drop is needed.
#
# eg:
# is-greater-than[3] |5> == |5>
# is-greater-than[7] |6> == |>
# is-greater-than[13] |age: 14> == |age: 14>
# assumes one is a ket
def greater_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[
                          -1])  # NB: if one is not a ket, one.label fails, and the exception is tripped. Neat!
    except:
        return ket()
    if value > t:
        return one
    return ket()


def greater_equal_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value >= t:
        return one
    return ket()


def less_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value < t:
        return one
    return ket()


def less_equal_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value <= t:
        return one
    return ket()


def equal(one, t):  # name clash with equal(SP1,SP2)??
    epsilon = 0.0001  # Need code since equal and float don't work well together.
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if (t - epsilon) <= value <= (t + epsilon):
        return one
    return ket()


def in_range(one, t1, t2):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if t1 <= value <= t2:
        return one
    return ket()


# set invoke method:
# compound_table['is-greater-than'] = ".apply_fn(is_greater_than,{0})"
compound_table['is-greater-than'] = ['apply_fn', 'is_greater_than', '']
# set usage info:
function_operators_usage['is-greater-than'] = """
    description:
      
    examples:
      is-greater-than[3] |price: 3.50>
        |yes>
"""


def is_greater_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[
                          -1])  # NB: if one is not a ket, one.label fails, and the exception is tripped. Neat!
    except:
        return ket()
    if value > t:
        return ket('yes')
    return ket('no')


# set invoke method:
# compound_table['is-greater-equal-than'] = ".apply_fn(is_greater_equal_than,{0})"
compound_table['is-greater-equal-than'] = ['apply_fn', 'is_greater_equal_than', '']
# set usage info:
function_operators_usage['is-greater-equal-than'] = """
    description:
      
    examples:
"""


def is_greater_equal_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value >= t:
        return ket('yes')
    return ket('no')


# set invoke method:
# compound_table['is-less-than'] = ".apply_fn(is_less_than,{0})"
compound_table['is-less-than'] = ['apply_fn', 'is_less_than', '']
# set usage info:
function_operators_usage['is-less-than'] = """
    description:
      
    examples:
"""


def is_less_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value < t:
        return ket('yes')
    return ket('no')


# set invoke method:
# compound_table['is-less-equal-than'] = ".apply_fn(is_less_equal_than,{0})"
compound_table['is-less-equal-than'] = ['apply_fn', 'is_less_equal_than', '']
# set usage info:
function_operators_usage['is-less-equal-than'] = """
    description:
      
    examples:
"""


def is_less_equal_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value <= t:
        return ket('yes')
    return ket('no')


# set invoke method:
# compound_table['is-equal'] = ".apply_fn(is_equal,{0})"
compound_table['is-equal'] = ['apply_fn', 'is_equal_op', '']
# set usage info:
function_operators_usage['is-equal'] = """
    description:
      
    examples:
"""


def is_equal_op(one, t):  # name clash with equal(SP1,SP2)?? Yup!
    epsilon = 0.0001  # Need code since equal and float don't work well together.
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if (t - epsilon) <= value <= (t + epsilon):
        return ket('yes')
    return ket('no')


# set invoke method:
# compound_table['is-in-range'] = ".apply_fn(is_in_range,{0})"
compound_table['is-in-range'] = ['apply_fn', 'is_in_range', '']
# set usage info:
function_operators_usage['is-in-range'] = """
    description:
      
    examples:
"""


def is_in_range(one, t1, t2):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if t1 <= value <= t2:
        return ket('yes')
    return ket('no')


# set invoke method:
context_whitelist_table_2['op-zip'] = 'op_zip'
# set usage info:
sequence_functions_usage['op-zip'] = """
    description:
      zip together a sequence of operators and a sequence of objects
      stops at the end of the shorter of the two sequences
            
    examples:
      op1 |*> #=> |op1: > _ |_self>
      op2 |*> #=> |op2: > _ |_self>
      op3 |*> #=> |op3: > _ |_self>
      op4 |*> #=> |op4: > _ |_self>
      op |seq> => |op: op1> . |op: op2> . |op: op3> . |op: op4>
      the |seq> => |a> . |b> . |c> . |d> . |e> . |f>
      op-zip(op |seq>, the |seq>)
      |op1: a> . |op2: b> . |op3: c> . |op4: d>
      
    see also:
      n2w in the big-numbers-to-words example
"""


# one, two are sequences
def op_zip(context, one, two):
    min_len = min(len(one), len(two))
    seq = sequence([])
    for k in range(min_len):
        op = one[k].label
        sp = two[k]
        if op.startswith('op: '):
            op = op[4:]
            r = sp.apply_op(context, op)
            seq += r
    return seq


# set invoke method:
whitelist_table_3['if'] = 'bko_if'
# set usage info:
sequence_functions_usage['if'] = """
    description:
      a crude approximation of an if function
      NB: it does not work the way you think it does!
      
      For example:
        if(some|condition>, branch|a>, branch|b>)
      evaluates all sequences: some|condition>, branch|a>, branch|b> before it is even fed to the if function.
      This is a big problem if you try to use it for recursion.
      But it is possible if you do an extra couple of steps:
        process-if if(some|condition>, |a>, |b>)
        process-if |a> #=> foo1
        process-if |b> #=> foo2
      Or:
        process-if if(some|condition>, |a:> __ |_self> , |b:> __ |_self>)
        process-if |a: *> #=> foo1 remove-leading-category |_self>
        process-if |b: *> #=> foo2 remove-leading-category |_self>
        
      3 parameter version:
        if(some|condition>, |branch a>, |branch b>, |branch c>)
      returns |branch a> if some|condition> is 'true' or 'yes'
      returns |branch b> if some|condition> is 'false' or 'no'
      returns |branch c> otherwise
                      
    examples:
      split-num |*> #=> process-if if(is-less-than[1000] |_self>, |less than 1000:> __ |_self>, |greater than 1000:> __ |_self>)
      process-if |less than 1000: *> #=> remove-leading-category |_self>
      process-if |greater than 1000: *> #=> mod[1000] remove-leading-category |_self> . split-num int-divide-by[1000] remove-leading-category |_self>

      split-num |532>
        |532>

      split-num |12345>
        |345> . |12>

      split-num |12345678901234567890>
        |890> . |567> . |234> . |901> . |678> . |345> . |12>
        
      if(|True>, |a>, |b>, |c>)
        |a>
        
      if(|False>, |a>, |b>, |c>)
        |b>
        
      if(|>, |a>, |b>, |c>)
        |c>
      
      if(|fish>, |a>, |b>, |c>)
        |c>
      
    see also:
      big-numbers-to-words example
      wif
"""


# 13/4/2014:
# Let's add an if/else statement to BKO.
# Motivated by recursion works without even trying (though vastly inefficient at the moment).
# So seems sensible to add if/else too.
#
# bko_if(|True>,|a>,|b>)  -- returns |a>
# bko_if(|False>,|c>,|d>) -- returns |d>
def bko_if(condition, one, two):
    #  print('condition: %s' % condition)
    #  print('one: %s' % one)
    #  print('two: %s' % two)
    if condition.to_sp().label.lower() in ["true", "yes"]:
        return one
    else:
        return two


# set invoke method:
whitelist_table_4['if'] = 'bko_if_3'


def bko_if_3(condition, one, two, three):
    condition = condition.to_sp().label.lower()
    if condition in ["true", "yes"]:
        return one
    if condition in ["false", "no"]:
        return two
    else:
        return three


# set invoke method:
whitelist_table_2['wif'] = 'weighted_bko_if'
# set usage info:
sequence_functions_usage['wif'] = """
    description:
      a weighted if
      works just like standard 'if', but takes into consideration the coefficient of the condition
      
    examples:
      wif(0.7|True>, |a>, |b>)
        0.7|a> + 0.3|b>
        
      wif(0.8|False>, |a>, |b>)
        0.2|a> + 0.8|b> 
        
    future:
      fix! It doesn't work quite right yet.
      
    see also:
      if
"""


# 14/12/2014:
# Let's add a weighted if to BKO.
# eg: wif(0.7|True>,|a>,|b>)
# returns: 0.7|a> + 0.3|b>
# and
# wif(0.8|False>,|a>,|b>)
# returns: 0.2|a> + 0.8|b>
# assumes the coeff of True/False is in [0,1] otherwise we get negative coeffs.
# though we can filter those using drop().
#
def weighted_bko_if(condition, one, two):
    label = condition.to_sp().label
    value = condition.to_sp().value
    if label.lower() in ["true", "yes"]:
        return one.multiply(value) + two.multiply(1 - value)
    else:
        return one.multiply(1 - value) + two.multiply(value)


def numbers_fn(foo, one, t):
    cat, value = extract_category_value(one.label)
    try:
        value = int(value)
    except:
        try:
            value = float(value)
        except:
            return one
    if len(cat) > 0:
        cat += ': '
    result = foo(value, t)
    return ket(cat + str(result), one.value)


# set invoke method:
# compound_table['round'] = ".apply_fn(round_numbers, {0})"
compound_table['round'] = ['apply_fn', 'round_numbers', '']
# set usage info:
function_operators_usage['round'] = """
    description:
      round the value in the ket, leaving the coefficient unchanged
      
    examples:
      round[3] |3.14159265>
        |3.142>

    see also:
      times-by, divide-by, int-divide-by, plus, minus, mod, is-mod    
"""


def round_numbers(one, t):  # cool, this one seems to work. Now need to do the rest.
    return numbers_fn(round, one, t)


# set invoke method:
# compound_table['times-by'] = ".apply_fn(times_numbers, {0})"
compound_table['times-by'] = ['apply_fn', 'times_numbers', '']
# set usage info:
function_operators_usage['times-by'] = """
    description:
      times the value in the ket, leaving the coefficient unchanged
      
    examples:
      times-by[5] |6.1>
        |30.5>

    see also:
      round, divide-by, int-divide-by, plus, minus, mod, is-mod    
"""


def times_numbers(one, t):
    def multiply(a, b):
        return a * b

    return numbers_fn(multiply, one, t)


# set invoke method:
# compound_table['divide-by'] = ".apply_fn(times_numbers, 1/{0})"
compound_table['divide-by'] = ['apply_fn', 'divide_numbers', '']
# set usage info:
function_operators_usage['divide-by'] = """
    description:
      divide the value in the ket, leaving the coefficient unchanged
      
    examples:
      divide-by[5] |625.5>
        

    see also:
      round, times-by, int-divide-by, plus, minus, mod, is-mod    
"""


def divide_numbers(one, t):
    def divide(a, b):
        return a / b

    return numbers_fn(divide, one, t)


# set invoke method:
# compound_table['int-divide-by'] = ".apply_fn(int_divide_numbers, {0})"
compound_table['int-divide-by'] = ['apply_fn', 'int_divide_numbers', '']
# set usage info:
function_operators_usage['int-divide-by'] = """
    description:
      integer divide the value in the ket, leaving the coefficient unchanged
      
    examples:
      int-divide-by[1000] |123456>
        |123>        

    see also:
      round, times-by, divide-by, plus, minus, mod, is-mod    
"""


def int_divide_numbers(one, t):  # cool, times_numbers, and plus_numbers both seem to work!
    def int_divide(a, b):
        return a // b

    return numbers_fn(int_divide, one, t)


# set invoke method:
# compound_table['plus'] = ".apply_fn(plus_numbers, {0})"
compound_table['plus'] = ['apply_fn', 'plus_numbers', '']
# set usage info:
function_operators_usage['plus'] = """
    description:
      add to the value in the ket, leaving the coefficient unchanged
      
    examples:
      plus[5] |3.14159265>
        |8.14159265>

    see also:
      round, times-by, divide-by, int-divide-by, minus, mod, is-mod    
"""


def plus_numbers(one, t):
    def add(a, b):
        return a + b

    return numbers_fn(add, one, t)


# set invoke method:
# compound_table['minus'] = ".apply_fn(plus_numbers, -{0})"
compound_table['minus'] = ['apply_fn', 'minus_numbers', '']
# set usage info:
function_operators_usage['minus'] = """
    description:
      subtract from the value in the ket, leaving the coefficient unchanged
      
    examples:
      minus[2] |3.14159265>
        |1.1415926500000002>

    see also:
      round, times-by, divide-by, int-divide-by, plus, mod, is-mod    
"""


def minus_numbers(one, t):
    def sub(a, b):
        return a - b

    return numbers_fn(sub, one, t)


# set invoke method:
# compound_table['mod'] = ".apply_fn(mod_numbers, {0})"
compound_table['mod'] = ['apply_fn', 'mod_numbers', '']
# set usage info:
function_operators_usage['mod'] = """
    description:
      apply the modulus to the value in the ket, leaving the coefficient unchanged
      
    examples:
      mod[1000] |1234567>
        |567>

    see also:
      round, times-by, divide-by, int-divide-by, plus, minus, is-mod    
"""


def mod_numbers(one, t):
    def mod(a, b):
        return a % b

    return numbers_fn(mod, one, t)


# set invoke method:
# compound_table['is-mod'] = ".apply_fn(is_mod_numbers, {0})"
compound_table['is-mod'] = ['apply_fn', 'is_mod_numbers', '']
# set usage info:
function_operators_usage['is-mod'] = """
    description:
      answers yes or no, if the given number is mod n
      
    examples:
      is-mod[3] |96>
        |yes>
        
      is-mod[17] |51>
        |yes>
        
      is-mod[5] |51>
        |no>
      
    see also:
      round, times-by, divide-by, int-divide-by, plus, minus, mod    
"""


def is_mod_numbers(one, t):
    def mod(a, b):
        return a % b

    return equal(numbers_fn(mod, one, t), 0).is_not_empty()  # maybe needs |> option too??


# set invoke method:
# compound_table['learn-map'] = ".apply_naked_fn(learn_map, context, \"{0}\")"
compound_table['learn-map'] = ['apply_naked_fn', 'learn_map', 'context']
# set usage info:
function_operators_usage['learn-map'] = """
    description:
      learn a rectangular map
      
    examples:
      learn-map[20,20]
      
    see also:
      display-map
"""


def learn_map(context, *params):
    if len(params) != 2:
        return ket()
    h, w = params
    h = int(h)
    w = int(w)

    def ket_elt(j, i):
        return ket("grid: " + str(j) + ": " + str(i))

    # Makes use of the fact that context.learn() ignores rules that are the empty ket |>.
    def ket_elt_bd(j, i, I, J):
        # finite universe model:
        if i <= 0 or j <= 0 or i > I or j > J:
            return ket()
        # torus model:
        #  i = (i - 1)%I + 1
        #  j = (j - 1)%J + 1
        return ket_elt(j, i)

    for j in range(1, w + 1):
        for i in range(1, h + 1):
            elt = ket_elt(j, i)
            context.learn('value', elt, '0')
            context.learn("N", elt, ket_elt_bd(j - 1, i, h, w))
            context.learn("NE", elt, ket_elt_bd(j - 1, i + 1, h, w))
            context.learn("E", elt, ket_elt_bd(j, i + 1, h, w))
            context.learn("SE", elt, ket_elt_bd(j + 1, i + 1, h, w))
            context.learn("S", elt, ket_elt_bd(j + 1, i, h, w))
            context.learn("SW", elt, ket_elt_bd(j + 1, i - 1, h, w))
            context.learn("W", elt, ket_elt_bd(j, i - 1, h, w))
            context.learn("NW", elt, ket_elt_bd(j - 1, i - 1, w, w))
    return ket('learn-map')


# set invoke method:
# compound_table['display-map'] = ".apply_naked_fn(display_map, context, \"{0}\")"
compound_table['display-map'] = ['apply_naked_fn', 'display_map', 'context']
# set usage info:
function_operators_usage['display-map'] = """
    description:
      display a rectangular map
      
    examples:
      learn-map[5,5]
      display-map[5,5]
        h: 5
        w: 5
        1     .  .  .  .  .
        2     .  .  .  .  .
        3     .  .  .  .  .
        4     .  .  .  .  .
        5     .  .  .  .  .
      
    see also:
      learn-map
"""


def display_map(context, *params):
    if len(params) < 2:
        return ket()
    if len(params) == 2:
        h, w = params
        op = 'value'
    if len(params) == 3:
        h, w, op = params
    w = int(w)
    h = int(h)

    def ket_elt(j, i):
        return ket("grid: " + str(j) + ": " + str(i))

    s = ""
    s += "h: " + str(h) + "\n"
    s += "w: " + str(w) + "\n"

    for j in range(1, w + 1):
        s += str(j).ljust(4)
        for i in range(1, h + 1):
            x = ket_elt(j, i)
            current_cell = context.recall('current', 'cell', True).to_sp()
            if current_cell.label == x.label:
                value = '###'
            else:
                value = context.recall(op, x, True).to_sp()
                if value.label == ' ':
                    value = float_to_int(value.value)
                else:
                    value = value.label
            if value == "0":
                # value = "."
                value = ' '
            s += value.rjust(3)
        s += "\n"
    print(s)
    return ket('display-map')


# set invoke method:
seq_fn_table['merge-value'] = 'merge_value'
# set usage info:
function_operators_usage['merge-value'] = """
    description:
      merges coeff's and label's into a single number
      works with superpositions, and sequences:
      
    examples:
      -- superposition example:
      merge-value (0|3> + 3|1> + 5|2>)
        |13>

      -- sequence of superpositions example:        
      merge-value (0|3> + 1|7> . 4|2> + 5|3> + 4|5>)
        |50>
"""


# one is a sequence
def merge_value(one):
    r = 0
    for sp in one:
        for x in sp:
            try:
                r += float(x.label) * x.value
            except:
                pass
    return ket(float_to_int(r))


# set invoke method:
whitelist_table_2['and'] = 'And'
# set usage info:
sequence_functions_usage['and'] = """
    description:
      simple 'and'
      NB: it evaluates both sequences before being passed to the 'and' function
      NB: it (currently?) only uses the first superposition in the given sequences
      
    examples:
      and(|yes>, |yes>)
        |yes>
        
      and(|yes>, |no>)
        |no>
    
    see also:
      if, or, xor
"""


def And(one, two):
    if one.to_sp().label.lower() in ['true', 'yes'] and two.to_sp().label.lower() in ['true', 'yes']:
        return ket('yes')
    return ket('no')


# set invoke method:
whitelist_table_2['or'] = 'Or'
# set usage info:
sequence_functions_usage['or'] = """
    description:
      simple 'or'
      NB: it evaluates both sequences before being passed to the 'or' function
      NB: it (currently?) only uses the first superposition in the given sequences
      
    examples:
      or(|yes>, |yes>)
        |yes>
        
      or(|yes>, |no>)
        |yes>
        
      or(|no>, |no>)
        |no>
    
    see also:
      if, and, xor
"""


def Or(one, two):
    one = one.to_sp()
    two = two.to_sp()
    if one.label.lower() in ['true', 'yes'] and two.label.lower() in ['true', 'yes']:
        return ket('yes', max(one.value, two.value))
    if one.label.lower() in ['true', 'yes'] and not two.label.lower() in ['true', 'yes']:
        return ket('yes', one.value)
    if not one.label.lower() in ['true', 'yes'] and two.label.lower() in ['true', 'yes']:
        return ket('yes', two.value)
    return ket('no')


# set invoke method:
compound_table['common'] = ['apply_sp_fn', 'common', 'context']
# set usage info:
function_operators_usage['common'] = """
    description:
      find kets in common, with respect to an operator
      
    examples:
      friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
      friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Rober> + |Frank> + |Julie>
      common[friends] split |Fred Sam>
        |Jack> + |Emma> + |Charlie>
"""
#
# 8/5/2014:
# common[op] (|x> + |y> + |z>)
# eg: common[friends] (|Fred> + |Sam>)
# eg: common[actors] (|movie-1> + |movie-2>)
# or indirectly
# |list> => |Fred> + |Sam> + |Charles>
# common[friends] "" |list>
def common(one, context, op):
    if len(one) == 0:
        return ket()
    for sp in one:
        r = sp.apply_op(context, op)
        break
    for sp in one:
        tmp = sp.apply_op(context, op)
        r = intersection(r, tmp)
    return r


# 2/2/2015:
# int-coeffs-to-sentence (3|apple> + 2|pear> + |orange> + 7|lemon>)
# |3 apples, 2 pears, 1 orange and 7 lemons>
# def int_coeffs_to_sentence(one,context):

# set invoke method:
ket_context_table['int-coeffs-to-word'] = 'int_coeffs_to_word'
# set usage info:
function_operators_usage['int-coeffs-to-word'] = """
    description:
      apply the coefficient to the word,
      and map the word to plural as required
      
    examples:
      plural |*> #=> |_self> _ |s>
      plural |mouse> => |mice>
      plural |tooth> => |teeth>
      int-coeffs-to-word (3|apple> + 2|pear> + |orange> + 7|lemon> + 3|mouse> + 2|tooth> + 9|cat>)
        |3 apples> + |2 pears> + |1 orange> + |7 lemons> + |3 mice> + |2 teeth> + |9 cats>
      
      list-to-words int-coeffs-to-word (3|apple> + 2|pear> + |orange> + 7|lemon> + 3|mouse> + 2|tooth> + 9|cat>)
        |3 apples, 2 pears, 1 orange, 7 lemons, 3 mice, 2 teeth and 9 cats>   

    see also:
      list-to-words, words-to-list
"""


# 2/2/2015:
# int-coeffs-to-word (3|apple> + 2|pear> + |orange> + 7|lemon>)
# |3 apples> + |2 pears> + |1 orange> + |7 lemons>
#
# Here is one common usage, combine it with list-to-words:
# sa: list-to-words int-coeffs-to-word (|apple> + 3|mouse> + 2|tooth> + 9|cat>)
# |1 apple, 3 mice, 2 teeth and 9 cats>
#
# assumes one is a ket
def int_coeffs_to_word(one, context):  # at some point maybe we want float_coeffs_to_word??
    label = one.label
    value = int(one.value)
    if value == 0:
        value = "no"
    if value != 1:
        label = one.apply_op(context, "plural").to_sp().label
        if label == '':
            label = one.label  # maybe return |> if plural not known? or the fed in ket? The fed in ket, is the correct way to do this.
    return ket(str(value) + " " + label)


# code from here:
# http://stackoverflow.com/questions/16996217/prime-factorization-list
def primes(n):
    print("n:", n)
    f, fs = 3, []
    while n % 2 == 0:
        fs.append(2)
        n //= 2  # this is the fix.
    while f * f <= n:
        while n % f == 0:
            fs.append(f)
            n //= f  # and this too.
        f += 2
    if n > 1: fs.append(n)
    print("factors:", fs)
    return fs


# set invoke method:
fn_table['is-prime'] = 'is_prime'
# set usage info:
function_operators_usage['is-prime'] = """
    description:
      returns |yes> or |no> if a prime or not

    examples:
      is-prime |379721>
        |yes>

    see also:
      prime-factors
"""


# returns |yes> if |x> is a prime, else |no>
# x is a ket
def is_prime(x):
    cat, v = extract_category_value(x.label)
    try:
        n = int(v)
    except:
        return ket()
    if n <= 1:
        return ket()

    if len(primes(n)) == 1:
        return ket("yes")
    else:
        return ket("no")


# the factor number function
# eg: factor |number: 30>  returns |number: 2> + |number: 3> + |number: 5>
# interestingly, you could use this to find in a completely different space,
# a set of objects that have the identical factor structure as positive integers.
# a weird kind of duality between primes and that other space.
# or I guess, an isomorphism.
#
# Though I guess that is a general idea.
# An example is say the network structure of your friends network
# can be identical to say the network structure of a certain set of websites.
# The only differentiator is the ket labels of the components.
# This also has the implication that reconstructing meaning
# just from a (local) network of neurons is essentially impossible.
# Without broader knowledge, the network could represent pretty much anything!
# x must be a ket! Or it bugs out in weird ways.
# set invoke method:
fn_table['prime-factors'] = 'factor_number'
# set usage info:
function_operators_usage['prime-factors'] = """
    description:
      returns a list of prime factors

    examples:
      -- without specifying a category:
      prime-factors |987654321>
        2|3> + 2|17> + |379721>
      
      -- with specifying a category, here 'number: '
      prime-factors |number: 123456789>
        2|number: 3> + |number: 3607> + |number: 3803>

    see also:
      is-prime
"""


# x is a ket
def factor_number(x):
    cat, v = extract_category_value(x.label)
    if len(cat) > 0:
        cat += ': '
    try:
        n = int(v)
    except:
        return ket()
    if n <= 1:
        return ket()

    r = superposition()
    for p in primes(n):
        r.add(cat + str(p), x.value)
    return r


# set invoke method:
# compound_table['inherit'] = ['apply_sp_fn', 'inherit_op', 'context']
compound_table['inherit'] = ['apply_fn', 'inherit_op', 'context']
# set usage info:
function_operators_usage['inherit'] = """
    description:
      inherit operator from parent data-types

    examples:
      -- learn a little about our old cat Trudy:
      -- and the inheritance structure:
      inherit |trudy> => |cat>
      inherit |cat> => |feline>
      inherit |feline> => |mammal>
      inherit |mammal> => |animal>
      has-fur |animal> => |yes>
      has-teeth |animal> => |yes>
      has-pointy-ears |feline> => |yes>
      
      -- Trudy has no teeth, which over-rides the animal has-teeth rule:
      has-teeth |trudy> => |no>
      
      -- now ask some questions:
      inherit[has-pointy-ears] |trudy>
        |yes>

      inherit[has-fur] |trudy>
        |yes>

      inherit[has-teeth] |trudy>
        |no>
"""


def inherit_op(one, context, op):  # maybe build this into the working of the new_context() class?
    r = one.apply_op(context, op)
    if len(r) != 0:
        return r
    while True:
        one = one.apply_op(context, 'inherit')
        if len(one) == 0:
            return ket()
        r = one.apply_op(context, op)
        if len(r) != 0:
            return r


# decided to natural sort for sort-by[], so need this:
# http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
# 6/8/2014: Doh! There is a bug in sorting things like 0 vs 00 vs 000.
def natural_sorted(list, key=lambda s: s):
    """
    Sort the list into natural alphanumeric order.
    """

    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]

    sort_key = get_alphanum_key_func(key)
    #    list.sort(key=sort_key)
    return sorted(list, key=sort_key)


# set invoke method:
compound_table['sort-by'] = ['apply_sp_fn', 'sort_by', 'context']
# set usage info:
function_operators_usage['sort-by'] = """
    description:
      sort the given superposition with respect to the given operator

    examples:
      load pretty-print-table-of-australian-cities.sw
      
      -- sort by area:
      table[city, area, population, annual-rainfall] sort-by[area] "" |city list>
        +-----------+------+------------+-----------------+
        | city      | area | population | annual-rainfall |
        +-----------+------+------------+-----------------+
        | Darwin    | 112  | 120900     | 1714.7          |
        | Adelaide  | 1295 | 1158259    | 600.5           |
        | Hobart    | 1357 | 205556     | 619.5           |
        | Melbourne | 1566 | 3806092    | 646.9           |
        | Sydney    | 2058 | 4336374    | 1214.8          |
        | Perth     | 5386 | 1554769    | 869.4           |
        | Brisbane  | 5905 | 1857594    | 1146.4          |
        +-----------+------+------------+-----------------+
      
      -- sort by population:
      table[city, area, population, annual-rainfall] reverse sort-by[population] "" |city list>
        +-----------+------+------------+-----------------+
        | city      | area | population | annual-rainfall |
        +-----------+------+------------+-----------------+
        | Sydney    | 2058 | 4336374    | 1214.8          |
        | Melbourne | 1566 | 3806092    | 646.9           |
        | Brisbane  | 5905 | 1857594    | 1146.4          |
        | Perth     | 5386 | 1554769    | 869.4           |
        | Adelaide  | 1295 | 1158259    | 600.5           |
        | Hobart    | 1357 | 205556     | 619.5           |
        | Darwin    | 112  | 120900     | 1714.7          |
        +-----------+------+------------+-----------------+

"""
# one is a superposition
def sort_by(one, context, op):
    def extract_ket_details(x):
        return x.apply_op(context, op).to_sp().label.lower()

    try:
        working_sp = [[k, extract_ket_details(x)] for k, x in enumerate(one)]
        sorted_sp = natural_sorted(working_sp, key=lambda x: x[1])
        data = list(one.items())
        r = superposition()
        for k, _ in sorted_sp:
            r.add(*data[k])
        return r
    except Exception as e:
        logger.info('sort-by exception.\nReason: %s' % e)
        return ket()


# set invoke method:
fn_table['read'] = 'read_text'
# set usage info:
function_operators_usage['read'] = """
    description:
      'read' a sentence

    examples:
"""
# one is a ket or superposition:
def read_text(one):
    cat, text = extract_category_value(one.label)
    text = "".join(c for c in text.lower() if c in 'abcdefghijklmnopqrstuvwxyz\'- ').split()

    seq = sequence([])
    for w in text:
        seq += ket('word: ' + w)
    return seq

# set invoke method:
compound_table['active-buffer'] = ['apply_seq_fn', 'active_buffer', 'context']
# one is a sequence:
def active_buffer(one, context, *params):
    #print('one: %s' % str(one))
    #print('params: %s' % str(params))
    try:
        N, t, op = params
        N = int(N)
        t = float(t)
    except:
        try:
            N, t = params
            N = int(N)
            t = float(t)
            op = ""
        except:
            return ket()
    seq = sequence([])
    for k in range(len(one.data)):
        sp = superposition()
        for n in range(min(N, len(one.data) - k)):
            y = sequence([])
            y.data = one.data[k:k+n+1]
            r = context.pattern_recognition(y, op).drop_below(t)
            #print('y: %s' % str(y))
            #print('r: %s\n' % str(r))
            if len(r) > 0:
                sp = union(sp, r)
        seq += sp
    return seq


# set invoke method:
sp_fn_table['list-to-words'] = 'sp_to_words'
# set usage info:
function_operators_usage['list-to-words'] = """
    description:
      convert the given superposition into a comma-separated word list
      it is the inverse of words-to-list

    examples:
      list-to-words |x>
        |x>
      
      list-to-words (|x> + |y>)
        |x and y>

      list-to-words (|x> + |y> + |z>)
        |x, y and z>
        
      list-to-words (|a> + |b> + |c> + |d> + |e>)
        |a, b, c, d and e>

      friends |Eric> => |Sam> + |Harry> + |Mary> + |Liz>
      list-to-words friends |Eric>
        |Sam, Harry, Mary and Liz>
    
      -- demonstration of inverse property:
      words-to-list list-to-words (|a> + |b> + |c> + |d> + |e>)
        |a> + |b> + |c> + |d> + |e>
      
    future:
      maybe also have an 'or' version too: 'x, y or z' 

    see also:
      words-to-list
"""
# one is a superposition
def sp_to_words(one):
    labels = [x.label for x in one]
    if len(labels) == 0:
        return ket()
    if len(labels) == 1:
        result = labels[0]
    else:
        head = ", ".join(labels[:-1])
        tail = labels[-1]
        result = head + " and " + tail
    return ket(result)


# set invoke method:
fn_table['words-to-list'] = 'words_to_sp'
# set usage info:
function_operators_usage['words-to-list'] = """
    description:
      splits the given ket on ', ' and ' and '
      it is the inverse of list-to-words

    examples:
      words-to-list |a, b, c, d and e>
        |a> + |b> + |c> + |d> + |e>
    
      -- demonstration of inverse property:
      list-to-words words-to-list |a, b, c, d and e>
        |a, b, c, d and e>
    
    see also:
      list-to-words
      
"""
# one is a ket
def words_to_sp(one):
    try:
        head, tail = one.label.split(' and ')
        front = head.split(', ')
        r = superposition()
        for x in front + [tail]:
            r.add(x)
        return r
    except Exception as e:
        logger.debug("words-to-list exception reason: " + str(e))
        return one



# lets do some temp conversion, as seen here:
# http://semantic-db.org/temperature-conversion.sw
# NB: inline code as seen on that page is a long way off!
# Hrmm... wondering if we want full names too. Celsius, Kelvin, Fahrenheit, or just the single letters?
# Should be easy enough. Just temperature_type[0] == 'C' and so on. Done.
# Is there any way to compact the logic down a bit?
def to_temperature_type(one, convert_to_type='C'):  # I'm Aussie, so default is C.
    print("one:", one)
    p = one.the_label().split(": ")
    if len(p) < 2:  # check for p[-2] out of index
        return ket("", 0)
    try:
        t = float(p[-1])
    except:
        return ket("", 0)
    label = ": ".join(p[:-2] + [convert_to_type])
    label += ": "
    temperature_type = p[-2]
    if convert_to_type[0] == 'F':
        if temperature_type[0] == 'F':
            pass
        elif temperature_type[0] == 'C':
            t = t * 9 / 5 + 32
        elif temperature_type[0] == 'K':
            t = t * 9 / 5 - 459.67
        else:
            return ket("", 0)

    elif convert_to_type[0] == 'C':
        if temperature_type[0] == 'F':
            t = (t - 32) * 5 / 9
        elif temperature_type[0] == 'C':
            pass
        elif temperature_type[0] == 'K':
            t = t - 273.15
        else:
            return ket("", 0)

    elif convert_to_type[0] == 'K':
        if temperature_type[0] == 'F':
            t = (t + 459.67) * 5 / 9
        elif temperature_type[0] == 'C':
            t = t + 273.15
        elif temperature_type[0] == 'K':
            pass
        else:
            return ket("", 0)
    else:
        return ket("", 0)
    return ket(label + "%.2f" % t)


def to_Fahrenheit(one):
    #  return to_temperature_type(one,'Fahrenheit')
    return to_temperature_type(one, 'F')


def to_Celsius(one):
    return to_temperature_type(one, 'C')


def to_Kelvin(one):
    return to_temperature_type(one, 'K')


# for now just km, m, and mi, but potential for a whole mess. mm, inches, cm, etc.
# Also, is there a neater way to do this?
def to_distance_type(one, convert_to_type='km'):  # I'm Aussie, so default is km
    print("one:", one)
    p = one.the_label().split(": ")
    if len(p) < 2:  # check for p[-2] out of index
        return ket()
    try:
        x = float(p[-1])
    except:
        return ket()
    label = ": ".join(p[:-2] + [convert_to_type])
    label += ": "
    distance_type = p[-2]
    if convert_to_type == 'km':
        if distance_type == 'km':
            pass
        elif distance_type == 'm':
            x = x / 1000
        elif distance_type == 'miles':
            x = x * 1.609344  # yeah, over precision!
        else:
            return ket()

    elif convert_to_type == 'm':
        if distance_type == 'km':
            x = x * 1000
        elif distance_type == 'm':
            pass
        elif distance_type == 'miles':
            x = x * 1609.344
        else:
            return ket()

    elif convert_to_type == 'miles':
        if distance_type == 'km':
            x = x / 1.609344
        elif distance_type == 'm':
            x = x / 1609.344
        elif distance_type == 'miles':
            pass
        else:
            return ket()
    else:
        return ket()
    return ket(label + float_to_int(x))


def to_km(one):
    return to_distance_type(one, 'km')


def to_meter(one):  # yeah, went for US spelling here.
    return to_distance_type(one, 'm')


def to_mile(one):
    return to_distance_type(one, 'miles')


# set invoke method:
context_whitelist_table_2['find-path-between'] = 'find_path_between'
# set usage info:
sequence_functions_usage['find-path-between'] = """
    description:
      find the path between the given kets
      potentially quite slow!
      
    examples:
      load fred-sam-friends.sw
      find-inverse[friends]
      find-path-between(|Fred>, |Sam>)
        |op: friends> . |op: inverse-friends>
        
      find-path-between(|Fred>, |Julie>)
        |op: friends> . |op: inverse-friends> . |op: friends>

        
      learn-map[10,10]
      find-path-between(|grid: 1: 1>, |grid: 3: 7>)
        |op: E> . |op: E> . |op: E> . |op: E> . |op: SE> . |op: SE>

    
      load george.sw
      find (*) #=> find-path-between(|person: George>, |_self>)
      find |person: Andrew>
        |op: friends>

      find (|person: Sarah> + |person: David> + |person: Frank>)
        |op: family>

      find (|person: Emily> + |person: Fred>)
        |op: family-and-friends>

      find (|person: Frank> + |person: Emily>)
        |op: siblings>

    future:
      optimize it!
      make it work with path-ways between sequences too.

    see also:
      finding-a-path-between-early-us-presidents worked example
"""
def first_find_path_between(context, one, two):
    max_steps = 10
    one = one.to_sp()
    two = two.to_sp()
    # print('one: %s' % str(one))
    # print('two: %s' % str(two))

    def print_path_ways(path_ways):
        for seq, r in path_ways:
            print('seq: %s' % str(seq))
            print('r: %s\n' % str(r))

    def find_path(context, path_ways):
        new_path_ways = []
        for seq, r in path_ways:
            for op in r.apply_op(context, 'supported-ops').to_sp():
                new_seq = seq + sequence(op)
                new_r = r.apply_op(context, op.label[4:])
                if len(new_r) > 0:
                    new_path_ways.append([new_seq, new_r])
        return new_path_ways

    def test_subset(A, B):              # test if one is a subset of two
        A = A.apply_sigmoid(clean)      # ignore coeffs for now
        B = B.apply_sigmoid(clean)
        r2 = intersection(A, B)
        if len(r2.to_sp()) == len(A.to_sp()):
            return True
        return False

    path_ways = [[sequence([]), one]]
    for _ in range(max_steps):
        path_ways = find_path(context, path_ways)
        # print_path_ways(path_ways)
        for seq, r in path_ways:
            if test_subset(two, r):
                return seq.apply_sigmoid(clean)

    return ket('path not found')

def is_subset(A, B):              # test if one is a subset of two
    A = A.apply_sigmoid(clean)      # ignore coeffs for now
    B = B.apply_sigmoid(clean)
    r = intersection(A, B)
    if len(r.to_sp()) == len(A.to_sp()):
        return True
    return False

def find_path_between(context, one, two):
    max_steps = 10                      # put a hard limit on the max number of operator steps
    one = one.to_sp()
    two = two.to_sp()

    path_ways = [[sequence([]), one]]
    for _ in range(max_steps):
        new_path_ways = []
        for seq, r in path_ways:
            if len(r) > 0:              # this is probably redundant. Remove later.
                # print('r: %s' % str(r))
                # print('len(r): %s' % len(r))
                for op in r.apply_op(context, 'supported-ops').to_sp():
                    new_seq = seq + sequence(op)
                    new_r = r.apply_op(context, op.label[4:])
                    if len(new_r) > 0:
                        if is_subset(two, new_r):
                            return new_seq.apply_sigmoid(clean)
                        new_path_ways.append([new_seq, new_r])
        path_ways = new_path_ways
    return ket('path not found')


# set invoke method:
context_whitelist_table_2['find-steps-between'] = 'find_steps_between'
# set usage info:
sequence_functions_usage['find-steps-between'] = """
    description:
      find the steps between the given kets
      potentially quite slow!

    examples:
      load early-us-presidents.sw
      info off
      find-inverse[president-number]
      find-inverse[president-era]
      find-inverse[full-name]

      find-steps-between(|person: George Washington>, |number: 6>)
        |person: George Washington> . |Washington> . |year: 1797> . |Adams> . |year: 1801> . |Jefferson> . |party: Democratic-Republican> . |year: 1825> . |Q Adams> . |number: 6>

    see also:
      find-path-between
"""
def first_find_steps_between(context, one, two):
    op_path = find_path_between(context, one, two)
    if type(op_path) is ket and op_path.label == 'path not found':
        return ket('steps not found')
    path_ways = [one]
    for op in op_path:
        new_path_ways = []
        for step in path_ways:
            seq = sequence(step)
            for elt in step.apply_op(context, op.label[4:]).to_sp():
                if len(elt) > 0:
                    if is_subset(two, elt):
                        return seq + elt
                        # return (seq + elt).apply_sigmoid(clean)
                    new_path_ways.append(seq + elt)
        path_ways = new_path_ways
        # for steps in path_ways:
        #     print('steps: %s' % str(steps))
    return ket('steps not found')

def find_steps_between(context, one, two):
    op_path = find_path_between(context, one, two)
    if type(op_path) is ket and op_path.label == 'path not found':
        return ket('steps not found')
    path_ways = [one]
    for op in op_path:
        new_path_ways = []
        for step in path_ways:
            seq = sequence(step)
            next_step = step.apply_op(context, op.label[4:]).to_sp()
            if is_subset(two, next_step):
                return seq + two
                # return (seq + two).apply_sigmoid(clean)
            for elt in next_step:
                if len(elt) > 0:
                    new_path_ways.append(seq + elt.apply_sigmoid(clean))
        path_ways = new_path_ways
    return ket('steps not found')


# set invoke method:
compound_table['exp'] = ['apply_fn', 'exp', 'context']
# 12/5/2014:
# exp[child,n] |x>
# maps to: (1 + child + child^2 + ... + child^n ) |x>
# cf: exp(A) |Psi> in QM.
# if n <= 0, return |x>
#
def exp(one, context, *params):
    try:
        op, n = params
        print("exp op " + op)
        print("exp n  " + n)
        n = int(n)
    except:
        return one

    r = one
    tmp = one
    for k in range(n):
        tmp = tmp.apply_op(context, op).to_sp()  # this is broken for some operators, depends on details of that operator though!
        r += tmp
    return r


# set invoke method:
compound_table['exp-max'] = ['apply_fn', 'exp_max', 'context']
# 4/8/2014:
# exp-max[op] |x>
# maps to (1 + op + op^2 + ... op^n) |x>
# such that exp[op,n] |x> == exp[op,n+1] |x>
# Warning: we have no idea before hand how many resources this will end up using. We don't know n, or how big the sp is going to be!
#
# Need to check it works. Cool. Seems to give the right result. eg, using binary-tree.sw
# Done.
#
# Now, let's implement: exp-max[op,t] |x>
# Now need to check this one works.
#
# Something I have wanted to do for a very long time is to split an academic field of study into categories.
# Roughly: exp-max[references,t] |some seed physics paper>
# where the "references" operator applied to a paper on arxiv.org returns the list of papers it references.
# We may (though maybe not) need t > 0, else it might drag in all of arxiv.org
# But won't know this for sure until we try.
def exp_max(one, context, *params):
    try:
        op, t = params
        t = int(t)
    except:
        op = params[0]
        t = 0

    r = one
    tmp = one
    previous_size = len(r)  # yup. I finally implemented len() for superpositions/kets.
    n = 0
    while True:
        tmp = tmp.apply_op(context, op).to_sp()
        r += tmp
        #    if len(r) == previous_size:            # a variant is: len(r) - previous_size <= t
        if len(r) - previous_size <= t:  # since kets add in sp, this difference is the number of newly discovered kets.
            break  # so, if this is 0, then we have reached the end of the network.
        previous_size = len(r)  # if this is say 1, then in this round we only found 1 new ket.
        n += 1  # which in some cases is enough to say, this will suffice as the end of the network.
    print("n:", n)
    return r





# 17/4/2015:
# full-exp[child,n] |x>
# maps to: (1 + child/1 + child^2/2 + ... + child^n/n! ) |x>
# cf: exp(A) |Psi> in QM.
# if n <= 0, return |x>
#
def full_exp(one, context, parameters):
    try:
        op, n = parameters.split(",")  # slightly hackish. Don't know a better way to do it ....
        print("exp op " + op)
        print("exp n  " + n)
        n = int(n)
    except:
        return one

    r = one
    tmp = one
    for k in range(n):
        tmp = tmp.apply_op(context, op)
        r += tmp.multiply(1 / factorial(k + 1))
    return r


# 19/5/2014:
# relevant-kets[op]
# eg: relevant-kets[friends]
# returns |Fred> + |Sam>
#
# 13/2/2015: idea for a tweak:
# relevant-kets[op] |> works as normal (ie, incoming superposition is the empty superposition)
# but, a tweak:
# relevant-kets[op2] relevant-kets[op1] |>
# returns intersection(relevant-kets[op2],relevant-kets[op1])
# also: relevant-kets[op] SP
# returns intersection(relevant_kets[op],SP)
# Cool! Seems to work!
#
# 17/2/2015: Nah. I was really mixing two ideas into the one function.
# what happens if your restrict down to |> relevant-kets, then you apply one more layer, and bam all of those kets are valid? Not what we want.
# So now a distinction: relevant-kets[op], and intn-relevant-kets[op]
#
# 22/2/2015: tweak: relevant-kets[op1,op2,...] SP
# no need to do: relevant-kets[op1] relevant-kets[op2] SP
#
# set invoke method:
compound_table['intn-rel-kets'] = ['apply_sp_fn', 'intersection_relevant_kets', 'context']

def intersection_relevant_kets(one, context, *ops):
    r = one
    for op in ops:
        kets_list = context.relevant_kets(op)
        r = intersection(r, kets_list)
    return r


# 22/2/2015 tweaked: now if op == "*" it returns a sp of all known kets.
def relevant_kets(one, context, op):
    return context.relevant_kets(op)


# FINISH!!
# 26/3/2015:
# just a simple one:
# mbr(|x>,SP)
# returns the coeff of |x> in SP, if 0 or not in set return |>
# Note, you can consider this an optimization of: intn(|x>,SP), but having tested it, I'm not sure it is much of one!
# though I haven't looked at exact timings. Maybe I should.
# Note though that when we swap in fast_sp, this will drop from O(n) to roughly O(1).
#

# set invoke method:
whitelist_table_2['mbr'] = 'mbr'
# set usage info:
sequence_functions_usage['mbr'] = """
    description:
        mbr(ket, sp) returns the coeff of 'ket' in 'sp'.
        If 'ket' not in 'sp' then return |>
        
    examples:
        mbr(|b>, |a> + |b> + |c>)
            |b>
        
        mbr(|c>, 0.3|a> + 2|b> + 9.7|c> + 13|d>)
            9.7|c>

    see also:
        is-mbr, intersection
"""
def mbr(e, two):
    e_label = e.to_sp().label
    value = two.to_sp().find_value(e_label)
    if value == 0:
        return ket()
    return ket(e_label, value)


# 19/1/2/2016:
# is-mbr(|x>,SP) returns |yes> if |x> is in the SP, |no> otherwise.
# eg:
# friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
# sa: is-mbr(|Ed>,friends |Fred>)
# |yes>
# sa: is-mbr(|Frank>,friends |Fred>)
# |no>
#
# set invoke method:
whitelist_table_2['is-mbr'] = 'is_mbr'
# set usage info:
sequence_functions_usage['is-mbr'] = """
    description:
        is-mbr(ket, sp) returns |yes> if 'ket' is in 'sp', else |no>

    examples:
        is-mbr(|b>, |a> + |b> + |c>)
            |yes>

        is-mbr(|c>, 0.3|a> + 2|b> + 9.7|c> + 13|d>)
            |yes>
        
        friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
        is-mbr(|Ed>, friends |Fred>)
            |yes>
        
        is-mbr(|Frank>, friends |Fred>)
            |yes>

    see also:
        mbr
"""
def is_mbr(e, two):
    return mbr(e, two).is_not_empty()


# 9/4/2015:
# subset(one,two)
# returns degree of subsetness of one with respect to two.
# now, need to test it! Seems to work!
#

# set invoke method:
whitelist_table_2['subset'] = 'subset'
# set usage info:
sequence_functions_usage['subset'] = """
    description:
        subset(one, two) returns the degree of subsetness of 'one' with respect to 'two'
        NB: I don't understand what this function is trying to do!

    examples:
        subset(|b>, |a> + |b> + |c>)
            |subset>

        subset(|c>, 0.3|a> + 2|b> + 9.7|c> + 13|d>)
            |subset>
            
        subset(|b> + |d>, |a> + |b> + |c>)
            0.5|subset>

    see also:
"""
def subset(one, two):
    if one.to_sp().count_sum() == 0:  # prevent div by 0.
        return ket()
    value = intersection(one.to_sp(), two.to_sp()).count_sum() / one.to_sp().count_sum()
    return ket("subset", value)


# 4/1/2015:
# equal(one,two), returns:                  # name clash with "equal[70] |number: 37>"
# 1|True> if one == two
# 0|True> if one and two are completely disjoint
# values in between otherwise (makes use of unscaled_simm)
# name change from test_equal() to equality_test() due to pytest.

# set invoke method:
whitelist_table_2['equal'] = 'equality_test'
# set usage info:
sequence_functions_usage['equal'] = """
    description:
        equal(one, two) returns:
        1|True> if one == two
        0|True> if one and two are completely disjoint
        values in between otherwise
        makes use of aligned-simm

    examples:

    see also:
        aligned-simm, is-equal
"""
def equality_test(one, two):
    value = aligned_simm_value(one, two)  # NB: equal(0|x>,0|x>) returns 0|True>. Not currently sure if we want this, or need to tweak.
    return ket("True", value)


# set invoke method:
whitelist_table_2['is-equal'] = 'is_equal'
# set usage info:
sequence_functions_usage['is-equal'] = """
    description:
        is-equal(one, two) returns:
        |yes> if one == two
        |no> if one and two are completely disjoint
        values in between otherwise
        makes use of aligned-simm 

    examples:

    see also:
        aligned-simm, equal
"""
def is_equal(one, two):
    value = aligned_simm_value(one, two)
    if value > 0:
        return ket('yes', value)
    return ket('no')


# smooth[dx] a|x: 3> => a/4 |x: 3 - dx> + a/2 |x: 3> + a/4 |x: 3 + dx>
# (where dx is an int or float)
# Heh. It works. But let's just say it is sloooow....
# Probably too slow for production use, as is.
# Really need a version that applies to lists of floats,
# with none of the this back and forth with kets, and str() and junk.
# Hrmm... in further testing, the speed seems fine. Just a glitch in the matrix I suppose.
#
# What about this tweak: smooth[dx,k] |x: 100>
# instead of the current: smooth[dx]^k |x: 100>
# Yup. Good idea. Problem is, not currently obvious to me how to do it!
#
# Note, BTW. This thing converges to a Guassian smooth if you apply it enough times.
# Even smooth[d]^10 |x> should be well on the way to a Gaussian/bell curve.

# set invoke method:
compound_table['smooth'] = ['apply_fn', 'smooth', '']
# set usage info:
function_operators_usage['smooth'] = """
    description:
        smooths peaks into Gaussian's
        smooth[dx] a|x: 3> => a/4 |x: 3 - dx> + a/2 |x: 3> + a/4 |x: 3 + dx>
        usually invoked in form: smooth[dx]^power
        also used to enable similarity between nearby integers

    examples:
        smooth[0.5] |age: 30>
            0.25|age: 29.5> + 0.5|age: 30> + 0.25|age: 30.5>
        
        smooth[1]^5 |age: 40>
            0.001|age: 35> + 0.01|age: 36> + 0.044|age: 37> + 0.117|age: 38> + 0.205|age: 39> + 0.246|age: 40> + 0.205|age: 41> + 0.117|age: 42> + 0.044|age: 43> + 0.01|age: 44> + 0.001|age: 45>
        
        rescale[1] smooth[1]^5 |age: 40>
            0.004|age: 35> + 0.04|age: 36> + 0.179|age: 37> + 0.476|age: 38> + 0.833|age: 39> + |age: 40> + 0.833|age: 41> + 0.476|age: 42> + 0.179|age: 43> + 0.04|age: 44> + 0.004|age: 45>

        age-simm (*,*) #=> aligned-simm(smooth[1]^5 |_self1>, smooth[1]^5 |_self2>)
        age-simm(|age: 36>, |age: 40>)
            0.227|simm>

    see also:
        rescale
"""
def smooth(one, dx):
    one = one.to_sp()
    coeff = one.value
    label, value = extract_category_value(one.label)
    if len(label) > 0:
        label += ": "
    try:
        dx = float(dx)
        x = float(value)
    except:
        #    return ket(one.label,one.value)    # possible alternative
        return ket("", 0)
    #  return ket(label + str(x - dx),coeff/4) + ket(label + str(x),coeff/2) + ket(label + str(x + dx),coeff/4)
    # hrmm... in float world, not guaranteed to work as expected ....
    return ket(label + float_to_int(x - dx), coeff / 4) + ket(label + float_to_int(x), coeff / 2) + ket(label + float_to_int(x + dx), coeff / 4)

