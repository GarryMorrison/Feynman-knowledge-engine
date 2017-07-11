#!/usr/bin/env python3

#######################################################################
# code to test the subseqlearn.py file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-07-11
# Update:
# Copyright: GPLv3
#
# Usage: py.text -v test_subseqlearn.py
#
#######################################################################

from subseqlearn import *

# learn some simple superpositions:
a = superposition()
a.add('a')
b = superposition()
b.add('b')
c = superposition()
c.add('c')
d = superposition()
d.add('d')
e = superposition()
e.add('e')
f = superposition()
f.add('f')
g = superposition()
g.add('g')
h = superposition()
h.add('h')
i = superposition()
i.add('i')
x = superposition()
x.add('x')
y = superposition()
y.add('y')
z = superposition()
z.add('z')


def test_superposition_addition():
  r = superposition() + a + b + 3.2*c + d/7 + e
  assert str(r) == '|a> + |b> + 3.2|c> + 0.143|d> + |e>'

def test_strict_vs_non_strict_similarity():
  sp_seq1 = sequence('sp seq 1', [a,b,c,d,e])
  sp_seq2 = sequence('sp seq 2', [a,c,b,d,e])
  assert seq_simm(sp_seq1, sp_seq2) == 0                     # strict similarity
  assert seq_simm(sp_seq1, sp_seq2, False) == 0.8125         # non-strict similarity

def test_similar_sequence_offset():
  sp_seq = sequence('sp seq', [a,b,c,d,e,f,g,h,i])
  seq_frag1 = sequence('seq frag 1', [c,d,e,f])
  seq_frag2 = sequence('seq frag 2', [f,g,h])

  r1 = sp_seq.similar_sequence_offset(seq_frag1)
  r2 = sp_seq.similar_sequence_offset(seq_frag2)

  assert str(r1) == '|2>'
  assert str(r2) == '|5>'


# test learn_subsequences, and fragment_sequence section:
raw_seq1 = sequence('raw seq 1', ['a','b','c','d','e','f','g','h','i','b','c','d','h','i','b','a','b','c','d'])
raw_seq2 = sequence('raw seq 2', ['a','b','c','d','e','f','g','h','i', 'a','b','c','d', 'h','i','b', 'a','b','c','d'])
raw_seq3 = sequence('raw seq 3', ['a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'f','f','f','h', 'h','i','b', 'e','f','g', 'e','f','g', 'e','f','g', 'h','i','b'])
raw_seq4 = sequence('raw seq 4', ['e','h','h','e','e', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'f','f','f','h', 'h','i','b', 'e','f','g', 'e','f','g', 'e','f','g', 'h','i','b'])
raw_seq5 = sequence('raw seq 5', ['e','h','h','e','e','e', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'f','f','h','d', 'h','i','b', 'e','f','g', 'e','f','g', 'e','f','g', 'h','i','b'])
raw_seq6 = sequence('raw seq 6', ['x','x','x','x','x', 'e','h','h','e','e', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'a','b','c','d', 'f','f','f','h', 'h','i','b', 'e','f','g', 'e','f','g', 'e','f','g', 'h','i','b'])
raw_seq7 = sequence('raw seq 7', ['x','x','x','x','x', 'e','h','h','e','e','e', 'x','x','x','x', 'a','b','c','d'])

full_seq1 = sequence('full seq 1', [a,b,c,d, e,f,g, h,i,b, c,d, h,i,b, a,b,c,d])
full_seq2 = sequence('full seq 2', [a,b,c,d, e,f,g, h,i, a,b,c,d, h,i, b, a,b,c,d])
full_seq3 = sequence('full seq 3', [a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f,h, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq4 = sequence('full seq 4', [e, h,h, e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f, h,h, i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq5 = sequence('full seq 5', [e,h,h,e,e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,h,d, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq6 = sequence('full seq 6', [x,x,x,x,x,e, h,h, e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f, h,h, i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq7 = sequence('full seq 7', [x,x,x,x, x,e,h,h,e,e,e, x,x,x,x, a,b,c,d])


def test_learn_subsequences_v1():
  partition_points1 = learn_subsequences(full_seq1)
  assert partition_points1 == [(0, 3), (7, 9), (10, 11), (12, 14), (15, 18)]

def test_fragment_sequence_v1():
  partition_points1 = [(0, 3), (7, 9), (10, 11), (12, 14), (15, 18)]
  subsequences = fragment_sequence(raw_seq1, partition_points1)
  assert subsequences == [['a', 'b', 'c', 'd'], ['e', 'f', 'g'], ['h', 'i', 'b'], ['c', 'd'], ['h', 'i', 'b'], ['a', 'b', 'c', 'd']]


def test_learn_subsequences_v2():
  partition_points2 = learn_subsequences(full_seq2)
  assert partition_points2 == [(0, 3), (7, 8), (9, 12), (13, 14), (16, 19)]

def test_fragment_sequence_v2():
  partition_points2 = [(0, 3), (7, 8), (9, 12), (13, 14), (16, 19)]
  subsequences = fragment_sequence(raw_seq2, partition_points2)
  assert subsequences == [['a', 'b', 'c', 'd'], ['e', 'f', 'g'], ['h', 'i'], ['a', 'b', 'c', 'd'], ['h', 'i'], ['b'], ['a', 'b', 'c', 'd']]


def test_learn_subsequences_v3():
  partition_points3 = learn_subsequences(full_seq3)
  assert partition_points3 == [(0, 3), (4, 7), (8, 11), (12, 15), (20, 22), (23, 25), (26, 28), (29, 31), (32, 34)]

def test_fragment_sequence_v3():
  partition_points3 = [(0, 3), (4, 7), (8, 11), (12, 15), (20, 22), (23, 25), (26, 28), (29, 31), (32, 34)]
  subsequences = fragment_sequence(raw_seq3, partition_points3)
  assert subsequences == [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], 
  ['f', 'f', 'f', 'h'], ['h', 'i', 'b'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]


def test_learn_and_fragment_sequence_v4():
  partition_points4 = learn_subsequences(full_seq4)
  subsequences = fragment_sequence(raw_seq4, partition_points4)
  assert subsequences == [['e'], ['h', 'h'], ['e', 'e'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], 
  ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['f', 'f', 'f'], ['h', 'h'], ['i', 'b'], ['e', 'f', 'g'], 
  ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]

def test_learn_and_fragment_sequence_v5():
  partition_points5 = learn_subsequences(full_seq5)
  subsequences = fragment_sequence(raw_seq5, partition_points5)
  assert subsequences == [['e', 'h', 'h', 'e', 'e', 'e'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], 
  ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['f', 'f', 'h', 'd'], ['h', 'i', 'b'], ['e', 'f', 'g'], 
  ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]

def test_learn_and_fragment_sequence_v6():
  partition_points6 = learn_subsequences(full_seq6)
  subsequences = fragment_sequence(raw_seq6, partition_points6)
  assert subsequences == [['x', 'x', 'x', 'x', 'x', 'e'], ['h', 'h'], ['e', 'e'], ['a', 'b', 'c', 'd'], 
  ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['f', 'f', 'f'], ['h', 'h'], ['i', 'b'], 
  ['e', 'f', 'g'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]

def test_learn_and_fragment_sequence_v7():
  partition_points7 = learn_subsequences(full_seq7)
  subsequences = fragment_sequence(raw_seq7, partition_points7)
  assert subsequences == [['x', 'x', 'x', 'x'], ['x', 'e', 'h', 'h', 'e', 'e', 'e'], ['x', 'x', 'x', 'x'], ['a', 'b', 'c', 'd']]

