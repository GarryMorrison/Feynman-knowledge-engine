#!c:/Python34/python.exe

#######################################################################
# apply edge-enhance, phi-transform, then edge-enhance to an image
# this should strongly highlight edges
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-12-05
# Update: 2017-4-25
# Copyright: GPLv3
#
# Usage: ./edge-transform.py image.{png,jpg}
#
#######################################################################

import os
import sys
from PIL import Image                 # if this line bugs out, you need to install Pillow, a python image library.
import numpy

#filename = "child.png"
#filename = "220px-Lenna.png"
#filename = "angelina-jolie.jpg"
#filename = "lena-headey.jpg"
filename = "portman.jpg"

enhance_factor_pre = 20              # image edge enhance factor before phi-transform
enhance_factor_post = 20             # image edge enhance factor after phi-transform
ngram_size = 10                      # image tile size
threshold = 0.8                      # average categorize threshold
#image_mode = "L"                    # switch between RGB and L mode
image_mode = "RGB"
saved_features_dir = "saved_average_categorize_features-edge"


#base = os.path.basename(name)
#filehead,ext = base.rsplit('.',1)
#im = Image.open(name)


def edge_enhance(image,k):
  width = image.size[0]
  height = image.size[1]
  original_pixels = image.load()

  # create an image with a 1*1 border:
  border_image = image.crop((-1,-1,width + 1,height + 1))
  border_pixels = border_image.load()

  # load the border_image into 3 image matrices, one for each of R,G,B:
  M_r = [[border_pixels[w,h][0] for w in range(width+2)] for h in range(height+2)]
  M_g = [[border_pixels[w,h][1] for w in range(width+2)] for h in range(height+2)]
  M_b = [[border_pixels[w,h][2] for w in range(width+2)] for h in range(height+2)]

  def smooth_pixel(M,w,h):
    r = M[h-1][w-1]/16 + M[h][w-1]/16 + M[h+1][w-1]/16 + M[h-1][w]/16 + M[h][w]/2 + M[h+1][w]/16 + M[h-1][w+1]/16 + M[h][w+1]/16 + M[h+1][w+1]/16
    return r

  # smooth our image matrices:
  # NB: we have to work with matrices and not images because we need to preserve floats at each step of smooth. Otherwise it harms the algo.
  # first, define some work-space matrices:
  new_M_r = [[0 for w in range(width+2)] for h in range(height+2)]
  new_M_g = [[0 for w in range(width+2)] for h in range(height+2)]
  new_M_b = [[0 for w in range(width+2)] for h in range(height+2)]

  # smooth k times:
  for _ in range(k):
    for h in range(height):
      for w in range(width):
        new_M_r[h+1][w+1] = smooth_pixel(M_r,w+1,h+1)
        new_M_g[h+1][w+1] = smooth_pixel(M_g,w+1,h+1)
        new_M_b[h+1][w+1] = smooth_pixel(M_b,w+1,h+1)
    M_r = new_M_r
    M_g = new_M_g
    M_b = new_M_b

  def massage_pixel(x):
    if x < 0:
      x = 0
    x *= 20
    x = int(x)
    if x > 255:
      x = 255
    return 255 - x

  # output the final matrix into image form:
  out_image = Image.new('RGB',(width,height))
  pixels = out_image.load()
  for h in range(height):
    for w in range(width):
      r = massage_pixel(M_r[h+1][w+1] - original_pixels[w,h][0])
      g = massage_pixel(M_g[h+1][w+1] - original_pixels[w,h][1])
      b = massage_pixel(M_b[h+1][w+1] - original_pixels[w,h][2])

      pixels[w,h] = (r,g,b)
#  out_image.show()
  return out_image

#im2 = edge_enhance(im,enhance_factor)
#im2.show()


def rescaled_list_simm(f,g):
  the_len = min(len(f),len(g))
  f = f[:the_len]                     # remove this step?
  g = g[:the_len]

# rescale step, first find size:
  s1 = sum(abs(f[k]) for k in range(the_len))
  s2 = sum(abs(g[k]) for k in range(the_len))

# if s1 == 0, or s2 == 0, we can't rescale:
  if s1 == 0 or s2 == 0:
    return 0
  
  wfg = sum(abs(f[k]/s1 - g[k]/s2) for k in range(the_len))
  
  return 1 - wfg/2


# average categorize the data:
# maybe later replace with a better feature extractor?
# I guess the question is, how well does average-categorize work?
# in testing seems to work not too bad.
#
def list_average_categorize(data,t):
  out_list = []
  for r0 in data:
    r = numpy.array(r0)
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
    print("max k:", len(out_list))
    print("best k:",best_k)
    print("best simm:",best_simm)

    if best_k == -1 or best_simm < t:
      out_list.append(r)
    else:
      out_list[best_k] = out_list[best_k] + r*best_simm       # this line is why we cast r to np array.
  return out_list

def rescale(arr):
  arr = arr - arr.min()
  if arr.max() == 0:
    return arr
  arr = arr*255/arr.max()
  return arr

def image_to_list(image):
  data = list(image.getdata())
  mode = image.mode
  print("data:",data)
  print("mode:",mode)
  if mode == "L":
    return numpy.array(data)
#    return data
  if mode in ["RGB","RGBA"]:
    r = []
    for value in data:
      R,G,B = value[:3]
      r.append(R)
      r.append(G)
      r.append(B)
    return numpy.array(r)
#    return r

def list_to_l_image(data, size):
  if len(data) != size*size:
    return None
  dim = (size, size)
  data = [int(x) for x in rescale(data)]
  im = Image.new('L',dim)  
  im.putdata(data)
  return im

def list_to_rgb_image(data, size):
  if len(data) != 3*size*size:
    return None
  dim = (size, size)
  data = [int(x) for x in rescale(data)]
  im_data = [ (data[i],data[i+1],data[i+2]) for i in range(0,len(data),3) ]
  im = Image.new('RGB',dim)
  im.putdata(im_data)
  return im

def image_to_ngrams(im,k):
  out_list = []
  try:
    width,height = im.size
    for h in range(0,height-k):
      for w in range(0,width-k):
        im2 = im.crop((w,h,w + k,h + k))
        r = image_to_list(im2)
        out_list.append(r)
  except Exception as e:
    print("image_to_ngrams exception reason:",e)
    return out_list
  return out_list

def save_list_of_images(data, size, image_mode, destination_dir, file_prefix, ext):
  # check destination directory exists, if not create it:
  if not os.path.exists(destination_dir):
    print("Creating %s directory." % destination_dir)
    os.makedirs(destination_dir)

  count = 0
  for image_list in data:
    try:
      if image_mode == "RGB":
        im = list_to_rgb_image(image_list, size)
      else:
        im = list_to_l_image(image_list, size)
      im.save("%s/%s-%s.%s" % (destination_dir, file_prefix, count, ext))
      count += 1
    except Exception as e:
      print("save_list_of_images exception reason:",e)
      continue


def replace_with_feature(image_features, image_list):
  best_match = image_list
  best_score = 0
  for feature in image_features:
    similarity = rescaled_list_simm(feature, image_list)
    if similarity > best_score:
      best_match = feature
      best_score = similarity
  return best_match


# this function could do with a huge tidy!!
def phi_transform_image(im, image_features, image_mode, ngram_size):
  try:
    width, height = im.size
    if image_mode == "L":
      arr = numpy.zeros((height,width),numpy.float)
    elif image_mode == "RGB":
      arr = numpy.zeros((height,width,3),numpy.float)

    count = 0                        # +1 or not to +1??
    for h in range(0,height - ngram_size + 1):                            # yeah, we are effectively calculating image ngrams twice,
      for w in range(0,width - ngram_size + 1):                           # once here, and once up above. fix?
        count += 1
        im2 = im.crop((w, h, w + ngram_size, h + ngram_size))
        image_ngram = image_to_list(im2)

        our_image = replace_with_feature(image_features, image_ngram)     # this is the whole point of this function!
        our_image = rescale(our_image)                                    # rescale back to [0,255]

        if image_mode == "L":
          phi_im = list_to_l_image(our_image, ngram_size)
          im3 = Image.new('L',(width,height),"white")
        elif image_mode == "RGB":
          phi_im = list_to_rgb_image(our_image, ngram_size)
          im3 = Image.new('RGB',(width,height),"white")
        im3.paste(phi_im, (w,h))
        image_array = numpy.array(im3, dtype=numpy.float)
        arr += image_array

        # see what we have:
#        phi_im.show()
#        return im3
        
    arr = arr/count                   # average the final array
    arr = rescale(arr)                # rescale to [0,255]
    arr=numpy.array(numpy.round(arr),dtype=numpy.uint8) # Round values in array and cast to integer

    # Generate final image
    if image_mode == "L":
      out=Image.fromarray(arr, mode="L")
    elif image_mode == "RGB":
      out=Image.fromarray(arr, mode="RGB")
    return out
  except Exception as e:
    print("phi_transform_image exception reason:", e)


# test what we have so far:
# Yup, works!
#im = Image.open("220px-Lenna.png")
#im = Image.open("angelina-jolie-5-800.jpg")
#im2 = edge_enhance(im, enhance_factor)
#im2.show()
#data = image_to_ngrams(im, 20)
#save_list_of_images(data, 20, "RGB", saved_features_dir, "small-lenna", "png")

#image_ngrams = image_to_ngrams(im2, ngram_size)
#image_features = list_average_categorize(image_ngrams, threshold)
#save_list_of_images(image_features, ngram_size, "RGB", saved_features_dir, "angelina-features", "png")
#sys.exit(0)

#phi_im = phi_transform_image(im2, image_features, image_mode, ngram_size)
#final_im = edge_enhance(phi_im, enhance_factor)
#final_im.show()


# edge-transform an image:
def edge_transform(im, enhance_factor_pre, enhance_factor_post, ngram_size, threshold, image_mode, saved_features_dir):
  im2 = edge_enhance(im, enhance_factor_pre)
  im2.show()

  image_ngrams = image_to_ngrams(im2, ngram_size)
  image_features = list_average_categorize(image_ngrams, threshold)
  save_list_of_images(image_features, ngram_size, image_mode, saved_features_dir, "features", "png")

  phi_im = phi_transform_image(im2, image_features, image_mode, ngram_size)
  phi_im.show()

  final_im = edge_enhance(phi_im, enhance_factor_post)
  final_im.show()
  return final_im


im = Image.open(filename)
im.thumbnail((300,300))
im.show()
final_im = edge_transform(im, enhance_factor_pre, enhance_factor_post, ngram_size, threshold, image_mode, saved_features_dir)

