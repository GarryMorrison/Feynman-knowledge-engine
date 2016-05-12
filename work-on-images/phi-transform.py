#!c:/Python34/python.exe

#######################################################################
# Convert an image to superposition, find similar layer-1, then map back to an image
# Calling this a phi-transform. More details later.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-04-14
# Update: 2016-5-12
# Copyright: GPLv3
#
# Usage: ./create-image-sw.py ngram-size image.{png,jpg} [image2 image3 ... ]
#
#######################################################################


import os
import sys
import glob
from PIL import Image
import numpy

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("phi transform of images")
context2 = context_list("images to phi superpositions")
#context.load("sw-examples/mnist-test-1--0_5-similarity.sw")
#context.load("sw-examples/mnist-1000--layer-1--0_5.sw")
#context.load("sw-examples/small-lenna-edge-40--layer-1--0_7.sw")
#context.load("sw-examples/small-lenna-edge-40--layer-1--0_4.sw")
#context.load("sw-examples/mnist-10000-train--k_5--t_0_5--layer-1.sw")
context.load("sw-examples/mnist-10000-train--k_5--t_0_4--layer-1.sw")
#sys.exit(0)

if len(sys.argv) < 3:
  print("\nUsage:")
  print("  ./create-image-sw.py ngram-size image.{png,jpg}")
  sys.exit(1)

try:
  ngram_size = int(sys.argv[1])
except:
  ngram_size = 10

#list_of_files = sys.argv[2:]
file_dir = sys.argv[2]
#print("files:",list_of_files)
#sys.exit(0)

destination_phi_transform = "work-on-handwritten-digits/phi-transformed-images/"
destination_phi_images = "work-on-handwritten-digits/phi-images/"
#image_mode = "RGB"
image_mode = "L"

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

def sp_to_image(sp,d=5):                        # assumes the sp is rescaled to 255 (so range is [0,255] )
#  d = 10                                    # hard wire in d = 10. This fixed the bug.
#  d = 5
  if len(sp) != d*d:                        # loaded into console, shows all have len 100.
    print("wrong length! len sp:",len(sp))
    sys.exit(1)
  size = (d,d)
  data = [ int(x.value) for x in sp ]
  im = Image.new('L',size)                  # assume this, rather than RGB. Will work for now.
  im.putdata(data)
#  im.save(destination + "mnist-test-1--phi-image-%s.bmp" % count)
  return im

def sp_to_rgb_image(sp):                    # assumes the sp is rescaled to 255 (so range is [0,255] )
  d = 10                                    # hard wire in d = 10. This fixed the bug.
  if len(sp) != 3*d*d:
    print("wrong length! len sp:",len(sp))
  size = (d,d)
  data = [ int(x.value) for x in sp ]
  im_data = [ (data[i],data[i+1],data[i+2]) for i in range(0,len(data),3) ]
  im = Image.new('RGB',size)
  im.putdata(im_data)
  return im

# does phi-transform even use this function??
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
    print("image_to_ngrams reason:",e)
    return

# some of the numpy code is from here:
# http://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
def phi_transform_image(context,name,k):
  try:
    base = os.path.basename(name)
    filehead,ext = base.rsplit('.',1)
    im = Image.open(name)
    width,height = im.size
    if image_mode == "L":
      arr = numpy.zeros((height,width),numpy.float)
    elif image_mode == "RGB":
      arr = numpy.zeros((height,width,3),numpy.float)
    count = 0
    image_phi_sp = fast_superposition()
    for h in range(0,height-k):
      for w in range(0,width-k):
        count += 1
        im2 = im.crop((w,h,w + k,h + k))
        our_sp = image_to_sp(im2)
        phi = our_sp.similar_input(context,"layer-1").select_range(1,1).ket()
        if phi.label == "":
          continue
        phi_similarity = phi.value
        image_phi_sp += phi                                   # map image to phi sp
        phi_sp = phi.apply_op(context,"layer-1").rescale(255)
        tweaked_phi_sp = phi_sp.apply_sigmoid(subtraction_invert,255).multiply(phi_similarity).apply_sigmoid(subtraction_invert,255)
        if image_mode == "L":
          phi_im = sp_to_image(tweaked_phi_sp)                          # tidy this later!
          im3 = Image.new('L',(width,height),"white")
        elif image_mode == "RGB":
          phi_im = sp_to_rgb_image(tweaked_phi_sp)
          im3 = Image.new('RGB',(width,height),"white")
        print("phi:",phi)
        print("phi sp:",phi_sp)
        im3.paste(phi_im,(w,h))
#        im3.save(destination + "mnist-test-1--phi-image-%s-%s.bmp" % (w,h))
        image_array = numpy.array(im3,dtype=numpy.float)
#        arr += image_array * phi_similarity
        arr += image_array

        # see what we have:
#        phi_im.show()
#        im3.show()
#        if count > 1000:
#          sys.exit(0)
#          break
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
    if image_mode == "L":
      out=Image.fromarray(arr,mode="L")
    elif image_mode == "RGB":
      out=Image.fromarray(arr,mode="RGB")
#    out.save("Average.png")
    out.save("%s%s.png" % (destination_phi_transform,filehead))
#    out.show()
    return image_phi_sp.superposition()
  except Exception as e:
    print("phi_transform_image reason:",e)
    return superposition()


#for filename in list_of_files:
# if given a directory:
#if os.path.isdir(file_dir):         # assume it exists, so I don't need to change indent.
for filename in glob.glob(file_dir + "/*"):

#  image_to_ngrams(context,filename,ngram_size)
  image_phi_sp = phi_transform_image(context,filename,ngram_size)
  base = os.path.basename(filename)
  filehead,ext = base.rsplit('.',1)
  context2.learn("phi-sp","image: " + filehead,image_phi_sp)  

  # convert image_phi_sp to an actual image:
#  empty = show_range(ket("phi: 1"),ket("phi: 289")).multiply(0)           # hard code in 289 just for now!
  empty = show_range(ket("phi: 1"),ket("phi: 289"))           # don't mult by 0, so coeffs are in [1,... instead of [0,...
  sp = (image_phi_sp + empty).ket_sort().apply_sigmoid(log).rescale(255)
  print("phi-sp:",sp)
  context2.learn("log-phi-sp","image: " + filehead,sp.drop())
  phi_image = sp_to_image(sp,17)
#  phi_image.show()  
  phi_image.save("%s%s.png" % (destination_phi_images,filehead))

context2.save("sw-examples/image-phi-superpositions-test-1000--%s--t_0_4.sw" % str(ngram_size))


#context.print_universe()
#context.save("sw-examples/image-ngram-superpositions-%s.sw" % str(ngram_size))


