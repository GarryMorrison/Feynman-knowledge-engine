#!c:/Python34/python.exe

#######################################################################
# Convert an image to a sw file. Later, will try for several images in one go.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-04-08
# Update:
# Copyright: GPLv3
#
# Usage: ./create-image-sw.py ngram-size image.{png,jpg} [image2 image3 ... ]
#
#######################################################################


import os
import sys
import glob
from PIL import Image

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = new_context("images to ngram superpositions")


if len(sys.argv) < 3:
  print("\nUsage:")
  print("  ./create-image-sw.py ngram-size image.{png,jpg}")
  sys.exit(1)

try:
  ngram_size = int(sys.argv[1])
except:
  ngram_size = 10

#list_of_files = sys.argv[2:]                   # too many command line arguments, use directory instead:
file_dir = sys.argv[2]

#print("files:",list_of_files)
#sys.exit(0)

def first_image_to_sp(image):                   # if the image is square, then this mapping to sp is invertable
  width,height = image.size
  i = 1
  r = fast_superposition()
  for h in range(0,height):
    for w in range(0,width):
      R,G,B = image.getpixel((w,h))[:3]
      r += ket(str(i),R) + ket(str(i+1),G) + ket(str(i+2),B)
      i += 3
  return r.superposition()

def image_to_sp(image):
  data = list(image.getdata())
  mode = image.mode
  print("data:",data)
  print("mode:",mode)
  r = superposition()
  if mode == "L":
    r.data = [ ket(str(k),value) for k,value in enumerate(data) ]
    return r
  if mode in ["RGB","RGBA"]:
    k = 0
    for value in data:
      R,G,B = value[:3]
      r.data.append(ket(str(k),R))
      r.data.append(ket(str(k+1),G))
      r.data.append(ket(str(k+2),B))
      k += 3
    return r

def image_to_ngrams(context,name,k):
  try:
    base = os.path.basename(name)
    filehead,ext = base.rsplit('.',1)
    im = Image.open(name)
    width,height = im.size
    for h in range(0,height-k):
      for w in range(0,width-k):
        im2 = im.crop((w,h,w + k,h + k))
        ket_name = "%s: %s: %s: %s" % (filehead,str(k),str(w),str(h))
        r = image_to_sp(im2)
        context.learn("layer-0",ket_name,r)
  except Exception as e:
    print("reason:",e)
    return

#for filename in list_of_files:
#  image_to_ngrams(context,filename,ngram_size)

# if given a directory:
if os.path.isdir(file_dir):
  for name in glob.glob(file_dir + "/*"):
    try:
      image_to_ngrams(context,name,ngram_size)
#      context.append_save("sw-examples/image-ngram-superpositions-%s.sw" % str(ngram_size))
#      context = new_context("images to ngram superpositions")
    except:
      print("couldn't open image file:",name)

#context.print_universe()
#context.save("sw-examples/image-ngram-superpositions-%s.sw" % str(ngram_size))


