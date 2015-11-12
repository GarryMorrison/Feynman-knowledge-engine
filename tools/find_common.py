#!/usr/bin/env python3

#######################################################################
# given two actors find their common movies
# or, given two movies, find their common actors
#
# NB: you have to get the movie/actor names exactly right!
# It would be nice to have a "do you mean" feature, but that would be computationally expensive!
# For now I first manually check with imdb.com to see I have it exactly right.
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015
# Update:
# Copyright: GPLv3
#
# Usage:
#  ./find_common.py actor1 actor2
#  ./find_common.py movie1 movie2
#
# Examples:
#  $ ./find_common.py 'Michael Palin' 'John Cleese'
#  $ ./find_common.py 'Leonard Nimoy' 'William Shatner'
#  $ ./find_common.py 'Pulp Fiction (1994)' 'Reservoir Dogs (1992)'
#  $ ./find_common.py 'Crocodile Dundee (1986)' "'Crocodile' Dundee II (1988)"
#  $ ./find_common.py 'Paul (I) Hogan' 'Linda Kozlowski'
#  $ ./find_common.py 'Leonard Nimoy' 'Leonard Nimoy'
#
#
# required sw file is here: http://semantic-db.org/sw-examples/improved-imdb.sw
#
#######################################################################


import sys
import os

if len(sys.argv) < 3:
  print("\nUsage:")
  print("  ./find_common.py actor1 actor2")
  print("  ./find_common.py movie1 movie2\n")
  sys.exit(1)

one = sys.argv[1]
two = sys.argv[2]

imdb_sw = "sw-examples/improved-imdb.sw"    # our imdb data

if not os.path.exists(imdb_sw):
  print("\nmovie sw file:",imdb_sw,"not found!")
  print("Download it from here: http://semantic-db.org/sw-examples/improved-imdb.sw")
  sys.exit(1)

def file_recall(filename,op,label):

  pattern = op + " |" + label + "> => "
  n = len(pattern)

  with open(filename,'r') as f:
    for line in f:
      if line.startswith(pattern):
        line = line[n:]
        return line[1:-1].split("> + |")
  return []

def display(line):
#  return ", ".join(line)
  return "\n".join(line)

def intersection(a,b):
  return list(set(a) & set(b))



def print_common_movies(sw_file,one,two):
  actor1 = "actor: " + one
  actor2 = "actor: " + two
  movies1 = file_recall(sw_file,"movies",actor1)
  movies2 = file_recall(sw_file,"movies",actor2)

# check if we have info on them:
#  if len(movies1) == 0:
#    print("I have no data on actor:",one)
#  if len(movies2) == 0:
#    print("I have no data on actor:",two)
  if len(movies1) == 0 or len(movies2) == 0:
    return

  common_movies = intersection(movies1,movies2)

  print()
  print("common movies for:")
  print(one)
  print(two)
  print("number of common movies:",len(common_movies))
#  print("common movies:",display(common_movies))
  print("common movies:")
  print(display(common_movies))
  print()


def print_common_actors(sw_file,one,two):
  movie1 = "movie: " + one
  movie2 = "movie: " + two
  actors1 = file_recall(sw_file,"actors",movie1)
  actors2 = file_recall(sw_file,"actors",movie2)

# check if we have info on them:
#  if len(actors1) == 0:
#    print("I have no data on movie:",one)
#  if len(actors2) == 0:
#    print("I have no data on movie:",two)
  if len(actors1) == 0 or len(actors2) == 0:
    return

  common_actors = intersection(actors1,actors2)

  print()
  print("common actors for:")
  print(one)
  print(two)
  print("number of common actors:",len(common_actors))
#  print("common actors:",display(common_actors))
  print("common actors:")
  print(display(common_actors))
  print()



print_common_actors(imdb_sw,one,two)
print_common_movies(imdb_sw,one,two)
