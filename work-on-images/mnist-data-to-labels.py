#!c:/Python34/python.exe

#######################################################################
# load the labels from csv into sw
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-05-12
# Update:
# Copyright: GPLv3
#
# Usage: ./mnist-data-to-labels.py
#
#######################################################################

import os
import sys

from PIL import Image

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("delete me")

# for now, assume they exist, without testing it:
source = "work-on-handwritten-digits/mnist_test_labels.csv"
#destination = "work-on-handwritten-digits/train-images/"
#source = "work-on-handwritten-digits/mnist_test_images.csv"
#destination = "work-on-handwritten-digits/test-images/"

with open(source,'r') as f:
  for line in f:
    line = line.strip()
    if len(line) == 0:
      continue
    for k,label in enumerate(line.split(',')):
      image_ket = ket("image: mnist-test-image-" + str(k+1))
      context.learn("test-label",image_ket,label)
context.print_universe()
context.save("sw-examples/mnist-test-labels.sw")
sys.exit(0)

count = 0
with open(source,'r') as f:
  for line in f:
    line = line.strip()
    if len(line) == 0:
      continue
    count += 1
    if count > k:
      break
    data = [ 255 - int(x) for x in line.split(',')]
    size = (28,28)     # standard MNIST data-set size
    im = Image.new('L',size)
    im.putdata(data)
#    im.save(destination + "mnist-test-image-%s.bmp" % count)
    im.save(destination + "mnist-train-image-%s.bmp" % count)
