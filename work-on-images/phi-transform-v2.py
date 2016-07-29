#!c:/Python34/python.exe

#######################################################################
# Convert an image to superposition, find similar layer-1, then map back to an image
# Calling this a phi-transform. More details later.
#
# Let's try to optimize this thing.
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-07-29
# Update: 
# Copyright: GPLv3
#
# Usage: ./phi-transform-v2.py ngram-size image-directory
#
#######################################################################


import os
import sys
import glob
from PIL import Image
import numpy
import copy

#from the_semantic_db_code import *
#from the_semantic_db_functions import *
#from the_semantic_db_processor import *

if len(sys.argv) < 3:
  print("\nUsage:")
  print("  ./phi-transform-v2.py ngram-size image-directory")
  sys.exit(1)

try:
  ngram_size = int(sys.argv[1])
except:
  ngram_size = 5

#list_of_files = sys.argv[2:]
file_dir = sys.argv[2]
#print("files:",list_of_files)
#sys.exit(0)

# switch verbose printing on and off:
verbose = False
#verbose = True

# assume these exist. ie, don't test first.
destination_phi_transform = "work-on-handwritten-digits/phi-transformed-images-v2/"
destination_phi_images = "work-on-handwritten-digits/phi-images-v2/"
#image_mode = "RGB"
image_mode = "L"

# define our bare-bones superposition class:
class superposition(object):
  def __init__(self):
    self.dict = {}

  def __str__(self):
    list_of_kets = []
    for key,value in self.dict.items():
      if value == 1:
        s = "|%s>" % key
      else:
        s = "%s|%s>" % (value,key)
      list_of_kets.append(s)
    return " + ".join(list_of_kets)

  def __iter__(self):
    for key,value in self.dict.items():
      yield key, value

  def __len__(self):
    return len(self.dict)

  def add(self,str,value=1):
    if str in self.dict:
      self.dict[str] += value
    else:
      self.dict[str] = value

  def pair(self):                               # if the dict is longer than 1 elt, this returns a random pair
    for key,value in self.dict.items():
      return key, value

  def rescale(self,t=1):
    if len(self.dict) == 0:
      return superposition()
#    result = copy.deepcopy(self)
    the_max = max(value for key,value in self.dict.items())
    result = superposition()
    if the_max > 0:
      for key,value in self:
        result.dict[key] = t*self.dict[key]/the_max
    return result


def load_simple_sw_into_dict(filename,op):
  op_head = op + " |"
  sw_dict = {}
  with open(filename,'r') as f:
    for line in f:
      line = line.strip()
      if line.startswith(op_head):
        try:
          head,tail = line.split('> => ',1)
          label = head.split(' |',1)[1]
          sw_dict[label] = superposition()
          for piece in tail[:-1].split('> + '):
            print("piece:",piece)
            float_piece, string_piece = piece.split('|')
            try:            
              float_piece = float(float_piece)
            except:
              float_piece = 1
            sw_dict[label].add(string_piece,float_piece)
        except Exception as e:
          print("Exception reason: %s" % e)
          continue
  return sw_dict

def print_sw_dict(dict):
  for label,sp in dict.items():
    print("|%s> => %s" % (label,sp))

filename = "sw-examples/mnist-60000-train-label-averaged--k_5--t_0_8--layer-1.sw"
sw_dict = load_simple_sw_into_dict(filename,"layer-1")
print_sw_dict(sw_dict)

# simm that is hopefully faster than the one in the full project.
# If not, then go home!
#
def fast_simm(A,B):
  if len(A) == 0 or len(B) == 0:
    return 0
  if len(A) == 1 and len(B) == 1:
    a_label, a_value = A.pair()
    b_label, b_value = B.pair()

    if a_label != b_label:                    # put a.label == '' test in here too?
      return 0
    a = max(a_value,0)                        # just making sure they are >= 0.
    b = max(b_value,0)
    if a == 0 and b == 0:                     # prevent div by zero.
      return 0
    return min(a,b)/max(a,b)
#  return intersection(A.normalize(),B.normalize()).count_sum()     # very slow version!

  # now calculate the superposition version of simm, while trying to be as fast as possible:
  try:
    merged = {}
    one_sum = 0
    one = {}
    for label,value in A:
      one[label] = value
      one_sum += value                     # assume all values in A are >= 0
      merged[label] = True                 # potentially we could use abs(elt.value)

    two_sum = 0
    two = {}
    for label,value in B:
      two[label] = value
      two_sum += value                     # assume all values in B are >= 0
      merged[label] = True

    # prevent div by zero:
    if one_sum == 0 or two_sum == 0:
      return 0

    merged_sum = 0
    for key in merged:
      if key in one and key in two:
        v1 = one[key]/one_sum
        v2 = two[key]/two_sum
        merged_sum += min(v1,v2)
    return merged_sum
  except Exception as e:
    print("fast_simm exception reason: %s" % e)

def pattern_recognition(sw_dict,pattern):
  result = ('',0)
  best_simm = 0
  for label,sp in sw_dict.items():
    similarity = fast_simm(pattern,sp)
    if similarity > best_simm:
      result = (label,similarity)
      best_simm = similarity
  return result


def image_to_sp(image):
  data = list(image.getdata())
  mode = image.mode
  print("data:",data)
  print("mode:",mode)
  r = superposition()
  if mode == "L":
#    r.data = [ ket(str(k),value) for k,value in enumerate(data) ]
    for k,value in enumerate(data):
      r.add(str(k),value)
    return r
  if mode in ["RGB","RGBA"]:                   # fix later! We don't need it for mnist digits.
    k = 0
    for value in data:
      R,G,B = value[:3]
      r.data.append(ket(str(k),R))
      r.data.append(ket(str(k+1),G))
      r.data.append(ket(str(k+2),B))
      k += 3
    return r

def sp_to_image(sp,d=5):                        # assumes the sp is rescaled to 255 (so range is [0,255] )
  if len(sp) != d*d:                        # loaded into console, shows all have len 100.
    print("wrong length! len sp:",len(sp))
    sys.exit(1)
  size = (d,d)
#  data = [ int(x.value) for x in sp ]
#  unsorted_data = []
#  for key,value in sp:                      # NB: these sp's are unsorted! We need to sort by key.
#    unsorted_data.append((key,value))
  unsorted_data = [(key,value) for key,value in sp ]       # doesn't seem to be any faster than data.append version.
#  sorted_data = sorted(unsorted_data, key = lambda x: float(x[0]), reverse = False)
  unsorted_data.sort(key = lambda x: float(x[0]), reverse = False)

  if verbose:
    print("sorted:",unsorted_data)

  data = [ x[1] for x in unsorted_data ]

  im = Image.new('L',size)                  # assume this, rather than RGB. Will work for now.
  im.putdata(data)
#  im.save(destination + "mnist-test-1--phi-image-%s.bmp" % count)
  return im


# now test these last 2 functions: 
# Yup! Works.
#image_filename = "work-on-handwritten-digits/label-average-images/mnist-train-7.bmp"
#im = Image.open(image_filename)
##im.show()
#our_sp = image_to_sp(im)
#print("our_sp:",our_sp)
#print("rescaled our_sp:", our_sp.rescale(255))
#im2 = sp_to_image(our_sp,28)
#im2.show()


#sys.exit(0)


# some of the numpy code is from here:
# http://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
def phi_transform_image(sw_dict,name,k):
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
#    image_phi_sp = superposition()                                                        # switch off image_phi_sp creation, see if it speeds things.
    for h in range(0,height-k):
      for w in range(0,width-k):
        count += 1
        im2 = im.crop((w,h,w + k,h + k))
        our_sp = image_to_sp(im2)
#        phi = our_sp.similar_input(context,"layer-1").select_range(1,1).ket()              # old method, presumably slower.
        phi_label, phi_value = pattern_recognition(sw_dict,our_sp)                          # this better be faster, or I have wasted a lot of time!
        if phi_label == "":
          continue
        phi_similarity = phi_value
#        image_phi_sp += phi                                   # map image to phi sp
#        phi_sp = phi.apply_op(context,"layer-1").rescale(255)
#        tweaked_phi_sp = phi_sp.apply_sigmoid(subtraction_invert,255).multiply(phi_similarity).apply_sigmoid(subtraction_invert,255)

#        image_phi_sp.add(phi_label,phi_value)
        phi_sp = sw_dict[phi_label].rescale(255)
        tweaked_phi_sp = phi_sp                                # look into full tweaked_phi_sp later, since we need sigmoids and multiply.

        if image_mode == "L":
          phi_im = sp_to_image(tweaked_phi_sp)                          
          im3 = Image.new('L',(width,height),"white")
        elif image_mode == "RGB":
          phi_im = sp_to_rgb_image(tweaked_phi_sp)
          im3 = Image.new('RGB',(width,height),"white")

        if verbose:
          print("phi: %s|%s>" % (phi_value,phi_label))
          print("phi sp:",phi_sp)
#        sys.exit(0)

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
#    sys.exit(0)

#    return image_phi_sp
    return None
  except Exception as e:
    print("phi_transform_image reason:",e)
    return superposition()


#for filename in list_of_files:
# if given a directory:
#if os.path.isdir(file_dir):         # assume it exists, so I don't need to change indent.
for filename in glob.glob(file_dir + "/*"):

  image_phi_sp = phi_transform_image(sw_dict,filename,ngram_size)
#  print("image_phi_sp:",image_phi_sp)
#  sys.exit(0)  
  continue

  base = os.path.basename(filename)
  filehead,ext = base.rsplit('.',1)
#  context2.learn("phi-sp","image: " + filehead,image_phi_sp)

  # convert image_phi_sp to an actual image:
#  empty = show_range(ket("phi: 1"),ket("phi: 289")).multiply(0)           # hard code in 289 just for now!
  empty = show_range(ket("phi: 1"),ket("phi: 289"))           # don't mult by 0, so coeffs are in [1,... instead of [0,...
  sp = (image_phi_sp + empty).ket_sort().apply_sigmoid(log).rescale(255)
  print("phi-sp:",sp)
  context2.learn("log-phi-sp","image: " + filehead,sp.drop())
  phi_image = sp_to_image(sp,17)
#  phi_image.show()
  phi_image.save("%s%s.png" % (destination_phi_images,filehead))

#context2.save("sw-examples/image-phi-superpositions--label-average--test-2000--%s--t_0_8.sw" % str(ngram_size))


#context.print_universe()
#context.save("sw-examples/image-ngram-superpositions-%s.sw" % str(ngram_size))


sys.exit(0)
#context = context_list("phi transform of images")
#context2 = context_list("images to phi superpositions")
#context.load("sw-examples/mnist-test-1--0_5-similarity.sw")
#context.load("sw-examples/mnist-1000--layer-1--0_5.sw")
#context.load("sw-examples/small-lenna-edge-40--layer-1--0_7.sw")
#context.load("sw-examples/small-lenna-edge-40--layer-1--0_4.sw")
#context.load("sw-examples/mnist-10000-train--k_5--t_0_5--layer-1.sw")
#context.load("sw-examples/mnist-10000-train--k_5--t_0_4--layer-1.sw")
#context.load("sw-examples/mnist-60000-train-label-averaged--k_5--t_0_8--layer-1.sw")

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

#context2.save("sw-examples/image-phi-superpositions--label-average--test-2000--%s--t_0_8.sw" % str(ngram_size))


#context.print_universe()
#context.save("sw-examples/image-ngram-superpositions-%s.sw" % str(ngram_size))


