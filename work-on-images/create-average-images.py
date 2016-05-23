#!c:/Python34/python.exe

#######################################################################
# convert a list of images into k*k tiles, then average categorize them down.
# The plan is to skip almost all of the intermediate sp stuff, and just use lists.
# should be faster, and use much less RAM.
# Yup. It is indeed faster and more RAM efficient!
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-04-08
# Update: 2016-5-10
# Copyright: GPLv3
#
# Usage: ./create-average-images.py ngram-size image-directory
# eg: ./create-average-images.py 5 work-on-handwritten-digits/train-images/
#
#######################################################################


import os
import sys
import glob
from PIL import Image
import numpy as np                      # yeah, another dependence.

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = new_context("images to average image ngrams")


if len(sys.argv) < 3:
  print("\nUsage:")
  print("  ./create-average-images.py ngram-size image-directory")
  sys.exit(1)

try:
  ngram_size = int(sys.argv[1])
except:
  ngram_size = 5

# too many command line arguments so we need to use directory instead:
file_dir = sys.argv[2]

def rescaled_list_simm(f,g):
  the_len = min(len(f),len(g))
  f = f[:the_len]
  g = g[:the_len]

# rescale step, first find size:
  s1 = sum(abs(f[k]) for k in range(the_len))
  s2 = sum(abs(g[k]) for k in range(the_len))

# if s1 == 0, or s2 == 0, we can't rescale:
  if s1 == 0 or s2 == 0:
    return 0
  
# now rescale:
#  f = [f[k]/s1 for k in range(the_len)]  
#  g = [g[k]/s2 for k in range(the_len)]  
  
# proceed with algo:
# if rescaled correctly, wf and wg should == 1.
#  wf = sum(abs(f[k]) for k in range(the_len))
#  wg = sum(abs(g[k]) for k in range(the_len))
# merged rescale:
  wfg = sum(abs(f[k]/s1 - g[k]/s2) for k in range(the_len))
  
  return (2 - wfg)/2


def list_average_categorize_suppress(context,data,t,phi,label):

  def simple_sp_to_list(sp):              # need to test these two, but I think they are correct.
    r = np.array([x.value for x in sp])
    return r
  def list_to_simple_sp(data):
    r = superposition()
    r.data = [ ket(str(k),x) for k,x in enumerate(data) ]
    return r
  def rescale(arr):
    arr = arr - arr.min()
    if arr.max() == 0:
      return arr
    arr = arr*255/arr.max()                            # maybe try rescale to [0,255] later. Bug, what about max == 0?
    return arr
    
  out_list = []
  for r0 in data:
    r = np.array(r0)
    if r.max() == 0:
      continue
    print("r:",r)
    best_k = -1
    best_simm = 0
    for k,sp in enumerate(out_list):
      similarity = rescaled_list_simm(r,sp)
      if similarity > best_simm:
        best_k = k
        best_simm = similarity
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append(r)
    else:
      out_list[best_k] = out_list[best_k] + r*best_simm
  for k,sp in enumerate(out_list):
    print("sp:",sp)
    context.learn(label,phi + ": " + str(k+1),list_to_simple_sp(sp)) 
  return out_list

def image_to_list(image):
  data = list(image.getdata())
  mode = image.mode
  print("data:",data)
  print("mode:",mode)
  if mode == "L":
    return data
  if mode in ["RGB","RGBA"]:
    r = []
    for value in data:
      R,G,B = value[:3]
      r.append(R)
      r.append(G)
      r.append(B)
    return r

def image_to_ngrams(name,k):
  out_list = []
  try:
    base = os.path.basename(name)
    filehead,ext = base.rsplit('.',1)
    im = Image.open(name)
    width,height = im.size
    for h in range(0,height-k):
      for w in range(0,width-k):
        im2 = im.crop((w,h,w + k,h + k))
        r = image_to_list(im2)
        out_list.append(r)
  except Exception as e:
    print("reason:",e)
    return out_list
  return out_list


if os.path.isdir(file_dir):
  result = []
  for name in glob.glob(file_dir + "/*"):
    try:
      result += image_to_ngrams(name,ngram_size)
    except:
      print("couldn't open image file:",name)
  out_list = list_average_categorize_suppress(context,result,0.8,"phi","layer-1")
context.print_universe()
#context.save("sw-examples/mnist-60000-train--k_5--t_0_4--layer-1.sw")
context.save("sw-examples/mnist-60000-train-label-averaged--k_5--t_0_8--layer-1.sw")

# now spit out the average images:
op = "layer-1"
destination = "work-on-handwritten-digits/average-categorize-images/"      # don't test for existance. Maybe later.
d = ngram_size

def sp_to_image(sp,count,d):                  # assumes the sp is rescaled to 255 (so range is [0,255] )
#  d = 10                                    # hard wire in d = 10.
#  d = 4
#  d = 5
  if len(sp) != d*d:                        # loaded into console, shows all have len 100.
    print("len sp:",len(sp))
  size = (d,d)
  data = [ int(x.value) for x in sp ]
  im = Image.new('L',size)                  # assume this, rather than RGB. Will work for now.
  im.putdata(data)
  im.save(destination + "mnist-60k-label-average--k_%s--average-image-%s.bmp" % (d,count))


def sp_to_rgb_image(sp,count,d):                  # assumes the sp is rescaled to 255 (so range is [0,255] )
#  d = 10                                    # hard wire in d = 10. This fixed the bug.
  if len(sp) != 3*d*d:
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
  sp_to_image(our_sp,count,d)
#  sp_to_rgb_image(our_sp,count,d)
  print("sp:",our_sp)

sys.exit(0)

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
context.save("sw-examples/mnist-60000--image-ngram-superpositions-%s.sw" % str(ngram_size))


