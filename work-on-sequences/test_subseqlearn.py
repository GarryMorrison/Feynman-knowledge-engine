#!/usr/bin/env python3

#######################################################################
# code to test the subseqlearn.py file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-07-11
# Update: 2017-7-13
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


def test_ket_sort():
  r = superposition()
  r.add('0')
  r.add('25')
  r.add('1', 0.86)
  r.add('24', 0.86)
  r = r.ket_sort()
  assert str(r) == '|0> + 0.86|1> + 0.86|24> + |25>'

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
raw_seq8 = sequence('raw seq 8', ['a','b','c','d','e','f','g'])

full_seq1 = sequence('full seq 1', [a,b,c,d, e,f,g, h,i,b, c,d, h,i,b, a,b,c,d])
full_seq2 = sequence('full seq 2', [a,b,c,d, e,f,g, h,i, a,b,c,d, h,i, b, a,b,c,d])
full_seq3 = sequence('full seq 3', [a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f,h, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq4 = sequence('full seq 4', [e, h,h, e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f, h,h, i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq5 = sequence('full seq 5', [e,h,h,e,e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,h,d, h,i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq6 = sequence('full seq 6', [x,x,x,x,x,e, h,h, e,e, a,b,c,d, a,b,c,d, a,b,c,d, a,b,c,d, f,f,f, h,h, i,b, e,f,g, e,f,g, e,f,g, h,i,b])
full_seq7 = sequence('full seq 7', [x,x,x,x, x,e,h,h,e,e,e, x,x,x,x, a,b,c,d])
full_seq8 = sequence('full seq 8', [a,b,c,d,e,f,g])


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
#  assert str(partition_points3) == ''
# [(0, 3), (4, 7), (8, 11), (12, 15), (21, 22), (23, 25), (26, 28), (29, 31), (33, 34)]


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

def test_learn_and_fragment_sequence_v8():
  partition_points8 = learn_subsequences(full_seq8)
  subsequences = fragment_sequence(raw_seq8, partition_points8)
  assert subsequences == [['a', 'b', 'c', 'd', 'e', 'f', 'g']]



def test_fragment_positive_sequence_v1():
  partition_points = learn_subsequences(full_seq1)
  subsequences = fragment_positive_sequence(raw_seq1, partition_points)
  assert subsequences == [['a', 'b', 'c', 'd'], ['h', 'i', 'b'], ['c', 'd'], ['h', 'i', 'b'], ['a', 'b', 'c', 'd']]

def test_fragment_positive_sequence_v2():
  partition_points = learn_subsequences(full_seq2)
  subsequences = fragment_positive_sequence(raw_seq2, partition_points)
  assert subsequences == [['a', 'b', 'c', 'd'], ['h', 'i'], ['a', 'b', 'c', 'd'], ['h', 'i'], ['a', 'b', 'c', 'd']]

def test_fragment_positive_sequence_v3():
  partition_points = learn_subsequences(full_seq3)
  subsequences = fragment_positive_sequence(raw_seq3, partition_points)
  assert subsequences == [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], 
  ['h', 'i', 'b'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]

def test_fragment_positive_sequence_v4():
  partition_points = learn_subsequences(full_seq4)
  subsequences = fragment_positive_sequence(raw_seq4, partition_points)
  assert subsequences == [['h', 'h'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], 
  ['h', 'h'], ['i', 'b'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]

def test_fragment_positive_sequence_v5():
  partition_points = learn_subsequences(full_seq5)
  subsequences = fragment_positive_sequence(raw_seq5, partition_points)
  assert subsequences == [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], 
  ['h', 'i', 'b'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]

def test_fragment_positive_sequence_v6():
  partition_points = learn_subsequences(full_seq6)
  subsequences = fragment_positive_sequence(raw_seq6, partition_points)
  assert subsequences == [['h', 'h'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], 
  ['h', 'h'], ['i', 'b'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['e', 'f', 'g'], ['h', 'i', 'b']]

def test_fragment_positive_sequence_v7():
  partition_points = learn_subsequences(full_seq7)
  subsequences = fragment_positive_sequence(raw_seq7, partition_points)
  assert subsequences == [['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x']]

def test_fragment_positive_sequence_v8():
  partition_points = learn_subsequences(full_seq8)
  subsequences = fragment_positive_sequence(raw_seq8, partition_points)
  assert subsequences == []

  


square = sequence('square', [0,2,2,2,2,2,2,0])
triangle = sequence('triangle', [0.0,0.08,0.16,0.24,0.32,0.4,0.48,0.56,0.64,0.72,0.8,0.88,0.96,1.04,0.92,0.84,0.76,0.68,0.6,0.52,0.44,0.36,0.28,0.2,0.12,0.04])
zero = sequence('zero', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

two_tri = sequence('two triangle') + triangle + triangle
mixed_seq = sequence('mixed seq') + triangle + zero + square + zero + triangle

encode_dict = {}
encoded_square = square.encode(encode_dict)
encoded_triangle = triangle.encode(encode_dict)
encoded_two_tri = two_tri.encode(encode_dict)
encoded_mixed = mixed_seq.encode(encode_dict)


def test_learn_and_fragment_float_sequence_v1():
  partition_points = learn_subsequences(encoded_square, 0.98)
  subsequences = fragment_sequence(square, partition_points)
  assert subsequences == [[0, 2, 2, 2, 2, 2, 2, 0]]

def test_learn_and_fragment_float_sequence_v2():
  partition_points = learn_subsequences(encoded_triangle, 0.98)
  subsequences = fragment_sequence(triangle, partition_points)
  assert subsequences == [[0.0, 0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.72, 0.8, 0.88, 0.96, 1.04, 0.92, 0.84, 0.76, 0.68, 0.6, 0.52, 0.44, 0.36, 0.28, 0.2, 0.12, 0.04]]

def test_learn_and_fragment_float_sequence_v3():
  partition_points = learn_subsequences(encoded_two_tri, 0.98)
  subsequences = fragment_sequence(two_tri, partition_points)
  assert subsequences == [[0.0, 0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.72, 0.8, 0.88, 0.96, 1.04, 0.92, 0.84, 0.76, 0.68, 0.6, 0.52, 0.44, 0.36, 0.28, 0.2, 0.12, 0.04], 
  [0.0, 0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.72, 0.8, 0.88, 0.96, 1.04, 0.92, 0.84, 0.76, 0.68, 0.6, 0.52, 0.44, 0.36, 0.28, 0.2, 0.12, 0.04]]

def test_learn_and_fragment_float_sequence_v3():
  partition_points = learn_subsequences(encoded_mixed, 0.98)
  subsequences = fragment_sequence(mixed_seq, partition_points)
  assert subsequences == [[0.0, 0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.72, 0.8, 0.88, 0.96, 1.04, 0.92, 0.84, 0.76, 0.68, 0.6, 0.52, 0.44, 0.36, 0.28, 0.2, 0.12, 0.04], 
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
  [2, 2, 2, 2, 2, 2], 
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0], 
  [0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.72, 0.8, 0.88, 0.96, 1.04, 0.92, 0.84, 0.76, 0.68, 0.6, 0.52, 0.44, 0.36, 0.28, 0.2, 0.12, 0.04]]


