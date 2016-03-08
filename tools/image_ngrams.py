#!c:/Python34/python.exe

#######################################################################
# convert image into k*k squares, for later image processing. 
# the next step will be image-to-sp, and then a tweaked average-categorize:
# described here: http://write-up.semantic-db.org/123-new-function-average-categorize.html
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-07
# Update:
# Copyright: GPLv3
#
# Usage: ./image_ngrams.py image.{png,jpg} [ngram-size]
#
# eg: ./image_ngrams.py Lenna.png
# eg: ./image_ngrams.py Lenna.png 50
#
#######################################################################

import sys
import os
from PIL import Image

if len(sys.argv) < 2:
  print("\nUsage:")
  print("  ./image_ngrams.py image.{png,jpg} [ngram-size]")
  sys.exit(1)
filename = sys.argv[1]

try:
  ngram_size = int(sys.argv[2])
except:
  ngram_size = 5                  # set default to 5*5 image partition

try:
  im = Image.open(filename)
except:
  print("couldn't open image file:",filename)
  sys.exit(1)

destination = "image-ngrams/"
# check if destination directory exists:
if not os.path.exists(destination):
  print("Creating " + destination + " directory.")
  os.makedirs(destination)



def image_ngrams(name,image,k):
  filehead,ext = name.rsplit('.',1)
  width,height = image.size
  for h in range(0,height-k):
    for w in range(0,width-k):
      im2 = image.crop((w,h,w + k,h + k))
      file_destination = "%s%s--%s-%s-%s.%s" % (destination,filehead,str(k),str(w),str(h),ext)
      im2.save(file_destination)

image_ngrams(filename,im,ngram_size)

