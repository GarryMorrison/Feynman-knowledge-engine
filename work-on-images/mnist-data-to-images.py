#!c:/Python34/python.exe

#######################################################################
# map mnist csv to actual images
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-04-10
# Update:
# Copyright: GPLv3
#
# Usage: ./mnist-data-to-images.py how-many-to-process
#
#######################################################################

import os
import sys

from PIL import Image

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("...")

try:
  k = int(sys.argv[1])
except:
  print("\nUsage: ./mnist-data-to-images.py how-many-to-process")
  sys.exit(1)

# for now, assume they exist, without testing it:
#source = "work-on-handwritten-digits/mnist_train_images.csv"
#destination = "work-on-handwritten-digits/train-images/"
source = "work-on-handwritten-digits/mnist_test_images.csv"
destination = "work-on-handwritten-digits/test-images/"


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
    im.save(destination + "mnist-test-image-%s.bmp" % count)
#    im.save(destination + "mnist-train-image-%s.bmp" % count)
