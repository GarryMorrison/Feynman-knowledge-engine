#!c:/Python34/python.exe

#######################################################################
# convert sw file to images
# usage in converting average-categorize back to images, to see what it has done.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-04-10
# Update: 2016-4-12
# Copyright: GPLv3
#
# Usage: ./create-sw-images.py
#
#######################################################################


import sys
import math
from PIL import Image

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("average categorized rescaled superpositions to images")

#context.load("sw-examples/mnist-1--save-average-categorize--0_9--rescaled-layer-1.sw")
#context.load("sw-examples/mnist-1--save-average-categorize--0_8--rescaled-layer-1.sw")
#context.load("sw-examples/mnist-100--save-average-categorize--0_8.sw")
#context.load("sw-examples/mnist-100--save-average-categorize--0_5.sw")
#context.load("sw-examples/mnist-100--save-average-categorize--0_6.sw")
#context.load("sw-examples/mnist-100--save-average-categorize--0_7.sw")
#context.load("sw-examples/mnist-100--save-average-categorize--0_65.sw")
#context.load("sw-examples/mnist-1000--layer-1--0_5.sw")
#context.load("sw-examples/small-lenna-edge-40--layer-1--0_7.sw")
context.load("sw-examples/small-lenna-edge-40--layer-1--0_4.sw")


#filename = sys.argv[1]
#op = "rescaled-layer-1"
op = "layer-1"
destination = "work-on-handwritten-digits/average-categorize-images/"      # don't test for existance. Maybe later.

def sp_to_image(sp,count):                  # assumes the sp is rescaled to 255 (so range is [0,255] )
#  d_squared = len(sp)
#  d = int(math.sqrt(d_squared))            # bug must be with this line.
  d = 10                                    # hard wire in d = 10. This fixed the bug.
  if len(sp) != 100:                        # loaded into console, shows all have len 100.
    print("len sp:",len(sp))
  size = (d,d)
  data = [ int(x.value) for x in sp ]
  im = Image.new('L',size)                  # assume this, rather than RGB. Will work for now.
  im.putdata(data)
  im.save(destination + "mnist-1000--average-image-%s.bmp" % count)


def sp_to_rgb_image(sp,count):                  # assumes the sp is rescaled to 255 (so range is [0,255] )
  d = 10                                    # hard wire in d = 10. This fixed the bug.
  if len(sp) != 300:         
    print("len sp:",len(sp))
  size = (d,d)
  data = [ int(x.value) for x in sp ]
  im_data = [ (data[i],data[i+1],data[i+2]) for i in range(0,len(data),3) ]
  im = Image.new('RGB',size)
#  im.putdata(data)
  im.putdata(im_data)
  im.save(destination + "small-lenna-edge-40--average-image-%s.bmp" % count)


count = 0
for elt in context.relevant_kets(op):
  count += 1
  print("elt:",elt)
  our_sp = context.recall(op,elt).rescale(255)
#  sp_to_image(our_sp,count)
  sp_to_rgb_image(our_sp,count)
  print("sp:",our_sp)

