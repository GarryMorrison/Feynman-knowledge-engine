#!/usr/bin/env python3

#######################################################################
# 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2015-06-30
# Update: 2016-2-8
# Copyright: GPLv3
#
# Usage: ./blog-to-html.py source-directory destination-directory pages
#
#######################################################################


import sys
import os
import glob
import datetime

if len(sys.argv) < 4:
  print("\nUsage: ./blog-to-html.py source-directory destination-directory pages\n")
  sys.exit(0)

source = sys.argv[1]
destination = sys.argv[2]
pages = int(sys.argv[3])

# check it exists, if not exit:
if not os.path.exists(source):
  print("\n",source,"not found. Exiting ...\n")
  sys.exit(0)

# check it exists, if not create it:
if not os.path.exists(destination):
  print("Creating",destination,"directory.")
  os.makedirs(destination)


print("source-directory:",source)
print("destination-directory:",destination)
print("pages:",pages,"\n")

def process_page(destination,file,title,k):
  page_header = '<html>\n<head><title>%s</title></head>\n<body>\n<h1>%s</h1>\n\n' % (title,title)

  null, previous_url, previous_title = find_page(k-1)
  null, next_url, next_title = find_page(k+1)

  page_footer = '<br><br>\n<hr>\n<a href="index.html">Home</a><br>\n'

  if previous_title != '':
    page_footer += 'previous: <a href="%s">%s</a><br>\n' % (previous_url,previous_title)

  if next_title != '':
    page_footer += 'next: <a href="%s">%s</a><br>\n' % (next_url,next_title)

  now = datetime.datetime.now()
  date = now.strftime('%d/%m/%Y')

  page_footer += '<br>\nupdated: %s<br>\n' % date
  page_footer += 'by Garry Morrison<br>\nemail: garry -at- semantic-db.org<br>\n'
  page_footer += '\n</body>\n</html>\n'
  
  page = page_header
  with open(file) as f:
    page += f.read()
  page += page_footer
  
  destination = destination.rstrip('/') + "/" + os.path.basename(file)
  dest = open(destination,'w')
  dest.write(page)
  dest.close()

def find_page(k):
  try:
    prefix = str(k+1) + "-"
    file = glob.glob(source + "/" + prefix + "*.html")[0]
    page_url = os.path.basename(file)

    title = page_url.replace("-"," ").replace(".html","")
    title = title.split(" ",1)[1]

    return file, page_url, title
  except:
    return "", "", ""


index_page = ""
with open(source + "/document-header.txt") as f:
  index_page += f.read()

index_page += "<ol>\n"

for k in range(pages):
  file, page_url, title = find_page(k)
  if file != "":
    print("title:",title)
    process_page(destination,file,title,k)
    index_page += '<li><a href="%s">%s</a></li>\n' % (page_url,title)
    previous_title = title
  else:
    continue

index_page += "</ol>\n\n"
with open(source + "/document-footer.txt") as f:
  index_page += f.read()
print(index_page)

dest = open(destination.rstrip('/') + "/index.html",'w')
dest.write(index_page)
dest.close()

