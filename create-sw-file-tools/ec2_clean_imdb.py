#!/usr/bin/env python3

# code that I ran on EC2 r3.large to create imdb.sw file.
# added tweak to better filter out TV shows, and such.
# So hopefully we just have movies now.

import sys

from the_semantic_db_code import *
#from the_semantic_db_functions import *
#from the_semantic_db_processor import *

C = context_list("full improved imdb")


#file = "data/10k-actors.txt"
#file = "data/30-actors.txt"
#file = "data/full-imdb.txt"
#file = "data/movie-imdb.txt"  

# testing file:
#file = "data/1000-imdb-test.txt"

file = "data/full-imdb.txt"


# chars that indicate it is a show, not a movie:
show_chars = ['\"', "(TV)", "(V)", "(VG)", "{", "}" ]



# for now, not much, but maybe more later.
def process_movie(s):
  r = s.split(")",1)[0] + ")"
  return ket("movie: " + r)

def process_actor(s):
  try:
    last, first = s.split(', ')
    return ket("actor: " + first + " " + last)
  except:
    return ket("actor: " + s)


actor = ""
#shows = []
movies = []

with open(file,'r') as f:
  for line in f:
    line = line.rstrip()
    if line == "":
      print("actor:",actor)
#      print("shows:",shows)

      r = superposition()
      r.data = movies
#      print("movies:",r)

      x = process_actor(actor)
      if len(r) > 0:
        C.learn("movies",x,r)

      for movie in movies:
        C.add_learn("actors",movie,x)

#      print()
      actor = ""
#      shows = []
      movies = []
    else:
      row = [x for x in line.split('\t') if x != '' ]
      try:
        actor, show = row
      except:
        show = row[0]
#      shows.append(show)
#      if not show.startswith('\"'):
#        movies.append(process_movie(show))
      match = any(True if x in show else False for x in show_chars)
      if not match:
        movies.append(process_movie(show))


#    print("line:",line)


#print(C.dump_universe())

name = "sw-examples/improved-imdb.sw"
save_sw(C,name)
