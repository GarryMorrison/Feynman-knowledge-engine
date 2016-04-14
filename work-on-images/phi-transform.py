#!c:/Python34/python.exe

#######################################################################
# Convert an image to superposition, find similar layer-1, then map back to an image
# Calling this a phi-transform. More details later.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-04-14
# Update:
# Copyright: GPLv3
#
# Usage: ./create-image-sw.py ngram-size image.{png,jpg} [image2 image3 ... ]
#
#######################################################################


import os
import sys
from PIL import Image
import numpy

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("images to ngram superpositions")
context.load("sw-examples/mnist-test-1--0_5-similarity.sw")
#sys.exit(0)

if len(sys.argv) < 3:
  print("\nUsage:")
  print("  ./create-image-sw.py ngram-size image.{png,jpg}")
  sys.exit(1)

try:
  ngram_size = int(sys.argv[1])
except:
  ngram_size = 10

list_of_files = sys.argv[2:]
#print("files:",list_of_files)
#sys.exit(0)

destination = "work-on-handwritten-digits/phi-images/"

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

def sp_to_image(sp):                        # assumes the sp is rescaled to 255 (so range is [0,255] )
  d = 10                                    # hard wire in d = 10. This fixed the bug.
  if len(sp) != 100:                        # loaded into console, shows all have len 100.
    print("len sp:",len(sp))
  size = (d,d)
  data = [ int(x.value) for x in sp ]
  im = Image.new('L',size)                  # assume this, rather than RGB. Will work for now.
  im.putdata(data)
#  im.save(destination + "mnist-test-1--phi-image-%s.bmp" % count)
  return im


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

# some of the numpy code is from here:
# http://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
def phi_transform_image(context,name,k):
  try:
    base = os.path.basename(name)
    filehead,ext = base.rsplit('.',1)
    im = Image.open(name)
    width,height = im.size
    arr = numpy.zeros((height,width),numpy.float)
    count = 0
    for h in range(0,height-k):
      for w in range(0,width-k):
        count += 1
        im2 = im.crop((w,h,w + k,h + k))
        our_sp = image_to_sp(im2)
        phi = our_sp.similar_input(context,"layer-1").select_range(1,1).ket()
        phi_similarity = phi.value
        phi_sp = phi.apply_op(context,"layer-1").rescale(255)
        tweaked_phi_sp = phi_sp.apply_sigmoid(subtraction_invert,255).multiply(phi_similarity).apply_sigmoid(subtraction_invert,255)
        phi_im = sp_to_image(tweaked_phi_sp)
        print("phi:",phi)
        print("phi sp:",phi_sp)
        im3 = Image.new('L',(width,height),255)
        im3.paste(phi_im,(w,h))
#        im3.save(destination + "mnist-test-1--phi-image-%s-%s.bmp" % (w,h))
        image_array = numpy.array(im3,dtype=numpy.float)
#        arr += image_array * phi_similarity
        arr += image_array
    arr = arr/count            # average the final array

    # normalize to range [0,255]:
    image_min = numpy.amin(arr)
    print("image min:",image_min)
    arr -= image_min
    new_max = numpy.amax(arr)
    arr *= 255/new_max

    # Round values in array and cast as 8-bit integer
    arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)

    # Generate, save and preview final image
    out=Image.fromarray(arr,mode="L")
#    out.save("Average.png")
    out.save("%s%s.png" % (destination,filehead))
#    out.show()
  except Exception as e:
    print("reason:",e)
    return


for filename in list_of_files:
#  image_to_ngrams(context,filename,ngram_size)
  phi_transform_image(context,filename,ngram_size)

#context.print_universe()
#context.save("sw-examples/image-ngram-superpositions-%s.sw" % str(ngram_size))


