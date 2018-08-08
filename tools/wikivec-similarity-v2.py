#!/usr/bin/env python3

#######################################################################
# display wikivec similarity, version 2
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018-8-8
# Update: 2018-8-8
# Copyright: GPLv3
#
# Usage: ./wikivec-similarity-v2.py wikipage-title [number-of-results-to-show]
#
# data source: 
# http://semantic-db.org/sw-examples/30k--wikivec.sw
# http://semantic-db.org/sw-examples/300k--wikivec.sw
#
# designed to work with kets with coefficient 1, and ket labels that are len 6 hashes
# this version does not work with general superpositions!!
# this is for speed/memory reasons.
# Yup, uses much less memory and is a bit faster!
# I wonder if I could implement it in C++ now?
#
#######################################################################


import sys
import hashlib
import zlib

if len(sys.argv) < 2:
  print("\nUsage: ./wikivec-similarity-v2.py wikipage-title [number-of-results-to-show]\n")
  sys.exit(1)

if len(sys.argv) >= 2:
  wikipage = sys.argv[1]

number_of_results = 30
if len(sys.argv) == 3:
  number_of_results = int(sys.argv[2])


op = "wikivec"

source = "sw-examples/30k--wikivec.sw"
# source = "sw-examples/300k--wikivec.sw"


interactive = True
#interactive = False

def load_clean_sw_into_set_dict(filename, op):
  op_head = op + " |"
  sw_dict = {}
  with open(filename,'r') as f:
    for line in f:
      line = line.strip()
      if line.startswith(op_head):
        try:
          head,tail = line.split('> => ',1)
          label = head.split(' |',1)[1]
          sw_dict[label] = set()
          for piece in tail[:-1].split('> + '):
            tidy_piece = piece.split('|')[1]
            int_tidy_piece = int(tidy_piece, base=16)
            sw_dict[label].add(int_tidy_piece)
        except Exception as e:
          print("Exception reason: %s" % e)
          continue
  return sw_dict

def print_set_dict(sw_dict):
    for key, value in sw_dict.items():
        print('wikivec |%s> => ' % key, end='')
        print(' + '.join( '|%X>' % x for x in value ))


# quick test of loading from source file:
# sw_dict = load_clean_sw_into_set_dict(source, op)
# print_set_dict(sw_dict)
# sys.exit(0)


# let's use: |A intersection B| / |A union B|
def simm(one, two):
    intersection = set(one).intersection(two)
    union = set(one).union(two)
    if len(union) == 0:
        return 0
    return len(intersection) / len(union)



# pretty print a float:
def float_to_int(x,t=2):
    if float(x).is_integer():
        return str(int(x))
    return str(round(x,t))



def pattern_recognition(dict, pattern, t=0):
    result = []
    for label,sp in dict.items():
        value = simm(pattern, sp)
        if value > t:
            result.append((label,value))
    return result



def find_wikivec_similarity(sw_dict, wikipage, number_of_results):
    # test wikipage is in sw_dict:
    if wikipage not in sw_dict:
        print("%s not in dictionary" % wikipage)
        return [()]

    # convert wikipage to wikivec pattern:
    print("----------------")
    pattern = sw_dict[wikipage]            # currently bugs out if wikipage is not in the dictionary.
    print("wikipage:",wikipage)
    print("pattern:",pattern)
    print("pattern length:",len(pattern))
    print("----------------")

    # find matching patterns:
    result = pattern_recognition(sw_dict,pattern)

    # sort the results:
    sorted_result = sorted(result, key = lambda x: float(x[1]), reverse = True)[:number_of_results]

    # format the results a little:
    return [(str(k+1), label.replace('&colon;',':'), float_to_int(100*value)) for k,(label,value) in enumerate(sorted_result) ]

# pretty print a table:
# table print tweaked from here: http://stackoverflow.com/questions/25403249/print-a-list-of-tuples-as-table
def print_table(table):
    max_length_column = []
    tuple_len = len(table[0])     # assume entire table has the same shape as the first row
    for i in range(tuple_len):
        max_length_column.append(max(len(e[i])+2 for e in table))    
    for e in table:
        for i in range(tuple_len):
            print(e[i].ljust(max_length_column[i]), end='')
        print()

# invoke it:
sw_dict = load_clean_sw_into_set_dict(source, op)

result = find_wikivec_similarity(sw_dict, wikipage, number_of_results)
print_table(result)
print()


# interactive wiki similarity:
if interactive:
    while True:
        line = input("Enter table row number, or wikipage: ")
        line = line.strip()
        if len(line) == 0:
            continue

        # exit the agent:
        if line in ['q','quit','exit']:
            break

        try:
            line = int(line)
            wikipage = result[line-1][1]
        except:
            wikipage = line

        result = find_wikivec_similarity(sw_dict, wikipage, number_of_results)
        print_table(result)
        print()
  
