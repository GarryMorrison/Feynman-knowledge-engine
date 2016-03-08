#!c:/Python34/python.exe

#######################################################################
# convert image ngrams to superpositions, so we can load them into average-categorize
# saves sw file "sw-examples/image-ngram-superpositions.sw"
# I suspect the resulting sw-file will be large!
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-08
# Update:
# Copyright: GPLv3
#
# Usage: ./image_to_sp.py image.{png,jpg} | directory
#
# eg: ./image_to_sp.py image-ngrams/Lenna--10-0-3.png
# eg: ./image_to_sp.py image-ngrams/
#
#######################################################################

import sys
import os
import glob
from PIL import Image

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = new_context("image to sp")


if len(sys.argv) < 2:
  print("\nUsage:")
  print("  ./image_to_sp.py image.{png,jpg} | directory")
  sys.exit(1)
filename = sys.argv[1]


def image_to_sp(image):
  def pixel_ket(type,h,w,r):
    return ket(type + ": " + str(w) + " " + str(h),r)
                                                             
  try:
    width,height = image.size

    pixel_list = superposition()
    pixels = im.load()


    tmp_list_r = [ pixel_ket("R",h,w,pixels[w,h][0]) for w in range(width) for h in range(height) ]  
    tmp_list_g = [ pixel_ket("G",h,w,pixels[w,h][1]) for w in range(width) for h in range(height) ]
    tmp_list_b = [ pixel_ket("B",h,w,pixels[w,h][2]) for w in range(width) for h in range(height) ]

    pixel_list.data += tmp_list_r + tmp_list_g + tmp_list_b
                  
# show the image:
#    im.show()
    return pixel_list
  except:
    return ket("")


# if given a single file:
if os.path.isfile(filename):
  try:
    im = Image.open(filename)
    base = os.path.basename(filename)
    r = image_to_sp(im)
    context.learn("image-sp",base,r)
  except:
    print("couldn't open image file:",filename)
    sys.exit(1)

# if given a directory:
if os.path.isdir(filename):
  for name in glob.glob(filename + "/*"):
    base = os.path.basename(name)
    try:
      im = Image.open(name)
      r = image_to_sp(im)
      context.learn("image-sp",base,r)
    except:
      print("couldn't open image file:",name)


context.print_universe()
context.save("sw-examples/image-ngram-superpositions.sw")
