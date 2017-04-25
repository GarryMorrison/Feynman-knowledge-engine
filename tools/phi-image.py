#!c:/Python34/python.exe

#######################################################################
# apply edge-enhance, phi-transform, then phi-image to an image
# this might work as a first layer in image recognition
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-12-7
# Update: 2017-4-25
# Copyright: GPLv3
#
# Usage: ./phi-image.py image.{png,jpg}
#
#######################################################################

import os
import sys
from PIL import Image                 # if this line bugs out, you need to install Pillow, a python image library.
import numpy

#filename = "child.png"
#filename = "220px-Lenna.png"
#filename = "portman.jpg"
#filename = "work-on-handwritten-digits/phi-transformed-images-v2--10k-test--edge-enhanced-20/mnist-test-image-403--edge-enhanced-20.png"
filename = "work-on-handwritten-digits/phi-transformed-images-v2--10k-test--edge-enhanced-20/mnist-test-image-396--edge-enhanced-20.png"
#filename = "work-on-handwritten-digits/phi-transformed-images-v2--10k-test--edge-enhanced-20/mnist-test-image-394--edge-enhanced-20.png"
filename = "work-on-handwritten-digits/phi-transformed-images-v2--10k-test--edge-enhanced-20/mnist-test-image-402--edge-enhanced-20.png"


enhance_factor_pre = 40              # image edge enhance factor before phi-transform
enhance_factor_post = 40             # image edge enhance factor after phi-transform
#ngram_size = 10                      # image tile size
#threshold = 0.4                      # average categorize threshold
ngram_size = 4
threshold = 0.9
image_mode = "L"                    # switch between RGB and L mode
#image_mode = "RGB"
saved_features_dir = "saved_average_categorize_features-im"
saved_features_dir2 = "saved_average_categorize_features2-im"


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

def edge_enhance_mode_L(image,k):
  width,height = image.size
  original_pixels = image.load()

  # create an image with a 1*1 border:
  border_image = image.crop((-1,-1,width + 1,height + 1))
  border_pixels = border_image.load()

  # load the border_image into a matrix:
  Matrix = [[border_pixels[w,h] for w in range(width+2)] for h in range(height+2)]

  def smooth_pixel(M,w,h):
    r = M[h-1][w-1]/16 + M[h][w-1]/16 + M[h+1][w-1]/16 + M[h-1][w]/16 + M[h][w]/2 + M[h+1][w]/16 + M[h-1][w+1]/16 + M[h][w+1]/16 + M[h+1][w+1]/16
    return r

  # smooth our image matrix:
  # NB: we have to work with matrices and not images because we need to preserve floats at each step of smooth. Otherwise it harms the algo.
  # first, define a work-space matrix:
  new_Matrix = [[0 for w in range(width+2)] for h in range(height+2)]

  # smooth k times:
  for _ in range(k):
    for h in range(height):
      for w in range(width):
        new_Matrix[h+1][w+1] = smooth_pixel(Matrix,w+1,h+1)
    Matrix = new_Matrix

  def massage_pixel(x):
    if x < 0:
      x = 0
    x *= 20
    x = int(x)
    if x > 255:
      x = 255
    return 255 - x

  # output the final matrix into image form:
  out_image = Image.new('L',(width,height))
  pixels = out_image.load()
  for h in range(height):
    for w in range(width):
      pix = massage_pixel(Matrix[h+1][w+1] - original_pixels[w,h])

      pixels[w,h] = pix
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

def pixel_to_l_image(pix):
  im = Image.new('L',(1,1))
  im.putdata([pix])
  return im

def image_to_ngrams(im,k):
  out_list = []
  try:
    width,height = im.size
    for h in range(0,height):
      for w in range(0,width):
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

def replace_with_feature_index(image_features, image_list):
  best_k = 0
  best_score = 0
  for k, feature in enumerate(image_features):
    similarity = rescaled_list_simm(feature, image_list)
    if similarity > best_score:
      best_k = k
      best_score = similarity
#  return 255 - int( 255 * best_k / (len(image_features)-1) )            # shift to make_phi_image() later?
#  if best_k == 255:
#    print("##: len(image_features) %s" % len(image_features) )
#  print("##: best_k %s" % best_k )
  return best_k


def make_phi_image(im, image_features, ngram_size):
  try:
    width, height = im.size
    im3 = Image.new('L',(width,height),"white")
    pix = im3.load()
    for h in range(0, height):                            # yeah, we are effectively calculating image ngrams twice,
      for w in range(0, width):                           # once here, and once up above. fix?
        im2 = im.crop((w, h, w + ngram_size, h + ngram_size))
        image_ngram = image_to_list(im2)
        pixel = replace_with_feature_index(image_features, image_ngram)     # this is the whole point of this function!
        pix[w, h] = pixel                                                   # currently assumes pixel is in [0,255]
        print("##: pixel: %s" % pixel )
    return im3
  except Exception as e:
    print("make_phi_image exception reason:", e)

im = Image.open(filename)
im.show()
#im2 = edge_enhance(im, enhance_factor_pre)
#im2 = edge_enhance_mode_L(im, 10)
#im2.show()
#sys.exit(0)

image_ngrams = image_to_ngrams(im, ngram_size)
image_features = list_average_categorize(image_ngrams, threshold)
save_list_of_images(image_features, ngram_size, image_mode, saved_features_dir, "features", "png")
phi_im = make_phi_image(im, image_features, ngram_size)
phi_im.show()
#r1 = image_to_list(im)
#r2 = image_to_list(phi_im)
#print(r1)
#print(r2)

#sys.exit(0)
#im2 = edge_enhance_mode_L(phi_im, 3)
#im2.show()
#r3 = image_to_list(im2)
#print(r3)
#sys.exit(0)

image_ngrams2 = image_to_ngrams(phi_im, ngram_size)
image_features2 = list_average_categorize(image_ngrams2, threshold)
save_list_of_images(image_features2, ngram_size, 'L', saved_features_dir2, "features", "png")
phi_im2 = make_phi_image(phi_im, image_features2, ngram_size)
phi_im2.show()


image_ngrams3 = image_to_ngrams(phi_im2, ngram_size)
image_features3 = list_average_categorize(image_ngrams3, threshold)
#save_list_of_images(image_features3, ngram_size, 'L', saved_features_dir3, "features", "png")
phi_im3 = make_phi_image(phi_im2, image_features3, ngram_size)
phi_im3.show()


image_ngrams4 = image_to_ngrams(phi_im3, ngram_size)
image_features4 = list_average_categorize(image_ngrams4, threshold)
#save_list_of_images(image_features4, ngram_size, 'L', saved_features_dir4, "features", "png")
phi_im4 = make_phi_image(phi_im3, image_features3, ngram_size)
phi_im4.show()


r1 = image_to_list(im)
r2 = image_to_list(phi_im)
r3 = image_to_list(phi_im2)
r4 = image_to_list(phi_im3)
r5 = image_to_list(phi_im4)
print(r1)
print(r2)
print(r3)
print(r4)
print(r5)

#final_im = edge_enhance(phi_im, 20)
#final_im.show()


sys.exit(0)
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


#im = Image.open(filename)
#final_im = edge_transform(im, enhance_factor_pre, enhance_factor_post, ngram_size, threshold, image_mode, saved_features_dir)

