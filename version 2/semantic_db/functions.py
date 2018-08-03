#!/usr/bin/env python

#######################################################################
# the semantic-db function-operator file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 31/7/2018
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
import os
from semantic_db.code import *
from semantic_db.sigmoids import *
import math
from math import factorial
from pprint import pprint
import numpy as np
from matplotlib import pyplot as plt
import datetime
from time import gmtime, strftime, ctime, sleep
import hashlib
import zlib
import itertools


# define our dictionaries:

# operators are of form: foo S, or foo[op1, ... , opn] S
# where S is either a ket, superposition or sequence
# operators of form: op ket:
fn_table = {}

# operators of form: op ket, but require context too:
ket_context_table = {}

# operators of form: op sp:
sp_fn_table = {}

# operators of form: op sp, but require context too:
sp_context_table = {}

# operators of form: op seq:
seq_fn_table = {}

# operators that require parameters:
# ie, foo[op1, ... , opn] S:
compound_table = {}


# sequence functions are of form: fn(input-seq, seq, seq, ... , seq) or fn(input-seq, context, seq, ... , seq)
# functions of form: fn(input-seq, seq):
whitelist_table_1 = {}

# functions of form: fn(input-seq, seq, seq):
whitelist_table_2 = {}

# functions of form: fn(input-seq, seq, seq, seq):
whitelist_table_3 = {}

# functions of form: fn(input-seq, seq, seq, seq, seq):
whitelist_table_4 = {}

# functions of form: fn(input-seq, context, seq, seq):
context_whitelist_table_2 = {}

# functions of form: fn(input-seq, context, seq, seq, seq):
context_whitelist_table_3 = {}


# define our usage dictionaries:
function_operators_usage = {}
sequence_functions_usage = {}



# mainly used in the parser code:
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


# function to pretty print seconds
# from here: http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
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


# set invoke method:
fn_table['display-time'] = 'pretty_display_time'
# set usage info:
function_operators_usage['display-time'] = """
    description:
        convert seconds to weeks/days/hours/minutes/seconds/milliseconds

    examples:
        display-time |3.1415>
            |3 seconds, 141 milliseconds>
        
        display-time |1234567890>
            |2041 weeks, 1 day, 23 hours, 31 minutes, 30 seconds>

        ssplit[", "] display-time |1234567890>
            |2041 weeks> . |1 day> . |23 hours> . |31 minutes> . |30 seconds>

    see also:
    
"""
def pretty_display_time(seconds):
    s = display_time(float(seconds.label))
    return ket(s)


# set invoke method:
sp_fn_table['ssplit'] = 'ssplit'
compound_table['ssplit'] = ['apply_sp_fn', 'ssplit', '']  # maybe it should be an apply_fn?
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
    
    see also:
        split, smerge
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
sp_fn_table['split'] = 'split_ket'
compound_table['split'] = ['apply_sp_fn', 'split_ket', '']
# set usage info:
function_operators_usage['split'] = """
    description:
        split |x> converts a ket to a superposition, splitting on the ' ' char.
        split[str] |x> converts a ket to a superposition, splitting on str.

    examples:
        split |a b c d e>
            |a> + |b> + |c> + |d> + |e>
        
        split[""] |abcdef>
            |a> + |b> + |c> + |d> + |e> + |f>
        
        split["d"] |abcdef>
            |abc> + |ef>
        
        split["g"] split["d"] |abcdefghij>
            |abc> + |ef> + |hij>

    see also:
        ssplit
"""
def split_ket(one, s1 = None):  # TODO: improve this code!
    if s1 == "":
        r = superposition()
        for key, value in one.items():
            for label in list(key):
                r.add(label, value)
        return r

    if s1 is None:
        s1 = " "
    r = superposition()
    for key, value in one.items():
        for label in key.split(s1):
            r.add(label, value)
    return r



# set invoke method:
seq_fn_table['smerge'] = 'smerge'
compound_table['smerge'] = ['apply_seq_fn', 'smerge', '']
# set usage info:
function_operators_usage['smerge'] = """
    description:
        smerge merges a sequence into a single ket
        smerge["str"] merges a sequence into a single ket, separated by the str string
      
    examples:
        smerge (|F> . |r> . |e> . |d>)
            |Fred>
      
        smerge[", "] (|a> . |b> . |c> . |d>)
            |a, b, c, d>
      
        -- NB: the dot in there
        -- ie, this is a sequence of two superpositions
        smerge[", "] (|a> + |b> + |c> . |d> + |e>)
            |a, b, c, d, e>

        smerge["\n"] (|b> . |c> . |> . |d>)
            |b
            c
            
            d>
       
    see also:
        ssplit
        
"""
# one is a sequence
def smerge(one, merge_char=''):
    # print('merge_char: %s' % merge_char)
    if merge_char == '\\n':  # not sure why it doesn't work without this. It used to work fine.
        merge_char = '\n'
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
compound_table['insert-string'] = ['apply_sp_fn', 'insert', '']
# set usage info:
function_operators_usage['insert-string'] = """
    description:
        insert string into ket at {1}, {2], etc
        probably deprecated by string-replace
         
    examples:
        insert-string["Fred"] |hey {1}!>
            |hey Fred!>
        
        insert-string["Fred", "Sam"] |Hello {1} and {2}.>
            |Hello Fred and Sam.>

    see also:
        string-replace
"""
def insert(one, *pieces):
    seq = sequence([])
    if type(one) in [ket, superposition]:
        for key, value in one.items():
            text = key.format('', *pieces)
            seq += ket(text, value)
    return seq


# set invoke method:
fn_table['to-upper'] = 'to_all_upper'
compound_table['to-upper'] = ['apply_sp_fn', 'to_upper', '']
# set usage info:
function_operators_usage['to-upper'] = """
    description:
        to-upper |x>
        set all characters to upper case 
        
        to-upper[i1, i2, ... , in] |x>
        change i'th characters to upper case
         
    examples:
        to-upper |fred>
            |FRED>
        
        to-upper[1] |fred>
            |Fred>
      
        to-upper[1,3,5] |abcdefg>
            |AbCdEfg>
    
    see also:
        to-lower
"""
def to_upper(one, *positions):
    try:
        positions = [int(x) - 1 for x in positions]  # maybe change the invoke pattern later, so don't need to split on ',' everywhere!
    except:
        return one
    r = superposition()
    if type(one) in [ket, superposition]:  # do we need this type check here?
        for key, value in one.items():
            text = "".join(key[i].upper() if i in positions else key[i] for i in range(len(key)))
            r.add(text, value)
    return r

def to_all_upper(one):
    r = superposition()
    if type(one) in [ket, superposition]:  # do we need this type check here?
        for key, value in one.items():
            r.add(key.upper(), value)
    return r


# set invoke method:
fn_table['to-lower'] = 'to_all_lower'
compound_table['to-lower'] = ['apply_sp_fn', 'to_lower', '']
# set usage info:
function_operators_usage['to-lower'] = """
    description:
        to-lower |x>
        set all characters to lower case 

        to-lower[i1, i2, ... , in] |x>
        change i'th characters to lower case

    examples:
        to-lower |FRED>
            |fred>

        to-lower[1] |Fred>
            |fred>

        to-lower[1,3,5] |ABCDEFG>
            |aBcDeFG>
            
    see also:
        to-upper            
"""
def to_lower(one, *positions):
    try:
        positions = [int(x) - 1 for x in
                     positions]  # maybe change the invoke pattern later, so don't need to split on ',' everywhere!
    except:
        return one
    r = superposition()
    if type(one) in [ket, superposition]:  # do we need this type check here?
        for key, value in one.items():
            text = "".join(key[i].lower() if i in positions else key[i] for i in range(len(key)))
            r.add(text, value)
    return r


def to_all_lower(one):
    r = superposition()
    if type(one) in [ket, superposition]:  # do we need this type check here?
        for key, value in one.items():
            r.add(key.lower(), value)
    return r



# set invoke method:
compound_table['remove-prefix'] = ['apply_fn', 'remove_prefix', '']
# set usage info:
function_operators_usage['remove-prefix'] = """
    description:
        remove-prefix["str"] |x>
        remove prefix "str" from the ket |x>, if it exists
        
        remove-prefix[n] |x>
        remove first n chars from |x>
            
    examples:
        -- remove prefix "not " if it exists:
        remove-prefix["not "] |not sitting at the beach>
            |sitting at the beach>
            
        -- do nothing if it doesn't have the right prefix:
        remove-prefix["xyz"] |abcdefg>
            |abcdefg>
    
        remove-prefix["word: "] |word: fish>
            |fish>
        
        -- if prefix is an int, then remove n chars:
        remove-prefix[3] |abcdefg>
            |defg>
    
    see also:
        remove-suffix   
"""
def remove_prefix(one, prefix):
    if type(one) is ket:
        if type(prefix) is str:
            if one.label.startswith(prefix):
                return ket(one.label[len(prefix):], one.value)
        if type(prefix) is int:
            return ket(one.label[prefix:], one.value)
    return one


# set invoke method:
compound_table['has-prefix'] = ['apply_fn', 'has_prefix', '']
# set usage info:
function_operators_usage['has-prefix'] = """
    description:
        has-prefix["str"] |x>
        asks if the ket has the given prefix
      
    examples:
        has-prefix["not "] |not sitting at the beach>
            |yes>
        
        has-prefix["not "] |sitting at the beach>
            |no>
    
    see also:
        has-suffix
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
        remove-suffix["str"] |x>
        remove suffix "str" from the ket |x>, if it exists
        
        remove-suffxi[n] |x>
        remove last n chars from |x>

    examples:
        remove-suffix[" sentence."] |This is a sentence.>
            |This is a>
        
        remove-suffix[3] |uvwxyz>
            |uvw>
    
    see also:
        remove-prefix
"""
def remove_suffix(one, suffix):
    if type(one) is ket:
        if type(suffix) is str:
            if one.label.endswith(suffix):
                return ket(one.label[:-len(suffix)], one.value)
        if type(suffix) is int:
            return ket(one.label[:-suffix], one.value)
    return one


# set invoke method:
compound_table['has-suffix'] = ['apply_fn', 'has_suffix', '']
# set usage info:
function_operators_usage['has-suffix'] = """
    description:
        has-suffix["str"] |x>
        asks if the ket has the given suffix

    examples:
        has-suffix["day"] |Tuesday>
            |yes>
            
    see also:
        has-prefix
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
        learn(sp, sp, seq)
        wrapper around a learn rule, so we can use it in operators
      
    examples:
        learn(|op: age>, |Fred>, |37>)
        implements: age |Fred> => |37>
    
    see also:
        add-learn, apply
"""
def learn_sp(input_seq, context, one, two, three):
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
        add-learn(sp, sp, seq)
        wrapper around an add-learn rule, so we can use it in operators
      
    examples:
        add-learn(|op: friends>, |Fred>, |Sam>)
        implements: friends |Fred> +=> |Sam>

    see also:
        learn, apply
"""
def add_learn_sp(input_seq, context, one, two, three):
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
        apply(seq, seq)
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
        
    see also:
        learn, add-learn
"""
def apply_sp(input_seq, context, one, two):
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
compound_table['such-that'] = ['apply_seq_fn', 'seq_such_that', 'context']
# set usage info:
function_operators_usage['such-that'] = """
    description:
        such-that[op1, op2, ... , opn] seq 
        filters the given sequence to elements that return true for "op |element>"
        where the coeff of |true> must be >= 0.5     
        
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
        
        -- filter our input sp to days:
        such-that[is-a-day] (|Monday> + |Tuesday> + |blah> + |Wednesday> + |Thursday> + |Friday> + |Saturday> + |foo> + |Sunday>)
            |Monday> + |Tuesday> + |Wednesday> + |Thursday> + |Friday> + |Saturday> + |Sunday>
    
    see also:

    TODO:
        fix quirk so we don't need literal operator wrappers around function operators.
        eg: is-prime |*> #=> is-prime |_self>
"""
def seq_such_that(one, context, *ops):
    def valid_ket(one, context, ops):
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
            if valid_ket(x, context, ops):
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
compound_table['table'] = ['apply_sp_fn', 'pretty_print_table', 'context']
# set usage info:
function_operators_usage['table'] = """
    description:
        table[op1, op2, ... , opn] sp
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

        load temperature-conversion.sw
        F |*> #=> to-F |_self>
        K |*> #=> to-K |_self>
        table[C, F, K] range(|C: 0>, |C: 100>, |5>)
            +-----+-------+--------+
            | C   | F     | K      |
            +-----+-------+--------+
            | 0   | 32.0  | 273.15 |
            | 5   | 41.0  | 278.15 |
            | 10  | 50.0  | 283.15 |
            | 15  | 59.0  | 288.15 |
            | 20  | 68.0  | 293.15 |
            | 25  | 77.0  | 298.15 |
            | 30  | 86.0  | 303.15 |
            | 35  | 95.0  | 308.15 |
            | 40  | 104.0 | 313.15 |
            | 45  | 113.0 | 318.15 |
            | 50  | 122.0 | 323.15 |
            | 55  | 131.0 | 328.15 |
            | 60  | 140.0 | 333.15 |
            | 65  | 149.0 | 338.15 |
            | 70  | 158.0 | 343.15 |
            | 75  | 167.0 | 348.15 |
            | 80  | 176.0 | 353.15 |
            | 85  | 185.0 | 358.15 |
            | 90  | 194.0 | 363.15 |
            | 95  | 203.0 | 368.15 |
            | 100 | 212.0 | 373.15 |
            +-----+-------+--------+
       
    see also:
        such-that, sort-by
      
    TODO:
        implement transpose table. eg, bots.sw would be simpler.
        implement a sequence version, probably called stable
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



# set invoke method:
sp_fn_table['plot'] = 'plot'
# set usage info:
function_operators_usage['plot'] = """
    description:
        plot sp
        plot a superposition as a bar chart using matplotlib
    
    examples:
        plot (|Fred> + 2|Sam>)
        plot rank split |a b c d e f>
        plot shuffle rank split |a b c d e f>
    
    see also:
        bar-chart
    
    TODO:
        improve the placement of the columns
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
        consume-reaction(sp, sp, sp)
        process a chemical reaction that consumes the reactants
        eg: 2 H_2 + O_2 -> 2 H_2 0
        is represented by: 
            consume-reaction(input-sp, 2|H2> + |O2>, 2|H2O>)
        which is equivalent to:
            input-sp - (2|H2> + |O2>) + 2|H2O>
      
        if input-sp doesn't contain the necessary reactants, then it is returned unchanged
        
        an alternate definition:
        consume-reaction (*,*,*) #=> if(is-subset(|_self2>, |_self1>), |_self1> - |_self2> + |_self3>, |_self1>)
      
    examples:
        -- learn some knowledge:
        current |state> => words-to-list |can opener, closed can and hungry>
        learn-state (*) #=> learn(|op: current>, |state>, |_self>)
        use |can opener> #=> learn-state consume-reaction(current |state>, |can opener> + |closed can>, |can opener> + |open can>)
        eat-from |can> #=> learn-state consume-reaction(current |state>, |open can> + |hungry>, |empty can> + |not hungry>)
      
        -- what is our starting state?
        current |state>
            |can opener> + |closed can> + |hungry>
      
        -- what is the state after using the can-opener?
        use |can opener>
            |can opener> + |hungry> + |open can>
      
        -- what is the state after we eat-from the can?
        eat-from |can>
            |can opener> + |empty can> + |not hungry>

    
        -- next, see: shopping.sw
        -- learn the prices for some items:
        the-price-for |apple> => 0.6|dollar>
        the-price-for |orange> => 0.8|dollar>
        the-price-for |milk> => 2.3|dollar>
        the-price-for |coffee> => 5.5|dollar>
        the-price-for |steak> => 9|dollar>
        
        -- learn our shopping list:
        the |shopping list> => |orange> + 4|apple> + |milk> + |coffee> + |steak>
        
        -- check if we know the price for an item:       
        price-is-defined |*> #=> do-you-know the-price-for |_self>
        
        -- filter our shopping list down to available items:
        the-list-of |available items> #=> such-that[price-is-defined] the |shopping list>
        
        -- define our buy operator:
        buy (*,*) #=> consume-reaction( |_self2>, the-price-for |_self1>, |_self1>)
        
        -- ask, what are the available items?
        the-list-of |available items>
            |orange> + 4|apple> + |milk> + |coffee> + |steak>
        
        -- now ask, what is the price for the available items?
        the-price-for the-list-of |available items>
            20|dollar>
                    
        -- now go shopping with $30:
        buy(the-list-of |available items>, 30 |dollar>)
            10|dollar> + |orange> + 4|apple> + |milk> + |coffee> + |steak>
            
        -- convert superposition result to English:
        plural |*> #=> |_self> _ |s>
        list-to-words int-coeffs-to-word buy(the-list-of |available items>, 30 |dollar>)
            |10 dollars, 1 orange, 4 apples, 1 milk, 1 coffee and 1 steak>

    see also:
        catalytic-reaction, eat-from-can, fission-uranium
"""
# one, two and three are superpositions
def process_reaction(input_seq, one, two, three):
    one = one.to_sp()
    two = two.to_sp()
    three = three.to_sp()

    def del_fn(x, y):  # NB: creates negative coeffs.
        return x - y

    if intersection(two, one).count_sum() != two.count_sum():
        return one
    else:
        return intersection_fn(del_fn, one, two).drop() + three  # can we do superposition subtraction? Maybe implement it?? Meaning: one - two + three


# set invoke method:
whitelist_table_3['catalytic-reaction'] = 'process_catalytic_reaction'
# set usage info:
sequence_functions_usage['catalytic-reaction'] = """
    description:
        catalytic-reaction(sp, sp, sp)
        process a catalyzed reaction (that doesn't consume the reactants) 
        if the necessary reactants are not present, then the state is left unchanged.
      
        catalytic-reaction(input-sp, |a> + |b>, |c> +|d>)
        is equivalent to:
            input-sp + |c> + |d>
        provided |a> + |b> is in input-sp
        else, return input-sp

        an alternate definition:
        catalytic-reaction (*,*,*) #=> if(is-subset(|_self2>, |_self1>), |_self1> + |_self3>, |_self1>)

    examples:
        
    
    see also:
        consume-reaction
"""
# 16/2/2016:
# process-catalytic-reaction(current-sp,|a> + |b>,|c> +|d>) = current-sp + |c> + |d> if |a> + |b> is in current-sp
# What if |c> + |d> is already in current-sp? Do you add it again?
#
# I suspect process-catalytic-reaction() can be used to encode maths proofs.
# One is the current state of knowledge.
# Two is the necessary conditions for the proof to be true.
# Three is the implications of that proof.
# Another example is simple physics problems.
# You write down what you know, and any possibly relevant equations.
# Then try to figure out a pathway to the desired result.
#
def process_catalytic_reaction(input_seq, one, two, three):
    one = one.to_sp()
    two = two.to_sp()
    three = three.to_sp()

    if intersection(two, one).count_sum() != two.count_sum():
        return one
    else:
        return one + three


# x,y are floats
def filter_fn(x, y):
    if x == 0:
        return 0
    return y

# filter-down-to(|b> + 3|c>, |a> + 5|b> + 0.7|c> + 9|d> + 3.2|e>) == 5|b> + 0.7|c>
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



# set invoke method:
fn_table['apply-value'] = 'apply_value'
# set usage info:
function_operators_usage['apply-value'] = """
    description:
        apply-value |x>
        apply value to the given ket
        return the ket if the value is not convertible to float
            
    examples:
        -- not convertible to float, so return input ket:
        apply-value |price: fish>
            |price: fish>
        
        -- is convertible to float:
        apply-value |price: 37>
            37|price: 37>
            
    see also:
    
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
        extract-category |x>
        extract the category from the given ket
            
    examples:
        -- if there is no category, then return unchanged:
        extract-category |fish>
            |fish>
        
        extract-category |animal: mammal: dog>
            |animal: mammal>
        
        extract-category |a: b: c: d: e: f>
            |a: b: c: d: e>
        
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
        extract-value |x>
        extract the value, ie remove the category, from the given ket
            
    examples:
        -- if there is no category, then return unchanged:
        extract-value |fish>
            |fish>
        
        extract-value |animal: mammal: dog>
            |dog>
        
        extract-value |a: b: c: d: e: f>
            |f>
        
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
        remove-leading-category |x>
        remove the leading category
            
    examples:
        -- if there is no category, then return unchanged:
        remove-leading-category |fish>
            |fish>
        
        remove-leading-category |animal: mammal: dog>
            |mammal: dog>
            
        remove-leading-category |a: b: c: d: e: f>
            |b: c: d: e: f>
        
    see also:
        find-leading-category, extract-category, extract-value    
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
        find-leading-category |x>
        find the leading category
            
    examples:
        -- if there is no category, then return unchanged:
        find-leading-category |fish>
            |fish>
        
        find-leading-category |animal: mammal: dog>
            |animal>
            
        find-leading-category |a: b: c: d: e: f>
            |a>
        
    see also:
        remove-leading-category, extract-category, extract-value  
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
        to-value |x>
        if the value is a float, remove from the ket, and apply it to the coefficient
        otherwise, return the ket unchanged
            
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
        to-category, push-float, pop-float
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
        to-category |x>
        append the coefficient of the ket, to the ket label
            
    examples:
        to-category 57| >
            |57>
      
        to-category |age>
            |age: 1>
        
        to-category 23|age>
            |age: 23>
        
    see also:
        to-value, push-float, pop-float
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
        arithmetic(ket, ket, ket)
        the arithmetic function
        supported operators: + - * / % ^
        if the categories are different, return |>
      
    examples:
        arithmetic(|number: 3>, |symbol: +>, |number: 8>)
            |number: 11>
        
        arithmetic(|3>, |^>, |4>)
            |81>
      
        -- the categories are not the same, so return |>
        arithmetic(|price: 37>, |->, |number: 5.20>)
            |>
        
        -- one way to make sure the categories are the same:
        number-to-price |number: *> #=> |price:> __ extract-value |_self>
        arithmetic(|price: 37>, |->, number-to-price |number: 5.20>)
            |price: 31.8>
      
        -- simple Fibonacci and factorial:
        fib |0> => |0>
        fib |1> => |1>
        n-1 |*> #=> arithmetic(|_self>, |->, |1>)
        n-2 |*> #=> arithmetic(|_self>, |->, |2>)
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

    see also:
        algebra, worked example Fibonacci-and-factorial
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
def arithmetic(input_seq, x, operator, y):
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
        range(sp, sp)
        range(sp, sp, ket)
        the range function
            
    examples:
        -- range between 1 and 10:
        range(|1>, |10>)
            |1> + |2> + |3> + |4> + |5> + |6> + |7> + |8> + |9> + |10>
      
        -- range between 1 and 5, using step of 0.5:
        range(|1>, |5>, |0.5>)
            |1> + |1.5> + |2> + |2.5> + |3> + |3.5> + |4> + |4.5> + |5>
        
        -- specify a category, in this case 'year':
        range(|year: 1981>, |year: 1985>)
            |year: 1981> + |year: 1982> + |year: 1983> + |year: 1984> + |year: 1985>
            
        -- specify the 'number' category:
        range(|number: 7>, |number: 13>)
            |number: 7> + |number: 8> + |number: 9> + |number: 10> + |number: 11> + |number: 12> + |number: 13>
        
        -- if the categories are not the same, return the don't know ket |>
        range(|number: 3>, |price: 7>)
            |>
        
        -- reverse-range, with step size 2, from 2018 to 2014:
        range(|year: 2018>, |year: 2014>, - |year: 2>)
            |year: 2018> + |year: 2016> + |year: 2014>
            
        -- if you need a sequence instead of a superposition, use sp2seq:
        sp2seq range(|number: 17>, |number: 23>)
            |number: 17> . |number: 18> . |number: 19> . |number: 20> . |number: 21> . |number: 22> . |number: 23>
        
        -- alternatively, you can define the srange function:
        srange (*,*) #=> sp2seq range(|_self1>, |_self2>)
        srange (*,*,*) #=> sp2seq range(|_self1>, |_self2>, |_self3>)
        
        srange(|5>, |9>)
            |5> . |6> . |7> . |8> . |9>
        
        srange(|17>, |23>, |2>)
            |17> . |19> . |21> . |23>
        
        -- filter down to prime numbers:
        -- due to a quirk, which we might change later, you need a literal operator wrapper around a function operator:
        is-prime |*> #=> is-prime |_self>
        
        -- now find our primes:
        such-that[is-prime] range(|2>, |40>)
            |2> + |3> + |5> + |7> + |11> + |13> + |17> + |19> + |23> + |29> + |31> + |37> 
        
    see also:
        sp2seq
"""
def show_range(input_seq, start, finish, step=ket("1")):
    start = start.to_sp() # we don't know how to handle range for sequences, so for now, cast them all to superpositions
    finish = finish.to_sp()
    step = step.to_sp()  # if step is a superposition, cast it to a ket

    if step.value < 0:
        return show_range(finish, start, ket(step.label)).reverse()

    start_label = start if type(start) == str else start.label
    finish_label = finish if type(finish) == str else finish.label
    step_label = step if type(step) == str else step.label

    cat1, v1 = extract_category_value(start_label)
    cat2, v2 = extract_category_value(finish_label)
    cat3, v3 = extract_category_value(step_label)

    if cat1 != cat2:  # do we want to check if cat3 == cat1/2 too?
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
whitelist_table_2['intersection'] = 'intersection_input'
whitelist_table_3['intersection'] = 'tri_intersection_input'
# set usage info:
sequence_functions_usage['intersection'] = """
    description:
        intersection(seq, seq)
        intersection(seq, seq, seq)
        the intersection function
        takes element-wise min of the coefficients
            
    examples:
        intersection(|a>, |b>, |c>)
            |>
        
        intersection(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)      
            3|a> + 0.9|b>

        intersection(|a1> + |a2> . 0.3|b1> + 0.5|b2>, 3|a1> + 0.9|a2> . 0.7|b2>)
            |a1> + 0.9|a2> . 0.5|b2>
        
    see also:
      union, complement, subset, mbr
"""
def intersection(one, two):
    return intersection_fn(min, one, two).drop()

# the triple intersection:
def tri_intersection(one, two, three):
    return intersection(intersection(one, two), three)

def intersection_input(input_seq, one, two):
    return intersection_fn(min, one, two).drop()

# the triple intersection:
def tri_intersection_input(input_seq, one, two, three):
    return intersection(intersection(one, two), three)


# now the union:
# set invoke method:
whitelist_table_2['union'] = 'union_input'
whitelist_table_3['union'] = 'tri_union_input'
# set usage info:
sequence_functions_usage['union'] = """
    description:
        union(seq, seq)
        union(seq, seq, seq)
        the union function
        takes element-wise max of the coefficients
            
    examples:
        union(|a>, |b>, |c>)
            |a> + |b> + |c>
        
        union(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)
            3.5|a> + 1.2|b> + 5.13|c>

        union(|a1> + |a2> . 0.3|b1> + 0.5|b2>, 3|a1> + 0.9|a2> . 0.7|b2>)
            3|a1> + |a2> . 0.3|b1> + 0.7|b2>

    see also:
        intersection, complement, subset, mbr
"""
def union(one, two):
    return intersection_fn(max, one, two)

# the triple union:
def tri_union(one, two, three):
    return union(union(one, two), three)

def union_input(input_seq, one, two):
    return intersection_fn(max, one, two)

# the triple union:
def tri_union_input(input_seq, one, two, three):
    return union(union(one, two), three)


# potentially we could write a wrapper that maps associative pair functions into triple, quad etc fns.
# eg: assoc_wrapper(fn,pieces)
# where pieces is the list of parameters to feed to "fn"
#



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
whitelist_table_2['complement'] = 'complement_input'
# set usage info:
sequence_functions_usage['complement'] = """
    description:
        complement(seq, seq)
        the complement function
            
    examples:

    see also:
        intersection, union,  
"""
def complement(one, two):
    return intersection_fn(comp_fn, one, two)

def complement_input(input_seq, one, two):
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
whitelist_table_2['multiply'] = 'multiply_input'
# set usage info:
sequence_functions_usage['multiply'] = """
    description:
        multiply(seq, seq)
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

def multiply_input(input_seq, one, two):
    return intersection_fn(mult_fn, one, two)


def sum_fn(x, y):
    return x + y


# set invoke method:
whitelist_table_2['addition'] = 'addition_input'
# set usage info:
sequence_functions_usage['addition'] = """
    description:
        addition(seq, seq)
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

def addition_input(input_seq, one, two):
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
        distance(ket, ket)
        the Euclidean distance function
        
    the algorithm:
        r = sqrt((x1 - y1)^2 + (x2 - y2)^2 + ... + (xn - yn)^2 )
        
    examples:
        -- without categories:
        distance(|0: 0>, |0: 7>)
            |number: 7>
            
        -- using categories, and a Pythagorean triple:
        distance(|grid: 0: 0>, |grid: 3: 4>)
            |number: 5>
        
        -- if categories are different, return don't know ket:
        distance(|grid: 0: 0>, |position: 3: 4>)
            |>

        -- another Pythagorean triple:
        distance(|grid: 0: 0>, |grid: 5: 12>)
            |number: 13>
        
        -- sqrt(2):
        distance(|0: 0>, |1: 1>)
            |number: 1.414>
        
        distance(|0: 0>, |1: 2>)
            |number: 2.236>        
           
    see also:
        simm 

    future:
        maybe change the number of decimal points in the result, currently set to 3
        maybe remove the number prefix too?
"""
def first_Euclidean_distance(one, two):
    one = one.to_sp()
    two = two.to_sp()

    return ket("number: " + float_to_int(math.sqrt(intersection_fn(squared_difference, one, two).count_sum())))

def Euclidean_distance(input_seq, one, two):
    one = one.to_sp().label.split(': ')[::-1]
    two = two.to_sp().label.split(': ')[::-1]
    if len(one) != len(two):
        return ket()

    # print('one:', one)
    # print('two:', two)

    x_values = []
    for x in one:
        if x.isdigit():
            x_values.append(float(x))
        else:
            break
    y_values = []
    for x in two:
        if x.isdigit():
            y_values.append(float(x))
        else:
            break

    # print('x-values:', x_values)
    # print('y-values:', y_values)

    if len(x_values) != len(y_values) or len(x_values) == 0:
        return ket()

    category_one = one[len(x_values):]
    category_two = two[len(y_values):]

    # print('category_one:', category_one)
    # print('category_two:', category_two)

    if category_one != category_two:
        return ket()

    r = sum((x_values[k] - y_values[k])**2 for k in range(len(x_values)))
    value = float_to_int(math.sqrt(r))
    return ket('number: ' + value)


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
whitelist_table_2['simm'] = 'aligned_simm'
# set usage info:
sequence_functions_usage['simm'] = """
    description:
        simm(seq, seq)
        the aligned sequences version of our similarity measure
        for each superposition in our sequences, calculate the similarity measure
        (ie, 0 for completely distinct, 1 for exactly the same, values in between otherwise)
        then average them
            
    examples:
        simm(|a>, |b>)
            0|simm>
        
        simm(3|a> + 1.2|b>, 3.5|a> + 0.9|b> + 5.13|c>)
            0.462|simm>        

        simm(|a1> + |a2> . 0.3|b1> + 0.5|b2>, 3|a1> + 0.9|a2> . 0.7|b2>)
            0.678|simm>        

        rename-simm |simm> => |result>
        push-float rename-simm simm(|a>, split |a b c d>)
            |result: 0.25>
            
    see also: 
"""
def aligned_simm(input_seq, one, two):
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
        predict[op] seq
        predict[op, n] seq
        given an input sequence, predict what is next
        optionally, specify the max sequence length you want returned
            
    examples:
        -- learn some short simple sequences:
        seq |count> => |1> . |2> . |3> . |4> . |5> . |6> . |7> . |8> . |9> . |10>
        seq |fib> => |1> . |1> . |2> . |3> . |5> . |8> . |13>
        seq |fact> => |1> . |2> . |6> . |24> . |120>
        seq |primes> => |2> . |3> . |5> . |7> . |11> . |13> . |17> . |19> . |23>
        
        -- given the sequence 2 . 5 predict the sequences:
        predict[seq] (|2> . |5>)
            1.0     count   |6> . |7> . |8> . |9> . |10>
            1.0     fib     |8> . |13>
            1.0     primes  |7> . |11> . |13> . |17> . |19> . |23>
            |count: 6 . 7 . 8 . 9 . 10> + |fib: 8 . 13> + |primes: 7 . 11 . 13 . 17 . 19 . 23>

        -- again, given the sequence 2 . 5 predict the next 3 elements:
        predict[seq, 3] (|2> . |5>)
            1.0     count   |6> . |7> . |8>
            1.0     fib     |8> . |13>
            1.0     primes  |7> . |11> . |13>
            |count: 6 . 7 . 8> + |fib: 8 . 13> + |primes: 7 . 11 . 13>
       
        -- use extract-category to predict the names of the sequences:
        extract-category predict[seq] (|2> . |5> . |7>)
            1.0     count   |8> . |9> . |10>
            1.0     primes  |11> . |13> . |17> . |19> . |23>
            |count> + |primes>

        -- use extract-value to predict just the sequences, with the names removed:
        extract-value predict[seq] (|2> . |5> . |7>)
            1.0     count   |8> . |9> . |10>
            1.0     primes  |11> . |13> . |17> . |19> . |23>
            |8 . 9 . 10> + |11 . 13 . 17 . 19 . 23>
       
        -- given the sequence 2 . 5 . 7 predict the next most likely value:
        extract-value predict[seq, 1] (|2> . |5> . |7>)
            1.0     count   |8>
            1.0     primes  |11>
            |8> + |11>


        -- learn some simple sentences:
        sentence |dog 1> => ssplit[" "] |the dog wants food>
        sentence |dog 2> => ssplit[" "] |the dog chased the ball>
        sentence |cat 1> => ssplit[" "] |a cat sat on the mat>
        
        -- given a word, predict what word follows:
        extract-value predict[sentence, 1] |the>
            1.0     dog 1   |dog>
            1.0     dog 2   |dog>
            1.0     dog 2   |ball>
            1.0     cat 1   |mat>
            2|dog> + |ball> + |mat>

        extract-value predict[sentence, 1] |a>
            1.0     cat 1   |cat>
            |cat>

        extract-value predict[sentence] ssplit[" "] |the dog>
            1.0     dog 1   |wants> . |food>
            1.0     dog 2   |chased> . |the> . |ball>
            |wants . food> + |chased . the . ball>

    see also: 
"""
def predict_next(one, context, *params):
    op = params[0]
    if len(params) == 1:
        count = False
    else:
        try:
            count = int(params[1])
        except:
            return ket()

    assert(type(one) == sequence)

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
        # seq = context.recall(op, elt, True)
        seq = elt.apply_op(context, op)
        sequences.append([1, elt.label, seq])

    # filter our sequences:
    next_sequences = sequences
    for sp in one:  # assumes one is a sequence
        next_sequences = find_next_sequences(sp, next_sequences)
        # next_sequences = find_next_sequences_v2(sp, next_sequences)  # for now, we don't want this variant.

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
        sp2seq sp
        sp2seq converts superpositions into sequences
      
    examples:
        sp2seq range(|1>, |5>)
            |1> . |2> . |3> . |4> . |5>

    see also:
        seq2sp
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
        seq2sp seq
        seq2sp flattens sequences into superpositions

    examples:
        seq2sp (|a> + 2.2|b> . 3|c> . 0.2|d> + |x> . 7|y> + 9|z>)
            |a> + 2.2|b> + 3|c> + 0.2|d> + |x> + 7|y> + 9|z>
    
    see also:
        sp2seq
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
# set invoke method:
compound_table['greater-than'] = ['apply_fn', 'greater_than', '']
# set usage info:
function_operators_usage['greater-than'] = """
    description:
        greater-than[value] ket
        returns the ket if value > the value in ket
        otherwise, return |>
        ie, a value filter

    examples:
        greater-than[5] |7>
            |7>

        greater-than[3] |price: 3.50>
            |price: 3.50>

        greater-than[26] |number: 25>
            |>

        -- if the ket has no float value, then return |>
        greater-than[13] |the cat>
            |>

    see also:
        greater-equal-than, less-than, less-equal-than, equal, in-range
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
"""
# assumes one is a ket
def greater_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value > t:
        return one
    return ket()


# set invoke method:
compound_table['greater-equal-than'] = ['apply_fn', 'greater_equal_than', '']
# set usage info:
function_operators_usage['greater-equal-than'] = """
    description:
        greater-equal-than[value] ket
        returns the ket if value >= the value in ket
        otherwise, return |>
        ie, a value filter

    examples:
        greater-equal-than[5] |7>
            |7>

        greater-equal-than[3.5] |price: 3.50>
            |price: 3.50>

        greater-equal-than[26] |number: 25>
            |>

        -- if the ket has no float value, then return |>
        greater-equal-than[13] |the cat>
            |>

    see also:
        greater-than, less-than, less-equal-than, equal, in-range
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
"""
def greater_equal_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value >= t:
        return one
    return ket()


# set invoke method:
compound_table['less-than'] = ['apply_fn', 'less_than', '']
# set usage info:
function_operators_usage['less-than'] = """
    description:
        less-than[value] ket
        returns the ket if value < the value in ket
        otherwise, return |>
        ie, a value filter

    examples:
        less-than[5] |7>
            |>

        less-than[3] |price: 3.50>
            |>

        less-than[26] |number: 25>
            |number: 25>

        -- if the ket has no float value, then return |>
        less-than[13] |the cat>
            |>

    see also:
        greater-than, greater-equal-than, less-equal-than, equal, in-range
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
"""
def less_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value < t:
        return one
    return ket()


# set invoke method:
compound_table['less-equal-than'] = ['apply_fn', 'less_equal_than', '']
# set usage info:
function_operators_usage['less-equal-than'] = """
    description:
        less-equal-than[value] ket
        returns the ket if value <= the value in ket
        otherwise, return |>
        ie, a value filter

    examples:
        less-equal-than[5] |7>
            |>

        less-equal-than[3.5] |price: 3.50>
            |price: 3.50>

        less-equal-than[26] |number: 25>
            |number: 25>

        -- if the ket has no float value, then return |>
        less-equal-than[13] |the cat>
            |>

    see also:
        greater-than, greater-equal-than, less-than, equal, in-range
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
"""
def less_equal_than(one, t):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if value <= t:
        return one
    return ket()


# set invoke method:
compound_table['equal'] = ['apply_fn', 'equal', '']
# set usage info:
function_operators_usage['equal'] = """
    description:
        equal[value] ket
        returns the ket if value == the value in ket
        otherwise, return |>
        ie, a value filter

    examples:
        equal[5] |7>
            |>

        equal[3.5] |price: 3.50>
            |price: 3.50>

        equal[26] |number: 25>
            |>

        -- if the ket has no float value, then return |>
        equal[13] |the cat>
            |>

    see also:
        greater-than, greater-equal-than, less-than, less-equal-than, in-range
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
"""
def equal(one, t):  # name clash with equal(SP1,SP2)??
    epsilon = 0.0001  # Need code since equal and float don't work well together.
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if (t - epsilon) <= value <= (t + epsilon):
        return one
    return ket()


# set invoke method:
compound_table['in-range'] = ['apply_fn', 'in_range', '']
# set usage info:
function_operators_usage['in-range'] = """
    description:
        in-range[value1, value2] ket
        returns the ket if value1 <= the value in ket <= value2
        otherwise, return |>
        ie, a value filter

    examples:
        in-range[31, 37] range(|1>, |100>)
            |31> + |32> + |33> + |34> + |35> + |36> + |37>
        
    see also:
        greater-than, greater-equal-than, less-than, less-equal-than, equal
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
"""
def in_range(one, t1, t2):
    try:
        value = float(one.label.rsplit(": ", 1)[-1])
    except:
        return ket()
    if t1 <= value <= t2:
        return one
    return ket()



# set invoke method:
compound_table['is-greater-than'] = ['apply_fn', 'is_greater_than', '']
# set usage info:
function_operators_usage['is-greater-than'] = """
    description:
        is-greater-than[value] ket
        returns yes/no if value > the value in ket
      
    examples:
        is-greater-than[5] |7>
            |yes>
    
        is-greater-than[3] |price: 3.50>
            |yes>
    
        is-greater-than[26] |number: 25>
            |no>
            
        -- if the ket has no float value, then return |>
        is-greater-than[13] |the cat>
            |>
        
    see also:
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
        greater-than, greater-equal-than, less-than, less-equal-than, equal, in-range
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
compound_table['is-greater-equal-than'] = ['apply_fn', 'is_greater_equal_than', '']
# set usage info:
function_operators_usage['is-greater-equal-than'] = """
    description:
        is-greater-equal-than[value] ket
        returns yes/no if value >= the value in ket
      
    examples:
        is-greater-equal-than[13] |number: 13>
            |yes>
        
        is-greater-equal-than[21] |age: 23>
            |yes>
        
        is-greater-equal-than[1980] |year: 1977>
            |no> 

        -- if the ket has no float value, then return |>
        is-greater-equal-than[13] |the cat>
            |>

    see also:
        is-greater-than, is-less-than, is-less-equal-than, is-equal, is-in-range
        greater-than, greater-equal-than, less-than, less-equal-than, equal, in-range
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
compound_table['is-less-than'] = ['apply_fn', 'is_less_than', '']
# set usage info:
function_operators_usage['is-less-than'] = """
    description:
        is-less-than[value] ket
        returns yes/no if value < the value in ket
      
    examples:
        is-less-than[80] |age: 76>
            |yes>
        
        is-less-than[2000] |year: 2018>
            |no>

        -- if the ket has no float value, then return |>
        is-less-than[13] |the cat>
            |>

    see also:
        is-greater-than, is-greater-equal-than, is-less-equal-than, is-equal, is-in-range
        greater-than, greater-equal-than, less-than, less-equal-than, equal, in-range
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
        is-less-equal-than[value] ket
        returns yes/no if value <= the value in ket
      
    examples:
        is-less-equal-than[80] |age: 76>
            |yes>
        
        is-less-equal-than[2010] |year: 2010>
            |yes>

        -- if the ket has no float value, then return |>
        is-less-equal-than[13] |the cat>
            |>

    see also:
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal, is-in-range
        greater-than, greater-equal-than, less-than, less-equal-than, equal, in-range
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
        is-equal[value] ket
        returns yes/no if value == the value in ket
      
    examples:
        is-equal[80] |age: 76>
            |no>
        
        is-equal[2010] |year: 2010>
            |yes>

        -- if the ket has no float value, then return |>
        is-equal[13] |the cat>
            |>

    see also:
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-in-range
        greater-than, greater-equal-than, less-than, less-equal-than, equal, in-range
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
compound_table['is-in-range'] = ['apply_fn', 'is_in_range', '']
# set usage info:
function_operators_usage['is-in-range'] = """
    description:
        is-in-range[value1, value2] ket
        returns yes/no if value1 <= the value in ket <= value2
        
    examples:
        is-a-child |*> #=> is-in-range[0,17] age |_self>
        is-a-teenager |*> #=> is-in-range[13,19] age |_self>
        is-an-adult |*> #=> not is-in-range[0,17] age |_self>

        -- if the ket has no float value, then return |>
        is-in-range[30, 42] |the cat>
            |>

    see also:
        is-greater-than, is-greater-equal-than, is-less-than, is-less-equal-than, is-equal
        greater-than, greater-equal-than, less-than, less-equal-than, equal, in-range
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
        op-zip(seq, seq)
        zip together a sequence of operators and a sequence of objects
        stops at the end of the shorter of the two sequences
            
    examples:
        -- define our for-example operators:
        op1 |*> #=> |op1: > _ |_self>
        op2 |*> #=> |op2: > _ |_self>
        op3 |*> #=> |op3: > _ |_self>
        op4 |*> #=> |op4: > _ |_self>
        
        -- define our sequence of operators:
        op |seq> => |op: op1> . |op: op2> . |op: op3> . |op: op4>
        
        -- define our for-example sequence:
        the |seq> => |a> . |b> . |c> . |d> . |e> . |f>

        -- see the result:
        op-zip(op |seq>, the |seq>)
            |op1: a> . |op2: b> . |op3: c> . |op4: d>
      
    see also:
        n2w in the big-numbers-to-words example
        
    future:
        a version that works for superpositions
"""
# one, two are sequences
def op_zip(input_seq, context, one, two):
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
whitelist_table_4['if'] = 'bko_if_3'
# set usage info:
sequence_functions_usage['if'] = """
    description:
        if(ket, seq, seq)
        if(ket, seq, seq, seq)
        a crude approximation to an if function
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
        wif, remove-leading-category
"""
# 13/4/2014:
# Let's add an if/else statement to BKO.
# Motivated by recursion works without even trying (though vastly inefficient at the moment).
# So seems sensible to add if/else too.
#
# bko_if(|True>,|a>,|b>)  -- returns |a>
# bko_if(|False>,|c>,|d>) -- returns |d>
def bko_if(input_seq, condition, one, two):
    #  print('condition: %s' % condition)
    #  print('one: %s' % one)
    #  print('two: %s' % two)
    if condition.to_sp().label.lower() in ["true", "yes"]:
        return one
    else:
        return two


def bko_if_3(input_seq, condition, one, two, three):
    condition = condition.to_sp().label.lower()
    if condition in ["true", "yes"]:
        return one
    if condition in ["false", "no"]:
        return two
    else:
        return three


# set invoke method:
whitelist_table_3['wif'] = 'weighted_bko_if'
# set usage info:
sequence_functions_usage['wif'] = """
    description:
        wif(ket, sp, sp)
        a weighted if
        works just like standard 'if', but takes into consideration the coefficient of the condition
      
    examples:
        wif(0.7|True>, |a>, |b>)
            0.7|a> + 0.3|b>
        
        wif(0.8|False>, |a>, |b>)
            0.2|a> + 0.8|b> 
        
    future:
        implement a version that works with sequences
      
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
def weighted_bko_if(input_seq, condition, one, two):
    condition = condition.to_sp()
    one = one.to_sp()
    two = two.to_sp()

    label = condition.label
    value = condition.value
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
        round[n] ket
        round the value in the ket to n places, leaving the coefficient unchanged
      
    examples:
        round[3] |3.14159265>
            |3.142>

        round[4] |number: 12.34567890>
            |number: 12.3457>
         
    see also:
        times-by, divide-by, int-divide-by, plus, minus, mod, is-mod, to-comma-number    
"""
def round_numbers(one, t):  # cool, this one seems to work. Now need to do the rest.
    return numbers_fn(round, one, t)


# set invoke method:
fn_table['to-comma-number'] = 'number_to_comma_number'
# set usage info:
function_operators_usage['to-comma-number'] = """
    description:
        to-comma-number ket
        insert thousands commas into numbers 

    examples:
        to-comma-number |8825>
            |8,825>

        to-comma-number |population: 2300000>
            |population: 2,300,000>

        to-comma-number |3759.27>
            |3,759.27>

        to-comma-number |km: 22956.53>
            |km: 22,9356.53>

        -- replace is an approximate inverse for to-comma-number:
        replace[",", ""] to-comma-number |number: 12345678>
            |number: 12345678>

    see also:
        table, round, replace
"""
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


# set invoke method:
# compound_table['times-by'] = ".apply_fn(times_numbers, {0})"
compound_table['times-by'] = ['apply_fn', 'times_numbers', '']
# set usage info:
function_operators_usage['times-by'] = """
    description:
        times-by[n] ket
        times the value in the ket by n, leaving the coefficient unchanged
      
    examples:
        times-by[5] |6.1>
            |30.5>

        times-by[3] 13|number: 3.14159265>
            13|number: 9.424777950000001>
        
    see also:
        round, divide-by, int-divide-by, plus, minus, mod, is-mod
        temperature-conversion.sw    
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
        divide-by[n] ket
        divide the value in the ket by n, leaving the coefficient unchanged
      
    examples:
        divide-by[5] |625.5>
            |125.1>

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
        int-divide-by[n] ket
        integer divide the value in the ket by n, leaving the coefficient unchanged
      
    examples:
        int-divide-by[1000] |123456>
            |123>        

    see also:
        round, times-by, divide-by, plus, minus, mod, is-mod
        big-numbers-to-words.sw    
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
        plus[n] ket
        add n to the value in the ket, leaving the coefficient unchanged
      
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
        minus[n] ket
        subtract n from the value in the ket, leaving the coefficient unchanged
      
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
compound_table['mod'] = ['apply_fn', 'mod_numbers', '']
# set usage info:
function_operators_usage['mod'] = """
    description:
        mod[n] ket
        apply mod n to the value in the ket, leaving the coefficient unchanged
        if the value is not a number, return the ket
      
    examples:
        mod[1000] |1234567>
            |567>

        mod[13] |the cat>
            |the cat>

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
        is-mod[n] ket
        answers yes or no, if the given number is mod n
      
    examples:
        is-mod[3] |96>
            |yes>
        
        is-mod[17] |number: 51>
            |yes>
        
        is-mod[5] |51>
            |no>

        -- if the ket is not a float value, return |no>
        is-mod[7] |the cat>
            |no>

        -- the fizzbuzz exercise:
        fizzbuzz |*> #=> print if-mod-5 if-mod-3 if-mod-15 |_self>

        if-mod-15 |*> #=> if(is-mod[15] |_self>, |FizzBuzz>, |_self>)
        if-mod-3 |*> #=> if(is-mod[3] |_self>, |Fizz>, |_self>)
        if-mod-5 |*> #=> if(is-mod[5] |_self>, |Buzz>, |_self>)

        -- now, find the results:
        fizzbuzz range(|1>, |20>)
            1
            2
            Fizz
            4
            Buzz
            Fizz
            7
            8
            Fizz
            Buzz
            11
            Fizz
            13
            14
            FizzBuzz
            16
            17
            Fizz
            19
            Buzz
            |1> + |2> + 5|Fizz> + |4> + 3|Buzz> + |7> + |8> + |11> + |13> + |14> + |FizzBuzz> + |16> + |17> + |19>
        
        -- or, if you want the sequence version:
        fizzbuzz sp2seq range(|1>, |20>)
            1
            2
            Fizz
            4
            Buzz
            Fizz
            7
            8
            Fizz
            Buzz
            11
            Fizz
            13
            14
            FizzBuzz
            16
            17
            Fizz
            19
            Buzz
            |1> . |2> . |Fizz> . |4> . |Buzz> . |Fizz> . |7> . |8> . |Fizz> . |Buzz> . |11> . |Fizz> . |13> . |14> . |FizzBuzz> . |16> . |17> . |Fizz> . |19> . |Buzz>
       
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
        learn-map[h, w]
        learn-map[h, w, op]
        learn a rectangular map, of height h, and width w
        where all cells are initialized to zero: 
            op |grid: x: y> => |0>
        and we learn all direction operators, N, NE, E, SE, S, SW, W, NW, that don't point outside the map
        the map is closed boundary, rather than torus shape
      
    examples:
        -- show what we learn for a small example map:
        learn-map[2,2]
        dump
            ----------------------------------------
             |context> => |context: global context>
            
            value |grid: 1: 1> => |0>
            E |grid: 1: 1> => |grid: 1: 2>
            SE |grid: 1: 1> => |grid: 2: 2>
            S |grid: 1: 1> => |grid: 2: 1>
            
            value |grid: 1: 2> => |0>
            S |grid: 1: 2> => |grid: 2: 2>
            SW |grid: 1: 2> => |grid: 2: 1>
            W |grid: 1: 2> => |grid: 1: 1>
            
            value |grid: 2: 1> => |0>
            N |grid: 2: 1> => |grid: 1: 1>
            NE |grid: 2: 1> => |grid: 1: 2>
            E |grid: 2: 1> => |grid: 2: 2>
            
            value |grid: 2: 2> => |0>
            N |grid: 2: 2> => |grid: 1: 2>
            W |grid: 2: 2> => |grid: 2: 1>
            NW |grid: 2: 2> => |grid: 1: 1>
            ----------------------------------------

        -- learn a larger map, then find path/steps between grid cells:    
        learn-map[20,20]
        find-path-between(|grid: 1: 1>, |grid: 4: 6>)
            |op: E> . |op: E> . |op: SE> . |op: SE> . |op: SE>

        find-steps-between(|grid: 1: 1>, |grid: 4: 6>)
            |grid: 1: 1> . |grid: 1: 2> . |grid: 1: 3> . |grid: 2: 4> . |grid: 3: 5> . |grid: 4: 6>

    see also:
        display-map, walking-ant.swc, find-path-between, find-steps-between
"""
def learn_map(context, *params):
    if len(params) < 2:
        return ket()
    if len(params) == 2:
        h, w = params
        op = 'value'
    if len(params) == 3:
        h, w, op = params
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

    for j in range(1, h + 1):
        for i in range(1, w + 1):
            elt = ket_elt(j, i)
            context.learn(op, elt, '0')
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
        display-map[h, w]
        display-map[h, w, op]
        display-map[h, w, op, empty-char]
        display a rectangular map, of height h, and width w
        where each cell is the value of op applied to that cell (default operator is 'value')
        where empty-char is printed for empty cells (default value of empty-char is ' ')
      
    examples:
        learn-map[5, 5, value]
        -- display an empty map:
        display-map[5, 5, value, "."]
            h: 5
            w: 5
            1     .  .  .  .  .
            2     .  .  .  .  .
            3     .  .  .  .  .
            4     .  .  .  .  .
            5     .  .  .  .  .

        -- learn some cell values:
        value |grid: 3: 1> => |H>
        value |grid: 3: 2> => |e>
        value |grid: 3: 3> => |l>
        value |grid: 3: 4> => |l>
        value |grid: 3: 5> => |o>

        -- now redraw our map:
        -- using default operator 'value', and default empty-char ' ':
        display-map[5, 5]
            h: 5
            w: 5
            1
            2
            3     H  e  l  l  o
            4
            5
                                
    see also:
        learn-map, walking-ant.swc
"""
def display_map(context, *params):
    if len(params) < 2:
        return ket()
    if len(params) == 2:
        h, w = params
        op = 'value'
        empty_char = ' '
    if len(params) == 3:
        h, w, op = params
        empty_char = ' '
    if len(params) == 4:
        h, w, op, empty_char = params
    w = int(w)
    h = int(h)

    def ket_elt(j, i):
        return ket("grid: " + str(j) + ": " + str(i))

    s = ""
    s += "h: " + str(h) + "\n"
    s += "w: " + str(w) + "\n"

    for j in range(1, h + 1):
        s += str(j).ljust(4)
        for i in range(1, w + 1):
            x = ket_elt(j, i)
            current_cell = context.recall('current', 'cell', True).to_sp() # not super happy with ant specific code here
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
                # value = ' '
                value = empty_char
            s += value.rjust(3)
        s += "\n"
    print(s)
    return ket('display-map')


# set invoke method:
seq_fn_table['merge-value'] = 'merge_value'
# set usage info:
function_operators_usage['merge-value'] = """
    description:
        merge-value seq
        merges coeff's and label's into a single number
        works with superpositions, and sequences
      
    examples:
        -- superposition example:
        merge-value (0|3> + 3|1> + 5|2>)
            |13>

        -- sequence of superpositions example:        
        merge-value (0|3> + 1|7> . 4|2> + 5|3> + 4|5>)
            |50>
    
    note:
        where is this even used? Can we get rid of it?
        looks like first version of walking-ant.sw uses it.
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
        and(ket, ket)
        the and function
        NB: it evaluates both sequences before being passed to the 'and' function
        NB: it currently doesn't handle sequences all that well
      
    examples:
        and(|yes>, |yes>)
            |yes>
        
        and(|yes>, |no>)
            |no>
    
    see also:
      if, or, xor
"""
def And(input_seq, one, two):
    if one.to_sp().label.lower() in ['true', 'yes'] and two.to_sp().label.lower() in ['true', 'yes']:
        return ket('yes')
    return ket('no')


# set invoke method:
whitelist_table_2['or'] = 'Or'
# set usage info:
sequence_functions_usage['or'] = """
    description:
        or(ket, ket)
        the or function
        NB: it evaluates both sequences before being passed to the 'or' function
        NB: it currently doesn't handle sequences all that well
      
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
def Or(input_seq, one, two):
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
        common[op] sp
        find kets in common, with respect to an operator
      
    examples:
        friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
        friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Rober> + |Frank> + |Julie>
        common[friends] split |Fred Sam>
            |Jack> + |Emma> + |Charlie>
            
    see also:
        union
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


# set invoke method:
compound_table['union'] = ['apply_sp_fn', 'operator_union', 'context']
# set usage info:
function_operators_usage['union'] = """
    description:
        union[op] sp
        find the unions of kets, with respect to an operator

    examples:
        friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
        friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Rober> + |Frank> + |Julie>
        union[friends] split |Fred Sam>
            |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie> + |George> + |Rober> + |Frank> + |Julie>

        -- this is in contrast to a simple addition:
        -- NB: the coefficients of 2, for repeated friends:
        friends split |Fred Sam>
            2|Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + 2|Emma> + 2|Charlie> + |George> + |Rober> + |Frank> + |Julie>

    see also:
        common
"""
def operator_union(one, context, op):
    if len(one) == 0:
        return ket("", 0)
    for sp in one:
        r = sp.apply_op(context, op)
        break
    for sp in one:
        tmp = sp.apply_op(context, op)
        r = union(r, tmp)  # we could probably make this a general function, and then pass in intersection(), union() etc.
    return r  # ie, cast pair-fn(sp1,sp2) into fn(sp1,sp2,...,spn)


# 2/2/2015:
# int-coeffs-to-sentence (3|apple> + 2|pear> + |orange> + 7|lemon>)
# |3 apples, 2 pears, 1 orange and 7 lemons>
# def int_coeffs_to_sentence(one,context):

# set invoke method:
ket_context_table['int-coeffs-to-word'] = 'int_coeffs_to_word'
# set usage info:
function_operators_usage['int-coeffs-to-word'] = """
    description:
        int-coeffs-to-word ket
        apply the coefficient to the word 
        and map the word to plural as required
      
    examples:
        -- learn some simple plurals:
        plural |*> #=> |_self> _ |s>
        plural |mouse> => |mice>
        plural |tooth> => |teeth>
        
        -- now put it to use:
        int-coeffs-to-word (3|apple> + 2|pear> + |orange> + 7|lemon> + 3|mouse> + 2|tooth> + 9|cat>)
            |3 apples> + |2 pears> + |1 orange> + |7 lemons> + |3 mice> + |2 teeth> + |9 cats>
      
        -- now apply the list-to-words operator:
        list-to-words int-coeffs-to-word (3|apple> + 2|pear> + |orange> + 7|lemon> + 3|mouse> + 2|tooth> + 9|cat>)
            |3 apples, 2 pears, 1 orange, 7 lemons, 3 mice, 2 teeth and 9 cats>   

    see also:
        list-to-words, words-to-list
        plurals.sw
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
        is-prime ket
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
        prime-factors ket
        returns a list of prime factors

    examples:
        -- without specifying a category:
        prime-factors |987654321>
            2|3> + 2|17> + |379721>
      
        -- with specifying a category, in this example 'number: '
        prime-factors |number: 123456789>
            2|number: 3> + |number: 3607> + |number: 3803>
        
         to-comma-number prime-factors |987654321987654321>
            2|3> + |7> + |11> + |13> + 2|17> + |19> + |52,579> + |379,721>

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
        inherit[op] ket
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
    
    see also:
        clone
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
        sort-by[op] sp
        natural sort the given superposition with respect to the given operator
        chomps any ',' chars, so you can sort by to-comma-numbers.

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
      
        -- reverse sort by population:
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

    see also:
        reverse, table
"""
# one is a superposition
def sort_by(one, context, op):
    def extract_ket_details(x):
        return x.apply_op(context, op).to_sp().label.lower().replace(',', '')

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
fn_table['read-text'] = 'read_text'
# set usage info:
function_operators_usage['read-text'] = """
    description:
        read-text ket
        'read' a sentence
        Not even sure this thing is useful!

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
# set usage info:
function_operators_usage['active-buffer'] = """
    description:
        active-buffer[N, t] seq
        active-buffer[N, t, op] seq
        an early version of 'actively' reading a sentence, and use back-ground knowledge to work out what is said
        not super impressive, and in many cases 'explain' does a better job.

    examples:
        -- learn a simple face:
        |body part: face> => 2|eye> + |nose> + 2|ear> + 2|lip> + |hair>
    
        active-buffer[7,0] (2|eye> + |nose>)
            0.375|body part: face>
            
        active-buffer[7,0] (2|eye> + |nose> + 2|ear> + 2|lip> + |hair>)
            |body part: face>

        
        -- reset the console:
        reset
        load internet-acronyms.sw
        apply-word |*> #=> |word:> __ |_self>
        remove-punctuation (*) #=> string-replace(|_self>, split[""] |:;.,!?$-"'>, |>)
        read |*> #=> apply-word ssplit[" "] to-lower remove-punctuation remove-prefix["text: "] |_self>
        active-buffer[7,0] read |text: fwiw I think it is all fud imho, lol. thx.>
            |phrase: For What It's Worth> . |> . |> . |> . |> . |> . |phrase: Fear, Uncertainty, Doubt> . |phrase: In My Humble Opinion> . |phrase: Laughing Out Loud> . |phrase: Thanks>

        reset
        load breakfast-menu.sw
        apply-word |*> #=> |word:> __ |_self>
        remove-punctuation (*) #=> string-replace(|_self>, split[""] |:;.,!?$-"'>, |>)
        read |*> #=> apply-word ssplit[" "] to-lower remove-punctuation remove-prefix["text: "] |_self>
        active-buffer[7,0] read description |food: Homestyle Breakfast>
            |number: 2> . |food: eggs> . |food: bacon> . |> . |food: sausage> . |food: toast> . |> . |> . |> . |food: hash browns> . |>

        reset
        apply-word |*> #=> |word:> __ |_self>
        remove-punctuation (*) #=> string-replace(|_self>, split[""] |:;.,!?$-"'>, |>)
        read |*> #=> apply-word ssplit[" "] to-lower remove-punctuation remove-prefix["text: "] |_self>
        load active-buffer-example.sw

        active-buffer[7,0] read |text: Hey Freddie what's up?>
            |greeting: Hey!> . 0.25|person: Fred Smith> . |> . |direction: up> + 0.333|phrase: up the duff>
            
        active-buffer[7,0] read |text: Hey Mazza, you with child, up the duff, in the family way, having a baby?>
            |greeting: Hey!> . |person: Mary> . |> . |phrase: with child> . |> . |direction: up> + |phrase: up the duff> + 0.25|phrase: in the family way> . |> . |> . |phrase: in the family way> + 0.333|phrase: up the duff> . |> . |> . |> . |phrase: having a baby> . |> . |>

        active-buffer[7,0] active-buffer[7,0] read |text: Hey Mazza, you with child, up the duff, in the family way, having a baby?>
            |> . |> . |> . 0.25|concept: pregnancy> . |> . 0.361|concept: pregnancy> . |> . |> . 0.5|concept: pregnancy> . |> . |> . |> . 0.25|concept: pregnancy> . |> . |>

    see also:
        explain
"""
# one is a sequence:
def active_buffer(one, context, *params):
    # print('one: %s' % str(one))
    # print('params: %s' % str(params))
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
            # print('y: %s' % str(y))
            # print('r: %s\n' % str(r))
            if len(r) > 0:
                sp = union(sp, r)
        seq += sp
    return seq


# set invoke method:
sp_fn_table['list-to-words'] = 'sp_to_words'
# set usage info:
function_operators_usage['list-to-words'] = """
    description:
        list-to-words sp
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
        handle sequences better

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
        words-to-list ket
        splits the given ket on ', ' and ' and '
        it is the inverse of list-to-words

    examples:
        words-to-list |a, b, c, d and e>
            |a> + |b> + |c> + |d> + |e>
    
        -- demonstration of inverse property:
        list-to-words words-to-list |a, b, c, d and e>
            |a, b, c, d and e>
    
        -- implemented using split/ssplit:
        split[" and "] split[", "] |a, b, c, d and e>
            |a> + |b> + |c> + |d> + |e>

        ssplit[" and "] ssplit[", "] |a, b, c, d and e>
            |a> . |b> . |c> . |d> . |e>

    see also:
      list-to-words, split, ssplit      
"""
# one is a ket
def words_to_sp(one):
    try:
        head, tail = one.label.split(' and ')
        front = head.split(', ')
        r = superposition()
        for x in front + [tail]:
            r.add(x, one.value)
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
        find-path-between(ket, sp)
        find the path between the ket, and the given superposition
        currently, potentially quite slow! But this is fixable.
      
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
        optimize it with Dijkstra's algorithm
        (since current algorithm is horrible!)
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



def find_path_between(input_seq, context, one, two):
    max_steps = 10                      # put a hard limit on the max number of operator steps
    one = one.to_sp()
    two = two.to_sp()

    def is_subset(A, B):  # test if one is a subset of two
        A = A.to_sp().apply_sigmoid(clean)  # ignore coeffs for now
        B = B.to_sp().apply_sigmoid(clean)
        r = intersection(A, B)
        if len(r) == len(A):
            return True
        return False

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
        find-steps-between(ket, ket)
        find the steps between the given kets
        currently potentially quite slow!

    examples:
        load early-us-presidents.sw
        find-inverse[president-number, president-era, full-name]

        find-steps-between(|person: George Washington>, |number: 6>)
            |person: George Washington> . |Washington> . |year: 1797> . |Adams> . |year: 1801> . |Jefferson> . |party: Democratic-Republican> . |year: 1825> . |Q Adams> . |number: 6>

    future:
        optimize it with Dijkstra's algorithm
        (since current algorithm is horrible!)
        make it work with path-ways between sequences too.
        
    see also:
        find-path-between
"""
def first_find_steps_between(context, one, two):
    op_path = find_path_between(context, one, two)
    if type(op_path) is ket and op_path.label == 'path not found':
        return ket('steps not found')

    def is_subset(A, B):  # test if one is a subset of two
        A = A.to_sp().apply_sigmoid(clean)  # ignore coeffs for now
        B = B.to_sp().apply_sigmoid(clean)
        r = intersection(A, B)
        if len(r) == len(A):
            return True
        return False

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

def find_steps_between(input_seq, context, one, two):
    op_path = find_path_between(input_seq, context, one, two)
    if type(op_path) is ket and op_path.label == 'path not found':
        return ket('steps not found')

    def is_subset(A, B):  # test if one is a subset of two
        A = A.to_sp().apply_sigmoid(clean)  # ignore coeffs for now
        B = B.to_sp().apply_sigmoid(clean)
        r = intersection(A, B)
        if len(r) == len(A):
            return True
        return False

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
# set usage info:
function_operators_usage['exp'] = """
    description:
        exp[op, n] |x>
        essentially the first n terms of exp(op) applied to |x>, ignoring factors of 1/n!
        if you want the 1/n! too, then see full-exp
        cf: exp(A) |Psi> in quantum mechanics
        ie: (1 + op + op^2 + ... + op^n) |x>
        if n <= 0, return |x>
         
    examples:
        -- load a binary tree:
        load tree.sw

        -- find left branch of tree:
        exp[left, 3] |x>
            |x> + |0> + |00> + |000>

        -- find right branch of tree:
        -- NB: in this case exp[right, 4] would have sufficed
        exp[right, 10] |x>
            |x> + |1> + |11> + |111> + |1111>

        -- find the head of the tree:
        exp[child, 2] |x>
            |x> + |0> + |1> + |00> + |01> + |10> + |11>

    see also:
        full-exp, exp-max, sexp
        
    TODO:
        currently it doesn't handle sequences all that well.
"""
# 12/5/2014:
# exp[child,n] |x>
# maps to: (1 + child + child^2 + ... + child^n ) |x>
# cf: exp(A) |Psi> in QM.
# if n <= 0, return |x>
#
def exp(one, context, *params):
    try:
        op, n = params
        n = int(n)
    except:
        return one

    r = superposition(one)
    tmp = one
    for k in range(n):
        tmp = tmp.apply_op(context, op).to_sp()  # this is broken for some operators, depends on details of that operator though!
        r.add_sp(tmp)
    return r


# set invoke method:
compound_table['exp-max'] = ['apply_fn', 'exp_max', 'context']
# set usage info:
function_operators_usage['exp-max'] = """
    description:
        exp-max[op] |x>
        exp(op) applied to |x>, ignoring factors of 1/n!
        if you want the 1/n! too, then see full-exp
        cf: exp(A) |Psi> in quantum mechanics
        ie: (1 + op + op^2 + ... + op^n) |x>
        where we go to full depth
        ie, n is such that len(exp[op, n] |x>) == len(exp[op, n+1] |x>)

    examples:
        -- load a binary tree:
        load tree.sw

        -- entire left branch of tree:
        exp-max[left] |x>
            n: 4
            |x> + |0> + |00> + |000> + |0000>
            
        -- full tree starting from |11>:
        exp-max[child] |11>
            n: 2
            |11> + |110> + |111> + |1100> + |1101> + |1110> + |1111>
        
        -- find the lengths of the node names in the full tree:
        ket-length exp-max[child] |x>
            n: 4
            3|number: 1> + 4|number: 2> + 8|number: 3> + 16|number: 4>

    see also:
        exp, full-exp
"""
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

    r = superposition(one)
    tmp = one
    previous_size = len(r)  # yup. I finally implemented len() for superpositions/kets.
    n = 0
    while True:
        tmp = tmp.apply_op(context, op).to_sp()
        r.add_sp(tmp)
        #    if len(r) == previous_size:            # a variant is: len(r) - previous_size <= t
        if len(r) - previous_size <= t:  # since kets add in sp, this difference is the number of newly discovered kets.
            break  # so, if this is 0, then we have reached the end of the network.
        previous_size = len(r)  # if this is say 1, then in this round we only found 1 new ket.
        n += 1  # which in some cases is enough to say, this will suffice as the end of the network.
    print("n:", n)
    return r


# set invoke method:
compound_table['full-exp'] = ['apply_fn', 'full_exp', 'context']
# set usage info:
function_operators_usage['full-exp'] = """
    description:
        full-exp[op, n] |x>
        the first n terms of exp(op) applied to |x>, including factors of 1/n!
        if you don't want the 1/n!, then see exp
        cf: exp(A) |Psi> in quantum mechanics
        ie: (1 + op/1! + op^2/2! + ... + op^n/n!) |x>
        if n <= 0, return |x>
        most of the time, you probably just want exp[op, n] or exp-max[op]

    examples:
        -- load a binary tree:
        load tree.sw

        -- find left branch of tree:
        full-exp[left, 3] |x>
            |x> + |0> + 0.5|00> + 0.167|000>            

        -- find right branch of tree:
        -- NB: in this case full-exp[right, 4] would have sufficed
        full-exp[right, 10] |x>
            |x> + |1> + 0.5|11> + 0.167|111> + 0.042|1111>

        -- find the head of the tree:
        full-exp[child, 3] |x>
            |x> + |0> + |1> + 0.5|00> + 0.5|01> + 0.5|10> + 0.5|11> + 0.167|000> + 0.167|001> + 0.167|010> + 0.167|011> + 0.167|100> + 0.167|101> + 0.167|110> + 0.167|111>
            
    see also:
        exp, exp-max
"""
# 17/4/2015:
# full-exp[child,n] |x>
# maps to: (1 + child/1 + child^2/2 + ... + child^n/n! ) |x>
# cf: exp(A) |Psi> in QM.
# if n <= 0, return |x>
#
def full_exp(one, context, *parameters):
    try:
        op, n = parameters
        n = int(n)
    except:
        return one

    r = superposition(one)
    tmp = one
    for k in range(n):
        tmp = tmp.apply_op(context, op).to_sp()
        r.add_sp(tmp.multiply(1 / factorial(k + 1)))
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
compound_table['rel-kets'] = ['apply_sp_fn', 'intersection_relevant_kets', 'context']
# set usage info:
function_operators_usage['rel-kets'] = """
    description:
        rel-kets[op]
        return all relevant kets that have op specified
        if op is * then return everything that has a literal operator specified for it
        NB: rel-kets[op] does not return kets that are only specified on the right hand side of a learn rule 
        
        rel-kets[op1,op2, ..., opn]
        return all relevant kets that have op1, ... , opn specified
        
        rel-kets[op1, ... , opn] sp
        return all relevant kets, in the given superposition, that have op1, ... , opn specified

    examples:
        load fred-sam-friends.sw
        rel-kets[friends]
            |Fred> + |Sam>
        
        age |Sam> => |47>
        rel-kets[friends, age]
            |Sam>
        
        load family.sw
        rel-kets[*]
            |context> + |sally> + |erica> + |trude> + |peter> + |tom> + |sara> + |sam> + |ruth> + |mike> + |gina> + |mary> + |mark>
        
        load family-relations.sw
        such-that[is-a-female] rel-kets[*]
            |sally> + |erica> + |trude> + |sara> + |ruth> + |gina> + |mary>

        such-that[is-an-uncle] rel-kets[*]
            |peter>

        such-that[have-a-sister] rel-kets[*]
            |sally> + |erica>
            
        such-that[have-a-sister, is-a-teenager] rel-kets[*]
            |sally>

        such-that[have-a-brother] rel-kets[*]
            |peter> + |tom>

         such-that[have-a-wife] rel-kets[*]
            |tom> + |sam> + |mike> + |mark>

    see also:
        such-that
        
    TODO:
        fix sequence behaviour
        maybe implement all-kets which returns even kets that are only specified on the right of a learn rule 
"""
def intersection_relevant_kets(one, context, *ops):
    if len(one) == 0:
        r = context.relevant_kets('*')
    else:
        r = one
    for op in ops:
        kets_list = context.relevant_kets(op)
        r = intersection(r, kets_list)
    return r


# 22/2/2015 tweaked: now if op == "*" it returns a sp of all known kets.
#def relevant_kets(one, context, op):
#    return context.relevant_kets(op)


# set invoke method:
compound_table['similar-input'] = ['apply_seq_fn', 'similar_input', 'context']
# set usage info:
function_operators_usage['similar-input'] = """
    description:
        similar-input[op] seq
        returns the similarity of seq with all kets that have op defined
        the back-end to this operator uses simm

    examples:
        -- learn the noises of cats and dogs:
        sounds-it-makes |cat> => |purring> + |miaowing> + |scratching at the door>
        sounds-it-makes |dog> => |panting> + |sniffing> + |scratching at the door>

        -- which animal is at the door, given the input noise:
        which-animal-given (*) #=> normalize[100] similar-input[sounds-it-makes] words-to-list |_self>

        -- now ask some questions:
        which-animal-given |panting>
            100.0|dog>

        which-animal-given |purring>
            100.0|cat>

        which-animal-given |scratching at the door>
            50.0|cat> + 50.0|dog>

        which-animal-given |sniffing and scratching at the door>
            66.667|dog> + 33.333|cat>

        -- predict which noises you will hear next, given the input noise:
        predict-noise-given (*) #=> normalize[100] sounds-it-makes similar-input[sounds-it-makes] words-to-list |_self>

        -- now ask some questions:
        predict-noise-given |panting>
            33.333|panting> + 33.333|sniffing> + 33.333|scratching at the door>

        predict-noise-given |purring>
            33.333|purring> + 33.333|miaowing> + 33.333|scratching at the door>

        predict-noise-given |sniffing and scratching at the door>
            22.222|panting> + 22.222|sniffing> + 33.333|scratching at the door> + 11.111|purring> + 11.111|miaowing>

        bar-chart[40] predict-noise-given |sniffing and scratching at the door>
            ----------
            panting                : ||||||||||||||||||||||||||
            sniffing               : ||||||||||||||||||||||||||
            scratching at the door : ||||||||||||||||||||||||||||||||||||||||
            purring                : |||||||||||||
            miaowing               : |||||||||||||
            ----------

    see also:
        find-topic, simm, map
"""
def similar_input(self, context, op):
    return context.pattern_recognition(self, op)



# set invoke method:
compound_table['find-topic'] = ['apply_fn', 'find_topic', 'context']
# set usage info:
function_operators_usage['find-topic'] = """
    description:
        find-topic[op] |x>
        find most similar frequency list, defined with respect to op, of |x>
        the back-end to this operator uses normed-frequency-class

    examples:
        -- load some knowledge:
        -- in this case US census frequency list of male, female and last names:
        -- NB: unfortunately this is super memory hungry!
        web-load http://semantic-db.org/sw-examples/names.sw
        
        -- define our operator:
        guess-name-type |*> #=> find-topic[names] to-lower |_self>
        
        -- ask about 'Emma'
        guess-name-type |Emma>
            90.323|female name> + 9.677|last name>
        
        -- ask about 'Gina'
        guess-name-type |Gina>
            100|female name>
                    
        -- ask about 'Mark'
        guess-name-type |Mark>
            54.664|male name> + 28.633|last name> + 16.703|female name>

        -- ask about 'Fred'
        guess-name-type |Fred>
            63.294|male name> + 28.418|last name> + 8.288|female name>
        
        -- ask about 'Branson'
        guess-name-type |Branson>
            100|last name>

        -- define our guess-gender operator:
        name-type |male name> => |male>
        name-type |female name> => |female>
        guess-gender |*> #=> clean select[1,1] name-type find-topic[names] to-lower |_self>
        
        guess-gender |Lisa>
            |female>

        guess-gender |Eric>
            |male>

        guess-gender |Jane>
            |female>

        guess-gender |Stephen>
            |male>

    see also:
        similar-input, normed-frequency-class
"""
# implements: find-topic[op] |x>
def find_topic(self, context, op):
    return context.map_to_topic(self, op)


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
            
        mbr(|x>, 0.3|a> + 2|b> + 9.7|c> + 13|d>)
            |>

    see also:
        is-mbr, intersection
"""
def mbr(input_seq, e, two):
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

        is-mbr(|x>, 0.3|a> + 2|b> + 9.7|c> + 13|d>)
            |no>
        
        friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
        is-mbr(|Ed>, friends |Fred>)
            |yes>
        
        is-mbr(|Frank>, friends |Fred>)
            |yes>

        is-mbr(|Jane>, friends |Fred>)
            |no>

    see also:
        mbr
"""
def is_mbr(input_seq, e, two):
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
        subset(one, two) returns the degree of subsetness of one with respect to two
        where one and two are superpositions

    examples:
        subset(|b>, |a> + |b> + |c>)
            |subset>

        subset(|c>, 0.3|a> + 2|b> + 9.7|c> + 13|d>)
            |subset>
            
        subset(|b> + |d>, |a> + |b> + |c>)
            0.5|subset>

    see also:
        is-subset, mbr, is-mbr
"""
def subset(input_seq, one, two):
    one = one.to_sp()
    two = two.to_sp()

    if one.count_sum() == 0:  # prevent div by 0.
        return ket()
    value = intersection(one, two).count_sum() / one.count_sum()
    return ket("subset", value)


# set invoke method:
whitelist_table_2['is-subset'] = 'is_subset'
# set usage info:
sequence_functions_usage['is-subset'] = """
    description:
        is-subset(one, two) returns |yes> if one is an exact subset of two, else |no>
        where one and two are superpositions

    examples:
        is-subset(|b>, |a> + |b> + |c>)
            |yes>

        is-subset(8|c> + 13|d> + 0.2|a>, 0.3|a> + 2|b> + 9.7|c> + 13|d>)
            |yes>

        is-subset(|b> + |d>, |a> + |b> + |c>)
            |no>

    see also:
        subset, mbr, is-mbr
"""
def is_subset(input_seq, one, two):
    result = subset(input_seq, one, two)
    if result.value >= 0.95:
        return ket('yes')
    return ket('no')



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
        makes use of simm

    examples:

    see also:
        simm, is-equal
    
    future:
        I'm not super happy with the way this is defined.
        Isn't it redundant, and just a wrapper around simm?
        Wouldn't it be cleaner for it to be binary, and return |True> or |False> and not mess with coefficients?
"""
def equality_test(input_seq, one, two):
    value = aligned_simm_value(one, two)  # NB: equal(0|x>,0|x>) returns 0|True>. Not currently sure if we want this, or need to tweak.
    return ket("True", value)


# set invoke method:
whitelist_table_2['is-equal'] = 'is_equal'
# set usage info:
sequence_functions_usage['is-equal'] = """
    description:
        is-equal(one, two) returns:
        |yes> if simm(one, two) >= 0.5
        |no> otherwise
        values in between otherwise
        makes use of simm 

    examples:
        -- alternate implementation:
        test-equal (*,*) #=> do-you-know drop-below[0.5] simm(|_self1>, |_self2>)
    
    see also:
        simm, equal, if
"""
def is_equal(input_seq, one, two):
    value = aligned_simm_value(one, two)
    # if value > 0:  # change this to value > 0.5 ?
    if value >= 0.5:
        return ket('yes', value)
    return ket('no')


# set invoke method:
whitelist_table_2['is-exactly-equal'] = 'is_exactly_equal'
# set usage info:
sequence_functions_usage['is-exactly-equal'] = """
    description:
        is-equal(one, two) returns:
        |yes> if simm(one, two) >= 0.95
        |no> otherwise
        values in between otherwise
        makes use of simm 

    examples:
        -- alternate implementation:
        test-equal (*,*) #=> do-you-know drop-below[0.95] simm(|_self1>, |_self2>)

    see also:
        simm, equal, if
"""
def is_exactly_equal(input_seq, one, two):
    value = aligned_simm_value(one, two)
    # if value > 0:  # change this to value > 0.5 ?
    if value >= 0.95:
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
        smooth[dx] ket
        smooths peaks into Gaussian's
        eg: 
            smooth[dx] a|x: 3>
        returns:
            a/4 |x: 3 - dx> + a/2 |x: 3> + a/4 |x: 3 + dx>
        usually invoked in form: smooth[dx]^power
        also used to enable similarity between nearby integers

    examples:
        smooth[0.5] |age: 30>
            0.25|age: 29.5> + 0.5|age: 30> + 0.25|age: 30.5>
            
        -- show what this looks like:
        bar-chart[40] smooth[0.5] |age: 30> 
            ----------
            age: 29.5 : ||||||||||||||||||||
            age: 30   : ||||||||||||||||||||||||||||||||||||||||
            age: 30.5 : ||||||||||||||||||||
            ----------
        
        smooth[1]^5 |age: 40>
            0.001|age: 35> + 0.01|age: 36> + 0.044|age: 37> + 0.117|age: 38> + 0.205|age: 39> + 0.246|age: 40> + 0.205|age: 41> + 0.117|age: 42> + 0.044|age: 43> + 0.01|age: 44> + 0.001|age: 45>
        
        -- show what this looks like:
        bar-chart[40] smooth[1]^5 |age: 40> 
            ----------
            age: 35 :
            age: 36 : |
            age: 37 : |||||||
            age: 38 : |||||||||||||||||||
            age: 39 : |||||||||||||||||||||||||||||||||
            age: 40 : ||||||||||||||||||||||||||||||||||||||||
            age: 41 : |||||||||||||||||||||||||||||||||
            age: 42 : |||||||||||||||||||
            age: 43 : |||||||
            age: 44 : |
            age: 45 :
            ----------

        rescale[1] smooth[1]^5 |age: 40>
            0.004|age: 35> + 0.04|age: 36> + 0.179|age: 37> + 0.476|age: 38> + 0.833|age: 39> + |age: 40> + 0.833|age: 41> + 0.476|age: 42> + 0.179|age: 43> + 0.04|age: 44> + 0.004|age: 45>

        age-simm (*,*) #=> simm(smooth[1]^5 |_self1>, smooth[1]^5 |_self2>)
        age-simm(|age: 36>, |age: 40>)
            0.227|simm>

    see also:
        rescale, simm, Gaussian
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


# set invoke method:
compound_table['Gaussian'] = ['apply_fn', 'Gaussian', '']
# set usage info:
function_operators_usage['Gaussian'] = """
    description:
        Gaussian[sigma] ket
        Gaussian[sigma, dx] ket
        implement a Gaussian smooth
        if dx is not specified, it defaults to 1
        sigma is the width of the Gaussian
        
    the algorithm:
        exp( - ED(x, y) / (2 * sigma^2) )
        where ED(x, y) is the Euclidean distance between x, y
        
    examples:
        -- 1D version:
        Gaussian[0.7] |age: 40>
            0.017|age: 36> + 0.047|age: 37> + 0.13|age: 38> + 0.36|age: 39> + |age: 40> + 0.36|age: 41> + 0.13|age: 42> + 0.047|age: 43> + 0.017|age: 44>
            
        -- bar-chart of 1D version:
        bar-chart[50] Gaussian[0.7] |age: 35>
            ----------
            age: 31 :
            age: 32 : ||
            age: 33 : ||||||
            age: 34 : ||||||||||||||||||
            age: 35 : ||||||||||||||||||||||||||||||||||||||||||||||||||
            age: 36 : ||||||||||||||||||
            age: 37 : ||||||
            age: 38 : ||
            age: 39 :
            ----------

        -- age similarity, using Gaussian[0.7]:
        Gauss-simm-40 |*> #=> round[3] push-float 100 simm(Gaussian[0.7] |_self>, Gaussian[0.7] |age: 40>)
        table[age, Gauss-simm-40] range(|age: 30>, |age: 50>)
            +-----+---------------+
            | age | Gauss-simm-40 |
            +-----+---------------+
            | 30  | 0             |
            | 31  | 0             |
            | 32  | 0.801         |
            | 33  | 1.601         |
            | 34  | 3.823         |
            | 35  | 6.044         |
            | 36  | 12.207        |
            | 37  | 18.37         |
            | 38  | 35.468        |
            | 39  | 52.565        |
            | 40  | 100.0         |
            | 41  | 52.565        |
            | 42  | 35.468        |
            | 43  | 18.37         |
            | 44  | 12.207        |
            | 45  | 6.044         |
            | 46  | 3.823         |
            | 47  | 1.601         |
            | 48  | 0.801         |
            | 49  | 0             |
            | 50  | 0             |
            +-----+---------------+

                    
        -- 2D version:
        Gaussian[0.5, 1] |grid: 10: 10>
            0.003|grid: 8: 8> + 0.011|grid: 8: 9> + 0.018|grid: 8: 10> + 0.011|grid: 8: 11> + 0.003|grid: 8: 12> + 0.011|grid: 9: 8> + 0.059|grid: 9: 9> + 0.135|grid: 9: 10> + 0.059|grid: 9: 11> + 0.011|grid: 9: 12> + 0.018|grid: 10: 8> + 0.135|grid: 10: 9> + |grid: 10: 10> + 0.135|grid: 10: 11> + 0.018|grid: 10: 12> + 0.011|grid: 11: 8> + 0.059|grid: 11: 9> + 0.135|grid: 11: 10> + 0.059|grid: 11: 11> + 0.011|grid: 11: 12> + 0.003|grid: 12: 8> + 0.011|grid: 12: 9> + 0.018|grid: 12: 10> + 0.011|grid: 12: 11> + 0.003|grid: 12: 12>

    see also:
        smooth, distance, normalize
"""
def Gaussian(one, sigma, dx=1):
    def ED(x, y):               # the Euclidean distance function
        if len(x) != len(y):
            return 0
        r = sum((x[k] - y[k])**2 for k in range(len(x)))
        return math.sqrt(r)

    def Gauss(x, y, sigma):
        r = - ED(x, y) / (2 * sigma**2)
        return math.exp(r)

    def find_gauss_width(sigma):  # given sigma, find the width of the Gaussian
        return 9 * sigma**2

    one = one.to_sp()
    values = one.label.split(': ')[::-1]
    # print('one:', one)
    # print('sigma:', sigma)
    # print('sigma^2:', sigma**2)
    # print('dx:', dx)

    x_values = []
    for x in values:
        if x.isdigit():
            x_values.append(float(x))
        else:
            break
    # print('x-values:', x_values)

    if len(x_values) == 0:
        return ket()

    category = values[len(x_values):]
    # print('category:', category)
    cat = ''
    if len(category) > 0:
        cat = ': '.join(category) + ': '

    width = find_gauss_width(sigma)
    # print('width:', width)

    if len(x_values) == 1:
        x = x_values[0]
        start = math.ceil((x - width)/dx)*dx
        finish = math.floor((x + width) / dx) * dx
        r = superposition()
        for y in float_range(start, finish, dx):
            value = Gauss([x], [y], sigma)
            # print('%s: %s' % (y, value))
            r.add(cat + float_to_int(y), value * one.value)
        return r

    elif len(x_values) == 2:
        x1, x2 = x_values

        start1 = math.ceil((x1 - width)/dx)*dx
        finish1 = math.floor((x1 + width) / dx) * dx
        start2 = math.ceil((x2 - width) / dx) * dx
        finish2 = math.floor((x2 + width) / dx) * dx

        r = superposition()
        for y1 in float_range(start1, finish1, dx):
            for y2 in float_range(start2, finish2, dx):
                value = Gauss([x1, x2], [y1, y2], sigma)
                # print('%s: %s' % (y, value))
                r.add(cat + float_to_int(y1) + ': ' + float_to_int(y2), value * one.value)  # need to verify order of y1 vs y2
                # r.add(cat + float_to_int(y2) + ': ' + float_to_int(y1), value * one.value)
        return r

    return ket()


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
# set invoke method:
compound_table['map'] = ['apply_sp_fn', 'map', 'context']
# set usage info:
function_operators_usage['map'] = """
    description:
        map[fn, op] sp
        map a function operator to a literal operator
        eg: map[fn, op] (|x> + |y> + |z>)
        runs:
        op |x> => fn |_self>
        op |y> => fn |_self>
        op |z> => fn |_self>

    examples:
        -- define the star operator:
        star-op |*> #=> apply( supported-ops |_self>, |_self>)
        map[star-op, star] rel-kets[*]
        
        -- define a binary tree:
        -- define the head:
        left |x> => |0>
        right |x> => |1>
        
        -- define our operators:
        child |*> #=> left |_self> + right |_self>
        left-op |*> #=> |_self> _ |0>
        right-op |*> #=> |_self> _ |1>
        
        -- now build the tree:
        map[left-op, left] child |x>
        map[right-op, right] child |x>

        map[left-op, left] child^2 |x>
        map[right-op, right] child^2 |x>
        
        map[left-op, left] child^3 |x>
        map[right-op, right] child^3 |x>

        map[left-op, left] child^4 |x>
        map[right-op, right] child^4 |x>
        ...

        -- approximate implementation using multi-line stored rules:
        -- makes use of the linearity of |*> rules
        map-fn-to-op |*> #=>
            op |__self> => fn |__self>
        
        -- then invoke it:
        map-fn-to-op (|x> + |y> + |z>)

    see also:
        tree.sw, copy-map
"""
def map(one, context, *op):
    try:
        fn, op = op
    except:
        fn = op

    for x in one:  # what if x has x.value != 1? x.apply_op handles that.
        if x.label != '*':  # what about foo |category: *> #=> ... rules? Should they be excluded too?
            context.learn(op, x, x.apply_op(context, fn))  # currently fn must be of form: fn |*> #=> bah.
    return ket("map")  # Would sometimes be useful to be able to use a full function here.
    # Something we probably need to take up with .apply_op()
    # As then (presumably) it could work for similar[op] |ket> too.
    # Code change for this is probably hard, since would need pieces from the processor file.


# 4/5/2015:
# a new version of map. This one puts results in a temporary store while doing the calculatoin, then copies the result back after.
# Basically to stop the code eating its own tail. eg, mapping a grid to a grid, you need a temporary grid.
def copy_map(one, context, *op):
    try:
        fn, op = op
    except:
        fn = op
    print("fn:", fn)
    print("op:", op)
    op_tmp = op + "-pDBUKObhYk"  # thanks: https://www.random.org/strings/
    print("op-tmp:", op_tmp)

    for x in one:
        context.learn(op_tmp, x, x.apply_op(context, fn))  # store results on temporary grid
    #  for x in one:
    #    context.learn(op,x,x.apply_op(context,op-tmp))
    #  context.copy_op(op_tmp,op)        # maybe ... still need some thinking time. What about context.mv_op(op_tmp,op)?
    #  context.delete_op(op-tmp)         # need to implement this function.
    context.move_op(op_tmp, op)
    return ket("copy-map")


# set invoke method:
# compound_table['inverse'] = ['apply_sp_fn', 'active_inverse', 'context']
compound_table['inverse'] = ['apply_fn', 'active_inverse', 'context']
# set usage info:
function_operators_usage['inverse'] = """
    description:
        inverse[op] sp
        reverses the direction of a literal operator, even |*> rules
        eg, say we have: op |A> => |B>
        then: inverse[op] |B> returns |A>
        and it really is an inverse, since:
        op inverse[op] |B> returns |B>
        and:
        inverse[op] op |A> returns |A>
        (though there are cases where it is not an exact inverse)
        
        NB: potentially quite slow, especially for |*> rules
        
    examples:
        load family.sw
        load family-relations.sw
        
        -- find who is an uncle in this data-set:
        such-that[is-an-uncle] rel-kets[*]
            |peter>
        
        -- find who Peter is an uncle for:
        inverse[uncle] |peter>
            |sally> + |erica>
            
        -- find who Peter is a brother-in-law for:
        inverse[brother-in-law] |peter>
            |trude>

        -- check this result:
        brother-in-law |trude>
            |peter>

        -- find who are grand-parents:
        such-that[is-a-grand-parent] rel-kets[*]
            |sara> + |sam> + |ruth> + |mike> + |gina> + |mary> + |mark>

        -- find who they are grand-parents for:
        inverse[grand-parent] |sara>
            |sally> + |erica>
        
        inverse[grand-parent] |sam>
            |sally> + |erica>
        
        inverse[grand-parent] |gina>
            |peter> + |tom>

        inverse[grand-parent] |mark>
            |peter> + |tom>

    see also:
        find-inverse
"""
def active_inverse(one, context, op):
    everyone = context.relevant_kets('*')
    # print(everyone)
    r = superposition()
    for x in everyone:
        y = x.apply_op(context, op).to_sp()
        # print('x: %s\ty: %s' % (x, y))
        for candidate in y:
            if candidate.label == one.label:
                r.add_sp(x)
    return r


# set invoke method:
ket_context_table['load-file'] = 'load_file'
# set usage info:
function_operators_usage['load-file'] = """
    description:
        load-file ket
        load a file from disk
        where file is in our sw-examples directory 

    examples:
        load-file |family.sw>

    see also:

    future:
        load a file from the web
        eg: load-file |http://semantic-db.org/sw-examples/george.sw>
"""
def load_file(one, context):
    name = one.label
    basename = os.path.basename(name)  # is this secure?
    print('loading: sw-examples/%s' % basename)
    context.load('sw-examples/' + basename)
    return ket('load-file')


# set invoke method:
compound_table['sexp'] = ['apply_seq_fn', 'seq_exp', 'context']
# set usage info:
function_operators_usage['sexp'] = """
    description:
        sexp[op] seq
        the sequence version of exp
        and the inverse of explain[op]

    examples:
        -- given this knowledge:
        cause |p> => |g> . |m> . |r>
        cause |t> => |p> . |p>
        cause |x> => |p> . |g>
        cause |z> => |r> . |p>

        -- find possible causes for: |g> . |m> . |r> . |g> . |m> . |r>
        explain[cause] ssplit[" . "] |g . m . r . g . m . r>
            t
            p . p
            g . m . z
            x . m . r
            g . m . r . p
            p . g . m . r
            g . m . r . g . m . r
        
        -- now use sexp to verify they all work:
        sexp[cause] |t>
            |g> . |m> . |r> . |g> . |m> . |r>
            
        sexp[cause] (|p> . |p>)
            |g> . |m> . |r> . |g> . |m> . |r>
            
        sexp[cause] (|g> . |m> . |z>)
            |g> . |m> . |r> . |g> . |m> . |r>
            
        sexp[cause] (|x> . |m> . |r>)
            |g> . |m> . |r> . |g> . |m> . |r>
            
        sexp[cause] (|g> . |m> . |r> . |p>)
            |g> . |m> . |r> . |g> . |m> . |r>
            
        sexp[cause] (|p> . |g> . |m> . |r>)
            |g> . |m> . |r> . |g> . |m> . |r>

    see also:
        exp, explain
"""
def seq_exp(one, context, *ops):
    if len(ops) == 1:
        op = ops[0]
        max_depth = 10 # hard code in a max_depth for now. Maybe later make it infinity.
    elif len(ops) == 2:
        op, max_depth = ops
    else:
        return ket()

    def single_step(one, context, op):
        seq = sequence([])
        for x in one:
            # print('x: %s' % x)
            child = x.apply_op(context, op)
            if len(child) == 0:
                child = x
            seq += child
        return seq

    len_one = len(one)
    for _ in range(max_depth):
        one = single_step(one, context, op)
        if len(one) == len_one:
            break
        len_one = len(one)
    return one


# set invoke method:
compound_table['explain'] = ['apply_seq_fn', 'third_explain', 'context']
# set usage info:
function_operators_usage['explain'] = """
    description:
        explain[op] seq
        given a cause structure, and an input sequence, find the possible cause
        See here for why we would want to do this:
        Parsimonious Covering Theory with Causal Chaining and Ordering Constraints:
        https://github.com/garrettkatz/copct

    examples:
        -- given this knowledge:
        cause |c> => |a> . |b>
        cause |d> => |a> . |b>
        cause |e> => |d> . |f>

        -- given this sequence: |a> . |b> . |f> . |a> . |b>
        -- find possible causes:
        -- note that even though it prints them all out, it only returns the shortest sequence:
        explain[cause] ssplit |abfab>
            e . c
            e . d
            e . a . b
            c . f . c
            c . f . d
            d . f . c
            d . f . d
            c . f . a . b
            a . b . f . c
            a . b . f . d
            d . f . a . b
            a . b . f . a . b
            |e> . |c>
            
        -- let's verify a couple of these:
        -- NB: we don't use the ssplit operator to make it clear the input is really a sequence, not a string:
        sexp[cause] (|e> . |c>)
            |a> . |b> . |f> . |a> . |b>

        sexp[cause] (|c> . |f> . |d>)
            |a> . |b> . |f> . |a> . |b>


        -- given this knowledge:
        cause |p> => |g> . |m> . |r>
        cause |t> => |p> . |p>
        cause |x> => |p> . |g>
        cause |z> => |r> . |p>

        -- find possible causes for: |g> . |m> . |r> . |g> . |m> . |r>
        explain[cause] ssplit[" . "] |g . m . r . g . m . r>
            t
            p . p
            g . m . z
            x . m . r
            g . m . r . p
            p . g . m . r
            g . m . r . g . m . r
        
        
        -- learn some knowledge about food:
        -- see breakfast-menu.sw
        seq |food: waffles> => |word: waffles>
        seq |country: Belgium> => |word: belgian>
        seq |food: strawberries> => |word: strawberries>
        seq |food: berries> => |word: berries>
        seq |country: France> => |word: french>
        seq |food: toast> => |word: toast>
        seq |meal: breakfast> => |word: breakfast>
        seq |food: egg> => |word: egg>
        seq |food: eggs> => |word: eggs>
        seq |food: bacon> => |word: bacon>
        seq |food: sausage> => |word: sausage>
        seq |food: sausages> => |word: sausages>
        seq |number: 2> => |word: two>
        seq |food: cream> => |word: cream>
        seq |food: belgian waffles> => |word: belgian> . |word: waffles>
        seq |food: maple syrup> => |word: maple> . |word: syrup>
        seq |food: whipped cream> => |word: whipped> . |word: cream>
        seq |food: hash browns> => |word: hash> . |word: browns>
        
        -- define our read operator:
        apply-word |*> #=> |word:> __ |_self>
        read |*> #=> apply-word ssplit[" "] replace[",", ""] remove-suffix[1] remove-prefix[1] remove-prefix["text: "] to-lower |_self>

        -- test it out:
        read |text: "Two eggs, bacon or sausage">
            |word: two> . |word: eggs> . |word: bacon> . |word: or> . |word: sausage>

        -- now use our explain[seq] operator:
        explain[seq] read |text: "Two eggs, bacon or sausage">
            |number: 2> . |food: eggs> . |food: bacon> . |word: or> . |food: sausage>
        
        -- now a couple of bigger examples:
        explain[seq] read |text: "Two eggs, bacon or sausage, toast, and our ever-popular hash browns">
            |number: 2> . |food: eggs> . |food: bacon> . |word: or> . |food: sausage> . |food: toast> . |word: and> . |word: our> . |word: ever-popular> . |food: hash browns>

        explain[seq] read |text: "Light Belgian waffles covered with strawberries and whipped cream">
            |word: light> . |food: belgian waffles> . |word: covered> . |word: with> . |food: strawberries> . |word: and> . |food: whipped cream>
        
        
        -- learn a different set of knowledge:
        -- see cause3.sw
        pattern |node: 1: 1> => |fred>
        pattern |node: 1: 2> => |freddie>
        pattern |node: 1: 3> => |smith>
        pattern |node: 1: 4> => |smithie>
        pattern |node: 1: 5> => |fred> . |smith>
        then |node: 1: *> => |person: Fred Smith>
        
        pattern |node: 2: 1> => |mazza>
        then |node: 2: *> => |person: Mary>
        
        pattern |node: 3: 1> => |hey>
        then |node: 3: *> => |greeting: Hey!>
        
        pattern |node: 4: 1> => |what's>
        pattern |node: 4: 2> => |what> . |is>
        then |node: 4: *> => |question: what is>
        
        pattern |node: 5: 1> => |up>
        then |node: 5: *> => |direction: up>
        
        pattern |node: 6: 1> => |having> . |a> . |baby>
        then |node: 6: *> => |phrase: having a baby>
        
        pattern |node: 7: 1> => |in> . |the> . |family> . |way>
        then |node: 7: *> => |phrase: in the family way>
        
        pattern |node: 8: 1> => |up> . |the> . |duff>
        then |node: 8: *> => |phrase: up the duff>
        
        pattern |node: 9: 1> => |with> . |child>
        then |node: 9: *> => |phrase: with child>
        
        pattern |node: 10: 1> => |phrase: having a baby>
        pattern |node: 10: 2> => |phrase: in the family way>
        pattern |node: 10: 3> => |phrase: up the duff>
        pattern |node: 10: 4> => |phrase: with child>
        then |node: 10: *> => |concept: pregnancy>
        
        -- our 'read' operator:
        read |*> #=> ssplit[" "] replace[",?", ""] to-lower |_self>
        
        -- if 'then' is not defined for a ket, then return itself: 
        then |*> #=> |_self>

        -- now a quick test of our read operator:
        -- yeah, we don't use apply-word this time.
        read |Hey Freddie what's up?>
            |hey> . |freddie> . |what's> . |up>

        -- now 'explain':
        explain[pattern] read |Hey Freddie what's up?>
            |node: 3: 1> . |node: 1: 2> . |node: 4: 1> . |node: 5: 1>
        
        -- now apply the 'then' operator, that maps nodes to concepts:
        then explain[pattern] read |Hey Freddie what's up?>
            |greeting: Hey!> . |person: Fred Smith> . |question: what is> . |direction: up>
        
        -- another example:
        then explain[pattern] read |Hey Mazza, you with child, up the duff, in the family way, having a baby?>
            |greeting: Hey!> . |person: Mary> . |you> . |phrase: with child> . |phrase: up the duff> . |phrase: in the family way> . |phrase: having a baby>
            
        -- then another layer of 'then explain[pattern]':
        then explain[pattern] then explain[pattern] read |Hey Mazza, you with child, up the duff, in the family way, having a baby?>
            |greeting: Hey!> . |person: Mary> . |you> . |concept: pregnancy> . |concept: pregnancy> . |concept: pregnancy> . |concept: pregnancy>
            
        -- further, we could wrap 'then explain[pattern]' into a new operator:
        explain (*) #=> then explain[pattern] |_self>
        explain read |Hey Freddie what is up?>
        explain read |Hey Mazza, you with child, up the duff, in the family way, having a baby?>
        explain^2 read |Hey Mazza, you with child, up the duff, in the family way, having a baby?>

    see also:
        sexp, cause1.sw, cause2.sw, cause3.sw, breakfast-menu.sw, active-buffer
        
    future:
        an example with depth > 2.
"""
def first_explain(one, context, op):
    max_depth = 10  # hard code in a max_depth for now. Maybe later make it infinity.

    def single_step(one, context, op):
        seq = sequence([])
        for x in one:
            # print('x: %s' % x)
            child = x.apply_op(context, op)
            if len(child) == 0:
                child = x
            seq += child
        return seq

    def learn_sexp_op(one, context, op): # one is a ket
        elt = one
        len_one = len(one)
        for k in range(max_depth):
            one = single_step(one, context, op)
            if len(one) == len_one:
                break
            len_one = len(one)
            context.learn('%s-%s' % (op, str(k+1)), elt.label, one)

    # learn all the cause tree's:
    for x in context.relevant_kets(op):
        learn_sexp_op(x, context, op)

    for N in range(1, len(one) + 1):
        for seq in generate_seq_ngrams(one, N):
            print('seq:', str(seq))

    return ket('explain')


def second_explain(one, context, *ops):
    if len(ops) == 1:
        op = ops[0]
        merge_char = ' . '  # currently bugs out if merge_char == ""
    else:
        op, merge_char = ops

    max_depth = 10  # hard code in a max_depth for now. Maybe later make it infinity.
    target = smerge(one, merge_char).label
    len_input = len(one)

    def single_step(one, context, op):
        seq = sequence([])
        for x in one:
            child = x.apply_op(context, op)
            if len(child) == 0:
                child = x
            seq += child
        return seq

    forward_cause = {}

    # learn input elements:
    for x in one:
        if x.label not in forward_cause:
            forward_cause[x.label] = superposition() + x

    # learn all the cause tree's:
    for x in context.relevant_kets(op):
        one = x
        len_one = 1
        for k in range(max_depth):
            one = single_step(one, context, op)
            if len(one) == len_one:
                break
            len_one = len(one)
            if x.label not in forward_cause:
                forward_cause[x.label] = superposition()
            forward_cause[x.label].add_sp(smerge(one, merge_char))

    # find causes:
    def find_next_step(solutions, forward_cause):
        new_solutions = []
        for head_label, target in solutions:
            if len(target) == 0:
                new_solutions.append([head_label, target])
            else:
                for label, sp in forward_cause.items():
                    for x in sp:
                        if target.startswith(x.label):
                            new_solutions.append([head_label + merge_char + label, target[len(x.label) + len(merge_char):]])
        return new_solutions

    # filter to valid first step solutions:
    solutions = []
    for label, sp in forward_cause.items():
        for x in sp:
            if target.startswith(x.label):
                solutions.append([label, target[len(x.label) + len(merge_char):]])
    # print(solutions)

    for _ in range(len_input + 1):
        solutions = find_next_step(solutions, forward_cause)
        # print(solutions)

    if len(merge_char) == 0:
        sorted_solutions = sorted(solutions, key=lambda x: len(x[0]), reverse=False)  # Nope. Doesn't sort correctly.
    else:
        sorted_solutions = sorted(solutions, key=lambda x: len(x[0].split(merge_char)), reverse=False)

    for label, _ in sorted_solutions:
        print(label)
    # return ket(target)

    return ssplit(ket(sorted_solutions[0][0]), merge_char)


def third_explain(one, context, *ops):
    if len(ops) == 1:
        op = ops[0]
        merge_char = ' . '  # currently bugs out if merge_char == ""
    else:
        op, merge_char = ops

    max_depth = 10  # hard code in a max_depth for now. Maybe later make it infinity.
    target = smerge(one, merge_char).label
    len_input = len(one)

    def single_step(one, context, op):
        seq = sequence([])
        for x in one:
            child = x.apply_op(context, op)
            if len(child) == 0:
                child = x
            seq += child
        return seq

    forward_cause = {}
    seen_sequences = {}

    # learn all the cause tree's:
    for x in context.relevant_kets(op):
        elt = x
        len_elt = 1
        for k in range(max_depth):
            elt = single_step(elt, context, op)
            if len(elt) == len_elt and k > 0:
                break
            len_elt = len(elt)
            # print('elt: %s' % elt)
            if x.label not in forward_cause:
                forward_cause[x.label] = superposition()
            seq = smerge(elt, merge_char)
            forward_cause[x.label].add_sp(seq)
            seen_sequences[seq.label] = True  # later convert to set

    # learn input elements:
    for x in one:
        if x.label not in seen_sequences:
            forward_cause[x.label] = superposition() + x

    # print cause tree:
    # for label, sp in forward_cause.items():
    #     print('%s: %s'% (label, sp))

    # find causes:
    def find_next_step(solutions, forward_cause):
        new_solutions = []
        for head_label, target in solutions:
            if len(target) == 0:
                new_solutions.append([head_label, target])
            else:
                for label, sp in forward_cause.items():
                    for x in sp:
                        if target.startswith(x.label):
                            new_solutions.append([head_label + merge_char + label, target[len(x.label) + len(merge_char):]])
        return new_solutions

    # filter to valid first step solutions:
    solutions = []
    for label, sp in forward_cause.items():
        for x in sp:
            if target.startswith(x.label):
                solutions.append([label, target[len(x.label) + len(merge_char):]])
    # print(solutions)

    for _ in range(len_input + 1):
        solutions = find_next_step(solutions, forward_cause)
        # print(solutions)

    if len(merge_char) == 0:
        sorted_solutions = sorted(solutions, key=lambda x: len(x[0]), reverse=False)  # Nope. Doesn't sort correctly.
    else:
        sorted_solutions = sorted(solutions, key=lambda x: len(x[0].split(merge_char)), reverse=False)

    for label, _ in sorted_solutions:
        print(label)
    # return ket(target)

    return ssplit(ket(sorted_solutions[0][0]), merge_char)


# set invoke method:
compound_table['sngrams'] = ['apply_seq_fn', 'seq_ngrams', '']
# set usage info:
function_operators_usage['sngrams'] = """
    description:
        create sequence ngrams

    examples:

    see also:
        letter-ngrams, word-ngrams
"""
def generate_seq_ngrams(one, N):
    for i in range(len(one)- N + 1):
        data = one.data[i:i + N]
        seq = sequence([])
        seq.data = data
        yield seq

def seq_ngrams(one, N):
    for seq in generate_seq_ngrams(one, N):
        print('seq:', str(seq))
    return ket('sngrams')


# 28/7/2014:
# Let's finally implement console train of thought.
# train-of-thought[n] some-superposition
# eg: train-of-thought[20] |colour: red>
# First up, I want to try it on this data set: http://semantic-db.org/next-gen/train_of_thought.py
# OK. In early testing seems to work just fine.
#
# where n is an int.
#
# set invoke method:
compound_table['train-of-thought'] = ['apply_sp_fn', 'console_train_of_thought', 'context']
# set usage info:
function_operators_usage['train-of-thought'] = """
    description:
        train-of-thought[n] sp
        the train-of-thought function
        given a seed ket, randomly walk through operator links to other kets
        works best with a large, well connected network
        
        The pseudo-code for this function is:

        train-of-thought[n] (*) #=>
            |X> => pick-elt |_self>
            |train> .=> "" |X>
            repeat[n]:
                |X> => pick-elt apply(pick-elt supported-ops "" |X>, ""|X>)
                print "" |X>
                |train> .=> "" |X>
            return "" |train>

    examples:
        load fred-sam-friends.sw
        find-inverse[friends]
        train-of-thought[10] |Fred>
            context: global context
            one: |Fred>
            n: 10
            |X>: |Fred>
            ------------
            |Mary>
            |Fred>
            |Rob>
            |Fred>
            |Jack>
            |Fred>
            |Charlie>
            |Sam>
            |Frank>
            |Sam>
            |Fred> . |Mary> . |Fred> . |Rob> . |Fred> . |Jack> . |Fred> . |Charlie> . |Sam> . |Frank> . |Sam>

        load family.sw
        find-inverse[age]
        train-of-thought[10] |sara>
            context: sw console
            one: |sara>
            n: 10
            |X>: |sara>
            ------------
            |sam>
            |56>
            |sam>
            |trude>
            |sally>
            |tom>
            |40>
            |tom>
            |mike>
            |60>
            |sara> . |sam> . |56> . |sam> . |trude> . |sally> . |tom> . |40> . |tom> . |mike> . |60>

    see also:

"""
def console_train_of_thought(one, context, n):
    try:
        n = int(n)
    except:
        return ket()

    print("context:", context.name)
    print("one:", one)
    print("n:", n)
    X = one.pick_elt()                                                          # |X> => pick-elt |_self>
    train = sequence(X)                                                         # |train> .=> "" |X>
    print("|X>:", X)
    print('------------')

    for k in range(n):
        op = X.apply_op(context, "supported-ops").pick_elt().to_sp().label[4:]  # |op> => pick-elt supported-ops |X>
        X = X.apply_op(context, op).pick_elt().to_sp()                          # |X> => pick-elt apply(|op>,|X>)
        train += X                                                              # |train> .=> "" |X>
        print(X)                                                                # print "" |X>
    return train  # return a record of the train-of-thought


# set invoke method:
fn_table['shout'] = 'shout'
# set usage info:
function_operators_usage['shout'] = """
    description:
        shout ket
        mostly just a test function. Print the given kets in upper-case

    examples:
        shout |fish soup>
            FISH SOUP
            |FISH SOUP>

    see also:
        print, to-upper, to-lower
"""
def shout(one):
    string = (one if type(one) == str else one.to_sp().label).upper()
    print(string)
    return ket(string)

# set invoke method:
fn_table['print'] = 'print_ket'
# set usage info:
function_operators_usage['print'] = """
    description:
        print ket
        print the given kets 

    examples:
        print |fish soup>
            fish soup
            |fish soup>

    see also:
        shout, to-upper, to-lower 
"""
def print_ket(one):
    string = (one if type(one) == str else one.to_ket().label)
    print(string)
    return ket(string)



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
            # print("x*y", x, "*", y)
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
# set invoke method:
whitelist_table_3['algebra'] = 'algebra'
# set usage info:
sequence_functions_usage['algebra'] = """
    description:
        algebra(sp, ket, sp)
        a minimalistic implementation of algebra over kets
        
    examples:
        algebra(|a>, |+>, |b>)
            |a> + |b>

        algebra(3|a>, |*>, 5|b>)
            15|a*b>

        algebra(|a> + |b>, |^>, |3>)
            |a*a*a> + 3|a*a*b> + 3|a*b*b> + |b*b*b>

    see also:
        non-Abelian-algebra, arithmetic, display-algebra
"""
def algebra(input_seq, one, operator, two, Abelian=True):
    op_label = operator if type(operator) == str else operator.to_sp().label
    null, op = extract_category_value(op_label)
    one = one.to_sp()  # cast objects to superpositions for now, since we don't know how to handle sequences!
    two = two.to_sp()

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
# set invoke method:
whitelist_table_3['non-Abelian-algebra'] = 'non_Abelian_algebra'
# set usage info:
sequence_functions_usage['non-Abelian-algebra'] = """
    description:
        non-Abelian-algebra(sp, ket, sp)
        a minimalistic implementation of non Abelian algebra over kets

    examples:
        non-Abelian-algebra(|a>, |+>, |b>)
            |a> + |b>

        non-Abelian-algebra(3|a>, |*>, 5|b>)
            15|a*b>

        non-Abelian-algebra(2|a> + 3|b>, |*>, 5|c> + 7|d>)
            10|a*c> + 14|a*d> + 15|b*c> + 21|b*d> 

        non-Abelian-algebra(|a> + |b>, |^>, |3>)
            |a*a*a> + |a*a*b> + |a*b*a> + |a*b*b> + |b*a*a> + |b*a*b> + |b*b*a> + |b*b*b>

    see also:
        algebra, arithmetic
"""
def non_Abelian_algebra(input_seq, one, operator, two):
    return algebra(input_seq, one, operator, two, Abelian=False)


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


# set invoke method:
sp_fn_table['display-algebra'] = 'display_algebra'
# set usage info:
function_operators_usage['display-algebra'] = """
    description:
        display-algebra sp
        display algebra in slightly tidier form

    examples:
        display-algebra (3|x*x> + 2|y> + |z> + 13| >)
            |3*x*x + 2*y + z + 13>
        
    see also:
         algebra
"""
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



# set invoke method:
whitelist_table_2['to-base'] = 'decimal_to_base'
# set usage info:
sequence_functions_usage['to-base'] = """
    description:
        to-base(ket, ket)
        convert a decimal number to the given base
        
    examples:
        to-base(|10>, |2>)
            0|1> + |2> + 0|4> + |8>

        to-base(|123454678>, |1000>)
            678|1> + 454|1000> + 123|1000000>

        push-float to-base(|123454678>, |1000>)
            |1: 678> + |1000: 454> + |1000000: 123>
            
    see also:
        is-prime, prime-factors
"""
def decimal_to_base(input_seq, number, base):
    r = int(category_number_to_number(number.to_sp()).value)
    b = int(category_number_to_number(base.to_sp()).value)
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




# convert the labels in a superposition to a pretty-print vector
def old_sp_to_vect(one):
    max_len = 0
    for x in one.data:
        max_len = max(max_len, len(x.label))
    for x in one.data:
        print("[ " + x.label.ljust(max_len) + " ]")


def sp_to_vect(one):
    # if one.count() <= 1:
    #     vect = one.the_label()
    # else:
    vect = "\n".join(x.label for x in one)
    return paste_columns([vect], '[ ', '', ' ]')


def sp_to_list(one):  # what happens if one is a ket? Fixed, I think.
    # if one.count() <= 1:
    #     return one.the_label()
    return "\n".join(x.label for x in one)


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
    # if type(one) is ket:
    #     return coeff_to_str(one.value)
    return "\n".join(coeff_to_str(x.value) for x in one)


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
def single_matrix_unmerged(one, context, op):
    def sp_coeffs_to_list(one):  # what happens if one is a ket? Fixed, I think.
        return "\n".join(coeff_to_str(x.value) for x in one)

    one = one.to_sp().apply_sigmoid(set_to, 1)
    two = superposition()  # two is the list of kets that will be on the left hand side.
    for elt in one:
        sp = elt.apply_op(context, op).to_sp()  # It would be nice to have a version that handles seq rules too!
        two = union(two, sp)
    two = two.ket_sort().multiply(0)  # merged two, and empty into the same thing.
    matrix_columns = [sp_coeffs_to_list((elt.apply_op(context, op).to_sp() + two).ket_sort()) for elt in one]

    M = paste_columns(matrix_columns, '[  ', '  ', '  ]')  # M is the matrix
    return two, M


# uses x.merged_apply_op(context,ops) instead of x.apply_op(context,op)
def single_matrix_merged(one, context, ops):
    def sp_coeffs_to_list(one):  # what happens if one is a ket? Fixed, I think.
        return "\n".join(coeff_to_str(x.value) for x in one)

    def merged_apply_op(one, context, ops):
        r = one
        for op in ops[::-1]:
            r = r.apply_op(context, op).to_sp()
        return r

    one = one.to_sp().apply_sigmoid(set_to, 1)
    two = superposition()  # two is the list of kets that will be on the left hand side.
    for elt in one:
        sp = merged_apply_op(elt, context, ops)
        two = union(two, sp)
    two = two.ket_sort().multiply(0)
    matrix_columns = [sp_coeffs_to_list((merged_apply_op(elt, context, ops) + two).ket_sort()) for elt in one]
    M = paste_columns(matrix_columns, '[  ', '  ', '  ]')  # M is the matrix
    return two, M


# second version of code to spit out a matrix:
# seems to be correct.
# set invoke method:
compound_table['merged-matrix'] = ['apply_sp_fn', 'matrix', 'context']
# set usage info:
function_operators_usage['merged-matrix'] = """
    description:
        merged-matrix[opn, ..., op2, op1]
        merged-matrix[opn, ..., op2, op1] sp
        merge the operators into a single merged matrix
        
    examples:
        load matrices.sw
        merged-matrix[M2,M1]
            [ z1 ] = [  0   42  6   6  36  24  6   ] [ x1 ]
            [ z2 ]   [  9   32  14  2  24  32  8   ] [ x2 ]
            [ z3 ]   [  12  73  23  7  58  60  15  ] [ x3 ]
            [ z4 ]   [  0   63  9   9  54  36  9   ] [ x4 ]
            [ z5 ]   [  3   41  9   5  34  28  7   ] [ x5 ]
                                                     [ x6 ]
                                                     [ x7 ]

        -- specify the input kets of interest, here |x1>, |x2>, |x3>:
        merged-matrix[M2, M1] split |x1 x2 x3>
            [ z1 ] = [  0   42  6   ] [ x1 ]
            [ z2 ]   [  9   32  14  ] [ x2 ]
            [ z3 ]   [  12  73  23  ] [ x3 ]
            [ z4 ]   [  0   63  9   ]
            [ z5 ]   [  3   41  9   ]


    see also:
        matrix, naked-matrix
"""
def matrix(one, context, *ops):
    def sp_to_vect(one):
        vect = "\n".join(x.label for x in one)
        return paste_columns([vect], '[ ', '', ' ]')

    if len(one) == 0:
        one = context.relevant_kets(ops[-1]).ket_sort()  # one is the list of kets that will be on the right hand side.
        if len(one) == 0:
            return ket()

    two, M = single_matrix_merged(one, context, ops)
    x = sp_to_vect(one)
    y = sp_to_vect(two)

    matrix = paste_columns([y, '=', M, x])
    print(matrix)
    return ket("matrix")


# set invoke method:
compound_table['naked-matrix'] = ['apply_sp_fn', 'naked_matrix', 'context']
# set usage info:
function_operators_usage['naked-matrix'] = """
    description:
        naked-matrix[opn, ..., op2, op1]
        naked-matrix[opn, ..., op2, op1] sp
        display a single merged adjacency matrix, without the input and output vectors

    examples:
        load matrices.sw
        naked-matrix[M2,M1]
            [  0   42  6   6  36  24  6   ]
            [  9   32  14  2  24  32  8   ]
            [  12  73  23  7  58  60  15  ]
            [  0   63  9   9  54  36  9   ]
            [  3   41  9   5  34  28  7   ]

        -- specify the input kets of interest, here |x1>, |x2>, |x3>:
        naked-matrix[M2,M1] split |x1 x2 x3>
            [  0   42  6   ]
            [  9   32  14  ]
            [  12  73  23  ]
            [  0   63  9   ]
            [  3   41  9   ]


    see also:
        matrix, merged-matrix
"""
def naked_matrix(one, context, *ops):
    if len(one) == 0:
        one = context.relevant_kets(ops[-1]).ket_sort()  # one is the list of kets that will be on the right hand side.
        if len(one) == 0:
            return ket()

    two, M = single_matrix_merged(one, context, ops)
    print(M)
    return ket("matrix")


# third version.
# this one I want to handle multiple ops at once, and then chain the matrices.
# eg: matrix[M2,M1]
# or: matrix[friends,friends]  -- ie, matrix of second-order friends
# set invoke method:
compound_table['matrix'] = ['apply_sp_fn', 'multi_matrix', 'context']
# set usage info:
function_operators_usage['matrix'] = """
    description:
        matrix[opn, ..., op2, op1]
        matrix[opn, ..., op2, op1] sp
        maps operators to adjacency matrices

    examples:
        -- learn some knowledge:
        -- load matrices.sw
        M1 |x1> => 3|y2>
        M1 |x2> => 7|y1> + 6|y2>
        M1 |x3> => |y1> + 4|y2>
        M1 |x4> => |y1>
        M1 |x5> => 6|y1> + 4|y2>
        M1 |x6> => 4|y1> + 8|y2>
        M1 |x7> => |y1> + 2|y2>
        
        M2 |y1> => 6|z1> + 2|z2> + 7|z3> + 9|z4> + 5|z5>
        M2 |y2> => 3|z2> + 4|z3> + |z5>

    
        -- display corresponding matrices:
        matrix[M1]
            [ y1 ] = [  0  7  1  1  6  4  1  ] [ x1 ]
            [ y2 ]   [  3  6  4  0  4  8  2  ] [ x2 ]
                                               [ x3 ]
                                               [ x4 ]
                                               [ x5 ]
                                               [ x6 ]
                                               [ x7 ]
        
        matrix[M2]
            [ z1 ] = [  6  0  ] [ y1 ]
            [ z2 ]   [  2  3  ] [ y2 ]
            [ z3 ]   [  7  4  ]
            [ z4 ]   [  9  0  ]
            [ z5 ]   [  5  1  ]
        
        matrix[M2, M1]
            [ z1 ] = [  6  0  ] [  0  7  1  1  6  4  1  ] [ x1 ]
            [ z2 ]   [  2  3  ] [  3  6  4  0  4  8  2  ] [ x2 ]
            [ z3 ]   [  7  4  ]                           [ x3 ]
            [ z4 ]   [  9  0  ]                           [ x4 ]
            [ z5 ]   [  5  1  ]                           [ x5 ]
                                                          [ x6 ]
                                                          [ x7 ]
        
        matrix[M1, M2]
            [  ] = [            ] [  6  0  ] [ y1 ]
                                  [  2  3  ] [ y2 ]
                                  [  7  4  ]
                                  [  9  0  ]
                                  [  5  1  ]

        -- only display matrix for desired inputs:
        matrix[M1] split |x1 x3 x5 x7>
            [ y1 ] = [  0  1  6  1  ] [ x1 ]
            [ y2 ]   [  3  4  4  2  ] [ x3 ]
                                      [ x5 ]
                                      [ x7 ]

    see also:
        merged-matrix, naked-matrix
"""
def multi_matrix(one, context, *ops):
    def sp_to_vect(one):
        vect = "\n".join(x.label for x in one)
        return paste_columns([vect], '[ ', '', ' ]')

    ops = ops[::-1]
    # print("ops:", ops)

    if len(one) == 0:
        one = context.relevant_kets(ops[0]).ket_sort()  # one is the list of kets that will be on the right hand side.
        if len(one) == 0:
            return ket()

    two, M = single_matrix_unmerged(one, context, ops[0])
    matrices = [M]
    for op in ops[1:]:
        two, M = single_matrix_unmerged(two, context, op)
        matrices.append(M)
    x = sp_to_vect(one)
    y = sp_to_vect(two)
    line = [y, '='] + matrices[::-1] + [x]
    matrix = paste_columns(line)
    print(matrix)

    # code to save the matrix (useful for big ones that are too hard to cut and paste from the console)
    print("saving to: saved-matrix.txt")
    file = open("saved-matrix.txt", 'w')
    file.write("sa: matrix[" + ",".join(ops[::-1]) + "]\n")
    file.write(matrix)
    file.close()

    return ket("matrix")



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

    two, M = single_matrix_merged(one, context, ops)

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

    two, M = single_matrix_merged(one, context, ops)
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
    two, M = single_matrix_merged(one, context, ops)
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

    two, M = single_matrix_merged(one, context, ops)
    x = sp_to_vect(one)
    y = sp_to_vect(two)
    matrix = paste_columns([y, '=', M, x])
    print(matrix)
    return ket("matrix")


# 7/8/2014, let's write a sp-propagate function.
# Takes an initial superposition, then takes an operator, and applies it repeatedly.
# Then display this all as a matrix, maybe something we can plot in gnuplot.
# First need this:
def sp_coeffs_to_column(one):
    def to_str(n):
        if n == 0:
            return "0"
            # return " "
        else:
            return str("%.2f" % n)
            # return "1"
    return "\n".join(to_str(x.value) for x in one)

# usage: sp-propagate[op,k] "" |list>
# op is an operator, k is the number of iterations.
# set invoke method:
compound_table['propagate'] = ['apply_sp_fn', 'sp_propagate', 'context']
# set usage info:
function_operators_usage['propagate'] = """
    description:
        the propagate function
        takes an initial superposition and an operator, and applies it repeatedly.

    examples:

    see also:

    TODO:
        work out what this is trying to do!!
"""
def sp_propagate(one, context, *parameters):
    def sp_coeffs_to_column(one):
        return "\n".join(float_to_int(x.value) for x in one)
    try:
        op, k = parameters
        k = int(k)
    except:
        return ket()

    matrix = []
    r = one
    empty = r.apply_sigmoid(set_to, 0)
    for idx in range(k):
        matrix.append(sp_coeffs_to_column((r + empty).ket_sort()))  # making use of adding an sp of all 0's does not change the meaning
        r = r.apply_op(context, op).to_sp()
    print(paste_columns(matrix, '', ' ', ''))
    return ket("matrix")





# day of the week function:
# day-of-the-week |date: 2014/06/3> => |day: Tuesday>
# Code from here: http://stackoverflow.com/questions/9847213/which-day-of-week-given-a-date-python
# Heh. Python makes this super easy!
# set invoke method:
fn_table['day-of-the-week'] = 'day_of_the_week'
# set usage info:
function_operators_usage['day-of-the-week'] = """
    description:
        day-of-the-week ket
        convert the date into the day of the week
        date must be in year/month/day format

    examples:
        day-of-the-week |date: 2018/7/10>
            |day: Tuesday>

    see also:
         current-date, current-time
"""
def day_of_the_week(one):
    cat, value = extract_category_value(one.label)
    if cat.split(': ')[-1] != "date":
        return ket()

    # 5/2/2015: tidy it up:
    try:
        year, month, day = (int(x) for x in value.split('/'))
    except:
        try:
            year, month, day = (int(x) for x in value.split('-'))
        except:
            return ket()
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    the_day = day_list[datetime.date(year, month, day).weekday()]
    return ket("day: " + the_day)


# set invoke method:
fn_table['current-date'] = 'current_date'
# set usage info:
function_operators_usage['current-date'] = """
    description:
        current-date
        return today's date

    examples:
        current-date
            |date: 2018-07-10>

    see also:
        current-time, day-of-the-week
"""
def current_date(one):
    return ket("date: " + str(datetime.date.today()))


# buggy! Not my local time. Not sure how to fix yet!


# set invoke method:
fn_table['current-time'] = 'current_time'
# set usage info:
function_operators_usage['current-time'] = """
    description:
        current-time
        return the current time

    examples:
        current-time
            |Tue Jul 10 05:06:21 2018>

    see also:
        current-date, day-of-the-week
    
    TODO:
        fix: currently it gets the local time-zone wrong
"""
def current_time(one):
    #  return ket("time: " + str(datetime.datetime.now().time()))
    #  return ket("time: " + str(datetime.datetime.now().strftime('%H:%M:%S')))
    # return ket("time: " + strftime('%H:%M:%S', gmtime()))
    return ket(ctime())


# set invoke method:
compound_table['sleep'] = ['apply_seq_fn', 'bko_sleep', '']
# set usage info:
function_operators_usage['sleep'] = """
    description:
        sleep[n] seq 
        sleeps for n seconds
        n is either an int or a float
        returns the input sequence, so it can be easily chained

    examples:
        sleep[3.14]
        
        sleep[2] (|a> + |b> . |c>)
            |a> + |b> . |c>

    see also:

"""
def bko_sleep(one, time):
    sleep(float(time))
    return one


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
# set invoke method:
context_whitelist_table_2['clone'] = 'clone_ket'
# set usage info:
sequence_functions_usage['clone'] = """
    description:
        clone(sp, sp)
        clone(|x>, |y>), copies rules from |x> and applies them to |y>

    examples:
        -- set the context:
        context clone example
        
        -- learn some knowledge:
        age |Sarah> => |31>
        mother |Sarah> => |Jane>
        father |Sarah> => |Rob>
        
        -- clone |Sarah> to |Emma> (eg, they are twin sisters)
        clone(|Sarah>, |Emma>)
        
        -- show what we now know:
        dump
            ----------------------------------------
             |context> => |context: clone example>
            previous |context> => |context: global context>
            
            age |Sarah> => |31>
            mother |Sarah> => |Jane>
            father |Sarah> => |Rob>
            
            age |Emma> => |31>
            mother |Emma> => |Jane>
            father |Emma> => |Rob>
            ----------------------------------------

    see also:
        inherit
        
    TODO:
        test it works with superpositions, as claimed
"""
def clone_ket(input_seq, context, one, two):
    one = one.to_sp()
    two = two.to_sp()
    for elt in one:
        for op_ket in context.recall("supported-ops", elt):
            op = op_ket.label[4:]
            rule = context.recall(op, elt)
            for x in two:
                context.learn(op, x, rule)
    return ket('clone')



# set invoke method:
fn_table['expand-hierarchy'] = 'expand_hierarchy'
# set usage info:
function_operators_usage['expand-hierarchy'] = """
    description:
        expand-hierarchy ket
        expand the category hierarchy
        
    examples:
        expand-hierarchy |a: b: c: d>
            |a> + |a: b> + |a: b: c> + |a: b: c: d>
        
        expand-hierarchy |a: b: c: d: e: f>
            |a> + |a: b> + |a: b: c> + |a: b: c: d> + |a: b: c: d: e> + |a: b: c: d: e: f>
        
        expand-hierarchy |a: b: c: x: y>
            |a> + |a: b> + |a: b: c> + |a: b: c: x> + |a: b: c: x: y>
        
        intersection(expand-hierarchy |a: b: c: d: e: f>, expand-hierarchy |a: b: c: x: y>)
            |a> + |a: b> + |a: b: c>
        
        expand-hierarchy |animal: mammal: dog>
            |animal> + |animal: mammal> + |animal: mammal: dog>
       
    see also:
        extract-category, extract-value, category-depth, inherit
"""
# assumes "one" is a ket.
def expand_hierarchy(one):
    r = superposition()
    L = []
    for x in one.label.split(": "):
        L.append(x)
        r += ket(": ".join(L))
    return r.multiply(one.value)


# set invoke method:
fn_table['category-depth'] = 'category_depth'
# set usage info:
function_operators_usage['category-depth'] = """
    description:
        category-depth ket
        return the depth of the categories

    examples:
        category-depth |>
            |number: 0>
            
        category-depth |dog>
            |number: 1>
        
        category-depth |animal: mammal: dog>
            |number: 3>

    see also:
        extract-category, extract-value, expand-hierarchy    
"""
def category_depth(one):
    if len(one) == 0:
        return ket("number: 0")
    return ket("number: " + str(one.label.count(": ") + 1))


# ket-length
# eg: ket-length |abcde> == |number: 5>
#
# set invoke method:
fn_table['ket-length'] = 'ket_length'
# set usage info:
function_operators_usage['ket-length'] = """
    description:
        ket-length ket
        return the length of the given ket

    examples:
        ket-length |>
            |number: 0>
    
        ket-length |abcde>
            |number: 5>

    see also:
        category-depth
"""
def ket_length(one):
    return ket("number: " + str(len(one.label)))


# set invoke method:
fn_table['push-float'] = 'push_float'
# set usage info:
function_operators_usage['push-float'] = """
    description:
        push-float ket
        pushes the float coefficient to a category

    examples:
        -- 3 times don't know equals don't know:
        push-float 3|>
            |>
        
        -- NB: the space in the ket:
        push-float 3| >
            |3>

        push-float 3|x>
            |x: 3>
        
        push-float 3.2|x: y: z>
            |x: y: z: 3.2>
        
    see also:
        pop-float, to-value, to-category
"""
def push_float(one):
    if len(one) == 0:
        return ket()
    value = one.value
    label = one.label.rstrip()
    if float(value).is_integer():
        value = str(int(value))
    else:
        value = str(value)
    if label == "":
        return ket(value)
    return ket(label + ": " + value)


# set invoke method:
fn_table['pop-float'] = 'pop_float'
# set usage info:
function_operators_usage['pop-float'] = """
    description:
        pop-float ket
        pops the trailing float in the given ket to the coefficient
        if the starting ket has a coefficient then multiply it by this value
        if the trailing value is not a float, then leave the ket unchanged

    examples:
        pop-float |3.2>
            3.2| >
        
        -- coefficient of 5, so multiply by 7:
        pop-float 5|7>
            35| >
        
        pop-float |x: 2>
            2|x>
            
        -- again, multiply the coefficient by the value
        pop-float 5.1|x: y: 2>
            10.2|x: y>
            
        -- y is not a float, so leave |x: y> unchanged
        pop-float |x: y>
            |x: y>

    see also:
        push-float, to-value, to-category
"""
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



# 24/3/2015:
# find-unique[names]
#
# unique-names |male name>
# unique-names |female name>
# unique-names |last name>
#
# yup. seems to work! And is fast! 4 days estimated for the names.sw data, down to 2 seconds, 753 milliseconds
# set invoke method:
compound_table['find-unique'] = ['apply_naked_fn', 'find_unique_multi', 'context']
# set usage info:
function_operators_usage['find-unique'] = """
    description:
        find-unique[op1, op2, ... , opn]
        learn the kets that are unique with respect to the given operator(s)
        
    examples:
        -- load our data:
        load fred-sam-friends.sw
        
        -- show the common friends between Fred and Sam:
        -- (these are the ones that are not unique)
        common[friends] split |Fred Sam>
            |Jack> + |Emma> + |Charlie>

        -- find the unique friends for Fred and Sam:
        find-unique[friends]
        
        -- display the results:
        dump
            ----------------------------------------
             |context> => |context: friends>
            previous |context> => |context: global context>
            
            friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
            unique-friends |Fred> => |Harry> + |Ed> + |Mary> + |Rob> + |Patrick>
            
            friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Rober> + |Frank> + |Julie>
            unique-friends |Sam> => |George> + |Rober> + |Frank> + |Julie>
            ----------------------------------------

    see also:
        find-inverse, common
"""
def find_unique(context, op):
    sp_dict = {}
    for x in context.relevant_kets(op):
        sp_dict[x.label] = x.apply_op(context, op).to_sp()

    for your_label, your_sp in sp_dict.items():
        other_dict = {}
        for label, sp in sp_dict.items():
            if label != your_label:
                for x in sp:
                    other_dict[x.label] = True
        r = superposition()
        for x in your_sp:
            if x.label not in other_dict:
                r.add_sp(x)
        context.learn('unique-' + op, your_label, r)

    return ket('find-unique')

def find_unique_multi(context, *ops):
    for op in ops:
        find_unique(context, op)
    return ket('find-unique')



# set invoke method:
compound_table['find-inverse'] = ['apply_naked_fn', 'find_inverse', 'context']
# set usage info:
function_operators_usage['find-inverse'] = """
    description:
        find-inverse[op1, op2, ... , opn]
        learn the set of inverses for the given operator(s)       

    examples:
        load fred-sam-friends.sw
        find-inverse[friends]
        dump
            ----------------------------------------
             |context> => |context: friends>
            previous |context> => |context: global context>
            
            friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
            friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Rober> + |Frank> + |Julie>
            
            inverse-friends |Jack> => |Fred> + |Sam>
            inverse-friends |Harry> => |Fred>
            inverse-friends |Ed> => |Fred>
            inverse-friends |Mary> => |Fred>
            inverse-friends |Rob> => |Fred>
            inverse-friends |Patrick> => |Fred>
            inverse-friends |Emma> => |Fred> + |Sam>
            inverse-friends |Charlie> => |Fred> + |Sam>
            inverse-friends |George> => |Sam>
            inverse-friends |Rober> => |Sam>
            inverse-friends |Frank> => |Sam>
            inverse-friends |Julie> => |Sam>
            ----------------------------------------
        
    see also:
        find-unique
"""
def find_inverse(context, *ops):
    for op in ops:
        context.create_inverse_op(op)
    return ket('find-inverse')


# set invoke method:
sp_fn_table['rank'] = 'rank'
# set usage info:
function_operators_usage['rank'] = """
    description:
        rank sp
        apply position in superposition to coefficient
        ie, rank them

    examples:
        rank (|a> + |b> + |c>)
            |a> + 2|b> + 3|c>
        
        rank split |a b c d e f>
            |a> + 2|b> + 3|c> + 4|d> + 5|e> + 6|f>
            
        -- NB: designed for superpositions, not sequences
        -- for sequences, you need srank
        -- eg, this doesn't do what you think it might:
        rank ssplit |abcdefg>
            |a> . |b> . |c> . |d> . |e> . |f> . |g>

        -- instead need:
        srank ssplit |abcdefg>
            |a> . 2|b> . 3|c> . 4|d> . 5|e> . 6|f> . 7|g>

    see also:
        srank
"""
# one is a superposition
def rank(one):
    r = superposition()
    for k, (label, value) in enumerate(one.items()):
        r.add(label, k + 1)
    return r


# set invoke method:
seq_fn_table['srank'] = 'srank'
# set usage info:
function_operators_usage['srank'] = """
    description:
        srank seq
        apply position in sequence to coefficient
        ie, rank them

    examples:
        srank ssplit |abcdefg>
            |a> . 2|b> . 3|c> . 4|d> . 5|e> . 6|f> . 7|g>

        -- works similarly for sequences of superpositions:
        srank (|a> + |b> . |c> . |d> + |e> + |f> . |g> . |h> + |i> + |j> + |k>)
            |a> + |b> . 2|c> . 3|d> + 3|e> + 3|f> . 4|g> . 5|h> + 5|i> + 5|j> + 5|k>

        long-display srank (|a> + |b> . |c> . |d> + |e> + |f> . |g> . |h> + |i> + |j> + |k>)
            seq |0> => |a> + |b>
            seq |1> => 2|c>
            seq |2> => 3|d> + 3|e> + 3|f>
            seq |3> => 4|g>
            seq |4> => 5|h> + 5|i> + 5|j> + 5|k>
            |a> + |b> . 2|c> . 3|d> + 3|e> + 3|f> . 4|g> . 5|h> + 5|i> + 5|j> + 5|k>


        -- an approximate implementation using op-zip:
        -- define our multiply operators:
        m1 |*> #=> |_self>
        m2 |*> #=> 2|_self>
        m3 |*> #=> 3|_self>
        m4 |*> #=> 4|_self>
        m5 |*> #=> 5|_self>

        -- define our operator sequence:
        op |seq> => |op: m1> . |op: m2> . |op: m3> . |op: m4> . |op: m5>

        -- define our version of srank:
        my-srank (*) #=> op-zip(op |seq>, |_self>)

        -- try it out:
        -- NB: |f> is ignored, since 'op |seq>' is only length 5
        my-srank (|a> . |b> . |c> . |d> . |e> . |f>)
            |a> . 2|b> . 3|c> . 4|d> . 5|e>

        long-display my-srank (|a> + |b> . |c> . |d> + |e> + |f> . |g> . |h> + |i> + |j> + |k>)
            seq |0> => |a> + |b>
            seq |1> => 2|c>
            seq |2> => 3|d> + 3|e> + 3|f>
            seq |3> => 4|g>
            seq |4> => 5|h> + 5|i> + 5|j> + 5|k>
            |a> + |b> . 2|c> . 3|d> + 3|e> + 3|f> . 4|g> . 5|h> + 5|i> + 5|j> + 5|k>

    see also:
        rank, op-zip
"""
# one is a sequence
def srank(one):
    seq = sequence([])
    for k, sp in enumerate(one):
        seq += sp.multiply(k + 1)
    return seq


# 14/4/2015:
# starts-with |a: b: > returns |a: b: c>, |a: b: c: d> and so on.
# eg, we can now do: starts-with |person: Fred > to list all people with first name Fred.
#
# set invoke method:
ket_context_table['starts-with'] = 'starts_with'
# set usage info:
function_operators_usage['starts-with'] = """
    description:
        starts-with ket
        returns all relevant kets that start with the given prefix

    examples:
        -- learn some knowledge:
        age |person: Fred Smith> => |47>
        mother |person: Fred Jones> => |Mary>
        age |person: Sam Hughes> => |49>

        -- now ask some questions:
        starts-with |>
            |context> + |person: Fred Smith> + |person: Fred Jones> + |person: Sam Hughes>

        starts-with |person: >
            |person: Fred Smith> + |person: Fred Jones> + |person: Sam Hughes>

        starts-with |person: Fred >
            |person: Fred Smith> + |person: Fred Jones>

    see also:
        rel-kets, guess-ket
"""
# e is a ket
def starts_with(e, context):
    return context.starts_with(e)



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


def make_ngrams(one, sizes, ngram_type):
    text = one.label if type(one) is ket else one
    if text.startswith('text: '):
        text = text[6:]

    if ngram_type == "word":
        words = [w for w in re.split('[^a-z0-9_\']', text.lower().replace('\\n', ' ')) if w]  # do we want .lower() in there?
        create_ngram_fn = create_word_n_grams

    elif ngram_type == "letter":
        words = list(text)
        create_ngram_fn = create_letter_n_grams
    else:
        return ket()

    result = superposition()
    for k in sizes:
        for w in create_ngram_fn(words, int(k)):
            result.add(w)
    return result.multiply(one.value)


# set invoke method:
compound_table['word-ngrams'] = ['apply_fn', 'word_ngrams', '']
# set usage info:
function_operators_usage['word-ngrams'] = """
    description:
        word-ngrams[k1, k2, ..., kn] ket
        create word ngrams, of specified sizes
        the result is multiplied by the coefficient of the ket
        
    examples:
        word-ngrams[1] |happy to see you>
            |happy> + |to> + |see> + |you>
            
        -- same thing again, but this time the ket has coefficient of 5.1:
        word-ngrams[1] 5.1|happy to see you>
            5.1|happy> + 5.1|to> + 5.1|see> + 5.1|you>

        word-ngrams[1,2,3] |happy to see you>
            |happy> + |to> + |see> + |you> + |happy to> + |to see> + |see you> + |happy to see> + |to see you>

    see also:
        letter-ngrams
"""
def word_ngrams(one, *parameters):
    return make_ngrams(one, parameters, 'word')


# set invoke method:
compound_table['letter-ngrams'] = ['apply_fn', 'letter_ngrams', '']
# set usage info:
function_operators_usage['letter-ngrams'] = """
    description:
        letter-ngrams[k1, k2, ..., kn] ket
        create letter ngrams, of specified sizes
        the result is multiplied by the coefficient of the ket

    examples:
        letter-ngrams[1] |fish>
            |f> + |i> + |s> + |h>

        -- same thing again, but this time the ket has coefficient of 3.2:
        letter-ngrams[1] 3.2|fish>
            3.2|f> + 3.2|i> + 3.2|s> + 3.2|h>

        letter-ngrams[1] |happy>
            |h> + |a> + 2|p> + |y>

        letter-ngrams[1,2,3] |happy>
            |h> + |a> + 2|p> + |y> + |ha> + |ap> + |pp> + |py> + |hap> + |app> + |ppy>

    see also:
        word-ngrams
"""
def letter_ngrams(one, *parameters):
    return make_ngrams(one, parameters, 'letter')




# set invoke method:
compound_table['ket-hash'] = ['apply_fn', 'ket_hash', '']
# set usage info:
function_operators_usage['ket-hash'] = """
    description:
        ket-hash[n] ket
        md5 hash the given ket, but only keep n characters

    examples:
        ket-hash[4] |fish>
            |b309>
        
        ket-hash[10] |soup>
            |ec72b9a612>

    see also:

"""
# one is a ket
def ket_hash(one, size):
    try:
        size = int(size)
    except:
        return ket()
    our_hash = hashlib.md5(one.label.encode('utf-8')).hexdigest()[-size:]
    return ket(our_hash, one.value)




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


# set invoke method:
compound_table['bar-chart'] = ['apply_sp_fn', 'bar_chart', '']
# set usage info:
function_operators_usage['bar-chart'] = """
    description:
        bar-chart[n] sp
        ascii bar chart of the given superposition        
        where n specifies max width of bar-chart
        
    examples:
        bar-chart[30] rank split |a b c d e f>
            ----------
            a : |||||
            b : ||||||||||
            c : |||||||||||||||
            d : ||||||||||||||||||||
            e : |||||||||||||||||||||||||
            f : ||||||||||||||||||||||||||||||
            ----------

        bar-chart[40] shuffle rank split |a b c d e f>
            ----------
            d : ||||||||||||||||||||||||||
            a : ||||||
            b : |||||||||||||
            c : ||||||||||||||||||||
            e : |||||||||||||||||||||||||||||||||
            f : ||||||||||||||||||||||||||||||||||||||||
            ----------

    see also:
        plot, sorted-bar-chart, coeff-sort, ket-sort
        
    future:
        implement sbar-chart, a version that works for sequences
"""
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


# set invoke method:
compound_table['sorted-bar-chart'] = ['apply_sp_fn', 'sorted_bar_chart', '']
# set usage info:
function_operators_usage['sorted-bar-chart'] = """
    description:
        sorted-bar-chart[n] sp
        ascii bar chart of the given superposition, sorted by coefficient
        where n specifies max width of bar-chart        
        note, somewhat redundant, since we can apply coeff-sort, or ket-sort and then use standard bar-chart
        ie: 
        bar-chart[30] ket-sort sp
        bar-chart[30] coeff-sort sp
        
    examples:
        sorted-bar-chart[30] rank split |a b c d e f>
            ----------
            f : ||||||||||||||||||||||||||||||
            e : |||||||||||||||||||||||||
            d : ||||||||||||||||||||
            c : |||||||||||||||
            b : ||||||||||
            a : |||||
            ----------
        
        sorted-bar-chart[40] shuffle rank split |a b c d e f>
            ----------
            f : ||||||||||||||||||||||||||||||||||||||||
            e : |||||||||||||||||||||||||||||||||
            d : ||||||||||||||||||||||||||
            c : ||||||||||||||||||||
            b : |||||||||||||
            a : ||||||
            ----------

    see also:
        plot, bar-chart, coeff-sort, ket-sort
"""
def sorted_bar_chart(one, width):
    return bar_chart(one, width, True)



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
# set invoke method:
compound_table['delete'] = ['apply_fn', 'edit_delete', '']
# set usage info:
function_operators_usage['delete'] = """
    description:
        delete[char, k] ket
        delete, one of three edit distance operators
        see: https://en.wikipedia.org/wiki/Edit_distance

    examples:
        delete["k", 0] |kitten>
            |itten>
        
        insert["g", 6] insert["i", 4] delete["e", 4] insert["s", 0] delete["k", 0] |kitten>
            |sitting>
    
    see also:
        insert, substitute
"""
def edit_delete(one, *parameters):  # cool. Seems to work!
    try:
        char, k = parameters
        k = int(k)
        text = one.label
        if text[k] == char:
            result = text[:k] + text[k + 1:]
        return ket(result, one.value)
    except:
        return one


# insert[s,0]
# set invoke method:
compound_table['insert'] = ['apply_fn', 'edit_insert', '']
# set usage info:
function_operators_usage['insert'] = """
    description:
        insert[char, k] ket
        insert, one of three edit distance operators
        see: https://en.wikipedia.org/wiki/Edit_distance

    examples:
        insert["g", 6] insert["i", 4] delete["e", 4] insert["s", 0] delete["k", 0] |kitten>
            |sitting>

    see also:
        delete, substitute
"""
def edit_insert(one, *parameters):
    try:
        char, k = parameters
        k = int(k)
        text = one.label
        result = text[:k] + char + text[k:]
        return ket(result, one.value)
    except:
        return one


# substitute[s,k,0]
# set invoke method:
compound_table['substitute'] = ['apply_fn', 'edit_substitute', '']
# set usage info:
function_operators_usage['substitute'] = """
    description:
        substitute[char1, char2, k] ket
        substitute, one of three edit distance operators
        see: https://en.wikipedia.org/wiki/Edit_distance

    examples:
        insert["g", 6] substitute["i", "e", 4] substitute["s", "k", 0] |kitten>
            |sitting>

    see also:
        delete, insert
"""
def edit_substitute(one, *parameters):
    try:
        char1, char2, k = parameters
        k = int(k)
        text = one.label
        if text[k] == char2:
            text = text[:k] + char1 + text[k + 1:]
        return ket(text, one.value)
    except:
        return one

# set invoke method:
seq_fn_table['print-type'] = 'print_type'
def print_type(one):
    print(type(one))
    return one

# long sp. Prints out the long_display form of a sp.
# set invoke method:
seq_fn_table['long-display'] = 'long_display'
# set usage info:
function_operators_usage['long-display'] = """
    description:
        long-display seq
        a slightly easier to read display of sequences
        
    examples:
        long-display ssplit 3.5 |abcd>
            seq |0> => 3.5|a>
            seq |1> => 3.5|b>
            seq |2> => 3.5|c>
            seq |3> => 3.5|d>
            3.5|a> . 3.5|b> . 3.5|c> . 3.5|d>

        long-display split 7|a b c d e>
            seq |0> => 7|a> + 7|b> + 7|c> + 7|d> + 7|e>
            7|a> + 7|b> + 7|c> + 7|d> + 7|e>

        long-display (|a> + 3|b> . |c> . 5|d> + 7|e> + 11|f>)
            seq |0> => |a> + 3|b>
            seq |1> => |c>
            seq |2> => 5|d> + 7|e> + 11|f>
            |a> + 3|b> . |c> . 5|d> + 7|e> + 11|f>

    see also:
"""
def long_display(one):
    one.long_display()
    return one




# the discrimination function.
# returns the difference between largest coeff, and second largest coeff.
# discrim (90|x> + 55|y>)
# should return 35| >
#
# I now think this should be moved to ket/sp classes.
# Done. This is now deprecated.
# Alternatively, remove from ket/sp and put in "sp_fn_table" -- see the processor.
# set invoke method:
sp_fn_table['discrimination'] = 'discrimination'
# set usage info:
function_operators_usage['discrimination'] = """
    description:
        discrimination sp
        discrimination, returns the difference between the largest coeff, and the second largest coeff.

    examples:
        discrimination (90|x> + 55|y>)
            35| >

    see also:
    
    future:
        maybe it should be built in to our ket/superposition/sequence classes?
"""
def discrimination(one):
    if type(one) is ket:
        result = one.value
    elif len(one) == 0:
        result = 0
    elif len(one) == 1:
        result = one.value
    else:  # assumes to get to this branch, one is a superposition, not a ket or sequence
        one = one.coeff_sort()
        first, second = list(itertools.islice(one.dict.items(), 0, 2))
        result = first[1] - second[1]
    return ket(" ", result)


# to-coeff 12|> == |>
# to-ceoff 26|a: b> == 26| >
#
# assumes one is a ket
# set invoke method:
fn_table['to-coeff'] = 'to_coeff'
# set usage info:
function_operators_usage['to-coeff'] = """
    description:
        to-coeff ket
        replace the ket text with ' '
        ie, only keep the coefficient

    examples:
        -- if the ket is the don't know ket, return the don't know ket:
        to-coeff 12|>
            |>
        
        to-coeff 26|a: b>
            26| >

        -- since the ket text is now the same, the coefficients add up:
        to-coeff (26|a: b> + 13|x>)
            39| >

        -- another longer example:
        to-coeff (3|a: b: c> + 5|x: y> + 7|fish> + 2.5|animal: mammal: cat>)
            17.5| >

    see also:

"""
def to_coeff(one):
    if len(one) == 0:
        return ket()
    return ket(" ", one.value)



# 9/2/2016:
# rename_kets:
# takes a superposition (one), and for each ket replaces the string in ket two with the string in ket three
#
# one is a superposition, two and three are kets.
def old_rename_kets(one, two, three):
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


# https://en.wikipedia.org/wiki/Production_(computer_science)
# set invoke method:
whitelist_table_3['string-replace'] = 'string_replace'
# set usage info:
sequence_functions_usage['string-replace'] = """
    description:
        string-replace(seq, sp, ket)
        for the sequence seq, for every label in sp, replace with ket.label

    examples:
        string-replace(|a> . |sad> . |fellow>, |sad>, |happy>)
            |a> . |happy> . |fellow>

        string-replace(|Today's date is ${date}.>, |${date}>, extract-value current-date |> )
            |Today's date is 2018-07-11.>

        -- remove " chars:
        remove-quotes (*) #=> string-replace(|_self> , |">, |>)
        
        remove-quotes |text: "some text">    
            |text: some text>

        -- replace "  " with " "
        -- ie, double space with single space:
        chomp-double-space (*) #=> string-replace(|_self>, |  >, | >)

        -- put it to use:
        chomp-double-space |some     text>
            |some   text>

        chomp-double-space^10 |some     text>
            |some text>

        -- remove punctuation chars:
        -- :;.,!?$-"'
        remove-punctuation (*) #=> string-replace(|_self>, split[""] |:;.,!?$-"'>, |>)
        
        -- now put it to use:
        remove-punctuation |some, ... ! $$? noise-text>
            |some    noisetext>
            
    see also:
        replace
"""
def string_replace(input_seq, one, two, three):
    two = two.to_sp()
    s2 = three.to_sp().label

    seq = sequence([])
    for sp in one:
        r = superposition()
        for x in sp:
            text = x.label
            for elt in two:
                s1 = elt.label
                text = text.replace(s1, s2)
            r.add(text, x.value)
        seq += r
    return seq



# set invoke method:
compound_table['replace'] = ['apply_fn', 'char_replace', '']
# set usage info:
function_operators_usage['replace'] = """
    description:
        replace[c1, c2] ket
        replace all the individual chars in c1 with c2

    examples:
        -- remove comma's from numbers:
        replace[", ", ""] |35,572,990>
            |35572990>
                    
        replace[", ", ""] |123, 920, 001, 558>
            |123920001558>
                    
        -- replace punctuation chars with ' '
        replace[".,!?$-", " "] |some, ... ! $$? noise-text> 
            |some            noise text>            

    see also:
        string-replace
    
    future:
        maybe rename to substitute
        how replace " char? For now, see string-replace
"""
def char_replace(one, *parameters):
    try:
        c1, c2 = parameters
        # text = re.sub(c1, c2, one.label)
        # text = one.label.replace()
        text = one.label
        for c in c1:
            text = text.replace(c, c2)
        return ket(text, one.value)
    except Exception as e:
        print('reason:', e)
        return one



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
# we need an example for this, before we can implement it!
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






# the frequency class equation:
# see: http://en.wikipedia.org/wiki/Frequency_list
# set invoke method:
whitelist_table_2['frequency-class'] = 'frequency_class_ket'
# set usage info:
sequence_functions_usage['frequency-class'] = """
    description:
        frequency-class(ket, sp)
        implement the frequency class equation
        see: https://en.wikipedia.org/wiki/Word_lists_by_frequency#Statistics

    the algorithm:
        drop all elements <= 0 from X
        smallest = the min coeff in X
        largest = the max coeff in X
        f = the value of e.label in X
        
        if largest <= 0:
            return 0
        if f <= 0:
            return math.floor(0.5 - math.log(smallest / largest, 2)) + 1
        return math.floor(0.5 - math.log(f / largest, 2))

    examples:

    see also:
        normed-frequency-class, map-to-topic
"""
def frequency_class_ket(input_seq, e, X):
    value = frequency_class_value(e, X)
    return ket('number: ' + str(value))

def frequency_class_value(e, X):
    e = e.to_sp().label
    X = X.to_sp().drop()  # filter out elements <= 0
    smallest = X.find_min_coeff()
    largest = X.find_max_coeff()
    f = X.find_value(e)

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
# set invoke method:
whitelist_table_2['normed-frequency-class'] = 'normed_frequency_class_ket'
# set usage info:
sequence_functions_usage['normed-frequency-class'] = """
    description:
        normed-frequency-class(e, X)
        implement the normed frequency class equation
        where: e is a ket, X is a superposition, and the result is in [0,1]
        1 for exact match, 0 for not in set, values in between otherwise
        
        if all coeffs in X are equal, it gives 1 for membership, and 0 for non-membership
        if the coeffs are not all equal, then it has fuzzier properties

        this function is the back-end to the map-to-topic function
        and works particularly well when X is a frequency list
        
    the algorithm:
        drop all elements <= 0 from X
        smallest = the min coeff in X
        largest = the max coeff in X
        f = the value of e.label in X
        
        if largest <= 0 or f <= 0:
            return 0
        fc_max = math.floor(0.5 - math.log(smallest / largest, 2)) + 1
        return 1 - math.floor(0.5 - math.log(f / largest, 2)) / fc_max
        
    examples:
        -- all coeffs in X equal:
        -- b is a member of |a> + |b> + |c> + |d> + |e>
        normed-frequency-class(|b>, |a> + |b> + |c> + |d> + |e>)
            |number: 1.0>

        -- all coeffs in X equal:
        -- c is a member of 7.2 |a> + 7.2 |b> + 7.2 |c> + 7.2 |d>
        normed-frequency-class(|c>, 7.2 |a> + 7.2 |b> + 7.2 |c> + 7.2 |d>)
            |number: 1.0>

        -- e is not a member of |a> + |b> + |c>
        normed-frequency-class(|e>, |a> + |b> + |c>)
            |number: 0>


        -- a "not all coeffs equal" example:
        -- consider: 
        smooth[0.5]^5 |10>
            0.001|7.5> + 0.01|8> + 0.044|8.5> + 0.117|9> + 0.205|9.5> + 0.246|10> + 0.205|10.5> + 0.117|11> + 0.044|11.5> + 0.01|12> + 0.001|12.5>

        -- this has this shape:
        bar-chart[40] smooth[0.5]^5 |10>
            ----------
            7.5  :
            8    : |
            8.5  : |||||||
            9    : |||||||||||||||||||
            9.5  : |||||||||||||||||||||||||||||||||
            10   : ||||||||||||||||||||||||||||||||||||||||
            10.5 : |||||||||||||||||||||||||||||||||
            11   : |||||||||||||||||||
            11.5 : |||||||
            12   : |
            12.5 :
            ----------

        -- now see the results:
        fc |*> #=> round[3] frequency-class(|_self>, smooth[0.5]^5 |10>)
        nfc |*> #=> round[3] normed-frequency-class(|_self>, smooth[0.5]^5 |10>)
        table[number, fc, nfc] range(|6>, |14>, |0.5>)
            +--------+----+-------+
            | number | fc | nfc   |
            +--------+----+-------+
            | 6      | 9  | 0     |
            | 6.5    | 9  | 0     |
            | 7      | 9  | 0     |
            | 7.5    | 8  | 0.111 |
            | 8      | 5  | 0.444 |
            | 8.5    | 2  | 0.778 |
            | 9      | 1  | 0.889 |
            | 9.5    | 0  | 1.0   |
            | 10     | 0  | 1.0   |
            | 10.5   | 0  | 1.0   |
            | 11     | 1  | 0.889 |
            | 11.5   | 2  | 0.778 |
            | 12     | 5  | 0.444 |
            | 12.5   | 8  | 0.111 |
            | 13     | 9  | 0     |
            | 13.5   | 9  | 0     |
            | 14     | 9  | 0     |
            +--------+----+-------+

    see also:
        frequency-class, map-to-topic
"""
def normed_frequency_class_ket(input_seq, e, X):
    value = normed_frequency_class_value(e, X)
    return ket('number: ' + str(value))

# e is a ket, X is a superposition
# for best effect X should be a frequency list
def normed_frequency_class_value(e, X):
    e = e.to_sp().label  # make sure e is a ket, not a superposition, else X.find_value(e) bugs out.
    X = X.to_sp().drop()  # drop elements with coeff <= 0
    smallest = X.find_min_coeff()  # return the min coeff in X as float
    largest = X.find_max_coeff()  # return the max coeff in X as float
    f = X.find_value(e)  # return the value of ket e in superposition X as float

    if largest <= 0 or f <= 0:  # otherwise the math.log() blows up!
        return 0

    fc_max = math.floor(0.5 - math.log(smallest / largest, 2)) + 1  # NB: the + 1 is important, else the smallest element in X gets reported as not in set.
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
    return intersection_fn(absolute_difference_fn, average.normalize(), specific.normalize())  # NB: .normalize() is vital for this to work!
    # return intersection_fn(absolute_difference_fn,average,specific)




# 9/2/2016:
# guess-ket |fred>          -- return the best matching known ket (using simm and so on)
# guess-ket[3] |Sam>        -- return the best 3 matching known kets, providing simm > 0
# guess-ket[*] |robbie>     -- return all matching known kets, providing simm > 0
#
# could do with some optimization!
#
# set invoke method:
ket_context_table['guess-ket'] = 'guess_ket'
compound_table['guess-ket'] = ['apply_fn', 'guess_ket', 'context']
# set usage info:
function_operators_usage['guess-ket'] = """
    description:
        guess-ket ket
        return the best matching known ket, using simm and letter-ngrams[1,2,3]
        
        guess-ket[n] ket
        return the best n matching kets, using simm and letter-ngrams[1,2,3]
        
        guess-ket[*] ket
        return all matching kets, using simm and letter-ngrams[1,2,3]
        
    examples:
        -- learn some knowledge:
        age |person: Fred Smith> => |47>
        mother |person: Fred Jones> => |Mary>
        age |person: Sam Hughes> => |49>
        
        -- now guess some kets:
        guess-ket |Fred>
            0.235|person: Fred Jones>

        guess-ket[*] |Fred>
            0.235|person: Fred Jones> + 0.216|person: Fred Smith> + 0.059|person: Sam Hughes> + 0.056|context>

        guess-ket[*] |Sam>
            0.157|person: Sam Hughes> + 0.059|person: Fred Smith> + 0.039|person: Fred Jones>

        guess-ket[*] |jones>
            0.353|person: Fred Jones> + 0.222|context> + 0.176|person: Sam Hughes> + 0.137|person: Fred Smith>
                
    see also:
        guess-operator, rel-kets, starts-with, simm, letter-ngrams
"""
# one is a ket
def guess_ket(one, context, t=1):
    def process_string(s):
        one = ket(s.lower())  # I presume we want s.lower(). Maybe sometimes we don't?
        return make_ngrams(one, (1,2,3), 'letter')

    try:
        guess = process_string(one.label)
        # print('guess:', guess)
        r = superposition()
        for x in context.relevant_kets("*"):  # what about kets that are only on the right hand side of a learn rule? This misses them. One way is run "create inverse", but is there a better way?
            similarity = aligned_simm_value(guess, process_string(x.label))
            if similarity > 0:
                r.add_sp(x.multiply(similarity))
        if t == '*':
            return r.coeff_sort()
        else:
            return r.coeff_sort().select_range(1, int(t))
    except Exception as e:
        print('guess-ket reason:', e)
        return ket()


# 9/2/2016:
# guess-operator[age]          -- return the best matching known operator (using simm and so on)
# guess-operator[friend,3]     -- return the best 3 matching known operators, providing simm > 0
# guess-operator[mother,*]     -- return all matching known operators, providing simm > 0
#
# set invoke method:
compound_table['guess-operator'] = ['apply_naked_fn', 'guess_operator', 'context']
# set usage info:
function_operators_usage['guess-operator'] = """
    description:
        guess-operator[age]
        return the best matching known operator, using simm and letter-ngrams[1,2,3]
        
        guess-operator[friend, 3]
        return the best 3 matching known operators, using simm and letter-ngrams[1,2,3]
        
        guess-operator[mother, *]
        return all matching known operators, using simm and letter-ngrams[1,2,3]
        
    examples:
        load bots.sw
        guess-operator[friend]
            0.833|op: friends>

        guess-operator[holiday, 3]
            0.349|op: favourite-holiday-spot> + 0.222|op: hair-colour> + 0.198|op: religion>

    see also:
        guess-ket, simm, letter-ngrams
"""
def guess_operator(context, *parameters):
    try:
        op, t = parameters
        if t != '*':
            t = int(t)
    except:
        op = parameters[0]
        t = 1

    def process_string(s):
        one = ket(s.lower())
        return make_ngrams(one, (1,2,3), 'letter')

    try:
        guess = process_string(op)
        r = superposition()
        for x in context.supported_operators():
            similarity = aligned_simm_value(guess, process_string(x.label[4:]))  # need to convert 'op: age' to 'age'
            r.add_sp(x.multiply(similarity))
        if t == '*':
            return r.drop().coeff_sort()
        else:
            return r.drop().coeff_sort().select_range(1, t)
    except Exception as e:
        print('guess-operator reason:', e)
        return ket("", 0)




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
def learn_ket_normalizations(context, *parameters):
    try:
        op1, op2, t = parameters
        t = float(t)
    except:
        return ket()

    the_kets = context.relevant_kets(op1)
    the_sum = superposition()
    for x in the_kets:
        the_sum.add_sp(x.apply_op(context, op1).to_sp())
    for x in the_sum:
        if x.value <= 0:
            continue
        y = ket(x.label)
        context.learn(op2, y, y.multiply(t / x.value))
    return ket("ket-norms")



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
        return x.apply_op(context, "encode").apply_fn(append_column, "10").similar_input(context, "pattern").multiply(10)

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
                if p in x_pieces and p in y_pieces:  # not perfect, but works for now.
                    continue
                new_pieces.append(p)
            #      new_pieces.sort()
            r += ket(": ".join(new_pieces))
    return r


# set invoke method:
whitelist_table_2['test-input-seq'] = 'input_seq_test'
# set usage info:
sequence_functions_usage['test-input-seq'] = """
    description:
        test-input-seq(input-seq, seq, seq)
        our first and only sequence function that makes use of input-seq
        all it does is print out the given sequences, and return input-seq
        just a place-holder until we find a real application of input-seq feature
    
    examples:
        test-input-seq(|a>, |b>) (|x> . |y>)
            input_seq: |x> . |y>
            one: |a>
            two: |b>
            |x> . |y>
        
    see also:

"""
def input_seq_test(input_seq, one, two):
    print('input_seq: %s' % input_seq)
    print('one: %s' % one)
    print('two: %s' % two)
    return input_seq
