#!c:/Python34/python.exe

#######################################################################
# edge enhance the given image
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-03-05
# Update: 
# Copyright: GPLv3
#
# Usage: ./image_edge_enhance_v2.py image.{png,jpg} [enhance-factor]
#
# eg: ./image_edge_enhance_v2.py Lenna.png
# eg: ./image_edge_enhance_v2.py Lenna.png 40
#
#######################################################################


import sys
from PIL import Image                 # if this line bugs out, you need to install Pillow, a python image library.

if len(sys.argv) < 2:
  print("\nUsage:")
  print("  ./image_edge_enhance_v2.py image.{png,jpg} [enhance-factor]")
  sys.exit(1)
filename = sys.argv[1]

try:
  enhance_factor = int(sys.argv[2])
except:
  enhance_factor = 20                  # set default to 20 iterations of smooth

try:
  im = Image.open(filename)
except:
  print("couldn't open image file:",filename)
  sys.exit(1)

# implements a Gaussian smooth.
# the 1D version: f[k] -> f[k-1]/4 + f[k]/2 + f[k+1]/4 rapidly approaches a bell curve if you apply it several times.
# image_smooth() implements a 2D version of that equation.
#
def image_smooth(image):
  def smooth_pixel(image,w,h):
    pix = image.load()
    r = pix[w-1,h-1][0]/16 + pix[w,h-1][0]/16 + pix[w+1,h-1][0]/16 + pix[w-1,h][0]/16 + pix[w,h][0]/2 + pix[w+1,h][0]/16 + pix[w-1,h+1][0]/16 + pix[w,h+1][0]/16 + pix[w+1,h+1][0]/16
    g = pix[w-1,h-1][1]/16 + pix[w,h-1][1]/16 + pix[w+1,h-1][1]/16 + pix[w-1,h][1]/16 + pix[w,h][1]/2 + pix[w+1,h][1]/16 + pix[w-1,h+1][1]/16 + pix[w,h+1][1]/16 + pix[w+1,h+1][1]/16
    b = pix[w-1,h-1][2]/16 + pix[w,h-1][2]/16 + pix[w+1,h-1][2]/16 + pix[w-1,h][2]/16 + pix[w,h][2]/2 + pix[w+1,h][2]/16 + pix[w-1,h+1][2]/16 + pix[w,h+1][2]/16 + pix[w+1,h+1][2]/16
    return (int(r),int(g),int(b))

  width = image.size[0]
  height = image.size[1]
  im2 = image.crop((-1,-1,width + 1,height + 1))
#  im2.show()

  out_image = Image.new('RGB',(width,height))
  pixels = out_image.load()
  for h in range(height):
    for w in range(width):
      pixels[w,h] = smooth_pixel(im2,w+1,h+1)
#  out_image.show()
  return out_image


def old_edge_enhance(image,k):
  def pixel_difference(im1,im2,w,h):
    def massage_pixel(x):
      if x < 0:
        x = 0
      x *= 20
      x = int(x)
      if x > 255:
        x = 255
      return 255 - x

    pix1 = im1.load()
    pix2 = im2.load()
    r = pix1[w,h][0] - pix2[w,h][0]
    g = pix1[w,h][1] - pix2[w,h][1]
    b = pix1[w,h][2] - pix2[w,h][2]

    r = massage_pixel(r)
    g = massage_pixel(g)
    b = massage_pixel(b)
  
    return (r,g,b)

  smoothed_image = image
  for _ in range(k):
    smoothed_image = image_smooth(smoothed_image)
  smoothed_image.show()

  width = image.size[0]
  height = image.size[1]

  out_image = Image.new('RGB',(width,height))
  pixels = out_image.load()
  for h in range(height):
    for w in range(width):
      pixels[w,h] = pixel_difference(smoothed_image,image,w,h)
  return out_image


# the old_edge_enhance() had a subtle bug.
# because image_smooth() was returning an integer based image at each iteration, small features ended up being lost!
# So I had to completely re-implement the thing, but this time allowing floats at each iteration of smooth.
# This had a massive improvement in quality.
# The old way also seemed to converge, in that if you applied k above some threshold, any larger k didn't seem to make much difference.
# Now, larger k has a noticable improvement.
# Very happy with the results this thing spits out!!
#
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


im2 = edge_enhance(im,enhance_factor)
im2.show()

# now save it:
filename, ext = filename.rsplit('.',1)
filename = filename + "--edge-enhanced-" + str(enhance_factor) + "." + ext
im2.save(filename)

