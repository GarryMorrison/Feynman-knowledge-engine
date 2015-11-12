#!/usr/bin/env python3

#######################################################################
# try and extract url data from wikipedia
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015-05-24
# Update:
# Copyright: GPLv3
#
# Usage: ./play_with_wikipeida.py wiki.xml
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


#r = ['political philosophy', 'stateless society|stateless societies', 'self-governance|self-governed', 'Hierarchy|hierarchical', 'Free association (communism and anarchism)|free associations', 'Peter Kropotkin', 'An Anarchist FAQ', 'state (polity)|state', 'The Globe and Mail']

#for x in r:
#  print("x:",x)
##  print("links:",process_anchor_text(x))
#  link, anchor = ket_process_anchor_text(x)
#  print("link:",link)
#  print("anchor:",anchor)

#sys.exit(0)
print(soup.sitename)
#print(soup.prettify())
#print(soup.page.text)

for page in soup.find_all('page'):
  try:
    print("title:",page.title)
    text =  ascii_filter(page.find('text').text)
#  print("text:",text)
    r = extract_links(text)
#  print("r:",r)
    page_name_ket = ket("WP: " + page.title.text.replace(' ','_'))
    print("name:",page_name_ket)
    print()

# now learn it all:
    for x in r:
      link, anchor = ket_process_anchor_text(x)
      C.add_learn("links-to",page_name_ket,link)
      C.add_learn("inverse-links-to",link,page_name_ket)

      C.add_learn("contains-anchor",page_name_ket,anchor)
      C.add_learn("inverse-contains-anchor",anchor,page_name_ket)

      C.add_learn("links-to",anchor,link)
      C.add_learn("inverse-links-to",link,anchor)
  except:
    continue

#print(C.dump_universe())
save_sw(C,"wikipedia-links.sw",False)
