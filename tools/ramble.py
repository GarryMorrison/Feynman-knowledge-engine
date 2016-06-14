#!/usr/bin/env python3

#######################################################################
# ramble using a given text file
#
# Author: Garry Morrison & procrasti
# email: garry -at- semantic-db.org
# Date: 2016-06-12
# Update: 2016-6-14
# Copyright: GPLv3
#
# Usage: ./ramble.py [source-text ramble-type ramble-len]
#
# References:
# http://write-up.semantic-db.org/151-introducing-the-ngram-stitch.html
# http://write-up.semantic-db.org/152-some-rambler-examples.html
# http://write-up.semantic-db.org/153-some-letter-rambler-examples.html
# http://write-up.semantic-db.org/167-revisiting-the-letter-rambler.html
#
# some sample source text:
# http://k5.semantic-db.org/extracted-kuron-text/tidy-rusty.txt
# http://k5.semantic-db.org/extracted-kuron-text/tidy-procrasti.txt
# http://k5.semantic-db.org/extracted-kuron-text/tdillo.txt
# http://k5.semantic-db.org/extracted-kuron-text/Cable4096.txt
# http://k5.semantic-db.org/extracted-kuron-text/complete-k5-posts.zip
#
#######################################################################

import os
import sys
import re
import random

# choose verbose ramble mode:
#verbose = False
verbose = True

# define our bare-bones superposition class:
class superposition(object):
  def __init__(self):
    self.dict = {}

  def add(self,str):
    if str in self.dict:
      self.dict[str] += 1
    else:
      self.dict[str] = 1

  def pick_elt(self):
    return random.choice(list(self.dict.keys()))       # improve this!! Is there a more efficient way? Does it matter?

  # tweaked from here: http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
  # need to test it! Seems to work better than pick_elt(), so must be right :)
  #
  # picks a string from the dictionary with probability of the value of that dictionary key
  def weighted_pick_elt(self):
    if len(self.dict) == 0:
      return ""
    total = sum(self.dict.values())
    r = random.uniform(0,total)
    upto = 0
    for key,value in self.dict.items():
      if upto + value > r:
        return key
      upto += value


# create 3/2 word ngrams:
def create_ngram_word_pairs(s):
  return [[" ".join(s[i:i+3])," ".join(s[i+3:i+5])] for i in range(len(s) - 4)]

# create 3/2 letter ngrams:
def create_ngram_letter_pairs(s):
  return [[s[i:i+3],s[i+3:i+5]] for i in range(len(s) - 4)]

# extract the last 3 words from a string:
def extract_3_word_tail(one):
  split_str = one.rsplit(' ',3)
  if len(split_str) < 4:
    return one
  return " ".join(split_str[1:])

# extract the last 3 letters from a string:
def extract_3_letter_tail(one):
  return one[-3:]

# learn word ngram pairs:
# should probably merge the learn_ngram_word and learn_ngram_letter code!
# since only 1 line of code difference.
def learn_ngram_word_pairs(text):
    ngram_dict = {}
    clean_text = re.sub('[<|>=\r\n]',' ',text)
    for head,tail in create_ngram_word_pairs(clean_text.split()):
      try:
        if head not in ngram_dict:
          ngram_dict[head] = superposition()
        ngram_dict[head].add(tail)
      except:
        continue
    return ngram_dict

# learn ngram letter pairs:
def learn_ngram_letter_pairs(text):
    ngram_dict = {}
    clean_text = re.sub('[<|>=\r\n]',' ',text)
    for head,tail in create_ngram_letter_pairs(clean_text):
      try:
        if head not in ngram_dict:
          ngram_dict[head] = superposition()
        ngram_dict[head].add(tail)
      except:
        continue
    return ngram_dict

# format word ramble into fake paragraphs:
# big readability improvement!
# is it just me, or has this stopped working?
def format_fake_paragraphs(text):
    paragraph_lengths = [1,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,5]
    dot_found = False
    dot_count = 0
    
    last_complete = ''

    result = ""
    for c in text:
        if c == ".":
          dot_found = True
          result += c
          last_complete = result
        elif c == " " and dot_found:
            dot_found = False
            dot_count += 1
            if dot_count == random.choice(paragraph_lengths) or dot_count >= max(paragraph_lengths):
                result+="\n"
                dot_count = 0
            else:
                result+=c
        else:
            dot_found = False
            result+=c
    return last_complete

# format word ramble into fake paragraphs:
def print_fake_paragraphs(str):
  print(format_fake_paragraphs(str))
  return

# format letter ramble:
# I don't know what to put here yet!
def print_fake_poem(str):
  print(str)

def generate_ramble(text, ramble_len, learn_ngram_pairs = learn_ngram_word_pairs, extract_3_tail = extract_3_word_tail, gram_space_char = " "):
    ngrams = learn_ngram_pairs(text)
    ramble_len = int(ramble_len) // 2    # since each step of the ramble generates 2 new elements, what?
    ramble = random.choice(list(ngrams.keys()))       # optimize this?
    if verbose:
      print("seed:",ramble)

    # now generate the ramble:
    for _ in range(ramble_len):
      try:
        tail = extract_3_tail(ramble)
        # next_gram = ngrams[tail].pick_elt()           # for word ramble, not much difference. For letter ramble a big difference!
        next_gram = ngrams[tail].weighted_pick_elt()
      except Exception as e:
        print("Excepion reason:",e)
        break

      if verbose:
        print("tail:",tail)
        print("next:",next_gram)
      ramble += gram_space_char + next_gram
    return ramble

def word_ramble(text, ramble_len):
    result = generate_ramble(text, ramble_len)
    result  = format_fake_paragraphs(result)
    return result
    
def letter_ramble(text, ramble_len):
    result = generate_ramble(text, ramble_len, learn_ngram_pairs = learn_ngram_letter_pairs, extract_3_tail = extract_3_letter_tail, gram_space_char = "")
    return result
    
if False and     __name__=="__main__":
    filename = "brother.txt"                           # I wonder what procrasti has in his sample text file? 
    ramble_len = 200
    text = ''
    with open(filename,'r') as f:
        text = f.read()
    print(word_ramble(text, ramble_len))

if __name__=="__main__":
    valid_params = False
    # try to load parameters from the command line:
    if len(sys.argv) == 4:
      filename = sys.argv[1]
      ramble_type = sys.argv[2].lower()
      ramble_len = sys.argv[3]

      # verify them:
      if os.path.isfile(filename) and ramble_type in ['w','l'] and ramble_len.isdigit():
        valid_params = True


    if not valid_params:
      # find file to load:
      filename = input("Enter source text file: ")
      while not os.path.isfile(filename):
        filename = input(filename + " not found. Enter source text file: ")

      # choose ramble type, word or letter:
      ramble_type = input("(w)ord or (l)etter ramble: ").lower()
      while ramble_type not in ['w','l']:
        ramble_type = input("(w)ord or (l)etter ramble: ").lower()

      # find number of word/letters to ramble:
      if ramble_type == 'l':
        question_text = "how many letters to ramble: "
      else:
        question_text = "how many words to ramble: "
      ramble_len = input(question_text)
      while not ramble_len.isdigit():
        ramble_len = input(question_text)

    if verbose:
        print("working ... \n")

    # learn our ngrams:
    with open(filename,'r') as f:
        text = f.read()
        if ramble_type == 'w':
          result = word_ramble(text, ramble_len)
        else:
          result = letter_ramble(text, ramble_len)

    if verbose:
        print("\n------------------------------")    
    # now print it all out:
    print(result)
