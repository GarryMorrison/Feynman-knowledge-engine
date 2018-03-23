#!c:/Python34/python.exe

#######################################################################
# create the imdb.sw file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 23/3/2018
# Update: 23/3/2018
# Copyright: GPLv3
#
# Usage: ./ec2_clean_imdb.py
#
#######################################################################

import sys

from semantic_db.code import *


#file = "data/10k-actors.txt"
#file = "data/30-actors.txt"
#file = "data/full-imdb.txt"
#file = "data/movie-imdb.txt"  

# testing file:
file = "data/1000-imdb-test.txt"
#file = "data/full-imdb.txt"


def remove_invalid_chars(s):
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('|', '&pipe;')
    return s

# for now, not much, but maybe more later.
def process_movie(s):
    s = remove_invalid_chars(s)
    r = s.split(")", 1)[0] + ")"
    return "movie: " + r

def process_actor(s):
    s = remove_invalid_chars(s)
    try:
        last, first = s.split(', ')
        return "actor: " + first + " " + last
    except:
        return "actor: " + s


def main(filename, sw_name):
    # substrings that indicate it is a tv show, not a movie:
    tv_substrings = ['\"', "(TV)", "(V)", "(VG)", "{", "}"]

    context = NewContext("new imdb")
    actor = ""
    movies = superposition()

    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            print("line:", line)
            if line == "":
                print("actor:", actor)
                print("movies:", str(movies))

                actor = process_actor(actor)
                if len(movies) > 0:
                    context.learn("movies", actor, movies)

                for movie in movies:
                    context.add_learn("actors", movie, actor)

                actor = ""
                movies = superposition()
            else:
                row = [x for x in line.split('\t') if x != '' ]
                try:
                    actor, show = row
                except:
                    show = row[0]
                    match = False
                    for substr in tv_substrings:
                        if substr in show:
                            match = True
                            break
                    if not match:
                        movies.add(process_movie(show))


    # print(context.dump_universe())
    context.save(sw_name, exact_dump=False)


main('data/1000-imdb-test.txt', 'sw-examples/testing-imdb.sw')
