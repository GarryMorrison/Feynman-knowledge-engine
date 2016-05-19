#!c:/Python34/python.exe

#######################################################################
# map mnist csv to label averaged images
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-5-19
# Update:
# Copyright: GPLv3
#
# Usage: ./mnist-data-to-average-images.py
#
#######################################################################

import os
import sys
import numpy
from PIL import Image

# for now, assume they exist, without testing it:
source = "work-on-handwritten-digits/mnist_train_images.csv"
label_source = "work-on-handwritten-digits/mnist_train_labels.csv"

#source = "work-on-handwritten-digits/mnist_test_images.csv"
#label_source = "work-on-handwritten-digits/mnist_test_labels.csv"

destination = "work-on-handwritten-digits/label-average-images/"

# learn the labels:
with open(label_source,'r') as f:
  for line in f:
    line = line.strip()
    if len(line) == 0:
      continue
    labels = line.split(',')
    break
print("labels:",labels)
#sys.exit(0)

digit_arrays = {}
digit_counts = [0,0,0,0,0,0,0,0,0,0]

# learn the average digits:
count = 0
with open(source,'r') as f:
  for line in f:
    line = line.strip()
    if len(line) == 0:
      continue
    data = [ 255 - int(x) for x in line.split(',')]
    r = numpy.array(data,dtype=numpy.float).reshape(28,28)
    digit_label = labels[count]
    if digit_label not in digit_arrays:
      digit_arrays[digit_label] = r
    else:
      digit_arrays[digit_label] = digit_arrays[digit_label] + r
    digit_counts[int(digit_label)] += 1

    count += 1

# have a quick look at what we have:
print("digit counts:",digit_counts)
print("0:",digit_arrays['0'])


# output the average digits:
for digit_label in ['0','1','2','3','4','5','6','7','8','9']:
  arr = digit_arrays[digit_label]

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
  out.show()
#  out.save(destination + "mnist-test-%s.bmp" % digit_label)
  out.save(destination + "mnist-train-%s.bmp" % digit_label)
