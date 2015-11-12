#!/usr/bin/env python3

#######################################################################
# extract word frequency lists from wikipedia
# write out as we go version
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015-06-02
# Update:
# Copyright: GPLv3
#
# Usage: ./play_with_wikipeida_freq_list.py wiki.xml
#
#######################################################################

import sys
from bs4 import BeautifulSoup

document = open(sys.argv[1],'rb')
soup = BeautifulSoup(document)

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("wikipedia frequency list")

destination = "30k--wikipedia-frequency-list.sw"

def ascii_filter(s):
# filter down to ascii only:
  return s.encode('ascii','ignore').decode('ascii')

# delete/escape chars we don't want inside kets:
def chomp_bad_chars(s):
# filter down to ascii only, escape \n, delete \r:
  s = s.encode('ascii','ignore').decode('ascii').replace('\n','\\n').replace('\r','')

# some escape:
  s = s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# some more escapes:
  s = s.replace(':','&colon;').replace('|','&pipe;')

  return s
  
def create_word_n_grams(s,N):
  return [" ".join(s[i:i+N]) for i in range(len(s)-N+1)]

def create_freq_list(s,N):
  result = fast_superposition()
  words = [w for w in re.split('[^a-z0-9_\']',s.lower()) if w]
  for gram in create_word_n_grams(words,N):
    result += ket(gram)
  return result.superposition().coeff_sort()

def extract_links(s):
  r = []
  while True:
    try:
      head, tail = s.split('[[',1)
      fragment, s = tail.split(']]',1)
      r.append(fragment)
    except:
      break
  return r

def process_anchor_text(s):
  try:
    link, anchor = s.split('|',1)
  except:
    link = s
    anchor = link
  link = link.replace(' ','_')
  return link, anchor

def ket_process_anchor_text(s):
  try:
    link, anchor = s.split('|',1)
  except:
    link = s
    anchor = link
  link = link.replace(' ','_')
  link = chomp_bad_chars(link)
  anchor = chomp_bad_chars(anchor)
  return ket("WP: " + link), ket("anchor: " + anchor)

def ket_process_link(s):
  try:
    link, anchor = s.split('|',1)
  except:
    link = s
  link = link.replace(' ','_')   # lower case too?
  link = chomp_bad_chars(link)
  return ket("WP: " + link)

print(soup.sitename)

dest = open(destination,'w')

for page in soup.find_all('page'):
  try:
    print("title:",page.title)
    text =  ascii_filter(page.find('text').text)
#  print("text:",text)
#    r = extract_links(text)
    r = create_freq_list(text,1)
#  print("r:",r)
    page_name_ket = ket("WP: " + page.title.text.replace(' ','_'))
    print("name:",page_name_ket)
    print()

#    result = superposition()
#    result.data = [ket_process_link(x) for x in r]  # what if duplicate links?
#    result = superposition()                         # not sure how slow this will be.
#    for x in r:
#      result += ket_process_link(x)
#    result = fast_superposition()
#    for x in r:
#      result += ket_process_link(x)
#    dest.write("links-to " + str(page_name_ket) + " => " + str(result.superposition().coeff_sort()) + "\n\n")
    dest.write("words-1" + str(page_name_ket) + " => " + str(r) + "\n\n")
  except:
    continue
dest.close()
