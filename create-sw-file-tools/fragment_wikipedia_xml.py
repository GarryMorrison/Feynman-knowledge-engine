#!/usr/bin/env python3

#######################################################################
# wiki.xml at 50 GB is just too large to work with.
# plan is for this code to split it into smaller, manageable pieces
#
# Author: Garry Morrison
# email: garry@semantic-db.org
# Date: 2015-05-27
# Update: 2015-05-30
# Copyright: public domain
#
# Usage: ./fragment_wikipedia_xml.py wiki.xml [pages-per-fragment]
# wiki.xml from here: http://en.wikipedia.org/wiki/Wikipedia:Database_download
# eg: $ bzip2 -dc enwiki-20150515-pages-articles.xml.bz2 > wiki.xml
#
#######################################################################


import sys
import os

if len(sys.argv) < 2:
  print("\nUsage: ./fragment_wikipedia_xml.py wiki.xml [pages-per-fragment]\n\n")
  sys.exit(0)

document = sys.argv[1]

# how many pages per fragment:
how_many_pages = 1
if len(sys.argv) == 3:
  how_many_pages = int(sys.argv[2])

print("\nwiki xml file     ",document)
print("pages per fragment",how_many_pages)


destination_dir = "data/fragments/"
if not os.path.exists(destination_dir):
  os.makedirs(destination_dir)


def ascii_filter(s):
# filter down to ascii only:
  return s.encode('ascii','ignore').decode('ascii')

is_text = False
page_count = 0
page_buffer = ""
fragment_id = 0

with open(document,'r',encoding='utf8') as f:
  for line in f:
    row = ascii_filter(line).strip().rstrip()
    if row.startswith("<page>") or row.startswith("</page>") or row.startswith("<title>"):
      page_buffer += row + "\n"
    elif row.startswith("<text ") and row.endswith(" />"):
      page_buffer += "<text xml:space=\"preserve\"> </text>\n"
    elif row.startswith("<text "):
      is_text = True
    if is_text:
      page_buffer += row + "\n"
      if row.endswith("</text>"):
        is_text = False
    if row.startswith("</page>"):
      page_count += 1
      if page_count >= how_many_pages:
        file = destination_dir + str(fragment_id) + ".xml"
        dest = open(file,'w')
        dest.write(page_buffer)
        dest.close()
        print(fragment_id)
        page_count = 0
        fragment_id += 1
        page_buffer = ""        

