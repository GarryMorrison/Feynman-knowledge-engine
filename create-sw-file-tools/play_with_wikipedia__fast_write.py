#!/usr/bin/env python3

#######################################################################
# try and extract url data from wikipedia
# write out as we go version
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015-05-26
# Update: 2015-07-21
# Copyright: GPLv3
#
# Usage: ./play_with_wikipeida__fast_write.py data/fragments/0.xml
#
#######################################################################

import sys
from bs4 import BeautifulSoup

document = open(sys.argv[1],'rb')
soup = BeautifulSoup(document)

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("wikipedia links")

if not os.path.exists("sw-results"):
  os.makedirs("sw-results")
prefix = sys.argv[1].rsplit('/',1)[-1].split('.')[0]
destination = "sw-results/" + prefix + "--30k--wikipedia-links.sw"

print(destination)
#sys.exit(0)

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
  link = link.replace(' ','_') #.lower()   # lower case too? Yup! (I think ...) Nope! Quick test, results are bad. Titles are hard to read in lowercase.
  link = chomp_bad_chars(link)
  return ket("WP: " + link)

print(soup.sitename)

dest = open(destination,'w')

for page in soup.find_all('page'):
  try:
    print("title:",page.title)
    text =  ascii_filter(page.find('text').text)
#  print("text:",text)
    r = extract_links(text)
#  print("r:",r)
    page_name_ket = ket("WP: " + page.title.text.replace(' ','_')) #.lower())
    print("name:",page_name_ket)
    print()

#    result = superposition()
#    result.data = [ket_process_link(x) for x in r]  # what if duplicate links?
#    result = superposition()                         # not sure how slow this will be.
#    for x in r:
#      result += ket_process_link(x)
    result = fast_superposition()
    for x in r:
      result += ket_process_link(x)
    dest.write("links-to " + str(page_name_ket) + " => " + str(result.superposition().coeff_sort()) + "\n\n")
  except:
    continue
dest.close()
